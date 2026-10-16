---
title: "project-docs-config"
doc-id: "mb-f7c435e5"
updated: "2026-10-16"
---
# mb-project-docs — Config

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | `66fb55a` (2026-10-16) — the skill declares no version field |
| Standard taken from | `C:\mybizz\mb-project-docs\mb-project-docs.md` at `66fb55a` |
| Last researched | 2026-10-15 |

## Installed surface

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Installed copy | `~/.config/opencode/skills/mb-project-docs/SKILL.md` | same | [[[mybizz-os-docs:os-reference-docs/skills-catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md); verified live 2026-10-15 | — |
| Authoritative copy | `C:\mybizz\mb-project-docs\mb-project-docs.md` (GitHub-backed public repository) | same | [[[mybizz-os-docs:os-reference-docs/skills-catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md); [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | — |
| Currency check | diff of the two copies' bodies — no version field exists | same; bodies identical on 2026-10-15 | installed `SKILL.md`; source | — |
| Helper script | `C:\mybizz\scripts\agents-from-reference.sh` | same; behaviour verified against its recorded description | [[[mybizz-config-docs:mb-project-docs/project-docs-reference]]](C:/mybizz/mybizz-config-docs/mb-project-docs/project-docs-reference.md) § The copy line | — |

## Form

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Invocation | `/mb-project-docs` — explicit invocation only, never auto-trigger | same | source frontmatter (description) | — |
| Scope of a run | the current project only | same | source, hard rule 1 | — |
| Language | natural-language procedure; no executable code of its own | same | source | — |
| Version field | none — frontmatter holds `name` and `description` only | same | installed `SKILL.md`; source | — |

## Project coverage

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Covered projects | `mb-3-cs`, `mb-4-ecom`, `mb-5-pdlf`, `pdlf` | same | source Step 1; [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) § Names | — |
| Documentation repositories | `{slug}-project-library` under `C:\dev\dev-{slug}\`; `pdlf` at `C:\pdlf` | same | source Step 1; [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | — |
| Code repositories | `{slug}-app1` (the development workspace), `{slug}-app3` and `{slug}-app5`; none for `pdlf` | same | source Step 1 | |

## Destination

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Documentation repository | the repository root | same | source Step 2 | — |
| Code repository | `theme\assets\docs\appN`, `N` the app's number; created once by the developer through Anvil's Add asset > Upload folder, never locally; `pilot-doc.txt` never removed; `anvil.yaml` or the folder missing → STOP, BLOCKED, with the setup steps | same | source Step 2 | L2 |

## Files written per repository

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `{slug}-config.md` | documentation repository root; code repository `theme\assets\docs\appN` | same | source Steps 2, 5, 7 | — |
| `{slug}-reference.md` | same, then its body is copied over the agent file and the file deleted | same | source Steps 5, 7 | — |
| `{slug}-explainer.md` | documentation repository root; code repository `theme\assets\docs\appN` | same | source Steps 2, 5, 7 | — |
| `README.md` | repository root, either kind | same | source Step 5 | — |
| `AGENTS.md` / `agents.md` | written only by the developer's terminal line; never by the agent | same | source Step 7, hard rule 5 | — |

## Dependencies

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Governing specification | `C:\mybizz\mybizz-config-docs\mb-sysdoc-creator\doc-suite-specification.md` | same, verified present | source, preamble | — |
| Facts about repositories | `C:\mybizz\mybizz-os-docs\os-reference-docs\repo-organization.md` — pointed to, never repeated | same, verified present | source Step 3 | — |

## Integration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Close-out | Step 3 of `/mb-close-out` runs the skill to its Step 6 inside the close-out gate, then runs its Step 7 | same, verified live | `~/.config/opencode/skills/mb-close-out/SKILL.md` | — |
| Global `AGENTS.md` | Rule "Project documents": agents read the README and the three files on entering a project | same, verified live | `~/.config/opencode/AGENTS.md` | — |
| Commit hook | covers the documentation repositories only; code repositories are outside it | same | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) § Commit hook | — |
| Git | documentation repositories committed with `commit-all.sh`; code repositories committed by the developer; `.gitignore` never touched | same | source Step 7, hard rule 6; [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | — |
| Grants | a policy block ends in a developer-run `mg-grant` or `net-grant` | same, proved live 2026-10-15 | [[[mybizz-os-docs:operating-procedures/grant-paths]]](C:/mybizz/mybizz-os-docs/operating-procedures/grant-paths.md) | — |

## Open items

None.
