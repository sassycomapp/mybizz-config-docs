---
name: mb-config-cupcake
description: Cupcake configuration exam — verifies the live policy-enforcement layer (binary, plugin, policy inventory, rule liveness) against cupcake-config.md, catches silent failures (rule present but not firing), proposes gated repairs. Use when asked to "exam cupcake", "check cupcake health", or as part of a full mb-config-manager run.
---

# mb-config-cupcake — Exam Skill

Exams the live Cupcake policy-enforcement system against its spec. This skill holds
the **procedure** only — expected values live in the spec doc and are read fresh at
the start of every run.

- Spec: `cupcake/cupcake-config.md` — read it first, every run
- **Exam plan: `cupcake/cupcake-exam-plan.md` — read second, every run.** The
  plan-driven cycle: the config-manager synthesizes this plan fresh before each run
  (from spec + last report + log + learnings) and this skill executes it in hand.
  The plan carries run-specifics and deltas; the **standing check inventory lives
  in this skill** (below) — permanent occurrences graduate here, never into plans
- Reference (health check, recovery, pitfalls): `cupcake/cupcake-reference.md`
- Report: `cupcake/cupcake-exam-report.md` — one file, overwritten each run
- Log: `cupcake/cupcake-log.md` — append one run row (date, verdict, findings,
  disposition) after every run; free rows for notable events witnessed between runs
- Learnings: `cupcake/cupcake-learnings.md` — file new patterns/nuances; delete
  entries once graduated into a permanent home

## The silent-failure class this exam exists for

Cupcake's documented failure modes are silent: rules that pass offline but produce
nothing live; scaffold files that compile-but-break the whole folder; duplicated
plugin copies that double-fire; checkers spawned without a working directory. The
exam's core discipline: **prove enforcement is firing, never infer it from presence.**

## Structural rule — what the agent may never do

`cupcake_exec_protection` blocks the agent from executing the cupcake binary — so the
authoritative live eval check (`cupcake eval`, per the reference doc) is
**developer-run**. The guard matches the token `cupcake` in command text broadly:
even non-execution commands whose path arguments contain it (`mkdir`, `mv`, `which`)
are denied — proven live 2026-09-12. Therefore **all file operations touching
cupcake-named paths (installing this skill, moving policy or plugin files) are
developer-run**: hand the developer the exact commands, never construct a token-
dodging alternative. The agent never runs the cupcake binary, never reads or edits
anything inside `.cupcake/` or `~/.config/cupcake/` beyond read-only inventory, and
never touches policy or plugin files. Enforcement evidence available to the agent:
a deny received during the exam run itself is proof the chain fires.

## Tier 0 — Liveness (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| C0-1 | A | Binaries resolve by filesystem listing: `~/.cupcake/bin/` real binary + `/usr/local/bin/` symlink; `opa` real file — **never name the cupcake binary in a command** | Matches spec identity rows |
| C0-2 | A | Enforcement firing: one harmless known-blocked probe (e.g. `curl` to a non-allowlisted domain — harmless whether denied or allowed) OR denies naturally received during the run | Deny received = liveness confirmed; allow received = fail-open/crash finding → `UNHEALTHY`, hand to developer |
| C0-3 | A | Plugin: exactly one live `cupcake.js` in `~/.config/opencode/plugin/` | One live copy (loader does not deduplicate — a second copy double-fires) |

## Tier 1 — Health (compile + structural integrity)

| ID | Runner | Check | Expected |
|---|---|---|---|
| C1-1 | A | `opa check` every `.rego` in `~/.config/cupcake/policies/opencode/` (deployed + builtins + system) — safe, invokes opa only | Zero failures — one failed file = the 7F crash pattern → `UNHEALTHY` |
| C1-2 | A | Scaffold absence: no `example.rego`, no non-`cup-`/non-builtin `.rego` in the policy folder; project `.cupcake/` skeletons intact | None (inventory from outside; never modify) |
| C1-3 | A | Backup discipline: all `.bak-*` files carry non-`.rego`/non-`.js` suffixes | All correctly suffixed (never loaded) |
| C1-4 | A | `cup-grants-data.rego` present, generated-form header | `GLOBAL-GRANTS-DATA` header; never hand-edited |

## Tier 2 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| C2-1 | A | Policy inventory | 19 custom + 3 builtins + `system/evaluate.rego` aggregator — file names matched against the spec's rule tables |
| C2-2 | A | Task-denial layer 1 | `"task": "deny"` in `~/.config/opencode/opencode.jsonc` (note: `.jsonc`, not `.json`) |
| C2-3 | A | `spawn-tools-denylist.json` | exactly: task, delegate, call_omo_agent, agent_session_create |
| C2-4 | A | Source↔deployed correspondence | 20 sources ↔ 19 deployed; `no_bash_mediated_file_writes_without_grant.md` folded into the cross-project rule (expected — bash-shape indicators verified present); a "missing" bash-governance deployment is NOT a finding |
| C2-5 | A | Grant tooling | `mg-grant`, `mg-revoke` present on PATH |
| C2-6 | A | Plugin backup set | inventoried vs spec (8 `.bak-*` files across plugin/policy/builtins) |
| C2-7 | A | Grants data file | present, generated-form |
  `GAP`
- Grant tooling: `mg-grant`, `mg-revoke` present on PATH
- Plugin backup exists (`.bak-20260912`)

## Tier 3 — Deep pass (all developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| C3-1 | D | Authoritative live eval: the reference doc's health-check invocation, run by the developer | Clean `{"decision":"allow"}` — anything else is a live incident |
| C3-2 | D | Real block/allow test sheet for representative rules (the 13/13 / 35/35 pattern) | All pass |
| C3-3 | D | Grant lifecycle live test — **agent-executed, with a non-always-open path** (never `/tmp` — it's on the always-open list; the plugin's hooks never fire in the developer's bare terminal, so only agent tool calls exercise the mechanism): mg-grant → Write-tool writes → verify decrement in `cup-grants-data.rego` → exhaustion denial | File-tool decrement 2→1→0 then denial; **bash-mediated writes do not decrement** — accepted as intended design (config.md, 2026-09-13) |
| C3-4 | D | Version corroboration | spec open item 3 — upstream release listing vs installed 0.3.0 |

## Heal allowlist (gate-gated)

By design this module has **no agent-healable items** — Cupcake is the governance
layer itself; the agent never edits its policies, plugin, or grants file:

- All repairs here are developer-run, or proposed through the report
- Doc corrections → flagged to docs governance, never applied here

## Deny-list (never heal, never touch)

Anything inside `~/.config/cupcake/` or any `.cupcake/` · `cupcake.js` (both live
copy and backup) · the cupcake/opa binaries · `opencode.json` permission section ·
`spawn-tools-denylist.json` · rule sources in `rules-cupcake-global/`. A denied
command is never worked around — the denial is the system working.

## Report

Write `cupcake-exam-report.md`: tier results, findings with class + evidence +
recommended repair, inventory deltas, liveness evidence (which deny proved firing).
Overwritten every run.