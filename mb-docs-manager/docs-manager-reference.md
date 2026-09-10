---
document: "docs-manager — Reference"
doc-id: docs-manager-reference
state: Live
date-created: 2026-09-10
---

# docs-manager — Reference

Execution procedure for the `mb-docs-manager` skill (V11). `SKILL.md` in the
installed folder (`~/.config/opencode/skills/mb-docs-manager/`) is the
authoritative definition; this document is the operational form. Why the
rules are shaped this way: `docs-manager-explainer.md`.

## Invocation

- `/mb-docs-manager (all)` — full scaffold sweep, unconditionally, once the target is known.
- `/mb-docs-manager (name)` — one folder or document, named in parentheses.
- `/mb-docs-manager (division-maps)` — pinned documents only (scaffold, docmap, register).
- `/mb-docs-manager (quick)` — pinned documents + discovered README.md files.
- `/mb-docs-manager (references)` — internal reference resolution only, no directory walk.
- `no-push` — trailing modifier: `/mb-docs-manager (all) no-push` — Phase 6 skipped; Phase 9
  offers the commit/push question, and an explicit yes there authorizes it.
- **Empty or omitted target: the skill asks for a target and does nothing until answered.**
  The target is never assumed.
- **Code repo named as target: denied.** State the denial (Anvil code repos are never
  touched, including any `theme\assets\docs` inside them) and ask for a planning-corpus target.
- Invocation with a valid target IS the trigger — Phase −1 and Phase 0 start immediately, no
  confirmation. The orchestrator speaks only at: an abort, a request for the missing target,
  or the Phase 2 report.

## Phase procedure

