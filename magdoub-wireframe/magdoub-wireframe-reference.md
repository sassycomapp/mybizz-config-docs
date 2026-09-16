---
document: "magdoub-wireframe — Reference: Invocation, Operation, Update"
doc-id: magdoub-wireframe-reference
state: Live
date-created: 2026-09-06
---

# magdoub-wireframe — Reference: Invocation, Operation, Update

Companion to `magdoub-wireframe-config.md` (current installed state, open items)
and `magdoub-wireframe-explainer.md` (design reasoning, system relationships).
Agent-facing. The full generation procedure lives in the skill's own `SKILL.md`
(auto-loaded on invocation); this doc carries what is needed to invoke, run,
constrain, update, and remove the skill on this machine.

Config-management set: `magdoub-wireframe-exam-plan.md` (transient job-spec — read
second, every run), `magdoub-wireframe-exam-report.md` (last verified state),
`magdoub-wireframe-log.md` (chronological events),
`magdoub-wireframe-learnings.md` (transient knowledge). The exam skill's canonical
source is `magdoub-wireframe-skill.md` (installed as `mb-config-magdoub-wireframe`).

---

## Invocation

```
/wireframe <free-text description of the feature or screen>
```

No flags. A directional intent embedded in the description ("more conversions",
"reduce clutter", "simplify", "redesign for X") is extracted automatically and
used as the optimization lens — no question asked when present.

## Questions the skill asks (and when)

| Question | When | Options |
|---|---|---|
| Wireframes only, or wireframes + visuals? | Arguments don't mention visuals | Wireframes + visuals (Clean + Polished — recommended) / Wireframes only |
| Optimization goal | Only when the description is neutral (no directional intent) | Conversions / drop-offs / time on page / discoverability — or skip |
| Target platform | First run only, if code + screenshots don't make it obvious | Mobile / Desktop-Web / Both (responsive) |
| Clarifications | At most 1–2, only on genuine feature ambiguity — never about visual styling | Free-form |

## First run in a project (ordered)

1. Create `wireframe/` and `wireframe/brain/` at project root if absent.
2. Create `wireframe/brain/design-taste.md` from the bundled template if absent.
3. If `wireframe/brain/design-context.md` exists: read it plus design-taste.md; skip to Phase 1.
4. If not: scan the codebase — CSS/SCSS/Less/CSS-in-JS, JS/TS/JSX/TSX, templates, key entry pages — for navigation, layout patterns, hierarchy, interactive elements, breakpoints, conventions.
5. Ask for 2–3 screenshots of the current app's key pages; save them into `wireframe/brain/`.
6. Ask target platform if still ambiguous; write `design-context.md` with the full structure (overview, platform, layouts, navigation, page types, interactions, hierarchy, screenshot observations, conventions).

## Phase 1 — UX Architect (B&W wireframes)

1. Create the output folder `wireframe/DDMM-<feature-name>/` — day-then-month, zero-padded (Feb 22 → `2202`). Not MMDD; the README's label is wrong, SKILL.md is authoritative.
2. Copy the bundled `wireframe/templates/base.css` into the output folder.
3. Copy the bundled `wireframe/templates/template.html` to `index.html`.
4. Create 5 empty `styles-optN.css` files.
5. Edit `index.html` placeholders: `FEATURE_NAME`, `PROJECT_NAME`, `rec-number` N, `OPTION_1..5_NAME`, `OPTION_1..5_PHILOSOPHY`, `FEATURE_SLUG` (replace_all), `<!-- OPTION_N_CONTENT -->`, `<!-- OPTION_N_ANNOTATIONS -->`, `<!-- SUMMARY_CONTENT -->`.
6. Write `styles.css` — wireframe-content rules only; framework rules are already in base.css, do not duplicate them. Budget ≤ 300 lines. Any `@import` goes at the very top.
7. Generate 5 options: Option 1 = Safe, extending patterns from `design-context.md`; Options 2–5 = each a genuinely different UX philosophy.
8. Do not modify the template's inline JS; do not regenerate footer, banner, badges, or browser chrome — they are pre-built in the template. One panel per option; the wrapper class toggles `wireframe`/`clean`/`polished`; annotations hide on color variants via CSS.
9. Wireframe sub-tab palette is strict: `#000 #333 #666 #999 #ccc #eee #fff` — no color, no brand colors; solid borders only; `href='#'` on all links; system fonts only; no CDN or external dependencies in Phase 1.
10. Open `index.html` in the browser; report options generated, recommendation with one-line rationale, per-option summaries, folder path. If scope is wireframes-only, stop here.

