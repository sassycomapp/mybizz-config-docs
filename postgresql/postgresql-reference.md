# PostgreSQL — Reference: Commands, Procedures, and Troubleshooting

Companion to `postgresql-config.md` (every setting, path, and value) and
`postgresql-explainer.md` (what this system is and why, for a human reader).
This document is agent-facing — how to actually connect to, query, and
troubleshoot each instance safely.

**Two entirely separate instances exist — every procedure below is scoped
to one or the other. Using the wrong one connects silently to the wrong
database; see the cross-instance rules.**

---

## Instance A — Windows PostgreSQL 15 (`pdlf` ledger)

### Connecting — the only correct method from WSL

WSL's binfmt does not pass Linux environment variables to Windows
executables, so a bridge through PowerShell is required — and separately,
a direct WSL-side `psql` call to `localhost:5432` would silently hit the
*wrong* database (Instance B, not this one). Never attempt a direct WSL
`psql` connection to reach `pdlf`.

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGPASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -U pdlf_agent -d pdlf -c '<SQL>'"
```

This is the exact pattern verified live 2026-09-09 (queries, inserts, role
management all executed through it).

### Superuser connection (Instance A) — for role management

The `postgres` superuser credential is held in the same `.env` as
`PGADMIN_USER`/`PGADMIN_PASSWORD` (referenced by variable name only —
never printed):

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGADMIN_PASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -U postgres -d postgres -c '<SQL>'"
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
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "<SQL>"
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

### Useful live queries (verified live 2026-09-09)

```powershell
# Server version
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "SELECT version();"

# All real databases with sizes
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;"

# Full role inventory
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "SELECT rolname, rolcanlogin FROM pg_roles ORDER BY rolname;"

# Table inventory
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "\dt"

# Row counts across all 7 ledger tables
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "SELECT 'projects', count(*) FROM projects UNION ALL SELECT 'steps', count(*) FROM steps UNION ALL SELECT 'gates', count(*) FROM gates UNION ALL SELECT 'deviations', count(*) FROM deviations UNION ALL SELECT 'bft_records', count(*) FROM bft_records UNION ALL SELECT 'isc', count(*) FROM isc UNION ALL SELECT 'triage_findings', count(*) FROM triage_findings;"
```

### Service management (Windows) — verified live 2026-09-09

```powershell
Get-Service -Name "*postgresql*" | Format-Table Name, Status, StartType
```
Only `postgresql-x64-15` should ever be Running. A second registration, plain `PostgreSQL`, exists pointing at the same data directory — leave it Stopped; do not start it (see `postgresql-config.md`).

---

## Instance B — WSL PostgreSQL 16 (`gbrain` + `memory_governor` host)

### Connecting

```bash
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "<SQL>"
```

For the `memory_governor` database, source the governor's own `.env` and
use its `MEMORY_GOVERNOR_DATABASE_URL` (referenced by name only).

### Management — `pg_ctlcluster`/`service`, never `systemctl`

WSL in this environment does not run `systemd` as PID 1 (confirmed:
`ps -p 1 -o comm=` → `init(Ubuntu)`). Any command involving `systemctl`
fails here (`Failed to connect to bus: Host is down`) — expected, not a
fault.

```bash
pg_lsclusters                          # list clusters and status (online/down)
sudo pg_ctlcluster 16 main start       # start manually
sudo pg_ctlcluster 16 main stop        # stop manually
service postgresql status              # status check (works here; systemctl does not)
service postgresql start               # start via the service wrapper
```

### Boot durability — extended 2026-09-09, proven live

The `/etc/wsl.conf` `[boot]` command now starts PostgreSQL **and** the
memory-system processes at every WSL boot:

```ini
[boot]
command = "service postgresql start; su dev-p -c /home/dev-p/memory-governor/scripts/start-memory-system.sh"
```

The `start-memory-system.sh` script is idempotent (each process starts
only if not already running) and self-healing (restarts a dead worker).
**The only real verification method:** a full WSL shutdown from PowerShell
(`wsl --shutdown`), then a fresh terminal, then `ss -tlnp | grep 8321` and
`ps aux | grep app.worker` — both alive with zero manual intervention.
Proven live 2026-09-09 (the full restart test; both processes born at
boot).

**If found down unexpectedly:** check `pg_lsclusters` for a "stale pid
file" message on manual start — indicates an unclean prior shutdown (WSL
terminating mid-session), not necessarily a config fault. If the boot fix
is confirmed present and the cluster is still down after a genuine reboot,
that's a real regression worth investigating fresh.

### Useful live queries (verified live 2026-09-09)

```bash
# Real embedding-coverage check, independent of gbrain doctor's own report
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "SELECT COUNT(*) AS total_chunks, COUNT(embedding) AS chunks_with_embedding, COUNT(*) - COUNT(embedding) AS missing FROM content_chunks;"

# Page count (the live number: 1,759 as of 2026-09-09)
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "SELECT count(*) FROM pages;"

# Tables and RLS coverage
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "SELECT count(*) AS tables, count(*) FILTER (WHERE relrowsecurity) AS rls_tables FROM pg_class WHERE relkind='r' AND relnamespace=(SELECT oid FROM pg_namespace WHERE nspname='public');"

# List all databases on this instance
psql "postgresql://postgres:gbrain_local@localhost:5432/postgres" -c "\l+"

# Table inventory in a database
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "\dt"

# Installed extensions
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "SELECT extname, extversion FROM pg_extension;"

# Role inventory (the roles the suite documents)
psql "postgresql://postgres:gbrain_local@localhost:5432/postgres" -c "SELECT rolname, rolcanlogin FROM pg_roles WHERE rolcanlogin ORDER BY rolname;"
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

- **Never assume `localhost:5432` means the same thing on both sides.** From WSL it's Instance B (`gbrain`, `memory_governor`). From Windows it's Instance A (`pdlf`). They share a port number and nothing else — genuinely independent servers.
- **A raw WSL `psql` call intended for `pdlf` will not fail — it will silently connect to `gbrain`'s cluster instead**, since both listen on `localhost:5432` from their own side. This is more dangerous than an outright connection failure; always use the PowerShell bridge for `pdlf`.
- **`compliance_ledger` no longer exists** (removed 2026-09-05, backed up first — see `postgresql-config.md`). It was never the real ledger — that's `pdlf` on Instance A — noted here in case an older reference to it is still found anywhere.
- **Destructive SQL from an agent is blocked by two layers** — the OpenCode permission deny patterns (`*DROP TABLE*`, `*DROP DATABASE*`, `*TRUNCATE*` in the global config) and Cupcake's own destructive-SQL rule. A denied database command should never be worked around; the denial is the system working.

## Do not

- Do not attempt a direct WSL `psql` connection to reach `pdlf` — use the PowerShell bridge.
- Do not build a `.sql` file with PowerShell `Out-File` and pass it to `psql -f` without confirming it's BOM-free.
- Do not use `systemctl` in WSL for PostgreSQL management — use `pg_ctlcluster`/`service`.
- Do not start the dead duplicate `PostgreSQL` Windows service.
- Do not assume a "stale pid file" message on WSL cluster start indicates a config fault — it usually means an unclean prior WSL shutdown.
- Do not drop a database role without first running `DROP OWNED BY <role>` in every database where it holds privileges — the real, verified drop sequence (2026-09-09).
- Do not quote a password or path value into any command output — reference credentials by variable name only, always.
