---
document: "GStack Skills Reference"
doc-id: gstack-skills-reference
state: Live
date-created: 2026-09-05
---

# GStack Skills Reference

Catalog of invocable GStack commands, verified live 2026-09-08 against the
installed `1.58.1.0` set. Topology and versions: `gstack-config.md`.
Workflows and authority: `gstack-reference.md`.

## Invocation rules — read before typing a command

- The slash command is the `name:` field in the skill's SKILL.md frontmatter
  — not the folder name. In current practice that is the bare skill name
  with the `gstack-` prefix dropped: the folder is `gstack-qa/`, the command
  is **`/qa`**. The prefixed form (`/gstack-qa`) returns nothing.
- **Exceptions that keep their full name:** `/gstack-upgrade` (frontmatter
  `name: gstack-upgrade`) and the aggregate `/gstack` router entry
  (frontmatter `name: gstack`).
- The `skill_prefix: true` option in `~/.gstack/config.yaml` would namespace
  all commands as `/gstack-<name>` — it is unset (default bare) here.
- If a known skill is missing or broken in OpenCode, re-run the installer:
  `cd /mnt/c/mybizz/gstack && ./setup --host opencode` — see
  `C:\_data-mybizz-mgt\WIP\_desktop\daily-ops.md`, "FIX: GSTACK SKILLS
  MISSING, OUTDATED, OR ONLY PARTIALLY WORKING IN OPENCODE".
- SKILL.md files are auto-generated — never edit one directly (see
  `gstack-config.md` for regeneration).

**Count: 53 invocable skills + the aggregate `/gstack` entry = 54** (verified
live 2026-09-08; supersedes all earlier counts of 52).

## Planning

| Command | What it does |
|---|---|
| `/office-hours` | YC Office Hours — six forcing questions for product ideas. Produces a design doc. |
| `/plan-ceo-review` | CEO/founder-mode plan review. Four modes: scope expansion, selective, hold, reduce. |
| `/plan-eng-review` | Eng manager review — locks in architecture, data flow, edge cases, test coverage. |
| `/plan-design-review` | Designer's-eye review — rates design dimensions 0–10, fixes the plan. |
| `/plan-devex-review` | Developer experience review — personas, benchmarks, friction points. |
| `/plan-tune` | Self-tuning question sensitivity — set per-question preferences. |
| `/autoplan` | Auto-review pipeline — runs CEO, design, DX reviews sequentially; eng review always last. |
| `/spec` | Turns vague intent into a precise, executable spec. Files a GitHub issue. |

## Build & Ship

| Command | What it does |
|---|---|
| `/review` | Pre-landing PR review — SQL safety, LLM trust-boundary violations, conditional side effects. |
| `/ship` | Detect + merge base, run tests, bump VERSION, update CHANGELOG, create PR. |
| `/land-and-deploy` | Merges PR, waits for CI, verifies production health via canary. |
| `/landing-report` | Read-only queue dashboard — claimed VERSION slots and open PRs. |

## Design

| Command | What it does |
|---|---|
| `/design-consultation` | Creates `DESIGN.md` — researches landscape, proposes full design system. |
| `/design-shotgun` | Generates multiple AI design variants, opens a comparison board. |
| `/design-html` | Generates production-quality HTML/CSS. |
| `/design-review` | Designer's-eye QA — finds visual issues, fixes with atomic commits. |
| `/diagram` | English description → Mermaid + editable `.excalidraw` + SVG/PNG. |

## QA & Testing

| Command | What it does |
|---|---|
| `/qa` | Systematically QA-tests a web app and fixes bugs found, committing each fix atomically. Three tiers: Quick, Standard, Exhaustive. |
| `/qa-only` | Report-only QA — structured bug report, no fixing. |
| `/benchmark` | Performance regression detection — Core Web Vitals, bundle sizes. |
| `/benchmark-models` | Cross-model benchmark — latency, tokens, cost, quality. |

## Investigation & Debugging

| Command | What it does |
|---|---|
| `/investigate` | Systematic debugging with root cause. Four phases: investigate, analyze, hypothesize, implement. |
| `/health` | Code quality dashboard — type checker, linter, tests, dead code, composite 0–10 score. |
| `/cso` | Chief Security Officer audit — secrets, dependency supply chain, CI/CD, LLM/AI security, OWASP, STRIDE. Daily (near-zero-noise) and monthly (comprehensive) modes. |

## Live audit

| Command | What it does |
|---|---|
| `/devex-review` | Live developer experience audit — actually tests the DX: navigates docs, times TTHW, screenshots errors. Compares against `/plan-devex-review` scores (the plan-vs-reality boomerang). Verified real 2026-09-08 (frontmatter + upstream description agree). |

## GBrain

