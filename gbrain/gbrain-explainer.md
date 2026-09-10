---
document: "GBrain — Explainer"
doc-id: gbrain-explainer
state: Live
date-created: 2026-09-05
---

# GBrain — Explainer

*Companion note: for current confirmed state (version, sources, credentials,
open items) see `gbrain-config.md`. For commands, incidents, and
troubleshooting, see `gbrain-reference.md`. For how the memory components fit
together, see `memory-master-explainer.md`.*

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
thirteen sources, four of them federated (participating in every other
source's search by default). A query is scoped to its own project's sources
unless told otherwise; federated sources are the mechanism by which shared
cross-project material is reachable everywhere without being named.

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
explainer.md`): four memory mechanisms — GBrain (semantic memory), Graphify
(deterministic code structure), the Dream Cycle (autonomous deepening), Memory
Governor (the durability gate) — with the authority model that orders them all
under the repository file. Both framings are recorded with provenance and
deliberately not merged: this document uses the six-component view for
operational coupling; the master explainer retains the four-mechanism view for
how memory work fits together, and owns that reasoning.

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
`gbrain-dream-cycle-explainer.md`.

**The brain's mirror can lag its sources** — sync is commit-based; content is
current only as of the last synced commit. The file wins.

---

*Companion documents: `gbrain-config.md` (state), `gbrain-reference.md`
(commands, incidents), `gbrain-dream-cycle-explainer.md` (the autonomous
mechanism), `memory-master-explainer.md` (the cross-component system).*
