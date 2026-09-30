---
title: "doc-auditor-config"
doc-id: "mb-2abc22b9"
---
# mb-doc-auditor — Configuration

Canonical current-state configuration record for `mb-doc-auditor` as a
division-wide system component. Agent-facing. Reflects the live-verified state
as of 2026-09-25. States facts, not history — reasoning in
[[doc-auditor-explainer|Explainer]]; commands and procedures in
[[doc-auditor-reference|Reference]].

---

## Identity

| Item | Value |
|---|---|
| Component | `mb-doc-auditor` — periodic and on-demand documentation-audit skill (wider estate) |
| Governing contract | `C:\mybizz\mybizz-config-docs\gbrain\gbrain-doc-contract.md` (Level A authority; consumed read-only, change-controlled by developer decision) |
| Source repo | `C:\mybizz\mb-doc-auditor` — git-initialized; GitHub `sassycomapp/mb-doc-auditor` (private); pushed at `aa91ff7` |
| Source artifact | `C:\mybizz\mb-doc-auditor\mb-doc-auditor-skill.md` — corpus two-field frontmatter (`title`/`doc-id` = `mb-doc-auditor-skill`); `SKILL.md` exists only at the managed install location |
| Installed skill | `~/.config/opencode/skills/mb-doc-auditor/SKILL.md` — OpenCode frontmatter (`name: mb-doc-auditor` + description); body byte-identical from H1; hash pair `8e0def60659e0854` (source) / `42790f675a784bdd` (installed), 2026-09-25 |
| Governing plan | `C:\data-mybizz-mgt\desktop\doc-auditor-maintaner-planning\mb-doc-auditor-Complete Consolidated Plan.md` (final; amendments A–H applied 2026-09-25; all decisions locked) |

## Component layout (source repo)

| Path | Role |
|---|---|
| `tool/scope.py` | scope reader + estate scanner (O5): parses the scope authority live; applies authority exceptions, the Anvil class rule (anvil.yaml folders never read), and treatment exclusions (`tmp-`, stencils, quarantine, backups, catalogue, logs); register discovery by walking up (both layouts); read-only |
| `tool/runlog.py` | maintainer run-log evidence reader (hard-wired to `doc-maintainer-run-log.md`); absent/empty → "no maintenance history available"; evidence, never a work queue |
| `tool/gbrain_reader.py` | read-only gbrain CLI wrappers (`sources list`, `orphans`) for G9/G10 verification; failure → `unavailable`, classified Can wait |
| `tool/record.py` | audit-record appender: one append-only block per run; creates the file with two-field frontmatter + register row on first use (register discovered live) |
| `tool/audit.py` | orchestrator: `check` (read-only evidence) and `repair` (dry-run/apply) over an audit scope; reuses the maintainer's `frontmatter.py`/`links.py`/`register.py` primitives as shared infrastructure without merging responsibilities |
| `tests/` | 22 stdlib-unittest tests, all passing 2026-09-25 (incl. byte-preservation and refusal classes) |

## Storage

| Item | Path | Character |
|---|---|---|
| Audit record | `C:\mybizz\mybizz-config-docs\mb-doc-auditor\doc-auditor-records.md` | append-only; one block per audit run (date, scope, purpose, checked, findings by classification, actions, outstanding, terminal); created + registered 2026-09-25 |

## Trigger model

| Item | Value |
|---|---|
| v1 triggers | explicit request, or a defined audit condition stated at invocation (restructuring, migration, G-brain ingestion/indexing change, requirement change, repeated maintenance evidence, degradation evidence) |
| Never | document saves; the auditor does not observe saves and has no watcher or queue |
| Scheduler | none in v1 — "defined schedule" recorded as future/not established (developer decision) |

## GBrain integration

| Item | Value |
|---|---|
| Source ID | `mb-doc-auditor` — registered 2026-09-27, non-federated (developer instruction, mirrors mb-doc-maintainer; open item #2 closed); first import 1 page / 7 chunks, 100% embedded, checkpoint `aa91ff7f` |
| Live reads | `gbrain sources list` / `gbrain orphans` via `gbrain_reader.py`, read-only, timeout 60 s |

## Register usage

| Register | Relevance |
|---|---|
| `C:\mybizz\mybizz-config-docs\register-local.md` | holds the audit-record row (`doc-auditor-records`, creation 2026-09-25); the auditor's suite docs register here (rows appended 2026-09-25) |
| Six-register inventory | `register-paths.md` (planning folder): `data-mybizz-mgt`, `makepdlf-project-library`, `mb-3-cs-project-library`, `mybizz-config-docs`, `mybizz-os-docs`, `project-library-global` — the current known universe |
| Discovery rule | walk up from the document's path (same as the maintainer); `pdlf-register.md` is outside the inventory — encountered under a C:\pdlf scope, it is a finding for human judgement |

## Recorded decisions (developer, 2026-09-25)

| Decision | Value |
|---|---|
| Obsolete registration | retire in place (`state: Retired`, `superseded-by` where known); rows never deleted; wrong-register row = retire there + append correct register |
| Registration refusals | basename-collision stems and multiply-occurring stems are never auto-registered — underdetermined identity is a human-judgement finding |
| Doc-id candidates (detection) | bare stem + trailing-pair join + full relative join, case-insensitive — detection only; the nested-corpus convention itself is a developer decision |
| Triggers | v1 explicit/condition only; no scheduler |
| Anvil class rule | any folder containing `anvil.yaml` is never documentation; `anvil.yaml` never read, written, or touched |
| gbrain CLI boundary | read-only calls only; the auditor never writes to G-brain |

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Nested-corpus registration convention (path-derived compound doc-ids vs bare stems) — detection heuristic works; the convention itself awaits a developer decision surfaced by the first live audit. | Open |
| 2 | GBrain source registration for `mb-doc-auditor` (+ repo-organization row) — registered 2026-09-27 (non-federated, mirrors mb-doc-maintainer); repo-organization.md row added; first import 1 page / 7 chunks / 100% embedded, checkpoint `aa91ff7f`. | Closed 2026-09-27 |
| 3 | First-live-audit outstanding items carried in `doc-auditor-records.md` (2026-09-25): 1 stem-collision registration decision (README ×5), 12 broken WikiLinks needing target decisions, 9 pre-existing legacy-schema register rows (Can wait). | Open — human decisions |
| 4 | Live-session confirmation of skill discovery (convention-verified 2026-09-25; listing confirms at next session start). | Open |
