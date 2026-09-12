---
document: "PostgreSQL — Explainer"
doc-id: postgresql-explainer
state: Live
date-created: 2026-09-05
---

# PostgreSQL — Explainer

Companion to `postgresql-config.md` (every setting and value) and
`postgresql-reference.md` (commands and procedures for agents). This
document is for a human reader: what PostgreSQL is doing across this whole
system, database by database — what each one is, what component of Mybizz
actually uses it, and why it exists at all. All counts and states verified
live 2026-09-09.

---

## 1. The big picture — two servers, five databases, three real consumers, and where each sits in the environment

This machine runs **two entirely separate PostgreSQL server installations**
— not one database wearing different hats, but two independent programs,
each with its own install, its own data directory, its own process. Across
those two servers sit **five databases total**. Of those five, **three are
real, in-use components of your system** (`gbrain`, `memory_governor`,
`pdlf`), and the rest are PostgreSQL's own standard administrative
databases, not part of your system at all.

**Where each server sits in the environment's layers** (per
`C:\pdlf\pdlf-library\pdlf-explainer-docs\pdlf-environment-explainer.md`): Instance B (WSL, PostgreSQL 16)
hosts the **pre-makePDLF layer's** memory — GBrain and the memory governor
are supporting systems built before and beneath PDLF. Instance A (Windows,
PostgreSQL 15) hosts the **PDLF layer's own ledger** — the record the PDLF
application writes as it builds the shipped estate. The two servers serve
two different layers; neither travels to the shipped estate, and neither
is present at runtime inside any client application.

Why two servers instead of one hosting everything: GBrain and the Memory
Governor are both high-churn, LLM-driven workloads — constant syncing,
embedding, writing. PDLF's ledger is the opposite kind of thing: low-churn,
but the single most consequential record in the entire build system — every
step, every gate, every approved deviation lives there, and if that record
is ever wrong, everything built downstream of it is untrustworthy. Putting
GBrain's high-churn database and PDLF's high-stakes database on physically
separate servers means a problem in one — a bad sync, a runaway process, a
corrupted write — can never reach across and damage the other. The
separation also mirrors the environment's own access-control pattern: each
server has its own, separately scoped roles with the minimum privilege each
writer needs (`sec-database-access-control.md`, which cites this exact
arrangement as its verified precedent).

**Instance A**, on Windows, runs PostgreSQL 15 and hosts `pdlf`.
**Instance B**, inside WSL, runs PostgreSQL 16 and hosts `gbrain` and
`memory_governor`.

Both happen to listen on the same port, 5432 — one from the Windows side,
one from the WSL side. That's a coincidence of default configuration, not a
relationship between them — and it is the single most operationally
dangerous fact about this arrangement: a database call made from the wrong
side connects to the wrong server *silently*. See
`postgresql-reference.md` for the rules that prevent it.

---

## 2. `gbrain` — the memory system's content store (Instance B, WSL)

**What it is:** the actual database behind GBrain, the tool that gives
every project in this system a searchable, synthesized memory of its own
documentation and code. When you run `gbrain sync`, this is where the
content ends up. When an agent runs `gbrain search` or `gbrain think`, this
is what's being queried.

**What's inside (verified live 2026-09-09):** 1,759 pages from every
registered source — chunked into 5,443 pieces, every single one carrying a
1,536-dimension vector embedding (100% embedding coverage, verified
independently of GBrain's own doctor report). Sixty-two tables, all with
row-level security enabled. The database is 148 MB and growing as sources
are added — it has grown steadily all week as the documentation suites
were built.

**Who uses it:** every GBrain source registered on this machine —
`default`, `dev-root-hub`, `makepdlf-project-library`, the `mb-*` code/docs
pairs, `mybizz-config-docs`, `mybizz-os-docs`, and `memory-governor-code`
all write into and are read out of this one database. It's the shared
memory layer underneath the entire Mybizz system, not scoped to any single
project.

**Why it lives on the WSL side:** GBrain itself is WSL-native software —
its CLI, its sync engine, its embedding pipeline all run inside WSL. Its
database naturally lives alongside it rather than reaching across to
Windows for every operation.

---

## 3. `memory_governor` — the gatekeeper in front of GBrain (Instance B, WSL)

**What it is:** the database behind Memory Governor, the service that sits
between "an agent wants to write something into permanent memory" and
"GBrain actually stores it durably." Nothing is supposed to reach GBrain's
durable memory without passing through here first.

**What's inside:** five tables — `projects` (which projects are registered
with the governor), `memory_candidates` (every piece of content that's ever
been submitted for review, with its confidence score and contradiction
assessment), `policy_versions`, `memory_events` (the async write queue that
actually pushes approved content into GBrain), and `audit_log`. Five real
candidate rows exist — small, but genuinely live, not just schema with
nothing in it.

