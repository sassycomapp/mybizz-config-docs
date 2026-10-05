---
title: "graphify-exam-report"
doc-id: "mb-b5af758f"
updated: "2026-10-05"
---
# Graphify — Exam Report

**Final verdict: HEALTHY** — all tiers 0–3 formally executed including the full Tier 3 realistic run (complete documented rebuild), every check PASS, one genuine tool defect found and fixed in-run (F-4, cwd provenance stamping), zero open findings.

Run #1 — first formal plan-driven run (bootstrap). Plan: [[[mybizz-config-docs:graphify/graphify-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/graphify/graphify-exam-plan.md) (hand-written bootstrap). Step-0: PASS (6/6 hash pairs via the approved glob form, suite completeness 6/6 at 8/8 files, register spec-doc paths 19/19 — recorded in [[[mybizz-config-docs:mb-config-manager/config-manager-log|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md)).

**Execution standard applied (developer directive):** an honoured guard denial never substitutes for a formal execution — every denied check was re-executed as a clean single-purpose command in this run (write grants requested via mg-grant where required). Tier 3 ran **in full** (developer direction: "tier 3 has got to be run in full — the big run, the realistic run").

## Tier 0 — Invocability (4/4 PASS, all formally executed)

| ID | Expected | Actual | Result |
|---|---|---|---|
| GF0-1 | `0.9.40` | `graphify 0.9.40` | PASS |
| GF0-2 | `graphifyy` 0.9.40, CLI and package agree | Name `graphifyy`, Version `0.9.40` | PASS |
| GF0-3 | Executable `/home/dev-p/.local/bin/graphify`; module dir `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` | Both exact (`MODULE_DIR_OK`) | PASS |
| GF0-4 | `SKILL.md` + `references/` present; `.graphify_version` = `0.9.40` | All present; marker `0.9.40` agrees with CLI | PASS |

## Tier 1 — State conformance (9 checks, all PASS after in-run heal and re-baseline)

| ID | Expected | Actual | Result |
|---|---|---|---|
| GF1-1 | Installed behind latest; spec records upstream `0.9.56` @2026-09-08 | Upstream latest `0.9.61` (live PyPI); installed `0.9.40` — lag state holds; spec row was stale → corrected (D-2) | PASS |
| GF1-2 | `.graphifyignore` exactly 2 lines; `.graphify_build.json` `{"gitignore": false}`; `.graphify_root` exact | All exact | PASS |
| GF1-3 | `.gitignore` carries `graphify-out/`, `.opencode/`, `agents.md`, `opencode.json`, `tests/` | 5/5 present | PASS |
| GF1-4 | `built_at_commit` == live HEAD; counts point-in-time; `directed` false | Pre-heal: `5ce243e1…` vs HEAD `59175d9e…` → **DRIFT (F-1)**. Healed by GF3-1; final state after the full rebuild: `built_at_commit` == HEAD; 537 nodes / 434 edges / 155 communities; 417 EXTRACTED + 17 INFERRED + 0 AMBIGUOUS; 95 ghosts; `directed: false` | PASS (post-rebuild) |
| GF1-5 | `mcp.graphify` type `local`, enabled `true`, command exact, no API-key field (project-root `opencode.json`) | Keys exactly `command`/`enabled`/`type` (no credential field); type `local`, enabled `true`, command exact | PASS |
| GF1-6 | AGENTS.md block markers present | `BEGIN` line 102, `END` line 126 | PASS |
| GF1-7 | `.opencode/plugins/graphify.js` + `.opencode/node_modules/` exist | Both present | PASS |
| GF1-8 | Eight suite files | 8/8 | PASS |
| GF1-9 | `anthropic` package absent (deterministic labels — accepted state) | Absent | PASS |

## Tier 2 — Functional proof (2/2 PASS)

| ID | Expected | Actual | Result |
|---|---|---|---|
| GF2-1 | `god-nodes --json` runs to completion, returns JSON | 3 god nodes returned (agents.md mb-3-cs degree 13; Anvil UI Build Standard degree 11; VaultDecryptionError degree 10) — artifact loads, query surface executes | PASS |
| GF2-2 | `check-update` runs to completion with a verdict | Exit 0, silent stdout — execution proven; the tool is cron-safe and silent on success (learning filed: verdicts by exit code; currency truth stays with `built_at_commit` vs HEAD) | PASS |

## Tier 3 — Deep pass (2/2 EXECUTED IN FULL — the realistic run)

**GF3-1 — executed at three stages, ending in a complete documented rebuild:**