| Command | What it does |
|---|---|
| `/setup-gbrain` | Installs and configures GBrain. **Do not trust its own backend description (PGLite/Supabase) — this environment runs self-hosted PostgreSQL; authority is `gbrain-config.md`.** |
| `/sync-gbrain` | Keeps GBrain current with a repo's code, refreshes agent search guidance. Flags: `--dream`, `--full`, `--code-only`, `--dry-run`. Idempotent. **`--dream` has a source-overlap trap against manually-registered sources — see `gbrain-reference.md` before using it.** |
| `/setup-deploy` | Configures deployment settings for `/land-and-deploy`. |

## Context & State

| Command | What it does |
|---|---|
| `/context-save` | Captures git state, decisions, remaining work for cross-session resume. |
| `/context-restore` | Loads the most recent saved context. |
| `/learn` | Manage project learnings — review, search, prune, export. |
| `/retro` | Weekly engineering retrospective — commit history, code quality, trends. |

## Safety

| Command | What it does |
|---|---|
| `/careful` | Warns before destructive commands (`rm -rf`, `DROP TABLE`, force-push). |
| `/freeze` | Restricts file edits to a specific directory for the session. |
| `/unfreeze` | Clears the freeze boundary. |
| `/guard` | `/careful` + `/freeze` combined. |

## Browser & Web

Browser skills run on GStack's bundled headless Chromium (Playwright) at
`1.58.1.0`. If they fail or hang, see
`C:\_data-mybizz-mgt\WIP\_desktop\daily-ops.md`, "FIX: GSTACK BROWSER SKILLS
WON'T LAUNCH".

| Command | What it does |
|---|---|
| `/browse` | Fast headless Chromium for QA — navigate, interact, screenshot, test. |
| `/open-gstack-browser` | Launch visible Chromium — watch agent actions in real time. |
| `/scrape` | Pull data from a web page. Returns JSON. |
| `/skillify` | Codify a `/scrape` flow into a permanent browser-skill. |
| `/setup-browser-cookies` | Import cookies from real Chromium into the headless session. |
| `/pair-agent` | Pair a remote AI agent with your browser. |
| `/canary` | Post-deploy monitoring — watches the live app for errors and regressions. |

## iOS

| Command | What it does |
|---|---|
| `/ios-qa` | Live-device iOS QA — connects to a real iPhone via USB, screenshots every screen. |
| `/ios-fix` | Autonomous iOS bug fixer — finds bug, writes fix, rebuilds, verifies on device. |
| `/ios-design-review` | Visual design audit for iOS apps on real hardware. |
| `/ios-sync` | Regenerates the iOS debug bridge against latest gstack templates. |
| `/ios-clean` | Removes the DebugBridge SPM package and `#if DEBUG` wiring. |

## Documentation

| Command | What it does |
|---|---|
| `/document-generate` | Generates missing docs from scratch (Diataxis framework). |
| `/document-release` | Post-ship doc update — cross-references diff, updates README/CHANGELOG. |
| `/make-pdf` | Turns markdown into a publication-quality PDF. |

## CLI wrappers

| Command | What it does |
|---|---|
| `/codex` | OpenAI Codex CLI wrapper — Review, Challenge, Consult modes. |
| `/claude` | Claude Code CLI wrapper — Review, Challenge, Consult modes. |

## Aggregate

| Command | What it does |
|---|---|
| `/gstack` | Router entry (frontmatter `name: gstack`) — orients the agent over the whole skill set. |

## Pipelines

**Planning** (new projects):
```
/office-hours → /plan-ceo-review → /plan-eng-review → /plan-design-review → /plan-devex-review → /plan-tune
```
Or run everything at once: `/autoplan`

**Build & ship** (after planning locked):
```
/review → /qa → /ship → /land-and-deploy
```

**Design** (new visual identity):
```
/design-consultation → /design-shotgun → /design-html → /design-review
```

**Daily workflow:**
```
/context-restore → work → /context-save
```

**Investigation:**
```
/investigate → /review → /qa → /ship
```

## Not real commands — do not assume these exist

- **`/handoff`** — no corresponding folder anywhere in the source repo.
- **`hackernews-frontpage`** — exists only as a sub-skill under
  `/mnt/c/mybizz/gstack/browser-skills/hackernews-frontpage/`; its discovery
  symlink is broken (dead target) and it is not a standalone command.

## Separate, unrelated set

Four `gstack-openclaw-*` folders (`ceo-review`, `investigate`,
`office-hours`, `retro`) exist in the discovery path — installed via
`clawhub install` for OpenClaw, which is not used in this environment.
Not part of this catalog; deliberately not removed (an update recreates them).

## Do not

- Do not type the `gstack-` prefix — bare names, except `/gstack-upgrade`
  and `/gstack`.
- Do not assume `/handoff` exists or that `hackernews-frontpage` is a
  standalone command.
- Do not trust `/setup-gbrain`'s own backend description — check
  `gbrain-config.md`.
- Do not hand-edit any SKILL.md — regenerate from the template.
- Do not run `/sync-gbrain --dream` against a manually-registered GBrain
  source — source-overlap trap (see `gbrain-reference.md`).
