import importlib.util
import io
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(HERE, "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

A1, A2, A3, A4 = "mb-aaaaaaa1", "mb-aaaaaaa2", "mb-aaaaaaa3", "mb-aaaaaaa4"


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], check=True, capture_output=True, text=True).stdout


def repo():
    d = os.path.realpath(tempfile.mkdtemp())
    git(d, "init", "-q")
    git(d, "config", "user.email", "t@t")
    git(d, "config", "user.name", "t")
    return d


def doc(d, rel, body, code=None, title=True):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    stem = os.path.basename(rel)[:-3]
    fm = ""
    if code or title:
        fm = "---\n" + ('title: "%s"\n' % stem if title else "") + ('doc-id: "%s"\n' % code if code else "") + "---\n"
    with open(p, "w", newline="") as f:
        f.write(fm + body)
    return p


def read(p):
    with open(p, "rb") as f:
        return f.read().decode()


def commit_all(d, msg="c"):
    git(d, "add", "-A")
    git(d, "commit", "-qm", msg)


def hook(d, extra=(), dry=False, delete_ok=False):
    rep = m.run_hook(d, list(extra), dry=dry, delete_ok=delete_ok)
    return rep, m.print_report(rep, d, dry)


class Renames(unittest.TestCase):
    def test_rename_plus_total_rewrite_still_repairs_links(self):
        d = repo()
        doc(d, "a.md", "old text " * 50, A1)
        ref = doc(d, "ref.md", "one [[a|Alpha]] two [[a#sec]] three [[a.md]]\n", A2)
        commit_all(d)
        git(d, "mv", "a.md", "renamed.md")
        with open(os.path.join(d, "renamed.md"), "w") as f:
            f.write('---\ntitle: "renamed"\ndoc-id: "%s"\n---\nCompletely different words here.\n' % A1)
        git(d, "add", "-A")
        self.assertNotIn("R", git(d, "diff", "--cached", "-M", "--name-status").split()[0])  # git itself lost the rename
        rep, (text, blocked) = hook(d)
        self.assertFalse(blocked)
        self.assertEqual(read(ref).split("---\n", 2)[2], "one [[renamed|Alpha]] two [[renamed#sec]] three [[renamed]]\n")
        self.assertIn("ref.md", git(d, "diff", "--cached", "--name-only"))

    def test_move_between_folders_rewrites_path_links_only(self):
        d = repo()
        doc(d, "docs/note.md", "x\n", A1)
        ref = doc(d, "ref.md", "[[docs/note]] and [[note]]\n", A2)
        commit_all(d)
        git(d, "mv", "docs/note.md", "new/note.md") if os.makedirs(os.path.join(d, "new")) is None else None
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertFalse(blocked)
        self.assertTrue(read(ref).endswith("[[new/note]] and [[note]]\n"))

    def test_legacy_files_without_codes_use_git_rename(self):
        d = repo()
        doc(d, "a.md", "same body line\n" * 5, None)
        ref = doc(d, "ref.md", "[[a]]\n", None)
        commit_all(d)
        git(d, "mv", "a.md", "b.md")
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertFalse(blocked)
        self.assertTrue(read(ref).endswith("[[b]]\n"))
        self.assertRegex(read(os.path.join(d, "b.md")), r'doc-id: "mb-[0-9a-f]{8}"')

    def test_rename_by_hand_pasting_code_into_new_file(self):
        d = repo()
        doc(d, "old.md", "x\n", A1)
        ref = doc(d, "ref.md", "[[old]]\n", A2)
        commit_all(d)
        os.remove(os.path.join(d, "old.md"))
        doc(d, "fresh.md", "y\n", A1)
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertFalse(blocked)
        self.assertTrue(read(ref).endswith("[[fresh]]\n"))


