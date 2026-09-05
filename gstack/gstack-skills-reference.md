# GStack Skills Reference

**Location:** skills are generated from `/mnt/c/mybizz/gstack/` (the
GStack source repo) and installed into
`~/.config/opencode/skills/gstack-<name>/SKILL.md` by running
`cd /mnt/c/mybizz/gstack && ./setup --host opencode`.

**Invocation — read this before typing a command.** The folder name and
the actual invocable command are not the same thing. Each skill's
`SKILL.md` frontmatter declares a `name:` field, and that field — not
the folder name — is what OpenCode registers as the slash command. In
current practice this `name:` field is the bare skill name without the
`gstack-` prefix. Example: the folder is `gstack-qa/SKILL.md`, its
`name:` field is `qa`, and the real command is **`/qa`**, not
`/gstack-qa`. Confirmed directly: `/gstack-qa` returns nothing;
`/qa` works. Type the bare name for every skill below.

**Verified count:** 52 skills currently installed and confirmed present
(per the setup script's own "linked skills" output, cross-checked
against the reference install at `/mnt/c/mybizz/gstack/.agents/skills/`).
The two items below are listed with their status marked, not silently
dropped or silently kept:
- `/handoff` — no corresponding folder found in the source repo. Not
  confirmed to exist. Do not assume it's installed.
- `/hackernews-frontpage` — exists as a sub-skill under
  `/mnt/c/mybizz/gstack/browser-skills/hackernews-frontpage/`, not as a
  top-level `gstack-*` folder. Not confirmed wired as a standalone
  OpenCode command.

**Separate, unrelated set — do not confuse with the catalog below:**
four `gstack-openclaw-*` folders (`gstack-openclaw-ceo-review`,
`gstack-openclaw-investigate`, `gstack-openclaw-office-hours`,
`gstack-openclaw-retro`) also exist in
`~/.config/opencode/skills/`. These are OpenClaw-specific skills
installed via a different mechanism (`clawhub install`), not part of
this GStack catalog. Not yet investigated for relevance — see
`master-task-list.md`.

---

## Planning Skills

| Skill | What it does |
|---|---|
| `/office-hours` | YC Office Hours — six forcing questions for product ideas. Produces design doc. |
| `/plan-ceo-review` | CEO/founder-mode plan review. Four modes: scope expansion, selective, hold, reduce. |
| `/plan-eng-review` | Eng manager review — locks in architecture, data flow, edge cases, test coverage. |
| `/plan-design-review` | Designer's eye review — rates design dimensions 0-10, fixes the plan. |
| `/plan-devex-review` | Developer experience review — personas, benchmarks, friction points. |
| `/plan-tune` | Self-tuning question sensitivity — set per-question preferences. |
| `/autoplan` | Auto-review pipeline — runs CEO, design, eng, DX reviews sequentially. |
| `/spec` | Turns vague intent into a precise, executable spec. Files as GitHub issue. |

## Build & Ship Skills

| Skill | What it does |
|---|---|
| `/review` | Pre-landing PR review — SQL safety, trust boundaries, conditional side effects. |
| `/ship` | Detect + merge base, run tests, bump VERSION, update CHANGELOG, create PR. |
| `/land-and-deploy` | Merges PR, waits for CI, verifies production health via canary. |
| `/landing-report` | Read-only queue dashboard — shows claimed VERSION slots and open PRs. |

## Design Skills

| Skill | What it does |
|---|---|
| `/design-consultation` | Creates DESIGN.md — researches landscape, proposes full design system. |
| `/design-shotgun` | Generates multiple AI design variants, opens comparison board. |
| `/design-html` | Generates production-quality Pretext-native HTML/CSS. |
| `/design-review` | Designer's eye QA — finds visual issues, fixes with atomic commits. |
| `/diagram` | English description to mermaid + editable .excalidraw + SVG/PNG. |

## QA & Testing Skills

| Skill | What it does |
|---|---|
| `/qa` | Systematic QA testing + iterative bug fixing. Three tiers: Quick, Standard, Exhaustive. Confirmed working — direct test, correct agent response. |
| `/qa-only` | Report-only QA — produces structured bug report without fixing. |
| `/benchmark` | Performance regression detection — Core Web Vitals, bundle sizes. |
| `/benchmark-models` | Cross-model benchmark — compares LLMs on latency, tokens, cost, quality. |

## Investigation & Debugging

