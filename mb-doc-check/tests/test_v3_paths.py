import importlib.util, os, subprocess, tempfile, unittest
os.environ["MB_DOC_CHECK_TODAY"] = "2030-01-02"
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

OS = "/mnt/c/mybizz/mybizz-os-docs"; CFG = "/mnt/c/mybizz/mybizz-config-docs"; GOV = "/home/dev-p/memory-governor"
FILES = [OS + "/os-reference-docs/frontmatter conventions.md", OS + "/os-reference-docs/page.md", OS + "/operating-procedures/daily-ops.md",
         CFG + "/gbrain/gbrain-config.md", GOV + "/registers/register-memory-governor.md"]

def pipe(text, frm=OS + "/os-reference-docs/page.md"):
    c = m.Corpus([OS, CFG, GOV], live_files=FILES, obs_files=[OS + "/obsolete/old doc.md"])
    t = m.unwrap(text); t, _ = m.convert_plain_links(t, frm, c); t, _ = m.wrap(t, frm, c)
    t, ch, un = m.convert_pasted_paths(t, frm, c)
    return t, ch, un

class Pasted(unittest.TestCase):
    def setUp(self):
        os.environ["MB_DOC_CHECK_ANYPATH"] = "0"
        m.SOURCES = m.SourceMap({"os": OS, "cfg": CFG, "gov": GOV})
    def tearDown(self): m.SOURCES = m.SourceMap()
    FC = "[[[os:os-reference-docs/frontmatter-conventions]]](frontmatter%20conventions.md)"
    def test_windows_path_with_a_space(self):
        t, ch, un = pipe("see C:\\mybizz\\mybizz-os-docs\\os-reference-docs\\frontmatter conventions.md now\n")
        self.assertEqual(t, f"see {self.FC} now\n"); self.assertEqual(len(ch), 1)
    def test_lowercase_drive_and_forward_slashes(self):
        self.assertEqual(pipe("see c:/mybizz/mybizz-os-docs/os-reference-docs/frontmatter conventions.md.\n")[0], f"see {self.FC}.\n")
    def test_case_does_not_matter_on_windows(self):
        self.assertEqual(pipe("C:\\MyBizz\\MYBIZZ-OS-DOCS\\OS-reference-docs\\Frontmatter Conventions.md\n")[0], self.FC + "\n")
    def test_linux_path(self):
        self.assertEqual(pipe("at /mnt/c/mybizz/mybizz-os-docs/os-reference-docs/frontmatter conventions.md, then\n")[0], f"at {self.FC}, then\n")
    def test_file_url(self):
        self.assertEqual(pipe("file:///C:/mybizz/mybizz-os-docs/os-reference-docs/frontmatter%20conventions.md\n")[0], self.FC + "\n")
    def test_wsl_network_path_to_a_document_outside_c(self):
        t, ch, un = pipe("\\\\wsl.localhost\\Ubuntu\\home\\dev-p\\memory-governor\\registers\\register-memory-governor.md\n")
        self.assertEqual(t, "[[gov:registers/register-memory-governor]]\n")          # no clickable path exists outside the C: drive
    def test_relative_paths(self):
        t, ch, un = pipe("a ../operating-procedures/daily-ops.md and b operating-procedures/daily-ops.md and c ../../mybizz-config-docs/gbrain/gbrain-config.md\n")
        D = "[[[os:operating-procedures/daily-ops]]](../operating-procedures/daily-ops.md)"
        self.assertEqual(t, f"a {D} and b {D} and c [[[cfg:gbrain/gbrain-config]]](../../mybizz-config-docs/gbrain/gbrain-config.md)\n")
    def test_anchor_is_kept(self):
        t, _, _ = pipe("see /mnt/c/mybizz/mybizz-os-docs/operating-procedures/daily-ops.md#Sync for it\n")
        self.assertEqual(t, "see [[[os:operating-procedures/daily-ops#Sync]]](../operating-procedures/daily-ops.md) for it\n")
    def test_code_is_never_touched(self):
        s = "a `C:\\mybizz\\mybizz-os-docs\\operating-procedures\\daily-ops.md` b\n```\n/mnt/c/mybizz/mybizz-os-docs/operating-procedures/daily-ops.md\n```\n"
        self.assertEqual(pipe(s)[0], s)
    def test_paths_inside_existing_links_are_not_converted_twice(self):
        t, ch, un = pipe("[the ops](C:\\mybizz\\mybizz-os-docs\\operating-procedures\\daily-ops.md) and [[C:\\mybizz\\mybizz-os-docs\\operating-procedures\\daily-ops.md|Ops]]\n")
        D = "(../operating-procedures/daily-ops.md)"
        self.assertEqual(t, f"[[[os:operating-procedures/daily-ops|the ops]]]{D} and [[[os:operating-procedures/daily-ops|Ops]]]{D}\n"); self.assertEqual(ch, [])
    def test_a_path_that_points_nowhere_is_left_and_reported(self):
        s = "see C:\\mybizz\\mybizz-os-docs\\nowhere\\ghost.md and docs/ghost.md\n"
        t, ch, un = pipe(s); self.assertEqual(t, s); self.assertEqual(len(un), 2)
    def test_bare_file_names_and_urls_are_not_paths(self):
        s = "the AGENTS.md pointer, daily-ops.md, https://github.com/x/operating-procedures/daily-ops.md and e.g. a/b.\n"
        t, ch, un = pipe(s); self.assertEqual(t, s); self.assertEqual(un, [])
    def test_path_into_obsolete_is_linked(self):
        t, _, _ = pipe("was /mnt/c/mybizz/mybizz-os-docs/obsolete/old doc.md\n")
        self.assertEqual(t, "was [[[os:obsolete/old-doc]]](../obsolete/old%20doc.md)\n")
    def test_second_pass_changes_nothing(self):
        once, _, _ = pipe("see C:\\mybizz\\mybizz-os-docs\\operating-procedures\\daily-ops.md\n"); self.assertEqual(pipe(once)[0], once)
    def test_two_paths_in_one_line(self):
        t, ch, un = pipe("C:\\mybizz\\mybizz-os-docs\\operating-procedures\\daily-ops.md and C:\\mybizz\\mybizz-config-docs\\gbrain\\gbrain-config.md\n")
        self.assertEqual(len(ch), 2); self.assertNotIn("C:\\", t)