class SameNames(unittest.TestCase):
    def test_new_same_name_file_makes_old_links_specific(self):
        d = repo()
        doc(d, "guide/README.md", "g\n", A1)
        ref = doc(d, "ref.md", "[[README]] and [[guide/README]]\n", A2)
        commit_all(d)
        doc(d, "other/README.md", "o\n", A3)
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertFalse(blocked)
        self.assertTrue(read(ref).endswith("[[guide/README]] and [[guide/README]]\n"))

    def test_new_link_to_shared_name_is_blocked(self):
        d = repo()
        doc(d, "guide/README.md", "g\n", A1)
        doc(d, "other/README.md", "o\n", A3)
        commit_all(d)
        doc(d, "ref.md", "see [[README]]\n", A2)
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertTrue(blocked)
        self.assertIn("shared by several", text)


class Deletions(unittest.TestCase):
    def setUp(self):
        self.d = repo()
        doc(self.d, "a.md", "x\n", A1)
        self.ref = doc(self.d, "ref.md", "[[a|Alpha]] and [[a]] and [[a#s]]\n", A2)
        commit_all(self.d)

    def test_pure_delete_turns_links_into_words(self):
        os.remove(os.path.join(self.d, "a.md"))
        git(self.d, "add", "-A")
        rep, (text, blocked) = hook(self.d)
        self.assertFalse(blocked)
        self.assertTrue(read(self.ref).endswith("Alpha and a and a\n"))

    def test_delete_plus_new_file_is_unclear_and_stops(self):
        os.remove(os.path.join(self.d, "a.md"))
        doc(self.d, "brandnew.md", "z\n", None)
        git(self.d, "add", "-A")
        before = read(self.ref)
        rep, (text, blocked) = hook(self.d)
        self.assertTrue(blocked)
        self.assertIn(A1, text)
        self.assertIn("MB_DELETE_OK=1", text)
        self.assertEqual(read(self.ref), before)

    def test_delete_ok_switch_converts(self):
        os.remove(os.path.join(self.d, "a.md"))
        doc(self.d, "brandnew.md", "z\n", None)
        git(self.d, "add", "-A")
        rep, (text, blocked) = hook(self.d, delete_ok=True)
        self.assertFalse(blocked)
        self.assertTrue(read(self.ref).endswith("Alpha and a and a\n"))

    def test_move_into_obsolete_keeps_links_and_does_not_stop(self):
        os.makedirs(os.path.join(self.d, "obsolete"))
        git(self.d, "mv", "a.md", "obsolete/a.md")
        before = read(self.ref)
        rep, (text, blocked) = hook(self.d)
        self.assertFalse(blocked)
        self.assertEqual(read(self.ref), before)


class Codes(unittest.TestCase):
    def test_new_documents_get_title_and_code(self):
        d = repo()
        doc(d, "seed.md", "s\n", A1)
        commit_all(d)
        p = doc(d, "new.md", "# hi\n", None, title=False)
        with open(p, "w") as f:
            f.write("# hi\n")
        git(d, "add", "-A")
        hook(d)
        self.assertRegex(read(p), r'^---\ntitle: "new"\ndoc-id: "mb-[0-9a-f]{8}"\nupdated: "\d{4}-\d\d-\d\d"\n---\n# hi\n$')

    def test_copy_gets_new_code_original_keeps_its_own(self):
        d = repo()
        orig = doc(d, "orig.md", "body\n", A1)
        commit_all(d)
        cp = doc(d, "copy.md", "body\n", A1)
        git(d, "add", "-A")
        hook(d)
        self.assertIn(A1, read(orig))
        self.assertNotIn(A1, read(cp))
        self.assertRegex(read(cp), r'doc-id: "mb-[0-9a-f]{8}"')

    def test_lost_frontmatter_gets_its_code_back(self):
        d = repo()
        p = doc(d, "a.md", "body\n", A1)
        commit_all(d)
        with open(p, "w") as f:
            f.write("agent rewrote everything and dropped the frontmatter\n")
        git(d, "add", "-A")
        hook(d)
        self.assertIn('doc-id: "%s"' % A1, read(p))

    def test_skill_md_and_empty_files_untouched(self):
        d = repo()
        doc(d, "seed.md", "s\n", A1)
        commit_all(d)
        with open(os.path.join(d, "SKILL.md"), "w") as f:
            f.write("# skill\n")
        with open(os.path.join(d, "empty.md"), "w") as f:
            f.write("   \n")
        git(d, "add", "-A")
        hook(d)
        self.assertEqual(read(os.path.join(d, "SKILL.md")), "# skill\n")
        self.assertEqual(read(os.path.join(d, "empty.md")), "   \n")

    def test_existing_frontmatter_kept_except_code_line(self):
        d = repo()
        doc(d, "seed.md", "s\n", A1)
        commit_all(d)
        p = os.path.join(d, "x.md")
        with open(p, "w", newline="") as f:
            f.write('---\r\ntitle: "Custom"\r\ntype: note\r\n---\r\nbody\r\n')
        git(d, "add", "-A")
        hook(d)
        out = read(p)
        self.assertTrue(out.startswith('---\r\ntitle: "Custom"\r\ntype: note\r\ndoc-id: "mb-'))
        self.assertTrue(out.endswith('"\r\n---\r\nbody\r\n'))


