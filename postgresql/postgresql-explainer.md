---
title: "postgresql-explainer"
doc-id: "mb-e4410ed0"
updated: "2026-10-14"
---
# PostgreSQL — Explainer

Companion to [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) (every setting and value — the spec),
[[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md) (commands and procedures for agents),
Exam Plan (next exam's job-spec), Exam Report
(current verified state), Log (notable events),
[[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md) (transient exam knowledge). This document is for any
reader — human developer, visiting technical consultant, or agent: what
PostgreSQL is doing across this whole system, database by database — what each
one is, what component of Mybizz actually uses it, and why it exists at all.
Current figures (sizes, counts, versions) live in the configuration, not here.

---

## The two PostgreSQL installations at a glance

This machine runs **two separate PostgreSQL installations. Both are installed,
running and needed; neither replaces the other.** Each serves a different part
of the system:

| | Instance A | Instance B |
|---|---|---|
| Program | PostgreSQL 15 | PostgreSQL 16 |
| Runs on | Windows | WSL installation `Ubuntu` (Ubuntu 24.04) |
| Serves | PDLF — the `pdlf` build ledger | GBrain (`gbrain`) and the Memory Governor (`memory_governor`) |
| Port | `5433` | `5432` |
| Reached from WSL | PowerShell bridge, always with `-p 5433` | directly, `localhost:5432` |
| Starts | automatically with Windows (service `postgresql-x64-15`) | automatically with WSL (systemd, `postgresql.service`) |
| Current use | running; the ledger's tables stay empty until PDLF runs a real project | running; holds GBrain's memory and the governor's records |

**The rule that follows:** every database command names its instance and its
port. Port 5432 reaches Instance B from both sides of the WSL boundary, so a
command meant for the ledger that omits `-p 5433` reaches GBrain's server
instead, without any error.

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
the supporting-systems, PDLF and shipped layers): Instance B (WSL, PostgreSQL 16)
hosts the **supporting-systems layer's** memory — GBrain and the memory governor
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
writer needs ([[[default:security-global/infrastructure/sec-database-access-control|Database Access Control]]](C:/dev/project-library-global/security-global/infrastructure/sec-database-access-control.md), which cites this exact
arrangement as its verified precedent).

**Instance A**, on Windows, runs PostgreSQL 15 and hosts `pdlf`.
**Instance B**, inside WSL, runs PostgreSQL 16 and hosts `gbrain` and
`memory_governor`.

The two servers listen on different ports by design: Instance B (WSL) keeps
the default 5432, and Instance A (Windows) listens on **5433**. The reason
is this machine's port topology: Windows port 5432 is WSL's localhost relay
to Instance B, so 5432 serves Instance B from *both* sides of the WSL
boundary — a bare connection to it reaches the memory system's server
whether it comes from WSL or Windows. That is the single most operationally
dangerous fact about this arrangement: a database call made from the wrong
side — or to the ledger without its port — connects to the wrong server
*silently*. See
[[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md) for the rules that prevent it.

---

## 2. `gbrain` — the memory system's content store (Instance B, WSL)

**What it is:** the actual database behind GBrain, the tool that gives
every project in this system a searchable, synthesized memory of its own
documentation and code. When you run `gbrain sync`, this is where the
content ends up. When an agent runs `gbrain search` or `gbrain think`, this
is what's being queried.

**What's inside:** every page from every registered GBrain source, split
into chunks, each carrying a 1,536-dimension vector embedding, so that
searches can match meaning as well as words. Every table has row-level
security enabled. It grows with every sync; the current page, chunk and
table counts are in the configuration.

**Who uses it:** every GBrain source registered on this machine (listed in
`repo-organization.md`) writes into and is read out of this one database. It's the shared
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
actually pushes approved content into GBrain), and `audit_log`.

**Who uses it:** the `mb-submit-memory` skill (the only sanctioned,
developer-facing way to submit content into memory), PDLF's own
step-completion process (once PDLF is actually running steps), and — by
design, and only by design — nothing else. GBrain's own automatic "dream
cycle" enrichment is deliberately unable to route through this database at
all; that's a confirmed, permanent architectural limitation, not an
oversight, documented in [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md).

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
the build framework at `C:\pdlf`. Every step the PDLF
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

**The schema matches its specification**, and the specification is
authoritative for column-level detail.

**Who uses it:** the PDLF orchestrator itself, and nothing else. This
database isn't meant to be touched directly by any other part of the
system — reads and writes to it are supposed to happen only through a
real PDLF step, per its own governing principle.

**Why it's on Windows, separate from everything else:** partly the
isolation reasoning from Section 1, and partly practical — this predates
some of the WSL-centric tooling and was set up as a standalone Windows
service. The real operational cost of that choice is that reaching it from
WSL requires a PowerShell bridge rather than a direct connection — covered
fully in [[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md). That cost is worth stating plainly:
the bridge exists because WSL cannot pass environment variables to Windows
programs, and because the ledger's port must always be named explicitly —
`localhost:5432` serves Instance B from both sides of the boundary, so only
`-p 5433` reaches the ledger. The same fact that makes the memory system's
own database calls safe from accidental cross-connection.

---

## 5. Objects that must stay absent

Three things that once existed on these servers must not come back, and every
exam checks that they have not:

- **The `compliance_ledger` database (Instance B).** Despite its name, it was
  never the real ledger; the real ledger is `pdlf` on Instance A.
- **User tables and the `vecs` schema in Instance A's `postgres` admin
  database.** The admin database holds PostgreSQL's own catalogs only.
- **The `pgvector_user` and `pgvector_readonly` roles (Instance A).** They
  belonged to earlier memory experiments that GBrain replaced.

They were leftovers of early experiments, and each was backed up before
removal; the backups are listed in the configuration. If any reappears, it
means something is recreating it, and that is a finding to investigate.

---

## 6. The two-databases trap — why the ledger's port must be explicit

Port 5432 serves **one** server everywhere: Instance B. WSL's PostgreSQL 16
listens on 5432 natively, and WSL's localhost relay binds Windows' 5432 to
that same Instance B — so from either side of the WSL boundary, a bare
connection to 5432 reaches `gbrain`'s cluster. The PDLF ledger (Instance A)
therefore listens on **5433** from the Windows side, and every ledger
command names that port explicitly.

The trap this prevents is a silent one: a database call made without the
bridge (from WSL) or without `-p 5433` (from Windows) does not fail
visibly — it connects to Instance B. The memory system's own database
checks have the same property in reverse, which is why every database
check names its instance and its port explicitly.

The working rules that prevent it (enforced in
[[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md)): all `pdlf` access goes through the PowerShell
bridge with `-p 5433`; all GBrain/governor access runs inside WSL; and any
database check names its instance explicitly.

---

## 7. The layer placement — where each database sits in the environment

Per the supporting-systems, PDLF and shipped layers:

- **Instance B (WSL PostgreSQL 16) is supporting-systems-layer infrastructure.**
  GBrain and the memory governor are supporting systems built before and
  beneath PDLF; their databases exist to serve the building of PDLF and,
  later, the building of web applications through it.
- **Instance A's `pdlf` database is PDLF-layer material.** The ledger is
  the record the PDLF application itself writes as it orchestrates builds
  — it comes into real use only when the PDLF layer runs real projects.
- **The shipped estate contains no PostgreSQL at all.** Client instances
  hold their data in Anvil's own Data Tables (per
  [[[default:adr-global/adr-client-instance-architecture|Client Instance Architecture]]](C:/dev/project-library-global/adr-global/adr-client-instance-architecture.md)), not in any database of ours. The
  shipped estate is out of scope for both PostgreSQL instances, exactly as
  it is out of scope for every developer-side system.

This placement is why the two-databases trap matters at all: the layers
are served by different servers, so a tool call that crosses a layer
boundary without the bridge silently lands in the wrong one.

---

## 8. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md) — tuned on this suite
first. The short local version:

- [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) is the **spec** — the ideal state every exam checks against.
- Before each exam run, the config-manager synthesizes Exam Plan:
  a fresh job-spec built from this spec, the last report, the log, and the
  learnings — carrying forward what was deferred, deriving probes from new log
  events, and folding in lessons not yet graduated. The plan is transient.
- The exam runs the installed skill (`mb-config-postgresql`) with the plan in
  hand — detection fully autonomous; healing only through the developer gate.
  Some checks are permanently **developer-run** (log scans, `.env`-dependent
  probes, superuser checks) — agent tooling is guard-blocked on them by design.
- The run rewrites Exam Report (current state, no history),
  appends one row to Log, files new learnings, and prunes
  absorbed log/learning entries.
- What may be healed is allowlisted in the plan; a spec correction is
  proposed at the gate and applied only after the developer approves it.

## 9. S.W.O.T.

**Strengths.** Physical isolation of high-stakes from high-churn data (two
servers, layered placement); verified 100% embedding coverage; strict role
scoping per instance (`pdlf_agent`, `memory_governor_svc` cannot cross); proven
boot durability; two independent guard layers against destructive SQL.

**Weaknesses.** The silent cross-connection trap (a bare port resolves to
Instance B from both sides of the WSL boundary) is permanent and relies on
discipline + bridge rules; several checks are permanently developer-run
(guard-forbidden to agents), so full examination coverage requires developer
participation; the dead duplicate Windows service remains registered
(cosmetic, but a permanent confusion risk).

**Opportunities.** The plan-driven exam cycle gives every system the same
exam discipline; Tier-3 checks (backup existence, a third-instance sweep) can
become routine.

**Threats.** A WSL shutdown without the clean shutdown procedure can leave
a stale pid file (documented, self-resolving); unvalidated policy/scaffold
content elsewhere in the system
has historically crashed whole subsystems (the Cupcake 7F lesson) — the same
class of risk applies to any future extension or role added carelessly;
spec-doc drift between runs would silently weaken the exam (mitigated: the
exam flags spec drift itself).

## 10. Closing

PostgreSQL's job across this environment is narrow: hold the records that
must survive — GBrain's memory, the governor's bookkeeping, PDLF's build
ledger — in two deliberately separate servers, each scoped to its own
consumers, each with its own roles, and each starting automatically: Instance
A with Windows, Instance B with WSL. The discipline that keeps them healthy is
the same everywhere: check directly, verify at each step, name the instance
and port in every command, and never let a database you did not create remain
a mystery.

---

*Companion documents: [[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) (spec),
[[[mybizz-config-docs:postgresql/postgresql-reference|Reference: Commands, Procedures, and Troubleshooting]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-reference.md) (commands), Exam Plan (next run),
Exam Report (current state), Log (events),
[[[mybizz-config-docs:postgresql/postgresql-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-learnings.md) (transient knowledge). The architecture standard:
[[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md). The layer map:
the supporting-systems, PDLF and shipped layers. The
memory system: [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md), `mb-submit-memory` (its own suites).
The ledger contract: [[[pdlf:pdlf-library/specifications-local/spec-postgres-ledger|Spec Postgres Ledger]]](C:/pdlf/pdlf-library/specifications-local/spec-postgres-ledger.md) (PDLF).*

*End of document*
