# PostgreSQL — Reference: Commands, Procedures, and Troubleshooting

Companion to `postgresql-config.md` (every setting, path, and value) and
`postgresql-explainer.md` (what this system is and why, for a human reader).
This document is agent-facing — how to actually connect to, query, and
troubleshoot each instance safely. Agent-facing.

**Two entirely separate instances exist — every procedure below is scoped
to one or the other. Using the wrong one connects silently to the wrong
database; see the WSL warning under Instance B.**

---

## Instance A — Windows PostgreSQL 15 (`pdlf` ledger)

### Connecting — the only correct method from WSL

WSL's binfmt does not pass Linux environment variables to Windows
executables, so a bridge through PowerShell is required — and separately,
a direct WSL-side `psql` call to `localhost:5432` would silently hit the
*wrong* database (Instance B, not this one). Never attempt a direct WSL
`psql` connection to reach `pdlf`.

```powershell
powershell.exe -Command '$env:PGPASSWORD="<value>"; & "C:\Program Files\PostgreSQL\15\bin\psql.exe" -h localhost -U pdlf_agent -d pdlf -c "<SQL>"'
```

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
- **Line 16 of the `.env` file holds an unquoted Windows path containing spaces**, which can break shell `source`-ing if the file is ever read that way rather than parsed line-by-line. Not yet fixed as of this writing.

### Useful live queries

```powershell
# Server version
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "SELECT version();"

# All real databases
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "\l+"

# Table inventory
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "\dt"

# Row counts across all 7 ledger tables
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "SELECT 'projects', count(*) FROM projects UNION ALL SELECT 'steps', count(*) FROM steps UNION ALL SELECT 'gates', count(*) FROM gates UNION ALL SELECT 'deviations', count(*) FROM deviations UNION ALL SELECT 'bft_records', count(*) FROM bft_records UNION ALL SELECT 'isc', count(*) FROM isc UNION ALL SELECT 'triage_findings', count(*) FROM triage_findings;"

# Installed extensions
& "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U pdlf_agent -d pdlf -h 127.0.0.1 -c "SELECT extname, extversion FROM pg_extension;"
```

### Service management (Windows)

```powershell
Get-Service -Name "*postgresql*"
```
Only `postgresql-x64-15` should ever be Running. A second registration, plain `PostgreSQL`, exists pointing at the same data directory — leave it Stopped; do not start it (see `postgresql-config.md`).

---

## Instance B — WSL PostgreSQL 16 (`gbrain` host)

### Connecting

```bash
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "<SQL>"
```

### Management — `pg_ctlcluster`/`service`, never `systemctl`

WSL in this environment does not run `systemd` as PID 1 (confirmed: `ps -p 1 -o comm=` → `init(Ubuntu)`). Any command involving `systemctl` fails here (`Failed to connect to bus: Host is down`) — expected, not a fault.

```bash
pg_lsclusters                          # list clusters and status (online/down)
sudo pg_ctlcluster 16 main start       # start manually
sudo pg_ctlcluster 16 main stop        # stop manually
service postgresql status              # status check (works here; systemctl does not)
service postgresql start               # start via the service wrapper
```

### Boot durability

PostgreSQL does not auto-start on WSL boot by default. Fix, applied and confirmed present in `/etc/wsl.conf`:
```ini
[boot]
command = "service postgresql start"
```

**The only real verification method:** a full WSL shutdown from PowerShell (`wsl --shutdown`), then a fresh terminal, then `pg_lsclusters` showing `online` with zero manual intervention. A simple new terminal does not exercise the real boot path.

**If found down unexpectedly:** check `pg_lsclusters` for a "stale pid file" message on manual start — indicates an unclean prior shutdown (WSL terminating mid-session), not necessarily a config fault. If the boot fix is confirmed present and the cluster is still down after a genuine reboot, that's a real regression worth investigating fresh.

### Useful live queries

```bash
# Real embedding-coverage check, independent of gbrain doctor's own report
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "SELECT COUNT(*) AS total_chunks, COUNT(embedding) AS chunks_with_embedding, COUNT(*) - COUNT(embedding) AS missing FROM content_chunks;"

# List all databases on this instance
psql "postgresql://postgres:gbrain_local@localhost:5432/postgres" -c "\l+"

# List real table names in a database
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "\dt"

# Inspect a specific table's real columns
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "\d <table_name>"

# Installed extensions
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "SELECT extname, extversion FROM pg_extension;"
```

**A note on `psql`'s pager:** results longer than one screen open in a pager (`~` lines, `(END)` at the bottom). Press `q` to exit before running further commands — a command typed while still inside the pager will not execute.

### When to use direct `psql` instead of `gbrain` CLI commands

GBrain's own CLI (`gbrain doctor`, `gbrain sources status`, etc.) is the primary interface and should be preferred for anything it already reports on. Direct `psql` access is appropriate specifically when:
- Cross-checking a CLI-reported fact independently (confirming a fact two ways, not trusting one report alone)
- The CLI doesn't expose a needed field (e.g. a source's raw `config` JSON — no dedicated subcommand for arbitrary key inspection)
- Diagnosing something the CLI's own error messages don't surface clearly enough

---

## Cross-instance rules

- **Never assume `localhost:5432` means the same thing on both sides.** From WSL it's Instance B (`gbrain`). From Windows it's Instance A (`pdlf`). They share a port number and nothing else — genuinely independent servers.
- **A raw WSL `psql` call intended for `pdlf` will not fail — it will silently connect to `gbrain`'s cluster instead**, since both listen on `localhost:5432` from their own side. This is more dangerous than an outright connection failure; always use the PowerShell bridge for `pdlf`.
- **`compliance_ledger` no longer exists** (removed 2026-09-05, backed up first — see `postgresql-config.md`). It was never the real ledger — that's `pdlf` on Instance A — noted here in case an older reference to it is still found anywhere.

## Do not

- Do not attempt a direct WSL `psql` connection to reach `pdlf` — use the PowerShell bridge.
- Do not build a `.sql` file with PowerShell `Out-File` and pass it to `psql -f` without confirming it's BOM-free.
- Do not use `systemctl` in WSL for PostgreSQL management — use `pg_ctlcluster`/`service`.
- Do not start the dead duplicate `PostgreSQL` Windows service.
- Do not assume a "stale pid file" message on WSL cluster start indicates a config fault — it usually means an unclean prior WSL shutdown.