class InHook(unittest.TestCase):
    def test_commit_converts_a_pasted_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = os.path.realpath(tmp); os.environ["MB_DOC_CHECK_ANYPATH"] = "1"; self.addCleanup(lambda: (os.environ.pop("MB_DOC_CHECK_ANYPATH", None), setattr(m, "SOURCES", m.SourceMap())))
            run = lambda *a: subprocess.run(["git", "-C", d, *a], check=True, capture_output=True, text=True).stdout
            run("init", "-q"); run("config", "user.email", "t@t"); run("config", "user.name", "t")
            os.makedirs(os.path.join(d, "docs"))
            for n in ("target doc", "x"):
                with open(os.path.join(d, "docs", n + ".md"), "w") as f: f.write(f'---\ntitle: "{n}"\ndoc-id: "mb-0000000{len(n)}"\nupdated: "2030-01-02"\n---\n')
            with open(os.path.join(d, "docs", "page.md"), "w") as f: f.write(f'---\ntitle: "page"\ndoc-id: "mb-00000099"\n---\nsee {d}/docs/target doc.md and `{d}/docs/x.md` and {d}/docs/ghost.md\n')
            run("add", "-A"); m.SOURCES = m.SourceMap({"s": d})
            rep = m.run_hook(d, [])
            body = open(os.path.join(d, "docs", "page.md")).read().split("---\n", 2)[2]
            self.assertEqual(body, f"see [[[s:docs/target-doc]]](target%20doc.md) and `{d}/docs/x.md` and {d}/docs/ghost.md\n")
            self.assertEqual(len(rep.pasted_converted), 1); self.assertEqual(len(rep.pasted_unresolved), 1)


class ReportDetail(unittest.TestCase):
    def test_all_lists_every_pasted_path_and_the_repositories_linked_to(self):
        import io
        from contextlib import redirect_stdout
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["MB_DOC_CHECK_ANYPATH"] = "1"; self.addCleanup(lambda: (os.environ.pop("MB_DOC_CHECK_ANYPATH", None), setattr(m, "SOURCES", m.SourceMap())))
            b = os.path.realpath(tmp); A = os.path.join(b, "A"); B = os.path.join(b, "B"); os.makedirs(A); os.makedirs(B)
            for d_, n in ((A, "x"), (A, "y"), (B, "far")):
                with open(os.path.join(d_, n + ".md"), "w") as f: f.write(f'---\ntitle: "{n}"\ndoc-id: "mb-0000000{len(n)}{ord(n[0])%10}"\n---\n')
            with open(os.path.join(A, "page.md"), "w") as f:
                f.write(f'---\ntitle: "page"\ndoc-id: "mb-00000077"\n---\n[[y]] [[far]] and {A}/x.md and {A}/ghost.md\n')
            m.SOURCES = m.SourceMap({"a": A, "b": B})
            buf = io.StringIO()
            with redirect_stdout(buf): m.cmd_links_report(m.build_parser().parse_args(["links-report", "--all"]))
            out = buf.getvalue()
            self.assertIn("links to other repositories go to: b 1", out)
            self.assertIn("pasted document paths that WOULD BECOME LINKS (1)", out); self.assertIn("page.md line 5:", out)
            self.assertIn("pasted paths LEFT AS TEXT", out); self.assertIn("ghost.md", out)
            buf2 = io.StringIO()
            with redirect_stdout(buf2): m.cmd_links_report(m.build_parser().parse_args(["links-report"]))
            self.assertNotIn("WOULD BECOME LINKS", buf2.getvalue())

if __name__ == "__main__": unittest.main()
