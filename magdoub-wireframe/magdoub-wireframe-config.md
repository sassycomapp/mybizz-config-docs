---
title: "magdoub-wireframe-config"
doc-id: "mb-3f021bf2"
---
# magdoub-wireframe — Configuration

Canonical current-state configuration record for the Magdoub Claude Wireframe
Skill as installed on this machine. Agent-facing. Reflects the live-verified
state as of 2026-09-06. This document states facts, not history — where a
decision was made and the reasoning matters, see
[[magdoub-wireframe-explainer|Explainer]]; for operational commands and rules, see
[[magdoub-wireframe-reference|Reference: Invocation, Operation, Update]].

---

## Identity

| Item | Value |
|---|---|
| Skill name (SKILL.md frontmatter) | `wireframe` |
| Component | Magdoub Claude Wireframe Skill — B&W UX wireframe generator with optional Clean/Polished color variants |
| Upstream repository | `github.com/Magdoub/claude-wireframe-skill` |
| Publisher | Magdoub (individual) |
| License | MIT |
| Version field | None in SKILL.md frontmatter — version is the git HEAD sha |
| Installed HEAD | `44a5814d1583c4dc7cafa36611838669f0895af9` — "Extract shared HTML/CSS into templates, clarify skill-bundled paths", 2026-03-01 |
| Upstream match | Local HEAD == upstream `main` HEAD — zero drift (verified 2026-09-06 via GitHub API) |
| Upstream activity at verification | 32 commits; 71 stars; 5 forks; last upstream commit 2026-03-01 |
| Invocation | `/wireframe <feature-description>` |

## Install architecture

