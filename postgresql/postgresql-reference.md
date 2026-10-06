---
title: "postgresql-reference"
doc-id: "mb-5bad908d"
updated: "2026-10-06"
---
# PostgreSQL — Reference: Commands, Procedures, and Troubleshooting

Companion to [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) (the spec — every setting, path, and value) and
[[[mybizz-config-docs:postgresql/postgresql-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-explainer.md) (the authoritative whole-system narrative — what this
system is and why, for every reader). Exam companions: [[[mybizz-config-docs:postgresql/postgresql-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-plan.md)
(next run's job-spec), [[[mybizz-config-docs:postgresql/postgresql-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-report.md) (current verified state),
[[[mybizz-config-docs:postgresql/postgresql-log|Log]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-log.md) (notable events), [[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md) (transient exam
knowledge). This document is agent-facing — how to actually connect to, query, and
troubleshoot each instance safely.

## The two PostgreSQL installations at a glance

This machine runs **two separate PostgreSQL installations. Both are installed,
running and needed; neither replaces the other.** Each serves a different part
of the system:

| | Instance A | Instance B |
|---|---|---|
| Program | PostgreSQL 15 | PostgreSQL 16 |
| Runs on | Windows | WSL installation `Ubuntu` (Ubuntu 24.04) |
| Serves | PDLF and makePDLF — the `pdlf` build ledger | GBrain (`gbrain`) and the Memory Governor (`memory_governor`) |
| Port | `5433` | `5432` |
| Reached from WSL | PowerShell bridge, always with `-p 5433` | directly, `localhost:5432` |
| Starts | automatically with Windows (service `postgresql-x64-15`) | automatically with WSL (systemd, `postgresql.service`) |
| Current use | running; the ledger's tables stay empty until PDLF runs a real project | running; holds GBrain's memory and the governor's records |

**The rule that follows:** every database command names its instance and its
port. Port 5432 reaches Instance B from both sides of the WSL boundary, so a
command meant for the ledger that omits `-p 5433` reaches GBrain's server
instead, without any error.

Every procedure below is scoped to one instance or the other; see the
cross-instance rules at the end.

---

## Instance A — Windows PostgreSQL 15 (`pdlf` ledger) — port 5433

### Connecting — the only correct method from WSL

WSL's binfmt does not pass Linux environment variables to Windows
executables, so a bridge through PowerShell is required — and separately,
a connection without the ledger's port (`-p 5433`) would silently hit the
*wrong* database (Instance B, reachable from Windows too via WSL's port
relay on 5432). Never omit `-p 5433` for the ledger.

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGPASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -p 5433 -U pdlf_agent -d pdlf -c '<SQL>'"
```

This is the verified working pattern for queries, inserts and role management.

### Superuser connection (Instance A) — for role management

The `postgres` superuser credential is held in the same `.env` as
`PGADMIN_USER`/`PGADMIN_PASSWORD` (referenced by variable name only —
never printed):

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGADMIN_PASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -p 5433 -U postgres -d postgres -c '<SQL>'"
```

**Role management requires `DROP OWNED` first.** A role holding privileges
in a database (e.g. EXECUTE on extension functions) cannot be dropped
until they are revoked — `DROP OWNED BY <role>;` in **each database where
the role holds anything** handles all of it, after which `DROP ROLE`
succeeds. Note: per-database
CONNECT via `PUBLIC` needs no revocation — a role relying on `PUBLIC`
connectivity holds no per-database grants.

### Direct Windows PowerShell connection (human-run only)

A developer running commands directly in a Windows PowerShell terminal
(not through OpenCode/WSL) uses the simpler direct form:

```powershell
$env:PGPASSWORD = "<value from .env>"
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -c "<SQL>"
```

**Reading the password without pasting it anywhere:**
```powershell
$envContent = Get-Content "C:\dev\dev-makepdlf\makepdlf-project-library\.env"
$pgLine = $envContent | Where-Object { $_ -match "^PGPASSWORD=" }
$env:PGPASSWORD = ($pgLine -split "=", 2)[1]
```

### Confirmed pitfalls

- **Do not build a `.sql` file via PowerShell's `Out-File` and pass it with `psql -f`.** `Out-File -Encoding utf8` adds an invisible byte-order-mark that `psql` fails to parse, producing `syntax error at or near "ï»¿ALTER"` on the first statement only. Pass SQL directly via `-c`, or verify the file is BOM-free before using `-f`.
- **`-h localhost` and `-h 127.0.0.1` are equivalent here** — a connection failure with either is a password problem, not an address problem.
- **Quote every Windows path in `.env`.** An unquoted value such as `C:\Program Files\...` is word-split by bash when the file is sourced.
- **An unquoted path in a `.env` breaks bash `source`-ing but not line-by-line parsing** — the OpenCode permission model's bridge pattern parses line-by-line and is unaffected. The distinction matters when choosing a fix.
- **`SHOW log_directory` is superuser-only** — `pdlf_agent` is correctly refused (`pg_read_all_settings` boundary). Instance A's `logging_collector` is off, so no log files are written while it stays off; faults surface via SCM/Event Viewer and probe errors (verified 2026-10-05).

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
Only `postgresql-x64-15` should ever be Running. A second registration, plain `PostgreSQL`, exists pointing at the same data directory — leave it Stopped; do not start it (see [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md)).

### Dumping Instance A (backup cycle, developer-run)

```powershell
& "C:\Program Files\PostgreSQL\15\bin\pg_dump.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -p 5433 -Fc -f "C:\backup-gbrain\pdlf-db-backup-<DATE>.dump"
& "C:\Program Files\PostgreSQL\15\bin\pg_dump.exe" -U postgres -d postgres -h 127.0.0.1 -p 5433 -Fc -f "C:\backup-gbrain\postgres-a-admin-db-backup-<DATE>.dump"
```
Dump once to `C:\backup-gbrain\` (the direct Windows target), then copy to the WSL location and hash-verify the pair — never re-dump one side of a live pair.

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
segment swapped (`"${PGURL%/*}/memory_governor"`) or
source the governor's own `.env` and use its `MEMORY_GOVERNOR_DATABASE_URL`
(referenced by name only). Keep the conninfo a single argument so psql
errors cannot echo it.

### Management

systemd is PID 1 in WSL. Both `systemctl` and `service` manage PostgreSQL;
`pg_ctlcluster` is the cluster-level start and stop tool.

`Ubuntu` is the only WSL installation and the default. Every WSL command
names it explicitly (`wsl -d Ubuntu ...`).

```bash
systemctl status postgresql            # systemd unit status
service postgresql status              # service wrapper (systemd-backed)
pg_lsclusters                          # cluster list and status (expect 16/main online, port 5432)
sudo pg_ctlcluster 16 main start       # cluster-level manual start
sudo pg_ctlcluster 16 main stop        # cluster-level manual stop
```

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

`/etc/wsl.conf` carries no `[boot]` command. Under systemd,
`postgresql.service` (enabled) starts the cluster when WSL starts, and the two
governor user units start the memory processes. The old
`start-memory-system.sh` script stays on disk as a manual fallback only. It
must not run at boot, because it competes with `memory-governor-api.service`
for port 8321 (see
[[[mybizz-config-docs:memory-governor/memory-governor-reference|Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md)).

**The only real verification method:** the clean shutdown procedure
(above), then a fresh terminal, then `pg_lsclusters` (16/main
online), `systemctl --user status memory-governor-api memory-governor-worker`
(both active), `ss -tlnp | grep 8321` (held by the unit's pid) — zero
manual intervention, zero crash-looping.

**If found down unexpectedly:** check `pg_lsclusters` for a "stale pid
file" message on manual start — a stale pid file means WSL was stopped
without the clean shutdown procedure, not necessarily a config fault. If
the units are confirmed present and the cluster is still down after a
genuine reboot, that's a real regression worth investigating fresh.

### Useful live queries

```bash
# Prerequisite: PGURL=$(jq -r .database_url /home/dev-p/.gbrain/config.json)
# Real embedding-coverage check, independent of gbrain doctor's own report
psql "$PGURL" -c "SELECT COUNT(*) AS total_chunks, COUNT(embedding) AS chunks_with_embedding, COUNT(*) - COUNT(embedding) AS missing FROM content_chunks;"

# Page count
psql "$PGURL" -c "SELECT count(*) FROM pages;"

# Tables and RLS coverage
psql "$PGURL" -c "SELECT count(*) AS tables, count(*) FILTER (WHERE relrowsecurity) AS rls_tables FROM pg_class WHERE relkind='r' AND relnamespace=(SELECT oid FROM pg_namespace WHERE nspname='public');"

# List all databases on this instance
psql "${PGURL%/*}/postgres" -c "\l+"

# Table inventory in a database
psql "$PGURL" -c "\dt"

# Installed extensions
psql "$PGURL" -c "SELECT extname, extversion FROM pg_extension;"

# Role inventory (the roles the suite documents)
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
- **`compliance_ledger` must stay absent.** It was never the real ledger; if it reappears, that is a finding (its baseline backup is listed in [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md)).
- **Destructive SQL from an agent is blocked by two layers** — the OpenCode permission deny patterns (`*DROP TABLE*`, `*DROP DATABASE*`, `*TRUNCATE*` in the global config) and Cupcake's own destructive-SQL rule. A denied database command should never be worked around; the denial is the system working.

## Do not

- Do not attempt a direct WSL `psql` connection to reach `pdlf` — use the PowerShell bridge with `-p 5433`.
- Do not omit `-p 5433` on any Instance A connection — a bare connection (from either side of the WSL boundary) reaches Instance B.
- Do not build a `.sql` file with PowerShell `Out-File` and pass it to `psql -f` without confirming it's BOM-free.
- Do not follow pre-systemd guidance: systemd is PID 1 in WSL, `systemctl` is a valid management path, and `pg_ctlcluster` remains the cluster-level tool.
- Do not start the dead duplicate `PostgreSQL` Windows service.
- Do not assume a "stale pid file" message on WSL cluster start indicates a config fault — it means WSL was stopped without the clean shutdown procedure.
- Do not run `wsl --shutdown` without the clean shutdown procedure first.
- Do not drop a database role without first running `DROP OWNED BY <role>` in every database where it holds privileges.
- Do not quote a password or path value into any command output — reference credentials by variable name only, always.
