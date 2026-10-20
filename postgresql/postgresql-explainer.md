---
title: "postgresql-explainer"
doc-id: "mb-e4410ed0"
updated: "2026-10-20"
---
# PostgreSQL — Explainer

For any reader — the developer, a visiting technical consultant, or an
agent — this is what PostgreSQL is doing across MyBizz: which servers
exist, which databases matter, and why the arrangement is shaped the way
it is. Every setting and value lives in [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md);
every command and procedure lives in [[[mybizz-config-docs:postgresql/postgresql-reference|Reference]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md).

## What it is

MyBizz runs two entirely separate PostgreSQL server installations on one
machine — not one server wearing different hats, but two independent
programs, each with its own install, its own data directory and its own
process. Across those two servers sit the databases that hold the records
which must survive: `gbrain`, the searchable, synthesized memory behind
GBrain; `memory_governor`, the gatekeeper's own bookkeeping in front of
that memory; and `pdlf`, the PDLF build ledger — the record the PDLF
orchestrator writes as it builds, where the project's own principle
applies: if it is not in `pdlf`, it did not happen. The remaining databases
are PostgreSQL's own administrative databases, not part of MyBizz.

The two servers serve two different layers of the environment (the
division docmap, `C:\dev\dev-root\docmap.md`, maps the layers). Instance
B, inside WSL, hosts the supporting-systems layer's memory — GBrain and
the memory governor are supporting systems built before and beneath PDLF.
Instance A, on Windows, hosts the PDLF layer's own ledger. Neither server
travels to the shipped estate, and neither is present at runtime inside
any client application.

## What it can do

- Hold durable, structured records that many different tools can query,
  with transactional safety.
- Enforce role-per-consumer access control: each consumer gets its own,
  separately scoped role with the minimum privilege it needs, and a role
  scoped to one database cannot connect to another.
- Enforce row-level security on every table of a database, as defense in
  depth beneath the role layer.
- Store vector embeddings alongside text, so search can match meaning as
  well as words — the mechanism behind GBrain's semantic memory.
- Back itself up on a schedule into compressed, hash-verified dump pairs
  in two locations, with a second, human-readable export lane for
  database-only content.
- Start automatically with its host — with Windows for one server, with
  WSL under systemd for the other — and submit to cluster-level,
  service-level and SQL-level inspection.

## Suitability

- **Best for:** records whose loss or corruption is unacceptable and that
  several tools must query under strict access control — a build ledger;
  a durable memory store with embedding search.
- **Good for:** local analytical stores, test fixtures, and any
  developer-side system that needs real relational guarantees on one
  machine.
- **Not good for:** the shipped estate — client instances hold their data
  in Anvil's own Data Tables ([[adr-client-instance-architecture|Client
  Instance Architecture]]), not in any database of MyBizz; file-lane
  content, whose home is the documentation repositories (a database mirror
  of files is a backup lane, not the primary store); and single-user
  scratch work, for which a flat file is the right tool.

## Why it works this way

**Two servers, not one.** GBrain and the memory governor are high-churn,
LLM-driven workloads — constant syncing, embedding, writing. The PDLF
ledger is the opposite kind of thing: low-churn, but the single most
consequential record in the build system — every step, every gate, every
approved deviation lives there, and if that record is wrong, everything
built downstream of it is untrustworthy. Putting the high-churn databases
and the high-stakes database on physically separate servers means a
problem in one — a bad sync, a runaway process, a corrupted write — can
never reach across and damage the other. The separation also mirrors the
environment's own access-control pattern: each server has its own,
separately scoped roles ([[sec-database-access-control|Database Access
Control]] cites this arrangement as its verified precedent).

**The port topology and the trap it prevents.** WSL's localhost relay
binds Windows' port for Instance B to that same Instance B, so one port
serves it from both sides of the WSL boundary. The ledger therefore
listens on a different port, and every database command names its instance
and its port. The trap this prevents is silent: a database call made
without the bridge, or without the ledger's port, does not fail visibly —
it connects to the wrong server. The discipline is absolute because the
failure mode gives no error.

**One role per consumer, minimum privilege.** Each database has its own
owner; scoped services cannot cross into each other; row-level security
covers every table in `gbrain`; and the test roles that proved the RLS
setup are documented rather than hidden — an unexplained object is treated
as a mystery to resolve, never as noise.

**Each server lives where its consumer lives.** GBrain is WSL-native
software — its CLI, sync engine and embedding pipeline run inside WSL — so
its database lives alongside it rather than reaching across to Windows for
every operation. The ledger is a Windows service, native to the layer it
serves. Each server starts with its host.

**Objects that must stay absent.** A small set of objects — one database
and two roles — must never reappear on the servers. They belong to no
current design; if any reappears, something is recreating it, and that is
a finding to investigate, not an object to adopt.

**Agents never run destructive SQL.** Two independent guard layers block
it; a denied command is the system working. And no credential is ever
printed: passwords are referenced by variable name only, held in
credential files and `pgpass` stores, never in documents.

## What has to happen

- Every database command names its instance and its port — the one rule
  that prevents the silent cross-connection.
- The weekly backup cycle covers every data-bearing database; dump pairs
  are hash-verified; an extra cycle always runs before upgrades, schema
  changes or destructive operations; and the markdown export lane runs
  after the database dumps.
- WSL is shut down only after the clean shutdown procedure — stopping the
  governor units and the cluster first — so PostgreSQL never recovers
  from a forced stop.
- Some checks stay with the developer: anything needing superuser rights
  on the Windows server, and anything reading the credential file. Agent
  tooling is guard-blocked on those by design, so full verification needs
  developer participation.
- The suite is kept current through MyBizz's config-management system
  ([[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Config Manager Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md)), which holds
  this system's register row; this suite's facts are what that system
  examines against.
- GBrain's own facts (its version, its reranker, its embedding model) live
  in [[[mybizz-config-docs:gbrain/gbrain-config|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md), and the memory governor's in
  [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) — this suite
  holds the database layer only. Memory writes reach GBrain only through
  the governor; `mb-submit-memory` is its developer-facing entry.
- Objects that must stay absent stay absent; any new database, role or
  listener is investigated before it is accepted, never adopted silently.

---

*Companion documents: [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) (settings),
[[[mybizz-config-docs:postgresql/postgresql-reference|Reference]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md) (commands and procedures),
[[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md) (what differs from the standard). The
ledger contract: [[[pdlf:pdlf-library/specifications-local/spec-postgres-ledger|Spec: Postgres Ledger]]](C:/pdlf/pdlf-library/specifications-local/spec-postgres-ledger.md) (PDLF).*
