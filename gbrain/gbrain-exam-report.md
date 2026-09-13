---
document: "GBrain — Exam Report"
doc-id: gbrain-exam-report
state: Live
date-created: 2026-09-12
---

# GBrain — Exam Report

First verification run of the `mb-config-gbrain` module (2026-09-12).
Detection only — Tiers 0–2. Tier 3 not unlocked. Spec: `gbrain-config.md`
(verified live 2026-09-06).

## Verdict: SYSTEM HEALTHY — spec doc stale in five places (docs governance)

## Tier 0 — Liveness: PASS

| Check | Expected | Actual | Result |
|---|---|---|---|
| Binary + VERSION | `/home/dev-p/.bun/bin/gbrain`, 0.46.1.0 | both agree | PASS |
| Engine responds | identity returns | 0.46.1.0, postgres engine, counters returned | PASS |
| DB ping | reachable | reachable (postgres module Tier 0 green) | PASS |

## Tier 1 — Health: PASS

| Check | Result |
|---|---|
| Sources | 14 live, all paths on disk, all with real page counts |
| Sync machinery | `sync-failures.jsonl` = 0 bytes — zero sync failures |
| Embedding coverage | 100% per current postgres-module exam report (cross-referenced, not re-probed) |
| Scheduled jobs | none in crontab — design state holds |
| Identity counters | 1,824 pages / 5,529 chunks — cross-match postgres exam exactly |

## Tier 2 — State conformance: PASS with drift flags

| Check | Expected (spec) | Actual | Result |
|---|---|---|---|
| Version | 0.46.1.0 live; upgrade only on check failure | 0.46.1.0; upstream now 0.50.0.0 (spec recorded 0.48.2.0) | PASS (policy holds) |
| Schema pack | gbrain-everything@1.0.0+7021205a, 30/12 | exact match | PASS |
| MCP entry | local, `[..., "serve"]`, enabled | exact match | PASS |
| Registered sources | 13 | **14** — see finding 1 | DRIFT |
| Legacy `brain.pglite` | present (stale) | **absent** — see finding 3 | DRIFT |
| Skills bundle | 60 skills + skillify | 65 entries, no skillify, 4 underscore metadata files — see finding 4 | DRIFT |
| config.json content | self_upgrade notify; no keys inside | not checked — guard-blocked, developer-run | DEFERRED |
| Source clone version (follow-up) | v0.25.0, far behind | **v0.25.0 confirmed** — spec record accurate | PASS |
| MCP env names (follow-up) | OPENAI_API_KEY, ZEROENTROPY_API_KEY by name | exact match (names only; values untouched) | PASS |

## Findings

1. **DRIFT — new source.** `pdlf` ("PDLF System", `/mnt/c/pdlf`, federated, 59 pages,
   synced 2026-09-11) registered after the spec's 2026-09-06 verification. Consistent
   with the pdlf project going live 2026-09-11 (see projects-config-register).
   → docs governance: add source row, refresh verification date.
2. **DRIFT — page-count table stale.** default 694 vs 281; mybizz-config-docs 116 vs
   425 (a large drop — needs explanation on the doc-refresh pass); memory-governor 47
   vs 53; mybizz-os-docs 7 vs 8; mb-3-cs-project-library 437 vs 435. Also: source sum
   = 1,551 vs identity total 1,824 (273 unaccounted — spec's sums reconciled exactly;
   the accounting question needs one focused follow-up next run). → docs governance
   refresh of the statistics + sources tables.
3. **DRIFT — legacy artifact gone.** `~/.gbrain/brain.pglite` no longer exists.
   Functionally fine (it was documented stale/unused; Postgres is the engine).
   Spec lists it as present → docs governance.
4. **DRIFT — skills bundle evolved.** 65 entries: no `skillify`, 4 underscore
   metadata files (`_AGENT_README.md`, `_brain-filing-rules.json/.md`,
   `_output-rules.md`) vs spec's "60 + skillify = 61". Project-local and gitignored —
   bundle regenerates with CLI; spec refresh → docs governance.
5. **Agent execution boundary (new, structural).** The sensitive-data guard blocks
   agent reads of `~/.gbrain/config.json` outright — config-content conformance
   (self_upgrade_mode, models, keys-absent) is **developer-run**. Skill amended
   same-run. Not a fault: the guard is doing exactly what the credential rule wants.

## Guard layers

Sensitive-data guard blocked the config.json read probe mid-exam — honored, no
workaround; checks rerouted to developer-run. Guard verified armed.

## Not run this cycle

Tier 3 (sync sample, restart behavior, upgrade decision); config.json content
checks; MCP restart behavior; the 273-page accounting question (finding 2 follow-up).