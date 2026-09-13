---
document: "PostgreSQL — Configuration"
doc-id: postgresql-config
state: Live
date-created: 2026-09-05
---

# PostgreSQL — Configuration

Canonical, current-state configuration record for every PostgreSQL instance on
this machine. Pure facts and settings — no narrative, no history, no design
rationale. For the "why," see `postgresql-explainer.md`. For commands and
procedures, see `postgresql-reference.md`. Last fully verified live: 2026-09-13
(run #2, first formal plan-driven exam).

**Two entirely separate instances exist. Do not confuse them.** The layer
placement: Instance B hosts the pre-makePDLF layer's memory; Instance A
hosts the PDLF layer's ledger (see
`C:\pdlf\pdlf-library\pdlf-explainer-docs\pdlf-environment-explainer.md` for the layer map).

---

## Instance A — Windows-native PostgreSQL 15 (the PDLF ledger host)

| Item | Value |
|---|---|
| Version | 15.14, compiled by Visual C++ build 1944, 64-bit (verified live 2026-09-13) |
| Install path | `C:\Program Files\PostgreSQL\15\` |
| Data directory | `C:\Program Files\PostgreSQL\15\data` |
| Port | `5432` |
| Host (from Windows) | `127.0.0.1` or `localhost` (equivalent — verified 2026-08-26) |
| Reached from WSL via | PowerShell bridge only — see `postgresql-reference.md`. Direct WSL `psql` to `localhost:5432` connects to Instance B instead, silently. |
| Auth method | `scram-sha-256` for all users/addresses, including `0.0.0.0/0` and `::/0`. No trust paths. (Verified 2026-09-05 with superuser access; `pg_hba.conf` itself is readable only by superuser — re-verification as `pdlf_agent` is refused by design.) |
| Service (real, running) | `postgresql-x64-15` — Status: Running, StartType: Automatic (verified live 2026-09-13) |
| Service (dead duplicate) | `PostgreSQL` — Status: Stopped, StartType: Automatic. Same data directory as above. Harmless; cannot conflict since only one process can bind the port. Do not start it. (Verified live 2026-09-09.) |
| Binary (for the WSL PowerShell bridge) | `C:\Program Files\PostgreSQL\15\bin\psql.exe` |

### Roles

| Role | Notes |
|---|---|
| `postgres` | Superuser. Credential: `PGADMIN_USER`/`PGADMIN_PASSWORD` in `C:\dev\dev-makepdlf\makepdlf-project-library\.env` (referenced by variable name only — never printed) |
| `pdlf_agent` | Owns the `pdlf` database. Password stored as `PGPASSWORD` in the same `.env` |
| ~~`pgvector_user`~~ / ~~`pgvector_readonly`~~ | **REMOVED 2026-09-09** — dormant leftovers from the pre-GBrain mem0/vector experiments (login-capable + a no-login group; EXECUTE grants on the pgvector extension functions in the `postgres` database; zero table grants; zero owned objects). Revoked via `DROP OWNED` in `postgres`, then dropped; verified gone cluster-wide 2026-09-09. See `postgresql-explainer.md` for the full investigation. |

### Databases (verified live 2026-09-13)

| Database | Owner | Size | Notes |
|---|---|---|---|
| `pdlf` | `pdlf_agent` | 7,877 kB | The PDLF build ledger. 7 tables, all currently hold 0 rows (verified live 2026-09-13). Extensions: `plpgsql` only |
| `postgres` (admin) | `postgres` | 8,485 kB | **Cleaned 2026-09-05** — 28 leftover mem0/vector-experiment tables and the `vecs` schema removed; database now holds no user tables. Backup: `C:\Users\dev-p\postgres_admin_backup_2026-09-05.dump` (194,019 bytes) |
| `template0` / `template1` | `postgres` | ~7.3 MB each | Standard. `template0` is not connectable (`datallowconn = false` — verified live 2026-09-13) |

### `pdlf` — table inventory

`projects`, `steps`, `gates`, `deviations`, `bft_records`, `isc`,
`triage_findings` — all in schema `public`, all owned by `pdlf_agent`. All
seven currently hold 0 rows (verified live 2026-09-13).

**Schema-vs-spec drift: RESOLVED.** The column-level drift noted on
2026-09-05 (6 of 7 tables) was corrected in the spec the same day — commit
`fae811c` ("docs(spec): correct postgres ledger spec — PowerShell
connection pattern + triage_findings live schema",
`specifications-local/spec-postgres-ledger.md`). The spec now documents the
live schema, including `resolution_note`/`resolved_at` on
`triage_findings`. The spec file is authoritative.

### The `.env` integrity note (fixed 2026-09-09)

Line 16 of `C:\dev\dev-makepdlf\makepdlf-project-library\.env` previously
held an **unquoted** Windows path (`PSQL_WIN_PATH=C:\Program
Files\PostgreSQL\15\bin\psql.exe`), which bash word-split on `source`
(`FilesPostgreSQL15binpsql.exe: command not found`). **Fixed 2026-09-09:**
the value is now quoted, and the file sources cleanly (verified live).
The variable itself has zero consumers — kept for future use.

---

## Instance B — WSL-native PostgreSQL 16 (the memory-system host)

| Item | Value |
|---|---|
| Version | 16.14 (Ubuntu 24.04 package) |
| Cluster name | `main` — status `online` (verified live 2026-09-13) |
| Port | `5432` |
| Host (from WSL) | `localhost` or `127.0.0.1` |
| Data directory | `/var/lib/postgresql/16/main` |
| Config directory | `/etc/postgresql/16/main/` (`postgresql.conf`, `pg_hba.conf`, `pg_ident.conf`, `start.conf`, `conf.d/`, `environment`) — `pg_hba.conf` is root/postgres-owned, not readable by `dev-p` |
| Log file | `/var/log/postgresql/postgresql-16-main.log` |
| Connection string (gbrain DB) | `postgresql://postgres:gbrain_local@localhost:5432/gbrain` |
| Connection string (governor DB) | In `memory_governor`'s own `.env` as `MEMORY_GOVERNOR_DATABASE_URL` (referenced by name only) |
| Management tooling | `pg_ctlcluster` / `service` — **not** `systemctl`. WSL PID 1 here is `init(Ubuntu)`, not `systemd`. |
| Boot config | `/etc/wsl.conf`, `[boot]` section: `command = "service postgresql start; su dev-p -c /home/dev-p/memory-governor/scripts/start-memory-system.sh"` — PostgreSQL **and** the memory-system processes auto-start at every WSL boot. Proven live: the 2026-09-09 full-restart test (both processes born at boot). |
| Autovacuum posture | `on` (cluster-wide). Hot-table recency is the health signal: `content_chunks` and `pages` vacuum within days of writes (last: 2026-09-11 / 2026-09-13). The `facts` table showing `last_autovacuum = never` is **normal** — it is low-write; flag only if a *hot* table stops vacuuming. |

