---
title: "doc-check-config"
doc-id: "mb-e7e60242"
updated: "2026-10-04"
---
# mb-doc-check — Configuration

Canonical current-state record of the `mb-doc-check` program. Agent-facing. Reflects the live-verified state as of 2026-10-01. States facts, not history — what it is and why it works as it does: [[[mybizz-config-docs:mb-doc-check/doc-check-explainer]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-explainer.md); commands, messages and procedures: [[[mybizz-config-docs:mb-doc-check/doc-check-reference]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-reference.md); the author's view of the link system: [[[mybizz-os-docs:os-reference-docs/documentation-linking-explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/documentation-linking-explainer.md).

---

## Identity

| Item | Value |
|---|---|
| Name | `mb-doc-check` — a Python program (standard library only). It is not an OpenCode skill |
| Purpose | At every commit: completes each committed document's frontmatter, writes every link in the standard form, repairs links after a rename, move or deletion, and stops the commit on a link that points to nothing |
| Location | `C:\\mybizz\\scripts\\mb-doc-check.py` (WSL: `/mnt/c/mybizz/scripts/mb-doc-check.py`), 88,758 bytes |
| Settings files | `mb-doc-check.sources` (789 bytes) and `mb-doc-check.roots`, in the same folder |
| How it runs | As a git `pre-commit` hook in each of the eight repositories: `python3 /mnt/c/mybizz/scripts/mb-doc-check.py hook`. A commit made in WSL runs it; a commit made from a Windows program does not |
| Failure behavior | If the program itself fails with an internal error, it prints "skipped because of an internal problem" and lets the commit through. A bug never blocks work. The skipped documents are corrected at their next commit |
| Network and GBrain | None, except two commands: `sources-check` calls the `gbrain` command, and `slug-selftest` runs GBrain's own page-name function with `bun` |
| Tests | 149 automated tests (Python `unittest`), stored in `mybizz-config-docs\gbrain\tests` and run with `bash /mnt/c/mybizz/mybizz-config-docs/gbrain/tests/run-tests.sh` |

## Covered repositories

| Source id | Folder (WSL) |
|---|---|
| `default` | `/mnt/c/dev/project-library-global` |
| `dev-root-hub` | `/mnt/c/dev/dev-root` |
| `makepdlf-project-library` | `/mnt/c/dev/dev-makepdlf/makepdlf-project-library` |
| `mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` |
| `mybizz-config-docs` | `/mnt/c/mybizz/mybizz-config-docs` |
| `mybizz-os-docs` | `/mnt/c/mybizz/mybizz-os-docs` |
| `data-mybizz-mgt` | `/mnt/c/data-mybizz-mgt` |
| `pdlf` | `/mnt/c/pdlf` |

Not covered: the two dormant libraries (`mb4ecom-project-library`, `mb5pdlf-project-library`), the code repositories, the Anvil clone and the memory governor's folder. The full list of repositories and sources is in [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md).

## Settings

| Setting | Current value | Meaning |
|---|---|---|
| Lines `source-id = folder` in `mb-doc-check.sources` | the eight rows above | Which folder is which GBrain source. Must equal GBrain's list (`sources-check`) |
| `@paths` in `mb-doc-check.sources` | `absolute` | The path part of every link is the full Windows path, for example `C:/mybizz/x/y.md`. Without the line the default is `relative` |
| `@eol` in `mb-doc-check.sources` | `lf` | Every committed document is stored with LF line endings. Without the line the endings are left as they are |
| `mb-doc-check.roots` | the eight folders | Folders whose documents may be linked to. One per line; a line starting with `#` is a comment |

Environment variables: `MB_DELETE_OK=1` lets a commit that deletes and adds documents at once go through (see the reference); `MB_DOC_CHECK_SOURCES` and `MB_DOC_CHECK_ROOTS` replace the two settings files; `MB_GBRAIN_DIR` and `MB_GBRAIN_BIN` point `slug-selftest` and `sources-check` at a different GBrain. `MB_DOC_CHECK_TODAY`, `MB_DOC_CHECK_ANYPATH` and `MB_DOC_CHECK_KEEP_SOURCES` exist for the automated tests only.

## What it reads and writes

| | |
|---|---|
| Reads | The `.md` documents of the covered repositories, including those in `obsolete` folders (as link targets only); the committed state and the staged state from Git; the settings files |
| Writes | The text of documents only: frontmatter, links, line endings, the `updated` date. It runs `git add` on the files it repaired so that they join the same commit. `install-hook` writes `.git/hooks/pre-commit` |
| Never | Moves, renames or deletes a file. Commits or pushes. Edits a `SKILL.md` file or anything inside an `obsolete` folder |

## What it does not scan

| Kind | Rule |
|---|---|
| Files | Not `.md`; names starting with `.`; names starting with `tmp-` (no frontmatter is added to them) |
| Folders | Names starting with `.` or `tmp-`; `.git`, `node_modules`, `__pycache__`; `stencils`, `quarantine`, `backups`, `catalogue`, `logs`; any folder that contains `anvil.yaml` (an Anvil app root) and everything below it |
| `obsolete` folders (any level) | Indexed as link targets, never edited |
| `SKILL.md` | Never edited |
| Empty files | No frontmatter is added |

## The stored forms

- **Link:** `[[[source-id:page-name|Shown text]]](C:/full/windows/path.md)`. Without shown text, the part from the pipe to the closing brackets is absent.
- **Link inside a markdown table row:** the pipe before the shown text is written with a backslash in front of it, so the table keeps its columns.
- **Link to a document outside the C: drive:** `[[source-id:page-name]]` with no path part, because no clickable path exists.
- **Page name:** the path from the repository root in lower case, spaces as hyphens, accents removed, without `.md`. It is a port of GBrain's own rule.
- **Frontmatter:** `title` (the file name without `.md`, quoted), `doc-id` (`mb-` and eight hexadecimal characters, permanent) and `updated` (`"YYYY-MM-DD"`, the date of the last real change). Other fields are left alone.
- **Line endings:** LF.

## What stops a commit

| Situation | Result |
|---|---|
| A link you just typed points to no document | The commit is stopped; the message names the file and line |
| A link you just typed names several documents | Stopped; the message lists the exact `[[source-id:name]]` links you can write |
| Damaged frontmatter | Stopped; the message names the file |
| A commit deletes documents and adds new ones at once, and links point to a deleted one | Stopped, because the program cannot tell a rename from a deletion. `MB_DELETE_OK=1` overrides it |
| The only difference in a staged document is its `updated` date | The document is put back exactly as committed; the message says "NOTHING TO COMMIT" |

Problems that already existed before the commit are reported but never stop it.

## Dependencies on GBrain

- `mb-doc-check.sources` must match `gbrain sources list` in source ids and folders. `sources-check` compares them.
- The page-name rule must equal GBrain's. `slug-selftest` compares them on every document of the covered repositories (1,292 paths, 0 differences on 2026-10-01). Run both after every GBrain upgrade.

## Open items

| # | Item | Status |
|---|---|---|
| 1 | The two dormant libraries are not covered; adding one needs the steps in [[[mybizz-config-docs:mb-doc-check/doc-check-reference]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-reference.md) | Open |
| 2 | The program's built-in help text still shows a relative-path example; the stored form follows `@paths` | Open |
