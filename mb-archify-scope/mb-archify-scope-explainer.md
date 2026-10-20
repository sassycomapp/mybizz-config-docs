---
title: "mb-archify-scope-explainer"
doc-id: "mb-b249e1f5"
updated: "2026-10-20"
---

# mb-archify-scope — Explainer

Orientation, suitability, and reasoning for the `mb-archify-scope` scoping
skill. State:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md).
Procedure:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md).
Learnings:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md).

## What it is

Archify draws well only when someone has already decided what the drawing is
for. `mb-archify-scope` is that deciding step, made explicit: before any
Archify authoring begins, it takes the developer's drawing request and produces
an agreed Scope Card — the intent in one paragraph, the one diagram type and
why, a fixed small budget of primary nodes, exactly one main path, an explicit
list of what is deferred, and a plan for where every flow crosses the layout.
The developer approves that card; the Archify run then consumes it as its input
contract. The skill never draws anything. It exists because an Archify
authoring run started on an undecided scope spends itself fighting corridor
failures that a short scoping conversation prevents.

## What it can do

- Converts a raw drawing request into a decided scope through a bounded
  interview rather than assumptions.
- Chooses the diagram type deliberately — using the archify guide as a check,
  not an oracle — because type choice is the single highest-leverage scoping
  decision.
- Caps the picture at a small fixed budget of primary nodes and forces
  everything else into an explicit Deferred List, so density is a decision, not
  an accident.
- Predicts where flows will cross layout bands — the corridor plan — turning
  the failure mode that wastes sessions into a pre-flight check.
- Declares, but does not execute, a feasibility probe, and defines the abort
  conditions a failed probe or an infeasible scope will trigger.
- Ends in an approved machine-readable contract the authoring run copies
  verbatim, so approval and execution cannot drift apart.
- Records run learnings on approval, feeding graduations into the skill itself
  and the archify reference.

## Suitability

**Best for:** dense, card-bearing, multi-flow subjects — system maps, pipelines
with gates, anything where type, density, and corridor decisions genuinely
matter — and recovery, when an earlier Archify run failed on routes or
corridors.

**Good for:** medium subjects where a recordable scope decision has value even
if the drawing would probably have succeeded anyway.

**Not good for:** a single component or a tiny unambiguous flow — that is an
explicit abort condition ("low technical intensity"): hand it to `/archify`
directly, no ceremony. Also the wrong tool for structural questions about code
(what actually calls what — Graphify's domain) and for page/UI design (GStack's
design-HTML). A subject legitimately needing two or more pictures is never
compressed into one — it is split.

## Why it works this way

**Why scoping precedes authoring.** Type, density, and corridor decisions made
before any node exists are what keep an Archify run on the rails: a subject
re-scoped to the right type validates clean in a couple of repair rounds,
while an undecided scope spends its session on corridor walls. The lesson is
built into the structure — decide type, density, and corridors first, and let
the guide call check the decision rather than carry it alone.

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
front-of-pipe component of the Archify suite, documented in that suite's
config/reference/explainer and verified by this suite's checks
(Reference §Checks). By the component-suite convention, the repo holds the
spec and the skills directory holds the installed copy. It deliberately
restates none of Archify's authoring procedure — anti-duplication by design;
its only owned output is the Phase 9 learnings file.

**A drawing is not evidence.** One adjacency from security-global: a diagram
produced through this pipeline is communication, not evidence — an
architecture review still needs an explicit trust-boundary list; the picture
never substitutes for one.

## What has to happen

- The installed-copy write stays developer-run: it touches
  `~/.config/opencode/skills/`, which standing Cupcake policy grant-requires
  (enforcement state per
  [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)
  §Operational status). Spec and installed copy move together, body-to-body,
  by hand (Reference §Keeping spec and installed copy in sync).
- commit all runs at every close-out; its GBrain sync is what keeps the
  `mb-archify-scope` source current (registration confirmed through the
  command line — Reference §Checks).
- The archify dependency stays installed: the guide check and the doctor
  health check both run through it.
- The layout budgets are read from the installed archify package at Phase 5;
  whenever the package moves, re-verify the budget rows in the Configuration
  §Layout budget (dataflow).

## S.W.O.T.

**Strengths.** Type, density, and corridor decisions made before any node
exists; the machine header as a verbatim contract, so approval and execution
cannot drift; read-only until the gate (nothing is written unasked);
abort-and-reshape (never ends on a refusal).

**Weaknesses.** Proven on a single real subject; the low-intensity abort
threshold is judgment, deliberately soft; no mechanical sync between repo spec
and installed copy — the body change is applied by hand on both sides, so the
spec-edited-after-install drift class stays real and is caught only by the
Body equality check.

**Opportunities.** Future runs feed Phase 9 learnings, which graduate into the
skill itself or the archify reference.

**Threats.** Spec-edited-after-install drift — mitigated: the Body equality
check re-proves the pair at every research run; Cupcake's grant posture on
installed-copy writes — mitigated: the body-to-body, developer-run sync
discipline is documented and checked.

---

*Companion documents:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md) (current state),
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md) (procedures),
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md),
the canonical spec
([[[mb-archify-scope:mb-archify-scope|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md), repo),
and the archify suite's component documentation
([[[mybizz-config-docs:archify/archify-config|Archify Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) §Scoping skill component ·
[[[mybizz-config-docs:archify/archify-reference|Archify Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md) ·
[[[mybizz-config-docs:archify/archify-explainer|Archify Explainer]]](C:/mybizz/mybizz-config-docs/archify/archify-explainer.md)).*

*End of document*