**Who uses it:** the `mb-submit-memory` skill (the only sanctioned,
developer-facing way to submit content into memory), PDLF's own
step-completion process (once PDLF is actually running steps), and — by
design, and only by design — nothing else. GBrain's own automatic "dream
cycle" enrichment is deliberately unable to route through this database at
all; that's a confirmed, permanent architectural limitation, not an
oversight, documented in `memory-governor-config.md`.

**The RLS test roles, explained.** Two login-capable roles on this
instance — `ledger_writer` and `ledger_approver` — exist from the memory
governor's own build: they were created to live-test the row-level
security on `memory_events`, and that test is cited as the verified
precedent in `security-global/infrastructure/
sec-database-access-control.md` (the role-per-instance access-control
pattern). They own nothing; they are test fixtures, documented here rather
than silently present.

**Why it's a separate database from `gbrain` itself**, even though they're
on the same server: Memory Governor needs its own tables for its own
bookkeeping — pending reviews, audit trails, policy versions — that have
nothing to do with GBrain's content schema. Keeping them separate means
neither system's schema constrains or gets confused with the other's, even
though both live conveniently on the same physical WSL Postgres instance.

---

## 4. `pdlf` — the PDLF build ledger (Instance A, Windows)

**What it is:** the single source of truth for PDLF's own build process —
the actual tool being built inside `dev-makepdlf`. Every step the PDLF
orchestrator runs, every gate it passes or fails, every deviation a
developer approves along the way, gets written here. The project's own
principle, stated directly in its specification: "if it's not in `pdlf`,
it didn't happen."

**What's inside:** seven tables — `projects`, `steps`, `gates`,
`deviations`, `bft_records`, `isc` (Ideal State Criteria), and
`triage_findings` (security/quality findings from Sentinel's step-triggered
reviews). All seven currently hold zero rows — not a fault, just an honest
reflection that the orchestrator hasn't yet run against a real project.
Once it does, this is where that entire history will live — including the
security findings Sentinel writes.

**The schema is now verified against the spec.** The column-level drift
noted on 2026-09-05 (6 of 7 tables) was corrected in the specification the
same day (commit `fae811c`); the spec and the live schema now agree, and
the spec is authoritative.

**Who uses it:** the PDLF orchestrator itself, and nothing else. This
database isn't meant to be touched directly by any other part of the
system — reads and writes to it are supposed to happen only through a
real PDLF step, per its own governing principle.

**Why it's on Windows, separate from everything else:** partly the
isolation reasoning from Section 1, and partly practical — this predates
some of the WSL-centric tooling and was set up as a standalone Windows
service. The real operational cost of that choice is that reaching it from
WSL requires a PowerShell bridge rather than a direct connection — covered
fully in `postgresql-reference.md`. That cost is worth stating plainly:
the bridge exists because WSL cannot pass environment variables to Windows
programs, and because `localhost:5432` is a different server on each side
— the same fact that makes the memory system's own database calls safe
from accidental cross-connection.

---

## 5. `compliance_ledger` — removed 2026-09-05

**What it was:** a small database that sat alongside `gbrain` in the WSL
cluster, with two tables — `ledger_events` (completely empty) and `tasks`
(exactly one row: `test-task-1`, created 2026-08-06, every other field
blank). Nothing read from or wrote to it, and nothing in GBrain's own
memory, across all twelve registered sources, ever mentioned it. It shared
no schema, no table names, and no real content with `pdlf` — despite the
similar-sounding name, it was never a copy or alternate version of the
real ledger.

**Most likely explanation:** a one-off smoke test — someone stood up a
`tasks` table, inserted a single placeholder row to confirm the mechanism
worked, and never returned to it.

**Disposition:** backed up in full
(`/home/dev-p/compliance_ledger_backup_2026-09-05.dump` — location
verified live 2026-09-09) and then dropped. The misleading name — close
enough to "the real ledger" to warrant a full investigation once already —
was reason enough to remove it rather than leave it as a permanent source
of confusion for any future database sweep.

---

## 6. The Windows `postgres` admin database — cleaned up 2026-09-05 (Instance A, Windows)

**What it should be:** PostgreSQL's own default administrative database —
normally just system catalogs, nothing of yours.

**What was actually inside it, until this cleanup:** roughly 28 real,
user-created tables — `episodic_memory`, `semantic_memory`,
`working_memory`, several `test_vector_*` tables, a `mem0` schema
(`mem0_memories`, `mem0migrations`). Unrelated to PDLF's `pdlf` database
sitting on the very same server.

