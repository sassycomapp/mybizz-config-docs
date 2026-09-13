---
name: mb-config-memory-governor
description: Memory-governor configuration exam — verifies the live governor system (API + worker processes, HTTP auth-gate, repo integrity, decision-engine conformance) against memory-governor-config.md, catches silent failures, proposes gated repairs. Use when asked to "exam memory governor", "check governor health", or as part of a full mb-config-manager run.
---

# mb-config-memory-governor — Exam Skill

Exams the live memory-governor system against its spec. This skill holds the
**procedure** only — expected values live in the spec doc and are read fresh at
the start of every run.

- Spec: `memory-governor/memory-governor-config.md` — read it first, every run
- Reference: `memory-governor/memory-governor-reference.md`
- Report: `memory-governor/memory-governor-exam-report.md` — one file, overwritten each run
- Log: `memory-governor/memory-governor-log.md` — one run row per exam; event rows between runs
- Learnings: `memory-governor/memory-governor-learnings.md` — transient; delete on graduation

## Scope boundary (anti-duplication)

- This module exams **the governor application**: processes, HTTP surface, repo,
  decision-engine conformance, register integrity.
- **Database-level checks** (5 tables, ownership, row counts) belong to
  `mb-config-postgresql` — cross-reference its current report; a quick row-count
  sanity check is permitted here, full DB conformance is not.
- **The backup convention** for the governor database lives in
  `postgresql-config.md` §Backups (estate-wide) — freshness checked there (P1-11).

## Hard behavioral rules (from the spec's own Do-not list)

- **Never hand-edit `registers/` or the database** — the worker and API are the
  only writers. Exam = read-only.
- **Never call `gbrain sync` to move governed content** — only `remember` via the
  governor's async path is governed.
- Do not assume test fixtures are shared across test files.
- Do not treat parked phases (13.4/16.2/16.3) as failed builds — deliberately
  parked infrastructure.

## Tier 0 — Liveness (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| M0-1 | A | API process: `pgrep -af "uvicorn app.main"` | One process, command matches the documented form (`uvicorn app.main:app --host 127.0.0.1 --port 8321`) |
| M0-2 | A | Worker process: `pgrep -af "app.worker"` | One process (`python -m app.worker`) |
| M0-3 | A | Port 8321 listening (`ss -tln \| grep 8321`) | LISTEN on 127.0.0.1:8321 |
| M0-4 | A | HTTP auth-gate live: unauthenticated `curl` to `http://127.0.0.1:8321/memory` records the status code | **422** (auth-gates unauthenticated calls — config-documented live observation); any 200 = the auth gate is silently open → `UNHEALTHY` |

## Tier 1 — Health

| ID | Runner | Check | Expected |
|---|---|---|---|
| M1-1 | A | Repo integrity at `/home/dev-p/memory-governor`: `git status --short` | Only expected dirt: `registers/` changes (worker auto-commits+pushes) — anything else uncommitted = finding |
| M1-2 | A | Venv present: `.venv/bin/python` | Exists, executable |
| M1-3 | A | DB quick sanity (single count query via the postgres module's established connection pattern) | 5 tables; row counts sane vs last recorded (projects 3, candidates 5, events 7, audit 5, policy 0 at 2026-09-13) |
| M1-4 | A | Register integrity: index rows in `registers/register-memory-governor.md` ↔ payload files in `registers/candidates/*.json` | 1:1 correspondence (read-only) |
| M1-5 | A | Log/error scan: application logs at `/tmp/memory-governor.log` + `/tmp/memory-governor-worker.log` — **the worker log carries no timestamps and retry warnings show only "attempt 1/5" with no resolution lines** (run #1 finding): failed-event fate requires developer verification via DB event status + worker PATH check. **Outbox semantics (run #1):** events absent from `memory_events` + `unprocessed=0` = delivered-and-purged (the outbox deletes on delivery) — absence is NOT loss; per-source attribution of old IDs requires comparing against the sequence | No unexpected errors; governor dev-testing errors (2026-09-09) are historical |

## Tier 2 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| M2-1 | A | Version | `0.1.0` (pyproject) |
| M2-2 | A | Two-outcome decision model | `auto_promote` / `needs_review` in source; no third automatic outcome |
| M2-3 | A | `HIGH_RISK_TYPES` | exactly five: policy, credential, identity, architecture, security |
| M2-4 | A | Decision thresholds | bootstrap defaults 0.65 (review) / 0.85 (auto-promote); policy changes are data changes |
| M2-5 | A | API surface | 12 routes in source (grep route decorators); NUL-byte global guard present |
| M2-6 | A | systemd user units | **not installed** (spec: permanent auto-start pending developer execution) — if found installed, that is spec drift/progress → flag |
| M2-7 | D | Credentialed registry/review-queue check (closes the governor-side `owning_project` verification — spec pending item 2) | as spec |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| M3-1 | D | Full test suite | **304 passed, 0 failed** (spec-verified 2026-09-08) |
| M3-2 | D | Permanent auto-start execution: systemd migration + two service units (spec pending item 4) | system becomes restart-independent |
| M3-3 | D | Recovery drill (isolated or full-system, per spec's proven procedures) | passes |
| M3-4 | D | Governor repo commit+push of resolution changes (spec pending item 3) | clean |

## Report

Write `memory-governor-exam-report.md`: verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair;
runner attribution for every deferred item (guard-forbidden vs unlock-gated vs
pending-developer-execution); overwritten in full each run (write-then-replace).
Then: one run row appended to `memory-governor-log.md`; new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — the governor is a governed memory system; the
  worker/API are the only writers; every repair is developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list: `registers/` and the database (never edited by the exam) · the
  `.env` (secrets guard — referenced by name only) · service starts/stops (the
  start script is idempotent and self-healing; restarts are event-triggered
  developer decisions) · any `gbrain sync` of governed content