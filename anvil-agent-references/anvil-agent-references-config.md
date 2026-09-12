---
document: "anvil-agent-references — Configuration"
doc-id: anvil-agent-references-config
state: Live
date-created: 2026-09-06
---

# anvil-agent-references — Configuration

Canonical current-state configuration record. Agent-facing. Reflects the
live-verified state as of 2026-09-06. This document states facts, not history —
where a decision was made and the reasoning matters, see
`anvil-agent-references-explainer.md`; for exact commands and per-skill
technical detail, see `anvil-agent-references-reference.md`.

---

## Identity

| Item | Value |
|---|---|
| Repository | `github.com/anvil-works/anvil-agent-references` (branch `master`) |
| Publisher | Anvil (anvil-works) — official Anvil-maintained repository |
| Nature | **Generated checkout** — produced from Anvil's main source repository by a GitHub Actions release workflow; "Do not edit these files directly" (upstream README). Read-only publish target, not hand-edited |
| Version field | None — version is the git HEAD sha plus the source-Anvil commit ref it was generated from |
| Installed HEAD | `3593c1639eec5b3a290509e0ab2f1f7f73e8cf13` — "Update agent references from anvil@aed6b9d5bc31" |
| Upstream HEAD at verification | `7c9b0a7a53a81f609fc6364cf70c0dc7fa1664b8` — 2026-09-03, generated from `anvil-works/anvil@23b5ed0d8547` |
| Drift status | **Clone behind upstream** — update pending (developer-run) |
| Upstream activity at verification | 48 commits; last upstream commit 2026-09-03 |
| License | **None found** — no LICENSE file in the clone, GitHub license API 404, no license badge on the repo page (see open items) |

## GBrain registration

| Item | Value |
|---|---|
| Source ID | `anvil-agent-references-code` |
| Registered | 2026-09-06, via host CLI `gbrain sources add` (MCP path registration is security-confined and refused) |
| Path | `/mnt/c/mybizz/anvil-agent-references` |
| Federated | `false` — only searched when explicitly named via `--source` (mirrors `mb-3-cs-code`, `mb4ecom-code`, `mb5pdlf-code`, `memory-governor-code`) |
| Index state at registration | 0 pages, never synced — content indexes on the next sync run |

## Install architecture

| Item | Value |
|---|---|
| Source clone (authoritative) | `/mnt/c/mybizz/anvil-agent-references` (Windows: `C:\mybizz\anvil-agent-references`) |
| Live install | `~/.agents/skills/` — five symbolic links, one per skill folder, into the clone's `skills/`. Nothing copied |
| Symlinks (created 2026-08-12) | `anvil-yaml`, `client-forms`, `client-modules`, `data-models`, `server-code` |
| OpenCode discovery | Confirmed working — all five skills appear in the OpenCode skill catalog (verified live 2026-09-06) |
| Duplicate discovery paths | None — no anvil entries in `~/.claude/skills/`; no project-local anvil skills |
| Shared root | `~/.agents/skills/` also hosts Matt Pocock's 35 skills (see `matt-pocock-skills-reference.md`) |

## Repository structure (live-verified 2026-09-06)

| Path | Contents |
|---|---|
| `AGENTS.md` | Template for an app project's own `AGENTS.md` — shared resources, validation, editing boundaries, skills list (5 resource roles) |
| `CLAUDE.md` | Same guidance for Claude Code-style agents; imports `AGENTS.md` via `@./AGENTS.md` |
| `README.md` | Install instructions (Codex plugin, Claude Code plugin, manual symlinks) |
| `skills/` | 5 skill folders — see Skills inventory |
| `stubs/` | 62 `.pyi` files — `stubs/client/` (31) and `stubs/server/` (31), covering **`anvil` and `stripe`** APIs |
| `reference/types/` | `anvil-yaml.d.ts`, `form-yaml.d.ts`, `index.d.ts` — generated `.d.ts` material for `anvil.yaml` and form templates |
| `docs/m3/` | Material 3 theme reference — `api.md` (generated API/attrs reference), `components/` (`_index.md`, `components.md`, `layouts.md`, `colour-schemes.md`, `img/`), `layouts.md` |
| `.codex-plugin/` | Codex plugin metadata (`plugin.json`) |
| `.claude-plugin/` | Claude Code plugin metadata (`plugin.json`) |

## Skills inventory (live line counts 2026-09-06)

| Skill | SKILL.md | One-line purpose |
|---|---|---|
| `anvil-yaml` | 62 lines | Update `anvil.yaml` — services, app metadata, `db_schema` |
| `client-forms` | 151 lines | Create/edit/style/validate/convert Anvil client Forms under `client_code/` |
| `client-modules` | 54 lines | Edit non-Form client-side Python modules under `client_code/` |
| `data-models` | 83 lines | Design Data Table model classes, buffering/drafts, Data Bindings, server methods |
| `server-code` | 73 lines | Edit server modules under `server_code/` — callables, background logic, server packages |

