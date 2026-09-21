---
document: "align-docs — Reference"
doc-id: align-docs-reference
state: Live
date-created: 2026-09-10
---

# align-docs — Reference

Execution procedure for the `mb-align-docs` skill (V2.1). `SKILL.md` and
`mb-align-docs-function-scope.md` (locked) in the installed folder
(`~/.config/opencode/skills/mb-align-docs/`) are the authoritative
definitions; this document is the operational form. Updated 2026-09-20 to
reflect `SKILL.md` V2.1 (2026-09-19: scope from the single authority list,
shared run frame, roles as permission disciplines, es.exe-first search).
Why the rules are shaped this way: [[align-docs-explainer|Explainer]].

## Invocation

- `/mb-align-docs (all)` — wide sweep: every in-scope corpus (per the scoping list
  [[mybizz-scope-list|Mybizz Scope List]]) plus `project-library-global`, processed sequentially, one
  target in flight at a time.
- `/mb-align-docs (slug)` — one named in-scope corpus — e.g. `pdlf`,
  `makepdlf-project-library`, `mb-3-cs-project-library`, `mybizz-os-docs`,
  `mybizz-config-docs`, `data-mybizz-mgt` — with `project-library-global` always
  included (never run alone; directionality checks require both sides present).
- **Empty or omitted target: the skill asks and does nothing until answered.** Never assumed.
- **A code repo is not a valid target** — Anvil code repos are denied entirely (including
  `theme\assets\docs` inside them); the skill states the denial and asks for a
  planning-corpus target.
- Manual invocation only — no autonomous scheduling.

## Scope rule

Scope comes from the scoping list
([[mybizz-scope-list|Mybizz Scope List]]) — the single scope
authority for every documentation skill, read at Phase 0 of every run. The skill never
carries its own scope list. In-scope roots: `C:\data-mybizz-mgt`, `C:\dev`, `C:\mybizz`,
`C:\pdlf`; exceptions only as listed there. The list's criterion governs: an exception is
content never referenced at any time; transient state (a project under development)
schedules the work, never removes scope. If asked to extend scope to an excepted path,
stop and confirm explicitly with the developer — the scoping list is the only
authorization for scope.

