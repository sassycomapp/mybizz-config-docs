---
document: "PostgreSQL — Exam Report"
doc-id: postgresql-exam-report
state: Live
date-created: 2026-09-12
---

# PostgreSQL — Exam Report

First verification run of the `mb-config-postgresql` pilot (2026-09-12).
Detection only — Tier 0–2, both instances. Tier 3 not unlocked. Spec:
`postgresql-config.md` (last verified live 2026-09-09).

## Verdict: SYSTEM HEALTHY — no DOWN, no UNHEALTHY. Two doc-drift findings.

## Tier 0 — Liveness: PASS (both instances)

| Check | Expected (spec) | Actual | Result |
|---|---|---|---|
| A: `postgresql-x64-15` | Running, Automatic | Running, Automatic | PASS |
| A: dead duplicate `PostgreSQL` | Stopped, not started | Stopped, Automatic | PASS |
| A: bridge query `pdlf` | connects, responds | 15.14 returned | PASS |
| B: cluster `16/main` | online | online | PASS |
| B: psql ping `gbrain` | 1 | 1 | PASS |
| B: port 8321 + worker | listening + alive | LISTEN; PIDs 315, 3101 | PASS |

## Tier 1 — Health: PASS

| Check | Result |
|---|---|
| B: waiting locks | 0 |
| B: connections | 7 — sane |
| B: embedding coverage | 5,529 / 5,529 — **100%** |
| B: disk | 2% used on data-disk volume |
| B: `gbrain` size | 164 MB (spec: 148 MB — see finding 1) |
| B: `memory_governor` | 5 tables present, sane |
| B: autovacuum (completed same-day follow-up) | `on`; last_autovacuum recent on `content_chunks` (2026-09-11) and `pages` (2026-09-12); `facts` never (low-write table — not pathological) | PASS |
| B: idle-in-transaction | 0 | PASS |

## Tier 2 — State conformance: PASS with drift

| Check | Expected (spec) | Actual | Result |
|---|---|---|---|
| A version | 15.14, VC++ 1944 | 15.14, VC++ 1944 | PASS |
| A databases | pdlf, postgres | pdlf, postgres | PASS |
| A `pdlf` tables | 7 exact | bft_records, deviations, gates, isc, projects, steps, triage_findings | PASS |
| B databases | gbrain, memory_governor, postgres (+templates) | exact match | PASS |
| B `compliance_ledger` | absent | absent | PASS |
| B login roles | postgres, memory_governor_svc, ledger_writer, ledger_approver | exact match | PASS |
| B gbrain tables / RLS | 62 / 62 | 62 / 62 | PASS |
| B extensions | plpgsql, vector 0.6.0, pg_trgm 1.6, pgcrypto 1.3 | exact match | PASS |
| B governor tables | 5, owned by memory_governor_svc | audit_log, memory_candidates, memory_events, policy_versions, projects | PASS |
| B pages | 1,759 (spec) | 1,824 live | DRIFT |
| B chunks | 5,443 (spec) | 5,529 live | DRIFT |
| B boot config | wsl.conf [boot] intact | not checked — see finding 2 | DEFERRED |
| B log scan | no ERROR/FATAL/PANIC | not run — see finding 2 | DEFERRED |

## Findings

1. **DRIFT — spec counts stale.** Live `pages` 1,824 vs spec 1,759; `chunks` 5,529 vs
   5,443; `gbrain` 164 MB vs 148 MB. Direction = growth, not regression; coverage
   still 100%. Recommended repair: refresh counts + verification date in
   `postgresql-config.md` → **docs governance** (flagged, not applied here).
2. **Agent execution boundary confirmed.** Log scan and `/etc/wsl.conf` reads are
   policy-blocked for agent execution (critical-path policy — the denial is the
   guard working). Skill updated same-day: these two checks are developer-run
   items. Not a system fault.

## Guard layers

Cupcake blocked a bundled probe command mid-exam (critical-path policy) — expected
behavior, recorded as verified for the guard-layers-armed invariant.

## Not run this cycle

Tier 3 (not unlocked). Instance A operational probes (locks, autovacuum,
idle-in-txn, disk, log scan): **developer-run** — the bridge `.env` sourcing is now
guard-blocked for agent execution (secrets rule); hand the developer:
`pg_locks WHERE NOT granted` count, `SHOW autovacuum`, idle-in-txn count, C: free
space, log scan. `.env` re-verification beyond the earlier same-day bridge run
(which succeeded and sourced cleanly — implicit pass at that time).