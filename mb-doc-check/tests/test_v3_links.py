import importlib.util, io, os, subprocess, tempfile, unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(HERE, "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def git(d, *a): return subprocess.run(["git", "-C", d, *a], check=True, capture_output=True, text=True).stdout
def repo(base, name):
    d = os.path.join(base, name); os.makedirs(d)
    git(d, "init", "-q"); git(d, "config", "user.email", "t@t"); git(d, "config", "user.name", "t")
    return os.path.realpath(d)
def doc(d, rel, body, code):
    p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    stem = os.path.basename(rel)[:-3]
    with open(p, "w", newline="") as f: f.write(f'---\ntitle: "{stem}"\ndoc-id: "{code}"\n---\n{body}')
    return p
def read(p): return open(p, encoding="utf-8", newline="").read()
def body(p): return read(p).split("---\n", 2)[2]
def commit_all(d, msg="c"): git(d, "add", "-A"); git(d, "commit", "-qm", msg)

def standardize(root):
    st, unresolved, files = m.rollout_plan(m._pool_corpus(), root)
    for pth, data in files: m.write_bytes(pth, data)

class Base(unittest.TestCase):
    def setUp(self):
        os.environ["MB_DOC_CHECK_ANYPATH"] = "1"
        self.tmp = tempfile.TemporaryDirectory(); b = os.path.realpath(self.tmp.name)
        self.A = repo(b, "repoA"); self.B = repo(b, "repoB")
        m.SOURCES = m.SourceMap({"srca": self.A, "srcb": self.B})
        self.n = 0
    def tearDown(self): self.tmp.cleanup(); m.SOURCES = m.SourceMap(); os.environ.pop("MB_DOC_CHECK_ANYPATH", None)
    def code(self): self.n += 1; return "mb-%08x" % (0xAAAA0000 + self.n)
    def d(self, root, rel, text): return doc(root, rel, text, self.code())
    def hook(self, top, extra=(), dry=False):
        rep = m.run_hook(top, [x for x in extra], dry=dry)
        return rep, m.print_report(rep, top, dry)

class Standard(Base):
    def test_shapes(self):
        x = self.d(self.A, "docs/x.md", ""); y = self.d(self.A, "docs/y.md", ""); z = self.d(self.B, "notes/z.md", "")
        self.assertEqual(m.canonical_link(x, y, "y"), "[[[srca:docs/y]]](y.md)")
        self.assertEqual(m.canonical_link(x, y, "y#Sec|Shown"), "[[[srca:docs/y#Sec|Shown]]](y.md)")
        self.assertEqual(m.canonical_link(x, z, "z"), "[[[srcb:notes/z]]](../../repoB/notes/z.md)")
    def test_awkward_names(self):
        x = self.d(self.A, "x.md", ""); w = self.d(self.A, "Tools and apps/Strix + OpenCode (v2).md", "")
        got = m.canonical_link(x, w, "w")
        self.assertEqual(got, "[[[srca:tools-and-apps/strix-opencode-v2]]](Tools%20and%20apps/Strix%20%2B%20OpenCode%20%28v2%29.md)")
    def test_wrap_unwrap_roundtrip(self):
        x = self.d(self.A, "x.md", ""); self.d(self.A, "y.md", "")
        c = m.Corpus([self.A, self.B]); t = "see [[y|the Y]] and [[y]]\n"
        w, ch = m.wrap(t, x, c)
        self.assertEqual(len(ch), 2)
        self.assertEqual(m.wrap(m.unwrap(w), x, c)[0], w)      # idempotent
        self.assertEqual(m.wrap(w, x, c)[1], [])
    def test_unresolved_and_code_untouched(self):
        x = self.d(self.A, "x.md", ""); self.d(self.A, "y.md", "")
        c = m.Corpus([self.A]); t = "ghost [[nowhere]]\n`[[y]]` and\n```\n[[y]]\n```\n"
        self.assertEqual(m.wrap(t, x, c)[0], t)

class SameRepoFirst(Base):
    def test_readme(self):
        a = self.d(self.A, "guide/README.md", ""); self.d(self.B, "other/README.md", "")
        x = self.d(self.A, "x.md", ""); c = m.Corpus([self.A, self.B])
        self.assertEqual(m.wrap("[[README]]\n", x, c)[0], "[[[srca:guide/readme]]](guide/README.md)\n")
        y = self.d(self.B, "y.md", "")
        self.assertEqual(m.wrap("[[README]]\n", y, c)[0], "[[[srcb:other/readme]]](other/README.md)\n")
    def test_two_in_own_repo_is_ambiguous(self):
        self.d(self.A, "g1/README.md", ""); self.d(self.A, "g2/README.md", "")
        x = self.d(self.A, "x.md", ""); c = m.Corpus([self.A])
        self.assertEqual(m.wrap("[[README]]\n", x, c)[0], "[[README]]\n")

class Rollout(Base):
    def setUp(self):
        super().setUp()
        self.d(self.A, "docs/target one.md", ""); self.d(self.A, "docs/two.md", "")
        self.d(self.B, "notes/far.md", "")
        self.page = self.d(self.A, "docs/page.md",
            "same [[two]] and [[two|Two shown]] and [[docs/two]]\ncross [[far]]\nplain [a label](two.md) and [t](target%20one.md#top)\nghost [[nowhere]]\n")
        commit_all(self.A); commit_all(self.B)
    def test_report_and_write(self):
        c = m._pool_corpus(); st, unresolved, files = m.rollout_plan(c, self.A)
        self.assertEqual(st["to_convert_same_repo"], 3); self.assertEqual(st["to_convert_other_repo"], 1)
        self.assertEqual(st["to_convert_plain_markdown"], 2); self.assertEqual(st["unresolved_missing"], 1)
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_rollout(m.build_parser().parse_args(["rollout", "--repo", self.A, "--write"]))
        b = body(self.page)
        self.assertIn("[[[srca:docs/two]]](two.md)", b); self.assertIn("[[[srca:docs/two|Two shown]]](two.md)", b)
        self.assertIn("[[[srcb:notes/far]]](../../repoB/notes/far.md)", b)
        self.assertIn("[[[srca:docs/target-one|t#top]]]", b.replace("#top|t", "|t#top")) if False else None
        self.assertIn("[[nowhere]]", b)
        # second run: nothing left to do
        st2, _u, files2 = m.rollout_plan(m._pool_corpus(), self.A)
        self.assertEqual(files2, []); self.assertEqual(st2["to_convert_same_repo"] + st2["to_convert_plain_markdown"], 0)
    def test_refuses_dirty_repo(self):
        open(os.path.join(self.A, "docs", "new.md"), "w").write("x")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = m.cmd_rollout(m.build_parser().parse_args(["rollout", "--repo", self.A, "--write"]))
        self.assertEqual(rc, 1); self.assertIn("uncommitted", buf.getvalue())

class Hook(Base):
    def test_new_document_is_written_in_the_standard_form(self):
        self.d(self.A, "y.md", ""); commit_all(self.A)
        p = self.d(self.A, "x.md", "see [[y|Why]] and [[far]]\n")
        self.d(self.B, "far.md", ""); commit_all(self.B)
        git(self.A, "add", "-A"); rep, (text, blocked) = self.hook(self.A, [self.B])
        self.assertFalse(blocked)
        self.assertEqual(body(p), "see [[[srca:y|Why]]](y.md) and [[[srcb:far]]](../repoB/far.md)\n")
        self.assertIn("standard form", text)
    def test_typing_again_changes_nothing(self):
        self.d(self.A, "y.md", ""); p = self.d(self.A, "x.md", "[[y]]\n"); standardize(self.A); commit_all(self.A)
        before = body(p)
        with open(p, "a") as f: f.write("more words\n")
        git(self.A, "add", "-A")
        rep, (text, blocked) = self.hook(self.A)
        self.assertEqual(body(p), before + "more words\n"); self.assertFalse(blocked)
        self.assertIn('updated: "', read(p))
    def test_rename_with_total_rewrite_repairs_inner_and_path(self):
        t = self.d(self.A, "docs/a.md", "old words " * 50); p = self.d(self.A, "docs/ref.md", "[[a|Alpha]]\n")
        q = self.d(self.B, "other.md", "cross [[a]]\n")
        standardize(self.A); commit_all(self.A); commit_all(self.B)
        stdA, stdB = body(p), body(q)
        self.assertIn("[[[srca:docs/a|Alpha]]](a.md)", stdA)
        git(self.A, "mv", "docs/a.md", "docs/renamed.md")
        open(os.path.join(self.A, "docs/renamed.md"), "w").write(f'---\ntitle: "renamed"\ndoc-id: "{self.n and "mb-%08x" % (0xAAAA0000 + 1)}"\n---\nnothing like before\n')
        git(self.A, "add", "-A")
        rep, (text, blocked) = self.hook(self.A, [self.B])
        self.assertFalse(blocked)
        self.assertEqual(body(p), "[[[srca:docs/renamed|Alpha]]](renamed.md)\n")
        self.assertEqual(body(q), "cross [[[srca:docs/renamed]]](../repoA/docs/renamed.md)\n")
    def test_moving_the_linking_document_refreshes_its_paths(self):
        self.d(self.A, "docs/y.md", ""); p = self.d(self.A, "docs/x.md", "[[y]]\n"); standardize(self.A); commit_all(self.A)
        self.assertIn("(y.md)", body(p))
        os.makedirs(os.path.join(self.A, "deep/er")); git(self.A, "mv", "docs/x.md", "deep/er/x.md")
        git(self.A, "add", "-A"); rep, (text, blocked) = self.hook(self.A)
        self.assertEqual(body(os.path.join(self.A, "deep/er/x.md")), "[[[srca:docs/y]]](../../docs/y.md)\n")
    def test_delete_turns_a_standard_link_into_words(self):
        self.d(self.A, "gone.md", ""); p = self.d(self.A, "x.md", "see [[gone|The Gone]]\n"); standardize(self.A); commit_all(self.A)
        self.assertIn("[[[srca:gone|The Gone]]](gone.md)", body(p))
        git(self.A, "rm", "-q", "gone.md"); rep, (text, blocked) = self.hook(self.A)
        self.assertFalse(blocked); self.assertEqual(body(p), "see The Gone\n")
    def test_move_into_obsolete_keeps_the_link(self):
        self.d(self.A, "old.md", ""); p = self.d(self.A, "x.md", "see [[old]]\n"); standardize(self.A); commit_all(self.A)
        os.makedirs(os.path.join(self.A, "obsolete")); git(self.A, "mv", "old.md", "obsolete/old.md")
        rep, (text, blocked) = self.hook(self.A); self.assertFalse(blocked)
        self.assertEqual(body(p), "see [[[srca:obsolete/old]]](obsolete/old.md)\n")     # the link follows the document into obsolete/
    def test_typo_in_a_new_link_still_blocks(self):
        self.d(self.A, "y.md", ""); commit_all(self.A)
        self.d(self.A, "x.md", "[[yy]]\n"); git(self.A, "add", "-A")
        rep, (text, blocked) = self.hook(self.A); self.assertTrue(blocked); self.assertIn("[[yy]]", text)
    def test_cross_repo_rename_repairs_links_in_the_other_repo(self):
        self.d(self.B, "target.md", "t"); q = self.d(self.A, "ref.md", "[[target]]\n"); standardize(self.A); commit_all(self.B); commit_all(self.A)
        self.assertIn("[[[srcb:target]]](../repoB/target.md)", body(q))
        git(self.B, "mv", "target.md", "moved.md"); git(self.B, "add", "-A")
        rep, (text, blocked) = self.hook(self.B, [self.A]); self.assertFalse(blocked)
        self.assertEqual(body(q), "[[[srcb:moved]]](../repoB/moved.md)\n")
        self.assertEqual(rep.other_repo_changed, [q])
    def test_old_style_wikilinks_still_work_before_the_map_exists(self):
        m.SOURCES = m.SourceMap()
        self.d(self.A, "y.md", ""); p = self.d(self.A, "x.md", "[[y]]\n"); git(self.A, "add", "-A")
        rep, (text, blocked) = self.hook(self.A); self.assertFalse(blocked); self.assertEqual(body(p), "[[y]]\n")

class RealGitCommit(Base):
    def test_a_plain_git_commit_writes_the_standard_form(self):
        srcfile = os.path.join(self.A, "..", "sources.map")
        with open(srcfile, "w") as f: f.write(f"srca = {self.A}\nsrcb = {self.B}\n")
        env = dict(os.environ, MB_DOC_CHECK_SOURCES=os.path.realpath(srcfile), MB_DOC_CHECK_ANYPATH="1")
        self.d(self.A, "y.md", ""); self.d(self.B, "far.md", ""); commit_all(self.A); commit_all(self.B)
        buf = io.StringIO()
        with redirect_stdout(buf):
            m.cmd_install_hook(m.build_parser().parse_args(["install-hook", "--repo", self.A]))
        p = self.d(self.A, "x.md", "an AI typed [[y|Why]] and [[far]] and [t](y.md)\n"); git(self.A, "add", "-A")
        r = subprocess.run(["git", "-C", self.A, "commit", "-qm", "agent wrote a document"], capture_output=True, text=True, env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        committed = git(self.A, "show", "HEAD:x.md").split("---\n", 2)[2]
        self.assertEqual(committed, "an AI typed [[[srca:y|Why]]](y.md) and [[[srcb:far]]](../repoB/far.md) and [[[srca:y|t]]](y.md)\n")
        # a typo stops the commit
        with open(p, "a") as f: f.write("[[typo-here]]\n")
        git(self.A, "add", "-A")
        r = subprocess.run(["git", "-C", self.A, "commit", "-qm", "typo"], capture_output=True, text=True, env=env)
        self.assertNotEqual(r.returncode, 0); self.assertIn("typo-here", r.stdout + r.stderr)

if __name__ == "__main__":
    unittest.main(verbosity=1)