1. **Realign** (`graphify update`, run under mg-grant): exit 0; one commit behind (`59175d9`, 2026-09-11: removed `theme/assets/anvil-ui-build-standard-v1.md`, 191 deletions); 1/1 uncached file re-extracted, no LLM; pre-update state auto-backed up. Provenance correct after this stage.
2. **Full rebuild, first pass** (`graphify extract . --force --code-only` from the agent's default cwd, then `cluster-only`): exit 0 both; full re-scan of 159 code files (100 non-code correctly skipped by `--code-only`, 4 unclassified skipped); fresh graph 537 nodes / 434 edges / 155 communities. **Verification caught a real defect (F-4): `built_at_commit` was stamped `1194ea9…` — the invoking repo's (mybizz-config-docs) HEAD — not the scanned repo's.** `graphify extract` takes the commit from the invoking working directory's git repo; the update path stamps from the scanned path.
3. **Full rebuild, corrected pass** (re-run from the mb-3-cs repo root, per the reference's cwd discipline): exit 0 both stages; final verified state — **`built_at_commit` == HEAD `59175d9e…`; 537 nodes / 434 edges / 155 communities; 417 EXTRACTED (96%) + 17 INFERRED (4%) + 0 AMBIGUOUS; 95 ghost template nodes; `directed: false`; GRAPH_REPORT.md, graph.html and labels regenerated.** The count difference vs the pre-rebuild state (562/457 → 537/434) is the documented code-only semantics: a fresh build contains no document-derived concept nodes; the fresh baseline matches the 2026-08-15 era (also 537 nodes).

**GF3-2 — upgrade decision procedure executed to its documented conclusion:** inputs installed 0.9.40, upstream 0.9.61, zero check failures across Tiers 0–2; standing policy "never on newness — only on check failure" → outcome: **stay on 0.9.40**; no upgrade trigger exists; W-2 closed for this cycle.

## Findings and dispositions (all closed)

| # | Class | Finding | Disposition |
|---|---|---|---|
| F-1 | DRIFT | Graph provenance behind checkout (`5ce243e1…` vs HEAD `59175d9e…`) | **Healed**: GF3-1 executed (realign, then full rebuild); provenance confirmed == HEAD; counts re-baselined in the spec (D-3). Closed |
| F-2 | Spec drift | Spec §Identity upstream row stale (`0.9.56`; live `0.9.61`); W-1 re-confirmed (`--exclude` still absent) | **Applied (developer-approved, finalize directive)**: spec corrected. Closed |
| F-3 | Method | Two composite re-probes guard-denied mid-run; honoured absolutely | **Resolved per developer standard**: every affected check re-executed formally — all PASS; write grants requested and granted where required. No check rests on prior-session evidence. Closed |
| F-4 | Tool defect (found by the full rebuild) | `graphify extract` stamps `built_at_commit` from the invoking cwd's git repo, not the scanned path — a rebuild from another repo mis-stamps provenance (caught by the procedure's step-4 confirmation) | **Fixed in-run**: rebuild re-run from the target repo root; provenance verified. Recorded as a spec open item + skill/reference learning (rebuilds always run from the target repo root; step-4 confirmation is mandatory). Closed |

## Spec corrections applied (developer-approved, 2026-09-14)

1. §Identity — Upstream latest (PyPI): `0.9.56` → `0.9.61` (verified live 2026-09-14).
2. §Current graph state — re-baselined to the rebuilt state: 537/434, 155 communities, 417+17+0, `built_at_commit` `59175d9e…`, live-HEAD-current verified 2026-09-14.
3. §graphify-out inventory — `2026-09-14/` auto-backup row recorded accurately (surviving snapshot: post-realign, pre-rebuild state).
4. §Open items — cwd quirk recorded; upstream row updated; `--exclude` re-confirmation dated.
5. Header verification note updated (2026-09-14 run #1).

## Graduations applied (2026-09-14, dual track — permanent homes exist, transient entries deleted)

- **Skill** (agent-applied): cwd-provenance hard rule + "Run #1 lessons graduated" section (F-4 confirmation discipline, check-update semantics, count-delta discipline). Re-installed by copy; re-hash `1ca73897a2023741`; register updated.
- **Reference** (developer-approved under the finalize directive): §Graph build procedures — mandatory from-repo-root discipline + step-4 confirmation; §Work memory — check-update silence semantics.
- [[[mybizz-config-docs:graphify/graphify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md) is empty again — nothing transient remains.

## Watch-state at close

- W-1 (`--exclude` absent in 0.9.40) — re-confirmed, unchanged, closed for this cycle.
- W-2 (upgrade decision) — executed via GF3-2: stay on 0.9.40; closed.
- W-3 (paused project) — graph rebuilt regardless; moot for this cycle.
- W-4 (deterministic labels) — GF1-9 PASS; unchanged.

**No open findings. No deferred items. Run closed.**
