---
title: "mb-close-out-config"
doc-id: "mb-e1c4d0bf"
updated: "2026-10-07"
---
# mb-close-out — Config

State of the `mb-close-out` skill as of 2026-10-07. All facts verified live this
date unless noted. Suite structure governed by [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md).

## Identity

| Field | Value |
|---|---|
| Component | `mb-close-out` — first-party OpenCode skill, mb-* family |
| Invocation | `/mb-close-out` — explicit invocation only, never auto-trigger |
| Class | Session close-out orchestrator — executes existing scripts and skills, replaces none |
| Version field | None declared in SKILL.md frontmatter (name + description only) |
| Language | Natural-language procedure; no executable code, no runtime dependencies |

## File inventory (this folder)

| File | Role |
|---|---|
| `mb-close-out-config.md` | This document |
| [[[mybizz-config-docs:mb-close-out/mb-close-out-reference]]](C:/mybizz/mybizz-config-docs/mb-close-out/mb-close-out-reference.md) | Companion — execution |
| [[[mybizz-config-docs:mb-close-out/mb-close-out-explainer]]](C:/mybizz/mybizz-config-docs/mb-close-out/mb-close-out-explainer.md) | Companion — orientation and reasoning |

## Installed surface

| Item | Value |
|---|---|
| Installed copy | `~/.config/opencode/skills/mb-close-out/SKILL.md` (91 lines) |
| Source document | `C:\mybizz\mb-close-out\mb-close-out.md` (86 lines, own git repository) |
| Sync state | Bodies byte-identical (diff-verified 2026-10-07); frontmatter differs by design |
| Drift detection | Diff of the two copies below the frontmatter — no version field exists to check instead |
| Skills-catalog status | OK — installed once, content identical to source ([[[mybizz-os-docs:os-reference-docs/skills-catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md), checked 2026-10-07) |

## Source repository

| Item | Value |
|---|---|
| Local path | `C:\mybizz\mb-close-out` (WSL `/mnt/c/mybizz/mb-close-out`) |
| GitHub | `mb-close-out` (Private) |
| GBrain source | `mb-close-out` (federated; indexed page `mb-close-out`) |
| Commit-all list | Member — committed, GBrain-updated, pushed by `commit-all.sh` |
| Cupcake readiness | Fallback (no skeleton) — global policies only ([[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md)) |
| Dream-cycle eligible | No |

## Procedure structure (SKILL.md)

| Section | Contents |
|---|---|
| Rules | 7 |
| Steps | 9 |
| Completion statuses | 3: DONE, DONE_WITH_REVIEWS_PENDING, BLOCKED |
| Traps | 3 |

## Step → existing component map

| Step | Executes |
|---|---|
| 1 — Session page | A file `sessions/<YYYY-MM-DD>-<short-slug>.md` in the repository; commit all imports it into GBrain |
| 2 — Candidate facts | Advisory/governed routing; governed → fact file + mb-submit-memory Steps 1–4 |
| 3 — Project documents | [[[mb-project-docs:mb-project-docs]]](C:/mybizz/mb-project-docs/mb-project-docs.md) Steps 1–6 (five projects only: makepdlf, mb-3-cs, mb4ecom, mb5pdlf, pdlf) |
| 4 — Changed files | `bash /mnt/c/mybizz/scripts/commit-all.sh --status` |
| 5 — Gate | Single approval; satisfies mb-submit-memory Step 5 and mb-project-docs Step 6 |
| 6 — After approval | GBrain `remember` (advisory); mb-submit-memory Steps 6–9; mb-project-docs Step 7 |
| 7 — Terminal block 1 | Developer: AGENTS.md copy line, rule-produced lines, `commit-all.sh "close-out: <topic>"` |
| 8 — Terminal block 2 | Developer: one promote per `under_review` memory id (memory-governor API) |
| 9 — Verify and report | Commit-all summary, worker-log grep, review-queue empty, report |

## Fact-file destination rule (Step 2)

| Condition | Destination |
|---|---|
| Current repository on the commit-all list | `<current-repo>/facts/` |
| Otherwise | `C:\mybizz\mybizz-config-docs\facts\` |
| File naming | `<YYYY-MM-DD>-<slug>.md`, body only — the commit hook adds the frontmatter |

## Memory Governor integration

| Item | Value |
|---|---|
| Relationship | Orchestrator, not a governed writer — governed facts flow through mb-submit-memory |
| Advisory facts | Direct GBrain `remember`, visibility `world`, provenance names the session |
| Promote endpoint (Step 8, developer-run) | `POST http://127.0.0.1:8321/memory/<memory-id>/review` |
| Credential | `$MEMORY_GOVERNOR_WRITER_MANUAL_SUBMISSION`, referenced by variable name only |
| End condition | Governor review queue empty before the close-out ends |
| Landing record | `grep "remembered as fact" /tmp/memory-governor-worker.log` piped to `tail -10` |

## GBrain integration

| Item | Value |
|---|---|
| Session pages | Corpus layer, slug `sessions/<YYYY-MM-DD>-<short-slug>` (ungoverned by design) |
| Facts | Governed layer via the governor; advisory via `remember` |
| Suite indexing | Lands in the `mybizz-config-docs` source by ordinary sync |

## Cross-cutting integration

| System | Finding |
|---|---|
| Cupcake | No component-specific rule (31-file policy inventory grepped 2026-10-07). Rules 1–3 of the skill mirror standing general rules (no autonomous commits, no grant self-approval, denials final). Enforcement status: ACTIVE per [[[mybizz-config-docs:cupcake/cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) (live-verified 2026-09-22) |
| Memory Governor | Orchestrates the governed path; no special treatment of the skill itself in governor config |
| security-global | [[[default:security-global/infrastructure/sec-local-filesystem-access-boundary]]](C:/dev/project-library-global/security-global/infrastructure/sec-local-filesystem-access-boundary.md) — the grant discipline implements the verified cross-project write boundary; supply-chain review satisfied (first-party, cataloged). Credential-hygiene doc: agent read Cupcake-denied 2026-10-07 (recorded, not worked around) |
| Related skills | mb-submit-memory (governed facts), mb-project-docs (its Rule 8: the close-out gate is its Step 6 approval) |
| Retired artifacts | sessions-log and facts-log — retired by decision (workflow-review Task 1.7); the skill writes to neither |

## Registers

| Register | State |
|---|---|
| Skills catalog (mybizz-os-docs) | Row present, status OK |
| mybizz-config-docs corpus register | None exists — flagged, not created (mb-archify-scope precedent) |

## Open items

1. Global AGENTS.md (`\\wsl.localhost\Ubuntu\home\dev-p\.config\opencode\AGENTS.md`, lines ~342–361) still instructs sessions-log/facts-log rows in three spots — both files no longer exist. Developer-owned edit.
2. `C:\data-mybizz-mgt\README.md` lines 30–33 still describe both logs as current. Developer-owned edit.
3. `C:\mybizz\mybizz-config-docs\facts\2026-09-15-session-numbers-from-sessions-log.md` asserts session numbers come from the retired log. Correction blocked on one question: what defines session numbers now (numbered pages 001–011 continued by convention after the log went stale).
4. `C:\dev\dev-root\docmap.md` line 31 still lists the `sessions-log/` folder. Developer-owned edit.
5. No version field in SKILL.md — currency between the two copies is provable only by diff (same open item as the sysdoc-creator suite).