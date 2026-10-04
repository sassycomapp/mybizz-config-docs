---
title: "cupcake-learnings"
doc-id: "mb-a3fa7539"
updated: "2026-10-04"
---
# Cupcake — Learnings

Transient way-station for exam-run knowledge: patterns, decisions, nuances. No
narrative, no history. Every entry is eventually dropped or written into a
**permanent home** (skill / config / reference / explainer) — then deleted from
here immediately on graduation. The plan is never an absorption destination — it
is transient; pruning into a plan destroys the knowledge when the next cycle
overwrites it. Entries never accumulate. Cross-cutting learnings (guard classes,
graduation rules) live in the orchestrator's own
[[[mybizz-config-docs:mb-config-manager/config-manager-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-learnings.md), not here.

| # | learning | right action | destination |
|---|---|---|---|
| 1 | The control-plane rule denies bash command TEXT that merely NAMES the grant tools — even read-only resolution such as `command -v` (proven live 2026-10-04, run #2). The exec-protection matcher additionally fires on read-shaped `sed` whose operand is a control-plane path, and on listings of the tools' bin dir | Verify grant tooling via filesystem listing + Read-tool inventory, never by naming the tools in bash; hand anything execution-shaped to the developer; every denial recorded as liveness evidence | skill (C2-5 runner note) — via next skill amendment |
| 2 | Grant decrements race under parallel tool calls: the read-modify-write span is unserialized, so concurrent writers lose decrements (proven live 2026-10-04: three writes succeeded against a count-2 grant — two parallel writes lost one decrement, the third was allowed at count 1; post-fix verification the same day confirmed the fix: two parallel writes both decremented, count 0 exactly, third write denied) | Standing verification probe: issue a count-2 grant on a restricted scratch path → two Write calls in ONE parallel batch → read the grants file (pre-fix: count 1; post-fix: count 0 exactly) → third write (pre-fix: allowed; post-fix: denied). Run it after any lock or decrement change | skill (C3-3 post-fix re-probe step) — via next skill amendment |
| 3 | The compiled cross-project rule's exempt list is `/tmp/`-only; until 2026-10-04 its source doc still documented an 8-entry always-open list. Developer decision (run #2 F-11): the compiled state stands, the rule is unchanged, the source doc is corrected to present state (applied 2026-10-04 — source and compiled rule now match). Live consequence from 2026-10-04: writes to the formerly listed shared-library folders require grants like any outside-project write | Treat the compiled rule as the enforcement truth; expect grant slips for cross-project doc work; the corrected source doc is the new correspondence baseline | resolved — config correspondence row updated 2026-10-04 |
| 4 | A "protected from every session" rule whose scope resolves against the session cwd leaves an ancestor-cwd hole: a session started in an ancestor of the protected tree sees writes into it as in-project (observed: a terminal-OpenCode session started in `/home/dev-p` wrote into `~/.config/opencode/skills/` without a grant). Before attributing an unexpected allow to a rule failure, first prove the harness loads Cupcake at all with a cwd-independent probe (the outbound-network deny on a non-allowlisted fetch) | Next exam: run the two-step carried-forward check recorded in the run #2 exam report (terminal liveness probe from `/home/dev-p`, then the ungranted skills-dir write probe); only an allow under confirmed enforcement indicts the F-7 rule | skill (next-exam carried-forward check) — via next skill amendment |
