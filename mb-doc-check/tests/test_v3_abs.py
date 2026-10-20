import importlib.util, os, subprocess, tempfile, unittest
os.environ["MB_DOC_CHECK_TODAY"] = "2030-01-02"
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
OS = "/mnt/c/mybizz/mybizz-os-docs"; CFG = "/mnt/c/mybizz/mybizz-config-docs"; DEF = "/mnt/c/dev/project-library-global"; GOV = "/home/dev-p/memory-governor"

class Absolute(unittest.TestCase):
    def setUp(self): m.SOURCES = m.SourceMap({"os": OS, "cfg": CFG, "default": DEF, "gov": GOV}, paths="absolute")
    def tearDown(self): m.SOURCES = m.SourceMap(); os.environ.pop("MB_DOC_CHECK_ANYPATH", None)
    def test_the_path_part_is_the_full_windows_path_whatever_the_linking_file(self):
        a = m.canonical_link(OS + "/os-reference-docs/page.md", CFG + "/gbrain/gbrain-config.md", "x")
        b = m.canonical_link(DEF + "/deep/er/folder/other.md", CFG + "/gbrain/gbrain-config.md", "x")
        self.assertEqual(a, "[[[cfg:gbrain/gbrain-config]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)"); self.assertEqual(a, b)
    def test_spaces_and_brackets_and_other_drive_folder(self):
        got = m.canonical_link(OS + "/x.md", DEF + "/Tools and apps/Strix + OpenCode (v2).md", "x|Shown")
        self.assertEqual(got, "[[[default:tools-and-apps/strix-opencode-v2|Shown]]](C:/dev/project-library-global/Tools%20and%20apps/Strix%20%2B%20OpenCode%20%28v2%29.md)")
    def test_a_target_outside_the_c_drive_gets_no_path(self):
        self.assertEqual(m.canonical_link(OS + "/x.md", GOV + "/registers/register-memory-governor.md", "x"), "[[gov:registers/register-memory-governor]]")
    def test_switching_the_setting_refreshes_existing_links(self):
        files = [OS + "/os-reference-docs/page.md", CFG + "/gbrain/gbrain-config.md"]
        c = m.Corpus([OS, CFG], live_files=files, obs_files=[])
        rel = "see [[[cfg:gbrain/gbrain-config]]](../../mybizz-config-docs/gbrain/gbrain-config.md)\n"
        t, ch = m.wrap(rel, files[0], c)
        self.assertEqual(t, "see [[[cfg:gbrain/gbrain-config]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)\n"); self.assertEqual(len(ch), 1)
        self.assertEqual(m.wrap(t, files[0], c)[1], [])
    def test_the_setting_is_read_from_the_sources_file(self):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "s.txt"); open(f, "w").write("@paths = absolute\nos = /mnt/c/mybizz/mybizz-os-docs\n")
            os.environ["MB_DOC_CHECK_SOURCES"] = f
            try: s = m.SourceMap.load()
            finally: os.environ.pop("MB_DOC_CHECK_SOURCES")
            self.assertEqual(s.paths, "absolute"); self.assertEqual(list(s.by_id), ["os"])
    def test_unknown_value_falls_back_to_relative(self):
        self.assertEqual(m.SourceMap({"a": "/x"}, paths="whatever").paths, "relative")

if __name__ == "__main__": unittest.main()
