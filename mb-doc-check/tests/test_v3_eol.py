import importlib.util, io, os, subprocess, tempfile, unittest
from contextlib import redirect_stdout
os.environ["MB_DOC_CHECK_TODAY"] = "2030-01-02"
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class Repo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.d = os.path.realpath(self.tmp.name)
        self.g = lambda *a: subprocess.run(["git", "-C", self.d, *a], check=True, capture_output=True, text=True).stdout
        self.g("init", "-q"); self.g("config", "user.email", "t@t"); self.g("config", "user.name", "t"); self.g("config", "core.autocrlf", "false")
        m.SOURCES = m.SourceMap({"s": self.d}, eol="lf"); os.environ["MB_DOC_CHECK_ANYPATH"] = "1"
    def tearDown(self): self.tmp.cleanup(); m.SOURCES = m.SourceMap(); os.environ.pop("MB_DOC_CHECK_ANYPATH", None)
    def w(self, n, data):
        os.makedirs(os.path.dirname(os.path.join(self.d, n)) or self.d, exist_ok=True)
        with open(os.path.join(self.d, n), "wb") as f: f.write(data)
    def r(self, n):
        with open(os.path.join(self.d, n), "rb") as f: return f.read()
    def commit(self, day):
        os.environ["MB_DOC_CHECK_TODAY"] = day; self.g("add", "-A"); rep = m.run_hook(self.d, []); self.g("commit", "-qm", day, "--no-verify"); return rep
    FM = b'---\r\ntitle: "a"\r\ndoc-id: "mb-00000001"\r\nupdated: "2030-01-02"\r\n---\r\nline one\r\nline two\r\n'

class Hook(Repo):
    def test_a_crlf_document_is_committed_with_lf(self):
        self.w("a.md", self.FM); self.g("add", "-A"); self.g("commit", "-qm", "old", "--no-verify")
        self.w("a.md", self.FM + b"a real new line\r\n"); rep = self.commit("2031-05-05")
        got = self.r("a.md"); self.assertNotIn(b"\r", got); self.assertIn(b"a real new line\n", got)
        self.assertEqual(self.g("show", "HEAD:a.md").count("\r"), 0)
    def test_a_mixed_document_becomes_uniform(self):
        self.w("a.md", b'---\r\ntitle: "a"\r\ndoc-id: "mb-00000001"\r\n---\nbody line\r\nmore\n'); self.commit("2030-01-02")
        self.assertNotIn(b"\r", self.r("a.md"))
    def test_a_line_ending_change_alone_does_not_move_the_date(self):
        self.w("a.md", self.FM); self.g("add", "-A"); self.g("commit", "-qm", "old", "--no-verify")
        buf = io.StringIO()
        with redirect_stdout(buf): m.cmd_eol(m.build_parser().parse_args(["eol", "--repo", self.d, "--write"]))   # nothing but the CRLF changes
        rep = self.commit("2035-09-09")
        got = self.r("a.md").decode(); self.assertIn('updated: "2030-01-02"', got); self.assertNotIn("\r", got)
        self.assertEqual(self.g("show", "--stat", "--format=", "HEAD").count("a.md"), 1)
    def test_a_real_change_in_a_crlf_document_moves_the_date_and_converts(self):
        self.w("a.md", self.FM); self.g("add", "-A"); self.g("commit", "-qm", "old", "--no-verify")
        self.w("a.md", self.FM.replace(b"line two", b"line two changed")); self.commit("2035-09-09")
        got = self.r("a.md").decode(); self.assertIn('updated: "2035-09-09"', got); self.assertNotIn("\r", got)
    def test_skill_md_keeps_its_line_endings(self):
        raw = b"---\r\nname: x\r\ndescription: y\r\n---\r\nBody\r\n"; self.w("s/SKILL.md", raw); self.commit("2030-01-02")
        self.assertEqual(self.r("s/SKILL.md"), raw)
    def test_without_the_setting_nothing_changes(self):
        m.SOURCES = m.SourceMap({"s": self.d}, eol="keep")
        self.w("a.md", self.FM); self.commit("2030-01-02"); self.assertIn(b"\r\n", self.r("a.md"))
    def test_lf_documents_are_untouched(self):
        raw = b'---\ntitle: "a"\ndoc-id: "mb-00000001"\nupdated: "2030-01-02"\n---\nbody\n'; self.w("a.md", raw); self.commit("2030-01-02"); self.assertEqual(self.r("a.md"), raw)

class Command(Repo):
    def run_(self, *a):
        buf = io.StringIO()
        with redirect_stdout(buf): rc = m.cmd_eol(m.build_parser().parse_args(["eol", "--repo", self.d, *a]))
        return rc, buf.getvalue()
    def setUp(self):
        super().setUp()
        self.w("lf.md", b"a\nb\n"); self.w("crlf.md", b"a\r\nb\r\n"); self.w("mixed.md", b"a\r\nb\nc\r\n"); self.w("s/SKILL.md", b"a\r\nb\r\n")
        self.g("add", "-A"); self.g("commit", "-qm", "base", "--no-verify")
    def test_dry_run_counts_and_changes_nothing(self):
        rc, out = self.run_(); self.assertIn("with LF: 1", out); self.assertIn("with CRLF: 1", out); self.assertIn("mix of both: 1", out)
        self.assertEqual(self.r("crlf.md"), b"a\r\nb\r\n"); self.assertIn("dry run", out)
    def test_write_converts_documents_but_not_skill_files(self):
        rc, out = self.run_("--write"); self.assertEqual(self.r("crlf.md"), b"a\nb\n"); self.assertEqual(self.r("mixed.md"), b"a\nb\nc\n")
        self.assertEqual(self.r("s/SKILL.md"), b"a\r\nb\r\n"); self.assertEqual(self.r("lf.md"), b"a\nb\n")
    def test_refuses_a_dirty_repository(self):
        self.w("new.md", b"x"); rc, out = self.run_("--write"); self.assertEqual(rc, 1)

if __name__ == "__main__": unittest.main()
