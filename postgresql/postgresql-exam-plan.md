---
document: "PostgreSQL — Exam Plan"
doc-id: postgresql-exam-plan
state: Live
date-created: 2026-09-12
---

# PostgreSQL — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[postgresql-config|Configuration]] (spec), the last [[postgresql-exam-report|Exam Report]],
[[postgresql-log|Log]] (events since last run), [[postgresql-learnings|Learnings]]. Consumed by
the skill at run time; rewritten at the start of the following cycle. The file is
live; its contents are transient.

The standing check inventory (P0-1…P3-6) **lives in the installed skill** — it
graduated there 2026-09-12. This plan carries run-specifics only (see §6). This
edition is the first hand-written plan and the format template.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #2 — **first formal plan-driven run** |
| Run date | 2026-09-13 |
| Prior report | [[postgresql-exam-report|Exam Report]] (2026-09-12, detection-only pilot) |
| Step-0 result | PASS (3/3 hash pairs match; suite files present; spec doc exists; no open run) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) Instance A log scan; (b) Instance A operational probes via bridge (`.env` sourcing is agent-forbidden); (c) Instance B log scan (system path — agent-forbidden); (d) boot-config check `/etc/wsl.conf` (system path — agent-forbidden); (e) `.env` integrity check (secrets guard); (f) `pg_hba` posture checks — only if Tier 3 unlocked |
| Expected-value source of truth | [[postgresql-config|Configuration]] — read fresh at run start; never rely on remembered values |

## 2. Carried-forward items (from last report)

| # | Item | Why deferred | This run's action |
|---|---|---|---|
| CF-1 | Instance A log scan | agent-forbidden (secrets guard on bridge `.env` sourcing) | Request developer run; record result |
| CF-2 | Instance A locks / autovacuum / idle-in-txn / disk | agent-forbidden (same guard) | Bundle into the same developer request |
| CF-3 | Tier 3 full pass | unlock not given | List as available; execute only on unlock |
| CF-4 | Findings 1 (spec counts stale: pages/chunks/size) | docs-governance flag | Verify whether governance approved + applied the refresh; if applied, re-probe counts and re-compare |
| CF-5 | Graduated check inventory (P0-1…P3-6 now lives in the skill) | graduation 2026-09-12 | Verify the skill's inventory executes correctly; report any drift between plan references and skill rows |

## 3. Erred last run (distinct from deferred)

| # | What erred | This run's action |
|---|---|---|
| ER-1 | Bundled probe command killed whole batch (critical-path guard) | Batch rule: psql probes one batch; system-path reads never bundled; split isolated |
| ER-2 | Instance A bridge probe passed then blocked same day (nondeterministic guard posture) | Treat class as unreliable; P0-2 carries the denial fallback; on denial hand to developer |

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-12 development-period guard denials recorded | Confirm guard classes still armed (implicitly proven by any denial this run) |
| LG-2 | No crashes/incidents logged for either instance | No specific check; if a new log row exists at synthesis time, derive a targeted probe from it |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | `facts` table never autovacuumed (low-write) | Repeat last_autovacuum probe; flag only if a *hot* table also stops vacuuming |

## 6. Standing checks

The complete, authoritative check inventory — **P0-1…P3-6, with runner (A=agent /
D=developer), probe, and pass rule per check — lives in the installed skill**
(`mb-config-postgresql/SKILL.md`, Tiers 0–3). It graduated there 2026-09-12; this
plan no longer duplicates it. Expected values for every check come from
[[postgresql-config|Configuration]], read fresh at run start. This section carries only
run-specific deltas to that inventory — this run: none.

## 7. Report requirements

The run writes [[postgresql-exam-report|Exam Report]]: verdict line; per-tier tables (check
ID, expected, actual, result); findings with class + evidence + recommended repair
+ rollback; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run. Then: one run row appended to
[[postgresql-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]); new
learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + rollback + risk
- Allowlist repairs (gate-gated): `.env` line-quoting fix (pattern per reference);
  documented real-service start; memory-system worker restart
- Flagged, never healed: spec-doc corrections (docs governance)
- Deny-list (never heal, proposal only): `pg_hba` edits, role/database drops,
  service deletion, dead-duplicate start, `wsl.conf`/boot edits, superuser-requiring
  operations, any data mutation
- Credentials: variable names only, never printed