## Phase 2 — Visual Designer (color variants)

**Environment constraint first.** *Cupcake qualifier: Cupcake's enforcement
status is not fixed and should not be assumed current at any given time — check
`cupcake-config.md`'s Current Operational Status before treating any
enforcement statement below as active, mechanical enforcement. What follows is
standing policy and what enforcement does when active; the behavioral rule
holds regardless of enforcement status.*

SKILL.md's Phase 2 instruction is to launch 5 parallel foreground Task agents.
Standing policy in this environment prohibits sub-agent creation, enforced when
active at three independent layers (OpenCode config deny — tool removed from
the visible set; `cup-block-task-tool.rego` + `spawn-tools-denylist.json`;
standing skill-review habit). As of this suite's research date (2026-09-06) the
`task` tool did not appear in the tool set. Do not invoke that instruction as
written. The replacement mechanism on this machine is unresolved —
`magdoub-wireframe-config.md` open item 1. What Phase 2 must produce, per
option N, by whatever mechanism runs it:

1. Read `index.html`, the option's own `styles-optN.css`, `design-taste.md`, `design-context.md`.
2. Write only `styles-optN.css` — never modify `index.html`. Budget ≤ 200 lines.
3. `.clean .selector` rules: flat color from the project palette, system fonts, no gradients or shadows.
4. `.polished .selector` rules: same palette and light base as Clean, plus Google Font pairing (`@import` at file top), perceptible same-hue gradients on light backgrounds, soft multi-layer shadows, entrance/hover micro-interactions honoring `prefers-reduced-motion`.
5. Color the browser-chrome dots per variant (`.clean .browser-dots span:nth-child(1)` red/yellow/green pattern).
6. Never dark backgrounds in Polished; palette from `design-context.md` only — no invented brand colors; layout locked (only `color`, `background`, `border-color`, `box-shadow`, `font-family`, `font-weight`, `transition`, `animation` may be overridden).
7. Append the self-reveal rules from the bundled `wireframe/templates/self-reveal.css`, with `N` replaced by the option number.
8. Avoid the five named CSS anti-patterns in SKILL.md: border/content overlap, clipped full-width sections, imperceptible gradients, content escaping the frame, dark-mode Polished.

## After generation

Check whether the run revealed page types or patterns not yet in `design-context.md`; append them to the appropriate section.

## Update (developer-run only)

```bash
git -C ~/.claude/skills/wireframe fetch origin && git -C ~/.claude/skills/wireframe reset --hard origin/main
```

- Developer-run only, from a terminal — never AI-invoked (cross-project-write rule; `reset --hard` also discards any local changes).
- The OpenCode symlink needs no action after an update — it points at the same path regardless of content.
- Content reaches GBrain by ordinary `gbrain sync` only — never through Memory Governor's API (permanent vendor-material bypass; see `magdoub-wireframe-config.md`).
- After any update, re-check bundled template paths referenced in Phase 1 — upstream commit 44a5814 moved these to "this skill's bundled" locations.

## Uninstall

```bash
rm -rf ~/.claude/skills/wireframe
```

Then remove the now-broken symlink `~/.config/opencode/skills/wireframe/SKILL.md` separately.

## Do not

- Do not launch the Phase 2 parallel Task agents as SKILL.md instructs — standing policy prohibits sub-agent creation regardless of enforcement status (three-layer denial enforces it when active) and the mechanism is an open item.
- Do not run the update command via AI/bash — developer-run only.
- Do not submit skill content through Memory Governor — permanent bypass; ordinary `gbrain sync` only.
- Do not create a second discovery path for this skill — a duplicate path double-loads it (dedup is by discovery path).
- Do not use any color or dotted/dashed borders in the Wireframe sub-tab — the palette is strictly the seven listed values.
- Do not follow the upstream README's MMDD folder label — DDMM per SKILL.md.
- Do not edit files inside the real clone expecting changes to survive an update — `reset --hard` discards them.
- Do not generate wireframes in a project governed by the `design-rules` ADR without completing that ADR's mandatory pre-wireframe reading — its authority is independent of this skill's own flow.
- Do not treat skill-index "working" as run evidence — no confirmed real run exists in this environment.