## Plugin metadata (verified from disk)

| Item | Codex (`.codex-plugin/plugin.json`) | Claude Code (`.claude-plugin/plugin.json`) |
|---|---|---|
| Plugin name | `anvil` | `anvil` |
| Version | `1.0.0` | `1.0.0` |
| Description | "Anvil app editing workflows and reference material for AI agents." | "Anvil app editing workflows and reference material for Claude Code." |
| Skills path | `./skills/` | — (plugin dir structure) |
| Author | — | Anvil |
| Invocation namespace | Bare skill name (per upstream docs) | `anvil:` prefix, e.g. `/anvil:server-code` (per upstream README) |

## Per-project setup status (live grep 2026-09-06, "Anvil Agent References" section in AGENTS.md)

| Project | Status |
|---|---|
| `makepdlf-project-library` | Done |
| `mb-3-cs-project-library` | Done |
| `mb-3-cs` (app root) | Not done |
| `mb4ecom` (app root) | Not done |
| `mb5pdlf` (app root) | Not done |

## Integration facts

| Item | Value |
|---|---|
| PDLF | Supplies platform-specific ground truth "underneath every single one of these steps" (`pdlf-system-explainer.md`); one of five skill families' supporting sources |
| Environment standards | Anvil.works working methods + Material 3 theme + M3 dependency + MUI overlay are prescribed standards (global AGENTS.md); this skill set is the agent-facing reference for them |
| Governing ADRs (project-library-global) | `anvil-extras-exclusion` (M3-only components), `htmltemplate-use` (HTMLTemplate banned), `material-3-theme-component-scope`, `anvil-platform-constraints` |
| Cupcake rules bearing on this component | `cup-block-anvil-yaml-writes.rego` (AI writes to `anvil.yaml`); `cup-protected_ai_governance_files_may_not_be_modified.rego` (AI writes to `AGENTS.md`/`CLAUDE.md`); `cup-no_cross_project_filesystem_access_by_default.rego` (AI writes outside the project root). Standing policy regardless; mechanically enforced only when Cupcake enforcement is active — status: `cupcake-config.md` Current Operational Status |
| Sibling corpus | `mybizz-config-docs/anvil-docs/` — separate vendor-docs mirror, adjacency only |

## Settled policies (developer decisions on record)

Cupcake-based statements in this suite describe standing policy and what
enforcement blocks when active — enforcement status is not fixed and is not
restated as current anywhere in this suite; check `cupcake-config.md`'s
Current Operational Status for the live state.

| Policy | Detail |
|---|---|
| Memory Governor bypass | Permanent — this source syncs into GBrain by ordinary `gbrain sync`, never through the governor's API. Vendor-published reference material: no genuine confidence/contradiction judgment to make (`memory-governor-config.md`). Keeping the source current is the developer's own responsibility. |
| Update command execution | `git pull` in the clone is developer-run only, never AI-invoked — the clone sits outside every project root; an AI-run write there is a cross-project write, which is the discipline Cupcake's cross-project-write rule enforces when active (status per the note above). |

## Known stale external references (state, 2026-09-06)

| Reference | Stale claim | Verified reality |
|---|---|---|
| Prior suite version | Config reference at `C:\mybizz\config\anvil-skills\` | `C:\mybizz\config\` does not exist; docs live in `C:\mybizz\mybizz-config-docs\anvil-agent-references\` |
| Prior suite version | Browsable symlink at `C:\mybizz\skills-collective\anvil-skills` | `C:\mybizz\skills-collective\` does not exist at all |
| Prior suite version | `docs/material-3/` | Actual path is `docs/m3/` with a different file layout |
| Older copy-verbatim block | 4 resource roles (stubs client/server, type references, docs) | Current `AGENTS.md` defines 5 roles — adds "Anvil skills: `skills/`" |

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Upstream update pending: clone at `3593c16`, upstream at `7c9b0a7` (2026-09-03). Developer-run `git pull`; re-verify this suite against the new HEAD afterwards. | Open |
| 2 | License: none found (no LICENSE file, GitHub API 404). Under `sec-dependency-skill-supply-chain`, three of four axes confirmed (publisher = platform vendor; maintenance active; no spawn capability); the license axis is formally unmet. No adoption-time review on record. | Open |
| 3 | Per-project setup not yet done in `mb-3-cs`, `mb4ecom`, `mb5pdlf` app roots. AI writes to `AGENTS.md` are prohibited as standing policy (Cupcake's AI-governance-file rule enforces this when active) — developer-run step either way. | Open |
| 4 | No confirmed run record of any of the five skills in this environment (no run logs found in GBrain). | Open |
| 5 | First `gbrain sync` of `anvil-agent-references-code` pending (registered 2026-09-06, 0 pages indexed). | Open |
