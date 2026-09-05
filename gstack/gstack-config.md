# GStack Configuration

Canonical current-state configuration record. Agent-facing. States facts,
not history — see `daily-ops.md` for common fixes, and the real skill
files themselves for full, authoritative detail on any individual skill.
Supersedes and retires the separate `gstack-skills-reference.md` — its
real, verified content is merged in below.

---

## Identity

| Item | Value |
|---|---|
| Version | `1.58.1.0` |
| Real install location | `C:\mybizz\gstack` (`/mnt/c/mybizz/gstack`) |
| OpenCode discovery path | `~/.config/opencode/skills/gstack-*` (individual skills) and `~/.config/opencode/skills/gstack/` (aggregate entry) |
| Install method | Linux symlinks from the discovery path into the real install folder |
| Install/refresh command | `cd /mnt/c/mybizz/gstack && ./setup --host opencode` |
| `SKILL.md` generation | **Auto-generated from `SKILL.md.tmpl` — never hand-edit directly.** Regenerate via `bun run gen:skill-docs`. |
| Upgrade | `/gstack-upgrade` — the one confirmed exception to the invocation rule below; keeps its full prefixed name |

## Real config files (confirmed present)

| File | Purpose |
|---|---|
| `.env.example` | Template for environment variables — not itself live configuration |
| `slop-scan.config.json` | Real, live config file — contents not yet reviewed in detail |

## Invocation — the folder name is NOT the command

**Critical, easily-missed rule: each skill's `SKILL.md` frontmatter declares
a `name:` field, and that field — not the folder name — is what OpenCode
registers as the real slash command.** In current practice this `name:`
field is the bare skill name, with the `gstack-` prefix dropped. Example:
the folder is `gstack-qa/`, its real command is **`/qa`**, not `/gstack-qa`
— confirmed directly, `/gstack-qa` returns nothing.

**The one confirmed exception: `/gstack-upgrade` keeps its full prefixed
name.** Every other skill in this document is listed by its real,
bare invocation — drop the `gstack-` prefix shown in the folder-name
column of the raw skill list.

## Skill inventory — 54 real skills confirmed (definitive count, 2026-09-01)

Confirmed via direct install-script output (`./setup --host opencode`),
cross-checked against a real `ls` of the discovery path — both agree at
54 (53 individually-named skills plus the bare `gstack` aggregate entry).

### Planning

| Command | What it does |
|---|---|
| `/office-hours` | YC Office Hours — six forcing questions for product ideas. Produces a design doc. |
| `/plan-ceo-review` | CEO/founder-mode plan review. Four modes: scope expansion, selective, hold, reduce. |
| `/plan-eng-review` | Eng manager review — locks in architecture, data flow, edge cases, test coverage. |
| `/plan-design-review` | Designer's-eye review — rates design dimensions 0–10, fixes the plan. |
| `/plan-devex-review` | Developer experience review — personas, benchmarks, friction points. |
| `/plan-tune` | Self-tuning question sensitivity — set per-question preferences. |
| `/autoplan` | Auto-review pipeline — runs CEO, design, eng, DX reviews sequentially. |
| `/spec` | Turns vague intent into a precise, executable spec. Files as a GitHub issue. |

### Build & Ship

| Command | What it does |
|---|---|
| `/review` | Pre-landing PR review — SQL safety, LLM trust-boundary violations, conditional side effects. |
| `/ship` | Detect + merge base, run tests, bump VERSION, update CHANGELOG, create PR. |
| `/land-and-deploy` | Merges PR, waits for CI, verifies production health via canary. |
| `/landing-report` | Read-only queue dashboard — claimed VERSION slots and open PRs. |

### Design

| Command | What it does |
|---|---|
| `/design-consultation` | Creates `DESIGN.md` — researches landscape, proposes full design system. |
| `/design-shotgun` | Generates multiple AI design variants, opens a comparison board. |
| `/design-html` | Generates production-quality HTML/CSS. |
| `/design-review` | Designer's-eye QA — finds visual issues, fixes with atomic commits. |
| `/diagram` | English description → Mermaid + editable `.excalidraw` + SVG/PNG. |

### QA & Testing

| Command | What it does |
|---|---|
| `/qa` | Systematically QA-tests a web app and fixes bugs found, committing each fix atomically. Three tiers: Quick, Standard, Exhaustive. |
| `/qa-only` | Report-only QA — structured bug report, no fixing. |
| `/benchmark` | Performance regression detection — Core Web Vitals, bundle sizes. |
| `/benchmark-models` | Cross-model benchmark — latency, tokens, cost, quality. |

### Investigation & Debugging

| Command | What it does |
|---|---|
| `/investigate` | Systematic debugging with root cause. Four phases: investigate, analyze, hypothesize, implement. |
| `/health` | Code quality dashboard — type checker, linter, tests, dead code, composite 0–10 score. |
| `/cso` | Chief Security Officer audit — secrets, dependency supply chain, CI/CD, LLM/AI security, OWASP, STRIDE. Daily (near-zero-noise) and monthly (comprehensive) modes. |

