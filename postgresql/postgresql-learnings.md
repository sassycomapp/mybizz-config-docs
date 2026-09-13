---
document: "PostgreSQL — Learnings"
doc-id: postgresql-learnings
state: Live
date-created: 2026-09-12
---

# PostgreSQL — Learnings

Transient way-station for exam-run knowledge: patterns, decisions, nuances. No
narrative, no history. Every entry is eventually dropped or written into a
**permanent home** (skill / config / reference / explainer) — then deleted from
here immediately on graduation. The plan is never an absorption destination — it
is transient; pruning into a plan destroys the knowledge when the next cycle
overwrites it. Entries never accumulate. Cross-cutting learnings (guard classes,
graduation rules) live in the orchestrator's own
`mb-config-manager/config-manager-learnings.md`, not here.

| # | learning | right action | destination |
|---|---|---|---|
| 1 | `facts` table never autovacuumed — low-write, not pathological; hot-table vacuum recency is the real signal | Flag only if a hot table stops vacuuming | config.md refresh (docs governance — pending approval) |