import importlib.util, os, subprocess, tempfile, unittest
os.environ["MB_DOC_CHECK_TODAY"] = "2030-01-02"
spec = importlib.util.spec_from_file_location("mbdc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb-doc-check.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def fm(raw):
    s, lines, o, c = m.fm_state(m._nobom(raw)); return b"".join(lines[o:c + 1]).decode()

class Full(unittest.TestCase):
    def t(self, raw, stem="My File", code="mb-11111111"):
        new, note = m.set_code(raw, stem, code); self.assertEqual(note, "ok"); return new
    def test_no_frontmatter(self):
        self.assertEqual(self.t(b"# Body\n"), b'---\ntitle: "My File"\ndoc-id: "mb-11111111"\nupdated: "2030-01-02"\n---\n# Body\n')
    def test_frontmatter_without_title_gets_one(self):
        out = self.t(b"---\ntags: [a]\nstatus: draft\n---\nBody\n")
        self.assertEqual(out, b'---\ntitle: "My File"\ntags: [a]\nstatus: draft\ndoc-id: "mb-11111111"\n---\nBody\n')
    def test_existing_title_is_never_changed(self):
        raw = b'---\ntitle: "My own words"\ndoc-id: "mb-22222222"\n---\nB\n'
        self.assertEqual(self.t(raw, code="mb-22222222"), raw)
    def test_empty_title_is_filled(self):
        out = self.t(b'---\ntitle:\nnote: x\n---\nB\n')
        self.assertEqual(out, b'---\ntitle: "My File"\nnote: x\ndoc-id: "mb-11111111"\n---\nB\n')
    def test_code_but_no_title_keeps_its_code(self):
        out = self.t(b'---\ndoc-id: "mb-33333333"\nx: 1\n---\nB\n', code="mb-33333333")
        self.assertEqual(out, b'---\ntitle: "My File"\ndoc-id: "mb-33333333"\nx: 1\n---\nB\n')
    def test_crlf_files_keep_their_line_endings(self):
        out = self.t(b"---\r\nx: 1\r\n---\r\nB\r\n")
        self.assertEqual(out, b'---\r\ntitle: "My File"\r\nx: 1\r\ndoc-id: "mb-11111111"\r\n---\r\nB\r\n')
    def test_title_written_as_block_scalar_counts_as_present(self):
        raw = b'---\ntitle: >\n  A long\n  title\n---\nB\n'
        self.assertTrue(m.has_title(raw))
    def test_bom_is_kept(self):
        out = self.t(b"\xef\xbb\xbf---\nx: 1\n---\nB\n"); self.assertTrue(out.startswith(b"\xef\xbb\xbf---"))
        self.assertIn(b'title: "My File"', out)
    def test_second_run_changes_nothing(self):
        once = self.t(b"---\nx: 1\n---\nB\n"); self.assertEqual(self.t(once), once)
    def test_broken_frontmatter_is_refused_not_touched(self):
        new, note = m.set_code(b"---\nx: 1\nno closing line\n", "s", "mb-44444444"); self.assertIsNone(new); self.assertEqual(note, "unclosed")

class Hook(unittest.TestCase):
    def test_commit_completes_a_file_that_has_a_code_but_no_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = os.path.realpath(tmp)
            run = lambda *a: subprocess.run(["git", "-C", d, *a], check=True, capture_output=True, text=True).stdout
            run("init", "-q"); run("config", "user.email", "t@t"); run("config", "user.name", "t")
            with open(os.path.join(d, "a.md"), "w") as f: f.write('---\ndoc-id: "mb-55555555"\n---\nBody\n')
            run("add", "-A"); rep = m.run_hook(d, []); 
            self.assertEqual([os.path.basename(x) for x in rep.titles_added], ["a.md"])
            got = open(os.path.join(d, "a.md")).read()
            self.assertEqual(got, '---\ntitle: "a"\ndoc-id: "mb-55555555"\nupdated: "2030-01-02"\n---\nBody\n')
    def test_skill_md_is_never_touched(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = os.path.realpath(tmp)
            run = lambda *a: subprocess.run(["git", "-C", d, *a], check=True, capture_output=True, text=True).stdout
            run("init", "-q"); run("config", "user.email", "t@t"); run("config", "user.name", "t")
            os.makedirs(os.path.join(d, "s")); raw = "---\nname: x\ndescription: y\n---\nBody\n"
            with open(os.path.join(d, "s", "SKILL.md"), "w") as f: f.write(raw)
            run("add", "-A"); m.run_hook(d, [])
            self.assertEqual(open(os.path.join(d, "s", "SKILL.md")).read(), raw)


class Date(unittest.TestCase):
    def test_added_after_doc_id_when_missing(self):
        out = m.set_updated(b'---\ntitle: "t"\ndoc-id: "mb-1"\nx: 1\n---\nB\n', "2030-01-02")
        self.assertEqual(out, b'---\ntitle: "t"\ndoc-id: "mb-1"\nupdated: "2030-01-02"\nx: 1\n---\nB\n')
    def test_replaced_every_time(self):
        out = m.set_updated(b'---\ntitle: "t"\nupdated: "2020-05-05"\n---\nB\n', "2030-01-02")
        self.assertEqual(out, b'---\ntitle: "t"\nupdated: "2030-01-02"\n---\nB\n')
    def test_same_day_changes_nothing(self):
        raw = b'---\ntitle: "t"\nupdated: "2030-01-02"\n---\nB\n'
        self.assertEqual(m.set_updated(raw, "2030-01-02"), raw)
    def test_only_if_missing_keeps_an_old_date(self):
        raw = b'---\ntitle: "t"\nupdated: "2020-05-05"\n---\nB\n'
        self.assertEqual(m.set_updated(raw, "2030-01-02", only_if_missing=True), raw)
    def test_unquoted_date_written_by_hand_is_normalised(self):
        out = m.set_updated(b'---\nupdated: 2020-05-05\n---\nB\n', "2030-01-02")
        self.assertEqual(out, b'---\nupdated: "2030-01-02"\n---\nB\n')
    def test_crlf_and_bom(self):
        out = m.set_updated(b"\xef\xbb\xbf---\r\ntitle: \"t\"\r\n---\r\nB\r\n", "2030-01-02")
        self.assertEqual(out, b'\xef\xbb\xbf---\r\ntitle: "t"\r\nupdated: "2030-01-02"\r\n---\r\nB\r\n')
    def test_duplicate_date_lines_collapse_to_one(self):
        out = m.set_updated(b'---\nupdated: "a"\nupdated: "b"\n---\nB\n', "2030-01-02")
        self.assertEqual(out.count(b"updated"), 1)
    def test_broken_frontmatter_untouched(self):
        raw = b"---\nx: 1\nno end\n"; self.assertEqual(m.set_updated(raw, "2030-01-02"), raw)

class CommitDate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.d = os.path.realpath(self.tmp.name)
        self.run_ = lambda *a: subprocess.run(["git", "-C", self.d, *a], check=True, capture_output=True, text=True).stdout
        self.run_("init", "-q"); self.run_("config", "user.email", "t@t"); self.run_("config", "user.name", "t")
        m.SOURCES = m.SourceMap()
    def tearDown(self): self.tmp.cleanup()
    def commit(self, day):
        os.environ["MB_DOC_CHECK_TODAY"] = day
        self.run_("add", "-A"); m.run_hook(self.d, []); self.run_("commit", "-qm", day, "--no-verify")
    def read(self, n): return open(os.path.join(self.d, n)).read()
    def test_first_commit_then_every_later_commit(self):
        with open(os.path.join(self.d, "a.md"), "w") as f: f.write("one\n")
        with open(os.path.join(self.d, "b.md"), "w") as f: f.write("two\n")
        self.commit("2030-01-02")
        self.assertIn('updated: "2030-01-02"', self.read("a.md")); self.assertIn('updated: "2030-01-02"', self.read("b.md"))
        with open(os.path.join(self.d, "a.md"), "a") as f: f.write("changed\n")          # only a.md is committed again
        self.commit("2030-01-03")
        self.assertIn('updated: "2030-01-03"', self.read("a.md"))
        self.assertIn('updated: "2030-01-02"', self.read("b.md"))                           # b.md was not in this commit
        with open(os.path.join(self.d, "a.md"), "a") as f: f.write("again\n")
        self.commit("2030-01-09")
        self.assertIn('updated: "2030-01-09"', self.read("a.md"))
    def test_skill_md_gets_no_date(self):
        os.makedirs(os.path.join(self.d, "s")); raw = "---\nname: x\ndescription: y\n---\nB\n"
        with open(os.path.join(self.d, "s", "SKILL.md"), "w") as f: f.write(raw)
        self.commit("2030-01-02"); self.assertEqual(self.read("s/SKILL.md"), raw)
    def test_a_blocked_commit_does_not_leave_a_wrong_date_behind_in_the_index(self):
        with open(os.path.join(self.d, "a.md"), "w") as f: f.write("[[nothing-here]]\n")
        os.environ["MB_DOC_CHECK_TODAY"] = "2030-01-02"; self.run_("add", "-A")
        rep = m.run_hook(self.d, []); self.assertTrue(rep.blocks)


class RealChangeOnly(unittest.TestCase):
    """The date follows a real change and nothing else."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.d = os.path.realpath(self.tmp.name)
        self.g = lambda *a: subprocess.run(["git", "-C", self.d, *a], check=True, capture_output=True, text=True).stdout
        self.g("init", "-q"); self.g("config", "user.email", "t@t"); self.g("config", "user.name", "t")
        m.SOURCES = m.SourceMap()
    def tearDown(self): self.tmp.cleanup()
    def w(self, n, text):
        os.makedirs(os.path.dirname(os.path.join(self.d, n)) or self.d, exist_ok=True)
        with open(os.path.join(self.d, n), "w", newline="") as f: f.write(text)
    def r(self, n):
        with open(os.path.join(self.d, n), newline="") as f: return f.read()
    def commit(self, day):
        os.environ["MB_DOC_CHECK_TODAY"] = day; self.g("add", "-A")
        rep = m.run_hook(self.d, []); self.g("commit", "-qm", day, "--no-verify"); return rep
    FM = '---\ntitle: "a"\ndoc-id: "mb-00000001"\nupdated: "%s"\n---\n%s'
    def test_a_date_only_difference_is_not_something_to_commit(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n")); self.commit("2030-01-02")
        self.w("a.md", self.FM % ("2031-07-07", "body\n"))            # only the date line differs from HEAD
        os.environ["MB_DOC_CHECK_TODAY"] = "2031-08-08"; self.g("add", "-A"); m.run_hook(self.d, [])
        self.assertEqual(self.r("a.md"), self.FM % ("2030-01-02", "body\n"))      # the committed version is put back
    def test_a_real_change_moves_the_date(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n")); self.commit("2030-01-02")
        self.w("a.md", self.FM % ("2030-01-02", "body changed\n")); self.commit("2030-03-04")
        self.assertIn('updated: "2030-03-04"', self.r("a.md"))
    def test_a_whitespace_change_counts(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n")); self.commit("2030-01-02")
        self.w("a.md", self.FM % ("2030-01-02", "body \n")); self.commit("2030-03-04")
        self.assertIn('updated: "2030-03-04"', self.r("a.md"))
    def test_a_frontmatter_change_other_than_the_date_counts(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n")); self.commit("2030-01-02")
        self.w("a.md", self.FM.replace('title: "a"', 'title: "A new title"') % ("2030-01-02", "body\n")); self.commit("2030-03-04")
        self.assertIn('updated: "2030-03-04"', self.r("a.md"))
    def test_nothing_staged_nothing_happens(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n")); self.commit("2030-01-02")
        os.environ["MB_DOC_CHECK_TODAY"] = "2031-01-01"; rep = m.run_hook(self.d, [])
        self.assertEqual(self.r("a.md"), self.FM % ("2030-01-02", "body\n")); self.assertEqual(rep.changed, [])
    def test_untouched_documents_keep_their_date(self):
        self.w("a.md", self.FM % ("2030-01-02", "a\n")); self.w("b.md", self.FM.replace("00000001", "00000002") % ("2030-01-02", "b\n")); self.commit("2030-01-02")
        self.w("a.md", self.FM % ("2030-01-02", "a2\n")); self.commit("2030-05-05")
        self.assertIn('2030-05-05', self.r("a.md")); self.assertIn('2030-01-02', self.r("b.md"))
    def test_first_date_on_a_document_that_had_none_is_kept(self):
        self.w("a.md", '---\ntitle: "a"\ndoc-id: "mb-00000001"\n---\nbody\n'); self.g("add", "-A"); self.g("commit", "-qm", "old", "--no-verify")   # HEAD has no date
        self.w("a.md", self.FM % ("2030-06-06", "body\n"))            # the one-time 'migrate' added the first date
        os.environ["MB_DOC_CHECK_TODAY"] = "2030-09-09"; self.g("add", "-A"); m.run_hook(self.d, [])
        self.assertEqual(self.r("a.md"), self.FM % ("2030-06-06", "body\n"))      # seeded date stays; it is not restamped
    def test_a_new_document_is_dated(self):
        self.w("a.md", "x\n"); self.commit("2030-01-02"); self.assertIn('updated: "2030-01-02"', self.r("a.md"))
    def test_a_move_is_something_to_commit(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n" * 40)); self.commit("2030-01-02")
        os.makedirs(os.path.join(self.d, "sub")); self.g("mv", "a.md", "sub/a.md"); self.commit("2030-07-07")
        self.assertIn('updated: "2030-07-07"', self.r("sub/a.md"))
    def test_a_link_repair_is_something_to_commit(self):
        self.w("t.md", '---\ntitle: "t"\ndoc-id: "mb-00000010"\nupdated: "2030-01-02"\n---\n' + "text " * 60 + "\n")
        self.w("ref.md", '---\ntitle: "ref"\ndoc-id: "mb-00000011"\nupdated: "2030-01-02"\n---\nsee [[t]]\n'); self.commit("2030-01-02")
        self.g("mv", "t.md", "moved.md"); self.commit("2030-08-08")
        self.assertIn("[[moved]]", self.r("ref.md")); self.assertIn('updated: "2030-08-08"', self.r("ref.md"))
    def test_a_blocked_commit_followed_by_an_abandoned_edit_leaves_no_stray_date(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n")); self.commit("2030-01-02")
        self.w("a.md", self.FM % ("2030-01-02", "body\n[[typo-nowhere]]\n"))
        os.environ["MB_DOC_CHECK_TODAY"] = "2030-04-04"; self.g("add", "-A"); rep = m.run_hook(self.d, []); self.assertTrue(rep.blocks)
        self.assertIn('updated: "2030-04-04"', self.r("a.md"))        # stamped for the attempted commit ...
        self.w("a.md", self.FM % ("2030-04-04", "body\n"))            # ... the author then removes the edit again
        os.environ["MB_DOC_CHECK_TODAY"] = "2030-04-05"; self.g("add", "-A"); m.run_hook(self.d, [])
        self.assertEqual(self.r("a.md"), self.FM % ("2030-01-02", "body\n"))      # back to the committed version, old date


class NoEmptyCommits(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.d = os.path.realpath(self.tmp.name)
        self.g = lambda *a: subprocess.run(["git", "-C", self.d, *a], check=True, capture_output=True, text=True).stdout
        self.g("init", "-q"); self.g("config", "user.email", "t@t"); self.g("config", "user.name", "t")
        self.env = dict(os.environ, MB_DOC_CHECK_SOURCES="/nonexistent")
        subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb-doc-check.py"), "install-hook", "--repo", self.d], capture_output=True)
    def tearDown(self): self.tmp.cleanup()
    FM = '---\ntitle: "a"\ndoc-id: "mb-00000001"\nupdated: "%s"\n---\n%s'
    def w(self, n, s):
        with open(os.path.join(self.d, n), "w") as f: f.write(s)
    def commit(self, msg, day):
        self.g("add", "-A")
        return subprocess.run(["git", "-C", self.d, "commit", "-qm", msg], capture_output=True, text=True, env=dict(self.env, MB_DOC_CHECK_TODAY=day))
    def count(self): return len(self.g("log", "--oneline").split("\n")) - 1
    def test_a_date_only_commit_is_refused_and_leaves_no_empty_commit(self):
        self.w("a.md", self.FM % ("2030-01-02", "body\n")); self.assertEqual(self.commit("one", "2030-01-02").returncode, 0)
        n = self.count(); self.w("a.md", self.FM % ("2031-05-05", "body\n"))
        r = self.commit("date only", "2031-06-06")
        self.assertNotEqual(r.returncode, 0); self.assertIn("NOTHING TO COMMIT", r.stdout + r.stderr)
        self.assertEqual(self.count(), n)
        self.assertIn('updated: "2030-01-02"', open(os.path.join(self.d, "a.md")).read())
    def test_a_date_only_document_beside_a_real_change_is_left_out(self):
        self.w("a.md", self.FM % ("2030-01-02", "a\n")); self.w("b.md", (self.FM % ("2030-01-02", "b\n")).replace("00000001", "00000002"))
        self.assertEqual(self.commit("two docs", "2030-01-02").returncode, 0)
        self.w("a.md", self.FM % ("2031-05-05", "a\n")); self.w("b.md", (self.FM % ("2030-01-02", "b changed\n")).replace("00000001", "00000002"))
        r = self.commit("one real", "2031-06-06"); self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.g("show", "--stat", "--format=", "HEAD").count("|"), 1)           # only b.md is in the commit
        self.assertIn('updated: "2031-06-06"', self.g("show", "HEAD:b.md")); self.assertIn('updated: "2030-01-02"', self.g("show", "HEAD:a.md"))
    def test_a_real_empty_commit_is_still_possible_when_asked_for(self):
        self.w("a.md", self.FM % ("2030-01-02", "a\n")); self.commit("one", "2030-01-02")
        r = subprocess.run(["git", "-C", self.d, "commit", "-qm", "empty on purpose", "--allow-empty"], capture_output=True, text=True, env=self.env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class QuietWhenNothingChanged(unittest.TestCase):
    def test_no_links_written_line_for_links_that_were_already_standard(self):
        os.environ["MB_DOC_CHECK_ANYPATH"] = "1"; self.addCleanup(lambda: (os.environ.pop("MB_DOC_CHECK_ANYPATH", None), setattr(m, "SOURCES", m.SourceMap())))
        with tempfile.TemporaryDirectory() as tmp:
            d = os.path.realpath(tmp); g = lambda *a: subprocess.run(["git", "-C", d, *a], check=True, capture_output=True, text=True).stdout
            g("init", "-q"); g("config", "user.email", "t@t"); g("config", "user.name", "t"); m.SOURCES = m.SourceMap({"s": d})
            with open(os.path.join(d, "y.md"), "w") as f: f.write('---\ntitle: "y"\ndoc-id: "mb-00000002"\nupdated: "2030-01-02"\n---\n')
            with open(os.path.join(d, "x.md"), "w") as f: f.write('---\ntitle: "x"\ndoc-id: "mb-00000001"\nupdated: "2030-01-02"\n---\nsee [[[s:y]]](y.md)\n')
            g("add", "-A"); g("commit", "-qm", "c", "--no-verify")
            with open(os.path.join(d, "x.md"), "a") as f: f.write("more\n")
            g("add", "-A"); rep = m.run_hook(d, [])
            self.assertEqual(rep.canonicalized, [])

if __name__ == "__main__": unittest.main()