`project-library-global` remains unconditionally in scope alongside every named target.
Project-level config refinements (e.g. `pdlf-config.yaml`'s folder in_scope flags) remain
valid treatment guidance within their project.

## Run-state discipline — mandatory, end to end

The shared run frame (resume check, learnings load, git-clean precondition, verified
stop-cold backup, decision-point checkpointing, run-record lifecycle, approvals in chat,
permission discipline, verification, commit plan and per-source GBrain sync, es.exe-first
search, Anvil code repos denied) is defined once in
[[doc-skills-run-discipline|Shared Run Discipline]] and is
mandatory for every run. This skill adds its own specifics:

- The working record lives at
  `C:\mybizz\logs\mb-align-docs\in-progress\<run-timestamp>.md` (Filename-Safe ISO 8601,
  UTC+2) and carries the full findings report, approval decisions verbatim, exact
  before/after per edit, and verification results.
- At close the record MOVES to `last-completed-run\` (never deleted) and ONE index row is
  appended to `C:\mybizz\logs\mb-align-docs\run-index.md` — the permanent audit trail;
  the full record is kept only for the most recent run.
- The alignment log remains append-only, one entry per approved-and-applied finding (per
  `alignment-log-template.md`); existing per-run records in the folder root are
  historical and remain untouched.

## Phase procedure

**Run order:** align-docs runs BEFORE mb-wikilinks — it validates and heals references in
their existing written form; wikilinks then packages them. Product-then-packaging.

1. **Phase −2 — Resume check.** Check `C:\mybizz\logs\mb-align-docs\in-progress\` for an
   unfinished run against the target. Found → offer resume (pick up exactly where it left
   off, including decisions made) or discard (move to `abandoned-runs\`, never delete).
   Never decided automatically.
2. **Phase −1 — Load learnings.** Read `...\mb-align-docs\learnings\` for the target
   corpus and global. Prior corrections steer this run. Learnings never authorize a
   write, skip a backup, or bypass approval.
3. **Phase 0 — Scope + Precondition + backup.** Read the scoping list and derive the
   run's targets from it. `git status` must be clean on the target project and on
   `project-library-global` — either dirty stops the run immediately. Then take a
   count-verified backup to `C:\backup-mb-align-docs\<timestamp>\` (`<timestamp>` =
   `YYYY-MM-DDTHHMMSS+0200`, per [[adr-timezone-utc-storage-display-conversion|Client Timezone: IANA String, UTC Storage, Display-Time Conversion]]).
   Backup verification failure stops the run cold — no exceptions.
4. **Phase 1 — Detect** (read-only role): scan the declared target folder (or, in wide
   mode, each in-scope target in turn); run the register enforcement diff (live folders
   vs `register-global\` and `register-local\` — **register always wins**); check
   directionality; check the versioning rule (any reference to a non-`Live` target is a
   drift item); run the missing/incomplete-front-matter checks (proposing identity for
   bare documents; only missing fields for incomplete ones). Progress checkpointed to
   `in-progress\` as it goes.
5. **Phase 2 — Report, in two tiers:**
   - **Standard tier** — reference-healing and front-matter findings, grouped by target
     then finding type; one-line header with count per group; every item individually
     listed; **one yes/no decision per group**; a group may be rejected and taken
     item-by-item. (Front-matter findings across a run may batch as one group — same
     type, same remediation path.)
   - **High-risk tier** — own section, grouped and labelled by risk type in bold:
     `HIGH RISK — identifier changes (N items, corpus-wide sweep each)`,
     `HIGH RISK — register mismatches (N items — rename-to-match or retire, decided
     each)`, `HIGH RISK — quarantine moves (N items)`. **Each item approved
     individually** — never batch — and structural actions keep the Phase 4b second
     confirmation.
6. **Phase 3 — Approve.** Per finding, individually — no batch approval across
   unrelated findings (the same-type front-matter exception above is the only batch).
   Approval questions are asked in chat, never the question tool. Resolved anomalies
   become learning candidates.
7. **Phase 3a — Grant handover (conditional).** Approved edits targeting folders outside
   the cross-project rule's shared-library list: construct the **entire request set as
   ONE copy-pasteable block**:
   ```bash
   mg-grant --path <folder-1> --count <n1>
   mg-grant --path <folder-2> --count <n2>
   ```
   Hand it to the developer (never invoke `mg-grant` on the skill's own initiative);
   verify every entry in `~/.config/cupcake/policies/opencode/cup-grants-data.rego`
   before applying; apply immediately (slips ~30 min, decrement per use); any policy
   denial at apply time → stop and report — never worked around.
8. **Phase 4a — Apply — text** (text-correction role: edit-only, no bash). Approved
   reference-healing repoints, missing-front-matter insertions, incomplete-front-matter
   field additions. Every write followed by an immediate re-read to confirm it resolved
   the finding.
9. **Phase 4b — Apply — structural** (structural role: edit+bash). Approved
   identifier-change renames **plus their immediate corpus-wide sweep** (project +
   global, same session, visibly); register mismatch actions (rename-to-match-register
   or retire — the only two options); Quarantine moves (copy + provenance block + no
   live reference left pointing there). Second explicit confirmation immediately before
   execution, always. **Never deletes** — retirement is a state flip; quarantining is
   copy-then-remove-references.
10. **Phase 5 — Verify** (per writer role): re-read/re-check what was just written;
    confirm it resolved the approved finding before moving to the next.
11. **Phase 6 — Commit / Log** (logging role: append-only). **Commit plan first:** one
    table — repo, folders touched, file count — **one batch approval**, then one commit
    per repo (`mb-align-docs: <run-timestamp> — N findings processed`). One append-only
    alignment-log entry per approved-and-applied finding, per
    `alignment-log-template.md`. Then GBrain per-source sync + embed for every changed
    source; verify `gbrain sources list` last-sync timestamps before reporting done.
12. **Phase 7 — Learnings (close).** Write back notable judgment calls
    (`learnings\<timestamp>-<short-topic>.md`); move the run record from `in-progress\`
    to `last-completed-run\`; append the run-index row.

This skill is the close-out hook of the register maintenance model: it is offered at
task close-out ("run mb-align-docs on the project just worked on?") after content
changes, alongside the commit/push and GBrain standing questions. Manual only — no
scheduled runs. The preferred mechanism is registration at the source (creation-time
hooks in doc-creating skills); this skill reconciles what those hooks miss and validates
them.

## Roles — permission discipline (no sub-agents)

The write classes are permission disciplines, enacted by the orchestrating agent —
never spawned as sub-agents (standing workchat rule 8):

- **Detection** — read-only. Never writes.
- **Text-level corrections** — reference repoints (healing fixes) and front-matter
  insertion. Cannot rename, move, or retire a file.
- **Structural actions** — identifier-change renames plus their triggered sweep,
  register rename/retire, Quarantine moves. Require the second confirmation gate in
  addition to standard approval.
- **Logging** — append-only.

## Hard constraints (operational form)

- No writes without approval — Detect and Report never touch a file.
- Structural writes require approval **plus** the Phase 4b confirmation.
- Mandatory count-verified backup before any write phase — failure stops the run cold.
- Git-clean precondition on the target project and global — either dirty refuses Detect.
- No deletion of content — heal, retire, or quarantine only; emptying Quarantine/Obsolete
  is out of scope.
- No autonomous state-changing commands — detection cannot invoke a writer.
- One target in flight at a time (wide mode sequences targets; it never merges them) —
  the one exception is an approved identifier change, which triggers the corpus-wide
  sweep immediately, visibly, before Apply proceeds.
- Grant handover for cross-project writes — one copy-pasteable block, never self-invoked.
- **Anvil code repos denied entirely** — including `theme\assets\docs`.
- A lost session never loses work — resume picks up exactly where it left off.

## Missing documents — the hard-won rule

Every corpus document was researched and built deliberately. When Detect encounters a
reference or register row whose target is not on disk, it investigates before proposing
anything: whole-corpus search for moved/renamed copies (**es.exe first** —
`es.exe <basename>` returns every path on the system bearing that name; filter to the
corpus sources; raise `-n` (≥20) or scope with `-p` before filtering); the register's
supersession chain; git history (`git log --follow`) for a deletion commit and its
message; the backup folders (`C:\backup-mb-align-docs\`, `C:\backup-general\`) and the
archive. A zero-hit es.exe result on a supposedly existing file is verified with one
fallback check before any missing/Retire finding is proposed. A Retire proposal is made
only when the document is genuinely unfindable with no successor, with the investigation
documented — and the developer decides.

## The two operations (never share a remediation path)

| Operation | Nature | Route | Sweep |
|---|---|---|---|
| Reference healing | Local, frequent — a link points somewhere that moved | text corrections | none — one folder at a time |
| Identifier change | The thing's canonical name is changing, not just a pointer | structural | **corpus-wide, immediate, same session, on approval** |

## Directionality rules (enforced during Detect)

| Direction | Status |
|---|---|
| Global → Global | permitted |
| Global → Local | **never permitted** |
| Local → Global | permitted (global is stable, referenced "blind") |
| Local → Local, same project | permitted |
| Local → Local, cross-project | **never live** — Quarantine copy with provenance, via structural |

## Versioning rule (enforced during Detect)

No live reference may resolve to a document whose front-matter `state` is not `Live`.
A reference to a `Retired` or `Quarantine` document is always a drift item — heal to
the current live version, or remove.

## Finding types

| Type | Route | Approval |
|---|---|---|
| reference-healing | text corrections (4a) | standard tier — batched by target×type |
| missing-front-matter | text corrections (4a) | standard tier — batch permitted (same type) |
| incomplete-front-matter | text corrections (4a) | standard tier — batch permitted (same type) |
| identifier-change | structural (4b) | **HIGH RISK — individual + second confirmation** |
| register-mismatch | structural (4b) | **HIGH RISK — individual + second confirmation; two options only: rename-to-match or retire** |
| quarantine move | structural (4b) | **HIGH RISK — individual + second confirmation** |

## Do not

- Do not write anything without an explicit, on-record approval for that exact finding.
- Do not batch-approve high-risk items — identifier changes, register actions, and
  quarantine moves are always individual decisions plus the second confirmation.
- Do not ask approvals through the question tool — approvals are asked in chat.
- Do not delete content — heal, retire, or quarantine only.
- Do not edit front matter of an existing document beyond adding approved missing fields.
- Do not let any trackable reference resolve into Quarantine or Obsolete — heal or
  remove, no third option.
- Do not create a third option for a register mismatch — rename-to-match or retire.
- Do not run outside the scoping list — it is the single scope authority; extending
  scope to an excepted path requires explicit developer confirmation.
- Do not open anything inside an Anvil code repo — including `theme\assets\docs`.
- Do not flag templates, `devlog-index.md`/`judgement-trail.md`, or UI build artefacts
  as front-matter gaps — templates lack front matter by design; devlog/judgement files
  are registered documents whose missing front matter IS a finding; UI renders carry
  identity by register row, not front matter.
- Do not invoke `mg-grant` on the skill's own initiative — hand the block to the
  developer.
- Do not edit front matter to carry references — front matter is identity only.
- Do not spawn sub-agents for the write classes — they are permission disciplines
  enacted by the orchestrating agent.
- Do not start without a target, and do not assume one when it is omitted.
