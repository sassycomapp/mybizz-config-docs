import importlib.util, io, os, subprocess, tempfile, unittest
from contextlib import redirect_stdout
os.environ["MB_DOC_CHECK_TODAY"] = "2030-01-02"
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def mk(d, rel, body, code):
    p = os.path.join(d, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", newline="") as f: f.write(f'---\ntitle: "{os.path.basename(rel)[:-3]}"\ndoc-id: "{code}"\n---\n{body}')
    return p
def rd(p):
    with open(p, newline="") as f: return f.read().split("---\n", 2)[2]

class Base(unittest.TestCase):
    def setUp(self):
        os.environ["MB_DOC_CHECK_ANYPATH"] = "1"
        self.tmp = tempfile.TemporaryDirectory(); b = os.path.realpath(self.tmp.name)
        self.A = os.path.join(b, "A"); self.B = os.path.join(b, "B"); os.makedirs(self.A); os.makedirs(self.B)
        for d in (self.A, self.B):
            subprocess.run(["git", "-C", d, "init", "-q"], check=True); subprocess.run(["git", "-C", d, "config", "user.email", "t@t"]); subprocess.run(["git", "-C", d, "config", "user.name", "t"])
        m.SOURCES = m.SourceMap({"a": self.A, "b": self.B}); self.n = 0
    def tearDown(self): self.tmp.cleanup(); m.SOURCES = m.SourceMap(); os.environ.pop("MB_DOC_CHECK_ANYPATH", None)
    def code(self): self.n += 1; return "mb-%08x" % (0xBBBB0000 + self.n)
    def commit(self, d): subprocess.run(["git", "-C", d, "add", "-A"], check=True); subprocess.run(["git", "-C", d, "commit", "-qm", "c", "--no-verify"], check=True, capture_output=True)

class CaseInsensitive(Base):
    def test_lower_case_name_finds_an_upper_case_file(self):
        mk(self.A, "AGENTS.md", "x", self.code()); x = mk(self.A, "x.md", "", self.code())
        c = m.Corpus([self.A, self.B]); t, ch = m.wrap("see [[agents|the rules]]\n", x, c)
        self.assertEqual(t, "see [[[a:agents|the rules]]](AGENTS.md)\n")
    def test_exact_case_wins_when_both_exist(self):
        mk(self.A, "one/README.md", "", self.code()); mk(self.B, "two/readme.md", "", self.code()); x = mk(self.B, "x.md", "", self.code())
        c = m.Corpus([self.A, self.B]); self.assertEqual(m.resolve(m.parse_wikilink("README"), c, x)[1], [os.path.join(self.A, "one/README.md")])
    def test_several_files_differing_only_in_case_are_ambiguous(self):
        mk(self.A, "AGENTS.md", "", self.code()); mk(self.B, "Agents.md", "", self.code()); x = mk(self.A, "x.md", "", self.code())
        c = m.Corpus([self.A, self.B]); st, hits = m.resolve(m.parse_wikilink("agents"), c, x)
        self.assertEqual(st, "ok"); self.assertEqual(hits, [os.path.join(self.A, "AGENTS.md")])      # the linking document's own repository wins
        y = mk(self.A.replace("/A", "/C") if False else os.path.join(os.path.dirname(self.A), "C"), "y.md", "", self.code())
        c2 = m.Corpus([self.A, self.B, os.path.dirname(y)]); self.assertEqual(m.resolve(m.parse_wikilink("agents"), c2, y)[0], "ambiguous")
    def test_a_typed_path_in_the_wrong_case_resolves(self):
        mk(self.A, "Docs/Target One.md", "", self.code()); x = mk(self.A, "x.md", "", self.code())
        c = m.Corpus([self.A]); t, ch, un = m.convert_pasted_paths(f"see {self.A.upper()}/docs/target one.md now\n", x, c)
        self.assertEqual(len(ch), 1)

class SelfReference(Base):
    def test_a_document_naming_its_own_path_is_left_alone(self):
        p = mk(self.A, "specs/spec-bft.md", f"Location: specs/spec-bft.md and {self.A}/specs/spec-bft.md\n", self.code())
        c = m.Corpus([self.A]); t, ch, un = m.convert_pasted_paths(open(p).read(), p, c)
        self.assertEqual(ch, []); self.assertEqual(t, open(p).read())
    def test_a_path_to_another_document_still_becomes_a_link(self):
        mk(self.A, "specs/spec-bft.md", "", self.code()); p = mk(self.A, "stepwise/step-1.md", "Read specs/spec-bft.md first\n", self.code())
        c = m.Corpus([self.A]); t, ch, un = m.convert_pasted_paths(open(p).read(), p, c); self.assertEqual(len(ch), 1)

class ProseFromDisplay(unittest.TestCase):
    def test_ellipsis_display_uses_the_name(self):
        self.assertEqual(m.prose_of("docs-manager-README|…"), "docs-manager-README")
        self.assertEqual(m.prose_of("agents|mb-3-cs"), "mb-3-cs")
        self.assertEqual(m.prose_of("x|..."), "x"); self.assertEqual(m.prose_of("AGENTS|AGENTS.md"), "AGENTS.md")

class FixBroken(Base):
    def setUp(self):
        super().setUp()
        self.x = mk(self.A, "x.md", "ok [[far]] | gone [[agents|mb-3-cs]] | gone2 [[pdlf-register|pdlf-register]] | dots [[old-readme|…]] | ambiguous [[dup]] | code `[[ghost]]`\n", self.code())
        mk(self.B, "far.md", "", self.code()); mk(self.A, "p/dup.md", "", self.code()); mk(self.A, "q/dup.md", "", self.code())
        self.commit(self.A); self.commit(self.B)
    def run_(self, *a):
        buf = io.StringIO()
        with redirect_stdout(buf): rc = m.cmd_fix_broken(m.build_parser().parse_args(["fix-broken", "--repo", self.A, *a]))
        return rc, buf.getvalue()
    def test_dry_run_changes_nothing_and_lists_everything(self):
        before = open(self.x).read(); rc, out = self.run_()
        self.assertEqual(open(self.x).read(), before); self.assertIn("mb-3-cs   [missing]", out); self.assertIn("dry run", out)
        self.assertIn("NOT touched", out)
    def test_write_turns_missing_links_into_words_only(self):
        rc, out = self.run_("--write"); b = rd(self.x)
        self.assertEqual(b, "ok [[far]] | gone mb-3-cs | gone2 pdlf-register | dots old-readme | ambiguous [[dup]] | code `[[ghost]]`\n")
    def test_include_ambiguous(self):
        self.run_("--write", "--include-ambiguous"); self.assertIn("ambiguous dup |", rd(self.x))
    def test_refuses_a_dirty_repository(self):
        open(os.path.join(self.A, "new.md"), "w").write("x"); rc, out = self.run_("--write"); self.assertEqual(rc, 1); self.assertIn("STOP", out)
    def test_then_the_rollout_has_nothing_left_that_cannot_be_converted(self):
        self.run_("--write", "--include-ambiguous"); self.commit(self.A)
        st, unresolved, files = m.rollout_plan(m.Corpus([self.A, self.B]), self.A)
        self.assertEqual(unresolved, [])


class AmbiguousMessage(Base):
    def test_the_blocked_commit_tells_the_writer_which_names_to_use(self):
        mk(self.A, "AGENTS.md", "", self.code()); mk(self.B, "AGENTS.md", "", self.code())
        c = os.path.join(os.path.dirname(self.A), "C"); os.makedirs(c)
        subprocess.run(["git", "-C", c, "init", "-q"]); subprocess.run(["git", "-C", c, "config", "user.email", "t@t"]); subprocess.run(["git", "-C", c, "config", "user.name", "t"])
        m.SOURCES = m.SourceMap({"a": self.A, "b": self.B, "c": c})
        mk(c, "x.md", "see [[agents]]\n", self.code())
        subprocess.run(["git", "-C", c, "add", "-A"], check=True)
        rep = m.run_hook(c, [self.A, self.B]); text, blocked = m.print_report(rep, c, False)
        self.assertTrue(blocked); self.assertIn("[[a:agents]]", text); self.assertIn("[[b:agents]]", text)

class CheckCountsOnlyRealWork(Base):
    def test_check_reports_zero_after_a_rollout_and_the_right_number_before(self):
        mk(self.A, "y.md", "", self.code()); mk(self.A, "x.md", "see [[y]] and [[y|Why]]\n", self.code()); self.commit(self.A)
        def nonstd():
            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf): m.cmd_check(m.build_parser().parse_args(["check", "--root", self.A]))
            line = [l for l in buf.getvalue().splitlines() if "standard form" in l][0]
            return int(line.rsplit(":", 1)[1])
        self.assertEqual(nonstd(), 2)
        st, un, files = m.rollout_plan(m.Corpus([self.A, self.B]), self.A)
        for pth, data in files: m.write_bytes(pth, data)
        self.assertEqual(nonstd(), 0)

