---
title: "archify-config"
doc-id: "mb-61a8f528"
updated: "2026-10-20"
---
# Archify — Configuration

State of the Archify skill. States facts, not history or reasoning — see [[[mybizz-config-docs:archify/archify-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/archify/archify-explainer.md) for what it is and why, [[[mybizz-config-docs:archify/archify-reference|Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md) for commands and procedures.

## Identity

| Field | Value |
|---|---|
| Issuer | tt-a1i |
| Installed version | 2.16.0 |
| Standard taken from | 2.16.0 — the installed `SKILL.md`, `schemas/` and `references/` (clone commit `665ac1f`) |
| Last researched | 2026-10-20 |

## Release and source

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| License | MIT | MIT | `SKILL.md` frontmatter; `LICENSE` | |
| Author | tt-a1i | tt-a1i | `SKILL.md` frontmatter | |
| Based on | Cocoon-AI/architecture-diagram-generator (MIT, v1.0) | as standard | `SKILL.md` frontmatter | |
| Source repository | `github.com/tt-a1i/archify` | cloned at `C:\mybizz\archify` (WSL: `/mnt/c/mybizz/archify`), clean tree at commit `665ac1f` | `skill-release.json`; live git status | |
| Release identity | `skill-release.json` carries version, channel and update manifest | version `2.16.0`, channel `stable` | `skill-release.json` | |

## Install on this machine

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Install method | — | WSL symlink from OpenCode's global skill discovery path to the Windows-drive package folder | live readlink | |
| Skill package root | — | `C:\mybizz\archify\archify` (WSL: `/mnt/c/mybizz/archify/archify`) | live listing | |
| Discovery path | — | `~/.config/opencode/skills/archify` → `/mnt/c/mybizz/archify/archify` | live readlink | |
| Skill status | — | Working — per [[[mybizz-os-docs:os-reference-docs/skills-catalog\|Skills Catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md); confirmed by the doctor run | skills-catalog; doctor | |
| Update check | notification-only awareness; never downloads, installs, or executes an update | as standard | `SKILL.md` §Update awareness | |
| Update-check disable | `ARCHIFY_UPDATE_CHECK_DISABLED` | `1` set — disables networking and reminder-state writes | `bin/archify.mjs` | |
| Update manifest URL | one fixed trusted URL | `https://tt-a1i.github.io/archify/skill-updates/archify/stable.json` | `skill-release.json` | |

## Runtime

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| CLI entry point | `bin/archify.mjs` | as standard | `SKILL.md`; `bin/` | |
| Invocation | — | `/archify` | `SKILL.md` frontmatter | |
| Node requirement | >=18 | v24.15.0 active | `package.json` engines; `node --version` | |
| Runtime dependencies | — | none (devDependencies only: `ajv`, `parse5`, `saxes`, `simple-icons`) | `package.json` | |
| Doctor | 15 checks | 15/15 pass — "Archify is ready." | `node bin/archify.mjs doctor` | |

## Package structure (`archify/archify/`)

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `SKILL.md` | the skill instruction file the harness reads | present — frontmatter `name: archify`, version `2.16` | live listing | |
| `skill-release.json` | release identity file | present | live listing | |
| `schemas/` | one schema per diagram type | 6 schema files plus `README.md`: `common`, `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle` | live listing | |
| `references/` | — | 4 files: `authoring-contract.md`, `brand-marks.md`, `delivery-contract.md`, `viewer-runtime.md` | live listing | |
| `bin/` | — | 4 files: `archify.mjs` (entry point), `open-artifact.mjs`, `preview.mjs`, `visual-check.mjs` | live listing | |
| `scripts/` | — | 6 files, including `check-update.mjs` and `update-contract.mjs` | live listing | |
| `renderers/` | — | per-type renderers plus `shared/` | live listing | |
| `recipes/`, `examples/`, `test/`, `migrations/`, `delta/`, `assets/`, `brand-marks/` | — | supporting package content | live listing | |

## Scoping component (`mb-archify-scope`)

Scoping facts — scope mechanics, Scope Card conventions, triggers, evidence — live in the mb-archify-scope suite: [[[mb-archify-scope:mb-archify-scope|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md).

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Role | — | permanent front-of-pipe component of the Archify pipeline: it turns a drawing request into an agreed Scope Card before any Archify authoring begins; it scopes, it never draws | [[[mb-archify-scope:mb-archify-scope\|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md) | |
| Installed copy | — | `~/.config/opencode/skills/mb-archify-scope/SKILL.md` — body identical to the canonical specification; headers differ by design (the committed spec carries document frontmatter, the installed file carries skill frontmatter) | body-hash check | |
| Invocation order | — | `/mb-archify-scope` runs before `/archify`, never instead of it | [[[mb-archify-scope:mb-archify-scope\|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md) | |

## Working files

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `output/` | an integrity system's folder may hold the working files it needs, each listed in its own config | runtime output — one folder per project slug under `output/<slug>/` (scope card, header, drafts, rendered HTML, visual-check evidence) | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) §The folder; live listing | |

## Integrations

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| OpenCode | — | skill discovered via the global skills symlink; invoked as `/archify` | skills-catalog | |
| GBrain | — | indexes this suite — the four documents are retrieval hits for the system's name and function; GBrain facts (version, reranker) live in the gbrain suite: [[[mybizz-config-docs:gbrain/gbrain-config\|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) | gbrain search; [[[mybizz-config-docs:gbrain/gbrain-config\|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) | |
| Cupcake | — | no archify-specific rule in the global policy folder; enforcement state is standing policy in [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) §Operational status — not fixed; re-check there | rules folder check; [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | |
| Memory Governor | — | no treatment — archify produces HTML artifacts, not memory submissions; not a governed writer | memory-governor folder check | |
| security-global | — | no principle bears directly; the only network surface is the optional update check (notification-only, disableable) | security-global library check | |
| Related skills | — | Graphify (knowledge graphs) and GStack `/design-html` (UI page HTML) are complementary, different-domain; no dependency in either direction | — | |

## Open items

None.