class Gate(unittest.TestCase):
    def test_new_dangling_blocks_old_dangling_does_not(self):
        d = repo()
        doc(d, "ref.md", "old [[ghost1]]\n", A1)
        commit_all(d)
        with open(os.path.join(d, "ref.md"), "a") as f:
            f.write("only ordinary words added\n")
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertFalse(blocked)
        with open(os.path.join(d, "ref.md"), "a") as f:
            f.write("brand new [[ghost2]]\n")
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertTrue(blocked)
        self.assertIn("ghost2", text)
        self.assertNotIn("ghost1]] points", text)

    def test_link_to_file_already_in_obsolete_is_fine(self):
        d = repo()
        doc(d, "obsolete/dead.md", "d\n", A1)
        commit_all(d)
        doc(d, "ref.md", "history: [[dead]]\n", A2)
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertFalse(blocked)

    def test_broken_frontmatter_blocks(self):
        d = repo()
        doc(d, "seed.md", "s\n", A1)
        commit_all(d)
        with open(os.path.join(d, "bad.md"), "w") as f:
            f.write("---\ntitle: x\nnever closed\n")
        git(d, "add", "-A")
        rep, (text, blocked) = hook(d)
        self.assertTrue(blocked)

    def test_unstaged_edits_left_alone(self):
        d = repo()
        doc(d, "a.md", "x\n", A1)
        ref = doc(d, "ref.md", "[[a]]\n", A2)
        commit_all(d)
        with open(ref, "a") as f:
            f.write("unstaged words\n")
        git(d, "mv", "a.md", "b.md")
        before = read(ref)
        rep, (text, blocked) = hook(d)
        self.assertEqual(read(ref), before)
        self.assertIn(ref, rep.skipped_unstaged)

    def test_dry_run_changes_nothing(self):
        d = repo()
        doc(d, "a.md", "x\n", A1)
        ref = doc(d, "ref.md", "[[a]]\n", A2)
        commit_all(d)
        git(d, "mv", "a.md", "b.md")
        git(d, "add", "-A")
        before = read(ref)
        rep, (text, blocked) = hook(d, dry=True)
        self.assertEqual(read(ref), before)
        self.assertIn("nothing was changed", text)
        self.assertEqual(len(rep.repointed), 1)


class CrossRepo(unittest.TestCase):
    def test_rename_in_one_repo_fixes_links_in_another(self):
        b = repo()
        a = repo()
        doc(b, "target.md", "t\n", A1)
        ref = doc(a, "ref.md", "[[target]]\n", A2)
        commit_all(b)
        commit_all(a)
        git(b, "mv", "target.md", "moved.md")
        git(b, "add", "-A")
        rep, (text, blocked) = hook(b, extra=[a])
        self.assertFalse(blocked)
        self.assertTrue(read(ref).endswith("[[moved]]\n"))
        self.assertEqual(rep.other_repo_changed, [ref])
        self.assertIn("OTHER repositories", text)
        self.assertEqual(git(a, "diff", "--cached", "--name-only"), "")  # not silently staged in the other repo

    def test_link_to_other_repo_is_not_a_false_alarm(self):
        b = repo()
        a = repo()
        doc(b, "target.md", "t\n", A1)
        commit_all(b)
        doc(a, "ref.md", "[[target]]\n", A2)
        git(a, "add", "-A")
        rep, (text, blocked) = hook(a, extra=[b])
        self.assertFalse(blocked)


