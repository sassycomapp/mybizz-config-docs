---
title: "README"
doc-id: "mb-46a3cb92"
updated: "2026-10-04"
---
# mybizz-config-docs — README

Tool-by-tool configuration reference documents — one folder per tool, each holding a single,
purely functional reference: what's installed, where, how it's configured, and how to verify
it's working. Not historical narrative, not task-completion reports — this suite is
steady-state functional reference only.

## Structure

| Folder | Reference document |
|---|---|
| `opencode/` | [[[mybizz-config-docs:opencode/opencode-reference\|Commands, Verification, Troubleshooting]]](C:/mybizz/mybizz-config-docs/opencode/opencode-reference.md) |
| `gstack/` | [[[mybizz-config-docs:gstack/gstack-reference\|GStack Reference]]](C:/mybizz/mybizz-config-docs/gstack/gstack-reference.md), [[[mybizz-config-docs:gstack/gstack-skills-reference\|GStack Skills Reference]]](C:/mybizz/mybizz-config-docs/gstack/gstack-skills-reference.md) |
| `gbrain/` | [[[mybizz-config-docs:gbrain/gbrain-reference\|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) |
| `postgresql/` | [[[mybizz-config-docs:postgresql/postgresql-reference\|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md) |
| `matt-pocock-skills/` | [[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-reference\|Matt Pocock Skills Reference]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-reference.md) |
| `anvil-agent-references/` | [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-reference\|Reference: Install, Skills, and Technical Detail]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-reference.md) |
| `magdoub-wireframe/` | [[[mybizz-config-docs:magdoub-wireframe/magdoub-wireframe-reference\|Reference: Invocation, Operation, Update]]](C:/mybizz/mybizz-config-docs/magdoub-wireframe/magdoub-wireframe-reference.md) |
| `graphify/` | [[[mybizz-config-docs:graphify/graphify-reference\|Graphify Reference]]](C:/mybizz/mybizz-config-docs/graphify/graphify-reference.md) |

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
- **Each project's configuration lives in exactly one file** — its own `{slug}-config.yaml`
  at the project's root — not duplicated in `docmap.md`, not
  scattered across skill definitions.
- **Reference documents point at each other instead of repeating content.** [[[mybizz-config-docs:gbrain/gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md)
  defers to [[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md) for database operational detail rather than duplicating
  it. `daily-ops.md` references config facts rather than hardcoding them.
- **ADRs use filename-based identity, not sequential numbers** — the same reasoning applied
  one level further: a number is a second, fragile identity alongside a document's real name,
  and it's the thing that kept silently breaking. See `adr-global/` for the applied result.

## Kept fresh by

The repository's documents are kept accurate by /mb-project-docs during
close-out ([[[mybizz-os-docs:operating-procedures/close-out-process]]](C:/mybizz/mybizz-os-docs/operating-procedures/close-out-process.md)); the documentation repositories listed in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md) are committed,
GBrain-updated and pushed by commit-all.sh ([[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md)).
