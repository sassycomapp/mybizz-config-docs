---
title: "doc-check-config"
doc-id: "mb-e7e60242"
updated: "2026-10-15"
---
# mb-doc-check — Configuration

Canonical current-state record of the `mb-doc-check` program. Agent-facing. What it is and why it works as it does: [[[mybizz-config-docs:mb-doc-check/doc-check-explainer]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-explainer.md). Commands, messages and procedures: [[[mybizz-config-docs:mb-doc-check/doc-check-reference]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-reference.md). The author's view of the link system: [[[mybizz-os-docs:os-reference-docs/documentation-linking-explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/documentation-linking-explainer.md).

---

## Identity

| Item | Value |
|---|---|
| Issuer | MyBizz. GBrain is the issuer for the page-name rule and the source-id list |
| Installed version | commit `236fdde` (2026-10-15). The program has no release system; 89,030 bytes live |
| Standard taken from | `mb-doc-check.py` and `mb-doc-check.sources` at commit `236fdde`; GBrain's source list and page-name rule |
| Last researched | 2026-10-15 |

## Settings — program

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Name | — | `mb-doc-check`, a Python program (standard library only). It is not an OpenCode skill | `mb-doc-check.py` at `236fdde` | |
| Location | — | `C:\mybizz\scripts\mb-doc-check.py` (WSL: `/mnt/c/mybizz/scripts/mb-doc-check.py`), 89,030 bytes | live check 2026-10-15 | |
| Settings file | — | `mb-doc-check.sources`, in the same folder | `mb-doc-check.py` at `236fdde` | |
| How it runs | — | As a git `pre-commit` hook in each of the covered repositories listed in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md): `python3 /mnt/c/mybizz/scripts/mb-doc-check.py hook`. A commit made in WSL runs it; a commit made from a Windows program does not | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Failure behavior | — | If the program itself fails with an internal error, it prints "skipped because of an internal problem" and lets the commit through. A bug never blocks work. The skipped documents are corrected at their next commit | `mb-doc-check.py` at `236fdde` | |
| Network and GBrain | — | None, except two commands: `sources-check` calls the `gbrain` command, and `slug-selftest` runs GBrain's own page-name function with `bun` | `mb-doc-check.py` at `236fdde` | |
| Tests | — | 150 automated tests (Python `unittest`), stored in `mybizz-config-docs\gbrain\tests` and run with `bash /mnt/c/mybizz/mybizz-config-docs/gbrain/tests/run-tests.sh`. It ends with `OK` | live run 2026-10-15 | |

## Settings — covered repositories

One row per repository the hook covers. The folder in GBrain's list must equal the folder in `mb-doc-check.sources`; `sources-check` compares them.

| Setting (source id) | Issuer standard (folder per GBrain) | MyBizz value (folder in `.sources`) | Source | Learning |
|---|---|---|---|---|
| `default` | `/mnt/c/dev/project-library-global` | `/mnt/c/dev/project-library-global` | `mb-doc-check.sources`; `sources-check` 2026-10-15 | |
| `dev-root-hub` | `/mnt/c/dev/dev-root` | `/mnt/c/dev/dev-root` | same | |
| `mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` | same | |
| `mb-4-ecom-project-library` | `/mnt/c/dev/dev-mb-4-ecom/mb-4-ecom-project-library` | `/mnt/c/dev/dev-mb-4-ecom/mb-4-ecom-project-library` | same | |
| `mb-5-pdlf-project-library` | `/mnt/c/dev/dev-mb-5-pdlf/mb-5-pdlf-project-library` | `/mnt/c/dev/dev-mb-5-pdlf/mb-5-pdlf-project-library` | same | |
| `mybizz-config-docs` | `/mnt/c/mybizz/mybizz-config-docs` | `/mnt/c/mybizz/mybizz-config-docs` | same | |
| `mybizz-os-docs` | `/mnt/c/mybizz/mybizz-os-docs` | `/mnt/c/mybizz/mybizz-os-docs` | same | |
| `data-mybizz-mgt` | `/mnt/c/data-mybizz-mgt` | `/mnt/c/data-mybizz-mgt` | same | |
| `pdlf` | `/mnt/c/pdlf` | `/mnt/c/pdlf` | same | |
| `mb-project-docs` | `/mnt/c/mybizz/mb-project-docs` | `/mnt/c/mybizz/mb-project-docs` | same | |
| `mb-memory-system-diagnostic` | `/mnt/c/mybizz/mb-memory-system-diagnostic` | `/mnt/c/mybizz/mb-memory-system-diagnostic` | same | |
| `mb-compile-rules` | `/mnt/c/mybizz/mb-compile-rules` | `/mnt/c/mybizz/mb-compile-rules` | same | |
| `mb-sentinel-review` | `/mnt/c/mybizz/mb-sentinel-review` | `/mnt/c/mybizz/mb-sentinel-review` | same | |
| `mb-sysdoc-creator` | `/mnt/c/mybizz/mb-sysdoc-creator` | `/mnt/c/mybizz/mb-sysdoc-creator` | same | |
| `mb-submit-memory` | `/mnt/c/mybizz/mb-submit-memory` | `/mnt/c/mybizz/mb-submit-memory` | same | |
| `mb-archify-scope` | `/mnt/c/mybizz/mb-archify-scope` | `/mnt/c/mybizz/mb-archify-scope` | same | |
| `mb-close-out` | `/mnt/c/mybizz/mb-close-out` | `/mnt/c/mybizz/mb-close-out` | same | |

Not covered: the code repositories, the Anvil clone and the memory governor's folder. The full list of repositories and sources is in [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md).

## Settings — link and storage

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `@paths` in `mb-doc-check.sources` | — | `absolute`. The path part of every link is the full Windows path, for example `C:/mybizz/x/y.md`. Without the line the default is `relative` | `mb-doc-check.sources` | |
| `@eol` in `mb-doc-check.sources` | — | `lf`. Every committed document is stored with LF line endings. Without the line the endings are left as they are | `mb-doc-check.sources` | |
| Stored link form | — | `[[[source-id:page-name|Shown text]]](C:/full/windows/path.md)`. Without shown text, the part from the pipe to the closing brackets is absent. Inside a markdown table row, the pipe before the shown text is written with a backslash in front of it, so the table keeps its columns. A link to a document outside the C: drive has no path part: `[[source-id:page-name]]`, because no clickable path exists | [[[mybizz-os-docs:os-reference-docs/documentation-linking-explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/documentation-linking-explainer.md) | |
| Page name | GBrain's rule | The path from the repository root in lower case, spaces as hyphens, accents removed, without `.md`. A port of GBrain's own rule | `slug-selftest` 2026-10-15 (1,404 paths, 0 differences) | |
| Frontmatter | — | `title` (the file name without `.md`, quoted), `doc-id` (`mb-` and eight hexadecimal characters, permanent) and `updated` (`"YYYY-MM-DD"`, the date of the last real change). Other fields are left alone | [[[mybizz-os-docs:os-reference-docs/frontmatter-conventions]]](C:/mybizz/mybizz-os-docs/os-reference-docs/frontmatter%20conventions.md) | |
| Environment variables | — | `MB_DELETE_OK=1` lets a commit that deletes and adds documents at once go through (see the reference). `MB_DOC_CHECK_SOURCES` and `MB_DOC_CHECK_ROOTS` replace the two settings files. `MB_GBRAIN_DIR` and `MB_GBRAIN_BIN` point `slug-selftest` and `sources-check` at a different GBrain. `MB_DOC_CHECK_TODAY`, `MB_DOC_CHECK_ANYPATH` and `MB_DOC_CHECK_KEEP_SOURCES` exist for the automated tests only | `mb-doc-check.py` at `236fdde` | |

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
- The page-name rule must equal GBrain's. `slug-selftest` compares them on every document of the covered repositories (1,404 paths, 0 differences on 2026-10-15). Run both after every GBrain upgrade.

## Open items

None.