### Role-isolation test method (authoritative, verified 2026-09-13)

Role access is tested via `has_database_privilege(role, db, 'CONNECT')` — never
via `SET ROLE` (from a superuser session `SET ROLE` always succeeds; impersonation
proves nothing about the role's own privileges). Verified: `memory_governor_svc`
→ `gbrain` = false; → `memory_governor` = true; `ledger_writer` → `gbrain` = false.

### Roles (verified live 2026-09-13)

| Role | Notes |
|---|---|
| `postgres` | Owns `gbrain`. Password: `gbrain_local` (in the connection string above) |
| `memory_governor_svc` | Owns `memory_governor` (all 5 tables). Scoped — cannot connect to `gbrain`. Password in `memory_governor`'s own `.env` (`MEMORY_GOVERNOR_DATABASE_URL`). |
| `ledger_writer` / `ledger_approver` | Login-capable test roles from the memory governor's own RLS live-testing — cited as the verified precedent in `security-global/infrastructure/sec-database-access-control.md` ("live-tested, correctly blocked the `ledger_writer` role from inserting override-type events it wasn't scoped for"). Own nothing (`gbrain`'s 62 tables are all owned by `postgres`). Documented here 2026-09-09 — the existing suite never mentioned them. |

### Databases (verified live 2026-09-13)

| Database | Owner | Size | Notes |
|---|---|---|---|
| `gbrain` | `postgres` | 164 MB | GBrain's memory/vector store. **1,824 pages, 5,529 chunks, 5,529 embedded (100%)** — verified live 2026-09-13. 62 tables, all with RLS enabled, all owned by `postgres`. Schema v128, embedding `openai:text-embedding-3-large` (1536d). Extensions: `plpgsql` 1.0, `vector` 0.6.0, `pg_trgm` 1.6, `pgcrypto` 1.3 |
| `memory_governor` | `memory_governor_svc` | 8,167 kB | 5 tables (all owned by `memory_governor_svc`): `projects`, `memory_candidates` (5 real rows), `policy_versions`, `memory_events`, `audit_log`. See `memory-governor-config.md`. |
| `postgres` (admin) | `postgres` | 7,503 kB | Standard, unremarkable. |
| `template0` / `template1` | `postgres` | ~7.3–7.6 MB each | Standard, unmodified. |

**`compliance_ledger` — removed 2026-09-05.** Backed up
(`/home/dev-p/compliance_ledger_backup_2026-09-05.dump`, 6,149 bytes —
location verified live 2026-09-13) then dropped. Confirmed absent
(verified live 2026-09-13).

---

## Confirmed: no third instance exists

Checked and closed: Windows registry (one PostgreSQL product only), Windows
services (two registrations, one data directory), no `Program Files (x86)`
install, WSL Ubuntu-24.04 (one cluster, this one), WSL Ubuntu-22.04 second
distro (no PostgreSQL at all — no binary, no cluster), no other listeners
in the 543x port range on either side. A manually-compiled,
never-registered instance can't be mathematically excluded, but no evidence
of one exists.

---

## Resolved record

| Item | Resolution |
|---|---|
| The Windows `postgres` admin-database graveyard | Removed 2026-09-05 after a verified backup (28 mem0/vector tables + the `vecs` schema). See Instance A above. |
| `compliance_ledger` on Instance B | Removed 2026-09-05 after a verified backup. See Instance B above. |
| `pgvector_user` + `pgvector_readonly` on Instance A | **Removed 2026-09-09** — the investigation closed the loose end: no grants except pgvector-function EXECUTE in `postgres`, no owned objects, no existence on Instance B. `DROP OWNED` in `postgres`, then dropped; verified gone cluster-wide. |
| The `pdlf`-schema/spec drift | The spec was corrected 2026-09-05 (commit `fae811c`); the spec is now authoritative. |
| The `.env` line-16 sourcing failure | Fixed 2026-09-09 (the value quoted); the file sources cleanly. |
| The boot-durability fix | Extended 2026-09-09: the boot command now also starts the memory-system processes; the whole chain proven across a real WSL restart. |

## Known undocumented items (deliberately retained, each documented)

- The dead duplicate `PostgreSQL` Windows service — cosmetic only, left in
  place deliberately. Removing the registration (`sc delete PostgreSQL`)
  is available to the developer if ever wanted.
- `pg_hba.conf` content on Instance B — root/postgres-owned, not readable
  by `dev-p`; the scram posture was verified 2026-09-05 with superuser
  access. Re-verification requires that access level.
