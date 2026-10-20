import importlib.util, os, subprocess, tempfile, unittest
os.environ["MB_DOC_CHECK_TODAY"] = "2030-01-02"
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
OS = "/mnt/c/mybizz/mybizz-os-docs"; CFG = "/mnt/c/mybizz/mybizz-config-docs"
FILES = [OS + "/os-reference-docs/page.md", CFG + "/gbrain/gbrain-config.md", CFG + "/gbrain/gbrain-reference.md"]

class Tables(unittest.TestCase):
    def setUp(self):
        os.environ.pop("MB_DOC_CHECK_ANYPATH", None)
        m.SOURCES = m.SourceMap({"os": OS, "cfg": CFG}, paths="absolute"); self.c = m.Corpus([OS, CFG], live_files=FILES, obs_files=[]); self.f = FILES[0]
    def tearDown(self): m.SOURCES = m.SourceMap()
    A = "(C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)"
    def test_alias_in_prose_uses_a_plain_pipe(self):
        self.assertEqual(m.wrap("see [[gbrain-config|Config]] now\n", self.f, self.c)[0], f"see [[[cfg:gbrain/gbrain-config|Config]]]{self.A} now\n")
    def test_alias_in_a_table_row_uses_an_escaped_pipe(self):
        t = "| a | [[gbrain-config|Config]] |\n"
        self.assertEqual(m.wrap(t, self.f, self.c)[0], f"| a | [[[cfg:gbrain/gbrain-config\\|Config]]]{self.A} |\n")
    def test_no_alias_in_a_table_row_has_no_pipe_at_all(self):
        self.assertEqual(m.wrap("| a | [[gbrain-config]] |\n", self.f, self.c)[0], f"| a | [[[cfg:gbrain/gbrain-config]]]{self.A} |\n")
    def test_an_already_escaped_link_is_understood_and_left_alone(self):
        t = f"| a | [[[cfg:gbrain/gbrain-config\\|Config]]]{self.A} |\n"; self.assertEqual(m.wrap(t, self.f, self.c), (t, []))
    def test_an_unescaped_standard_link_in_a_table_is_repaired(self):
        t = f"| a | [[[cfg:gbrain/gbrain-config|Config]]]{self.A} |\n"
        self.assertEqual(m.wrap(t, self.f, self.c)[0], f"| a | [[[cfg:gbrain/gbrain-config\\|Config]]]{self.A} |\n")
    def test_an_old_escaped_wikilink_in_a_table_resolves(self):
        self.assertEqual(m.wrap("| a | [[gbrain-config\\|Config]] |\n", self.f, self.c)[0], f"| a | [[[cfg:gbrain/gbrain-config\\|Config]]]{self.A} |\n")
    def test_a_row_indented_or_with_two_links(self):
        t = "  | a | [[gbrain-config|One]] | [[gbrain-reference|Two]] |\n"
        out = m.wrap(t, self.f, self.c)[0]; self.assertEqual(out.count("\\|"), 2); self.assertNotRegex(out, r"(?<!\\)\|One")
    def test_second_pass_changes_nothing(self):
        once = m.wrap("| a | [[gbrain-config|Config]] |\nand [[gbrain-config|Config]]\n", self.f, self.c)[0]
        self.assertEqual(m.wrap(once, self.f, self.c)[1], [])
    def test_unwrap_then_wrap_round_trips_in_a_table(self):
        once = m.wrap("| a | [[gbrain-config|Config]] |\n", self.f, self.c)[0]
        self.assertEqual(m.wrap(m.unwrap(once), self.f, self.c)[0], once)
    def test_prose_of_understands_the_escape(self):
        self.assertEqual(m.prose_of("x\\|Shown words"), "Shown words")
    def test_a_missing_target_inside_a_table_becomes_words(self):
        self.assertEqual(m.prose_of("ghost\\|Ghost words"), "Ghost words")

if __name__ == "__main__": unittest.main()
