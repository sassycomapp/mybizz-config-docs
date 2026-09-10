---
document: "align-docs — Reference"
doc-id: align-docs-reference
state: Live
date-created: 2026-09-10
---

# align-docs — Reference

Execution procedure for the `mb-align-docs` skill (V2). `SKILL.md` and
`mb-align-docs-function-scope.md` (locked) in the installed folder
(`~/.config/opencode/skills/mb-align-docs/`) are the authoritative
definitions; this document is the operational form. Why the rules are
shaped this way: `align-docs-explainer.md`.

## Invocation

- `/mb-align-docs (all)` — wide sweep: every in-scope project library (per the scope
  scaffold `mybizz-scope-list.md`) plus `project-library-global`, processed sequentially.
- `/mb-align-docs (slug)` — one named project's `{slug}-project-library` plus
  `project-library-global` (global is always included, never run alone).
- **Empty or omitted target: the skill asks and does nothing until answered.** Never assumed.
- **A code repo is not a valid target** — Anvil code repos are denied entirely (including
  `theme\assets\docs` inside them); the skill states the denial and asks for a
  planning-corpus target.
- Manual invocation only — no autonomous scheduling.

## Phase procedure

1. **Phase −2 — Resume check.** Check `C:\mybizz\logs\mb-align-docs\in-progress\` for an
   unfinished run against the target. Found → offer resume (pick up exactly where it left
   off, including decisions made) or discard (move to `abandoned-runs\`, never delete).
   Never decided automatically.
2. **Phase −1 — Load learnings.** Read `...\mb-align-docs\learnings\` for the target project
   and global. Prior corrections steer this run. Learnings never authorize a write, skip a
   backup, or bypass approval.
3. **Phase 0 — Precondition + backup.** `git status` must be clean on the target project and
   on `project-library-global` — either dirty stops the run immediately. Then take a
   count-verified backup to `C:\backup-mb-align-docs\<timestamp>\` (`<timestamp>` =
   `YYYY-MM-DDTHHMMSS+0200`, per `adr-timezone-utc-storage-display-conversion.md`). Backup
   verification failure stops the run cold — no exceptions.
4. **Phase 1 — Detect** (detector sub-agent, read-only): scan the declared target folder (or,
   in wide mode, each in-scope target in turn); run the register enforcement diff (live
   folders vs `register-global\` and `register-local\` — **register always wins**); check
   directionality; check the versioning rule (any reference to a non-`Live` target is a
   drift item); run the missing/incomplete-front-matter checks (proposing identity for bare
   documents; only missing fields for incomplete ones). Progress checkpointed to
   `in-progress\` as it goes.
5. **Phase 2 — Report, in two tiers:**
   - **Standard tier** — reference-healing and front-matter findings, grouped by target then
     finding type; one-line header with count per group; every item individually listed;
     **one yes/no decision per group**; a group may be rejected and taken item-by-item.
     (Front-matter findings across a run may batch as one group — same type, same
     remediation path.)
   - **High-risk tier** — own section, grouped and labelled by risk type in bold:
     `HIGH RISK — identifier changes (N items, corpus-wide sweep each)`,
     `HIGH RISK — register mismatches (N items — rename-to-match or retire, decided each)`,
     `HIGH RISK — quarantine moves (N items)`. **Each item approved individually** — never
     batch — and structural actions keep the Phase 4b second confirmation.
6. **Phase 3 — Approve.** Per finding, individually — no batch approval across unrelated
   findings (the same-type front-matter exception above is the only batch). Resolved
   anomalies become learning candidates.
7. **Phase 3a — Grant handover (conditional).** Approved edits targeting folders outside the
   cross-project rule's shared-library list: construct the **entire request set as ONE
   copy-pasteable block**:
   ```bash
   mg-grant --path <folder-1> --count <n1>
   mg-grant --path <folder-2> --count <n2>
   ```
   Hand it to the developer (never invoke `mg-grant` on the skill's own initiative); verify
   every entry in `~/.config/cupcake/policies/opencode/cup-grants-data.rego` before
   applying; apply immediately (slips ~30 min, decrement per use); any policy denial at
   apply time → stop and report — never worked around.
8. **Phase 4a — Apply — text** (writer-text: edit-only, no bash). Approved reference-healing
   repoints, missing-front-matter insertions, incomplete-front-matter field additions. Every
   write followed by an immediate re-read to confirm it resolved the finding.
9. **Phase 4b — Apply — structural** (writer-structural: edit+bash). Approved
   identifier-change renames **plus their immediate corpus-wide sweep** (project + global,
   same session, visibly); register mismatch actions (rename-to-match-register or retire —
   the only two options); Quarantine moves (copy + provenance block + no live reference left
   pointing there). Second explicit confirmation immediately before execution, always.
   **Never deletes** — retirement is a state flip; quarantining is copy-then-remove-references.
10. **Phase 5 — Verify** (per writer): re-read/re-check what was just written; confirm it
    resolved the approved finding before moving to the next.
11. **Phase 6 — Commit / Log** (logger: append-only). **Commit plan first:** one table —
    repo, folders touched, file count — **one batch approval**, then one commit per repo
    (`mb-align-docs: <run-timestamp> — N findings processed`). One append-only
    alignment-log entry per finding — including rejected and skipped ones (the log reflects
    every decision, not only the writes). Per finding-type entry contents per
    `alignment-log-template.md`.
12. **Phase 7 — Learnings (close).** Write back notable judgment calls
    (`learnings\<timestamp>-<short-topic>.md`); move the run record from `in-progress\` to
    `last-completed-run\`.

## Hard constraints (operational form)

- No writes without approval — Detect and Report never touch a file.
- Structural writes require approval **plus** the Phase 4b confirmation.
- Mandatory count-verified backup before any write phase — failure stops the run cold.
- Git-clean precondition on the target project and global — either dirty refuses Detect.
- No deletion of content — heal, retire, or quarantine only; emptying Quarantine/Obsolete is
  out of scope.
- No autonomous state-changing commands — the detector cannot invoke a writer.
- One target in flight at a time (wide mode sequences targets; it never merges them) — the
  one exception is an approved identifier change, which triggers the corpus-wide sweep
  immediately, visibly, before Apply proceeds.
- Grant handover for cross-project writes — one copy-pasteable block, never self-invoked.
- **Anvil code repos denied entirely** — including `theme\assets\docs`.
- A lost session never loses work — resume picks up exactly where it left off.

## The two operations (never share a remediation path)

| Operation | Nature | Route | Sweep |
|---|---|---|---|
| Reference healing | Local, frequent — a link points somewhere that moved | writer-text | none — one folder at a time |
| Identifier change | The thing's canonical name is changing, not just a pointer | writer-structural | **corpus-wide, immediate, same session, on approval** |

## Directionality rules (enforced during Detect)

| Direction | Status |
|---|---|
| Global → Global | permitted |
| Global → Local | **never permitted** |
| Local → Global | permitted (global is stable, referenced "blind") |
| Local → Local, same project | permitted |
| Local → Local, cross-project | **never live** — Quarantine copy with provenance, via writer-structural |

## Finding types

| Type | Route | Approval |
|---|---|---|
| reference-healing | writer-text (4a) | standard tier — batched by target×type |
| missing-front-matter | writer-text (4a) | standard tier — batch permitted (same type) |
| incomplete-front-matter | writer-text (4a) | standard tier — batch permitted (same type) |
| identifier-change | writer-structural (4b) | **HIGH RISK — individual + second confirmation** |
| register-mismatch | writer-structural (4b) | **HIGH RISK — individual + second confirmation; two options only: rename-to-match or retire** |
| quarantine move | writer-structural (4b) | **HIGH RISK — individual + second confirmation** |

## Do not

- Do not write anything without an explicit, on-record approval for that exact finding.
- Do not batch-approve high-risk items — identifier changes, register actions, and
  quarantine moves are always individual decisions plus the second confirmation.
- Do not delete content — heal, retire, or quarantine only.
- Do not edit front matter of an existing document beyond adding approved missing fields.
- Do not let any trackable reference resolve into Quarantine or Obsolete — heal or remove,
  no third option.
- Do not create a third option for a register mismatch — rename-to-match or retire.
- Do not run against out-of-scope projects (mb4ecom, mb5pdlf, project-template) or
  `C:\pdlf` — scaffold scope governs wide mode.
- Do not open anything inside an Anvil code repo — including `theme\assets\docs`.
- Do not flag templates, `devlog-index.md`/`judgement-trail.md`, or UI build artefacts as
  front-matter gaps — their lack of front matter is correct by design.
- Do not invoke `mg-grant` on the skill's own initiative — hand the block to the developer.
- Do not edit front matter to carry references — front matter is identity only.
- Do not start without a target, and do not assume one when it is omitted.
