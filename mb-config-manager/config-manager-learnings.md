---
document: "Config Manager — Learnings"
doc-id: config-manager-learnings
state: Live
date-created: 2026-09-12
---

# Config Manager — Learnings

Transient way-station for the config-manager's own knowledge: patterns, decisions,
nuances — especially cross-cutting ones that apply to every system module. No
narrative, no history. Every entry is eventually dropped or written into a
**permanent home** (skill / config / reference / explainer) — then deleted from
here. The plan is never an absorption destination (it is transient; pruning into
a plan destroys the knowledge when the next cycle overwrites it). Entries never
accumulate. System-specific learnings live in that system's own
`{system}-learnings.md`; this file holds what generalizes.

| # | learning | right action | destination |
|---|---|---|---|
| 1 | Guard-denial classes are permanent execution boundaries: `.env` sourcing (secrets guard), `config.json` reads (sensitive-data guard), system-path reads (critical-path policy), cupcake-token paths (exec guard — matches even non-execution commands) | Any check in a blocked class is permanently developer-run; bundle those into the run's one developer request; never work around, never token-dodge | reference (Guard denials section — graduated 2026-09-12) |
| 2 | A check that passed earlier the same day may still be denied later (same-day pass-then-block proven on the postgres bridge). Guard behavior is not deterministic from the agent's viewpoint | Treat any once-denied check class as unreliable for agents; prefer developer-run on reclassification; never retry after denial | reference (Guard denials — graduated 2026-09-12) |
| 3 | Graduation timing: a learning is deleted on graduation, immediately — retention "until verified" contradicts the transient-file doctrine; verification belongs to the next exam-plan's carried-forward section | Delete on graduate; add verification duty to the plan instead | reference (Learnings procedure — recorded 2026-09-12) |