1. **Phase −2 — Resume check.** Check `C:\mybizz\logs\mb-docs-manager\in-progress\`. Empty →
   new run (clear `last-completed-run\`). File found → stop and ask: resume (append to the
   same record, jump past completed phases; re-verify each approved change against current
   content before applying) or discard (move to `abandoned-runs\`, never delete). Never
   decided automatically.
2. **Continuous checkpointing** — one file, `in-progress\<run-timestamp>.md`, appended
   unconditionally after every phase: learnings count, backup result, the full verbatim
   change report, approval decisions verbatim, exact before/after per edit, per-operation
   records, verification result, commit/push result, learnings one-liners inline.
3. **Phase −1 — Load learnings.** Read every file in `...\mb-docs-manager\Learnings\`;
   carry forward. Learnings overrule SKILL.md on scope/classification/recommendation —
   never on the three hard constraints.
4. **Phase 0 — Pre-flight + backup.** (a) `git status` on all 12 Active Repositories from
   `projects-config-register.md`'s GitHub-repositories section — any dirty repo aborts the
   entire run (`REPOS_DIRTY`) before backup; (b) discover the six managed types across the
   scaffold-defined in-scope walk (scaffold read first, it wins), copy them to
   `C:\backup-mb-docs-manager\<run-timestamp>\` preserving relative paths, then **verify by
   direct file count** — mismatch is `BACKUP_FAILED`, abort.
5. **Phase 1 — Scan** (read-only): read the 3 pinned documents + every discovered managed
   document; walk in-scope folders (existence/structure only); extract and resolve internal
   references; apply per-type update rules incl. `verified:` date proposals; exact counts; a
   concrete recommendation on every flagged item. Anvil code repos: top-level existence-check
   only, contents never opened.
6. **Phase 2 — Report, in two tiers:**
   - **Standard tier** — text edits grouped by folder×type; one-line header with count per
     group ("docmap.md — pointer corrections, 12 items"); every item individually listed;
     **one yes/no decision per group**; a group may be rejected and taken item-by-item.
   - **High-risk tier** — own section, grouped and labelled by risk type in bold
     (`HIGH RISK — renames/moves (2 items)`); **every item approved individually**, never
     batch; file-system operations keep the second confirmation.
   - Plus: proposed file-system operations table (separate — never a delete; a delete is a
     move to `obsolete\`), flagged anomalies with recommendations, newly discovered documents.
7. **Phase 3 — Approval.** Three embedded rules: (a) push approval is a separate decision,
   recorded verbatim — no explicit yes = Phase 6 skipped; (b) **AGENTS.md edits require the
   developer naming the exact file** in the reply — a batch "approved" without naming
   authorizes nothing on AGENTS.md; (c) resolved anomalies become approved changes +
   learning candidates.
8. **Phase 3a — Grant handover (conditional).** Approved edits targeting folders outside the
   shared-library list: group by folder, drop always-open folders, construct the **entire
   request set as ONE copy-pasteable block** (count = approved files per folder + 2):
   ```bash
   mg-grant --path <folder-1> --count <n1>
   mg-grant --path <folder-2> --count <n2>
   ```
   Hand it to the developer (the skill never invokes `mg-grant` itself); verify every entry
   in `~/.config/cupcake/policies/opencode/cup-grants-data.rego` before Phase 4a; apply
   immediately (slips ~30 min, decrement per use); lapsed/short slip → re-request; a denied
   write → stop and report — never worked around.
9. **Phase 4a — Apply text edits** (sub-agent: edit-only, no bash). Approved items only.
10. **Phase 4b — Apply file-system operations** (separate sub-agent: bash-only, no edit).
    Rename/move/copy only; **never deletes**; second explicit confirmation immediately
    before execution, always; no obvious `obsolete\` destination → flag back, don't guess.
11. **Phase 5 — Verify** (read-only): re-read changed docs, re-resolve references, confirm
    no new breakage.
12. **Phase 6 — Commit & push.** Only under recorded push approval + clean verification.
    **Step 0: commit plan** — one table (repo, folders touched, file count), **one batch
    approval for the whole set**, then one commit per repo. Then: resolve git-tracked
    filenames via `git ls-files --full-name` (NTFS case-insensitivity); stage only changed
    files (never `git add -A`); commit message `mb-docs-manager: <run-timestamp> — N changes
    applied`; commit locally regardless of remote; validate via `git ls-remote --heads origin`
    then push; failure → `PUSH_FAILED` reported immediately, local commit stands. Per-repo
    results to `C:\mybizz\logs\github-logs\commit-push-<date>.md`.
13. **Phase 7 — Log.** `C:\mybizz\logs\mb-docs-manager\<timestamp>.md` (timestamp = run
    completion time) — structured fields only, exact counts.
14. **Phase 8 — Update learnings (mandatory when changes were applied).** One file per
    learning, `Learnings\<timestamp>-<short-topic>.md` (Context / Decision / Applies to);
    verify at least one file matches this run's timestamp — no file = process failure,
    report it. No novel judgment calls → write the explicit minimal learning.
15. **Phase 9 — Completion gate.** (1) `division-maps` re-scan of the three pinned documents;
    (2) GitHub confirmation prompt (separate question); (3) GBrain sync prompt (separate
    question — the orchestrator launches `setsid bash /mnt/c/mybizz/scripts/sync-gbrain.sh`,
    never the skill); (3a) after 4b structural changes: static mb-align-docs reminder;
    (4) closing git-status snapshot → `github-logs\git-status-<date>.md`; (5) checkpoint
    completeness check — missing entry = process failure; (6) move `in-progress\` record to
    `last-completed-run\` (update its H1 title), leaving `in-progress\` empty.

## Hard constraints (operational form)

1. **Nothing is written except in Phase 4a/4b**, and only developer-approved changes — 4b
   additionally requires a second explicit confirmation. Exemptions (create-only): Phase 0
   backup, Phase 7 log, Phase 8 learnings, continuous checkpointing. **Creation of any
   managed document type is permanently out of scope.** **Phase 4b never deletes.**
2. **Phase 0 runs in full, in order, every invocation** — git-status pre-flight (dirty →
   abort whole run) then verified backup (verification failure → abort). Neither skippable.
3. **Never run `gbrain sync` or any GBrain state-changing command.** Read-only inspection
   only, where the procedure calls for it.

## Anomaly classes

| Class | Action |
|---|---|
| REPOS_DIRTY | Abort entire run before backup — developer cleans, re-invokes |
| BACKUP_FAILED | Abort entire run — no scan |
| BROKEN / MISMATCHED / AMBIGUOUS / MISSING / UNDOCUMENTED / COUNT MISMATCH / STALE DATE | Propose fix or flag with recommendation; never guess |
| CODE_REPO_AMBIGUOUS | Flag with recommendation; never auto-resolve. `makepdlf` placeholder exempt per learning |
| GRANT_REQUIRED | Phase 3a handover — one copy-paste block; never work around |
| NO_REPO | Report under "Skipped — Not a Git Repository" — expected, not an error |
| PUSH_FAILED | Report immediately — local commit stands; push retried manually |

## Do not

- Do not write anything outside Phase 4a/4b, and never unapproved changes.
- Do not create any managed document — missing ones are findings.
- Do not delete anything — a delete is a move to `obsolete\`.
- Do not skip, reorder, or ask about Phase 0.
- Do not report an unverified backup as successful.
- Do not run `gbrain sync` or change GBrain state.
- Do not run `git add -A` or stage beyond the approved change set.
- Do not invoke `mg-grant` on your own initiative — hand the block to the developer.
- Do not work around a policy denial — stop and report.
- Do not edit the scope scaffold — scope changes are the developer's.
- Do not touch `anvil.yaml` — ever, in any way.
- Do not open, read, or edit anything inside an Anvil code repo — including
  `theme\assets\docs`.
- Do not use vague quantifiers — exact counts, every document named.
- Do not start without a target, and do not assume one when it is omitted.
