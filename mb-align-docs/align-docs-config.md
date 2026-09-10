---
document: "align-docs — Config"
doc-id: align-docs-config
state: Live
date-created: 2026-09-10
---

# align-docs — Config

State of the `mb-align-docs` skill as of 2026-09-10. All facts verified
live this date unless noted. Skill version: **V2** (target grammar +
wide mode + Anvil denial, 2026-09-10; function scope locked V2).

## Identity

| Field | Value |
|---|---|
| Component | `mb-align-docs` — first-party custom OpenCode skill (developer-built) |
| Role | Document-consistency checker — content agreement, cross-references, document identity/lifecycle |
| Invocation | `/mb-align-docs (all)` — wide sweep; `/mb-align-docs (slug)` — one project (+ global always); empty/omitted target → the skill ASKS, never assumes |
| Version | V2 (`version: V2`, `status: active`); function scope locked at V2 (2026-09-10, amending locked V1 of 2026-07-24) |
| Language | Natural-language procedure + 4 sub-agent definition files; no executable code |

## File inventory

| Location | Files |
|---|---|
| This folder (canonical suite) | `align-docs-config.md`, `align-docs-reference.md`, `align-docs-explainer.md` |
| Installed skill — `~/.config/opencode/skills/mb-align-docs/` | `SKILL.md` (V2, 301 ln), `mb-align-docs-function-scope.md` (locked V2), `mb-align-docs-detector.md`, `mb-align-docs-writer-text.md`, `mb-align-docs-writer-structural.md`, `mb-align-docs-logger.md`, `front-matter-schema.md`, `register-template.md`, `quarantine-provenance-template.md`, `alignment-log-template.md`, `finding-report-format.md`, `mb-align-docs-README.md` |
| Artifacts documented, not deleted | 2 `:Zone.Identifier` files (README, former explainer) |
| Former in-folder explainer | `mb-align-docs-explainer.md` (27 KB) — superseded by this suite; pending obsolete-move to `C:\mybizz\archive\` |

## Skill package structure

| Piece | Role |
|---|---|
| SKILL.md | Phases, sub-agents, hard constraints, invocation grammar, scope rules |
| function-scope.md (locked) | What the skill exists to do — two operations, directionality, Quarantine, identity, versioning, registers, exclusions; V2 amendments appended |
| detector.md | Sub-agent, read-only (edit deny, bash deny) — Detect + Report |
| writer-text.md | Sub-agent, edit-only — reference healing + front-matter insertion |
| writer-structural.md | Sub-agent, edit+bash — identifier changes, register actions, Quarantine moves; second-confirmation gated |
| logger.md | Sub-agent, append-only — log, git commit, learnings, run close-out |
| front-matter-schema.md | The four required fields + timestamp format |
| 4 templates | register, quarantine provenance, alignment log, finding report format |

## Target grammar and scope (V2)

| Element | Value |
|---|---|
| Grammar | `(all)` / `(slug)` / empty-asks — shared across all three documentation skills |
| Wide mode | Every in-scope project library (per scaffold `mybizz-scope-list.md`) + `project-library-global`, processed sequentially; one target in flight at a time; per-target checkpointing; per-target commit (batch-approved commit plan) |
| Scope rule (unchanged) | Named project's `{slug}-project-library` **plus** `project-library-global` unconditionally — directionality checks need both sides |
| Anvil code repos | **Denied entirely (V2)** — never opened/read/backed-up/edited, including `theme\assets\docs` inside them (Anvil app assets); top-level paths existence-checked on reference only |
| Front-matter exclusions | `templates-global`/`templates-local` (categorical); `devlog-index.md`/`judgement-trail.md` (historical logs); UI build artefacts (`*.html`, `*.png` under `ui\{package}\{form}\`) |
| Alignment targets under the scaffold | mb-3-cs, makepdlf project libraries + project-library-global (mb4ecom/mb5pdlf out of scaffold scope) |

## Core rules (function scope, locked)

| Rule | Content |
|---|---|
| Two operations | Reference healing (local, frequent → writer-text) and identifier change (global effect, rare → writer-structural + corpus-wide sweep on approval). Never share a remediation path |
| Directionality | Global→Global ✓; Global→Local never; Local→Global ✓; Local→Local same project ✓; Local→Local cross-project never live — Quarantine copy with provenance |
| Front matter | Identity only — never carries references; set once, never edited; state ∈ `Live`/`Retired`/`Quarantine`; required fields: document, doc-id, state, date-created |
| Versioning | One Live version at a time; supersession = new document + new front matter, old flips `Retired`; no live reference to a non-Live target, ever |
| Register enforcement | Register always wins; new global file → appended on approval; renamed/diverged global file → exactly two options: rename-to-match-register or retire (Phase 4b gated); no bypass except run abort |
| Timestamps | `YYYY-MM-DDTHHMMSS+0200` (Filename-Safe ISO 8601, UTC+2) per `adr-timezone-utc-storage-display-conversion.md` |

## Phases

−2 resume → −1 learnings (project + global) → 0 pre-flight (git-clean on target + global) + verified backup → 1 Detect (detector) → 2 Report (two-tier: standard batched by target×type, high-risk grouped + labelled by risk type, individually approved) → 3 Approve (per finding; batch only for same-type front-matter groups) → 4a text apply → 4b structural apply (second confirmation) → 5 verify → 6 commit/log (batched commit plan: one table, one approval, one commit per repo) → 7 learnings + close-out.

## Operational state (live, 2026-09-10)

| Item | Value |
|---|---|
| Runs completed | **None** — log infrastructure fully scaffolded but all folders empty; the skill has never completed a run |
| `C:\mybizz\logs\mb-align-docs\` | learnings / in-progress / last-completed-run / abandoned-runs — all empty |
| `C:\backup-mb-align-docs\` | exists, empty (no snapshots yet) |
| Global register | `project-library-global\register-global\register-global.md` — 158 table rows; regenerated 2026-08-27; corrected 2026-09-01 (rules-cupcake-global + security-global added) |
| Local register | `register-local\` present in project libraries (e.g. mb-3-cs) |
| Global quarantine | `project-library-global\quarantine\` exists |
| skill-index status | "mb-align-docs — working" |
| V2 remediations applied | backup path canonicalized (`C:\backup-mb-align-docs\<timestamp>\` — fixed a three-way contradiction: SKILL said `C:\backups-general\...` [nonexistent], README said `C:\backup-mb-align-docs\<timestamp>\` [correct]); ADR citation fixed in 7 files (was missing the `adr-` prefix); stale `global-0037` identifier removed; README inventory path re-pointed from the removed `projects-reference` tree; broken dev-root README pointer fixed; retired `project-inventory` references replaced with the register |

## Cross-cutting integration

| System | Finding |
|---|---|
| Cupcake | No component-specific rule. Cross-project writes → grant-handover block (one copy-pasteable `mg-grant` set); git commit/push → batched commit plan under approval. Enforcement status of Cupcake is not fixed — live status: `cupcake-config.md` Current Operational Status |
| Memory Governor | None found |
| security-global | None found |
| Related skills | mb-docs-manager (deliberately NON-interoperating companion — structure vs content; its Phase 9 reminder points here after structural changes); mb-wikilinks (must run BEFORE align-docs so references validate against the final `[[wikilink]]` convention); mb-sysdoc-creator (produced this suite) |

## Open items

1. **Never run yet** — first real run is the planned wide-mode run (after all three suites exist); expect first-run findings at volume; the two-tier approval exists for exactly that.
2. **Run order (corrected 2026-09-10):** mb-docs-manager → mb-wikilinks → mb-align-docs — align-docs must validate the final reference convention, per wikilinks' own design note.
3. Old skill-folder explainer: obsolete-move to archive pending (same pattern as docs-manager).
4. Front-matter growth (e.g. PDLF step-linkage): deliberately deferred — identity-only stays small; additions would arrive via a broad-sweep insertion decision when PDLF actually needs them.
5. Anvil-hosted documentation (`theme\assets\docs`): standing research task (Anvil's formatting expectations; whether wikilinks can ever resolve there) — feeds a future decision; does not block anything since code repos are denied.
6. The 2 `:Zone.Identifier` artifacts: documented, not deleted (standing pattern).
