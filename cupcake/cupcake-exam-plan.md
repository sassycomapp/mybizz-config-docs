---
title: "cupcake-exam-plan"
doc-id: "cupcake-exam-plan"
---
# Cupcake — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[cupcake-config|Cupcake Configuration]] (spec), the last [[cupcake-exam-report|Exam Report]],
[[cupcake-log|Log]] (events since last run), [[cupcake-learnings|Learnings]]. Consumed by
the skill at run time; rewritten at the start of the following cycle. The file is
live; its contents are transient.

**This first plan is hand-written** (emulation of the PostgreSQL architecture): it
also served as the format template — the standing-checks section below was the
complete, authoritative enumeration of every check the exam performs. It
**graduated into the skill on 2026-09-13** (after run #1 verified it); this plan
is retained as the format template, and future plans carry run-specifics +
references instead.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (pilot 2026-09-12 was detection-only, pre-architecture) |
| Run date | set at execution |
| Prior report | [[cupcake-exam-report|Exam Report]] (2026-09-12, pilot) |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run (Tier 3 items are inherently developer-run: the exec-protection guard forbids agents from executing the cupcake binary) |
| Developer-run requests this run (bundled into ONE request) | (a) authoritative live eval health check (reference-doc invocation); (b) any check whose command text the guards deny |
| Expected-value source of truth | [[cupcake-config|Cupcake Configuration]] — read fresh at run start; never rely on remembered values |
| Structural constraint | the agent never executes the cupcake binary, never reads/edits anything inside `.cupcake/` or `~/.config/cupcake/` beyond read-only inventory, never touches policy or plugin files |

## 2. Carried-forward items (from pilot report, 2026-09-12)

| # | Item | Why deferred | This run's action |
|---|---|---|---|
| CF-1 | Finding 2 — backup inventory vs spec (2 plugin backups + 5 rego `.bak-*` files exist; spec documents one) | docs-governance flag | Verify whether governance approved + applied the spec refresh; re-inventory and compare |
| CF-2 | Finding 3 — config filename drift (spec says `opencode.json`, live file is `opencode.jsonc`) | docs-governance flag | Verify whether governance applied; re-check task-deny against the actual file |
| CF-3 | Finding 0 — guard false-positive class (token `cupcake` in command text is denied even for non-execution) | reclassified operations developer-run | Confirm the class still holds; any new denial = further evidence, never worked around |
| CF-4 | Tier 3 deep pass (developer eval + test sheets + grant lifecycle + version corroboration) | unlock not given; inherently developer-run | List as available; execute only on unlock |

## 3. Erred last run (distinct from deferred)

| # | What erred | This run's action |
|---|---|---|
| ER-1 | `which cupcake` denied by exec-protection (binary-name resolution) | Binary resolution via filesystem listing only (`ls` on bin dirs); never name the binary in a command |
| ER-2 | Skill-install `mkdir`/`mv` denied (token in path args) | Install operations touching cupcake-named paths are developer-run — standing rule, confirmed 2026-09-12 |

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-13 copy-install backfill + register hash recorded | Step-0 hash check covers the cupcake skill pair |
| LG-2 | No crashes/incidents since 2026-09-12 fixes | If a new log row exists at synthesis time, derive a targeted probe from it |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | Source↔deployed correspondence: 20 sources, 19 deployed files — bash-write-shapes are folded into `cup-no_cross_project_filesystem_access_by_default.rego` (verified: 4 bash-shape indicator groups) | Count correspondence with the fold-in expected; a "missing" bash-governance deployment is NOT a finding |

## 6. Standing checks — the complete enumeration (Tiers 0-3)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass rule.
This enumeration graduates into the skill after a verified run; future plans carry
run-specific deltas only.

### Tier 0 — Liveness (run first; any failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| C0-1 | A | Binaries resolve by filesystem listing: `~/.cupcake/bin/` real binary + `/usr/local/bin/` symlink; `opa` real file — **never name the cupcake binary in a command** | Matches spec identity rows |
| C0-2 | A | Enforcement firing: one harmless known-blocked probe (e.g. `curl` to a non-allowlisted domain — harmless whether denied or allowed) OR denies naturally received during the run | Deny received = liveness confirmed; allow received = fail-open/crash finding → `UNHEALTHY`, hand to developer |
| C0-3 | A | Plugin: exactly one live `cupcake.js` in `~/.config/opencode/plugin/` | One live copy (loader does not deduplicate — a second copy double-fires) |

### Tier 1 — Health (compile + structural integrity)

| ID | Runner | Check | Expected |
|---|---|---|---|
| C1-1 | A | `opa check` every `.rego` in `~/.config/cupcake/policies/opencode/` (deployed + builtins + system) | Zero failures — one failed file = the 7F crash pattern → `UNHEALTHY` |
| C1-2 | A | Scaffold absence: no `example.rego`, no non-`cup-`/non-builtin `.rego` in the policy folder; project `.cupcake/` skeletons intact | None (inventory from outside; never modify) |
| C1-3 | A | Backup discipline: all `.bak-*` files carry non-`.rego`/non-`.js` suffixes | All correctly suffixed (never loaded) |
| C1-4 | A | `cup-grants-data.rego` present, generated-form header | `GLOBAL-GRANTS-DATA` header; never hand-edited |

### Tier 2 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| C2-1 | A | Policy inventory | 19 custom + 3 builtins + `system/evaluate.rego` aggregator — file names matched against the spec's rule tables |
| C2-2 | A | Task-denial layer 1 | `"task": "deny"` in `~/.config/opencode/opencode.jsonc` (note: `.jsonc`, not `.json`) |
| C2-3 | A | `spawn-tools-denylist.json` | exactly: task, delegate, call_omo_agent, agent_session_create |
| C2-4 | A | Source↔deployed correspondence | 20 sources ↔ 19 deployed; [[no_bash_mediated_file_writes_without_grant|Rule: No Bash-Mediated File Writes Without Grant]] folded into the cross-project rule (expected — see LE-1); verify bash-shape indicators still present in that rego |
| C2-5 | A | Grant tooling | `mg-grant`, `mg-revoke` present on PATH |
| C2-6 | A | Plugin backup set | inventoried vs spec (CF-1) |
| C2-7 | A | Grants data file | present, generated-form |

### Tier 3 — Deep pass (all developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| C3-1 | D | Authoritative live eval: the reference doc's health-check invocation, run by the developer | Clean `{"decision":"allow"}` — anything else is a live incident |
| C3-2 | D | Real block/allow test sheet for representative rules (the 13/13 / 35/35 pattern) | All pass |
| C3-3 | D | Grant lifecycle live test | grant → write attempt → decrement → expiry |
| C3-4 | D | Version corroboration | spec open item 3 — upstream release listing vs installed 0.3.0 |

## 7. Report requirements

The run writes [[cupcake-exam-report|Exam Report]]: verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair;
runner attribution for every deferred item (guard-forbidden vs unlock-gated);
liveness evidence (which denial proved firing); overwritten in full each run
(write-then-replace: failed runs never touch the prior report). Then: one run row
appended to [[cupcake-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **This module has no agent-healable items by design** — Cupcake is the
  governance layer itself; the agent never edits its policies, plugin, or grants
  file. All repairs are developer-run, or proposed through the report
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never touch): anything inside `~/.config/cupcake/` or any `.cupcake/`
  · `cupcake.js` (live copy and backups) · the binaries · `opencode.jsonc`
  permission section · `spawn-tools-denylist.json` · rule sources in
  `rules-cupcake-global/`
- Credentials: variable names only, never printed
