---
title: "mb-close-out-config"
doc-id: "mb-e1c4d0bf"
updated: "2026-10-16"
---
# mb-close-out — Config

Settings of the `mb-close-out` skill, governed by [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification|doc suite specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md).

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | `5499a8f` — latest commit of the source repository (2026-10-15) |
| Standard taken from | `C:\mybizz\mb-close-out\mb-close-out.md` at commit `5499a8f` |
| Last researched | 2026-10-15 |

## Component

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Component | first-party OpenCode skill, mb-* family; session close-out orchestrator that executes existing scripts and skills, replaces none | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Invocation | `/mb-close-out`; explicit invocation only, never auto-trigger | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Version field | none declared in SKILL.md frontmatter | none | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | L1 |
| Language | natural-language procedure; no executable code, no runtime dependencies | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |

## Copies and sync

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Source document | the issuer standard itself | `C:\mybizz\mb-close-out\mb-close-out.md` (86 lines) | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Installed copy | — | `~/.config/opencode/skills/mb-close-out/SKILL.md` (90 lines) | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Copy sync | bodies byte-identical below the frontmatter | verified 2026-10-15 | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | L2 |
| Frontmatter | differs between the copies by design | OpenCode format (`name`, `description`) on the installed copy; corpus format (`title`, `doc-id`, `updated`) on the source | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | L2 |
| Drift detection | body diff of the two copies below the frontmatter | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | L1 |
| Skills-catalog status | row present, status OK | OK (checked 2026-10-15) | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | |

## Source repository

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Local path | — | `C:\mybizz\mb-close-out` (WSL `/mnt/c/mybizz/mb-close-out`) | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| GitHub | — | `mb-close-out`, Public (developer-confirmed 2026-10-15); remote `https://github.com/sassycomapp/mb-close-out.git` | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Commit-all list | — | member — committed, GBrain-updated and pushed by commit all | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Cupcake readiness | — | fallback (no skeleton); global policies only | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Dream-cycle eligible | — | no | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| GBrain source | — | `mb-close-out`, federated, 1 page (verified 2026-10-15) | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |

## Procedure structure

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Rules | 7 | 7 | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Steps | 9 | 9 | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Completion statuses | 3 — DONE, DONE_WITH_REVIEWS_PENDING, BLOCKED | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Traps | 3 | 3 | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |

### Step → existing component

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Step 1 — Session page | file `sessions/<YYYY-MM-DD>-<short-slug>.md` in the current repository when it is on the commit-all list, else `C:\mybizz\mybizz-config-docs\sessions\`; commit all imports it into GBrain | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 2 — Candidate facts | advisory/governed routing; governed → fact file + mb-submit-memory Steps 1–4 | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 3 — Project documents | [[[mb-project-docs:mb-project-docs\|mb-project-docs]]](C:/mybizz/mb-project-docs/mb-project-docs.md) Steps 1–6, for the four projects mb-3-cs, mb-4-ecom, mb-5-pdlf, pdlf | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 4 — Changed files | `bash /mnt/c/mybizz/scripts/commit-all.sh --status` | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 5 — Gate | one approval; satisfies mb-submit-memory Step 5 and mb-project-docs Step 6 | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 6 — After approval | GBrain `remember` (advisory); mb-submit-memory Steps 6–9; mb-project-docs Step 7 | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 7 — Terminal block 1 | developer runs: the AGENTS.md copy line, rule-produced lines, `commit-all.sh "close-out: <topic>"` | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 8 — Terminal block 2 | developer runs one promote per `under_review` memory id | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Step 9 — Verify and report | worker-log grep, review queue empty, report; commit-all verified per its own procedure | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |

## Fact-file destination (Step 2)

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Current repository on the commit-all list | fact file in that repository's `facts/` folder | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Otherwise | `C:\mybizz\mybizz-config-docs\facts\` | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Naming | `<YYYY-MM-DD>-<slug>.md`, body only; the commit hook adds the frontmatter | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |

## Memory Governor integration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Relationship | orchestrator, not a governed writer — governed facts flow through mb-submit-memory | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Advisory facts | direct GBrain `remember`, visibility `world`, provenance names the session, entity set when the fact has a subject | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Promote endpoint (Step 8, developer-run) | `POST http://127.0.0.1:8321/memory/<memory-id>/review` | same | [[[mybizz-config-docs:memory-governor/memory-governor-reference\|memory governor reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md) | |
| Credential | `$MEMORY_GOVERNOR_WRITER_MANUAL_SUBMISSION`, referenced by variable name only | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| End condition | governor review queue empty before the close-out ends | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Landing record | `grep "remembered as fact" /tmp/memory-governor-worker.log`, last 10 lines | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |

## GBrain integration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Session pages | written as files (never `put_page` or `gbrain capture` — no source owner exists), corpus slug `sessions/<YYYY-MM-DD>-<short-slug>`, imported by commit all | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Facts | governed lane through the governor; advisory lane through `remember` | same | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |
| Suite indexing | this folder lands in the `mybizz-config-docs` source by ordinary sync | same | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |

## Cross-cutting

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Cupcake rule coverage | no component-specific rule (27 active policies grepped 2026-10-15); Rules 1–3 of the skill mirror standing general rules | same | [[[mybizz-config-docs:cupcake/cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | |
| Cupcake enforcement | per the operational status in [[[mybizz-config-docs:cupcake/cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | Active and enforcing everywhere (verified 2026-10-15) | [[[mybizz-config-docs:cupcake/cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | |
| security-global | the grant discipline implements the verified cross-project write boundary | boundary document present at the cited path (2026-10-15) | [[[default:security-global/infrastructure/sec-local-filesystem-access-boundary]]](C:/dev/project-library-global/security-global/infrastructure/sec-local-filesystem-access-boundary.md) | |
| Related skills | mb-submit-memory Steps 1–4 and 6–9 (governed facts); mb-project-docs Steps 1–6 and 7 (its Rule 8: the close-out gate is its Step 6 approval) | verified against the installed skills 2026-10-15 | [[[mb-submit-memory:mb-submit-memory]]](C:/mybizz/mb-submit-memory/mb-submit-memory.md) · [[[mb-project-docs:mb-project-docs\|mb-project-docs]]](C:/mybizz/mb-project-docs/mb-project-docs.md) | |
| Retired artifacts | sessions-log and facts-log, retired by decision; the skill writes to neither | neither file exists | [[[mb-close-out:mb-close-out]]](C:/mybizz/mb-close-out/mb-close-out.md) | |

## Registers

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Skills catalog (mybizz-os-docs) | row present, status OK | OK (checked 2026-10-15) | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | |
| mybizz-config-docs corpus register | none exists | flagged, not created (checked 2026-10-15) | folder listing | |

## Open items

None.
