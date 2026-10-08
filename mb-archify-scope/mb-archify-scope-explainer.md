---
title: "mb-archify-scope-explainer"
doc-id: "mb-b249e1f5"
updated: "2026-10-08"
---

# mb-archify-scope — Explainer

Orientation, suitability, and reasoning for the `mb-archify-scope` scoping
skill. State: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md). Procedure:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md). The
config-management exam set for this suite ([[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-plan.md) ·
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-report.md) · [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-log|Log]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-log.md) ·
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md) · [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-skill|Exam Skill]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-skill.md)) is
synthesized and consumed per the [[[mybizz-config-docs:mb-config-manager/config-manager-agent|Config Manager]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md)
plan-driven cycle — the exam verifies this suite's state and never runs the
subject skill itself.

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

- **Two output conventions in flight — resolved 2026-10-08 (gate-approved F-1,
  run #1).** The spec's flat file-convention paths (§File conventions table,
  Phase 8 inline paths, Phase 9 learnings path) were corrected to the nested
  per-slug convention in one pass, the installed copy re-synced body-to-body,
  and the pair re-verified. The header contract now carries one path shape.
- **Where "low technical intensity" ends.** The abort threshold is judgment,
  deliberately so — but the boundary case (a two-component flow with one label
  of consequence) will recur, and each instance either hardens the line or
  proves it should stay soft.
- **The skills-dir ancestor-cwd case.** Cupcake's grant requirement for
  skills-directory writes has one unresolved probe case (sessions opened in an
  ancestor folder); until resolved, the sync procedure treats every
  installed-copy write as grant-required.

## Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[mybizz-config-docs:mb-config-manager/config-manager-explainer|the config-manager
explainer]] — emulated from the PostgreSQL pilot. The short local version:

- [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md) is the **spec** — the ideal state every
  exam checks against.
- Before each exam run, the config-manager synthesizes
  [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-plan.md): a fresh job-spec built from this spec, the
  last report, the log, and the learnings. The plan is transient (the file is
  live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-mb-archify-scope`) with the
  plan in hand — detection fully autonomous; healing gated.
- **Agent-healable items are suite-file repairs only** (the exam set files).
  The installed subject copy, the repo spec, the archify suite's documents,
  GBrain's engine, Cupcake internals, and the run artifacts are deny-list:
  changes reach them only as gate proposals the developer approves item by
  item.
- No credential route exists in this system — nothing to reference by name,
  nothing to withhold.
- The run rewrites [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-report.md) (current state, no
  history), appends one row to [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-log|Log]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-log.md), files new learnings, and
  prunes absorbed entries.

## S.W.O.T.

**Strengths.** Type, density, and corridor decisions made before any node
exists — the lesson that created the skill; the machine header as a verbatim
contract, so approval and execution cannot drift; read-only until the gate
(nothing is written unasked); abort-and-reshape (never ends on a refusal);
proven on its first real subject (corridor failures 17→0; 9/9 showcase).

**Weaknesses.** Proven on a single live run; the low-intensity abort threshold
is judgment, deliberately soft; no mechanical sync between repo spec and
installed copy — the body change is applied by hand on both sides, and the
2026-09-16 AR2-3 event proved the spec-edited-after-install class fires for
real; the suite is young — its first formal exam run is pending at build-out.

**Opportunities.** The config-management exam adds standing verification this
skill never had; the W-1 spec correction (one line) removes the two
path-shapes ambiguity; the fact-ownership reduction (W-2) simplifies
archify-config; future runs feed Phase 9 learnings, which graduate into the
skill or the archify reference.

**Threats.** Spec-edited-after-install drift recurrence (mitigated: the hash
pair is re-verified every run — AS1-2/AS1-3 here, AR2-3 in the archify exam);
the two output path shapes in flight (W-1) could route a header to the wrong
folder (mitigated: flagged every run until the developer's correction lands);
Cupcake grant posture on installed-copy writes (mitigated: the body-to-body,
developer-run sync discipline is documented and checked — AS2-4).

---

*Companion documents: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md) (current state),
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md) (procedures), the exam set ([[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-plan.md) ·
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-report.md) · [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-log|Log]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-log.md) ·
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md) · [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-skill|Exam Skill]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-skill.md)), the
canonical spec ([[[mb-archify-scope:mb-archify-scope|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md), repo), the archify suite's component documentation
([[[mybizz-config-docs:archify/archify-config|Archify Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) §Scoping skill component ·
[[[mybizz-config-docs:archify/archify-reference|Archify Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md) ·
[[[mybizz-config-docs:archify/archify-explainer|Archify Explainer]]](C:/mybizz/mybizz-config-docs/archify/archify-explainer.md)), and the provenance pages
([[[mybizz-config-docs:sessions/2026-09-15-006-archify-scope-skill|Session 006]]](C:/mybizz/mybizz-config-docs/sessions/2026-09-15-006-archify-scope-skill.md) ·
[[[mybizz-config-docs:facts/2026-09-15-archify-scope-pre-work|durable fact]]](C:/mybizz/mybizz-config-docs/facts/2026-09-15-archify-scope-pre-work.md) ·
[[[mybizz-config-docs:archify/output/memory-ecosystem-project/learnings/2026-09-15-memory-ecosystem|first-run learnings]]](C:/mybizz/mybizz-config-docs/archify/output/memory-ecosystem-project/learnings/2026-09-15-memory-ecosystem.md)).*

*End of document*