### GBrain

| Command | What it does |
|---|---|
| `/setup-gbrain` | Installs and configures GBrain. **Caveat: its own description mentions "PGLite or Supabase" — not accurate for this project, which runs real, self-hosted PostgreSQL. Check `gbrain-config.md` for actual current setup.** |
| `/sync-gbrain` | Keeps GBrain current with a repo's code, refreshes agent search guidance. Flags: `--dream`, `--full`, `--code-only`, `--dry-run`. Re-runnable, idempotent. |
| `/setup-deploy` | Configures deployment settings for `/land-and-deploy`. |

### Context & State

| Command | What it does |
|---|---|
| `/context-save` | Captures git state, decisions, remaining work for cross-session resume. |
| `/context-restore` | Loads the most recent saved context. |
| `/learn` | Manage project learnings — review, search, prune, export. |
| `/retro` | Weekly engineering retrospective — commit history, code quality, trends. |

### Safety

| Command | What it does |
|---|---|
| `/careful` | Warns before destructive commands (`rm -rf`, `DROP TABLE`, force-push). |
| `/freeze` | Restricts file edits to a specific directory for the session. |
| `/unfreeze` | Clears the freeze boundary. |
| `/guard` | `/careful` + `/freeze` combined. |

### Browser & Web

**Requires headless Chromium (Playwright) to actually launch** — see
`daily-ops.md`, "FIX: GSTACK BROWSER SKILLS WON'T LAUNCH."

| Command | What it does |
|---|---|
| `/browse` | Fast headless Chromium for QA — navigate, interact, screenshot, test. |
| `/open-gstack-browser` | Launch visible Chromium — watch agent actions in real time. |
| `/scrape` | Pull data from a web page. Returns JSON. |
| `/skillify` | Codify a `/scrape` flow into a permanent browser-skill. |
| `/setup-browser-cookies` | Import cookies from real Chromium into the headless session. |
| `/pair-agent` | Pair a remote AI agent with your browser. |
| `/canary` | Post-deploy monitoring — watches the live app for errors and regressions. |

### iOS

| Command | What it does |
|---|---|
| `/ios-qa` | Live-device iOS QA — connects to a real iPhone via USB, screenshots every screen. |
| `/ios-fix` | Autonomous iOS bug fixer — finds bug, writes fix, rebuilds, verifies on device. |
| `/ios-design-review` | Visual design audit for iOS apps on real hardware. |
| `/ios-sync` | Regenerates the iOS debug bridge against latest gstack templates. |
| `/ios-clean` | Removes the DebugBridge SPM package and `#if DEBUG` wiring. |

### Documentation

| Command | What it does |
|---|---|
| `/document-generate` | Generates missing docs from scratch (Diataxis framework). |
| `/document-release` | Post-ship doc update — cross-references diff, updates README/CHANGELOG. |
| `/make-pdf` | Turns markdown into a publication-quality PDF. |

### CLI Wrappers

| Command | What it does |
|---|---|
| `/codex` | OpenAI Codex CLI wrapper — Review, Challenge, Consult modes. |
| `/claude` | Claude Code CLI wrapper — Review, Challenge, Consult modes. |

### Not yet documented

| Command | Status |
|---|---|
| `/devex-review` | Real folder confirmed present (`gstack-devex-review`), no verified description available — appears to have been added since the last skill-reference pass. Do not assume its behavior; check the real `SKILL.md` directly before relying on it. |

### Confirmed NOT real commands — do not assume these exist

- **`/handoff`** — no corresponding folder found anywhere in the source repo.
- **`hackernews-frontpage`** — exists only as a sub-skill under
  `/mnt/c/mybizz/gstack/browser-skills/hackernews-frontpage/`, not as a
  standalone, top-level `gstack-*` command. Not confirmed wired as an
  invocable skill at all.

## Real pipelines (confirmed sequences)

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

## Known scope limitations

- **OpenClaw-specific skill folders exist but are not in use** — `gstack-openclaw-ceo-review`, `gstack-openclaw-investigate`, `gstack-openclaw-office-hours`, `gstack-openclaw-retro`. Installed via a different mechanism (`clawhub install`), not part of this catalog. Confirmed: OpenClaw itself is not used in this environment. Deliberately not removed — any future GStack update would simply recreate them.
- **`/devex-review`'s real behavior is unverified** — see the table above.

## Do not

- Do not hand-edit any `SKILL.md` file directly — auto-generated from
  `SKILL.md.tmpl`; edit the template and regenerate.
- Do not assume the folder name is the real command — drop the
  `gstack-` prefix for every skill except `/gstack-upgrade`.
- Do not assume `/handoff` exists, or that `hackernews-frontpage` is a
  standalone command — both confirmed not real, top-level skills.
- Do not trust `/setup-gbrain`'s own description of GBrain's backend —
  check `gbrain-config.md` instead.
- Do not remove the unused OpenClaw skill folders — any GStack update
  will simply recreate them.
