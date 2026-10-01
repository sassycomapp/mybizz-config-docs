---
title: "gbrain-exam-report"
doc-id: "mb-0192f9b2"
updated: "2026-10-01"
---
# GBrain — Exam Report

Run #1 — **first formal plan-driven run** (2026-09-13). Plan:
[[[mybizz-config-docs:gbrain/gbrain-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-plan.md) (step-0 self-validation: PASS — 8 suite files, hash pair
MATCH 4a2e10d8a69752f7, spec present, no open run). Detection only — Tiers 0–2
agent-runnable checks executed; Tier 3 locked. Scope boundary honored: DB-level
facts cross-referenced from the postgres module's run-#2 report, not re-probed.

## Verdict: SYSTEM HEALTHY — all agent-runnable checks green; 273-page accounting question RESOLVED; 4 spec-drift flags re-confirmed pending governance

## Tier 0 — Liveness: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| G0-1 | Binary + VERSION | present, 0.46.1.0 | exact | PASS |
| G0-2 | Engine responds (identity call) | version + counters, no error | 0.46.1.0, postgres engine, 1,880 pages / 5,581 chunks | PASS |
| G0-3 | DB ping | 1 | 1 | PASS |

## Tier 1 — Health: PASS

| ID | Check | Result |
|---|---|---|
| G1-1 | 14 registered sources, **14/14 paths exist on disk**, page counts sane (growth-at-sync explained) | PASS |
| G1-2 | Sync machinery: `sync-failures.jsonl` 0 bytes; **zero** crontab gbrain entries | PASS |
| G1-3 | Embedding coverage: postgres module run-#2 report = 100%; this run's quick count 5,581/5,581 after two syncs | PASS (100% held through syncs) |
| G1-4 | `brain.pglite` absent — expected (CF-3 documented state) | PASS w/ flag |
| G1-5 | `~/.gbrain/` structure intact; `config.json` present with restrictive permissions (`-rw-------`) | PASS |

## Tier 2 — State conformance: PASS with carried spec-drift flags

| ID | Expected | Actual | Result |
|---|---|---|---|
| G2-1 | 0.46.1.0 live; upgrade only on check failure | 0.46.1.0; upstream latest 0.50.0.0 (banner) | PASS (policy holds) |
| G2-2 | `gbrain-everything@1.0.0+7021205a`, 30/12 | exact match (MCP) | PASS |
| G2-3 | MCP entry exact | **guard-denied this run** → developer bundle | DEFERRED |
| G2-4 | embedding 3-large 1536d | [[[makepdlf-project-library:docs-local/config\|Config]]](C:/dev/dev-makepdlf/makepdlf-project-library/docs-local/config.md) table: model + dims + chunk_strategy=semantic | PASS |
| G2-5 | bundle per spec | 65 entries + 4 underscore metadata files (matches evolved state; spec stale — CF-4) | DRIFT (carried) |
| G2-6 | Page accounting reconciles | **RESOLVED: per-source DB attribution sums to exactly 1,880 = identity; zero unattributed pages** — see finding 2 | PASS |
| G2-7 | All source paths exist | 14/14 | PASS |
| G2-8 (config.json content) | self_upgrade notify; no keys inside | developer-run (guard) | DEFERRED |

## Findings

1. **Spec-drift flags re-confirmed (CF-1..4, pending governance).** The
   [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) refresh has **not** been approved/applied: spec lists 13
   sources (live: 14 incl. `pdlf`); counts/dates stale; `brain.pglite` still
   listed present (absent since before the pilot); bundle row stale (65 entries,
   no `skillify`, 4 underscore metadata files). All re-flagged for one batched
   governance approval.
2. **273-page accounting question RESOLVED (CF-2).** Per-source DB attribution
   (`GROUP BY source_id`) sums to **exactly 1,880 = identity total**, zero
   unattributed pages. The pilot's gap was **snapshot lag**: the MCP sources
   list reports per-source counts as-of each source's last sync, which lag the
   live DB mid-cycle. The durable check is the per-source DB query, not
   cross-snapshot sums. → learning graduated into the plan/skill method.
3. **Guard reclassification (G2-3).** `opencode.jsonc` jq reads were denied this
   run (previously passed) — the MCP-entry check moves to the developer bundle;
   the nondeterminism documented in [[[mybizz-config-docs:mb-config-manager/config-manager-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-learnings.md) revalidated.
4. **Learning confirmed (LE-1):** count drift at sync is by design — coverage %
   held at 100% through two syncs today; config.md's point-in-time note is the
   correct doctrine.

## Guard layers

Sensitive-data guard denied config.json and opencode.jsonc reads — honored,
rerouted developer-run. Guard armed and behaving per the execution-boundary
learnings.

## Developer-run request (bundled — Tier 3 + guard-denied items)

1. **G3-1 `config.json` content** (masked output, never print the DB URL):
   `jq '{self_upgrade_mode, models, mcp_surface: has("mcp_surface"), keys: (keys | length)}' ~/.gbrain/config.json` — report values except anything secret-shaped
2. **G2-3 MCP entry** — `jq '.mcp.gbrain | {type, command, enabled}' ~/.config/opencode/opencode.jsonc`
3. **G3-2 sync sample** (unlock-dependent, writes): `gbrain sync --source mybizz-os-docs`
4. **G3-3 restart behavior** (unlock-dependent, disruptive): full `wsl --shutdown` test
5. **G3-4 upgrade decision** (policy question — your call, never agent-initiated)

## Not run this cycle

Tier 3 items above (locked); the gbrain upgrade decision; the source-clone
refresh/retire question (spec open item 3 — never resolve unilaterally).
