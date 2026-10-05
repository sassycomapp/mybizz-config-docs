---
title: "postgresql-reference"
doc-id: "mb-5bad908d"
updated: "2026-10-05"
---
# PostgreSQL — Reference: Commands, Procedures, and Troubleshooting

Companion to [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) (the spec — every setting, path, and value) and
[[[mybizz-config-docs:postgresql/postgresql-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-explainer.md) (the authoritative whole-system narrative — what this
system is and why, for every reader). Exam companions: [[[mybizz-config-docs:postgresql/postgresql-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-plan.md)
(next run's job-spec), [[[mybizz-config-docs:postgresql/postgresql-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-exam-report.md) (current verified state),
[[[mybizz-config-docs:postgresql/postgresql-log|Log]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-log.md) (notable events), [[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md) (transient exam
knowledge). This document is agent-facing — how to actually connect to, query, and
troubleshoot each instance safely.

**Two entirely separate instances exist — every procedure below is scoped
to one or the other. Using the wrong one connects silently to the wrong
database; see the cross-instance rules. Port map: 5432 is Instance B from
both sides (WSL native, and Windows via WSL's port relay); the ledger
(Instance A) is on 5433 from Windows.**

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

This is the exact pattern verified live (queries, inserts, role
management all executed through it; re-verified 2026-10-05 on port 5433).

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
succeeds. Verified live 2026-09-09: the pgvector roles' function-EXECUTE
grants in `postgres` blocked the first drop attempt; `DROP OWNED` in
`postgres` cleared them and both roles dropped cleanly. Note: per-database
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
- **`-h localhost` vs `-h 127.0.0.1` are equivalent here** — an earlier documentation version incorrectly blamed a connection failure on IPv6 resolution; a live four-test matrix (2026-08-26) confirmed the real cause was always a wrong password, not the address form.
- **The `.env` sourcing failure — FIXED 2026-09-09.** Line 16 held an unquoted Windows path (`PSQL_WIN_PATH=C:\Program Files\...`), which bash word-split on `source`. The value is now quoted and the file sources cleanly (verified live). Keep Windows-path values quoted if ever re-added.
- **An unquoted path in a `.env` breaks bash `source`-ing but not line-by-line parsing** — the OpenCode permission model's bridge pattern parses line-by-line and is unaffected. The distinction matters when choosing a fix.
- **`SHOW log_directory` is superuser-only** — `pdlf_agent` is correctly refused (`pg_read_all_settings` boundary). Instance A's `logging_collector` is off, so no log files are written while it stays off; faults surface via SCM/Event Viewer and probe errors (verified 2026-10-05).

### Useful live queries (verified live 2026-09-09; port 5433 verified 2026-10-05)

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

### Service management (Windows) — verified live 2026-09-09

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
# ~/.gbrain/config.json (database_url) and ~/.pgpass, never in documents
# (credential rotated 2026-09-28; the previously-quoted literal is retired).
PGURL=$(jq -r .database_url /home/dev-p/.gbrain/config.json)
psql "$PGURL" -c "<SQL>"
```

For the `memory_governor` database, use the postgres URL with the database
segment swapped (`"${PGURL%/*}/memory_governor"` — verified 2026-09-28) or
source the governor's own `.env` and use its `MEMORY_GOVERNOR_DATABASE_URL`
(referenced by name only). Keep the conninfo a single argument so psql
errors cannot echo it.

### Management — systemd is PID 1 since the 2026-09-15 migration; `systemctl` and `service` both work — reconciled 2026-09-28

**Reconciled 2026-09-28** by the `memory-system-diagnostic` skill's §2 live
init-check (the open item below is closed). Live results in this environment:

- PID 1 = `systemd` (`ps -p 1 -o comm=`).
- `systemctl status postgresql` → active (exited), preset enabled, EXIT 0.
- `service postgresql status` → works, EXIT 0 — the service wrapper now
  delegates to systemd; both management paths are currently valid.
- `pg_lsclusters` → 16/main online, port 5432.

```bash
systemctl status postgresql            # systemd unit status — verified 2026-09-28
service postgresql status              # service wrapper — verified 2026-09-28 (systemd-backed)
pg_lsclusters                          # cluster list/status — verified 2026-09-28
sudo pg_ctlcluster 16 main start       # cluster-level manual start (not re-verified 2026-09-28)
sudo pg_ctlcluster 16 main stop        # cluster-level manual stop (not re-verified 2026-09-28)
```

Historical note (2026-09-13): WSL then ran `init(Ubuntu)` as PID 1 and
`systemctl` failed (`Failed to connect to bus: Host is down`). The
2026-09-15 Memory Governor auto-start migration flipped `systemd=true` in
`/etc/wsl.conf` — a change to the entire WSL environment's init model. The
prior "never systemctl" guidance described the pre-migration environment
only and no longer applies.

### Boot durability — systemd owns the boot since the 2026-09-28 retirement

**Boot-command retirement (2026-09-28):** `/etc/wsl.conf` no longer carries
a `[boot]` command invoking `start-memory-system.sh`. Under systemd
(PID 1 since 2026-09-15): `postgresql.service` (enabled) starts the
cluster, and the two governor user units start the memory processes.
Historical: the 2026-09-09 boot command (`service postgresql start` +
`start-memory-system.sh`) was proven live then, but at both 2026-09-28
boots its script instance won the port-8321 bind race against
`memory-governor-api.service`, which crash-looped until the duplicate was
killed — full retirement decided 2026-09-28 (see
[[[mybizz-config-docs:memory-governor/memory-governor-reference|Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md) §Permanent auto-start migration).

**The only real verification method:** a full WSL shutdown from PowerShell
(`wsl --shutdown`), then a fresh terminal, then `pg_lsclusters` (16/main
online), `systemctl --user status memory-governor-api memory-governor-worker`
(both active), `ss -tlnp | grep 8321` (held by the unit's pid) — zero
manual intervention, zero crash-looping.

**If found down unexpectedly:** check `pg_lsclusters` for a "stale pid
file" message on manual start — indicates an unclean prior shutdown (WSL
terminating mid-session), not necessarily a config fault. If the units are
confirmed present and the cluster is still down after a genuine reboot,
that's a real regression worth investigating fresh.

### Useful live queries (verified live 2026-09-09; variable form 2026-09-28)

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
- **`compliance_ledger` no longer exists** (removed 2026-09-05, backed up first — see [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md)). It was never the real ledger — that's `pdlf` on Instance A — noted here in case an older reference to it is still found anywhere.
- **Destructive SQL from an agent is blocked by two layers** — the OpenCode permission deny patterns (`*DROP TABLE*`, `*DROP DATABASE*`, `*TRUNCATE*` in the global config) and Cupcake's own destructive-SQL rule. A denied database command should never be worked around; the denial is the system working.

## Do not

- Do not attempt a direct WSL `psql` connection to reach `pdlf` — use the PowerShell bridge with `-p 5433`.
- Do not omit `-p 5433` on any Instance A connection — a bare connection (from either side of the WSL boundary) reaches Instance B.
- Do not build a `.sql` file with PowerShell `Out-File` and pass it to `psql -f` without confirming it's BOM-free.
- Since the 2026-09-15 migration systemd is PID 1 in WSL — `systemctl` is a valid PostgreSQL management path (reconciled 2026-09-28, see Management above); `pg_ctlcluster` remains the cluster-level start/stop tool. Do not assume either the pre- or post-migration init model without a live check.
- Do not start the dead duplicate `PostgreSQL` Windows service.
- Do not assume a "stale pid file" message on WSL cluster start indicates a config fault — it usually means an unclean prior WSL shutdown.
- Do not drop a database role without first running `DROP OWNED BY <role>` in every database where it holds privileges — the real, verified drop sequence (2026-09-09).
- Do not quote a password or path value into any command output — reference credentials by variable name only, always.