class Commands(unittest.TestCase):
    def test_migrate_dry_and_real(self):
        d = repo()
        legacy = doc(d, "a.md", "x\n", "a")  # old-style doc-id equal to stem
        none = os.path.join(d, "b.md")
        with open(none, "w") as f:
            f.write("# no frontmatter\n")
        crlf = os.path.join(d, "c.md")
        with open(crlf, "w", newline="") as f:
            f.write('---\r\ntitle: "c"\r\n---\r\nbody\r\n')
        keep = doc(d, "k.md", "x\n", A1)
        obs = doc(d, "obsolete/o.md", "x\n", None)
        skill = os.path.join(d, "SKILL.md")
        with open(skill, "w") as f:
            f.write("---\nname: s\ndescription: d\n---\nbody\n")
        snap = {p: read(p) for p in (legacy, none, crlf, keep, obs, skill)}
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_migrate(m.build_parser().parse_args(["migrate", "--root", d]))
        self.assertEqual(snap, {p: read(p) for p in snap})
        with redirect_stdout(buf):
            m.cmd_migrate(m.build_parser().parse_args(["migrate", "--root", d, "--write"]))
        self.assertRegex(read(legacy), r'doc-id: "mb-[0-9a-f]{8}"')
        self.assertNotIn('doc-id: "a"', read(legacy))
        self.assertTrue(read(none).startswith('---\ntitle: "b"\ndoc-id: "mb-'))
        self.assertTrue(read(crlf).startswith('---\r\ntitle: "c"\r\ndoc-id: "mb-'))
        self.assertEqual(read(keep), snap[keep].replace('doc-id: "mb-aaaaaaa1"\n', 'doc-id: "mb-aaaaaaa1"\nupdated: "%s"\n' % m.today_str()))   # keeps code and title, gains the date
        self.assertEqual(read(obs), snap[obs])
        self.assertEqual(read(skill), snap[skill])
        codes = [m.read_id(read(p).encode()) for p in (legacy, none, crlf, keep)]
        self.assertEqual(len(set(codes)), 4)

    def test_check_reports(self):
        d = repo()
        doc(d, "a.md", "[[ghost]] [[dup]]\n", A1)
        doc(d, "x/dup.md", "1\n", A2)
        doc(d, "y/dup.md", "2\n", A3)
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_check(m.build_parser().parse_args(["check", "--root", d]))
        out = buf.getvalue()
        self.assertIn("point to no document: 1", out)
        self.assertIn("shared by several documents: 1", out)

    def test_check_resolves_links_into_other_folders_and_reports_only_its_own(self):
        a, b = repo(), repo()
        doc(a, "one.md", "[[elsewhere]] [[ghost]]\n", A1)
        doc(b, "elsewhere.md", "[[alsoghost]]\n", A2)
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_check(m.build_parser().parse_args(["check", "--root", a, "--also-root", b]))
        out = buf.getvalue()
        self.assertIn("point to no document: 1", out)
        self.assertIn("[[ghost]]", out)
        self.assertNotIn("alsoghost", out)
        self.assertNotIn("[[elsewhere]]", out)

    def test_hook_exit_codes_and_internal_errors_never_block(self):
        d = repo()
        doc(d, "seed.md", "s\n", A1)
        commit_all(d)
        doc(d, "ref.md", "[[ghost]]\n", A2)
        git(d, "add", "-A")
        cwd = os.getcwd()
        os.chdir(d)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(m.cmd_hook(m.build_parser().parse_args(["hook", "--dry-run"])), 0)
                self.assertEqual(m.cmd_hook(m.build_parser().parse_args(["hook"])), 1)
            orig = m.run_hook
            m.run_hook = lambda *a, **k: 1 / 0
            try:
                with redirect_stdout(buf):
                    self.assertEqual(m.cmd_hook(m.build_parser().parse_args(["hook"])), 0)
            finally:
                m.run_hook = orig
        finally:
            os.chdir(cwd)


