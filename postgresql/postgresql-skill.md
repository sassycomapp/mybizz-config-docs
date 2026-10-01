---
title: "postgresql-skill"
doc-id: "mb-ef9195fc"
updated: "2026-10-01"
---
# mb-config-postgresql — Exam Skill

Exams the live PostgreSQL system against its spec. This skill holds the **procedure**
only — expected values live in the spec doc and are read fresh at the start of every
run. Never rely on remembered values.

- Spec: [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) — read it first, every run
- **Exam plan: [[[mybizz-config-docs:postgresql/postgresql-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-plan.md) — read second, every run.** The
  plan-driven cycle: the config-manager synthesizes this plan fresh before each run
  (from spec + last report + log + learnings) and this skill executes it in hand.
  The plan carries run-specifics and deltas; the **standing check inventory lives
  in this skill** (below) — permanent occurrences graduate here, never into plans
- Reference (connection patterns, pitfalls): [[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md)
- Report: [[[mybizz-config-docs:postgresql/postgresql-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-report.md) — one file, overwritten each run
- Log: [[[mybizz-config-docs:postgresql/postgresql-log|Log]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-log.md) — append one run row (date, verdict,
  findings, disposition) after every run; free rows for notable events witnessed
  between runs
- Learnings: [[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md) — file new patterns/nuances;
  delete entries once graduated into a permanent home

## Instance map — never confuse them

- **Instance A** — Windows PostgreSQL 15, the `pdlf` ledger. Reachable **only** via the
  PowerShell bridge (see reference doc). A direct WSL `psql` to `localhost:5432` hits
  Instance B silently — this is the system's most dangerous pitfall.
- **Instance B** — WSL PostgreSQL 16, hosts `gbrain` + `memory_governor`. Direct `psql`
  from WSL.

## Tier 0 — Liveness (run first; any failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| P0-1 | A | `Get-Service -Name '*postgresql*'` (PowerShell) | `postgresql-x64-15` Running/Automatic; dead duplicate `PostgreSQL` Stopped |
| P0-2 | A | Bridge `SELECT version();` as `pdlf_agent` on `pdlf` | Connects; version matches spec. The bridge sources `.env`, which the secrets guard has blocked for agents (the same command form passed and was blocked the same day, 2026-09-12 — treat as unreliable). If denied: no retry, no workaround — hand to the developer request; P0-1 still proves Instance A liveness |
| P0-3 | A | `pg_lsclusters` | `16 main 5432 online` |
| P0-4 | A | `psql ... -tAc "SELECT 1;"` on `gbrain` | Returns 1 |
| P0-5 | A | `ss -tln \| grep 8321` + `pgrep -f app.worker` | Port listening; worker PID present |

## Tier 1 — Health (operational probes)

Batch rule: psql probes run as one batch; never bundle system-path reads
(`/etc/...`, `/var/log/...`) into a probe command — the Cupcake critical-path
policy blocks them, and the block kills the whole bundled command.

**Instance A execution boundary (graduated 2026-09-12):** the bridge requires
`.env` sourcing, which the secrets guard blocks for agent execution — so **all
Instance A operational probes are developer-run**. Bundle them into the run's one
developer request; never source `.env` as agent; never construct a workaround.

| ID | Runner | Check | Expected |
|---|---|---|---|
| P1-1 | A | B: `pg_stat_activity` connection count | Sane; no stale idle-in-transaction |
| P1-2 | A | B: `pg_locks WHERE NOT granted` | 0 waiting |
| P1-3 | A | B: `SHOW autovacuum` + last_autovacuum on hot tables | `on`; recent on `content_chunks`/`pages` (`facts` never = normal, low-write) |
| P1-4 | A | B: disk free on data volume | Adequate (>20%) |
| P1-5 | A | B: `gbrain` + `memory_governor` sizes vs spec | Sane vs baseline; growth explainable |
| P1-6 | A | B: embedding coverage — independent count | 100% of `content_chunks` (never trust `gbrain doctor` alone) |
| P1-7 | A | B: governor table row-count sanity | 5 tables; counts sane; `audit_log` growing not exploding |
| P1-11 | A | **DB backup freshness — estate-wide** (developer default 2026-09-13: all 5 data-bearing DBs across both instances, weekly cycle, exam-enforced): newest `<db>-db-backup-*.dump` per database in `/home/dev-p/backup-gbrain/` covers `pdlf`, `postgres-a`, `gbrain`, `memory_governor`, `postgres-b`, dated ≤ 7 days; matching copies exist in `/mnt/c/backup-gbrain/` (hash pairs verified). Older than 7 days = finding that forces a fresh cycle (Instance-B dumps agent-runnable; Instance-A dumps via bridge = developer-run) | All 5 fresh ≤7 days; 5/5 hash pairs match |
| P1-8 | D | B: log scan, last 7 days (`/var/log/postgresql/`) | No ERROR/FATAL/PANIC; no recurring stale-pid-file |
| P1-9 | D | A: log scan (`data\log\`) | No ERROR/FATAL/PANIC beyond documented noise |
| P1-10 | D | A: locks / autovacuum / idle-in-txn / C: disk | 0 waiting; autovacuum on; no stale idle-in-txn; disk adequate |

## Tier 2 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| P2-1 | A | A version | 15.14, VC++ 1944, 64-bit |
| P2-2 | A | A database set | exactly `pdlf`, `postgres`, `template0`, `template1` |
| P2-3 | A | `pdlf` table inventory | 7 exact; schema `public`; owner `pdlf_agent` |
| P2-4 | A | `pdlf` schema vs spec | Column match incl. `resolution_note`/`resolved_at` on `triage_findings` (spec file authoritative) |
| P2-5 | A | `pdlf` extensions | `plpgsql` only |
| P2-6 | A | `postgres` admin DB | zero user tables, no `vecs` schema |
| P2-7 | A | A role set | exactly `postgres`, `pdlf_agent` |
| P2-8 | A | B version | 16.14 |
| P2-9 | A | B database set | exactly `gbrain`, `memory_governor`, `postgres` (+templates); `compliance_ledger` absent |
| P2-10 | A | `gbrain` conformance | owner `postgres`; 62 tables; all RLS; schema v128; embedding `openai:text-embedding-3-large` (1536d) |
| P2-11 | A | `gbrain` extensions | plpgsql, vector 0.6.0, pg_trgm 1.6, pgcrypto 1.3 |
| P2-12 | A | `memory_governor` conformance | owner `memory_governor_svc`; 5 tables, all owned by it |
| P2-13 | A | B role set | exactly `postgres`, `memory_governor_svc`, `ledger_writer`, `ledger_approver`; svc cannot connect to `gbrain` — **tested via `has_database_privilege(role, db, 'CONNECT')`, never via `SET ROLE`** (superuser impersonation always succeeds and proves nothing) |
| P2-14 | D | Boot config | `/etc/wsl.conf` `[boot]` command intact |
| P2-15 | D | `.env` integrity | sources cleanly; `PGPASSWORD`, `PGADMIN_USER`, `PGADMIN_PASSWORD` present by name |

Removed items stay removed: `compliance_ledger`, `pgvector_user`,
`pgvector_readonly` confirmed absent — a reappearance is a finding.

## Tier 3 — Deep pass (each executes only if the developer unlocks this tier for the run)

| ID | Runner | Check | Expected |
|---|---|---|---|
| P3-1 | D | Auth posture A: `pg_hba.conf` | scram-sha-256 only, no trust paths |
| P3-2 | D | Auth posture B: file unreadable to `dev-p` as documented | As spec |
| P3-3 | D | Boot durability | `wsl --shutdown` → fresh boot → PostgreSQL + memory chain alive, zero intervention |
| P3-4 | A | No third instance | One Windows product; one WSL cluster; no other 543x listeners |
| P3-5 | A | Guard layers armed | OpenCode deny patterns + Cupcake destructive-SQL rule present (read-only) |
| P3-6 | A | Backups exist + sized | `postgres_admin_backup_2026-09-05.dump` (194,019 B); `compliance_ledger_backup_2026-09-05.dump` (6,149 B) |

## Heal allowlist (gate-gated, one at a time)

- `.env` line quoting fix (the documented bash-source failure pattern)
- Doc value corrections → **flagged to docs governance, not applied here**
- Memory-system worker restart (documented self-healing pattern)
- Service start of the documented real service only

## Deny-list (never heal — diagnosis + proposal only)

`pg_hba.conf` edits · role drops · database drops · service deletion · starting the
dead duplicate · `wsl.conf`/boot edits · anything requiring superuser · any data
mutation. Credentials by variable name only, never printed.

## Report

Write [[[mybizz-config-docs:postgresql/postgresql-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-report.md): tier results (pass/fail per check), findings with
class + evidence + recommended repair + rollback plan, expected-value source (spec
doc section). Overwritten every run.
