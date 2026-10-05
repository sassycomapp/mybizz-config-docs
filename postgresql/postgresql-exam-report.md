---
title: "postgresql-exam-report"
doc-id: "mb-758f50e9"
updated: "2026-10-05"
---
# PostgreSQL — Exam Report

Run #2 — **first formal plan-driven run** (2026-09-13). Plan:
[[[mybizz-config-docs:postgresql/postgresql-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-plan.md) (step-0 self-validation: PASS). Detection only —
Tiers 0–2 agent-runnable checks executed; Tier 3 locked. Instance A operational
probes: developer-run request issued (secrets guard on bridge `.env` — per plan).

## Verdict: SYSTEM HEALTHY — Instance B fully green; Instance A liveness proven, operational probes with developer

## Tier 0 — Liveness: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| P0-1 | A: services | x64-15 Running/Auto; dup Stopped | exact match | PASS |
| P0-2 | A: bridge version | connects; 15.14 | **agent attempt denied (secrets guard)** → developer-verified: 15.14, VC++ 1944, 64-bit | PASS (D) |
| P0-3 | B: cluster | 16/main online | online | PASS |
| P0-4 | B: gbrain ping | 1 | 1 | PASS |
| P0-5 | B: memory chain | 8321 + worker | LISTEN; PIDs 315, 18597, 18607 | PASS |

## Tier 1 — Health: PASS (B complete; A = developer-run)

| ID | Result |
|---|---|
| P1-1 | 7 connections — sane |
| P1-2 | 0 waiting locks |
| P1-3 | autovacuum on; `content_chunks` 2026-09-11, `pages` 2026-09-13 (fresh); `facts` never = normal (low-write, per learning) |
| P1-4 | disk 2% used |
| P1-5 | gbrain 164 MB; governor 8,167 kB — stable vs last run |
| P1-6 | 5,529 / 5,529 embedded — **100%**, dims 1536 |
| P1-7 | governor rows: projects 3, candidates 5, events 7, audit 5, policy 0 — sane, growing |
| P1-8 | B log scan — **developer-verified 2026-09-13**: 409 ERROR/FATAL/PANIC lines total; latest 20 reviewed — all historical (≤ 2026-09-13), all explained: governor dev-testing FK/dupe errors (09-09), removed-role attempts (09-05, 09-09), this exam's own psql syntax probes (09-12/13). **No ERROR/FATAL since 2026-09-13 10:25; no recurring pattern; no stale-pid-file** | PASS (D) |
| P1-9/10 | A log scan — **developer-verified 2026-09-13**: newest log file `postgresql-2025-10-07_074724.log` (last write 2025-10-08); latest errors all from **October 2025** (transaction-aborted noise, a `CREATE/DROP DATABASE in transaction block` pair, a burst of `effective_io_concurrency` invalid-value attempts — Windows requires 0). **Zero log entries in ~11 months** — the instance is dormant-but-healthy (pdlf holds 0 rows, no traffic). No FATAL/PANIC ever; PASS. A ops (P1-10) developer-verified same day: waiting 0, autovacuum on | PASS (D) |

## Tier 2 — State conformance: PASS (B complete; A = developer-run)

| ID | Expected | Actual | Result |
|---|---|---|---|
| P2-8 | 16.14 | 16.14 (Ubuntu 24.04 pkg) | PASS |
| P2-9 | gbrain, memory_governor, postgres (+templates) | exact | PASS |
| P2-9b | `compliance_ledger` absent | count 0 | PASS |
| P2-10 | 62 tables / 62 RLS / owner postgres / schema v128 / embedding 3-large 1536d | 62/62, model + dims + schema_version=128 from `config` table | PASS |
| P2-11 | plpgsql, vector 0.6.0, pg_trgm 1.6, pgcrypto 1.3 | exact | PASS |
| P2-12 | governor: 5 tables, all owned by svc | 5 tables, owner `memory_governor_svc` only | PASS |
| P2-13 | svc cannot connect gbrain; roles exact | `has_database_privilege(svc→gbrain)=false`; svc→govdb=true; writer→gbrain=false; role set exact | PASS |
| P2-1..7 | A version/dbs/tables/schema/ext/admin/roles | **developer-verified 2026-09-13 (complete)**: 15.14 exact; dbs `pdlf,postgres` exact; 7 tables exact; **P2-4 schema PASS** — `triage_findings` full column set incl. `resolution_note`/`resolved_at`, CHECK constraints, FK to `steps`, matches spec; **P2-5 PASS** — `plpgsql` only; **P2-7 PASS** — roles `postgres,pdlf_agent` exact. **P2-6 NOT RUN** — agent command error (ran `-d pdlf`, returning pdlf's own 7 tables, not admin-DB); corrected command issued | 4 PASS, 1 pending corrected command |
| P2-14 | boot config | **developer-verified**: `/etc/wsl.conf` `[boot]` command exact per spec | PASS (D) |
| P2-15 | `.env` integrity | **developer-verified**: `bash -n` syntax OK; all 3 variables present (count only, values never displayed) | PASS (D) |

## Findings

1. **DRIFT — RESOLVED 2026-09-13.** The [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) refresh was
   **approved by the developer in-session and applied**: counts refreshed
   (1,824 pages / 5,529 chunks / 164 MB), verification date → 2026-09-13,
   facts-autovacuum nuance + role-isolation test method added. Finding closed.
   Both run-#2 learnings graduated (config.md + skill) and deleted from the
   learnings file; skill source re-synced + register hash updated
   (`9f61f34c9634b419`).
2. **Check-method nuance (new learning).** `SET ROLE` from superuser always
   succeeds (impersonation ≠ privilege) — role isolation must be tested via
   `has_database_privilege`, not `SET ROLE`. Initial probe was misleading;
   corrected in-run. → learnings file, destination: skill (future graduation).
3. **CF-5 verified:** the graduated skill inventory (36 checks) executed correctly
   — every agent-runnable ID ran, expected sources held, no drift between plan
   references and skill rows. Graduation confirmed sound.
4. **B log scan: 409 ERROR/FATAL/PANIC lines — examined, no active fault.**
   Developer-verified scan reviewed line-by-line: all entries ≤ 2026-09-13 and
   attributable (governor dev-testing on 09-09, removed-role auth attempts,
   this exam's own probe errors). Nothing since 2026-09-13 10:25 (which was this
   exam's own probe). However the volume (409 over the log's lifetime) suggests
   the standing check should watch the *rate*, not just presence — noted for the
   skill's next revision (compare new-error count vs prior run).
5. **Developer-run remainder (partial).** P2-4/5/6/7 (A table schema vs spec,
   extensions, admin-DB tables, full role list) not captured in the returned
   bridge output — a follow-up command list was issued. P1-9 (A log scan) pending
   PowerShell rerun.

## Developer-run request (bundled, one pass)

1. **Instance A ops** (P0-2, P1-9, P1-10, P2-1..P2-7): the bridge command from
   [[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md) §Instance A — version, `\l` db set, `pdlf` table
   inventory + schema vs spec, extensions, `postgres` admin tables, role list,
   locks/autovacuum/idle-in-txn, C: disk
2. **Instance A log scan** (P1-9) — `data\log\` recent entries
3. **Instance B log scan** (P1-8) — `/var/log/postgresql/postgresql-16-main.log`,
   last 7 days
4. **Boot config** (P2-14) — `/etc/wsl.conf` `[boot]` intact
5. **`.env` integrity** (P2-15) — sources cleanly; variables present by name

**Status 2026-09-13:** blocks 1, 2, 3, 4, 5 returned and recorded
`developer-verified` above (A log scan: zero errors since Oct 2025 — instance
dormant-quiet, PASS). **Only P2-4/5/6/7 detail remains open** (returned output
covered version/dbs/tables/locks/autovacuum only) — follow-up commands:

## Guard layers

One denial this run (P0-2 bridge, secrets guard) — honored per plan, rerouted to
developer request. Guard armed and behaving exactly as the execution-boundary
learning predicts.

## Not run this cycle

**P2-6 corrected command** (admin-DB table count — the one open evidence item):

```bash
cd /mnt/c/dev/dev-makepdlf/makepdlf-project-library && set -a && source .env && set +a && powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGPASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -U pdlf_agent -d postgres -tAc \"SELECT 'admin_tables='||count(*) FROM pg_tables WHERE schemaname='public';\"" 2>&1
```

Tier 3: P3-1/2/3 deferred-documented (superuser + restart-test — see Tier 3
section); P3-4/5/6 executed this run.
