---
title: "memory-governor-exam-plan"
doc-id: "mb-24d4eef4"
updated: "2026-10-05"
---
# Memory Governor — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) (spec), the last
[[[mybizz-config-docs:memory-governor/memory-governor-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-exam-report.md), [[[mybizz-config-docs:memory-governor/memory-governor-log|Log]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-log.md), and
[[[mybizz-config-docs:memory-governor/memory-governor-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-learnings.md). Consumed by the skill at run time; rewritten at
the start of the following cycle. The file is live; its contents are transient.

**This first plan is hand-written** (emulation of the PostgreSQL architecture): it
also serves as the format template — the standing-checks section below is the
complete, authoritative enumeration of every check the exam performs. Once
verified by a run, it graduates into the skill, and future plans carry
run-specifics + references instead.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — first-run bootstrap: synthesize from spec alone; missing report/log = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) M2-7 credentialed registry check (needs real credential headers); (b) any check whose command text the guards deny |
| Expected-value source of truth | [[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) — read fresh at run start; never rely on remembered values |
| Scope boundary | DB conformance belongs to `mb-config-postgresql` (cross-reference; quick row counts permitted); backup freshness checked there (P1-11) |

## 2. Carried-forward items

| # | Item | Why deferred | This run's action |
|---|---|---|---|
| CF-1 | Spec pending item 2 — credentialed registry/review-queue check | needs real credential headers | Bundle into the developer request |
| CF-2 | Spec pending item 3 — governor repo commit+push of resolution changes | developer's repo action | Check repo state; report uncommitted changes |
| CF-3 | Spec pending item 4 — permanent auto-start (systemd migration + two units) | developer execution; system currently restart-dependent | Verify units still absent; flag if installed |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-09 governor dev-testing errors in the postgres log (historical) | Confirm no new application errors since |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | Row-count expectations are point-in-time (postgres run #2: projects 3, candidates 5, events 7, audit 5, policy 0) | Compare against last recorded + growth explainability; exact equality never asserted |

## 6. Standing checks — the complete enumeration (Tiers 0-3)

The complete enumeration lives in the skill ([[[mybizz-config-docs:memory-governor/memory-governor-skill|Memory Governor Skill]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-skill.md), Tiers
0–3, M0-1…M3-4 with runners and pass rules); this plan carries run-specifics.
Summary of the standing inventory:

- **Tier 0 (A):** M0-1 API process · M0-2 worker process · M0-3 port 8321 · M0-4 HTTP auth-gate returns 422
- **Tier 1 (A):** M1-1 repo integrity · M1-2 venv · M1-3 DB quick sanity · M1-4 register index↔payload correspondence · M1-5 application error scan
- **Tier 2 (A/D):** M2-1 version 0.1.0 · M2-2 two-outcome model · M2-3 HIGH_RISK_TYPES ×5 · M2-4 thresholds 0.65/0.85 · M2-5 12 routes + NUL guard · M2-6 systemd units absent (pending) · M2-7 (D) credentialed registry check
- **Tier 3 (D, locked):** M3-1 full test suite (304/0) · M3-2 auto-start execution · M3-3 recovery drill · M3-4 repo commit+push

## 7. Report requirements

The run writes [[[mybizz-config-docs:memory-governor/memory-governor-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-exam-report.md): verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence +
recommended repair; runner attribution for every deferred item (guard-forbidden /
unlock-gated / pending-developer-execution); overwritten in full each run
(write-then-replace). Then: one run row appended to [[[mybizz-config-docs:memory-governor/memory-governor-log|Log]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-log.md);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — worker/API are the only writers; every repair is
  developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list: `registers/` and the database (never edited by the exam) · the
  `.env` (secrets guard) · service starts/stops · any `gbrain sync` of governed
  content
- Credentials: variable names only, never printed
