---
document: "Matt Pocock Skills Configuration"
doc-id: matt-pocock-skills-config
state: Live
date-created: 2026-09-08
---

# Matt Pocock Skills Configuration

Canonical current-state configuration record. Agent-facing. States facts,
not history or rules — commands and rules in
[[matt-pocock-skills-reference|Matt Pocock Skills Reference]], reasoning in
[[matt-pocock-skills-explainer|Matt Pocock Skills Explainer]]. All values verified live 2026-09-08
unless noted.

## Identity

| Item | Value |
|---|---|
| Tool | "Skills For Real Engineers" — Matt Pocock's personal AI-agent skill set |
| Source clone (authoritative) | `/mnt/c/mybizz/matt-pocock-skills-source` (`C:\mybizz\matt-pocock-skills-source`), git HEAD `84fdeff` (2026-08-06, PR #788 "grill-me-align") |
| Upstream repository | `github.com/mattpocock/skills` (MIT) |
| Upstream HEAD | `3cca18b` (2026-09-04, PR #1025 "stop linking misc/ into local skill directories") — clone is ~1 month behind |
| Upgrade policy | **No upgrade required — updates/upgrades by deliberate decision only** (developer-stated standing rule, 2026-09-08) |
| Install method | Manual pinned clone + symlinks — not the vendor's plugin/`npx skills` paths |

## Install topology

| Element | State |
|---|---|
| Live install root | `~/.agents/skills/` — an OpenCode discovery root |
| Mechanism | 35 matt-pocock skill symlinks → source clone's `skills/<category>/<name>/` (created 2026-08-12); nothing copied |
| Shared root | Same directory hosts 5 Anvil skills (`anvil-yaml`, `client-forms`, `client-modules`, `data-models`, `server-code` → `anvil-agent-references/skills/`) — pointer: [[anvil-agent-references-config|Configuration]] |
| Broken links | 0 (verified 2026-09-08) |
| GStack relationship | None — GStack installs to its own discovery path; no shared entries |
| Stale artifact | `matt-pocock-skills-reference.md:Zone.Identifier` (25 B) sits in `~/.agents/skills/` — inert Windows-Zone remnant; cleanup optional, no action taken |

## Skill inventory (35 = 18 + 7 + 6 + 4)

| Category | Count | Skills |
|---|---|---|
| Engineering | 18 | ask-matt, code-review, codebase-design, diagnosing-bugs, domain-modeling, grill-with-docs, implement, improve-codebase-architecture, prototype, research, resolving-merge-conflicts, setup-matt-pocock-skills, tdd, to-spec, to-tickets, triage, wayfinder, wizard |
| Productivity | 7 | grill-me, grilling, handoff, teach, to-questionnaire, wait-what, writing-for-agents |
| In-progress | 6 | claude-handoff, loop-me, setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape |
| Misc | 4 | git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit |
| Deprecated | 0 | (folder contains README only) |

## Per-project setup state (`/setup-matt-pocock-skills` gate)

| Project | Configured (4 `agents/` files present) |
|---|---|
| `makepdlf-project-library` | Yes |
| `mb-3-cs-project-library` | No |
| `mb-3-cs` | No |
| `mb4ecom` | No |
| `mb5pdlf-project-library` | No |

## Supersession

| Item | State |
|---|---|
| Prior document | [[matt-pocock-skills-reference|Matt Pocock Skills Reference]] — **removed**; its verified content is merged into this suite (developer decision, 2026-09-08) |
| Stale claims retired with it | `C:\mybizz\skills-collective\matt-pocock-skills` browsable-hub path (does not exist); pre-drift state |

## Open items

- Zone.Identifier artifact cleanup — optional, no action taken.
- Upstream's newest change (stop linking `misc/`) noted for any future deliberate upgrade decision — under the standing rule, no upgrade is planned.
