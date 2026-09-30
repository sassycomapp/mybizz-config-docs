---
title: "config-manager-learnings"
doc-id: "mb-8c382f68"
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
| 4 | An honoured denial never substitutes for a formal execution: a run re-executes denied checks (clean, single-purpose commands; write grants requested via mg-grant where a write outside the project is required) or reclassifies them developer-run — prior-session evidence informs but never substitutes (developer standard, stated 2026-09-14 during graphify run #1) | Re-execute or reclassify at once; never mark a denied check PASS on earlier evidence | reference (Guard denials / Developer-returned results sections) |
| 5 | A component skill's installed copy drifts silently when its spec gains a phase after install (archify run #1: `mb-archify-scope` installed 15:58, spec gained Phase 9 at 17:22, same day). The suite folder holds the canonical spec; the installed copy is a copy — a spec edit is not a re-install | Component skills (front-of-pipe helpers, not just exam modules) need the same source↔installed hash discipline as the exam skills; step-0's glob form already catches them when they live under `~/.config/opencode/skills/` | skill (step-0 / AR2-3 pattern — graduated into the archify skill row; recorded here for the general class) |