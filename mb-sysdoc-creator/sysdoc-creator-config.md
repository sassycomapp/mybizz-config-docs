---
title: "sysdoc-creator-config"
doc-id: "mb-7688c176"
updated: "2026-10-15"
---
# sysdoc-creator — Config

State of the `mb-sysdoc-creator` skill.

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | Source commit `61ffe23` |
| Standard taken from | Own repository `C:\mybizz\mb-sysdoc-creator\` (origin `sassycomapp/mb-sysdoc-creator`), commit `61ffe23` |
| Last researched | 2026-10-15 |

## Documents in this folder

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Config document | Required; a new document takes the same name start as the documents already in the folder | Present — `sysdoc-creator-config.md` | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | |
| Reference document | Required; a new document takes the same name start as the documents already in the folder | Present — `sysdoc-creator-reference.md` | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | |
| Explainer document | Required; a new document takes the same name start as the documents already in the folder | Present — `sysdoc-creator-explainer.md` | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | |
| Learnings document | Required; a new document takes the same name start as the documents already in the folder | Present — `sysdoc-creator-learnings.md` | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | |

## Working files

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| doc-suite-specification.md | An integrity system's folder may hold the working files it needs, each listed in its own config | Present — the governing specification every suite this skill writes must satisfy | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md); `SKILL.md` | — |

## Source and install

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Canonical skill definition | A system MyBizz built takes its standard from its own source files | `C:\mybizz\mb-sysdoc-creator\mb-sysdoc-creator.md` — own repository, origin `sassycomapp/mb-sysdoc-creator` | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md); [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | — |
| Installed copy | An OpenCode skill installs as `~/.config/opencode/skills/{name}/SKILL.md` | `~/.config/opencode/skills/mb-sysdoc-creator/SKILL.md` | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills-catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | — |
| Source↔installed sync | Installed body = canonical body; only frontmatter may differ | Byte-identical (body hash `9d53bcf94b3049e1`) | [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-reference\|reference]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-reference.md) Checks | — |

## GBrain

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| GBrain pages | — | `mb-sysdoc-creator`; `mb-sysdoc-creator/doc-suite-specification`; `mb-sysdoc-creator/sysdoc-creator-config`; `mb-sysdoc-creator/sysdoc-creator-reference`; `mb-sysdoc-creator/sysdoc-creator-explainer` | GBrain resolve, live 2026-10-14 | — |
| Source registration | — | Own repository registered as federated GBrain source `mb-sysdoc-creator`; suite pages on the `mybizz-config-docs` host source | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md); GBrain search | — |
| Memory Governor treatment | — | None — outputs are developer-authored documents synced as ordinary corpus | memory-governor suite grep, 2026-10-14 | — |

## Integrations

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Cupcake | — | No component-specific rule existed at research time (2026-10-14). Standing rules that bind the skill's operation: no cross-project filesystem writes by default (grants required); no autonomous commits. Live enforcement status: [[[mybizz-config-docs:cupcake/cupcake-config\|cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) Current Operational Status | policy inventory grep, 2026-10-14 | — |
| security-global | — | None found that changes this system's defaults (2026-10-14) | grep at `C:\dev\project-library-global\security-global\`, 2026-10-14 | — |
| Related skills | — | mb-config-manager (examines this suite, register cycle); mb-compile-rules; mb-submit-memory; mb-doc-check | [[[mybizz-config-docs:mb-config-manager/config-manager-agent\|config-manager agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md) | — |

## Open items

None.