| Skill | What it does |
|---|---|
| `/investigate` | Systematic debugging with root cause. Four phases: investigate, analyze, hypothesize, implement. |
| `/health` | Code quality dashboard — type checker, linter, tests, dead code, composite 0-10 score. |
| `/cso` | Security audit — secrets, supply chain, CI/CD, OWASP, STRIDE. |

## GBrain Skills

| Skill | What it does |
|---|---|
| `/setup-gbrain` | One-time GBrain setup — CLI, PGLite, MCP, trust policy. |
| `/sync-gbrain` | Keep GBrain current — sync code, memory, update AGENTS.md guidance. Accepts `--dream`, `--full`, `--code-only`, `--dry-run`. |
| `/sync-gbrain --dream` | Build call graph via dream cycle. Prerequisite: code-aware schema pack. |
| `/sync-gbrain --full` | Full code reindex (~25-35 min). Auto-builds call graph if never built. |
| `/setup-deploy` | Configures deployment settings for `/land-and-deploy`. |

## Context & State Skills

| Skill | What it does |
|---|---|
| `/context-save` | Captures git state, decisions, remaining work for cross-session resume. |
| `/context-restore` | Loads most recent saved context — picks up where you left off. |
| `/learn` | Manage project learnings — review, search, prune, export. |
| `/retro` | Weekly engineering retrospective — commit history, code quality, trends. |

## Safety Skills

| Skill | What it does |
|---|---|
| `/careful` | Warns before destructive commands (rm -rf, DROP TABLE, force-push). |
| `/freeze` | Restricts file edits to a specific directory for the session. |
| `/unfreeze` | Clears the freeze boundary. |
| `/guard` | Full safety: `/careful` + `/freeze` combined. |

## Browser & Web Skills

**Requires headless Chromium (Playwright) to actually launch.** If these
skills fail or hang, see `daily-ops.md`, "FIX: GSTACK BROWSER SKILLS
WON'T LAUNCH."

| Skill | What it does |
|---|---|
| `/browse` | Fast headless Chromium for QA — navigate, interact, screenshot, test. |
| `/open-gstack-browser` | Launch visible Chromium — watch agent actions in real time. |
| `/scrape` | Pull data from a web page. Returns JSON. |
| `/skillify` | Codify a `/scrape` flow into a permanent browser-skill (~200ms). |
| `/setup-browser-cookies` | Import cookies from real Chromium into headless session. |
| `/pair-agent` | Pair a remote AI agent with your browser. |
| `/canary` | Post-deploy monitoring — watches live app for errors and regressions. |

## iOS Skills

| Skill | What it does |
|---|---|
| `/ios-qa` | Live-device iOS QA — connects to real iPhone via USB, screenshots every screen. |
| `/ios-fix` | Autonomous iOS bug fixer — finds bug, writes fix, rebuilds, verifies on device. |
| `/ios-design-review` | Visual design audit for iOS apps on real hardware. |
| `/ios-sync` | Regenerates iOS debug bridge against latest gstack templates. |
| `/ios-clean` | Removes DebugBridge SPM package and #if DEBUG wiring. |

## Documentation Skills

| Skill | What it does |
|---|---|
| `/document-generate` | Generate missing docs from scratch. Diataxis framework. |
| `/document-release` | Post-ship doc update — cross-references diff, updates README/CHANGELOG. |
| `/make-pdf` | Turns markdown into publication-quality PDF. |

## Codex & Claude Skills

| Skill | What it does |
|---|---|
| `/codex` | OpenAI Codex CLI wrapper — Review, Challenge, Consult modes. |
| `/claude` | Claude Code CLI wrapper — Review, Challenge, Consult modes. |

## Other

| Skill | What it does |
|---|---|
| `/gstack-upgrade` | Upgrades gstack to latest version. Note: this one keeps its full prefixed name — confirmed present as `gstack-upgrade` in the linked-skills list. |

---

## Pipelines

**Planning pipeline** (new projects):
```
/office-hours → /plan-ceo-review → /plan-eng-review → /plan-design-review → /plan-devex-review → /plan-tune
```
Or run everything: `/autoplan`

**Build & ship pipeline** (after planning locked):
```
/review → /qa → /ship → /land-and-deploy
```

**Design pipeline** (new visual identity):
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

**Design workflow (confirm with user before running):**
```
/plan-design-review → /plan-eng-review → /design-html → /design-review
```
1. `/plan-design-review` — rate design dimensions 0-10, identify gaps, propose fixes
2. `/plan-eng-review` — lock in execution plan (architecture, data flow, edge cases, test coverage)
3. `/design-html` — generate production HTML/CSS from approved designs
4. `/design-review` — visual QA, find inconsistencies, fix with atomic commits
