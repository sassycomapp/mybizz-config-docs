---
title: "2026-09-15-006-archify-scope-skill"
doc-id: "mb-6c56787b"
updated: "2026-10-01"
---
# Session 006 — mb-archify-scope

Session number 006 (per the developer sessions log). Documents the design,
installation, and first live run of the `mb-archify-scope` front-of-pipe skill,
plus the Archify authoring learnings gained from the Run Learnings (memory-ecosystem 2026-09-15) diagram.

## What happened this session

1. **Diagnosis of an earlier Archify failure.** The original "map the memory
   flows" task (dataflow, keyword-chosen) failed with 42→21→12 route/corridor
   diagnostics: the Gate column acted as a wall, and explicit `via` conflicted
   with the renderer's automatic port spread. Conclusion: Archify needs
   pre-work before a drawing project.

2. **The scoping skill was agreed and produced.** Eight-phase contract finalized
   with the developer (Intent, ASK, Context, Preliminary scope, Scope the source,
   Feasibility probe, Report and gate, Handoff contract) plus a Phase 9
   close-out (learnings) added during the run. Deliverables:
   - Repo spec: [[[mybizz-config-docs:archify/archify-scope-skill|Scoping Skill Specification]]](C:/mybizz/mybizz-config-docs/archify/archify-scope-skill.md)
   - Installed skill: `~/.config/opencode/skills/mb-archify-scope/SKILL.md`
     (invoked as `/mb-archify-scope`; rename from `mb-archify-scoping`)
   - Output folder: `C:\mybizz\mybizz-config-docs\archify\output\`

3. **First live run — memory-ecosystem architecture diagram.** Scope approved:
   [[[mb-3-cs-project-library:docs-local/architecture|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md) type (guide-consistent), 9 primary nodes, one store with two
   badges (GBrain: mirror/durable), read paths as primary nodes, one
   `security-group` "durable gate" boundary. Probe (nodes-only) passed before
   connecting. Authoring converged 17 → 0 diagnostics over two focused repair
   rounds.

4. **Delivery + browser evidence.**
   - `validate`: 9/9 showcase artifact checks, 0 errors, 0 warnings
   - `deliver`: atomic, SHA-256 receipts for spec and artifact
   - `visual-check`: Chrome available via Playwright Chromium
     (`~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`); produced
     four viewport PNGs + contact sheet; **containment gate fails at all four
     desktop viewports** — the shipped reference example
     (`examples/dataflow-product-analytics.html`) fails identically, so the
     strict `scrollHeight <= innerHeight` gate is viewer-inherent for
     card-bearing artifacts, not a defect of this drawing
   - `visual_review: passed` — recorded on the developer's own inspection of
     the rendered artifact (this model cannot read the PNG sidecars;
     `image input not supported`)

5. **Output artifacts.**
   - memory-ecosystem (Scope Card)
   - `output/memory-ecosystem-header.json` (machine contract)
   - `output/memory-ecosystem-probe.json` (stub probe — passes)
   - `output/memory-ecosystem-draft.json` (frozen candidate)
   - `output/memory-ecosystem-render.html` (delivered artifact)
   - `output/memory-ecosystem-render.visual-check.*.png` (+ contact sheet + JSON)
   - Run Learnings (memory-ecosystem 2026-09-15) (10 run learnings)

## Key learnings (detailed in the run learnings file)

- Type choice is the highest-leverage scoping decision; run
  `archify guide "<scenario>" --json` at scope time; prefer [[[mb-3-cs-project-library:docs-local/architecture|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md)
  (free pos, edge-tolerant) unless grid semantics are required
- Probe (components+boundary stub) before connecting — catches
  desktop-readability/font-scale and overlap classes pre-flight
- Explicit `via`/`fromSide`/`toSide` must hit exact side-midpoint anchors;
  Automatic Port Spread is skipped for explicit routes
- ViewBox must fit ~1240px usable width for 1440px desktop (else sub-6px fonts)
- Anti-parallel read pairs need separate physical channels (one over, one under)
- Desktop containment `scrollHeight <= innerHeight` is unachievable for
  card-bearing artifacts in this viewer build (reference-calibrated)
- Visual review requires an image-capable reviewer; the developer's look is the
  perceptual review

## Open items (carried forward)

- **Installed skill Phase 9 sync**: the repo spec has Phase 9 (close-out
  learnings); the installed copy at
  `~/.config/opencode/skills/mb-archify-scope/SKILL.md` still needs the
  developer's `cp /tmp/opencode/installed-SKILL.md
  ~/.config/opencode/skills/mb-archify-scope/SKILL.md` to land (skill-directory
  writes are blocked for the agent by policy)
- **Git**: [[[mybizz-config-docs:archify/archify-scope-skill|Scoping Skill Specification]]](C:/mybizz/mybizz-config-docs/archify/archify-scope-skill.md) and `archify/output/` are new/untracked in
  `mybizz-config-docs`; also a pre-existing modification to
  [[[mybizz-config-docs:gbrain/gbrain-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-explainer.md) (not from this session) — commit/push pending
  developer instruction
- The archify GBrain knowledge gap noted in [[[mybizz-config-docs:archify/archify-config|Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) (no dedicated
  GBrain page) is partially addressed by this session page

## Next steps

- Developer runs the Phase 9 copy command for the installed skill
- On instruction: commit + push to GitHub (`mybizz-config-docs`), then run the
  gbrain sync script
- Future drawing tasks route through `/mb-archify-scope` first
