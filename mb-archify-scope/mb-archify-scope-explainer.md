---
title: "mb-archify-scope-explainer"
doc-id: "mb-b249e1f5"
updated: "2026-10-07"
---

# mb-archify-scope — Explainer

Orientation, suitability, and reasoning for the `mb-archify-scope` scoping
skill. State: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md). Procedure:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md).

## What this actually is

Archify draws well only when someone has already decided what the drawing is
for. `mb-archify-scope` is that deciding step, made explicit: before any
Archify authoring begins, it takes the developer's drawing request and produces
an agreed Scope Card — the intent in one paragraph, the one diagram type and
why, a fixed small budget of primary nodes, exactly one main path, an explicit
list of what is deferred, and a plan for where every flow crosses the layout.
The developer approves that card; the Archify run then consumes it as its input
contract. The skill never draws anything. It exists because the alternative was
learned the hard way: an authoring session started on an undecided scope spent
itself fighting corridor failures that a short scoping conversation would have
prevented.

## Feature summary

- Converts a raw drawing request into a decided scope through a bounded
  interview rather than assumptions.
- Chooses the diagram type deliberately — using the archify guide as a check,
  not an oracle — because type choice is the single highest-leverage scoping
  decision.
- Caps the picture at a small fixed budget of primary nodes and forces
  everything else into an explicit Deferred List, so density is a decision, not
  an accident.
- Predicts where flows will cross layout bands — the corridor plan — turning
  the failure mode that wasted sessions into a pre-flight check.
- Declares, but does not execute, a feasibility probe, and defines the abort
  conditions a failed probe or an infeasible scope will trigger.
- Ends in an approved machine-readable contract the authoring run copies
  verbatim, so approval and execution cannot drift apart.
- Records run learnings on approval, feeding graduations into the skill itself
  and the archify reference.

## Suitability

**Best for:** dense, card-bearing, multi-flow subjects — system maps, pipelines
with gates, anything where type, density, and corridor decisions genuinely
matter — and recovery, when a previous Archify run failed on routes or
corridors.

**Good for:** medium subjects where a recordable scope decision has value even
if the drawing would probably have succeeded anyway.

**Not good for:** a single component or a tiny unambiguous flow — that is an
explicit abort condition ("low technical intensity"): hand it to `/archify`
directly, no ceremony. Also the wrong tool for structural questions about code
(what actually calls what — Graphify's domain) and for page/UI design (GStack's
design-HTML). A subject legitimately needing two or more pictures is never
compressed into one — it is split.

## Design reasoning

**Why scoping precedes authoring.** The first memory-ecosystem attempt chose
the dataflow type because the subject said "flows", and spent a session
fighting corridor walls (42→21→12 diagnostics) before dying. Re-scoped as
architecture, the same subject validated clean in two repair rounds. The lesson
became the skill's structure: decide type, density, and corridors before any
node exists, and let the guide call check the decision rather than carry it
alone.

**Why read-only until the gate.** The skill often runs in plan mode, where
writes are forbidden — but the deeper reason is the gate itself: a scope nobody
approved is a picture nobody asked for. Every artifact before the handoff is
chat-only; the first write is the approved contract.

**Why a machine header.** The handoff is a contract, not a summary: the
authoring run consumes the header's type, nodes, corridors, and abort
conditions directly. Copying approved text verbatim — never re-deriving — keeps
approval and execution from drifting apart.

**Why abort-and-reshape instead of refusal.** An honest "do not draw this yet"
still owes the developer a path forward. After every abort the skill offers one
to two genuinely different scopes — reshaping is the third move, not an
apology.

**Where this sits relative to the archify suite.** It is a permanent
front-of-pipe component of the Archify suite, documented in its
config/reference/explainer and checked by the archify exam, which verifies the
installed copy matches the spec. By the component-suite convention, the repo
holds the spec and WSL holds the runnable copy. It deliberately restates none
of Archify's authoring procedure — anti-duplication by design; its only owned
output is the Phase 9 learnings file.

**Standing cautions.** Installed-copy writes touch the skills directory, which
standing Cupcake policy grant-requires (developer-run; enforcement active as of
2026-10-04). And one adjacency from security-global: a diagram produced through
this pipeline is communication, not evidence — an architecture review still
needs an explicit trust-boundary list; the picture never substitutes for one.

## Open architectural questions

- **Two output conventions in flight.** The spec's file-conventions table still
  shows flat output paths while the live convention nests under one folder per
  project slug. The header is the contract the authoring run consumes; two path
  shapes invite exactly the drift this suite exists to prevent. Resolving it is
  a one-line spec edit — developer-owned.
- **Where "low technical intensity" ends.** The abort threshold is judgment,
  deliberately so — but the boundary case (a two-component flow with one label
  of consequence) will recur, and each instance either hardens the line or
  proves it should stay soft.
- **The skills-dir ancestor-cwd case.** Cupcake's grant requirement for
  skills-directory writes has one unresolved probe case (sessions opened in an
  ancestor folder); until resolved, the sync procedure treats every
  installed-copy write as grant-required.