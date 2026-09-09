# docs-manager — Reference

Execution procedure for the `mb-docs-manager` skill (V10). `SKILL.md` in the
installed folder (`~/.config/opencode/skills/mb-docs-manager/`) is the
authoritative definition; this document is the operational form. Why the
rules are shaped this way: `docs-manager-explainer.md`.

## Invocation

- `/mb-docs-manager` — full run, unconditionally. No keyword means full run; never ask.
- `/mb-docs-manager <document-path>` — one document only (backup still covers the full in-scope set).
- `/mb-docs-manager division-maps` — pinned documents only (scaffold, docmap, register).
- `/mb-docs-manager quick` — pinned documents + discovered README.md files.
- `/mb-docs-manager references` — internal reference resolution only, no directory walk.
- `/mb-docs-manager no-push` — through Phase 5 + 7, skipping Phase 6.
- Invocation IS the trigger — Phase −1 and Phase 0 start immediately, no confirmation. The
  orchestrator speaks only at: an abort (REPOS_DIRTY, BACKUP_FAILED), the resume/discard
  question, or the Phase 2 report.

## Phase procedure

1. **Phase −2 — Resume check.** Check `C:\mybizz\logs\docs-manager\in-progress\`. Empty →
   new run (clear `last-completed-run\`). File found → stop and ask: resume (append to the
   same record, jump past completed phases; re-verify each approved change against current
   content before applying) or discard (move to `abandoned-runs\`, never delete, then fresh
   run). Never decided automatically.
2. **Continuous checkpointing** — one file, `in-progress\<run-timestamp>.md`, appended
   unconditionally after every phase: learnings count, backup result, the full verbatim
   change report, approval decisions verbatim, exact before/after per edit, per-operation
   records, verification result, commit/push result, learnings one-liners inline.
3. **Phase −1 — Load learnings.** Read every file in `...\docs-manager\Learnings\`;
   carry forward as context. Learnings overrule SKILL.md on scope/classification/
   recommendation — never on the three hard constraints.
4. **Phase 0 — Pre-flight + backup.** (a) `git status` on all 12 Active Repositories from
   `projects-config-register.md`'s GitHub-repositories section (the scaffold's list) — any
   dirty repo aborts the entire run (`REPOS_DIRTY`) before backup; (b) discover the six
   managed types across the scaffold-defined in-scope walk, copy them to
   `C:\backup-docs-manager\<run-timestamp>\` preserving relative paths, then **verify by
   direct file count** against the discovery count — mismatch is `BACKUP_FAILED`, abort.
   Creating the folder is not the backup.
5. **Phase 1 — Scan** (read-only): read the 3 pinned documents + every discovered managed
   document; walk in-scope folders (existence/structure only, all depths); extract and
   resolve internal references (Section 2 rules); apply per-type update rules incl.
   `verified:` date proposals; exact counts; a concrete recommendation on every flagged item.
6. **Phase 2 — Report:** summary counts; proposed text edits table; proposed file-system
   operations table (separate — never includes a delete); flagged anomalies with
   recommendations; newly discovered documents.
7. **Phase 3 — Approval.** Per-document, per-change, or batch. Three embedded rules:
   (a) **push approval is a separate decision** — recorded verbatim; no explicit yes = Phase 6
   skipped; (b) **AGENTS.md edits require the developer naming the exact file** in the
   approval reply — a batch "approved" without naming authorizes nothing on AGENTS.md;
   (c) resolved anomalies become approved changes + learning candidates.
8. **Phase 3a — Grant handover (conditional).** If approved edits target folders outside the
   shared-library list: group by folder, construct `mg-grant --path <folder> --count
   <approved-files + 2>`, hand the commands to the developer to run (the skill never invokes
   `mg-grant` itself), verify `~/.config/cupcake/policies/opencode/cup-grants-data.rego`
   contains every entry, then apply immediately — slips expire ~30 minutes and decrement per
   use; lapsed/short slip → re-request, never work around.
9. **Phase 4a — Apply text edits** (sub-agent: edit-only, no bash). Approved items only.
   A policy-denied write → stop and report, never work around.
10. **Phase 4b — Apply file-system operations** (separate sub-agent: bash-only, no edit).
    Rename/move/copy only; **never deletes** — a delete is a move to the relevant
    `obsolete\` folder; no obvious destination → flag back, don't guess. Second explicit
    confirmation immediately before execution, always.
11. **Phase 5 — Verify** (read-only): re-read changed docs, re-resolve references, confirm
    no new breakage.
12. **Phase 6 — Commit & push.** Only under the recorded Phase 3 push approval + clean
    verification. Resolve git-tracked filenames via `git ls-files --full-name` (NTFS
    case-insensitivity); stage only the changed files (never `git add -A`); commit message
    `mb-docs-manager: <run-timestamp> — N changes applied`; commit locally regardless of
    remote reachability; validate remote via `git ls-remote --heads origin` then push;
    failure → `PUSH_FAILED` reported immediately, local commit stands. Per-repo results to
    `C:\mybizz\logs\github-logs\commit-push-<date>.md`.
13. **Phase 7 — Log.** Write `C:\mybizz\logs\docs-manager\<timestamp>.md` (timestamp = run
    completion time) — structured fields only, no narrative, exact counts.
14. **Phase 8 — Update learnings (mandatory when changes were applied).** One file per
    learning, `Learnings\<timestamp>-<short-topic>.md` (Context / Decision / Applies to);
    then verify at least one file matches this run's timestamp — no file = process failure,
    report it. No novel judgment calls → write the explicit minimal learning saying so.
15. **Phase 9 — Completion gate.** (1) `division-maps` re-scan of the three pinned documents
    (own changes can drift them); findings go through their own report-approve-apply cycle;
    (2) GitHub confirmation prompt (separate question); (3) GBrain sync prompt (separate
    question — the orchestrator launches `setsid bash /mnt/c/mybizz/scripts/sync-gbrain.sh`,
    never the skill itself); (3a) after any 4b structural changes: static reminder to run
    mb-align-docs next; (4) closing git-status snapshot →
    `github-logs\git-status-<date>.md`; (5) verify the checkpoint has an entry for every
    executed phase — missing = process failure, reconstruct before closing; (6) move
    `in-progress\` record to `last-completed-run\` (update its H1 title), leaving
    `in-progress\` empty.

## Hard constraints (operational form)

1. **Nothing is written except in Phase 4a/4b**, and only developer-approved changes — 4b
   additionally requires a second explicit confirmation. Exemptions (create-only): Phase 0
   backup, Phase 7 log, Phase 8 learnings, continuous checkpointing. **Creation of any
   managed document type is permanently out of scope** — a missing managed doc is a flagged
   finding, never created by the skill. **Phase 4b never deletes.**
2. **Phase 0 runs in full, in order, every invocation** — git-status pre-flight (dirty →
   abort whole run) then verified backup (verification failure → abort). Neither skippable.
3. **Never run `gbrain sync` or any GBrain state-changing command.** Read-only GBrain
   inspection only, where Section 3 calls for it.

## Anomaly classes

| Class | Action |
|---|---|
| REPOS_DIRTY | Abort entire run before backup — developer cleans, re-invokes |
| BACKUP_FAILED | Abort entire run — no scan |
| BROKEN / MISMATCHED / AMBIGUOUS / MISSING / UNDOCUMENTED / COUNT MISMATCH / STALE DATE | Per report rules — propose fix or flag with recommendation; never guess |
| CODE_REPO_AMBIGUOUS | Flag with recommendation; never auto-resolve. `makepdlf` placeholder exempt per learning |
| GRANT_REQUIRED | Phase 3a handover — prefilled `mg-grant` commands; never work around |
| NO_REPO | Report under "Skipped — Not a Git Repository" — expected, not an error |
| PUSH_FAILED | Report immediately — local commit stands; push retried manually |

## Do not

- Do not write anything outside Phase 4a/4b, and never unapproved changes.
- Do not create any managed document (scaffold, docmap, register, README, AGENTS.md, INDEX.md) — missing ones are findings.
- Do not delete anything — a delete is a move to `obsolete\`.
- Do not skip, reorder, or ask about Phase 0.
- Do not report an unverified backup as successful.
- Do not run `gbrain sync` or change GBrain state.
- Do not run `git add -A` or stage beyond the approved change set.
- Do not invoke `mg-grant` on your own initiative — hand the commands to the developer.
- Do not work around a policy denial — stop and report.
- Do not edit the scope scaffold — scope changes are the developer's.
- Do not touch `anvil.yaml` — ever, in any way.
- Do not use vague quantifiers — exact counts, every document named.
- Do not ask permission to start, or which scope was meant.
