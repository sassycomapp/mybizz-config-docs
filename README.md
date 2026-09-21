---
document: "mybizz-config-docs — README"
doc-id: README
state: Live
date-created: 2026-09-05
---

# mybizz-config-docs — README

Tool-by-tool configuration reference documents — one folder per tool, each holding a single,
purely functional reference: what's installed, where, how it's configured, and how to verify
it's working. Not historical narrative, not task-completion reports — this suite is
steady-state functional reference only.

## Structure

| Folder | Reference document |
|---|---|
| `opencode/` | [[opencode-reference|Commands, Verification, Troubleshooting]] |
| `gstack/` | [[gstack-reference|GStack Reference]], [[gstack-skills-reference|GStack Skills Reference]] |
| `gbrain/` | [[gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]] |
| `postgresql/` | [[postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]] |
| `matt-pocock-skills/` | [[matt-pocock-skills-reference|Matt Pocock Skills Reference]] |
| `anvil-agent-references/` | [[anvil-agent-references-reference|Reference: Install, Skills, and Technical Detail]] |
| `magdoub-wireframe/` | [[magdoub-wireframe-reference|Reference: Invocation, Operation, Update]] |
| `graphify/` | [[graphify-reference|Graphify Reference]] |

Plus, directly in this folder: `projects-config-register.md` — the register of every
project's `{slug}-config.yaml` (see below).

**Not here, despite an earlier plan to place it here:** individual projects' `{slug}-config.yaml`
files live inside each project's own root folder (`C:\pdlf\pdlf-config.yaml`,
`C:\dev\dev-mb-3-cs\mb-3-cs-config.yaml`, etc.), not centralized under a `config/projects/`
subfolder — a config file's natural home is inside the thing it configures. `docmap.md`'s
reference to `config/projects/` is stale and should be corrected.

## The governing principle behind all of this

**One fact, one home, everywhere else references it rather than restating it.** This folder,
and the work it documents, exists specifically to eliminate the drift problem that comes from
the same configuration fact being written down in two or more places and quietly falling out
of sync. Concretely, this shows up as:

- **Tools are installed once, as a real source clone, and every access point is a symlink back
  to it** — never a copy. GStack, Matt Pocock's skills, Anvil's skills, and the Magdoub
  wireframe skill all follow this pattern. `~/.config/opencode/skills/` (WSL) is the
  browsable runtime surface of these symlinks, not a second copy of anything.
- **Each project's configuration lives in exactly one file** — its own `{slug}-config.yaml`,
  registered in `projects-config-register.md` — not duplicated in `docmap.md`, not
  scattered across skill definitions.
- **Reference documents point at each other instead of repeating content.** [[gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]]
  defers to [[postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]] for database operational detail rather than duplicating
  it. `daily-ops.md` references config facts rather than hardcoding them.
- **ADRs use filename-based identity, not sequential numbers** — the same reasoning applied
  one level further: a number is a second, fragile identity alongside a document's real name,
  and it's the thing that kept silently breaking. See `adr-global/` for the applied result.

## Kept fresh by

`mb-docs-manager` (installed skill — register verification is defined in its SKILL.md
Section 3.1) — reads `projects-config-register.md` and cross-checks it against the real
filesystem, flagging missing or orphaned entries. Registering a new project's config YAML
here is a required step in the "start a project" protocol, checked by mb-docs-manager runs
rather than after the fact.
