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
| 2 | Grant decrements race under parallel tool calls: the read-modify-write span is unserialized, so concurrent writers lose decrements (proven live 2026-10-04: three writes succeeded against a count-2 grant — two parallel writes lost one decrement, the third was allowed at count 1) | Standing verification probe: issue a count-2 grant on a restricted scratch path → two Write calls in ONE parallel batch → read the grants file (pre-fix: count 1; post-fix: count 0 exactly) → third write (pre-fix: allowed; post-fix: denied). Run it after any lock or decrement change | skill (C3-3 post-fix re-probe step) — via next skill amendment |
| 3 | The deployed cross-project rule's exempt list is `/tmp/`-only while its source doc documents an 8-entry always-open list (incl. `mybizz-config-docs`, `logs`, both config homes) — live consequence: writes to those documented folders currently require grants. The control-plane rule, added 2026-09-24, has no source document at all | Flag the divergence at every C2-4 until the developer reconciles (re-add entries vs update the source doc); treat the compiled rule as the enforcement truth | config open item / F-11 gate decision — via governance |
