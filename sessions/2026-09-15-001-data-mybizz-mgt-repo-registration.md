---
title: "2026-09-15-001-data-mybizz-mgt-repo-registration"
doc-id: "mb-7c925181"
updated: "2026-10-04"
---
# Session 2026-09-15 — data-mybizz-mgt repo + GBrain + opencode registration

## What was done

1. **Folder renamed.** `C:\_data-mybizz-mgt` → `C:\data-mybizz-mgt`. Developer
   decision to drop the leading underscore ("save us a lot of trouble later").
   Agent-side `mv` failed twice (Windows-side handle; later diagnosed as an OS
   lock — an initial `cmd.exe /c ren` attempt was rejected by the developer and
   the developer renamed the folder manually in Explorer).
2. **GitHub repo created and pushed** per the GitHub-backed ADR required
   pattern: `sassycomapp/data-mybizz-mgt`, private, branch `master`, remote
   `origin`. Two commits, both developer-run (see standards below):
   - `27c0e2e` — Initial commit — 28 files, 2206 insertions
   - `f38b285` — master-task-list.md frontmatter YAML fix
3. **GBrain source registered**: `gbrain sources add data-mybizz-mgt --path
   /mnt/c/data-mybizz-mgt --federated --force` (force needed because the first
   commit didn't exist yet at registration time). Two syncs run; final sync
   checkpoint `f38b285`, 23 pages embedded. `gbrain extract --stale
   --source-id data-mybizz-mgt`: 23/23 pages swept, **0 links + 0 timeline
   entries persisted; 78 candidates skipped** — targets are documents in other
   sources, not pages; expected to self-correct when mb-wikilinks retrofits
   wikilinks.
4. **opencode registration**: `external_directory` gained
   `"C:\\data-mybizz-mgt\\**": "allow"` in the global `opencode.jsonc`
   (edit tool, granted). Verified in resolved config via `opencode debug
   config`. Takes effect on next opencode restart.
5. **Excel replaced by Markdown**: `Repo organization.xlsx` (deleted by the
   developer) → [[[mybizz-os-docs:os-reference-docs/repo-organization|Repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md), built from the developer's
   image of the sheet; the new repo row appended (13 rows total).
6. **Root files created** in data-mybizz-mgt: `README.md` (structure, key
   documents, naming note) and `register-local.md` The use of registers has been discontinued. Please review (append-only; _desktop
   docs registered provisionally; Budget/Models/prompts membership left open
   for mb-align-docs).
7. **Scope scaffold updated** ([[[mybizz-os-docs:os-reference-docs/mybizz-scope-list|Mybizz Scope List]]](C:/mybizz/mybizz-os-docs/os-reference-docs/mybizz-scope-list.md)): in-scope root
   entry and GitHub repo list row updated to the new name. Developer later
   asked to "update" it, then aborted on seeing it was already done.
8. **mb-docs-manager skill files fixed** (4 files, agent-editable under
   grant): `SKILL.md` (3 refs), `docs-manager-scan.md` (4 refs),
   `docs-manager-backup.md` (2 refs), `docs-manager-README.md` (1 ref) — all
   `_data-mybizz-mgt` → `data-mybizz-mgt`; verified 0 remaining.
9. **Global AGENTS.md fixed** — developer-run `sed -i
   's/_data-mybizz-mgt/data-mybizz-mgt/g'` after the
   protected-AI-governance-files policy refused the agent edit (even with a
   developer-issued grant on the file path).
10. **YAML repair**: [[[data-mybizz-mgt:desktop/master-task-list|mybizz-OS]]](C:/data-mybizz-mgt/desktop/master-task-list.md) frontmatter `status:` value
    contained an unquoted colon → gbrain sync blocked with a parse failure.
    Fixed by quoting the value; committed and pushed by the developer
    (`f38b285`).

## Standards the developer set this session

- **Grants are developer-issued.** The agent requests grants in exactly
  `mg-grant --path <folder> --count N` and the developer runs them in the WSL
  terminal. The agent may run `mg-grant` only when the developer's instruction
  to do so is explicit for that occasion. Do not revoke grants unless the
  developer says so.
- **Cupcake commit-gate is absolute.** The no-autonomous-commits policy
  denies agent-run `git commit|push|merge` unconditionally — a question-tool
  approval does NOT satisfy it. Commit/push are developer terminal blocks,
  always.
- **Protected governance files** (global `AGENTS.md`, policy regos) are
  developer-edit-only; grants do not unlock them.
- **Keep finishing, don't stockpile flags** — surface what's needed to finish;
  leave corpus doc management to mb-docs-manager / mb-align-docs / mb-wikilinks.
- Excel artifacts in this folder are replaced by Markdown equivalents going
  forward.

## Quirks and dispositions

- **mg-grant lowercases paths** (`to_wsl()`): granting
  `/home/dev-p/.config/opencode/AGENTS.md` recorded the grant as
  `.../agents.md` — on a case-sensitive FS a file-level grant for an uppercase
  filename may not match. Prefer folder-level grants for uppercase paths.
  (Moot here: the protected-files policy blocks agent edits regardless.)
- **Permission-denied rename** on DrvFs was an OS-level handle, not a grants
  or ACL problem; `lsof` showed nothing (9p handles are not visible that way).
- **`gbrain sources add` refuses paths with no committed files** — offers
  `--force`; used here, sync run after the commit landed.
- **Cupcake pre-tool deny evaluates the whole command string** — a compound
  command containing one ungranted path is refused before ANY part runs
  (an `mg-grant && mv` combo left the grant unexecuted; split the steps).

## Artifacts

- GitHub: `sassycomapp/data-mybizz-mgt` (private, master, 2 commits)
- GBrain source: `data-mybizz-mgt` (federated), 23 pages, synced to `f38b285`
- `opencode.jsonc` external_directory entry (restart pending)
- [[[mybizz-os-docs:os-reference-docs/repo-organization|Repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md), `README.md`, `register-local.md` The use of registers has been discontinued. Please review
- Fixed: scope scaffold, 4 mb-docs-manager skill files, global AGENTS.md
  (developer-run), master-task-list.md frontmatter

## Open / next

- **Docs corpus sweep (assigned to the docs skills, not done here)**: old-path
  references remain in `dev-root/docmap.md`, `mybizz-config-docs` (
  `projects-config-register.md` The use of registers has been discontinued. Please review, [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md), gstack references,
  [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md), `docs-manager-config.md`, one sessions page),
  `mybizz-os-docs` ([[[mybizz-os-docs:operating-procedures/fact-save-and-recall|Operating Procedure]]](C:/mybizz/mybizz-os-docs/operating-procedures/fact-save-and-recall.md), [[[mybizz-os-docs:operating-procedures/opening-and-closing|Operating Procedure]]](C:/mybizz/mybizz-os-docs/operating-procedures/opening-and-closing.md)), and
  pdlf docs (2 files).
- **Restart opencode** — `external_directory` + AGENTS.md + skill files load
  at process start.
- **Grants active, left un-revoked** per developer instruction: the obsolete
  `/mnt/c/_data-mybizz-mgt` grant (dead path), `/mnt/c/data-mybizz-mgt`,
  `opencode.jsonc`, `agents.md` (lowercased), `skills/mb-docs-manager`.
- **Flagged in mybizz-config-docs working tree** (Phase F, not handled): tracked
  file deleted — `sessions/2026-09-14-001-dream-cycle-config-mgmt.md` (` D`);
  untracked artifact dir `.sources/`. Developer decides; nothing committed.
- **Open decision**: whether data-mybizz-mgt gets a `{slug}-config.yaml` +
  projects-config-register The use of registers has been discontinued. Please review row (start-a-project protocol) — for
  mb-docs-manager/mb-config-manager.
- gbrain CLI upgrade available (0.46.1.0 → 0.50.0.0).
