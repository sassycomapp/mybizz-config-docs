# C:\mybizz\config — README

Tool-by-tool configuration reference documents — one folder per tool, each holding a single,
purely functional reference: what's installed, where, how it's configured, and how to verify
it's working. Not historical narrative, not task-completion reports — those live in
`config-changelog.md` (`C:\mybizz\WIP\`) instead.

## Structure

| Folder | Reference document |
|---|---|
| `opencode/` | `opencode-reference.md` |
| `gstack/` | `gstack-reference.md`, `gstack-skills-reference.md` |
| `gbrain/` | `gbrain-reference.md` |
| `postgresql/` | `postgresql-reference.md` |
| `matt-skills/` | `matt-pocock-skills-reference.md` |
| `anvil-skills/` | `anvil-skills-reference.md` |
| `magdoub-wireframe/` | `magdoub-claude-wireframe-skill-reference.md` |
| `graphify/` | `graphify-reference.md` |

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
  wireframe skill all follow this pattern. `skills-collective/` (`C:\mybizz\`) is the
  browsable hub of these symlinks, not a second copy of anything.
- **Each project's configuration lives in exactly one file** — its own `{slug}-config.yaml} —
  not restated in `project-inventory.md` (now retired), not duplicated in `docmap.md`, not
  scattered across skill definitions.
- **Reference documents point at each other instead of repeating content.** `gbrain-reference.md`
  defers to `postgresql-reference.md` for database operational detail rather than duplicating
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