**Best available explanation:** this looked like the remains of an
earlier phase of experimenting with AI-agent memory architecture — likely
using the open-source `mem0` framework directly against Postgres with the
`pgvector` extension — before the current GBrain-based approach was
adopted instead. Nearly everything in it was empty or held only a handful
of test rows; nothing suggested recent or ongoing use.

**Disposition:** backed up in full
(`C:\Users\dev-p\postgres_admin_backup_2026-09-05.dump` — location
verified live 2026-09-09, via the `postgres` superuser role, since the
`pdlf_agent` account lacked read permission on several of the tables — a
sign in itself that these tables belonged to a different, earlier setup).
All 28 tables and the `vecs` schema were then dropped; confirmed clean
afterward. The `vector` extension was deliberately left untouched.

---

## 7. The pgvector roles — investigated and removed 2026-09-09

Two roles on Instance A — `pgvector_user` (login-capable) and
`pgvector_readonly` (a no-login group) — existed with no documented
origin, flagged as the suite's open item since 2026-09-05.

**The investigation (2026-09-09, closed):** `pgvector_user` held CONNECT
on every Instance-A database and EXECUTE on 30 pgvector extension
functions (in the `postgres` database); `pgvector_readonly` was a
no-login group alongside it; neither owned a single object; neither exists
on Instance B. This is the fingerprint of the mem0/vector experiments that
produced the admin-database graveyard: the roles were the experiment's
own access pair, left behind when the experiments ended. The hypothesis
recorded on 2026-09-05 — "possibly a leftover from whatever built the
graveyard" — is confirmed by the fingerprint.

**Disposition:** both roles removed 2026-09-09 (`DROP OWNED` in
`postgres` first, then `DROP ROLE` for each; verified gone cluster-wide
from a second database). The removal closes the suite's last open item.

---

## 8. The two-databases trap — why the same port means different servers

The single most operationally dangerous fact about this arrangement:
`localhost:5432` is a **different server** depending on which side of the
WSL boundary the call is made from. WSL's PostgreSQL 16 and Windows'
PostgreSQL 15 both bind port 5432 on their own side of the boundary, and
neither can see the other.

This has bitten twice in this project's history. The PDLF ledger's own
specification documents both reasons the bridge exists: WSL cannot pass
Linux environment variables to Windows programs (a password exported in
WSL never reaches a Windows-side client), and a direct WSL-side database
call **does not fail visibly** — it silently connects to whatever is
listening on that side. The memory system's own database checks have the
same property in reverse.

The working rules that prevent it (enforced in
`postgresql-reference.md`): all `pdlf` access goes through the PowerShell
bridge; all GBrain/governor access runs inside WSL; and any database check
names its instance explicitly. The 2026-09-09 audits of both instances
were run under exactly those rules.

---

## 9. The layer placement — where each database sits in the environment

Per `C:\pdlf\pdlf-library\pdlf-explainer-docs\pdlf-environment-explainer.md` (the pre-makePDLF, makePDLF,
PDLF, and shipped layers):

- **Instance B (WSL PostgreSQL 16) is pre-makePDLF-layer infrastructure.**
  GBrain and the memory governor are supporting systems built before and
  beneath PDLF; their databases exist to serve the building of PDLF and,
  later, the building of web applications through it.
- **Instance A's `pdlf` database is PDLF-layer material.** The ledger is
  the record the PDLF application itself writes as it orchestrates builds
  — it comes into real use only when the PDLF layer runs real projects.
- **The shipped estate contains no PostgreSQL at all.** Client instances
  hold their data in Anvil's own Data Tables (per
  `adr-client-instance-architecture`), not in any database of ours. The
  shipped estate is out of scope for both PostgreSQL instances, exactly as
  it is out of scope for every developer-side system.

This placement is why the two-databases trap matters at all: the layers
are served by different servers, so a tool call that crosses a layer
boundary without the bridge silently lands in the wrong one.

---

## 10. Closing

PostgreSQL's job across this environment is narrow: hold the records that
must survive — GBrain's memory, the governor's bookkeeping, PDLF's build
ledger — in two deliberately separate servers, each scoped to its own
consumers, each with its own roles. Every real correction described here —
the graveyard cleanup, the compliance_ledger removal, the pgvector role
investigation and removal, and the boot-durability fix that now starts
both servers' workloads automatically — came from the same discipline:
check directly, verify at each step, and never let a database you didn't
create remain a mystery.

---

*Companion documents: `postgresql-config.md` (current state),
`postgresql-reference.md` (commands and procedures). The layer map:
`C:\pdlf\pdlf-library\pdlf-explainer-docs\pdlf-environment-explainer.md`. The memory system:
`memory-governor-config.md`, `mb-submit-memory` (its own suites). The
ledger contract: `spec-postgres-ledger.md` (makepdlf-project-library).*

*End of document*
