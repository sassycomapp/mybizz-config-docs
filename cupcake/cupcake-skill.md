---
name: mb-config-cupcake
description: Cupcake configuration exam — verifies the live policy-enforcement layer (binary, plugin, policy inventory, rule liveness) against cupcake-config.md, catches silent failures (rule present but not firing), proposes gated repairs. Use when asked to "exam cupcake", "check cupcake health", or as part of a full mb-config-manager run.
---

# mb-config-cupcake — Exam Skill

Exams the live Cupcake policy-enforcement system against its spec. This skill holds
the **procedure** only — expected values live in the spec doc and are read fresh at
the start of every run.

- Spec: `cupcake/cupcake-config.md` — read it first, every run
- Reference (health check, recovery, pitfalls): `cupcake/cupcake-reference.md`
- Report: `cupcake/cupcake-exam-report.md` — one file, overwritten each run
- Learnings: `cupcake/cupcake-learnings.md`

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

## Tier 0 — Liveness (run first; failure = report `DOWN`, stop)

- Binary resolves: `cupcake` and `opa` on PATH; `~/.config/opencode/plugin/cupcake.js`
  exists
- **Enforcement firing**: one harmless known-blocked probe (e.g. `curl` to a
  non-allowlisted domain — harmless whether allowed or denied). Deny received =
  liveness confirmed. Allow received = **fail-open/crash finding** — report as
  `UNHEALTHY`, hand to developer; never retry with an indirect path.
- Denies already received naturally during this exam run count as firing evidence —
  record them.

## Tier 1 — Health (compile + structural integrity)

- `opa check` every `.rego` in `~/.config/cupcake/policies/opencode/` (safe — invokes
  opa, never cupcake) — zero failures. One failed file = the 7F crash pattern; finding
  class `UNHEALTHY`, repair proposal: remove/fix the bad file (developer-run — the
  policy folder is Cupcake-protected)
- No scaffold files: no `example.rego`, no non-`cup-`/non-builtin `.rego` in the
  global policy folder; no `.cupcake/policies/opencode` scaffold files in project
  folders (inventory from outside; do not enter `.cupcake/` to modify)
- Plugin single-copy discipline: exactly one `cupcake.js` in
  `~/.config/opencode/plugin/` (a symlinked second copy double-fires — loader does
  not deduplicate). The `.bak-*` backup must keep a non-`.js` suffix
- `cup-grants-data.rego` present, generated-form (never hand-edited content shape)

## Tier 2 — State conformance (spec comparison)

- Policy inventory vs spec: 19 custom + 3 builtins + `system/evaluate.rego` — file
  names matched one-by-one against the spec's rule tables
- Three-layer task denial: `"task": "deny"` present in `~/.config/opencode/opencode.json`
  (read-only); `spawn-tools-denylist.json` lists exactly: task, delegate,
  call_omo_agent, agent_session_create
- Source↔deployed sync: `cup-*.md` sources in
  `C:\dev\project-library-global\rules-cupcake-global\` vs deployed `cup-*.rego` —
  count and name correspondence; a deployed rule with no source, or vice versa, is a
  `GAP`
- Grant tooling: `mg-grant`, `mg-revoke` present on PATH
- Plugin backup exists (`.bak-20260912`)

## Tier 3 — Deep pass (developer-run; detection-only unless unlocked)

- Authoritative live eval: the reference doc's health-check invocation, run by the
  developer — anything other than a clean allow is a live incident
- Real block/allow test sheet for representative rules (the 13/13 / 35/35 pattern)
- Grant lifecycle live test: grant → write attempt → decrement → expiry
- Version corroboration (spec open item 3)

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