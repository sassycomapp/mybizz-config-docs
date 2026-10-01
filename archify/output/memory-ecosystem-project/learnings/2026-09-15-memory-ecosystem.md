---
title: "2026-09-15-memory-ecosystem"
doc-id: "mb-9e40a3d5"
updated: "2026-10-01"
---
# Archify — Run Learnings — memory-ecosystem (2026-09-15)

Transient way-station for learnings gained from the first real `/mb-archify-scope`
run and its Archify authoring. Model-inferred; each entry is either dropped or
graduated into a permanent home (`mb-archify-scope` skill → [[[mybizz-config-docs:archify/archify-scope-skill|Scoping Skill Specification]]](C:/mybizz/mybizz-config-docs/archify/archify-scope-skill.md),
or [[[mybizz-config-docs:archify/archify-reference|Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md) / [[[mybizz-config-docs:archify/archify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/archify/archify-learnings.md) suite file) — then deleted.

| # | learning | right action | destination |
|---|---|---|---|
| 1 | **Type choice is the highest-leverage scoping decision.** "Memory flows" → `dataflow` (keyword-driven) produced repeated corridor-wall failures in an earlier session (42 → 21 → 12 diagnostics with nodes stacked in the gate column). Re-scoped as [[[mb-3-cs-project-library:docs-local/architecture\|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md) (guide-consistent), the same subject validated clean in two repair rounds. `dataflow` is a strict stage/row grid (row tops `y=128,242,356,470,584`, stage centers `x=100+stage×215`); [[[mb-3-cs-project-library:docs-local/architecture\|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md) uses free `pos` and forgives edge count | Run `archify guide "<scenario>" --json` at scope time; pick the forgiving type unless the subject demands grid semantics; record type+why in the Scope Card | skill (Phase 4 decision tree — graduate the dataflow budget table) |
| 2 | **Probe before connecting.** A components+boundary-only stub validates in seconds and surfaces the composition/desktop-readability class of failure (e.g. viewBox too wide → sub-6px projected font) before any flow/label work. This converted last session's heat-of-battle diagnostics into a pre-flight pass | Always run the stub probe (Phase 6) before authoring connections; abort-and-reshape on probe failure | skill (Phase 6 — already declared; note probe catches font-scale, not just overlaps) |
| 3 | **Desktop readability is a viewBox-width constraint.** At 1440px desktop the viewer scales the whole SVG down; a 1360-wide viewBox dropped a 8.4px sublabel to 5.7px (`composition/desktop-readability`). Compress node columns and widen long-label nodes instead of shrinking copy | Size the viewBox for ≤~1240 usable width; widen nodes that carry long sublabels; re-probe at 1440 | reference (desktop-readability fix — graduate) |
| 4 | **Explicit `via`/`fromSide` must hit exact side-midpoint anchors.** With explicit geometry the renderer pins ports at node side midpoints (e.g. GBrain top port at `(880,300)`, left at `(790,336)`); a `via` not sharing the port coordinate makes a diagonal final segment and fails `endpoint-side-direction`. Automatic Port Spread is skipped for explicit routes, so multi-flow sides share one midpoint | Derive `via` coordinates from computed port midpoints; or leave the side automatic and let spread handle multi-flow sides; never mix one hardcoded port with several auto ones on the same side | reference (authoring contract note — graduate; learned empirically via logger) |
| 5 | **Override auto routes in the order: crossing → endpoint direction → label.** The contract's repair order held: after crossings and endpoint-direction are clean, remaining diagnostics are label-route-clearance only. Two focused repair rounds took the full candidate from 17 → 0 | Keep single-diagnostic repairs until the objective count reaches a new minimum; stop repairing at the minimum | skill (antis-duplication — reference repair order) |
| 6 | **The shared-corridor read pair needs physical separation.** Bidirectional flows between two adjacent nodes (developer ⇄ GBrain) collide on a shared 70px channel; labels cannot coexist there. Fix: route one over the top, one along the bottom, each on its own orthogonal channel with its own label band | In the corridor plan (Phase 5), name a separate lane for each anti-parallel pair; don't expect the router to separate them | skill (corridor plan guidance — graduate) |
| 7 | **Showcase desktop containment (`scrollHeight <= innerHeight`) is not achievable for card-bearing artifacts in this viewer build.** The shipped `examples/dataflow-product-analytics.html` (9/9-validated) fails the identical overflow check at all four viewports; my artifact overflows 1414–1534. The viewer stacks dock + diagram + legend + cards vertically; the gate is a regression guard, not a passable bar | Report `browser_evidence: failed` truthfully with the reference-artifact calibration; treat overflow as viewer-inherent when the reference fails identically; still compact redundant viewBox height | reference (delivery-contract calibration note — graduate) |
| 8 | **Visual review requires an image-capable reviewer.** The agent model here cannot read the PNG sidecars (`image input not supported`); the developer's own look at `output/memory-ecosystem-render.html` (or the `.visual-check.*.png` files) is the perceptual review. `visual_review: passed` was recorded on the developer's confirmation | Always write the four PNG sidecars (via visual-check chrome available) so a human can review; report `visual_review` only from an actual inspection | reference (delivery contract — already documented; noted the model limit) |
| 9 | **Automated learnings capture needs a trigger, not a watcher.** No demon in this stack watches Archify runs and writes learnings; the pack's update checker only checks version state, and the skill itself produces no log. A developer-requested learnings write (as now) is the reliable trigger. | Make learnings capture explicit: developer invokes `/mb-archify-scope (learnings)` or asks to write learnings after a run; the skill appends to `output/learnings/` | skill (Phase 8 extension — optional future "learnings" verb) |
| 10 | **GBrain is PostgreSQL (multi-writer); "database is locked" is a SQLite-family message.** Locks here would come from a PGLite/SQLite-backed tool, not the Postgres brain; `gbrain sync` runs alongside a live MCP session with no lock conflict (standing record) | On a "database is locked" error, identify the SQLite/PGLite holder; check WAL/busy_timeout; don't chase it in Postgres tooling | facts (not Archify-specific; cross-reference only) |

## Automation answer for the developer

Full unattended capture is not possible in this stack: nothing fires "on run
complete" — the skill's own lifecycle ends at handoff, the update checker is
version-only, and there is no daemon watching the CLI. The reliable triggers,
in order of preference:

1. **Developed-invoked verb** — extend `/mb-archify-scope` with an explicit
   `learnings` verb; the developer types `/mb-archify-scope (learnings)` at
   close-out, and the skill writes the run's entries to `output/learnings/`.
   Same single-run discipline as the recording skills.
2. **Close-out question** — the skill's Phase 8 handoff lists "record
   learnings?" as its final question; the agent writes the file when approved.
3. **Suite file graduation** — the run file stays transient; notable entries are
   promoted into [[[mybizz-config-docs:archify/archify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/archify/archify-learnings.md) (suite) then into the skill/reference.

*End of document*