| Item | Value |
|---|---|
| Real install (authoritative) | `~/.claude/skills/wireframe/` (WSL: `/home/dev-p/.claude/skills/wireframe/`) — genuine git clone, official install location |
| Git remote / branch | `https://github.com/Magdoub/claude-wireframe-skill.git` / `main` |
| Working tree at verification | Clean; local `main` == `origin/main` |
| OpenCode discovery path | `~/.config/opencode/skills/wireframe/SKILL.md` — single-file symlink into the real clone |
| Install pattern | Two-hop: OpenCode discovery folder → SKILL.md symlink → real clone in `~/.claude/skills/` (per [[opencode-explainer|OpenCode Explainer]]) |
| Clone as registered GBrain source | No — the clone is not registered |
| This doc suite's GBrain source | `mybizz-config-docs` (`/mnt/c/mybizz/mybizz-config-docs`, federated) |
| Destination of this doc suite | `C:\mybizz\mybizz-config-docs\magdoub-wireframe\` |

## Bundled files (live-counted 2026-09-06)

| File | Size / lines | Role |
|---|---|---|
| `SKILL.md` | 27,731 bytes / 404 lines | Full skill instructions — two personas, two phases |
| `wireframe/templates/base.css` | 244 lines | Framework CSS: layout, tabs, browser frame, annotations, banner, footer |
| `wireframe/templates/template.html` | 274 lines | HTML skeleton with placeholders |
| `wireframe/templates/self-reveal.css` | 9 lines | Badge-hiding rules appended by Phase 2 agents |
| `wireframe/brain/design-taste.md` | 116 lines | Craft principles, style tokens, quality checks, anti-patterns |
| `README.md` | — | Upstream install/update/uninstall docs |
| `LICENSE` | — | MIT |
| `examples/` | 3 PNGs | Annotated screenshots of skill output |

## Runtime output structure (per project, per run)

| Path | Contents |
|---|---|
| `wireframe/brain/design-context.md` | Persistent per-project design context (created on first run: codebase scan + user screenshots) |
| `wireframe/brain/design-taste.md` | Copied from the bundled template on first run |
| `wireframe/DDMM-<feature-name>/index.html` | Shared HTML + inline JS — 5 options, 3 sub-tabs each |
| `wireframe/DDMM-<feature-name>/styles.css` | B&W wireframe content CSS (≤ 300-line budget) |
| `wireframe/DDMM-<feature-name>/styles-opt1.css … opt5.css` | Per-option Clean + Polished variants (≤ 200 lines each) |

Folder naming is DDMM — day-then-month, zero-padded, per SKILL.md (see known stale references below).

## Integration facts

| Item | Value |
|---|---|
| PDLF registration | Step 22 — Phase 1, structural B&W wireframes; Step 26 — Phase 2 + gate `wireframes-approved` |
| PDLF skill-family role | "Magdoub owns visual iteration" — one of five skill families |
| [[skills-register|Skill Register]] status | `wireframe` — working (discoverability status, not run evidence) |
| Confirmed real runs in this environment | None found — no `wireframe/` output dirs in mb-3-cs, project-library, or makepdlf; no run logs in GBrain |
| Pre-existing single-file reference | `~/.config/opencode/skills/wireframe/magdoub-claude-wireframe-skill-reference.md` (2026-08-12), inside the OpenCode discovery folder; two of its claims now stale (below) |

## Settled policy — updates and syncing (developer decision, 2026-09-06)

| Rule | Detail |
|---|---|
| Content sync into GBrain | Ordinary `gbrain sync` — permanent bypass of Memory Governor's review pipeline. Same standing exception as `anvil-agent-references`: vendor-published material via a real git clone, not developer-authored content; no genuine confidence/contradiction judgment to make. |
| Update command execution | The update command (git fetch + `git reset --hard` inside the clone) is developer-run only, never AI-invoked — the clone sits outside every project root; an AI-run invocation is a cross-project write, the discipline Cupcake's cross-project-write rule enforces when active (enforcement status not fixed — see [[cupcake-config|Cupcake Configuration]]'s Current Operational Status). |

## Known stale external references (state, 2026-09-06)

| Reference | Stale claim | Verified reality |
|---|---|---|
| Upstream `README.md` | Output folder label `<MMDD-feature-name>` | SKILL.md (the executed instruction) specifies DDMM; the README's own example (`2302-signup-flow`) matches DDMM |
| `docmap` (dev-root-hub) | Config reference at `C:\mybizz\config\magdoub-wireframe\` | `C:\mybizz\config\` does not exist; docs live in `C:\mybizz\mybizz-config-docs\` |
| Old in-folder reference doc | Browsable symlink at `C:\mybizz\skills-collective\magdoub-claude-wireframe-skill` | No magdoub entry exists in `skills-collective\` |
| Old in-folder reference doc | Reference doc located at `C:\mybizz\config\magdoub-wireframe\` | That folder does not exist; the file sits inside the skill folder |

## Security supply-chain review (recorded 2026-09-16, gate-approved)

Discharged at run #1's gate (applied to this spec with explicit developer approval,
the established precedent). Axes per [[sec-review-before-trust|Review Before Trust]] /
[[sec-dependency-skill-supply-chain|Dependency and Skill Supply Chain]]:

| Axis | Finding | Verdict |
|---|---|---|
| Publisher | Magdoub — individual developer | Acceptable (single-maintainer vendor; same class as other community skills in the estate) |
| License | MIT (LICENSE file present in clone) | Clear |
| Maintenance | 71 stars / 5 forks / 32 commits; last upstream commit 2026-03-01 (dormant ~6 months at review) | Acceptable — dormant but stable; no drift pressure and no supply-pressure; deliberate-decision gate covers any future update |
| Spawn-capability | Skill instructions reference launching parallel Task agents (Phase 2); the executing environment denies the Task/spawn tool family natively | Benign in this environment — the instruction cannot execute here (open item 1); content itself is plain HTML/CSS generation |

Overall: benign on every axis. Recorded here with the review date; open item 3
closed.

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Phase 2 execution mechanism: SKILL.md instructs launching 5 parallel foreground Task agents; sub-agent creation is prohibited as standing policy in this environment, enforced when active at three independent layers (native OpenCode config deny — tool removed from the visible set; `cup-block-task-tool.rego` checked against `spawn-tools-denylist.json`; standing skill-review habit). As of research (2026-09-06) the `task` tool was absent from the tool set. How Phase 2 actually executes here is unresolved. | Open — deferred 2026-09-16 to a deliberate session (gate decision); candidates recorded: main-agent sequential fallback (loses parallelism, keeps output contract) vs Phase-1-only in this environment |
| 2 | No confirmed real run of the skill anywhere in this environment. | Open (recorded state, confirmed run #1) |
| 3 | ~~No record of a security supply-chain review at adoption (2026-07-02)~~ — **reviewed and recorded 2026-09-16** (see Security supply-chain review above); benign on all axes | **Closed** |
| 4 | ~~[[adr-design-rules|Wireframe Design Rules]] ADR (project-library-global; binding on every agent creating wireframe HTML documents; mandates a three-section instructive structure and pre-wireframe reading) vs. the skill's own fixed output format — reconciliation undocumented~~ — **reconciled 2026-09-16 by developer decision, applied to the ADR:** [[adr-design-rules|Wireframe Design Rules]] gained Section A — the ADR applies only to wireframes NOT created by the Magdoub skill (exploratory comparison artifact = different genre, exempt); wireframes by any other skill or by hand are fully governed; Magdoub output is not an escape hatch for ADR-conforming deliverables (A3) | **Closed** |
| 5 | Whether the old in-folder single-file reference doc is retired or retained now that this suite exists. | Open — **retained for now** (gate decision 2026-09-16); sits alongside a 25 B Zone.Identifier artifact; retirement to ride with future suite maintenance |
