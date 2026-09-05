# PostgreSQL Reference

## What This Covers

PostgreSQL as used by GBrain specifically. **Two entirely separate PostgreSQL contexts exist on this machine — do not confuse them:**

| | This instance (GBrain) | PDLF's ledger instance |
|---|---|---|
| Host | WSL-native | Windows-native |
| Reached via | Direct WSL connection | WSL-to-Windows bridge |
| Purpose | GBrain's memory/vector store | PDLF's build ledger (source of truth for the build pipeline) |
| Why separate | Deliberate architectural decision — GBrain is a higher-churn, LLM-driven workload; a GBrain problem must never be able to take down PDLF's ledger | — |

This document covers the WSL-native GBrain instance only.

---

## Cluster Details

**Version:** PostgreSQL 16 | **Cluster name:** `main` | **Port:** `5432`
**Data directory:** `/var/lib/postgresql/16/main`
**Log file:** `/var/log/postgresql/postgresql-16-main.log`
**Connection string:** `postgresql://postgres:gbrain_local@localhost:5432/gbrain`

**Extensions confirmed installed:** `pgvector` (version `0.6.0`).

**Management mechanism on this machine:** Ubuntu's cluster-based `pg_ctlcluster`/`service` tooling — **not** `systemctl`. WSL in this environment is not running `systemd` as PID 1, so any instruction involving `systemctl` will fail here (`Failed to connect to bus: Host is down`). This is expected, not a fault.

---

## Commands

| Command | Description |
|---|---|
| `pg_lsclusters` | List all clusters and their status (`online`/`down`) |
| `sudo pg_ctlcluster 16 main start` | Start the cluster manually |
| `sudo pg_ctlcluster 16 main stop` | Stop the cluster manually |
| `service postgresql status` | Check status (works in this environment; `systemctl status` does not) |
| `service postgresql start` | Start via the `service` wrapper (used in the boot-start fix below) |
| `psql "<connection-string>" -c "<query>"` | Run a single query directly from the shell |

---

## Boot Durability — Confirmed Required, Not Optional

**PostgreSQL does not auto-start on WSL boot by default.** Confirmed directly: `/etc/wsl.conf` originally had no `[boot]` section at all, and neither `.bashrc` nor `.profile` started the service. Every WSL restart left the database down until someone manually noticed and ran `pg_ctlcluster` — the exact kind of silent, recurring gap this system has been built to eliminate elsewhere.

**Fix, applied and verified:** `/etc/wsl.conf` now includes:
```ini
[boot]
command = "service postgresql start"
```

**Verification method — the only one that actually proves this works:** a full WSL shutdown from PowerShell (`wsl --shutdown`), followed by opening a fresh terminal and running `pg_lsclusters` — confirming the cluster shows `online` with zero manual intervention. A simple new terminal is not sufficient to test this; it does not exercise the actual boot path.

**If PostgreSQL is ever found down unexpectedly:** first check `pg_lsclusters` for a "stale pid file" message on the next manual start — this indicates an unclean prior shutdown (WSL terminating mid-session), not necessarily a configuration fault. If the boot fix above is confirmed present in `/etc/wsl.conf` and the cluster is still down after a real reboot, that's a genuine regression worth investigating fresh, not assumed to be the same historical issue.

---

## Direct Database Access — When and Why

GBrain's own CLI (`gbrain doctor`, `gbrain sources status`, etc.) is the primary interface and should be preferred for anything it already reports on. Direct `psql` access is appropriate specifically when:

- Cross-checking a CLI-reported fact independently (e.g. confirming schema version two ways, not trusting one report alone)
- The CLI's own commands don't expose a needed field (e.g. a source's raw `config` JSON, which has no dedicated `sources` subcommand for editing arbitrary keys)
- Diagnosing something the CLI's error messages don't surface clearly enough on their own

**Useful direct queries, confirmed working:**

```bash
# Real embedding-coverage check, independent of doctor's own report
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "SELECT COUNT(*) AS total_chunks, COUNT(embedding) AS chunks_with_embedding, COUNT(*) - COUNT(embedding) AS missing FROM content_chunks;"

# List real table names when unsure what exists
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "\dt"

# Inspect a specific table's real columns
psql "postgresql://postgres:gbrain_local@localhost:5432/gbrain" -c "\d <table_name>"
```

**A note on `psql`'s pager:** results longer than one screen open in a pager (shown as `~` lines with `(END)` at the bottom). Press `q` to exit it before running further commands — a command typed while still inside the pager will not execute.

---

## File Locations

| Item | Location |
|---|---|
| WSL boot config | `/etc/wsl.conf` |
| Cluster data | `/var/lib/postgresql/16/main` |
| Cluster log | `/var/log/postgresql/postgresql-16-main.log` |

---

*End of document*
