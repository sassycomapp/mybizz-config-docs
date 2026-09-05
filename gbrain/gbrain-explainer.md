# GBrain Explainer

## 1. Opening

Every AI coding session starts from nothing. Close the window, open a new one tomorrow, and the agent has no memory of what was decided, what was tried and abandoned, what the codebase actually looks like, or what conversation led to the current state of a file. It has to be told again, every time, or it has to guess — and guessing is where mistakes live.

GBrain exists to fix that specific problem. It is a persistent memory layer, sitting outside any single conversation, that stores what has been written, decided, and built, and makes it searchable the next time an agent — or you — needs to know something without re-reading everything from scratch.

It is not a replacement for your own documents. It is not authoritative. It is memory in the ordinary sense: useful, searchable, sometimes stale, and never the final word over what's actually written down in a real file. That distinction matters enough to state plainly before anything else: **GBrain can be wrong, and when it disagrees with an actual file, the file wins, always.**

---

## 2. What GBrain Actually Is

GBrain reads project repositories — documentation, ADRs, specifications, and, where configured, actual source code — and stores them as searchable content in a database. When an agent needs to answer "where is this handled?" or "what did we decide about X?", it can query GBrain instead of grepping blindly through every file in a repo, or worse, guessing.

It does this two ways. Keyword search matches text directly. Hybrid search combines that with semantic (meaning-based) matching, so a query for "vault secret handling" can find a function called `get_vault_secret` even if the words don't match exactly. A separate, autonomous background mechanism — the Dream Cycle — attempts to build a deeper structural understanding of everything stored; it's substantial enough to warrant its own document — see `gbrain-dream-cycle-explainer.md`.

Everything GBrain produces is advisory. It is not read by the actual build pipeline, it does not override a file that says something different, and an agent that trusts GBrain's memory over the real, current state of a repo is making a mistake. GBrain's entire value is in reducing how much re-reading and re-explaining has to happen — not in being a second source of truth that competes with the first.

---

## 3. PostgreSQL — The Foundation GBrain Is Actually Built On

GBrain's memory has to live somewhere, and where it lives is not a minor implementation detail — it is the reason the whole system is reliable or unreliable. GBrain runs on a self-hosted PostgreSQL database, and understanding what that database actually does is close to understanding GBrain itself.

**Why Postgres, and not something simpler.** GBrain didn't start this way. It originally ran on PGLite — an embedded, single-writer database living inside the application rather than running as its own separate service. That design has a real weakness: only one process can safely write to it at a time. In practice, that weakness stopped being theoretical — a real corruption incident occurred when OpenCode held the database lock during a `gbrain sync` operation, and the database was damaged. The fix wasn't to be more careful about locking; it was to stop using a database architecture that made this kind of collision possible in the first place. PostgreSQL is a genuine multi-writer database, built to handle exactly this — many processes reading and writing safely, at the same time. That single architectural fact is why GBrain is trustworthy today in a way it wasn't before. The legacy PGLite artifact is still present on disk (`~/.gbrain/brain.pglite`) but is stale and unused — the live engine is Postgres, full stop.

**`pgvector` — the extension that makes semantic search possible.** A plain database can match text against text, but has no concept of *meaning*. `pgvector` stores content as vectors — long lists of numbers representing the meaning of a piece of text, produced by an embedding model. Two pieces of text with similar meaning end up with mathematically close vectors, even without sharing a single word. This is what makes hybrid search actually useful rather than just a faster grep.

**A separate database from PDLF's own ledger, deliberately.** GBrain's Postgres instance is not the same one PDLF's own build ledger runs on. The two are kept apart on purpose: GBrain is a higher-churn, LLM-driven workload with real failure modes of its own (as the PGLite incident showed), while PDLF's ledger is the single most load-bearing, correctness-critical part of the entire build system. A problem in one must never be able to reach into the other.

---

## 4. Providers, Models, and API Keys

GBrain doesn't reason or embed anything on its own — every search, and every phase of deeper processing, calls out to an external AI provider. Which provider does which job is a deliberate, constrained choice.

Embeddings come from OpenAI — this isn't just a preference; Anthropic's own models cannot perform embeddings at all, a genuine structural gap rather than a missing-key state. Chat and query-expansion work also runs on OpenAI. Provider keys must live as environment variables, never written into GBrain's own configuration file in plaintext — a key sitting in a config file in plaintext is a real, confirmed exposure risk, not a theoretical one.

For the exact current credential set and status, see `gbrain-config.md`.

---

## 5. Search & Retrieval

GBrain's search is hybrid by design — it combines exact keyword matching with vector-based semantic matching, and can additionally expand a query using an LLM to catch related phrasing the literal words wouldn't find. The practical effect: a search doesn't need to guess the exact terminology used in the original document; it can find conceptually related content even when the wording is completely different. This is the layer most agents interact with day to day — most queries never need the Dream Cycle's deeper synthesis at all, they just need to find the right existing content quickly.

---

## 6. A Real, Permanent Limitation: Code Call-Graph Resolution

`code-callers` and `code-callees` sound like they'd resolve exactly what calls what across a codebase. They don't, and it's worth knowing precisely why rather than periodically re-discovering it.

It was initially assumed this could be fixed by switching to a different, more "code-aware" schema pack — one called `gbrain-engineer` looked like the obvious candidate by name. That assumption was wrong. A closer look at the actual pack manifest showed `gbrain-engineer` adds almost nothing beyond the base pack, and — critically — the `code` page type itself is marked as not extractable in *every* bundled schema pack, including `gbrain-everything`, the one actually in use. No pack switch fixes this; it's a property of how GBrain's bundled packs are built, not a configuration mistake.

The practical upshot: `code-callers`/`code-callees` return the right symbol names but can't resolve them to an actual defining location — a name, not a confirmed link. This is a real, permanent, formally-accepted limitation, not something still being chased. **Graphify's `get_neighbors` does the identical job correctly and completely** — fully resolved, typed, cross-file relationships, with source locations attached. The working rule: for "what calls/imports/contains what," always reach for Graphify — see `graphify-explainer.md`.

---

## 7. Integration With OpenCode & GStack

Inside OpenCode, GBrain is reached through the `/sync-gbrain` skill, which wraps the underlying sync and dream commands and, on a project's first real use, adds a guidance block to that project's own `AGENTS.md` — telling any agent working there how to prefer GBrain's search over a blind file grep.

**A genuinely counter-intuitive mechanical fact, worth remembering:** GBrain (and any other MCP server, including Graphify) is only ever started once, when the OpenCode process itself boots up. A brand new chat conversation does not restart it. If a new MCP integration is added, or an existing one's configuration changes, while OpenCode is already running, the change sits correctly written to disk and does nothing — no error, no warning, just silent absence — until the whole process is fully quit and relaunched. This tripped up the Graphify MCP setup for exactly this reason during its own initial integration; the fix was never a configuration correction, just a restart.

---

## 8. Known Limitations, Honestly Stated

**The call graph only resolves same-file references, and no schema pack extracts it at all.** Covered fully in Section 6. This is the single most important limitation to carry forward, given how much weight might otherwise be placed on "the call graph will catch it."

**MCP integrations require a full process restart to take effect**, not just a new chat session. Section 7.

**Dream Cycle failures can be silent**, and provider-dependent phases can fail while the rest of GBrain remains healthy. See `gbrain-dream-cycle-explainer.md`.

---

*Companion documents: `gbrain-config.md` (current configuration facts), `gbrain-reference.md` (command syntax and troubleshooting), `gbrain-dream-cycle-explainer.md` (the autonomous background intelligence mechanism, its own case).*

*End of document*
