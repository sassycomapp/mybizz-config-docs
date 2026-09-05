# PostgreSQL — Configuration

Canonical, current-state configuration record for every PostgreSQL instance on
this machine. Pure facts and settings — no narrative, no history, no design
rationale. For the "why," see `postgresql-explainer.md`. For commands and
procedures, see `postgresql-reference.md`. Last fully verified live: 2026-09-05.

**Two entirely separate instances exist. Do not confuse them.**

---

## Instance A — Windows-native PostgreSQL 15 (the PDLF ledger host)

| Item | Value |
|---|---|
| Version | 15.14 |
| Install path | `C:\Program Files\PostgreSQL\15\` |
| Data directory | `C:\Program Files\PostgreSQL\15\data` |
| Port | `5432` |
| Host (from Windows) | `127.0.0.1` or `localhost` |
| Reached from WSL via | PowerShell bridge only — see `postgresql-reference.md`. Direct WSL `psql` to `localhost:5432` connects to Instance B instead, silently. |
| Auth method | `scram-sha-256` for all users/addresses, including `0.0.0.0/0` and `::/0`. No trust paths. |
| Service (real, running) | `postgresql-x64-15` — Status: Running, StartType: Automatic |
| Service (dead duplicate) | `PostgreSQL` — Status: Stopped, StartType: Automatic. Same data directory as above. Harmless; cannot conflict since only one process can bind the port. Do not start it. |
| Binary (for the WSL PowerShell bridge) | `C:\Program Files\PostgreSQL\15\bin\psql.exe` |

### Roles

| Role | Notes |
|---|---|
| `postgres` | Superuser |
| `pdlf_agent` | Owns the `pdlf` database. Password stored as `PGPASSWORD` in `C:\dev\dev-makepdlf\makepdlf-project-library\.env` |
| `pgvector_user` | Present, undocumented origin. Whether anything currently authenticates as this role is unconfirmed — open item. |

### Databases

| Database | Owner | Size | Extensions | Notes |
|---|---|---|---|---|
| `pdlf` | `pdlf_agent` | 7,877 kB | `plpgsql` only | The PDLF build ledger. 7 tables, all currently empty. |
| `postgres` (admin) | `postgres` | 14 MB (pre-cleanup) | `adminpack`, `btree_gist`, `pg_stat_statements`, `pg_trgm`, `plpgsql`, `vector 0.8.0` | **Cleaned 2026-09-05** — 28 leftover user tables and the `vecs` schema removed; database now holds no user tables. Backup taken before removal: `postgres_admin_backup_2026-09-05.dump` (194,019 bytes). `vector` extension and `pgvector_user` role deliberately left in place — see below. |
| `template0` / `template1` | `postgres` | ~7.3 MB each | — | Standard, unmodified. |

### `pdlf` — table inventory

`projects`, `steps`, `gates`, `deviations`, `bft_records`, `isc`, `triage_findings` — all in schema `public`, all owned by `pdlf_agent`. All seven currently hold 0 rows.

Live column-level schema has drifted from `specifications-local/spec-postgres-ledger.md` on 6 of 7 tables (`triage_findings` matches exactly). A column-level rewrite of that spec is in progress as of this writing — treat the spec file, once updated, as authoritative over any older copy.

### `postgres` (admin database) — cleanup record

**Removed 2026-09-05**, after a verified backup: `departments`, `diary_cache`, `episodic_memory`, `episodic_memory_2023`, `episodic_memory_partitioned`, `episodic_memory_y2025m10`, `global_cache`, `other_table`, `products`, `roles`, `semantic_cache`, `semantic_cache_entries`, `semantic_memory`, `test_performance`, `test_python_integration`, `test_similarity`, `test_table`, `test_vector_10/128/3/5/512`, `test_vector_table`, `test_vectors`, `users`, `vector_cache`, `vector_search_test`, `working_memory` (schema `public`); `mem0_memories`, `mem0migrations` (schema `vecs`, dropped via `DROP SCHEMA vecs CASCADE`). Confirmed clean afterward — `\dt` returns "Did not find any relations." Backup: `postgres_admin_backup_2026-09-05.dump`, taken via the `postgres` superuser role (`pdlf_agent` lacked read permission on several of these tables). See `postgresql-explainer.md` for background on what this was.

---

## Instance B — WSL-native PostgreSQL 16 (the GBrain host)

| Item | Value |
|---|---|
| Version | 16.14 (Ubuntu 24.04 package) |
| Cluster name | `main` |
| Port | `5432` |
| Host (from WSL) | `localhost` or `127.0.0.1` |
| Data directory | `/var/lib/postgresql/16/main` |
| Log file | `/var/log/postgresql/postgresql-16-main.log` |
| Connection string (gbrain DB) | `postgresql://postgres:gbrain_local@localhost:5432/gbrain` |
| Management tooling | `pg_ctlcluster` / `service` — **not** `systemctl`. WSL PID 1 here is `init(Ubuntu)`, not `systemd`. |
| Boot config | `/etc/wsl.conf`, `[boot]` section: `command = "service postgresql start"` — confirmed present and correct. |

### Extensions (on the `gbrain` database)

`plpgsql` 1.0, `vector` 0.6.0, `pg_trgm` 1.6, `pgcrypto` 1.3.

### Roles

| Role | Notes |
|---|---|
| `postgres` | Owns `gbrain`, `compliance_ledger` |
| `memory_governor_svc` | Owns `memory_governor`. Scoped — cannot connect to `gbrain`. Password in `memory_governor`'s own `.env` (`MEMORY_GOVERNOR_DATABASE_URL`). |

### Databases

| Database | Owner | Size | Notes |
|---|---|---|---|
| `gbrain` | `postgres` | 126 MB | GBrain's own memory/vector store. ~1,500+ pages, ~5,000+ chunks, 62 tables (RLS on all), schema v128, embedding `openai:text-embedding-3-large` (1536d). |
| `memory_governor` | `memory_governor_svc` | 8,183 kB | 5 tables: `projects`, `memory_candidates`, `policy_versions`, `memory_events`, `audit_log`. See `memory-governor-config.md`. |
| `postgres` (admin) | `postgres` | 7,503 kB | Standard, unremarkable. |
| `template0` / `template1` | `postgres` | ~7.3–7.6 MB each | Standard, unmodified. |

**`compliance_ledger` — removed 2026-09-05.** Formerly a small, unused database here (2 tables, one test row). Backed up (`compliance_ledger_backup_2026-09-05.dump`, 6,149 bytes) then dropped via `DROP DATABASE`. Confirmed no longer present. See `postgresql-explainer.md` for background.

---

## Confirmed: no third instance exists

Checked and closed: Windows registry (one PostgreSQL product only), Windows services (two registrations, one data directory), no `Program Files (x86)` install, WSL Ubuntu-24.04 (one cluster, this one), WSL Ubuntu-22.04 second distro (no PostgreSQL at all — no binary, no cluster), no other listeners in the 543x port range on either side. A manually-compiled, never-registered instance can't be mathematically excluded, but no evidence of one exists.

---

## Known undocumented items (not yet resolved, deliberately deferred)

- `pgvector_user` role on Instance A — purpose and active usage unconfirmed. Deliberately left untouched during the 2026-09-05 cleanup.
- The dead duplicate `PostgreSQL` service on Instance A — cosmetic only, left in place deliberately.

## Resolved 2026-09-05

- The `postgres` admin-database "graveyard" on Instance A — backed up and removed. See Instance A section above.
- `compliance_ledger` on Instance B — backed up and removed. See Instance B section above.
