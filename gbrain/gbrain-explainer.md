---
title: "gbrain-explainer"
doc-id: "mb-3187a352"
updated: "2026-10-01"
---
# GBrain — Explainer

*Companion note: for current confirmed state (version, sources, credentials,
open items) see [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md). For commands, incidents, and
troubleshooting, see [[[mybizz-config-docs:gbrain/gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md). For how the memory components fit
together, see [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md). Exam companions:
[[[mybizz-config-docs:gbrain/gbrain-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-plan.md) (next run's job-spec), [[[mybizz-config-docs:gbrain/gbrain-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md) (current
verified state), [[[mybizz-config-docs:gbrain/gbrain-log|Log]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-log.md) (notable events), [[[mybizz-config-docs:gbrain/gbrain-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-learnings.md)
(transient exam knowledge). The architecture standard:
[[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md).*

---

## 1. Opening

Every AI coding session starts from nothing. Close the window, open a new one
tomorrow, and the agent has no memory of what was decided, what was tried and
abandoned, or what conversation led to the current state of a file. GBrain
exists to fix that: a persistent, searchable memory layer sitting outside any
single conversation.

It is not authoritative — it is memory in the ordinary sense: useful,
searchable, sometimes stale, never the final word over a real file. That
distinction is the foundation everything else rests on: **GBrain can be wrong,
and when it disagrees with an actual file, the file wins, always.**

## 2. What GBrain Actually Is

GBrain reads project repositories — documentation, ADRs, specifications, and
where configured, source code — and stores them as searchable content in a
PostgreSQL database. It organizes everything into **brains** (databases) and
**sources** (registered repos inside a brain); this brain currently holds
fifteen sources (2026-09-30), ten of them federated (participating in every other
source's search by default). A query is scoped to its own project's sources
unless told otherwise; federated sources are the mechanism by which shared
cross-project material is reachable everywhere without being named.

A source is `federated`, `unset` or `isolated`. `unset` (never set) keeps a
source out of other sources' searches, while a session working inside it can still
read the federated sources — the state of the four code sources. `isolated` (set
explicitly with `sources unfederate`) cuts a source off in both directions — the
state of `anvil-agent-references-code`.

**Links between sources (2026-09-30).** In 0.46.1.0 a link connected only to pages
of its own source (or of the source named `default`). From 0.51.8.0 on — the
installed 0.59.18.0 included — a link written `[[source-id:page-name]]` connects
to that page in the named source, provided the page holding the link is in a
federated source. Bare names and ordinary markdown links still cannot cross
sources, and a wrong page name is dropped. The page name is GBrain's slug:
lowercase, spaces as hyphens, no `.md`, the path counted from the root of the
target repository. These links are written only when links are collected from the
database (`gbrain extract --stale`), never by a plain sync. This was tested on a
sandbox copy of 0.59.18.0 and is the reason for the upgrade; it has not yet been
exercised on this brain.

Search is hybrid: exact keyword matching combined with vector-based semantic
matching (content embedded via an external model, so meaning-similar text is
mathematically close even with zero shared words), optionally expanded by an
LLM to catch related phrasings. **Schema packs govern what structure gets
extracted** — a page type marked `extractable: false` in the active pack is
indexed for search but nothing more is ever built from it; this single
mechanic is the entire reason the code call-graph doesn't work through GBrain
(§8).

Everything GBrain produces is advisory. Nothing that builds, deploys, or
enforces reads it; no path exists by which GBrain's stored belief silently
overrides a real file. Its entire value is reducing re-reading and
re-explaining — not competing with the first source of truth.

## 3. What GBrain Can Actually Do

- **Persistent cross-session memory** — documents, decisions, ADRs, and code stored as searchable content that survives every session boundary.
- **Hybrid semantic search** — keyword + vector + LLM query expansion, so queries find conceptually related content with different wording.
- **Source-scoped or federated retrieval** — per-project scoping by default, explicit cross-source reach, and federated sources for shared material.
- **Code-symbol lookup** — definition and reference finding (`code-def`/`code-refs`) across indexed code sources.
- **Structured extraction governed by schema packs** — page types, link types, and per-type extractability determining what becomes queryable structure.
- **Multi-hop synthesis** (`think`) — composed, cited answers across pages, takes, and the knowledge graph, with gap analysis.
- **Autonomous background deepening** — the Dream Cycle consolidates, extracts, and maintains the brain on a schedule (its own document suite).
- **An MCP tool surface inside OpenCode** — the full operation wall plus the memory verbs, served per process boot.

## 4. Suitability

**Best for:** answering "what did we decide / where is this handled / what
does the codebase look like" questions across sessions and projects; making
cross-project institutional knowledge reachable without re-reading everything;
holding the reasoning behind decisions (ADRs, specs, incident history) where a
semantic query can find it.

**Good for:** code orientation via symbol lookup (`code-def`/`code-refs`);
advisory cross-checks where a second, independent source of context is useful
(the master explainer's worked example: GBrain's sourced-document answer
agreeing with Graphify's EXTRACTED edges); maintaining searchability of
inactive projects' history at near-zero cost.

**Not good for:** anything requiring a mechanically enforced guarantee —
GBrain is advisory by design; nothing that builds or enforces reads it.
Cross-file call-graph resolution — a permanent, double-verified limitation
(§8); Graphify owns that job. Answers where staleness is unacceptable without
verification — GBrain content can lag the repos it mirrors; the file wins.
And it is not a general knowledge product: upstream GBrain has grown far
beyond this environment's slice (§7) — bootstrap personal agents, company
brains, and connector ingestion are upstream capabilities this environment
deliberately does not run.

## 5. Why PostgreSQL — The Foundation

GBrain originally ran on PGLite — an embedded, single-writer database. That
architecture's weakness stopped being theoretical: a real corruption incident
occurred when OpenCode held the lock during a sync. The fix was architectural,
not procedural: PostgreSQL is genuinely multi-writer, built for many processes
reading and writing safely at once. That single fact is why GBrain is
trustworthy today in a way it wasn't before. The legacy PGLite artifact remains
on disk, stale and unused. `pgvector` is what makes semantic search possible —
meaning-as-vectors, so similar meaning lands mathematically close even with no
shared words.

GBrain's Postgres instance is deliberately separate from PDLF's own ledger
database: a higher-churn, LLM-driven workload with real failure modes must
never be able to reach the correctness-critical build ledger.

## 6. Providers and Keys

GBrain embeds and expands via external providers — it reasons about nothing
itself. Embeddings: OpenAI (`text-embedding-3-large`); chat/expansion:
`gpt-5.2`. Anthropic models cannot perform embeddings at all — a structural
gap, not a missing-key state. API keys live in the environment only, never in
GBrain's own config file in plaintext — a confirmed exposure discipline, not
a preference. (The config file does carry the local database URL; masked
throughout this suite per the standing masking decision — config.md.)

## 7. Upstream Scope — A Larger Product Than This Environment Runs

Upstream (`github.com/garrytan/gbrain`, MIT, by Garry Tan) has grown into a
full personal/company brain product: bootstrap personal-agent flows, company
brains with per-user scoping, Google/calendar connectors, transcript and chat
ingestion, ambient memory writeback, LLM-as-judge oversight, HTTP MCP with
OAuth, and schema authoring. **This environment deliberately runs a narrow
slice:** Postgres engine, the `gbrain-everything` pack, OpenCode stdio MCP,
source-sync as the ingestion model, and the Dream Cycle invoked manually on
demand. The one autonomous mechanism upstream ships — the `gbrain autopilot`
daemon — was found here as an installed-but-doubly-inert cron entry (cron not
running; a target path dead since the pre-`C:\dev` layout; its log never
created) and was deliberately removed on 2026-09-06: no 24/7 daemon, no
identity layer, no connector ingestion, and no scheduled cycles. The suite
documents this slice; upstream docs cover the rest.

**One upstream warning worth carrying verbatim in practice:** GBrain is not
distributed on npm — the npm package named `gbrain` is unrelated and will
shadow the real binary. Install/upgrade only via the documented GitHub paths.

## 8. The Permanent Call-Graph Limitation

`code-callers`/`code-callees` sound like they resolve what calls what across a
codebase. They don't, for two independent, verified reasons: the symbol
resolver works within-file only, and — decisively — the `code` page type is
`extractable: false` in every bundled schema pack, including
`gbrain-everything`. No pack switch fixes it; it was investigated and
confirmed a dead end, and is formally accepted as permanent. The practical
consequence: those commands return symbol names, not confirmed links.
**Graphify's `get_neighbors` does the identical job correctly** — fully
resolved, typed, cross-file edges. The working rule: for "what calls/imports/
contains what," reach for Graphify.

## 9. Where GBrain Sits — The Six-Component System

**The developer's framing (developer-stated, 2026-09-06):** GBrain is one of
six closely-related components — **GBrain, gbrain-dream-cycle, gstack,
memory-governor, PostgreSQL, and the installed `mb-submit-memory` skill** —
so interrelated that assessing one without the others is unreliable. The
couplings are structural, not incidental: PostgreSQL is GBrain's foundation;
the Dream Cycle is GBrain's own autonomous deepening process;
`mb-submit-memory` is the entry to the governed write path — the only way
content becomes *governed* durable memory (facts layer, via Memory Governor's
async `remember` write), while corpus pages arrive through sync — two
complementary layers, neither superseding the other, with sync-into-governance
explicitly prohibited by design. And `mb-submit-memory` is, by documented
design intent, "the only sanctioned way a developer or a PDLF step submits
real content into memory" — the deliberate replacement for habit-driven raw
sync/remember writes **for governed memory claims specifically**; corpus
indexing was never that job. Memory Governor decides what reaches durable
memory and structurally cannot intercept the Dream Cycle — a permanent limit
that makes the governed path the only governed one. GStack supplies both the
integration skills and the model for the sync discipline.

**The memory master explainer's framing** (`mybizz-os-docs/memory-master-
explainer.md`): the full memory family — GBrain, the dream cycle,
memory-governor (with its API), mb-submit-memory, and Graphify, with PostgreSQL
and Cupcake indirectly related — integrated as one ecosystem, with the
authority model that orders them all under the repository file. This document
uses the six-component view for operational coupling; the master explainer owns
the whole-ecosystem integration view.

**Maintenance obligation (settled, 2026-09-06):** the master explainer is
passed to every memory-component run and updated by each such session,
committed and pushed to `mybizz-os-docs` at that run's close-out — standing
authorization, not re-decided per run.

## 10. Integration With OpenCode and GStack

Inside OpenCode, GBrain is a local MCP server started once at process boot —
config changes need a full restart, never just a new chat. The installed
`/sync-gbrain` skill wraps sync and dream commands and maintains a
`GBrain Search Guidance` block in project guidance files. The upstream gstack
integration (`/setup-gbrain`, per-remote trust triad, 3-stage sync) is
installed but is not this environment's operational path — the custom sync
script is. One real overlap trap: the gstack orchestrator derives its own
source IDs and fails on path overlap with manually registered sources; run
`gbrain dream --source <id>` directly against the existing source instead.

## 11. Known Limitations, Honestly Stated

**The call graph only resolves same-file references, and no schema pack
extracts it at all** — §8; the single most important limitation to carry
forward.

**MCP integrations require a full process restart** — §10; silent absence, no
error, when changed mid-process.

**Dream Cycle failures can be silent** — provider-dependent phases can fail
while GBrain remains healthy, and "completed successfully" means the sequence
ended, not that every phase did meaningful work. See
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-explainer.md).

**The brain's mirror can lag its sources** — sync is commit-based; content is
current only as of the last synced commit. The file wins.

**Facts are stored per source.** `remember` writes into the source that the call
selects, and `recall` reads it (0.59.18.0: also every federated source, unless a
source is given). The memory governor's facts therefore sit in
`memory-governor-code` — see [[[mybizz-config-docs:memory-governor/memory-governor-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-explainer.md) §5.

**A stale brain default stops sync.** The memory governor changes the brain-level
default source with every write. In 0.59.18.0 a default that names a deleted
source makes every sync end with an error (incident 2026-09-30, in the reference).

## 12. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md) — emulated from the
PostgreSQL pilot. The short local version:

- [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) is the **spec** — the ideal state every exam checks against.
- Before each exam run, the config-manager synthesizes [[[mybizz-config-docs:gbrain/gbrain-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-plan.md):
  a fresh job-spec built from this spec, the last report, the log, and the
  learnings — carrying forward what was deferred, addressing what erred,
  deriving probes from new log events, and folding in lessons not yet graduated.
  The plan is transient (the file is live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-gbrain`) with the plan in hand —
  detection fully autonomous; healing gated. **No live-system heals are defined
  for gbrain**: sync, schema changes, upgrades, source registration are all
  state changes to a memory system governed elsewhere — diagnosis and proposal
  only, every change through the developer gate.
- **Scope boundary with the postgres module:** database-level facts (tables,
  RLS, roles, extensions, embedding coverage) belong to `mb-config-postgresql`'s
  exam; this exam cross-references its current report instead of re-probing.
- Several checks are permanently **developer-run**: config.json content (the
  sensitive-data guard blocks agent reads — proven), full sync samples
  (content-changing), MCP restart behavior, and any upgrade decision.
- The run rewrites [[[mybizz-config-docs:gbrain/gbrain-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md) (current state, no history), appends
  one row to [[[mybizz-config-docs:gbrain/gbrain-log|Log]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-log.md), files new learnings, and prunes absorbed entries.

## 13. S.W.O.T.

**Strengths.** Division-wide memory proven at scale (2,400+ pages per the
doctor of 2026-09-30, 100% embedding coverage verified independently on
2026-09-13); multi-source federation across every project repo; a proven sync path
(the standing script syncs every registered source; the failures recorded on
2026-09-30 — a stale brain default, one network lookup error and one invalid-YAML
file — were all resolved); a scripted, backed-up upgrade procedure (proven
2026-09-30); the
schema-pack system pins structure (30/12) and is verified via cheap MCP calls.

**Weaknesses.** The live install is a Git checkout in detached HEAD on a release
tag, with a local commit parked on `master` (the stale source clone was deleted
2026-09-13); page-accounting between sources and identity totals was unexplained
at pilot (273 pages — on 2026-09-30 the doctor reported 273 database pages with no
backing file before the upgrade and 30 after); several checks are permanently
developer-run (config.json content, sync samples); the version lags upstream
(0.59.18.0 installed, 0.60.11.0 exists) by deliberate policy; the dream cycle has
not run for most sources (an accepted `cycle_freshness` FAIL).

**Opportunities.** The config-management exam makes silent memory degradation —
coverage decay, source drift, sync failure — detectable on demand; the
plan-driven cycle means every incident (e.g. the pdlf source appearing) becomes
a spec-refresh loop rather than undocumented drift.

**Threats.** Unsynced mirrors silently diverge from their sources (sync is
commit-based); a failed upgrade would be self-inflicted (policy guards against
newness-driven upgrades; the upgrade of 2026-09-30 was scripted and backed up);
the brain default source is changed by the memory governor and can go stale, which
stops every sync.

---

*Suite: [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) (spec), [[[mybizz-config-docs:gbrain/gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) (commands, incidents),
[[[mybizz-config-docs:gbrain/gbrain-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-plan.md) / [[[mybizz-config-docs:gbrain/gbrain-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md) / [[[mybizz-config-docs:gbrain/gbrain-log|Log]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-log.md) /
[[[mybizz-config-docs:gbrain/gbrain-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-learnings.md) (config-management set), [[[mybizz-config-docs:gbrain/gbrain-skill|Gbrain Skill]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-skill.md) (exam skill
canonical source). Architecture: [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md).
Related: [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-explainer.md) (the autonomous mechanism),
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) (the cross-component system).*

*End of document*
