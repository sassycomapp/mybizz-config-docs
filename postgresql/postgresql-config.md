---
title: "postgresql-config"
doc-id: "mb-a8b414df"
updated: "2026-10-05"
---
# PostgreSQL — Configuration

Canonical, current-state configuration record for every PostgreSQL instance on
this machine. Pure facts and settings — no narrative, no history, no design
rationale. For the "why," see [[[mybizz-config-docs:postgresql/postgresql-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-explainer.md). For commands and
procedures, see [[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md). Last fully verified live: 2026-10-05.

**Two entirely separate instances exist. Do not confuse them.** The layer
placement: Instance B hosts the pre-makePDLF layer's memory; Instance A
hosts the PDLF layer's ledger (see
[[[pdlf:pdlf-library/pdlf-explainer-docs/pdlf-environment-explainer|the pre-makePDLF, makePDLF, PDLF, and shipped layers]]](C:/pdlf/pdlf-library/pdlf-explainer-docs/pdlf-environment-explainer.md) for the layer map).

**Port map:** 5432 is Instance B from both sides — WSL-native, and on Windows
via WSL's localhost port relay. 5433 is Instance A (Windows). Every Instance A
command carries `-p 5433`; a bare connection to 5432 from either side reaches
Instance B silently.

---

## Instance A — Windows-native PostgreSQL 15 (the PDLF ledger host)

| Item | Value |
|---|---|
| Version | 15.14, compiled by Visual C++ build 1944, 64-bit (verified live 2026-10-05) |
| Install path | `C:\Program Files\PostgreSQL\15\` |
| Data directory | `C:\Program Files\PostgreSQL\15\data` |
| Port | `5433` |
| Host (from Windows) | `127.0.0.1` or `localhost` (equivalent) |
| Reached from WSL via | PowerShell bridge only, always with `-p 5433` — see [[[mybizz-config-docs:postgresql/postgresql-reference\|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md). A bare `psql` to `localhost:5432` connects to Instance B instead, silently — from WSL directly, and from Windows via WSL's port relay (Windows port 5432 belongs to WSL's relay, which is why this instance listens on 5433). |
| Auth method | `scram-sha-256` for all users/addresses, including `0.0.0.0/0` and `::/0`. No trust paths. `pg_hba.conf` is readable only by superuser — verification requires superuser access. |
| Service (real) | `postgresql-x64-15`, StartType: Automatic — expected Running at every exam; status is live-checked each exam (Running, verified 2026-10-05) |
| Service (dead duplicate) | `PostgreSQL` — Status: Stopped, StartType: Automatic. Same data directory as above. Harmless; cannot conflict since only one process can bind the port. Do not start it. |
| Logging | `logging_collector` = off — Instance A writes no log files while it stays off (`data\log\` holds only historical files, newest 2025-10-08). Faults surface via SCM/Event Viewer and probe errors. `SHOW log_directory` is superuser-only. (Verified 2026-10-05.) |
| Binary (for the WSL PowerShell bridge) | `C:\Program Files\PostgreSQL\15\bin\psql.exe` |

### Roles

| Role | Notes |
|---|---|
| `postgres` | Superuser. Credential: `PGADMIN_USER`/`PGADMIN_PASSWORD` in `C:\dev\dev-makepdlf\makepdlf-project-library\.env` (referenced by variable name only — never printed) |
| `pdlf_agent` | Owns the `pdlf` database. Password stored as `PGPASSWORD` in the same `.env` |

Historically removed roles (`pgvector_user`, `pgvector_readonly`) must remain
absent — reappearance is a finding.

### Databases (verified live 2026-10-05)

| Database | Owner | Size | Notes |
|---|---|---|---|
| `pdlf` | `pdlf_agent` | 7,877 kB | The PDLF build ledger. 7 tables, all currently hold 0 rows (verified live 2026-10-05). Extensions: `plpgsql` only |
| `postgres` (admin) | `postgres` | 8,425 kB | Holds no user tables. Baseline backup: `postgres_admin_backup_2026-09-05.dump` (194,019 bytes, `C:\Users\dev-p\`) |
| `template0` / `template1` | `postgres` | ~7,297 kB each | Standard. `template0` is not connectable (`datallowconn = false` — verified live 2026-10-05) |

### `pdlf` — table inventory

`projects`, `steps`, `gates`, `deviations`, `bft_records`, `isc`,
`triage_findings` — all in schema `public`, all owned by `pdlf_agent`. All
seven currently hold 0 rows (verified live 2026-10-05).

The schema documented in
[[[makepdlf-project-library:specifications-local/spec-postgres-ledger|Spec: Postgres Ledger]]](C:/dev/dev-makepdlf/makepdlf-project-library/specifications-local/spec-postgres-ledger.md)
matches the live database; the specification file is authoritative for
column-level detail (including `resolution_note`/`resolved_at` on
`triage_findings`).

### Project `.env` integrity

The project `.env` sources cleanly; Windows-path values are quoted. It carries
`PGPORT=5433` (the ledger's port since the 2026-10-05 port move). `PSQL_WIN_PATH`
has zero consumers — kept for future use.

---

## Instance B — WSL-native PostgreSQL 16 (the memory-system host)

| Item | Value |
|---|---|
| Version | 16.15 (Ubuntu 24.04 package) (verified live 2026-10-05) |
| Cluster name | `main` — status `online` (verified live 2026-10-05) |
| Port | `5432` |
| Host (from WSL) | `localhost` or `127.0.0.1` |
| Data directory | `/var/lib/postgresql/16/main` |
| Config directory | `/etc/postgresql/16/main/` (`postgresql.conf`, `pg_hba.conf`, `pg_ident.conf`, `start.conf`, `conf.d/`, `environment`) — `pg_hba.conf` is root/postgres-owned, not readable by `dev-p` |
| Log file | `/var/log/postgresql/postgresql-16-main.log` |
| Connection string (gbrain DB) | `postgresql://postgres:<password>@localhost:5432/gbrain` — the password lives only in `~/.gbrain/config.json` (`database_url`) and `~/.pgpass`; reference by variable name in every command |
| Connection string (governor DB) | In `memory_governor`'s own `.env` as `MEMORY_GOVERNOR_DATABASE_URL` (referenced by name only) |
| Management tooling | systemd is PID 1; `systemctl` and `service` both work; `pg_ctlcluster` remains the cluster-level start/stop tool. |
| Boot config | `/etc/wsl.conf` carries no `[boot]` command: under systemd, `postgresql.service` (enabled) owns the cluster and the two governor user units own the memory processes; the script remains on disk as a manual fallback only. |
| Autovacuum posture | `on` (cluster-wide). Hot-table recency is the health signal: `content_chunks` and `pages` vacuum within days of writes (recency re-checked each exam). The `facts` table showing `last_autovacuum = never` is **normal** — it is low-write; flag only if a *hot* table stops vacuuming. |

### Role-isolation test method (authoritative)

Role access is tested via `has_database_privilege(role, db, 'CONNECT')` — never
via `SET ROLE` (from a superuser session `SET ROLE` always succeeds; impersonation
proves nothing about the role's own privileges). Expected: `memory_governor_svc`
→ `gbrain` = false; → `memory_governor` = true; `ledger_writer` → `gbrain` = false.

### Roles

| Role | Notes |
|---|---|
| `postgres` | Owns `gbrain`. Password: held only in `~/.pgpass` and `~/.gbrain/config.json` (`database_url`) — never quoted in corpus documents |
| `memory_governor_svc` | Owns `memory_governor` (all 5 tables). Scoped — cannot connect to `gbrain`. Password in `memory_governor`'s own `.env` (`MEMORY_GOVERNOR_DATABASE_URL`). |
| `ledger_writer` / `ledger_approver` | Login-capable test roles from the memory governor's own RLS live-testing — cited as the verified precedent in [[[default:security-global/infrastructure/sec-database-access-control\|Database Access Control]]](C:/dev/project-library-global/security-global/infrastructure/sec-database-access-control.md). Own nothing (`gbrain`'s tables are all owned by `postgres`). |

### Databases (verified live 2026-10-05)

| Database | Owner | Size | Notes |
|---|---|---|---|
| `gbrain` | `postgres` | 242 MB | GBrain's memory/vector store. **2,477 pages, 7,171 chunks, 7,171 embedded (100%)** — point-in-time at exam (grows with every sync; exams check coverage % + growth explainability, never exact equality). 93 tables, all with RLS enabled, all owned by `postgres`. Schema v169, embedding `openai:text-embedding-3-large` (1536d). Extensions: `plpgsql` 1.0, `vector` 0.6.0, `pg_trgm` 1.6, `pgcrypto` 1.3 |
| `memory_governor` | `memory_governor_svc` | 8,359 kB | 5 tables (all owned by `memory_governor_svc`): `projects`, `memory_candidates`, `policy_versions`, `memory_events`, `audit_log`. See [[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md). |
| `postgres` (admin) | `postgres` | 7,345 kB | Standard, unremarkable. |
| `template0` / `template1` | `postgres` | ~7.3–7.6 MB each | Standard, unmodified. |

Removed database `compliance_ledger` must remain absent — reappearance is a
finding. Its baseline backup: `compliance_ledger_backup_2026-09-05.dump`
(6,149 bytes, `/home/dev-p/`).

---

## Instance census: exactly two instances

Windows registry: one PostgreSQL product. Windows services: two registrations,
one data directory. No `Program Files (x86)` install. WSL Ubuntu-24.04: one
cluster. WSL Ubuntu-22.04: no PostgreSQL. Port listeners: Windows 5432 = WSL's
relay (to Instance B), Windows 5433 = Instance A; WSL 5432 = Instance B; no
other listeners in the 543x range on either side. A manually-compiled,
never-registered instance can't be mathematically excluded, but no evidence
of one exists.

## Backups (estate-wide)

| Location | Role | Notes |
|---|---|---|
| `/home/dev-p/backup-gbrain/` | **Default** | WSL-native, same host as Instance B — fastest to produce and restore (name is historical) |
| `/mnt/c/backup-gbrain/` (`C:\backup-gbrain`) | **Security net** | Windows-drive copy — survives a full WSL distro reinstall or loss; also the direct dump target for Instance A (Windows `pg_dump.exe` writes there natively) |

- **Coverage: every data-bearing database on both instances, always** (developer default): Instance A `pdlf` + `postgres` (admin); Instance B `gbrain` + `memory_governor` + `postgres` (admin). **Templates excluded** — standard system objects, rebuildable from the install itself; `template0` is not connectable and cannot be dumped normally.
- Format: `pg_dump -Fc` (custom, compressed); one file per database (pg_dump is per-database by design). Naming: `<db>-db-backup-YYYY-MM-DD.dump`, admin DBs disambiguated `-a-` / `-b-` by instance.
- **Cadence: weekly (7 days), exam-enforced** — every config-management exam checks dump age; older than 7 days = finding that forces a fresh cycle. No cron/scheduler (respects the standing "nothing gbrain-related is scheduled" design decision). Event-triggered extras: always before upgrades, schema changes, or destructive operations.
- **Retention: the two most recent verified cycles in each location; older dumps are deleted at the cycle that supersedes them** (developer decision 2026-10-05).
- **Live-database rule:** never re-dump one side of the pair; dump once, copy to both locations immediately, then hash-verify (`cmp`/sha256). A mismatched pair means re-dump + re-copy both, never copy one way twice.
- Latest completed cycle: 2026-10-05 — all five pairs hash-verified identical: `gbrain` 78,946,270 B · `memory_governor` 60,086 B · `postgres-b` 1,093 B · `pdlf` 21,720 B · `postgres-a` 5,179 B. The prior retained cycle is 2026-09-28 (partial — Instance B only; its governor dump uses the historical `memory-governor-…` hyphen spelling).
- Instance-A dumps are produced by `pg_dump.exe` on Windows (developer-run — the bridge `.env` sourcing is agent-forbidden), written directly to `C:\backup-gbrain\` on port 5433; the agent copies to the WSL location and hash-verifies the pair. Instance-B dumps are agent-runnable.
- **Second lane — markdown export:** dream-synthesized concept pages are DB-only (no backing file); their second line of defense is `gbrain export --dir /mnt/c/backup-dream-cycle/` (`C:\backup-dream-cycle`) — developer-run, weekly, alongside the DB dumps. The PostgreSQL dump remains line one; the export adds file-lane-visible, human-readable recovery for DB-only content.

## Known undocumented items (deliberately retained, each documented)

- The dead duplicate `PostgreSQL` Windows service — cosmetic only, left in
  place deliberately. Removing the registration (`sc delete PostgreSQL`)
  is available to the developer if ever wanted.
- `pg_hba.conf` content on Instance B — root/postgres-owned, not readable
  by `dev-p`; the scram posture verification requires superuser access
  (`pg_hba.conf` is not readable by `dev-p`).
