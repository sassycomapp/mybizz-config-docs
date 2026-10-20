---
title: "postgresql-config"
doc-id: "mb-a8b414df"
updated: "2026-10-20"
---
# PostgreSQL — Configuration

Settings sheet for every PostgreSQL instance on this machine. Commands and
procedures: [[[mybizz-config-docs:postgresql/postgresql-reference|Reference]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md). What the system is and why:
[[[mybizz-config-docs:postgresql/postgresql-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-explainer.md).

## Identity

| Field | Value |
|---|---|
| Issuer | PostgreSQL Global Development Group (WSL instance via the Ubuntu archive package; Windows instance via the EDB installer) |
| Installed version | WSL: 16.15 / Windows: 15.14 |
| Standard taken from | PostgreSQL 16.15 (WSL instance) and PostgreSQL 15.14 (Windows instance) |
| Last researched | 2026-10-20 |

## Estate census

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| PostgreSQL installations | — | Two, entirely separate: Instance A (Windows) and Instance B (WSL) | — | — |
| WSL installations | — | One: `Ubuntu` (the default). Every WSL command names it explicitly (`wsl -d Ubuntu ...`) | — | — |
| Windows services | — | One: `postgresql-x64-15` | — | — |
| Windows registry product keys | — | One: `postgresql-x64-15` | — | — |
| Port listeners (543x range) | [Default port 5432](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-PORT) | Windows 5432 = WSL's localhost relay to Instance B; Windows 5433 = Instance A; WSL 5432 = Instance B; no other listeners | [Default port](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-PORT) | L1 |

## Instance A — Windows, the PDLF ledger

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Version | — | 15.14, compiled by Visual C++ build 1944, 64-bit | — | — |
| Install path | — | `C:\Program Files\PostgreSQL\15\` | [EDB installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) | — |
| Data directory | — | `C:\Program Files\PostgreSQL\15\data` | — | — |
| Port | [5432](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-PORT) | `5433` | [Port default](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-PORT) | L1 |
| `listen_addresses` | [localhost](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-LISTEN-ADDRESSES) | `localhost` | [listen_addresses default](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-LISTEN-ADDRESSES) | — |
| `pg_hba.conf` | — (contents are deployment-specific) | Local rules only; readable by superuser only — verification requires superuser access | — | — |
| `password_encryption` | [scram-sha-256](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION) | `scram-sha-256` | [password_encryption default](https://www.postgresql.org/docs/15/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION) | — |
| `logging_collector` | [off](https://www.postgresql.org/docs/15/runtime-config-logging.html#GUC-LOGGING-COLLECTOR) | `off` — Instance A writes no log files; faults surface via SCM/Event Viewer and probe errors; `SHOW log_directory` is superuser-only | [logging_collector default](https://www.postgresql.org/docs/15/runtime-config-logging.html#GUC-LOGGING-COLLECTOR) | — |
| Service | — | `postgresql-x64-15`, StartType: Automatic, Running | — | — |
| Bridge binary | — | `C:\Program Files\PostgreSQL\15\bin\psql.exe` | — | — |
| Backup output | — | `pg_dump.exe` writes Instance A dumps directly to `C:\backup-gbrain\` on port 5433 | — | — |
| Serves | — | PDLF — the `pdlf` build ledger. Schema contract: [[[pdlf:pdlf-library/specifications-local/spec-postgres-ledger\|Spec: Postgres Ledger]]](C:/pdlf/pdlf-library/specifications-local/spec-postgres-ledger.md) | — | — |
| PDLF project `.env` | — | Sources cleanly; Windows-path values are quoted; carries `PGPORT=5433`; `PSQL_WIN_PATH` has zero consumers, kept for future use | — | — |

### Instance A roles

| Role | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `postgres` | — | Superuser. Credential held as `PGADMIN_USER`/`PGADMIN_PASSWORD` in `C:\pdlf\.env` (referenced by variable name only — never printed) | — | — |
| `pdlf_agent` | — | Owns the `pdlf` database. Password held as `PGPASSWORD` in the same `.env` | — | — |
| `pgvector_user` / `pgvector_readonly` | — | Absent. Reappearance is a finding | — | — |

### Instance A databases

| Database | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `pdlf` | — | Owner `pdlf_agent`; 7,893 kB; seven tables in schema `public`, all owned by `pdlf_agent`, all holding 0 rows (the ledger fills when PDLF runs a real project); extensions: `plpgsql` only. Tables: `projects`, `steps`, `gates`, `deviations`, `bft_records`, `isc`, `triage_findings`. Column-level detail: [[[pdlf:pdlf-library/specifications-local/spec-postgres-ledger\|Spec: Postgres Ledger]]](C:/pdlf/pdlf-library/specifications-local/spec-postgres-ledger.md) | — | — |
| `postgres` (admin) | — | Owner `postgres`; 8,469 kB; PostgreSQL's own catalogs only — no user tables, no `vecs` schema. Baseline backup: `postgres_admin_backup_2026-09-05.dump` (194,019 bytes, `C:\Users\dev-p\`) | — | — |
| `template0` / `template1` | Standard system databases | Owner `postgres`; ~7,297 kB each; `template0` is not connectable (`datallowconn = false`) | — | — |

## Instance B — WSL, the memory-system host

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Version | — | 16.15 (Ubuntu 24.04 package) | — | — |
| Cluster | — | `16/main`, online | `man pg_lsclusters` | — |
| Port | [5432](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-PORT) | `5432` | [Port default](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-PORT) | — |
| `listen_addresses` | [localhost](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-LISTEN-ADDRESSES) | `localhost` — loopback only | [listen_addresses default](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-LISTEN-ADDRESSES) | — |
| Data directory | Ubuntu cluster convention | `/var/lib/postgresql/16/main` | `man pg_lsclusters` | — |
| Config directory | Ubuntu convention: `/etc/postgresql/<version>/<cluster>/` | `/etc/postgresql/16/main/` — `postgresql.conf`, `pg_hba.conf`, `pg_ident.conf`, `start.conf`, `conf.d/`, `environment`. `pg_hba.conf` is root/postgres-owned, not readable by `dev-p` | `man pg_lsclusters` | — |
| Log file | — | `/var/log/postgresql/postgresql-16-main.log` | — | — |
| `password_encryption` | [scram-sha-256](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION) | `scram-sha-256` | [password_encryption default](https://www.postgresql.org/docs/16/runtime-config-connection.html#GUC-PASSWORD-ENCRYPTION) | — |
| `autovacuum` | [on](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM) | `on`, cluster-wide | [autovacuum default](https://www.postgresql.org/docs/16/runtime-config-autovacuum.html#GUC-AUTOVACUUM) | — |
| Row-level security (`gbrain`) | — (the issuer mandates no coverage; the feature is opt-in per table) | Enabled on every table in `gbrain` | [Row security](https://www.postgresql.org/docs/16/ddl-rowsecurity.html) | — |
| `systemd` | — | PID 1 in WSL. `/etc/wsl.conf` sets `systemd=true` and carries no `[boot]` command: `postgresql.service` (enabled) owns the cluster, the two governor user units own the memory processes; `start-memory-system.sh` stays on disk as a manual fallback only | — | — |
| Management tooling | — | `systemctl` and `service` both manage PostgreSQL; `pg_ctlcluster` is the cluster-level start/stop tool | — | — |
| Memory governor units | — | `memory-governor-api` and `memory-governor-worker` (systemd user units, active) | [[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) | — |
| Connection string (`gbrain`) | — | `postgresql://postgres:<password>@localhost:5432/gbrain` — the password lives only in `~/.gbrain/config.json` (`database_url`) and `~/.pgpass`; referenced by variable name in every command | — | — |
| Connection string (`memory_governor`) | — | Held in the governor's own `.env` as `MEMORY_GOVERNOR_DATABASE_URL` (referenced by name only) | — | — |
| Serves | — | GBrain (`gbrain`) and the memory governor (`memory_governor`). GBrain's own facts (version, reranker, embedding model) live in [[[mybizz-config-docs:gbrain/gbrain-config\|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md); governor facts in [[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) | — | — |

### Instance B roles

| Role | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `postgres` | — | Owns `gbrain` and every table in it. Password held only in `~/.pgpass` and `~/.gbrain/config.json` (`database_url`) — never quoted in documents | — | — |
| `memory_governor_svc` | — | Owns `memory_governor` (all five tables). Scoped — cannot connect to `gbrain`. Password in the governor's own `.env` (`MEMORY_GOVERNOR_DATABASE_URL`) | — | — |
| `ledger_writer` / `ledger_approver` | — | Login-capable test roles from the memory governor's own RLS live-testing, cited as the verified precedent in [[[default:security-global/infrastructure/sec-database-access-control\|Database Access Control]]](C:/dev/project-library-global/security-global/infrastructure/sec-database-access-control.md). Own nothing — `gbrain`'s tables are all owned by `postgres` | — | — |

### Instance B databases

| Database | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `gbrain` | — | Owner `postgres`; 263 MB; GBrain's memory/vector store; every table has row-level security enabled; all tables owned by `postgres`. Extensions: `plpgsql` 1.0, `vector` 0.6.0, `pg_trgm` 1.6, `pgcrypto` 1.3. Page and chunk counts are read live with the commands in [[[mybizz-config-docs:postgresql/postgresql-reference\|Reference]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md), never recorded here — they move with every sync | [pgvector](https://github.com/pgvector/pgvector); [supplied extensions](https://www.postgresql.org/docs/16/contrib.html) | — |
| `memory_governor` | — | Owner `memory_governor_svc`; 8,359 kB; five tables, all owned by `memory_governor_svc`: `projects`, `memory_candidates`, `policy_versions`, `memory_events`, `audit_log`. Detail: [[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) | — | — |
| `postgres` (admin) | — | Owner `postgres`; 7,503 kB; standard | — | — |
| `template0` / `template1` | Standard system databases | Owner `postgres`; ~7.3–7.6 MB each; unmodified | — | — |
| `compliance_ledger` | — | Absent. Reappearance is a finding — it means something is recreating it. Baseline backup: `compliance_ledger_backup_2026-09-05.dump` (6,149 bytes, `/home/dev-p/`) | — | — |

## Backups (estate-wide)

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Locations | — | `/home/dev-p/backup-gbrain/` (default — same host as Instance B); `/mnt/c/backup-gbrain/` (security net — survives a full WSL reinstall; also Instance A's direct dump target, since Windows `pg_dump.exe` writes there natively) | — | — |
| Coverage | — | Every data-bearing database on both instances, always: Instance A `pdlf` + `postgres` (admin); Instance B `gbrain` + `memory_governor` + `postgres` (admin). Templates excluded — standard system objects, rebuildable from the install; `template0` is not connectable and cannot be dumped normally | — | — |
| Format | — | `pg_dump -Fc` (custom, compressed); one file per database (pg_dump is per-database by design). Naming: `<db>-db-backup-YYYY-MM-DD.dump`, admin databases disambiguated `-a-`/`-b-` by instance | — | — |
| Cadence | — | Weekly: Task Scheduler task `SundayBackup` runs `C:\mybizz\scripts\sunday-backup.sh` every Sunday at 10:00; a missed start is not caught up; a missed or failed run is reported at the next logon. An extra cycle always runs before upgrades, schema changes or destructive operations | — | — |
| Retention | — | The two most recent verified cycles in each location; older dumps are deleted at the cycle that supersedes them | — | — |
| Pair rule | — | Dump once, copy to both locations immediately, hash-verify (`cmp`/sha256). A mismatched pair means re-dump and re-copy both sides — never copy one way twice | — | — |
| Cycle record | — | The Sunday task reports the result in a pop-up and writes a log to `C:\mybizz\logs\sunday-backup\`; the latest log is the record of the latest cycle | — | — |
| Windows credential source | — | The task reads `%APPDATA%\postgresql\pgpass.conf` for Instance A dumps; `pgpass.conf` exists on Windows | — | — |
| Markdown export lane | — | `gbrain export --dir /mnt/c/backup-dream-cycle/` runs in the same Sunday task, after the DB dumps. Second line of defense for DB-only pages; the PostgreSQL dump remains line one | — | — |

## Open items

None.
