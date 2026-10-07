---
title: "sysdoc-creator-exam-plan"
doc-id: "mb-8bad3cf4"
updated: "2026-10-07"
---

# sysdoc-creator — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager
before each run from [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-config.md) (spec), the last
[[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-exam-report.md), [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-log.md) (events
since last run), [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-learnings.md). Consumed by the skill
at run time; rewritten at the start of the following cycle. The file is live;
its contents are transient.

**This first plan is hand-written** (bootstrap emulation of the proven
cycle); it also serves as the format template. The **standing check inventory
lives in the skill** ([[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-exam-skill|Exam Skill source]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-exam-skill.md),
born-with-inventory); this plan carries run-specifics and references.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | 2026-10-07 |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution ([[[mybizz-config-docs:mb-config-manager/config-manager-log\|Config Manager Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md)) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request at the gate) | (a) Tier 3 unlock decision (SC3-1 full source-vs-spec conformance walk; SC3-2 output-discipline evidence audit of the two 2026-10-07 run logs + one produced-suite spot-check); (b) any check whose command text a guard denies; (c) none else anticipated |
| Expected-value source of truth | [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-config\|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-config.md) — read fresh at run start; never rely on remembered values |
| Named state-change steps (procedural conflicts stated, not asked) | **S-1 (2026-10-07):** the register row for this system stands `Deferred` (developer decision 2026-09-13) where the build-out expects `WIP` — flipped `Deferred` → `WIP` by this named step, citing the developer instruction "run mb-config-manager on mb-sysdoc-creator" (2026-10-07) and the mb-memory-system-diagnostic S-1 precedent (2026-09-28); the row flips `WIP` → `Installed` at Phase 2 per the setup prompt. **S-2 (2026-10-07):** grant discipline — three grants issued by the developer for this run (suite folder 12; config-manager folder 4; install folder 3); denials are never worked around |
| Scope boundary | This module exams **the subject skill itself**: installed copy, source copy, suite documents, the governing specification (artifact, examined never edited), run-log infrastructure (read-only), GBrain integration, invocation surface. **Produced suites belong to their own `mb-config-*` modules** — never re-tested here. **Running the skill is out of scope.** Cupcake internals out of scope entirely. |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec open items kept under
watch (observations, not findings):

| # | Watch item (spec open items) | This run's action |
|---|---|---|
| W-1 | Spec open item #1: skills catalog records `mb-sysdoc-creator` as installed | SC2-2 verifies the catalog row live (the 2026-10-07 archify-scope run log already records "row OK") |
| W-2 | Spec open item #2: no version field — currency provable only by diff | SC1-2/SC2-4 exercise exactly that mechanism; the mechanism is currently broken by the empty source copy (F-1) |
| W-3 | Spec open item #3: suite prefix `sysdoc-creator-` differs from folder/skill name — developer-stated naming | Standing watch; no action — recorded naming decision, not a defect |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-10-07: two live runs of the subject skill (`mb-archify-scope`, `mb-close-out`) — run logs present in `last-completed-run/`; spec §Suites produced table ends at 2026-09-09 | SC2-5 enumerates run logs vs the spec table; staleness flagged as spec DRIFT |
| LG-2 | 2026-10-07 09:00: installed copy modified (15,600 bytes vs spec-recorded 15,152) — hunk inventory vs the git-recovered source: description phrase naming retired systems removed (benign, aligns with retirements) + **Phase 9a — Register at birth added** | SC1-1/SC1-2/SC2-4 formalize: source copy is a stub (F-1), hash pair mismatched (F-2), Phase 9a content references retired machinery |
| LG-3 | 2026-10-07: Phase 9a fired on the archify-scope run and flagged a spurious open item ("no suite register exists in mybizz-config-docs") against the register institution discontinued 2026-09-30/10-05 | SC1-4 structure check locates Phase 9a; finding presented at the gate (F-3) |

## 5. Learnings-driven items

None — bootstrap (the learnings table is empty at first plan synthesis).

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in the [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-exam-skill|Exam Skill source]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-exam-skill.md)
(Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** SC0-1 installed copy present with functional frontmatter · SC0-2 discoverable in the session skill surface · SC0-3 governing specification present at its permanent location (absent = the subject cannot lawfully run)
- **Tier 1 (A) — state conformance:** SC1-1 source copy format + body intact · SC1-2 hash pair + body identity below frontmatter · SC1-3 suite completeness · SC1-4 structure inventory vs spec (rules/phases/constraints/statuses/folders) · SC1-5 log infrastructure vs spec · SC1-6 GBrain integration state · SC1-7 register row conformance
- **Tier 2 (A) — functional proof (present ≠ working; read-only only):** SC2-1 installed copy machine-parsable · SC2-2 invocation contract live (skills-catalog row) · SC2-3 resume machinery real · SC2-4 drift-detection mechanism functions · SC2-5 run-log evidence vs spec suites-produced table
- **Tier 3 (D, locked):** SC3-1 full source-vs-spec conformance walk · SC3-2 output-discipline evidence audit (run logs + one produced-suite spot-check)

## 7. Report requirements

The run writes [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-exam-report.md): verdict line;
per-tier tables (check ID, expected, actual, result); findings with class +
evidence + recommended repair + risk; runner attribution for every deferred
item (guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-log.md) (run-row
format per [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings filed.

## 8. Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- Agent-healable: suite-file repairs only (config-manager standard);
  everything else developer-run or proposed
- Deny-list (never heal, never touch without the developer's explicit
  per-item approval naming the file): the subject `SKILL.md` · its source
  copy · `doc-suite-specification.md` · the run-log infrastructure · produced
  suites' documents · Cupcake internals
- Spec-doc corrections → flagged to docs governance, never applied here
- Tier 3 unlock decision asked at the gate, never assumed
- Credentials: variable names only, never printed (no credential surfaces
  exist in this system)