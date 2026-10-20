---
title: "memory-governor-explainer"
doc-id: "mb-47216ab9"
updated: "2026-10-20"
---
# Memory Governor — Explainer

What the system is, why it works the way it does, and what keeps it working.
State: [[[mybizz-config-docs:memory-governor/memory-governor-config|Config]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md). Procedures:
[[[mybizz-config-docs:memory-governor/memory-governor-reference|Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md). Standing differences:
[[[mybizz-config-docs:memory-governor/memory-governor-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-learnings.md).

## What it is

An AI agent that writes directly from its own raw output into durable memory
has no check on whether what it just wrote is true — memory formation is
typically ungoverned. GBrain's dream cycle, for example, synthesizes concepts
and facts from raw project material, and nothing checks those candidates for
provenance, contradiction, or risk before they become part of GBrain's
durable, queryable memory.

The memory governor closes that gap. It is MyBizz's control-plane service —
provenance-checked, rule-based, audit-logged — sitting between memory
generation and durable GBrain storage. No candidate reaches durable memory
through the governed path without passing through it. It is a gatekeeping
layer, not a memory store: it does not replace GBrain; it decides what GBrain
is allowed to durably remember. The gate is built and running: a deciding API
and a delivering worker, auto-started by systemd, with register copies of
every promoted candidate kept outside the database.

## What it can do

- Verify writer identity server-side, from the authenticating credential —
  never from the payload.
- Validate scope declarations at write time and resolve visibility at read
  time, per requesting project.
- Run contradiction checking on every candidate, every memory type.
- Hold back the five high-risk types and low-confidence material for review.
- Produce exactly two automatic outcomes: promote straight through, or route
  to the developer's review list carrying a recommendation, a validation
  summary and a ramifications statement.
- Record human decisions, supersede records atomically, and keep a full
  provenance trail per candidate.
- Write every promoted memory twice — a register index row and a full JSON
  payload — as the disaster-recovery copy outside the database.
- Observe patterns in its own decision record and propose a policy change —
  which routes through the same human gate, because a change to policy is
  itself high-risk content.

## Suitability

- **Best for:** gating developer- and PDLF-authored facts and decisions into
  durable memory with real provenance, contradiction and risk checks; any
  submission where being believed later is the point.
- **Good for:** deliberate corrections via atomic supersession; cross-project
  sharing with read-time visibility; self-observation through its own
  decision record.
- **Not good for:** bulk raw content (GBrain sync's job); GBrain's
  dream-cycle output (structurally ungovernable — the manual discipline
  applies); forcing past review (the engine has no such path); running
  without both processes.
- **Writer coverage:** manual submission runs through the `mb-submit-memory`
  suite; the PDLF step-completion writer is built and PDLF does not call it;
  the dream cycle cannot submit at all.

## Why it works this way

- **A deterministic engine, never AI judgment.** The decision function is
  rule-based and auditable by a human. It may only promote or route to
  review; it never closes a candidate out on its own — a decision taken
  silently, rejection or quarantine without the developer ever being told,
  is exactly the failure a governance layer exists to prevent. A routed
  candidate is genuinely blocking: it cannot reach a durable state before an
  explicit developer decision is recorded.
- **Confidence and contradiction values come from the submitting agent.** The
  governor enforces rules against those values but never computes them —
  computing them would require the AI judgment the determinism rules out.
  The agent proposing a candidate is the one with direct, contemporaneous
  knowledge of what it just did, so the judgment obligation sits in every
  writer's procedure: query GBrain for related material, read what comes
  back, submit genuinely reasoned values, never placeholders.
- **A contradiction flag is not a verdict.** It only means two things
  disagree. A deliberate replacement is handled by supersession with the
  resolution `closed_by_new_fact`, and a resolved contradiction does not
  block promotion. Only a genuinely unexplained disagreement routes to
  review. Cross-project contradictions are a hard exception: they always
  route to review, regardless of confidence or type.
- **Isolation is the governor's job, not GBrain's.** GBrain stores facts per
  source, and the worker names the owning project's own documentation source
  on every write, so a governed fact lands with the documents it belongs to.
  On top of that, every fact carries its owning project as its entity, and
  visibility is mapped from declared scope. Project-scoped recall is
  entity-scoped recall; read-time resolution enforces sharing between
  projects. The separation between projects does not come from GBrain's
  sources.
- **Two writes per promotion.** The register index alone cannot reconstruct
  a lost database record — it has no column for the content text. Postgres
  and git cannot commit atomically together, so the register write is an
  asynchronous, retryable consumer of the same outbox mechanism as every
  other downstream effect; after repeated consecutive failures it surfaces
  the failure rather than blocking promotion or retrying silently forever.
- **No message broker.** For a single-operator, single-machine deployment a
  separate broker is unjustified infrastructure. A transactional outbox plus
  Postgres LISTEN/NOTIFY with one dedicated worker gives a durable event log
  and a queue in one mechanism; the worker wakes on notify and polls on a
  fixed interval as a safety net.
- **Deciding and delivering are separate processes.** The API makes the
  governed decision; the worker performs every downstream effect. Both read
  their configuration from the environment at start — an API without a
  worker silently strands promotions in the outbox.
- **The dream cycle is the one ungovernable writer.** GBrain's dream cycle
  has no interception point of any kind; forking GBrain to add one is
  rejected — a permanent re-merge obligation against GBrain's releases, for
  a problem solvable another way. The standing control is manual discipline:
  run a real dream cycle, then run GBrain's suspected-contradictions
  evaluation and review the findings.
- **`anvil-agent-references` bypasses the governor by design.** Official,
  direct-from-Anvil reference material is a dictionary; it does not need to
  be fact-checked against itself. It syncs into GBrain the ordinary way, and
  ordinary syncing of it remains the developer's own responsibility.

## What has to happen

- **Both processes keep running.** The systemd user units own them and start
  them at boot; the worker unit must keep its PATH line, because the worker
  shells out to the `gbrain` command.
- **Every writer keeps the judgment obligation** — reasoned confidence and
  contradiction values against real GBrain reads, never placeholders.
- **The developer keeps deciding.** Review items are resolved only by
  explicit human decision, and no PDLF step begins while any review item is
  open.
- **Superseding a fact retires its GBrain copy too**, so the governor's
  record and the brain agree.
- **The repository is committed by hand** — the standing commit routine does
  not cover it.
- **The brain default source is validated after governed writes**, because
  every governed write re-points it.
- **The dream discipline is applied on every real dream run.**
