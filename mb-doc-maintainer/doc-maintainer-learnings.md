---
title: "doc-maintainer-learnings"
doc-id: "mb-92498092"
---
# mb-doc-maintainer — Learnings

Transient way-station for exam-run knowledge: patterns, decisions, nuances. No
narrative, no history. Every entry is eventually dropped or written into a
**permanent home** (skill / config / reference / explainer) — then deleted from
here immediately on graduation. The plan is never an absorption destination —
it is transient; pruning into a plan destroys the knowledge when the next cycle
overwrites it. Entries never accumulate. Cross-cutting learnings (guard classes,
graduation rules) live in the orchestrator's own
[[config-manager-learnings|Learnings]], not here.

| # | learning | right action | destination |
|---|---|---|---|
| 1 | The 2026-09-24 corpus retrofit normalized every config-manager suite skill-source to corpus two-field frontmatter, splitting sources (title/doc-id) from installed copies (name/description) — a systemic hash divergence that re-flags every future step-0 | **RESOLVED 2026-09-25 at the doc-maintainer run #1 gate:** option (a) approved — register hashes re-baselined to post-retrofit sources; dual-format convention recorded in the register's install-discipline note; step-0 source↔installed comparisons treat the frontmatter block as the expected difference | Graduated into config-manager-register (install-discipline note) — deleted |
| 2 | The suite folder's ninth file (doc-maintainer-run-log.md) is a spec-recorded component artifact co-resident with the 8-file suite standard — "8 files" checks must read the spec's Storage table, not a bare count | Already handled: DM1-7 expected-value wording notes the co-residency | Graduated into skill (DM1-7) at birth — no further action |
| 3 | register.py correctly detects legacy malformed register rows (unescaped pipes, 6 cells) on real data — the finding classes work beyond the test fixtures | F-3 delegated to maintainer work at the gate (the tool exists for exactly this) | Closed at gate — no permanent home needed beyond the report |
| 5 | Stop-ScheduledTask does not kill the cmd-wrapper's PowerShell child — the orphan keeps holding the single-instance mutex; an explicit process kill is required before a restart can take the guard | Already embedded in the reference watcher-management section as the kill-then-restart pattern | Graduated into skill hard-rules + reference — deleted |