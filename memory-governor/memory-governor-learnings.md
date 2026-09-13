---
document: "Memory Governor — Learnings"
doc-id: memory-governor-learnings
state: Live
date-created: 2026-09-13
---

# Memory Governor — Learnings

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
| 1 | The governor's API auth-gate is itself a liveness probe: an unauthenticated request returning **422** proves the gate is closed AND the API is alive in one check — a 200 would mean the gate is silently open | Tier-0 check M0-4 asserts the 422; any 200 = UNHEALTHY finding | skill (born with the exam-plan design 2026-09-13) |
| 2 | Row-count expectations are point-in-time — the governor DB is live (worker/API write continuously); exact equality with any recorded count can only hold at verification time | Compare against last recorded + growth explainability; exact equality never asserted | config.md (row-count notes — via governance refresh) |
| 3 | The worker log carries **no timestamps**, and its retry warnings show only "attempt 1/5" with no resolution lines — failed-event fate is undeterminable from the log alone | Tier-1 finding class: worker retry outcomes require developer verification (event status via DB query + worker PATH check); a logging-timestamps code change is a gated developer decision | skill Tier 1 note (graduated 2026-09-13); developer decision pending |