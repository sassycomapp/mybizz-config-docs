---
title: "2026-11-17-pdlf-step20-design-system"
doc-id: "mb-a636f57b"
updated: "2026-11-18"
---
# PDLF Step 20 — Design System (run app1) — 2026-11-17

## What was done

The orchestrator resumed run `app1` at Step 20 (Design system, Phase C). The prior state: steps 11–19 complete, gate `domain-locked` passed; Step 20 had no row. Step 20 ran as the `design-consultation` skill held to `c20-config.md`'s fixed answers. Evidence: `mb-3-cs-project-library/pdlf-outputs/c20/` — `mb-3-cs-c20-app1-checks.xml` (PR-01, DC-12: 2 passed, 0 failed), the design copy, and the Step Receipt. Ledger: Step 20 `complete`, BFT full record id 9.

The work: `docs-local/DESIGN.md` was rewritten under the developer's law — nothing departs from `m3-custom-theme`; the document records choices only, named with the theme's tokens (`--m3x-*`, colour roles, type roles); every value and every recorded departure removed (type scale, spacing scale, radius/elevation/density tables, the `color-mix()` card shadow, the hairline opacity, state-layer percentages, pixel lengths, and the whole "Project Deviations from M3 Defaults" section — nine departures). Anvil canonical built-in components are not departures. Roboto stays as Material 3's standard typeface. Every decision, lifecycle, permitted-action table and empty state was carried.

## Decisions and standards the developer set

1. **No upgrades in PDLF.** Gstack and gbrain update prompts are permanently disabled (`gstack-config set update_check false`); upgrades are the developer's own schedule, never part of a PDLF step.
2. **The theme law** (above). The only departure is a colour, font, size or style value of our own that the theme does not define; none allowed.
3. **Approved with the step:** menu style `baseline` and motion scheme `standard` stay as recorded, carried into ticket `19-f31-design-system`'s startup calls.

## Quirks

- The PowerShell bridge mangles JSON with escaped double quotes; `jsonb_build_object()` in SQL avoids the problem.
- The theme's WCAG AA contrast guarantee lives in `m3-custom-theme-project-library/tools/build_palettes.py` (4.5:1 text, 3:1 outlines, every palette, light and dark, build stops on failure) and `m3-custom-theme.md` line 41 — DC-12's evidence, not authored by the step.

## Documents written or changed

- `mb-3-cs-project-library/docs-local/DESIGN.md` — rewritten (choice 1 of the step).
- `mb-3-cs-project-library/pdlf-outputs/c20/mb-3-cs-c20-app1-checks.xml`, `-design.md`, `-receipt.md`.
- `~/.gstack` config: update checks disabled.

## Open

- Run `app1` continues at Step 21 (concept lock) in a new session via `/pdlf-init`.