class RealGitCommit(unittest.TestCase):
    def test_commit_is_repaired_or_stopped_by_the_installed_hook(self):
        d = repo()
        doc(d, "a.md", "x\n", A1)
        ref = doc(d, "ref.md", "[[a]]\n", A2)
        commit_all(d)
        self.assertEqual(m.cmd_install_hook(m.build_parser().parse_args(["install-hook", "--repo", d])), 0)
        self.assertEqual(m.cmd_install_hook(m.build_parser().parse_args(["install-hook", "--repo", d])), 1)
        # a rename with a total rewrite, committed with nothing but "git commit"
        git(d, "mv", "a.md", "b.md")
        with open(os.path.join(d, "b.md"), "w") as f:
            f.write('---\ntitle: "b"\ndoc-id: "%s"\n---\nall new words\n' % A1)
        git(d, "add", "-A")
        r = subprocess.run(["git", "-C", d, "commit", "-qm", "rename"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(git(d, "show", "HEAD:ref.md").endswith("[[b]]\n"))
        # a typo in a new link stops the commit
        with open(os.path.join(d, "ref.md"), "a") as f:
            f.write("[[nope]]\n")
        git(d, "add", "-A")
        r = subprocess.run(["git", "-C", d, "commit", "-qm", "typo"], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("nope", r.stdout + r.stderr)



class CodeProtection(unittest.TestCase):
    """The five confirmed damage shapes plus a multi-line inline span: text inside
    inline code must never be converted, even when it names a document or a path."""

    def setUp(self):
        self.d = repo()
        doc(self.d, "agents.md", "a\n", "mb-aaaaaaa1")
        doc(self.d, "architecture.md", "a\n", "mb-aaaaaaa2")
        doc(self.d, "config.md", "c\n", "mb-aaaaaaa3")
        doc(self.d, "anvil.md", "v\n", "mb-aaaaaaa4")
        os.makedirs(os.path.join(self.d, "registers"))
        doc(self.d, "registers/register-memory-governor.md", "r\n", "mb-aaaaaaa5")
        m.SOURCES = m.SourceMap({"r": self.d})

    def tearDown(self):
        m.SOURCES = m.SourceMap()

    def _ref(self, body):
        ref = doc(self.d, "ref.md", body, "mb-aaaaaaa6")
        git(self.d, "add", "-A")
        hook(self.d)
        return read(ref)

    def test_gitignore_style_inline_path_stays_code(self):
        out = self._ref("lines: `graphify-out/`, `.opencode/`, `agents.md`, `opencode.json`\n")
        self.assertIn("`agents.md`", out)
        self.assertNotIn("[[", out)

    def test_bare_schema_name_stays_code(self):
        out = self._ref("schemas: (`common`, `architecture`, `workflow`)\n")
        self.assertIn("`architecture`", out)
        self.assertNotIn("[[", out)

    def test_bare_table_name_stays_code(self):
        out = self._ref("via DB `config` table, unlike `config.json`\n")
        self.assertIn("`config`", out)
        self.assertNotIn("[[", out)

    def test_bare_plugin_name_stays_code(self):
        out = self._ref("plugin name `anvil`, version `1.0.0`\n")
        self.assertIn("`anvil`", out)
        self.assertNotIn("[[", out)

    def test_inline_path_survives_even_when_target_is_deleted(self):
        ref = doc(self.d, "ref.md", "rows in `registers/register-memory-governor.md` ↔ files\n", "mb-aaaaaaa6")
        git(self.d, "add", "-A")
        hook(self.d)
        self.assertIn("`registers/register-memory-governor.md`", read(ref))
        os.remove(os.path.join(self.d, "registers", "register-memory-governor.md"))
        git(self.d, "add", "-A")
        hook(self.d)
        self.assertIn("`registers/register-memory-governor.md`", read(ref))
        self.assertNotIn("register-memory-governor", read(ref).replace("`registers/register-memory-governor.md`", ""))

    def test_multiline_inline_span_stays_code(self):
        out = self._ref("see `gbrain/\nconfig.md` here\n")
        self.assertIn("`gbrain/", out)
        self.assertNotIn("[[", out)



if __name__ == "__main__":
    unittest.main(verbosity=1)
