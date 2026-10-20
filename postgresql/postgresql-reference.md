---
title: "postgresql-reference"
doc-id: "mb-5bad908d"
updated: "2026-10-20"
---
# PostgreSQL — Reference

Companion to [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) (every setting, path and
value) and [[[mybizz-config-docs:postgresql/postgresql-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-explainer.md) (what the system is and why).
What differs from the issuer standard: [[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md).
This document is agent-facing — how to connect to, query and troubleshoot
each instance safely.

## The one rule that governs every command

Two entirely separate PostgreSQL installations exist, and port 5432 reaches
Instance B from both sides of the WSL boundary. **Every database command
names its instance and its port.** A command meant for the ledger that omits
`-p 5433` reaches Instance B instead, without any error.

---

## Instance A — Windows PostgreSQL 15 (`pdlf` ledger) — port 5433

### Connecting — the only correct method from WSL

WSL's binfmt does not pass Linux environment variables to Windows
executables, so a bridge through PowerShell is required. Never omit
`-p 5433`.

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGPASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -p 5433 -U pdlf_agent -d pdlf -c '<SQL>'"
```

This is the verified working pattern for queries, inserts and role
management.

### Superuser connection (Instance A) — developer-run

The `postgres` superuser credential is held in the same `.env` as
`PGADMIN_USER`/`PGADMIN_PASSWORD` (referenced by variable name only —
never printed). Verification that needs superuser rights — for example
`pg_hba_file_rules` or `SHOW data_directory` — is developer-run; agent
tooling is guard-blocked on the credential file:

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGADMIN_PASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -p 5433 -U postgres -d postgres -c '<SQL>'"
```

**Role management requires `DROP OWNED` first.** A role holding privileges
in a database (e.g. EXECUTE on extension functions) cannot be dropped
until they are revoked — `DROP OWNED BY <role>;` in **each database where
the role holds anything** handles all of it, after which `DROP ROLE`
succeeds. Note: per-database CONNECT via `PUBLIC` needs no revocation — a
role relying on `PUBLIC` connectivity holds no per-database grants.

### Direct Windows PowerShell connection (human-run only)

A developer running commands directly in a Windows PowerShell terminal
(not through OpenCode/WSL) uses the simpler direct form:

```powershell
$env:PGPASSWORD = "<value from .env>"
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -c "<SQL>"
```

**Reading the password without pasting it anywhere:**
```powershell
$envContent = Get-Content "C:\pdlf\.env"
$pgLine = $envContent | Where-Object { $_ -match "^PGPASSWORD=" }
$env:PGPASSWORD = ($pgLine -split "=", 2)[1]
```

### Confirmed pitfalls

- **Do not build a `.sql` file via PowerShell's `Out-File` and pass it with `psql -f`.** `Out-File -Encoding utf8` adds an invisible byte-order-mark that `psql` fails to parse, producing `syntax error at or near "ï»¿ALTER"` on the first statement only. Pass SQL directly via `-c`, or verify the file is BOM-free before using `-f`.
- **`-h localhost` and `-h 127.0.0.1` are equivalent here** — a connection failure with either is a password problem, not an address problem.
- **Quote every Windows path in `.env`.** An unquoted value such as `C:\Program Files\...` is word-split by bash when the file is sourced.
- **An unquoted path in a `.env` breaks bash `source`-ing but not line-by-line parsing** — the OpenCode permission model's bridge pattern parses line-by-line and is unaffected. The distinction matters when choosing a fix.
- **`SHOW log_directory` is superuser-only** — `pdlf_agent` is correctly refused (`pg_read_all_settings` boundary). Instance A's `logging_collector` is off, so no log files are written while it stays off; faults surface via SCM/Event Viewer and probe errors.

### Useful live queries

```powershell
# Server version
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -c "SELECT version();"

# All real databases with sizes
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -c "SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;"

# Full role inventory
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -c "SELECT rolname, rolcanlogin FROM pg_roles ORDER BY rolname;"

# Table inventory
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -c "\dt"

# Row counts across all 7 ledger tables
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -c "SELECT 'projects', count(*) FROM projects UNION ALL SELECT 'steps', count(*) FROM steps UNION ALL SELECT 'gates', count(*) FROM gates UNION ALL SELECT 'deviations', count(*) FROM deviations UNION ALL SELECT 'bft_records', count(*) FROM bft_records UNION ALL SELECT 'isc', count(*) FROM isc UNION ALL SELECT 'triage_findings', count(*) FROM triage_findings;"
```

### Service management (Windows)

```powershell
Get-Service -Name "*postgresql*" | Format-Table Name, Status, StartType
```

`postgresql-x64-15` is the only registration; expect it Running.

### Dumping Instance A (backup cycle, developer-run)

```powershell
& "C:\Program Files\PostgreSQL\15\bin\pg_dump.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -Fc -f "C:\backup-gbrain\pdlf-db-backup-<DATE>.dump"
& "C:\Program Files\PostgreSQL\15\bin\pg_dump.exe" -U postgres -d postgres -h 127.0.0.1 -p 5433 -Fc -f "C:\backup-gbrain\postgres-a-admin-db-backup-<DATE>.dump"
```
Dump once to `C:\backup-gbrain\` (the direct Windows target), then copy to
the WSL location and hash-verify the pair — never re-dump one side of a
live pair.

---

## Instance B — WSL PostgreSQL 16 (`gbrain` + `memory_governor` host) — port 5432

### Connecting

```bash
# Read the connection string into a variable — the password lives in
# ~/.gbrain/config.json (database_url) and ~/.pgpass, never in documents.
PGURL=$(jq -r .database_url /home/dev-p/.gbrain/config.json)
psql "$PGURL" -c "<SQL>"
```

For the `memory_governor` database, use the postgres URL with the database
segment swapped (`"${PGURL%/*}/memory_governor"`) or source the governor's
own `.env` and use its `MEMORY_GOVERNOR_DATABASE_URL` (referenced by name
only). Keep the conninfo a single argument so psql errors cannot echo it.

### Management

`systemd` is PID 1 in WSL. Both `systemctl` and `service` manage
PostgreSQL; `pg_ctlcluster` is the cluster-level start and stop tool.

`Ubuntu` is the only WSL installation and the default. Every WSL command
names it explicitly (`wsl -d Ubuntu ...`).

```bash
systemctl status postgresql            # systemd unit status
service postgresql status              # service wrapper (systemd-backed)
pg_lsclusters                          # cluster list and status (expect 16/main online, port 5432)
sudo pg_ctlcluster 16 main start       # cluster-level manual start
sudo pg_ctlcluster 16 main stop        # cluster-level manual stop
```

### Role-isolation test method (authoritative)

Role access is tested via `has_database_privilege(role, db, 'CONNECT')` —
never via `SET ROLE`. From a superuser session `SET ROLE` always succeeds;
impersonation proves nothing about the role's own privileges. Expected:
`memory_governor_svc` → `gbrain` = false; → `memory_governor` = true;
`ledger_writer` → `gbrain` = false.

### Clean shutdown — used every time WSL is shut down

`wsl --shutdown` stops Linux instantly; PostgreSQL then has to recover on
the next start. Stopping the services first avoids that. The sequence:

1. `systemctl --user stop memory-governor-api memory-governor-worker`
2. `sudo pg_ctlcluster 16 main stop`
3. Confirm: `pg_lsclusters` shows the cluster `down`, and
   `systemctl --user is-active memory-governor-api memory-governor-worker`
   shows `inactive` for both.
4. From PowerShell: `wsl --shutdown`.

### Boot durability

`/etc/wsl.conf` sets `systemd=true` and carries no `[boot]` command. Under
systemd, `postgresql.service` (enabled) starts the cluster when WSL starts,
and the two governor user units start the memory processes.
`start-memory-system.sh` stays on disk as a manual fallback only and must
not run at boot — it competes with `memory-governor-api.service` for port
8321 ([[[mybizz-config-docs:memory-governor/memory-governor-reference|Memory Governor Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md)).

**The only real verification method:** the clean shutdown procedure
(above), then a fresh terminal, then `pg_lsclusters` (16/main
online), `systemctl --user status memory-governor-api memory-governor-worker`
(both active), `ss -tlnp | grep 8321` (held by the unit's pid) — zero
manual intervention, zero crash-looping.

**If found down unexpectedly:** check `pg_lsclusters` for a "stale pid
file" message on manual start — a stale pid file means the last WSL stop
skipped the clean shutdown procedure, not necessarily a config fault. If
the units are confirmed present and the cluster is still down after a
genuine reboot, that's a real regression worth investigating fresh.

### Useful live queries

```bash
# Prerequisite: PGURL=$(jq -r .database_url /home/dev-p/.gbrain/config.json)
# Real embedding-coverage check, independent of gbrain doctor's own report
psql "$PGURL" -c "SELECT COUNT(*) AS total_chunks, COUNT(embedding) AS chunks_with_embedding, COUNT(*) - COUNT(embedding) AS missing FROM content_chunks;"

# Page count — read live, never recorded as a constant
psql "$PGURL" -c "SELECT count(*) FROM pages;"

# Row-level security coverage — expect every table covered
psql "$PGURL" -c "SELECT count(*) AS tables, count(*) FILTER (WHERE relrowsecurity) AS rls_tables FROM pg_class WHERE relkind='r' AND relnamespace=(SELECT oid FROM pg_namespace WHERE nspname='public');"

# Autovacuum recency — hot tables vacuum within days of writes; the low-write facts table lagging is normal
psql "$PGURL" -c "SELECT relname, last_autovacuum FROM pg_stat_user_tables ORDER BY last_autovacuum DESC NULLS LAST;"

# List all databases on this instance
psql "${PGURL%/*}/postgres" -c "\l+"

# Table inventory in a database
psql "$PGURL" -c "\dt"

# Installed extensions
psql "$PGURL" -c "SELECT extname, extversion FROM pg_extension;"

# Role inventory
psql "${PGURL%/*}/postgres" -c "SELECT rolname, rolcanlogin FROM pg_roles WHERE rolcanlogin ORDER BY rolname;"
```

**A note on `psql`'s pager:** results longer than one screen open in a
pager (`~` lines, `(END)` at the bottom). Press `q` to exit before running
further commands — a command typed while still inside the pager will not
execute. For scripted/agent use, pipe through `-t` (tuples-only) or add
`PAGER=cat`.

### When to use direct `psql` instead of `gbrain` CLI commands

GBrain's own CLI (`gbrain doctor`, `gbrain sources status`, etc.) is the
primary interface and should be preferred for anything it already reports
on. Direct `psql` access is appropriate specifically when:
- Cross-checking a CLI-reported fact independently (confirming a fact two
  ways, not trusting one report alone)
- The CLI doesn't expose a needed field (e.g. a source's raw `config`
  JSON — no dedicated subcommand for arbitrary key inspection)
- Diagnosing something the CLI's own error messages don't surface clearly
  enough

---

## Cross-instance rules

- **Port 5432 is Instance B from both sides.** WSL's PostgreSQL 16 listens on 5432 natively, and WSL's localhost relay binds Windows' 5432 to that same Instance B. The ledger (Instance A, Windows PostgreSQL 15) listens on **5433** — every ledger command carries `-p 5433`, always.
- **A raw WSL `psql` call intended for `pdlf` will not fail — it will silently connect to `gbrain`'s cluster instead**, and a bare Windows-side `psql` without `-p 5433` does the same through the relay. This is more dangerous than an outright connection failure; always use the PowerShell bridge with `-p 5433` for `pdlf`.
- **`compliance_ledger` must stay absent.** If it reappears, that is a finding (its baseline backup is listed in [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md)).
- **Destructive SQL from an agent is blocked by two layers** — the OpenCode permission deny patterns (`*DROP TABLE*`, `*DROP DATABASE*`, `*TRUNCATE*` in the global OpenCode config) and Cupcake's own destructive-SQL rule (enforcement state recorded in [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md), section Operational status). A denied database command should never be worked around; the denial is the system working.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Runtime configuration — connections and authentication (port, listen_addresses, password_encryption) | https://www.postgresql.org/docs/16/runtime-config-connection.html | 16.15 | 2026-10-20 |
| Runtime configuration — logging (logging_collector) | https://www.postgresql.org/docs/16/runtime-config-logging.html | 16.15 | 2026-10-20 |
| Runtime configuration — autovacuum | https://www.postgresql.org/docs/16/runtime-config-autovacuum.html | 16.15 | 2026-10-20 |
| Row security policies | https://www.postgresql.org/docs/16/ddl-rowsecurity.html | 16.15 | 2026-10-20 |
| Additional supplied extensions (pg_trgm, pgcrypto, plpgsql) | https://www.postgresql.org/docs/16/contrib.html | 16.15 | 2026-10-20 |
| Runtime configuration — connections and authentication (Instance A) | https://www.postgresql.org/docs/15/runtime-config-connection.html | 15.14 | 2026-10-20 |
| Runtime configuration — logging (Instance A) | https://www.postgresql.org/docs/15/runtime-config-logging.html | 15.14 | 2026-10-20 |
| pgvector | https://github.com/pgvector/pgvector | 0.6.0 | 2026-10-20 |
| EDB PostgreSQL installers (Windows builds) | https://www.enterprisedb.com/downloads/postgres-postgresql-downloads | 15.14 | 2026-10-20 |
| Ubuntu PostgreSQL cluster layout and management | `man pg_lsclusters` | 16 (Ubuntu 24.04 package) | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version (Instance A) | `SELECT version();` over the PowerShell bridge (pdlf_agent) | agent |
| Installed version (Instance B) | `psql "$PGURL" -c "SELECT version();"` | agent |
| Works (Instance A) | `Get-Service -Name "*postgresql*"` — expect `postgresql-x64-15` Running | agent |
| Works (Instance B cluster) | `pg_lsclusters` — expect `16/main` online; `systemctl status postgresql` — active and enabled | agent |
| Works (memory governor) | `systemctl --user is-active memory-governor-api memory-governor-worker` — active for both | agent |
| Server settings (Instance B: port, autovacuum, logging_collector, password_encryption, data_directory) | `psql "$PGURL" -c "SHOW <setting>;"` | agent |
| Row-level security coverage (`gbrain`) | The RLS-coverage query above — every table covered | agent |
| Embedding coverage (`gbrain`) | The embedding-coverage query above | agent |
| Page and chunk counts (`gbrain`) | The page-count query above — read live, never recorded | agent |
| Database inventory and sizes (either instance) | `\l+`, or the `pg_database_size` query | agent |
| Role inventory (either instance) | The `pg_roles` query | agent |
| Role isolation (Instance B) | `has_database_privilege(role, db, 'CONNECT')` per the test method above | agent |
| `compliance_ledger` absent | `\l` on Instance B — no such database | agent |
| `pgvector_user` / `pgvector_readonly` absent (Instance A) | The `pg_roles` query over the bridge | agent |
| WSL census | `wsl.exe -l -v` — one installation, `Ubuntu`, the default | agent |
| Windows service and registry census | `Get-Service -Name "*postgresql*"`, and `reg query HKLM\SOFTWARE\PostgreSQL /s` via `powershell.exe -NoProfile -Command "..."` — one product key | agent |
| Port listeners | `ss -tlnp` (WSL side); `netstat -ano` filtered to the 543x range (Windows side) | agent |
| Backups fresh and paired | List both backup locations for the two most recent cycles; `cmp` each pair; read the latest log in `C:\mybizz\logs\sunday-backup\` | agent |
| `SundayBackup` task | `schtasks /query /tn SundayBackup /v /fo list` via `powershell.exe` — Status Ready, last result 0 | agent |
| `pgpass.conf` present (Windows) | `Test-Path "$env:APPDATA\postgresql\pgpass.conf"` via `powershell.exe` | agent |
| Instance A superuser rows (`pg_hba_file_rules`, `SHOW data_directory`) | Superuser connection over the bridge with `PGADMIN_PASSWORD` | developer |
| PDLF `.env` integrity | Read `C:\pdlf\.env` directly: variable names, quoted Windows paths, `PGPORT=5433` | developer |

## Do not

- Do not attempt a direct WSL `psql` connection to reach `pdlf` — use the PowerShell bridge with `-p 5433`.
- Do not omit `-p 5433` on any Instance A connection — a bare connection (from either side of the WSL boundary) reaches Instance B.
- Do not build a `.sql` file with PowerShell `Out-File` and pass it to `psql -f` without confirming it's BOM-free.
- Do not start or stop the WSL cluster outside `systemctl`, `service` or `pg_ctlcluster`.
- Do not test role access with `SET ROLE` — use `has_database_privilege(role, db, 'CONNECT')`.
- Do not assume a "stale pid file" message on WSL cluster start indicates a config fault — it means the last WSL stop skipped the clean shutdown procedure.
- Do not run `wsl --shutdown` without the clean shutdown procedure first.
- Do not drop a database role without first running `DROP OWNED BY <role>` in every database where it holds privileges.
- Do not work around a denied destructive-SQL command — the two guard layers blocking it are the system working.
- Do not hard-code record, chunk or table counts from this suite as constants in other tools or checks — re-derive counts live with the queries above.
- Do not quote a password or path value into any command output — reference credentials by variable name only, always.
