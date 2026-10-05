---
title: "postgresql-exam-report"
doc-id: "mb-758f50e9"
updated: "2026-10-05"
---
# PostgreSQL — Exam Report

Run #3 (2026-10-05) — single-system cycle on explicit developer instruction. Plan:
[[[mybizz-config-docs:postgresql/postgresql-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-plan.md) (step-0: PASS, one estate finding routed to the
config-manager's own doc). Plan-driven detection ran autonomously; the gate decided
every item; approved heals were applied and re-verified the same session. This
report is the current verified state — no history (the gate-era narrative lives in
[[[mybizz-config-docs:postgresql/postgresql-log|Log]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-log.md)).

## Verdict: detection DOWN (Instance A) → final state HEALTHY after gate — Instance A Running on port 5433; Instance B green; backup cycle fresh 5/5

At detection the real Windows service was Stopped (Instance A down since the
2026-10-02 boot) and the backup estate was stale. The gate (all approved):
F-1 repaired (service started, Running verified); **G9: Instance A moved
permanently to port 5433** (developer-executed; cause: WSL's port relay holds
Windows 5432 for Instance B); the fresh backup cycle executed with **5/5 pairs
hash-verified**; the G5 retention rule applied; spec/skill/register refreshed.

## Final verified state (2026-10-05)

### Instance A (Windows, PostgreSQL 15 — port 5433)

| Check | State | Source |
|---|---|---|
| Service `postgresql-x64-15` | Running / Automatic | developer-verified (G1) |
| Listeners | `127.0.0.1:5433` + `[::1]:5433` = postgres.exe (PID 12812); Windows 5432 = wslrelay only (→ Instance B) | developer-verified |
| Version (P0-2/P2-1) | 15.14, VC++ 1944, 64-bit — via `-p 5433` | developer-verified |
| Database set (P2-2) | `pdlf` 7,877 kB · `postgres` 8,425 kB · template0/template1 7,297 kB each | developer-verified |
| Tables (P2-3) | 7 exact, all owner `pdlf_agent`; all row counts 0 | developer-verified |
| Roles (P2-7) | exactly `postgres`, `pdlf_agent` (removed roles absent) | developer-verified |
| Logging | `logging_collector` = off — no log files written; `data\log\` historical only; `log_directory` SHOW correctly superuser-refused | developer-verified |
| Schema/`pdlf`-schema, extensions, admin-DB, locks/autovacuum (P2-4/5/6, P1-10) | **developer-verified 2026-10-05, all PASS**: P2-4 — `triage_findings` full column set incl. `resolution_note`/`resolved_at`, CHECKs on confidence/severity/source_step/triage_label, FK `step_id → steps(id)` — matches spec; P2-5 — `plpgsql` 1.0 only; P2-6 — `admin_tables=0`, `vecs_schema=0` (**the run-#2 carried corrected command — closed**); P1-10 — waiting_locks 0, autovacuum on, idle-in-txn 0 | developer-verified |
| C: disk (P1-10 partial) | 19 GB free of 238 GB (~8%) — below the >20% adequacy threshold; watch | developer-verified |
| Log scan (P1-9) | No-op — no log files while the collector is off | agent-verified via spec fact |

### Instance B (WSL, PostgreSQL 16 — port 5432)

| Check | State | Source |
|---|---|---|
| Cluster (P0-3) | 16/main online, 5432 | agent-verified |
| gbrain ping (P0-4) | 1 (variable-form credential path exercised) | agent-verified |
| Memory chain (P0-5) | 8321 LISTEN; worker PID 448 | agent-verified |
| Connections/locks (P1-1/2) | 14 conns sane, 0 idle-in-txn; 0 waiting locks | agent-verified |
| Autovacuum (P1-3) | on; `pages` + `content_chunks` vacuumed today; `facts` never = normal | agent-verified |
| Disk (P1-4) | WSL / 2% used | agent-verified |
| Sizes (P1-5) | gbrain 242 MB; governor 8,359 kB; postgres 7,345 kB — growth explainable | agent-verified |
| Coverage (P1-6) | 7,171 / 7,171 = 100%, dims 1536 | agent-verified |
| Governor rows (P1-7) | 5 / 53 / 0 / 174 / 76 — growing, not exploding | agent-verified |
| Version (P2-8) | 16.15 (matches refreshed spec; unattended-upgrades 2026-09-16) | agent-verified |
| DB set (P2-9) | exact 5; `compliance_ledger` absent | agent-verified |
| gbrain conformance (P2-10) | owner postgres; 93/93 RLS; schema v169; 3-large 1536d; 2,477 pages / 7,171 chunks | agent-verified |
| Extensions (P2-11) | plpgsql 1.0, vector 0.6.0, pg_trgm 1.6, pgcrypto 1.3 | agent-verified |
| Governor conformance (P2-12) | 5 tables, sole owner `memory_governor_svc` | agent-verified |
| Roles + isolation (P2-13) | 4 login roles exact; svc→gbrain false, svc→gov true, writer→gbrain false | agent-verified |
| B log scan + rate watch (P1-8) | not returned — next-plan evidence item | pending |

### Backup estate (P1-11) — fresh cycle executed

**All five pairs hash-verified identical** (`cmp` + sha256): `gbrain` 78,946,270 B ·
`memory_governor` 60,086 B · `postgres-b` 1,093 B · `pdlf` 21,720 B ·
`postgres-a` 5,179 B — in both `/home/dev-p/backup-gbrain/` and `/mnt/c/backup-gbrain/`.
Instance-B dumps agent-run; Instance-A dumps developer-run on port 5433, dumped once
to `C:\backup-gbrain\`, copied to the WSL location, pairs verified. Retention (G5,
approved as a rule): the two most recent verified cycles kept per location
(2026-10-05 full + 2026-09-28 partial); **the five 2026-09-13 dumps were deleted
from both locations — deletion executed by the agent under grant; no commands owed
to the developer.** Windows C: remains at ~8% free (watch; dumps fit comfortably).

### Gate outcome per item (2026-10-05)

| Item | Decision | Result |
|---|---|---|
| G1 | approve | F-1 repaired: service Running; cause = port held by wslrelay at boot; verified |
| G9 | developer decision: permanent port move to 5433 | Applied by developer (`port = 5433` appended to postgresql.conf — no port line existed; rollback artifact `postgresql.conf.pre-5433-2026-10-05` retained; `.env` `PGPORT=5433`); consumers #1–#12 applied and sweep-verified clean |
| G2 | approve | Fresh cycle executed and verified 5/5 |
| G3/G4 + S-1…S-32 | approve, with correction | Spec rewritten to present state (32 rewordings + F-3/F-4 values + port map + logging fact + retention rule); correction honored: removed history dropped, not moved — the Explainer gained present-tense reasons only |
| G5 | approve as rule | Retention rule in spec; 2026-09-13 dumps deleted both locations |
| G6 | approve | No spec change; new dumps follow spec naming; the retained 09-28 file documented as historical spelling |
| G7 | approve | Skill amended (P0-2 `-p 5433`, P1-8 rate watch, P1-9 no-log posture, P2-8 16.15, P2-10 93/v169 point-in-time, P2-14 boot, P2-15 `PGPORT`) and re-installed — pair verified `8ac4c647d0c74aae` both sides (install write was guard-denied for the agent → developer-run; honored) |
| G8 | approve | Register diagnostic column refreshed `ed5cb00b8a3b3a2f`; postgresql column refreshed `8ac4c647d0c74aae` |

### Open items for the next plan

1. P1-8 (B log scan + rate watch), P2-14 (`/etc/wsl.conf` file read), P2-15
   (`.env` integrity) — not returned this run; next-plan evidence items.
2. F-5 watch — C: ~8% free; developer housekeeping decision pending (not an
   allowlist heal).

## Guard layers

Two denials this run, both honored, both resolved in-protocol: (1) the
installed-skill re-install write (Cupcake tool-registration guard) → developer-run
per precedent; (2) one expired grant slip caught by the guard (a write attempted
after the 30-minute expiry) → re-asked and re-issued. The `.env` names-only read
was guard-blocked → routed developer-run as the boundary requires.

## Not run this cycle

Tier 3 (locked): P3-1/2/3 (superuser + boot-durability), P3-4 (full census
re-verification — partially covered by the port-listener checks this run),
P3-5/6 (guard layers; backup artifacts — P3-6's artifacts were implicitly
re-confirmed by the P1-11 full listing). The exam-plan file is transient and is
rewritten at the start of the next cycle.
