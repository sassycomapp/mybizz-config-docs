---
title: "gbrain-explainer"
doc-id: "mb-3187a352"
updated: "2026-10-20"
---
# GBrain — Explainer

*Companion note: for current confirmed state (version, sources, credentials)
see [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md). For commands, incidents, and
troubleshooting, see [[[mybizz-config-docs:gbrain/gbrain-reference|Reference]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md). For how the memory
components fit together, see
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md).
[[[mybizz-config-docs:gbrain/gbrain-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-learnings.md) holds what differs from the standard in this
setup.*

---

## What it is

Every AI coding session starts from nothing. Close the window, open a new one
tomorrow, and the agent has no memory of what earlier sessions decided, what
they tried and abandoned, or what conversation led to the current state of a
file. GBrain
exists to fix that: a persistent, searchable memory layer sitting outside any
single conversation.

It is not authoritative — it is memory in the ordinary sense: useful,
searchable, sometimes stale, never the final word over a real file. That
distinction is the foundation everything else rests on: **GBrain can be wrong,
and when it disagrees with an actual file, the file wins, always.**

GBrain reads project repositories — documentation, ADRs, specifications, and
where configured, source code — and stores them as searchable content in a
PostgreSQL database. It organizes everything into **brains** (databases) and
**sources** (registered repos inside a brain); this brain holds nineteen
sources, seventeen of them federated (participating in every other source's
search by default). A query is scoped to its own project's sources unless told
otherwise; federated sources are the mechanism by which shared cross-project
material is reachable everywhere without being named.

A source is `federated`, `unset` or `isolated`. `unset` (never set) keeps a
source out of other sources' searches, while a session working inside it can
still read the federated sources — the state of `memory-governor-code`.
`isolated` (set explicitly with `sources unfederate`) cuts a source off in
both directions — the state of the Anvil clone
(`anvil-agent-references-code`). Those two are kept out of the search on
purpose: Graphify handles code, and every other source is federated.
Application code is not indexed in GBrain at all — agents read app code
directly from the app folders; the sources are the project libraries, the
documentation repositories, the mb-* skill folders, and the two system-code
exceptions above.

**Links between sources.** A link written `[[source-id:page-name]]` connects
to that page in the named source, provided the page holding the link is in a
federated source. Bare names and ordinary markdown links cannot cross sources,
and a wrong page name is dropped. The page name is GBrain's slug: lowercase,
spaces as hyphens, no `.md`, the path counted from the root of the target
repository. These links are written only by the full database read that the
standing sync script ends with — never by a plain sync, and not by the
stale-page pass, because the sync has already marked its pages as done.

In the documents themselves every link is stored as
`[[[source-id:page-name]]](C:/full/path.md)`: GBrain reads the part inside the
brackets, MarkText opens the path. A link with only a bare name inside the
wrapper is not followed by this version.

Search is hybrid: exact keyword matching combined with vector-based semantic
matching (content embedded via an external model, so meaning-similar text is
mathematically close even with zero shared words), optionally expanded by an
LLM to catch related phrasings. **Schema packs govern what structure gets
extracted** — a page type marked `extractable: false` in the active pack is
indexed for search but nothing more is ever built from it; this single
mechanic is the entire reason the code call-graph doesn't work through GBrain
(see the call-graph limitation under Why it works this way).

Everything GBrain produces is advisory. Nothing that builds, deploys, or
enforces reads it; no path exists by which GBrain's stored belief silently
overrides a real file. Its entire value is reducing re-reading and
re-explaining — not competing with the first source of truth.

## What it can do

- **Persistent cross-session memory** — documents, decisions, ADRs, and code stored as searchable content that survives every session boundary.
- **Hybrid semantic search** — keyword + vector + LLM query expansion, so queries find conceptually related content with different wording.
- **Source-scoped or federated retrieval** — per-project scoping by default, explicit cross-source reach, and federated sources for shared material.
- **Code-symbol lookup** — definition and reference finding (`code-def`/`code-refs`) across indexed code sources.
- **Structured extraction governed by schema packs** — page types, link types, and per-type extractability determining what becomes queryable structure.
- **Multi-hop synthesis** (`think`) — composed, cited answers across pages, takes, and the knowledge graph, with gap analysis.
- **Background deepening** — the Dream Cycle consolidates, extracts, and maintains the brain; it runs by hand weekly (its own document suite).
- **An MCP tool surface inside OpenCode** — the full operation wall plus the memory verbs, served per process boot.

## Suitability

**Best for:** answering "where is this handled / what does the codebase look
like / what did past sessions decide" questions across sessions and projects;
making cross-project institutional knowledge reachable without re-reading
everything; holding the reasoning behind decisions (ADRs, specs, incident
history) where a semantic query can find it.

**Good for:** code orientation via symbol lookup (`code-def`/`code-refs`);
advisory cross-checks where a second, independent source of context is useful
(the master explainer's worked example: GBrain's sourced-document answer
agreeing with Graphify's EXTRACTED edges); maintaining searchability of
inactive projects' history at near-zero cost.

**Not good for:** anything requiring a mechanically enforced guarantee —
GBrain is advisory by design; nothing that builds or enforces reads it.
Cross-file call-graph resolution — a permanent, double-verified limitation
(see Why it works this way); Graphify owns that job. Answers where staleness
is unacceptable without verification — GBrain content can lag the repos it
mirrors; the file wins. And it is not a general knowledge product: upstream
GBrain has grown far beyond this environment's slice (see Upstream scope) —
bootstrap personal agents, company brains, and connector ingestion are
upstream capabilities this environment deliberately does not run.

## Why it works this way

### Why PostgreSQL

GBrain runs on PostgreSQL because it is genuinely multi-writer — many
processes read and write safely at once. An embedded, single-writer database
cannot do that: OpenCode holding its lock during a sync corrupts it, which is
exactly the failure that forced the architecture change. That single fact is
why GBrain is trustworthy in a multi-process environment. `pgvector` is what
makes semantic search possible — meaning-as-vectors, so similar meaning lands
mathematically close even with no shared words.

GBrain's Postgres instance is deliberately separate from PDLF's own ledger
database: a higher-churn, LLM-driven workload with real failure modes must
never be able to reach the correctness-critical build ledger.

### Providers and keys

GBrain embeds and expands via external providers — it reasons about nothing
itself. Embeddings: OpenAI (`text-embedding-3-large`); chat/expansion:
`gpt-5.2`. Anthropic models cannot perform embeddings at all — a structural
gap, not a missing-key state. API keys live in the environment only, never in
GBrain's own config file in plaintext — a confirmed exposure discipline, not
a preference. (The config file does carry the local database URL; masked
throughout this suite per the standing masking decision — config.md.)

### Reranking and search timing

GBrain finds candidate passages by meaning and by keyword, then sends the best 25 to Voyage's `rerank-2.5` model, which orders them by how well each one answers the question. Reranking puts the right document first far more often than either method alone.

Voyage usually answers in under two seconds, but some answers take close to ten. GBrain therefore waits up to 20 seconds. If Voyage still has not answered, search returns its results in their unranked order instead of failing, so a slow reranker never stops a search.

Before searching, OpenAI turns the question into numbers. OpenAI's first call in a session can take about seven seconds, so GBrain waits up to 15 seconds for it.

Two WSL settings keep these calls reliable. Addresses are tried IPv4 first, because WSL has no working IPv6 route and an IPv6 attempt hangs until it times out. Only Windows sets the WSL clock, because a second time service inside WSL made the clock jump, and every jump cut calls short.

Voyage only gives full speed to an account with a payment method on the organization that holds the API key. Without one, it allows three requests a minute, which a few searches use up.

### Upstream scope — a larger product than this environment runs

Upstream (`github.com/garrytan/gbrain`, MIT, by Garry Tan) has grown into a
full personal/company brain product: bootstrap personal-agent flows, company
brains with per-user scoping, Google/calendar connectors, transcript and chat
ingestion, ambient memory writeback, LLM-as-judge oversight, HTTP MCP with
OAuth, and schema authoring. **This environment deliberately runs a narrow
slice:** Postgres engine, the `gbrain-everything` pack, OpenCode stdio MCP,
source-sync as the ingestion model, and the Dream Cycle run by hand weekly.
No 24/7 daemon, no identity layer, no connector ingestion, no scheduled
cycles — autopilot is off by decision. The suite documents this slice;
upstream docs cover the rest.

**One upstream warning worth carrying verbatim in practice:** GBrain is not
distributed on npm — the npm package named `gbrain` is unrelated and will
shadow the real binary. Install/upgrade only via the documented GitHub paths.

### The permanent call-graph limitation

`code-callers`/`code-callees` sound like they resolve what calls what across a
codebase. They don't, for two independent, verified reasons: the symbol
resolver works within-file only, and — decisively — the `code` page type is
`extractable: false` in every bundled schema pack, including
`gbrain-everything`. No pack switch fixes it — investigated, confirmed a dead
end, and formally accepted as permanent. The practical
consequence: those commands return symbol names, not confirmed links.
**Graphify's `get_neighbors` does the identical job correctly** — fully
resolved, typed, cross-file edges. The working rule: for "what calls/imports/
contains what," reach for Graphify.

### Where GBrain sits — the six-component system

**The developer's framing:** GBrain is one of six closely-related components
— **GBrain, gbrain-dream-cycle, gstack, memory-governor, PostgreSQL, and the
installed `mb-submit-memory` skill** — so interrelated that assessing one
without the others is unreliable. The couplings are structural, not
incidental: PostgreSQL is GBrain's foundation; the Dream Cycle is GBrain's own
deepening process; `mb-submit-memory` is the entry to the governed write path
— the only way content becomes *governed* durable memory (facts layer, via
Memory Governor's async `remember` write), while corpus pages arrive through
sync — two complementary layers, neither superseding the other, with
sync-into-governance explicitly prohibited by design. And `mb-submit-memory`
is, by documented design intent, "the only sanctioned way a developer or a
PDLF step submits real content into memory" — the deliberate replacement for
habit-driven raw sync/remember writes **for governed memory claims
specifically**; corpus indexing is not that job. Memory Governor decides
what reaches durable memory and structurally cannot intercept the Dream Cycle
— a permanent limit that makes the governed path the only governed one.
GStack supplies both the integration skills and the model for the sync
discipline.

**The memory master explainer's framing** (`mybizz-os-docs/memory-master-
explainer.md`): the full memory family — GBrain, the dream cycle,
memory-governor (with its API), mb-submit-memory, and Graphify, with
PostgreSQL and Cupcake indirectly related — integrated as one ecosystem, with
the authority model that orders them all under the repository file. This
document uses the six-component view for operational coupling; the master
explainer owns the whole-ecosystem integration view.

### The writer-model boundary

GBrain's upstream writer/ownership model — claiming a source so an agent can
write pages into it directly — is not adopted. Claiming stops ordinary sync
until activation is complete, so adoption is deferred and decided together
with the next GBrain upgrade, as one planned change. Until then the
command-line page-write path refuses with `owner_unavailable`, session pages
are written as files and imported by commit all, and the database fact path
(`remember`, `forget`) carries the governed memory.

### Integration with OpenCode and GStack

Inside OpenCode, GBrain is a local MCP server started once at process boot —
config changes need a full restart, never just a new chat. The installed
`/sync-gbrain` skill wraps sync and dream commands and maintains a
`GBrain Search Guidance` block in project guidance files. The upstream gstack
integration (`/setup-gbrain`, per-remote trust triad, 3-stage sync) is
installed but is not this environment's operational path — the custom sync
script is. One real overlap trap: the gstack orchestrator derives its own
source IDs and fails on path overlap with manually registered sources; run
the dream cycle directly against the existing source instead (command in the
reference).

GBrain ships its own agent skills, and none of them is installed. GBrain
serves here as the search index over the documentation repositories, not as a
personal knowledge base, so its intake skills have nothing to work on. Its
administration skills would let an agent set up, upgrade or repair GBrain,
and those actions are reserved for the developer. Its search skills would
give agents a second set of rules for GBrain beside `mb-submit-memory` and
the memory governor, and one job has one set of rules.

### Known limitations, honestly stated

**The call graph only resolves same-file references, and no schema pack
extracts it at all** — see the call-graph limitation above; the single most
important limitation to carry forward.

**MCP integrations require a full process restart** — see Integration with
OpenCode and GStack; silent absence, no error, when changed mid-process.

**Dream Cycle failures can be silent** — provider-dependent phases can fail
while GBrain remains healthy, and "completed successfully" means the sequence
ended, not that every phase did meaningful work. See
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-explainer|Dream Cycle Explainer]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-explainer.md).

**The brain's mirror can lag its sources** — sync is commit-based; content is
current only as of the last synced commit. The file wins.

**Facts are stored per source.** `remember` writes into the source that the
call selects, and `recall` reads the facts of that one source. The memory
governor names the owning project's own documentation source on every write,
so its facts sit with the documents they belong to (see the governor
explainer).

**A stale brain default stops sync.** The memory governor changes the
brain-level default source with every write; the sync script resets it back
before every run. A default that names a deleted source makes every sync end
with an error — the incident playbook is in the reference.

## What has to happen

- **The developer runs the Dream Cycle by hand weekly**, after the Sunday backup, through the memory diagnostic (`mb-memory-system-diagnostic`). Nothing GBrain-related is scheduled; autopilot stays off.
- **The sync runs with every commit all** (the standing script). Files moved or deleted in a source need a full resync of that source, or their pages linger in the brain.
- **API keys stay in the environment**, and the Voyage payment method stays on the organization that holds the key — the reranker degrades to three requests a minute without it.
- **The Sunday backup cycle keeps covering the `gbrain` and `memory_governor` databases** (the estate convention is owned by the PostgreSQL suite).
- **Several checks stay developer-run**: `config.json` content (the sensitive-data guard), full sync samples (content-changing), MCP restart behavior, and any upgrade decision.
- **The master explainer is passed to every memory-component run** and updated by each such session, committed and pushed at that run's close-out — standing authorization.
- **This suite is kept current by `mb-sysdoc-creator` research runs** against the doc-suite specification.

## S.W.O.T.

**Strengths.** Division-wide memory at scale (2,244 pages with 100% embedding
coverage at the last research); multi-source federation across every project
repo; a scripted sync path that covers every registered source; a scripted,
backed-up upgrade procedure; the schema-pack system pins structure (30/12)
and is verified via cheap MCP calls.

**Weaknesses.** The live install is a Git checkout in detached HEAD on a
release tag, with a local commit parked on `master`; several checks are
permanently developer-run (config.json content, sync samples); per-source
dream-cycle freshness lags for sources that rarely cycle; the call-graph
limitation above.

**Opportunities.** Silent memory degradation — coverage decay, source drift,
sync failure — is detectable on demand through the doctor health check and
the suite refresh loop; every incident becomes a spec-refresh rather than
undocumented drift.

**Threats.** Unsynced mirrors silently diverge from their sources (sync is
commit-based); a failed upgrade would be self-inflicted (policy guards
against newness-driven upgrades, and the procedure is scripted and backed
up); the brain default source is changed by the memory governor and can go
stale, which stops every sync.

---

*Suite: [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) (state),
[[[mybizz-config-docs:gbrain/gbrain-reference|Reference]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) (commands, incidents),
[[[mybizz-config-docs:gbrain/gbrain-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-learnings.md) (what differs and why).
Related: [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-explainer|Dream Cycle Explainer]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-explainer.md) (the deepening mechanism),
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) (the cross-component system).*

*End of document*
