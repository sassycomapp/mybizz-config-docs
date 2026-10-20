---
title: "gstack-reference"
doc-id: "mb-c02446bd"
updated: "2026-10-20"
---
# GStack Reference

Execution reference for GStack. State and values:
[[[mybizz-config-docs:gstack/gstack-config|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md). What GStack is and why:
[[[mybizz-config-docs:gstack/gstack-explainer|GStack Explainer]]](C:/mybizz/mybizz-config-docs/gstack/gstack-explainer.md). Differences from the standard:
[[[mybizz-config-docs:gstack/gstack-learnings|GStack Learnings]]](C:/mybizz/mybizz-config-docs/gstack/gstack-learnings.md). Which skills are installed, and why
the others are not: [[[mybizz-os-docs:os-reference-docs/skills-catalog|Skills Catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md).

## Authority model

1. User decision in the current session
2. Authoritative repo files and ADRs
3. OpenCode rules (global + project AGENTS.md, opencode.json)
4. GStack workflow conventions
5. GBrain advisory memory

When GStack workflow expectations conflict with OpenCode config, project
rules, or user instruction — the stricter layer wins.

## Invoking skills

- The slash command is the skill's frontmatter `name:` field. OpenCode loads
  a skill only when its `name:` matches the folder containing it: the tree
  folder is `gstack-qa/`, the shortcut is `qa`, the command is `/qa`.
- Type bare names. The one prefixed command is `/gstack-upgrade`; the
  aggregate router entry is `/gstack`.
- `skill_prefix` is false; gstack's setup, upgrade and relink tools read
  that setting and create plain shortcuts only.
- Resolve gstack tooling through `$GSTACK_BIN`
  (`~/.config/opencode/skills/gstack/bin`). The generated preambles default
  to OpenClaw and Claude host roots that do not resolve on this host — never
  rely on those defaults.
- A known skill missing, broken or outdated in OpenCode: re-run
  `cd /mnt/c/mybizz/gstack && ./setup --host opencode`. If it still fails:
  `C:\mybizz\mybizz-os-docs\operating-procedures\daily-ops.md`, "FIX: GSTACK
  SKILLS MISSING, OUTDATED, OR ONLY PARTIALLY WORKING IN OPENCODE".
- GStack is exposed through skills, not a separate CLI; no `.opencode/gstack`
  config exists.

## Command catalog

### Planning

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

### Build and ship

| Command | What it does |
|---|---|
| `/review` | Pre-landing PR review — SQL safety, LLM trust-boundary violations, conditional side effects. |
| `/ship` | Detect + merge base, run tests, bump VERSION, update CHANGELOG, create PR. |
| `/land-and-deploy` | Merges PR, waits for CI, verifies production health via canary. |
| `/landing-report` | Read-only queue dashboard — claimed VERSION slots and open PRs. |
| `/gstack-upgrade` | Upgrades the installed GStack — rebase the MyBizz-local commits first ([[[mybizz-config-docs:gstack/gstack-learnings\|Learnings L1]]](C:/mybizz/mybizz-config-docs/gstack/gstack-learnings.md)). |

### Design

| Command | What it does |
|---|---|
| `/design-consultation` | Creates DESIGN.md — researches the landscape, proposes a full design system. |
| `/design-shotgun` | Generates multiple AI design variants, opens a comparison board. |
| `/design-html` | Generates production-quality HTML/CSS. |
| `/design-review` | Designer's-eye QA — finds visual issues, fixes with atomic commits. |
| `/diagram` | English description → Mermaid + editable `.excalidraw` + SVG/PNG. |

### QA and testing

| Command | What it does |
|---|---|
| `/qa` | Systematically QA-tests a web app and fixes bugs found, committing each fix atomically. Three tiers: Quick, Standard, Exhaustive. |
| `/qa-only` | Report-only QA — structured bug report, no fixing. |
| `/benchmark` | Performance regression detection — Core Web Vitals, bundle sizes. |
| `/benchmark-models` | Cross-model benchmark — latency, tokens, cost, quality. |

### Investigation and debugging

| Command | What it does |
|---|---|
| `/investigate` | Systematic debugging with root cause. Four phases: investigate, analyze, hypothesize, implement. |
| `/health` | Code quality dashboard — type checker, linter, tests, dead code, composite 0–10 score. |
| `/cso` | Chief Security Officer audit — secrets, dependency supply chain, CI/CD, LLM/AI security, OWASP, STRIDE. Daily (near-zero-noise) and monthly (comprehensive) modes. |

### Live audit

| Command | What it does |
|---|---|
| `/devex-review` | Live developer experience audit — navigates docs, times time-to-hello-world, screenshots errors; compares against `/plan-devex-review` scores. |

### GBrain

| Command | What it does |
|---|---|
| `/setup-gbrain` | Installs and configures GBrain. Do not trust its own backend description — this environment runs self-hosted PostgreSQL; [[[mybizz-config-docs:gbrain/gbrain-config\|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) is authoritative. |
| `/sync-gbrain` | Keeps GBrain current with a repo's code, refreshes agent search guidance. Flags: `--dream`, `--full`, `--code-only`, `--dry-run`. Idempotent. `--dream` has a source-overlap trap against manually-registered sources — read [[[mybizz-config-docs:gbrain/gbrain-reference\|GBrain Reference]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) before using it. |
| `/setup-deploy` | Configures deployment settings for `/land-and-deploy`. |

### Context and state

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

### Browser and web

Browser skills run on GStack's bundled headless Chromium (Playwright). If
they fail or hang: `C:\mybizz\mybizz-os-docs\operating-procedures\daily-ops.md`,
"FIX: GSTACK BROWSER SKILLS WON'T LAUNCH".

| Command | What it does |
|---|---|
| `/browse` | Fast headless Chromium for QA — navigate, interact, screenshot, test. |
| `/open-gstack-browser` | Launch visible Chromium — watch agent actions in real time. |
| `/scrape` | Pull data from a web page. Returns JSON. |
| `/skillify` | Codify a `/scrape` flow into a permanent browser-skill. |
| `/setup-browser-cookies` | Import cookies from the real Chromium into the headless session. |
| `/pair-agent` | Pair a remote AI agent with this browser. |
| `/canary` | Post-deploy monitoring — watches the live app for errors and regressions. |

### Documentation

| Command | What it does |
|---|---|
| `/document-generate` | Generates missing docs from scratch (Diataxis framework). |
| `/document-release` | Post-ship doc update — cross-references diff, updates README/CHANGELOG. |
| `/make-pdf` | Turns markdown into a publication-quality PDF. |

### Aggregate

| Command | What it does |
|---|---|
| `/gstack` | Router entry (frontmatter `name: gstack`) — orients the agent over the whole skill set. |

## Not real commands

- `/handoff` — no corresponding folder anywhere in the source repo.
- `hackernews-frontpage` — a sub-skill under
  `/mnt/c/mybizz/gstack/browser-skills/hackernews-frontpage/`; no discovery
  shortcut; not a standalone command.

## Pipelines

Planning (new projects):

```
/office-hours → /plan-ceo-review → /plan-eng-review → /plan-design-review → /plan-devex-review → /plan-tune
```

Or run everything at once: `/autoplan`

Build and ship (after planning is locked):

```
/review → /qa → /ship → /land-and-deploy
```

Design (new visual identity):

```
/design-consultation → /design-shotgun → /design-html → /design-review
```

Daily workflow:

```
/context-restore → work → /context-save
```

Investigation:

```
/investigate → /review → /qa → /ship
```

## Workflows

Three core workflow families, named against whichever project is currently
active (see [[[mybizz-config-docs:opencode/opencode-reference|Commands, Verification, Troubleshooting]]](C:/mybizz/mybizz-config-docs/opencode/opencode-reference.md),
Active Project Standard).

### docs-plan (active project's `-project-library` repo)

**Use when:** analysis, validation, architecture, planning, ADR work, prompt
authoring.
**Agent:** plan (primary)
**Skills:** `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`,
`/plan-design-review`

**Mandatory initial steps:**
1. Consult [[[pdlf:pdlf-library/docs-local/pdlf-todo|Active PDLF To-Do List]]](C:/pdlf/pdlf-library/docs-local/pdlf-todo.md) — incorporate relevant
   items, mark completed as `[DONE]`
2. Consult the ADR folder — treat as authoritative, create new ADRs for new
   decisions

**Exit condition:** planning objective complete, OR build-ready handoff
prepared, OR canonical tracking updated.

### code-plan-build (code repos)

**Use when:** implementation, refactoring, migration, code validation, file
edits.
**Agent:** build (primary), plan for complex/risky work
**Skills:** `/investigate`, `/review`, `/qa`, `/ship`

**Mandatory initial steps:**
1. Confirm the repo path
2. Consult [[[pdlf:pdlf-library/docs-local/pdlf-todo|Active PDLF To-Do List]]](C:/pdlf/pdlf-library/docs-local/pdlf-todo.md) for relevant items
3. Consult ADRs for the architectural baseline

**Mandatory checks before edits:** repo path confirmed, protected files
checked, backup rule applied, timestamp rule applied, write scope checked.

**Exit condition:** implementation complete, validation recorded, tracking
requirements handed off.

### status-handover (cross-workspace)

**Use when:** session close, checkpoint, handover for continuation.
**Agent:** plan (primary)
**Skills:** `/context-save`, `/context-restore`

**Exit condition:** current state captured clearly enough for a fresh
session to resume without reconstructing context.

## Handoff contract

Work that changes ownership (Plan↔Build, docs↔code, session↔session) must
produce a structured handoff.

### Plan→Build template

```
Task summary:
Scope in:
Scope out:
Files read:
Relevant ADRs:
Files expected to change:
Files that must not change:
Key constraints:
Implementation steps:
Validation required:
Tracking handoff required (devlog / todo / ADR):
```

### Build→Plan template

```
Completion status:
Files changed:
Backup confirmation:
Protected-file confirmation:
Validation result:
Implementation summary:
Proposed devlog handoff:
Proposed todo handoff:
Proposed ADR updates:
```

### Quality bar

A handoff is acceptable only if: short and specific, file paths explicit,
scope boundaries clear, ADRs and tracking expectations visible, unresolved
risks listed, sufficient for a new session to continue without
reconstructing context.

## Role map

| Workspace | Default agent | Workflow family | Primary responsibility |
|---|---|---|---|
| Active project's `-project-library` repo | plan | docs-plan | ADRs, specs, planning, devlog/todo |
| code repos | build | code-plan-build | Implementation, refactors, validation |
| cross-workspace | plan | status-handover | Session close, checkpoints, handoffs |

The developer chooses the workspace, decides risk thresholds, and accepts or
rejects plans and handoffs. Agents propose plans and handoffs, keep
devlog/todo/ADRs in sync, and respect permissions.

## SKILL.md generation

- Every skill's `SKILL.md` is generated — never hand-edit a generated file.
- Sources are the top-level `<skill>/SKILL.md(.tmpl)` files; the per-host
  trees under the clone are generated output and are gitignored.
- Build the OpenCode tree with:

```bash
cd /mnt/c/mybizz/gstack && bun run scripts/gen-skill-docs.ts --host opencode --respect-detection
```

- Rebuild after any change to skill sources. The loaded tree reflects the
  sources only once rebuilt — the MyBizz Brain Context Load sections are
  live in 10 loaded skills because the tree is built from the local sources.

## Artifact locations

- Every GStack skill saves its output under `~/.gstack/projects/$SLUG/`,
  where `$SLUG` is the deterministic per-repo project slug produced by
  `$GSTACK_BIN/gstack-slug` (this repo: `sassycomapp-mybizz-config-docs`).
  That directory is the single machine-wide home for GStack artifacts.
- The `gstack-outputs/` copy lane named in project AGENTS.md files is a
  convention only — it does not exist on this system. Never rely on a
  repo-side copy; find prior output only under `~/.gstack/projects/$SLUG/`.

Sub-directory layout inside `~/.gstack/projects/$SLUG/` (skills not listed
use the bare root):

| Skill | Save location |
|---|---|
| `/office-hours`, `/plan-eng-review`, `/plan-design-review`, `/plan-devex-review` | `~/.gstack/projects/$SLUG/` |
| `/plan-ceo-review` | `~/.gstack/projects/$SLUG/ceo-plans/` |
| `/design-consultation` | `~/.gstack/projects/$SLUG/designs/` |
| `/retro` | `~/.gstack/projects/$SLUG/retros/` |
| `/context-save` | `~/.gstack/projects/$SLUG/.context/` |
| `/qa`, `/qa-only` | `~/.gstack/projects/$SLUG/qa-reports/` |
| `/health` | `~/.gstack/projects/$SLUG/health/` |
| `/cso` | `~/.gstack/projects/$SLUG/security-audits/` |
| `/spec` | `~/.gstack/projects/$SLUG/specs/` |

How a later skill finds prior output:

1. Compute the same slug: `eval "$($GSTACK_BIN/gstack-slug)"` → `$SLUG`
   (deterministic per repo — a later skill in the same project resolves to
   the same directory).
2. Read the skill's sub-directory from the table above.
3. Cross-session handoff: `/context-save` writes `.context/`;
   `/context-restore` reads it — the standing handoff pair for a fresh
   session to resume without reconstructing context.
4. Learnings compound across sessions in
   `~/.gstack/projects/$SLUG/learnings.jsonl` (loaded by every skill
   preamble once it exists).
5. `timeline.jsonl`, `decisions.active.json` and `~/.gstack/analytics/` are
   project-keyed under `~/.gstack/projects/$SLUG/` and appear on first use.

Open GStack folders in Windows Explorer (always via `wslpath -w` from WSL —
a raw Linux path opens the wrong location):

```bash
explorer.exe "$(wslpath -w /home/dev-p/.gstack/)"
explorer.exe "$(wslpath -w /home/dev-p/.gstack/projects/)"
```

## Brain sync

Pushes learnings, plans and retros into the git-backed worktree. No remote
is configured — sync is local-only
([[[mybizz-config-docs:gstack/gstack-config|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md), Brain remote).

| Command | Description |
|---|---|
| `bash /mnt/c/mybizz/gstack/bin/gstack-brain-sync --once` | Sync pending changes |
| `bash /mnt/c/mybizz/gstack/bin/gstack-brain-sync --status` | Check sync health |
| `/mnt/c/mybizz/gstack/bin/gstack-gbrain-detect` | GBrain + GStack status JSON — bun script; run it directly, never through `bash` |

## Detection snapshot

`~/.gstack/gbrain-detection.json` is a point-in-time snapshot. Never read
it as the live GBrain version — refresh it by re-running
`/mnt/c/mybizz/gstack/bin/gstack-gbrain-detect`, then compare with
`gbrain --version`.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| GStack repository | https://github.com/garrytan/gstack | 1.58.1.0 | 2026-10-20 |
| Brain-sync documentation | `/mnt/c/mybizz/gstack/docs/gbrain-sync.md` | 1.58.1.0 | 2026-10-20 |
| Configuration template | `/mnt/c/mybizz/gstack/config.yaml` | 1.58.1.0 | 2026-10-20 |
| Skill-doc generator | `/mnt/c/mybizz/gstack/scripts/gen-skill-docs.ts` | 1.58.1.0 | 2026-10-20 |
| GBrain integration guide | `/mnt/c/mybizz/gstack/USING_GBRAIN_WITH_GSTACK.md` | 1.58.1.0 | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `cat /mnt/c/mybizz/gstack/VERSION` — package.json agrees | agent |
| Local commits | `git -C /mnt/c/mybizz/gstack log --oneline -3`; `git -C /mnt/c/mybizz/gstack branch -v` — expect `main` ahead 2 on the MyBizz commits | agent |
| Topology | `ls /mnt/c/mybizz/gstack/.opencode/skills \| wc -l` → 54; `readlink -f ~/.config/opencode/skills/gstack/bin` resolves into the clone | agent |
| Loaded-tree currency | `grep -rl 'Brain Context Load' /mnt/c/mybizz/gstack/.opencode/skills/ \| wc -l` → 10 | agent |
| Runtime settings | read `~/.gstack/config.yaml` against [[[mybizz-config-docs:gstack/gstack-config\|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md) | agent |
| Repo policy | read `~/.gstack/gbrain-repo-policy.json` — 8 repositories, all `read-write` | agent |
| Detection snapshot | `/mnt/c/mybizz/gstack/bin/gstack-gbrain-detect` — bun shebang; rewrites `~/.gstack/gbrain-detection.json`; verify status `ok` and the GBrain version against `gbrain --version` | developer |
| Works | `bash /mnt/c/mybizz/gstack/bin/gstack-brain-sync --status`; then a real skill invocation | developer |

## Do not

- Do not hand-edit any `SKILL.md` — regenerate (SKILL.md generation, above).
- Do not delete `~/.config/opencode/skills/gstack/bin` — actively managed,
  not leftover.
- Do not assume the folder name is the command (Invoking skills, above).
- Do not run `/sync-gbrain --dream` against a manually-registered GBrain
  source — source-overlap trap; full account in
  [[[mybizz-config-docs:gbrain/gbrain-reference|GBrain Reference]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md).
- Do not trust `/setup-gbrain`'s own GBrain backend description —
  [[[mybizz-config-docs:gbrain/gbrain-config|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) is authoritative.
- Do not remove the clone's `openclaw/` skill folders — updates recreate
  them; removal is churn, not a fix.
- Do not `bash` the bun script `gstack-gbrain-detect` — follow the shebang.
- Do not read `~/.gstack/gbrain-detection.json` as the live GBrain version —
  point-in-time snapshot (Detection snapshot, above).
- Do not assume `/handoff` exists or that `hackernews-frontpage` is a
  standalone command.
- Do not type the `gstack-` prefix — bare names, except `/gstack-upgrade`
  and `/gstack`.
