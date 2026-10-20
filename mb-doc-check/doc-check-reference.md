---
title: "doc-check-reference"
doc-id: "mb-08c8ef59"
updated: "2026-10-20"
---
# mb-doc-check — Reference: Commands, Messages, Procedures, Troubleshooting

Companion to [[[mybizz-config-docs:mb-doc-check/doc-check-config]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-config.md) (current state) and [[[mybizz-config-docs:mb-doc-check/doc-check-explainer]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-explainer.md) (what it is and why). The author's view of the link system is [[[mybizz-os-docs:os-reference-docs/documentation-linking-explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/documentation-linking-explainer.md); the procedure to follow every time you finish work is [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md). Agent-facing.

Every command is run as `python3 /mnt/c/mybizz/scripts/mb-doc-check.py <command>`. Day to day nothing is run by hand: the hook runs inside every commit made with `commit-all.sh`.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| `mb-doc-check.py` (source repo `mybizz-scripts`) | `C:\mybizz\scripts\mb-doc-check.py` | commit `236fdde` (2026-10-15) | 2026-10-15 |
| `mb-doc-check.sources` | `C:\mybizz\scripts\mb-doc-check.sources` | current | 2026-10-15 |
| Repository and source list | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | current | 2026-10-15 |
| Commit-all procedure | [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md) | current | 2026-10-15 |

## Checks

All are read-only; the agent runs every one.

| Check | Method | Run by |
|---|---|---|
| Installed version | `ls -la /mnt/c/mybizz/scripts/mb-doc-check.py` (byte size) and `git -C /mnt/c/mybizz/scripts log -1 --format='%h %ad' --date=short` | agent |
| Settings file | Read `mb-doc-check.sources`, then `python3 /mnt/c/mybizz/scripts/mb-doc-check.py sources-check`. It must say `everything matches` | agent |
| Covered repositories vs GBrain | `sources-check`. Its `note` lines about code sources not in the file are informational | agent |
| Page-name rule vs GBrain | `python3 /mnt/c/mybizz/scripts/mb-doc-check.py slug-selftest`. It must report `0 difference(s)` | agent |
| Works | `check --root <repo>` must end with `all clear`; `bash /mnt/c/mybizz/mybizz-config-docs/mb-doc-check/tests/run-tests.sh` must end with `OK` | agent |

---

## Commands

| Command | What it does | Changes files? |
|---|---|---|
| `hook` | What git runs at commit time. `--dry-run` shows what would happen. `--also-root FOLDER` adds a folder whose documents may be linked to | Yes (not with `--dry-run`) |
| `check --root REPO` | Health report of one repository: links pointing nowhere, names shared by several documents, documents without a code, title or date, CRLF documents, links not yet in the standard form. `--all` lists every item | No |
| `links-report` | Counts the links of every covered repository by kind. `--all` also lists every unresolved link and every pasted path | No |
| `collisions --root REPO` | Lists file names used by more than one document. `--all` lists every one | No |
| `sources-check` | Compares `mb-doc-check.sources` with `gbrain sources list` | No |
| `slug-selftest` | Compares the page-name rule with GBrain's own. `--paths FILE` uses a list of paths instead of the documents | No |
| `install-hook --repo REPO` | Installs the pre-commit hook. It never overwrites an existing hook; it prints the line to add | Writes the hook |
| `migrate --root REPO` | Counts documents lacking a code, title or date. With `--write` it adds them | With `--write` |
| `rollout --repo REPO` | Puts every link of one repository in the standard form. Without `--write` it only reports. It refuses a repository with uncommitted changes unless `--force` | With `--write` |
| `fix-broken --repo REPO` | Turns every link that points to nothing into plain words. `--include-ambiguous` also handles shared names | With `--write` |
| `eol --repo REPO` | Converts the documents of one repository to LF. `--show N` lists the first N | With `--write` |

`rollout`, `fix-broken` and `eol` never commit. Commit afterwards with `commit-all.sh`.

## What the hook prints and what to do

| Message | Meaning | What to do |
|---|---|---|
| `THE COMMIT IS STOPPED` with `points to no document` | A link you typed names a document that does not exist | Correct the name, or write the words without a link, then commit again |
| `is a name shared by several documents (N); write the one you mean, for example [[source-id:name]]` | The name exists in several repositories | Write one of the suggested `[[source-id:name]]` links, then commit again |
| `was deleted and new document(s) were added in the same commit` | The program cannot tell a rename from a deletion | If it is a rename, put the printed `doc-id` line into the new document's frontmatter. If the old document is really gone, commit with `MB_DELETE_OK=1 bash /mnt/c/mybizz/scripts/commit-all.sh "message"` |
| `NOTHING TO COMMIT` | Only the `updated` date differed, so the file was put back | Nothing. Change a document for real before committing |
| `documents given a permanent code`, `given a title`, `'updated' date set`, `links written in the standard form`, `line endings changed to LF` | Information: the program completed documents | Nothing |
| `links made specific because two documents now share a name` | A new document created a shared name, so existing links were rewritten as `[[source-id:name]]` | Nothing |
| `pasted paths left as text (no such document in the documentation repositories)` | A path that looks like a document path points to no document | Nothing, unless it should have been a link |
| `older broken links elsewhere (not from this commit, not blocking)` | Existing broken links | Fix them when convenient; `check --root REPO` lists them |
| `skipped because of an internal problem (...)` | The program failed and the commit went through unchecked | Paste the message to Claude, then run `check --root REPO` on that repository |

## Procedures

**Check one repository.**

```
python3 /mnt/c/mybizz/scripts/mb-doc-check.py check --root /mnt/c/mybizz/mybizz-os-docs
```

It must end with `all clear`.

**Bring one repository under the rules** (a new repository, or one left out until now). Do the steps of "Adding a new documentation repository" in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md) first, then:

```
bash /mnt/c/mybizz/scripts/rollout-repo.sh /mnt/c/path/to/repo
```

`rollout-repo.sh` makes four commits: LF line endings, broken links to plain words, every link in the standard form, the `updated` date on every document. It stops at the first problem and never pushes.

**After a GBrain upgrade.**

```
python3 /mnt/c/mybizz/scripts/mb-doc-check.py slug-selftest
python3 /mnt/c/mybizz/scripts/mb-doc-check.py sources-check
```

`slug-selftest` must report `0 difference(s)` and `sources-check` must say `everything matches`.

## Troubleshooting

**A new document has no frontmatter after a commit.** Check whether it is skipped (see "What it does not scan" in [[[mybizz-config-docs:mb-doc-check/doc-check-config]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-config.md)), and whether the hook exists: `ls /mnt/c/mybizz/mybizz-os-docs/.git/hooks/pre-commit`. If the hook is missing, run `install-hook --repo REPO`. A commit made from Windows does not run the hook.

**`sources-check` prints PROBLEM.** The source id or folder in `mb-doc-check.sources` differs from GBrain's list. Correct the line in `mb-doc-check.sources`, never GBrain's list.

**A link shows as `[[source-id:page]]` with no path.** The target is outside the C: drive (for example the memory governor's folder). No clickable path exists. This is expected.

**A link opens nothing in MarkText.** Open the document with File > Open, hold Ctrl and click. A document pasted into a new tab has no folder.

**`slug-selftest` reports differences.** GBrain's page-name rule changed. Stop and paste the output to Claude. Links written since the change may carry names GBrain does not know.

## Do not

- Do not commit with `git commit --no-verify`, and do not commit from a Windows program. Both skip the hook.
- Do not write the long link form, `doc-id` or `updated` by hand.
- Do not run `rollout`, `fix-broken` or `eol` with `--force` unless you know why the repository has uncommitted changes.
- Do not delete or reorder lines in `mb-doc-check.sources` without running `sources-check`.
- Do not name a frontmatter field `date`.
