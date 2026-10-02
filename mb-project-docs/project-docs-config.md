---
title: "project-docs-config"
doc-id: "mb-f7c435e5"
updated: "2026-10-02"
---
# mb-project-docs — Config

State of the `mb-project-docs` skill as of 2026-10-02.

## Identity

| Field | Value |
|---|---|
| Component | `mb-project-docs` — first-party OpenCode skill, mb-* family |
| Invocation | `/mb-project-docs` — explicit invocation only, never auto-trigger |
| Version field | None declared in SKILL.md frontmatter (name and description only) |
| Language | Natural-language procedure; no executable code of its own |
| Scope of a run | The current project only |

## Installed surface

| Item | Value |
|---|---|
| Installed copy | `~/.config/opencode/skills/mb-project-docs/SKILL.md` |
| Authoritative copy | `skill.md` in this folder |
| Drift detection | Diff of the two copies — no version field exists |
| Helper script | `C:\mybizz\scripts\agents-from-reference.sh` |

## File inventory (this folder)

| File | Role |
|---|---|
| `skill.md` | Skill definition — authoritative copy |
| `project-docs-config.md` | This document |
| `project-docs-reference.md` | Companion — usage and execution |
| `project-docs-explainer.md` | Companion — orientation and reasoning |

## Projects covered

| Project | Documentation repository | Code repository |
|---|---|---|
| `makepdlf` | `makepdlf-project-library` | `makepdlf` (empty shell today: no Anvil app) |
| `mb-3-cs` | `mb-3-cs-project-library` | `mb-3-cs` |
| `mb4ecom` | `mb4ecom-project-library` | `mb4ecom` |
| `mb5pdlf` | `mb5pdlf-project-library` | `mb5pdlf` |
| `pdlf` | `pdlf` | none |

Paths, GitHub repositories and GBrain sources of these repositories are in [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md).

## Files written per repository

| File | Documentation repository | Code repository |
|---|---|---|
| `{slug}-config.md` | Repository root | `theme\docs` |
| `{slug}-reference.md` | Repository root, then copied over the agent file and deleted | `theme\docs`, then the same |
| `{slug}-explainer.md` | Repository root | `theme\docs` |
| `README.md` | Repository root | Repository root |
| `AGENTS.md` | Written by the developer's terminal line, never by the agent | Same; the file `agents.md` is used where that name exists (`mb-3-cs`) |

## Destination check for a code repository

| Condition | Result |
|---|---|
| `anvil.yaml` and `theme\` both exist | `theme\docs` is created if missing, without asking |
| Either is missing | The run stops with status BLOCKED; the developer must create the Anvil app first |

## Dependencies

| Item | Value |
|---|---|
| Governing specification | `C:\mybizz\mybizz-config-docs\mb-sysdoc-creator\doc-suite-specification.md` |
| Facts about repositories | `C:\mybizz\mybizz-os-docs\os-reference-docs\repo-organization.md` — pointed to, never repeated |

## Integration

| System | State |
|---|---|
| Close-out | Step 2a of the close-out procedure runs the skill before the approval gate; its proposed changes are shown at that gate |
| Global `AGENTS.md` | Rule "Project documents": agents read the README and the three files on entering a project |
| Commit hook | Covers documentation repositories only; code repositories are outside it |
| Git | Documentation repositories: committed with `commit-all.sh`. Code repositories: committed by the developer. `.gitignore` is never touched |
| Grants | A policy block ends in a request for `mg-grant` or `net-grant`, run by the developer |

## Completion statuses

DONE, BLOCKED, PERMISSION_REQUIRED, CANCELLED.

## Open items

| # | Item | Status |
|---|---|---|
| 1 | The documentation repositories of `mb4ecom` and `mb5pdlf` are not under the commit hook yet, so their files are not checked | Open |
| 2 | No version field in SKILL.md; currency of the two copies is provable only by diff | Open |
| 3 | Whether Anvil accepts and keeps an extra folder `theme\docs` has not been verified | Open |