class SameFolderListedTwice(Base):
    def test_a_repository_in_both_the_roots_file_and_the_sources_file_is_not_ambiguous(self):
        mk(self.B, "far.md", "", self.code()); x = mk(self.A, "x.md", "see [[[b:far]]](%s/far.md) and [[far]]\n" % self.B, self.code())
        c = m.Corpus([self.A, self.B, self.B, self.A, self.B])
        self.assertEqual(len(c.live_files), 2)
        self.assertEqual(m.resolve(m.parse_wikilink("b:far"), c, x)[0], "ok")
        self.assertEqual(m.resolve(m.parse_wikilink("far"), c, x)[0], "ok")
    def test_a_commit_with_the_roots_file_and_the_sources_file_both_listing_the_repositories(self):
        mk(self.B, "far.md", "", self.code()); self.commit(self.B)
        x = mk(self.A, "x.md", "see [[far]] and [[far|Far]]\n", self.code()); subprocess.run(["git", "-C", self.A, "add", "-A"], check=True)
        os.environ["MB_DOC_CHECK_ROOTS"] = os.pathsep.join([self.A, self.B])
        try:
            rep = m.run_hook(self.A, m.load_roots_file() + list(m.SOURCES.by_id.values())); text, blocked = m.print_report(rep, self.A, False)
        finally: os.environ.pop("MB_DOC_CHECK_ROOTS")
        self.assertFalse(blocked, text); self.assertIn("[[[b:far]]]", rd(x))

if __name__ == "__main__": unittest.main()
