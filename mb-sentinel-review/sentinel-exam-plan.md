---
title: "sentinel-exam-plan"
doc-id: "mb-dcb63c92"
updated: "2026-10-07"
---
# sentinel — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager
before each run from [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) (spec), the last
[[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-report.md), [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md) (events since last
run), and [[[mybizz-config-docs:mb-sentinel-review/sentinel-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-learnings.md). Consumed by the skill at run time;
rewritten at the start of the following cycle. The file is live; its contents
are transient.

**This first plan is hand-written** (bootstrap emulation of the proven
cycle); it also serves as the format template. The **standing check inventory
lives in the skill** ([[[mybizz-config-docs:mb-sentinel-review/sentinel-skill|Exam Skill source]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-skill.md), born-with-inventory);
this plan carries run-specifics and references.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | 2026-10-07 |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution ([[[mybizz-config-docs:mb-config-manager/config-manager-log\|Config Manager Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md)) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request at the gate) | (a) Tier 3 unlock decision (SN3-1 full spec-vs-live conformance walk; SN3-2 database deep probe via the bridge; SN3-3 methodology currency); (b) the three guard-forbidden Tier 1 classes — SN1-10 security-global library counts (sensitive-token class, denial proven live 2026-10-07), SN1-11 `triage_findings` database state (bridge route; `source .env` secrets class, proven), SN1-12 rules-cupcake rule inventory (cupcake-token class, proven) — exact commands supplied with the bundle; (c) none else anticipated |
| Expected-value source of truth | [[[mybizz-config-docs:mb-sentinel-review/sentinel-config\|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) — read fresh at run start; never rely on remembered values |
| Named state-change steps (procedural conflicts stated, not asked) | **S-1 (2026-10-07):** the register row for this system stands `Deferred` (developer decision 2026-09-13) where the build-out expects `WIP` — flipped `Deferred` → `WIP` by this named step, citing the developer instruction "run mb-config-manager on C:\mybizz\mybizz-config-docs\mb-sentinel-review" (2026-10-07) and the mb-sysdoc-creator S-1 precedent (2026-10-07; original precedent mb-memory-system-diagnostic S-1, 2026-09-28); the row flips `WIP` → `Installed` at Phase 2 per the setup prompt. **S-2 (2026-10-07):** grant discipline — three grants issued by the developer for this run (suite folder 12; config-manager folder 4; install folder 3); denials are never worked around |
| Scope boundary | This module exams **the Sentinel system itself**: the two subject skills' installed copies, the reasoning-methodology install, the security-global library's recorded shape (never content), the `triage_findings` database state (read-only, bridge-only), the step-intensity wiring in PDLF step files (read-only evidence), and this suite's documents. **Running the subject skill is out of scope** (a review writes database rows). **Cupcake internals out of scope entirely.** The governing ADR is Sealed — cited, never touched. |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Spec known-limitation rows kept under
watch (observations, not findings):

| # | Watch item (spec known limitations) | This run's action |
|---|---|---|
| W-1 | `mb-sentinel-review` has never been run live against a real feature — the first real PDLF-run feature is the test that matters | Standing watch; no exam action possible (running a review is out of exam scope) |
| W-2 | `finding_id` has no companion table — free-standing text identifier | Standing design fact; recorded, no action |
| W-3 | Methodology installed 2026-09-09 "without a restart — OpenCode may need a session restart before the skill registers in its catalog" | SN2-6 observes the session catalog directly; the caveat is expected superseded (registered) — spec-side freshness note if confirmed |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-10-07: build-out initiated per developer instruction; grants issued (12/4/3); exam set created; S-1 executed | Step-0 + SN1-8/SN1-9 verify the built state; register flip verified at Phase 2 |
| LG-2 | 2026-10-01/04: PDLF step files for the intensity table built/modified — all twelve steps now exist on disk, while the spec's built-status column records only Step 16 | SN1-5 formalizes: built-status staleness expected as a spec-side DRIFT finding; SN1-6 gathers the unwired-built-steps evidence (coverage gap surfaced at the gate) |
| LG-3 | 2026-09-13: `sentinel-skill.md` stub born empty (commit 4a15dae) — never a mirror of Skill 1, contrary to the spec §Identity claim | SN1-13 formalizes the mirror-claim staleness as a spec-side DRIFT finding |

## 5. Learnings-driven items

None — bootstrap (the learnings table is empty at first plan synthesis).

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in the [[[mybizz-config-docs:mb-sentinel-review/sentinel-skill|Exam Skill source]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-skill.md) (Tiers 0–3).
Summary:

- **Tier 0 (A) — invocability:** SN0-1 installed Skill 1 present with functional frontmatter · SN0-2 discoverable in the session skill surface · SN0-3 spec doc present (absent = DOWN, stop)
- **Tier 1 (A) — state conformance:** SN1-1 Skill 2 installed · SN1-2 methodology install · SN1-3 companion artifacts (genesis, scope, ADR) · SN1-4 Step-16 wiring (item 7 + item 9) · SN1-5 intensity built-status vs live · SN1-6 unwired-built-steps evidence · SN1-7 skill §1 table vs spec table · SN1-8 suite completeness · SN1-9 register row · SN1-13 spec mirror claim vs live — plus **Tier 1 (D), guard-forbidden classes:** SN1-10 security-global counts · SN1-11 `triage_findings` state (bridge) · SN1-12 rules-cupcake inventory
- **Tier 2 (A) — functional proof (present ≠ working; read-only only):** SN2-1 installed skill machine-parsable · SN2-2 CLEAR-fast-path + CLEAR-row doctrine · SN2-3 gate-proof semantics · SN2-4 three-outcome discipline · SN2-5 bridge-only route documented · SN2-6 methodology discoverable in session
- **Tier 3 (D, locked):** SN3-1 full spec-vs-live conformance walk · SN3-2 database deep probe (bridge) · SN3-3 methodology currency

## 7. Report requirements

The run writes [[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-report.md): verdict line; per-tier
tables (check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md) (run-row
format per [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings filed.

## 8. Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- Agent-healable: suite-file repairs only (config-manager standard);
  everything else developer-run or proposed
- Deny-list (never heal, never touch without the developer's explicit
  per-item approval naming the file): the installed subject skills · PDLF
  step files · the security-global library · the governing ADR (Sealed) ·
  `triage_findings` and its database · Cupcake internals
- Spec-doc corrections → flagged to docs governance, never applied here
- Tier 3 unlock decision asked at the gate, never assumed
- Credentials: variable names only, never printed (`PGPASSWORD` from `.env`
  by the bridge; never read, never copied)