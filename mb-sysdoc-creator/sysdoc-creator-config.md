---
title: "sysdoc-creator-config"
doc-id: "mb-7688c176"
updated: "2026-10-01"
---
# sysdoc-creator — Config

State of the `mb-sysdoc-creator` skill as of 2026-09-09. All facts
verified live this date unless noted.

## Identity

| Field | Value |
|---|---|
| Component | `mb-sysdoc-creator` — first-party OpenCode skill, mb-* family |
| Invocation | `/mb-sysdoc-creator (system-name)` — explicit invocation only, never auto-trigger |
| Version field | None declared in SKILL.md frontmatter (name + description only) |
| Language | Natural-language procedure; no executable code, no runtime dependencies |

## File inventory (this folder)

| File | Lines | Role |
|---|---|---|
| `skill.md` | 309 | Skill definition — authoritative copy |
| [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|config / reference / explainer]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | 135 | Governing specification for every suite this skill produces |
| `sysdoc-creator-config.md` | — | This document |
| [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-reference\|Reference]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-reference.md) | — | Companion — execution |
| [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-explainer\|Explainer]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-explainer.md) | — | Companion — orientation and reasoning |

## Installed surface

| Item | Value |
|---|---|
| Installed copy | `~/.config/opencode/skills/mb-sysdoc-creator/SKILL.md` |
| Size / date | 15,152 bytes, 2026-09-06 |
| Sync state | Byte-identical to `skill.md` in this folder (diff-verified 2026-09-09) |
| Drift detection | Diff of the two copies — no version field exists to check instead |

## Governing specification

| Item | Value |
|---|---|
| File | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|config / reference / explainer]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) |
| Indexed in GBrain as | `mb-sysdoc-creator/doc-suite-specification` |
| Defines | Per-document contents, never-contains lists, stray-line tests for all three suite documents |
| Applies to | Every suite this skill drafts — no independent structure improvisation permitted |

## Procedure structure (SKILL.md)

| Section | Contents |
|---|---|
| Hard rules | 7 (Section 0) |
| Phases | 0–10 (Section 1), one continuous run |
| Hard constraints | 5 (Section 2) |
| Completion statuses | 5: DONE, BLOCKED, PERMISSION_REQUIRED, REPORT_REJECTED, DRAFT_REJECTED |
| Log folders | 5 (see below) |

## Log infrastructure

| Path | Holds | State 2026-09-09 |
|---|---|---|
| `C:\mybizz\logs\mb-sysdoc-creator\` | Permanent history root | Live |
| `...\learnings\learnings.md` | Durable cross-run patterns | 16 run sections, 2026-09-06 → 2026-09-09 |
| `...\in-progress\` | Current run only; resume source | Empty |
| `...\last-completed-run\` | Full detail of finished runs | 18 run logs (16 systems, incl. 2 correction runs) + 1 directory |
| `...\abandoned-runs\` | Declined-resume runs, never deleted | Empty |

## GBrain integration

| Item | Value |
|---|---|
| GBrain pages | `mb-sysdoc-creator/skill`, `mb-sysdoc-creator/doc-suite-specification` |
| Source | `mybizz-config-docs` host source — ordinary sync |
| Memory Governor treatment | None — no bypass exemption; settled policy from the 2026-09-06 anvil-docs run applies to the whole repo |

## Cross-cutting integration

| System | Finding |
|---|---|
| Cupcake | No component-specific rule found (rule inventory checked 2026-09-09). The skill's own Hard Rule 7 defines its block-handling discipline; enforcement status of any Cupcake rule is not fixed — live status lives in [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)'s Current Operational Status |
| Memory Governor | None found — not a governed writer; its outputs are developer-authored docs synced ordinarily |
| security-global | None found — no principles bear directly on this component's defaults |
| Related skills | mb-docs-manager (structural/navigational docs), mb-align-docs (cross-document consistency), mb-wikilinks (cross-reference conversion), mb-compile-rules (Cupcake rule pipeline), mb-submit-memory (memory submission) — see explainer for the division of labor |

## Suites produced (proven by run logs)

| Date | Systems |
|---|---|
| 2026-09-06 | archify, magdoub-wireframe, anvil-agent-references, anvil-docs, cupcake, gbrain, gbrain-dream-cycle |
| 2026-09-08 | graphify, gstack, matt-pocock-skills, mb-compile-rules, mb-submit-memory, memory-governor |
| 2026-09-09 | mb-sentinel-review, opencode, postgresql |

16 systems, 18 run logs (2 are Cupcake-phrasing correction runs).

## Open items

1. [[[mybizz-os-docs:skills-reference/skills-register|Skill Register]]](C:/mybizz/mybizz-os-docs/skills-reference/skills-register.md) (`mybizz-os-docs`) lists six mb-* siblings as working — `mb-sysdoc-creator` is absent. Correct the register if it is meant to be complete.
2. No version field in SKILL.md — currency between the two copies is provable only by diff.
3. This suite's file prefix (`sysdoc-creator-`) differs from the folder/skill name (`mb-sysdoc-creator`) — developer-stated naming for this suite; sibling suites use the folder name as prefix.
