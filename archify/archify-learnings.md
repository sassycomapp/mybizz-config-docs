---
document: "Archify — Learnings"
doc-id: archify-learnings
state: Live
date-created: 2026-09-16
---

# Archify — Learnings

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
| L-1 | The memory-ecosystem run's canonical facts were graduated into the explainer/reference permanent homes during suite build-out (run #1) — type-choice leverage, probe-before-connect, desktop viewBox constraint, exact-port anchoring, repair order, corridor separation, visual-review-by-human | Learnings file starts transient at run #1 with nothing to absorb; future runs record only run-observed patterns not already permanently documented | explainer / reference (already graduated) |
| L-2 | The scoping skill is a documented component of this suite (config §Scoping skill component) — the exam's scope includes verifying the installed scope-skill copy stays byte-identical to `archify-scope-skill.md` (AR2-3) | Treat the scope-skill as examinable state, not an external skill | skill (AR2-3 already carries it) |
| L-3 | Run #1 proved the AR2-3 pattern fires: the installed scope-skill copy had drifted (missing Phase 9) and was re-synced at the gate with the hash pair `0e40e984ba82a5f6`. The general class (spec-gained-after-install) is captured in `config-manager-learnings.md` #5 | Keep the re-sync path gated; the hash check every run is the detection that made it visible | skill (AR2-3) + config-manager-learnings #5 (graduated) |