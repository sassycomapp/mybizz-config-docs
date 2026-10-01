---
title: "cupcake-learnings"
doc-id: "mb-a3fa7539"
updated: "2026-10-01"
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
| 1 | Source↔deployed correspondence: 20 rule sources, 19 deployed files — the bash-governance source ([[[default:rules-cupcake-global/no_bash_mediated_file_writes_without_grant\|Rule: No Bash-Mediated File Writes Without Grant]]](C:/dev/project-library-global/rules-cupcake-global/no_bash_mediated_file_writes_without_grant.md)) is compiled into `cup-no_cross_project_filesystem_access_by_default.rego` (same file/package, own rule id; 4 bash-shape indicator groups verified) | Expect the fold-in in every correspondence check; a "missing" bash-governance deployment is NOT a finding | config.md (source-inventory note — via governance) |
| 2 | `.bak-*` files accumulate by design (plugin ×2, rego ×5 as of 2026-09-12) — the spec documents only one | Check suffix discipline (non-`.rego`/non-`.js` = never loaded), not backup absence; spec's backup list needs a full-set refresh | config.md (backup inventory — via governance) — **APPLIED 2026-09-13** |
| 3 | Guard denials during an exam run are dual-purpose: enforcement proof AND a reclassification signal. The token-`cupcake` class denies even non-execution commands (proven: `which`, `mkdir`, `mv`); binary-path checks work via filesystem `ls` only | Route denied checks to the developer-run list; log the denial as liveness evidence | skill (graduated into exam-plan C0-1/C0-2 design 2026-09-13) |
