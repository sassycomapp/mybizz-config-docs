# PostgreSQL — Explainer

Companion to `postgresql-config.md` (every setting and value) and
`postgresql-reference.md` (commands and procedures for agents). This
document is for a human reader: what PostgreSQL is doing across this whole
system, database by database — what each one is, what component of Mybizz
actually uses it, and why it exists at all.

---

## 1. The big picture — two servers, six databases, three real consumers

This machine runs **two entirely separate PostgreSQL server installations**
— not one database wearing different hats, but two independent programs,
each with its own install, its own data directory, its own process. Across
those two servers sit **six databases total**. Of those six, **three are
real, in-use components of your system** (`gbrain`, `memory_governor`,
`pdlf`), and **two are inactive leftovers** (`compliance_ledger`, and the
"graveyard" tables inside the Windows admin database) that don't belong to
anything currently running. The rest are PostgreSQL's own standard
administrative databases, not part of your system at all.

Why two servers instead of one hosting everything: GBrain and the Memory
Governor are both high-churn, LLM-driven workloads — constant syncing,
embedding, writing. PDLF's ledger is the opposite kind of thing: low-churn,
but the single most consequential record in the entire build system — every
step, every gate, every approved deviation lives there, and if that record
is ever wrong, everything built downstream of it is untrustworthy. Putting
GBrain's high-churn database and PDLF's high-stakes database on physically
separate servers means a problem in one — a bad sync, a runaway process, a
corrupted write — can never reach across and damage the other.

**Instance A**, on Windows, runs PostgreSQL 15 and hosts `pdlf`.
**Instance B**, inside WSL, runs PostgreSQL 16 and hosts `gbrain`,
`memory_governor`, and `compliance_ledger`.

Both happen to listen on the same port, 5432 — one from the Windows side,
one from the WSL side. That's a coincidence of default configuration, not a
relationship between them. See `postgresql-reference.md` for why this
specific detail matters operationally.

---

## 2. `gbrain` — GBrain's memory (Instance B, WSL)

**What it is:** the actual database behind GBrain, the tool that gives
every project in this system a searchable, synthesized memory of its own
documentation and code. When you run `gbrain sync`, this is where the
content ends up. When an agent runs `gbrain search` or `gbrain think`, this
is what's being queried.

**What's inside:** every page GBrain has ever imported from every
registered source — over 1,500 pages and growing, chunked into roughly
5,000 pieces, each with a 1536-dimension vector embedding attached so
GBrain can find content by meaning, not just keyword. Sixty-two tables in
total, with row-level security enabled on all of them (so, in a
multi-brain or multi-user setup, one project's content can be walled off
from another's — not currently exercised on a single-developer machine,
but built in).

**Who uses it:** every GBrain source registered on this machine —
`default`, `dev-root-hub`, `makepdlf-project-library`, all six `mb-*`
code/docs pairs, `mybizz-config-docs`, `mybizz-os-docs`, and
`memory-governor-code` all write into and are read out of this one
database. It's the shared memory layer underneath the entire Mybizz
system, not scoped to any single project.

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
actually pushes approved content into GBrain), and `audit_log`. Currently
five real candidate rows exist — small, but genuinely live, not just
schema with nothing in it.

**Who uses it:** the `mb-submit-memory` skill (the only sanctioned,
developer-facing way to submit content into memory), PDLF's own
step-completion process (once PDLF is actually running steps), and — by
design, and only by design — nothing else. GBrain's own automatic "dream
cycle" enrichment is deliberately unable to route through this database at
all; that's a confirmed, permanent architectural limitation, not an
oversight, documented in `memory-governor-config.md`.

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
`triage_findings` (security/quality findings from the build's own review
steps). All seven currently hold zero rows — not a fault, just an honest
reflection that the orchestrator hasn't yet run against a real project.
Once it does, this is where that entire history will live.

**Who uses it:** the PDLF orchestrator itself, and nothing else. This
database isn't meant to be touched directly by any other part of the
system — reads and writes to it are supposed to happen only through a
real PDLF step, per its own governing principle.

**Why it's on Windows, separate from everything else:** partly the
isolation reasoning from Section 1, and partly practical — this predates
some of the WSL-centric tooling and was set up as a standalone Windows
service. The real operational cost of that choice is that reaching it from
WSL requires a PowerShell bridge rather than a direct connection — covered
fully in `postgresql-reference.md`.

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

**Disposition:** backed up in full (`compliance_ledger_backup_2026-09-05.dump`)
and then dropped. The misleading name — close enough to "the real ledger"
to warrant a full investigation once already — was reason enough to
remove it rather than leave it as a permanent source of confusion for any
future database sweep.

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

**Disposition:** backed up in full (`postgres_admin_backup_2026-09-05.dump`,
via the `postgres` superuser role, since the `pdlf_agent` account lacked
read permission on several of the tables — a sign in itself that these
tables belonged to a different, earlier setup). All 28 tables and the
`vecs` schema were then dropped; confirmed clean afterward. The `vector`
extension and the `pgvector_user` role were deliberately left untouched —
a separate decision, not yet made, kept apart from this cleanup on
purpose.

---

## 7. Loose ends, left deliberately open

- **A role called `pgvector_user` exists on the Windows instance**, but
  nothing has confirmed whether anything currently authenticates as it —
  possibly a leftover from whatever built the `postgres` graveyard above.
- **A second, stopped Windows service** is registered under the plain name
  `PostgreSQL`, pointing at the exact same data directory as the real,
  running `postgresql-x64-15` service — almost certainly a leftover from
  the original installer, before the service got reconfigured under its
  versioned name. Inert: since both registrations point at the same data,
  only one can ever actually run.
- **PDLF's own ledger specification document had drifted from the live
  schema** on 6 of its 7 tables — a correction is being made separately;
  noted here only as a confirmed, real discrepancy, not assumed.

None of these are urgent. They're recorded so a future investigation
doesn't have to rediscover them from scratch.
