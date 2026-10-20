---
title: "archify-explainer"
doc-id: "mb-7923ad74"
updated: "2026-10-20"
---
# Archify — Explainer

What Archify is, when to use it, and why it is built the way it is.
Current state: [[[mybizz-config-docs:archify/archify-config|Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md). Mid-task commands and rules: [[[mybizz-config-docs:archify/archify-reference|Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md).
What differs from the standard and why: [[[mybizz-config-docs:archify/archify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/archify/archify-learnings.md).

---

## What it is

Archify is a Node.js tool that turns a small, typed JSON description of a system into a polished, interactive HTML diagram — one self-contained file a person can open, explore, and share. It exists for a specific gap: when an AI coding agent is asked to "draw the architecture," the alternatives either produce throwaway pictures (a chat-rendered Mermaid block nobody can open, verify, or reuse) or demand manual work in a drawing editor that agents cannot perform. Archify sits in between: the agent authors a structured specification, the tool compiles it deterministically into a real artifact, and a validation pipeline refuses to hand over anything that fails structural checks.

The person it serves is the developer or reviewer who needs to read a system — at review time, in documentation, or in a presentation — and needs the picture to be honest: every node, edge, and label traceable back to something the author actually wrote, not invented by a layout engine.

## What it can do

- Renders five distinct diagram semantics — component architecture, process workflow, message sequence, data flow, and state lifecycle — each with its own schema, so the shape of the picture matches the shape of the question.
- Validates before it delivers: schema, layout, HTML/SVG composition, route, and label-clearance checks must all pass before an artifact replaces the previous known-good output; a failed delivery never destroys the last good diagram.
- Produces interactive readers, not static pictures: the generated HTML carries search, focus, route tracing, upstream/downstream traversal, role comparison, guided stories, dark/light themes, and finite motion — all derived from the authored source.
- Exports a portable proof surface: PNG, SVG, WebM, and canonical 1200×630 share cards, with temporary viewer state stripped so the shared image says exactly what the artifact says.
- Accepts Mermaid input as a topology source — re-authored, not restyled — and supports an explicit, fail-closed deployment-ownership review profile when a production topology must name owners, regions, and boundary crossings.
- Compares two validated architecture snapshots (Before/Delta/After) with a machine receipt that classifies added, removed, changed, and moved elements — without inferring risk or merge safety.

## Suitability

**Best for:**

- Agent-authored system maps that must be trustworthy — architecture, workflow, sequence, dataflow, or lifecycle views where every visual element should trace to authored facts.
- Architecture change review: showing exactly what a proposed change adds, removes, changes, and moves, as a review artifact rather than an impact claim.
- Communication artifacts with a long shelf life: a single HTML file that stays explorable, themes correctly, and exports cleanly for READMEs and releases.

**Good for / adequate for:**

- Converting existing Mermaid diagrams into something with better information architecture — the topology is reused, the styling deliberately is not.
- Documenting pipelines, request lifecycles, or state machines during planning, where a durable, shareable picture beats chat-transient rendering.

**Not good for / wrong tool for:**

- Freeform drawing or WYSIWYG editing — there is no editor; the source of truth is typed JSON. A general drawing tool is the right tool there.
- Making existing Mermaid merely prettier without improving structure — explicitly out of scope by the project's own design.
- Fully automatic layout with no author judgment — layout quality is an authored responsibility; if nobody can judge hierarchy and emphasis, generic auto-layout tools are more appropriate.
- Claims about runtime behavior: reachability queries say what the author wrote, never blast radius or breakage. Those need real code analysis — in this environment, Graphify's structural graph is the complementary tool for code-level questions.

## Why it works this way

**Why typed JSON IR instead of generating SVG directly.** A schema plus validators means every failure has a name, a subject, and a machine-readable repair — the agent fixes the diagnosed thing instead of re-rolling a prompt and hoping. It also makes the source reproducible: the JSON is the artifact's provenance, so iteration edits the source while unrelated structure stays stable. The cost is authoring discipline (reading a schema, writing JSON), which is exactly the work an agent is good at and a human rarely wants.

**Why validation gates delivery.** The pipeline's central promise is "the output was checked before you saw it." Atomic delivery — a candidate is rendered and verified in a same-directory snapshot and only then replaces the target — is what lets an agent iterate without ever leaving a broken diagram behind. This mirrors this environment's own verification discipline: a self-reported "should work" never substitutes for a checked artifact.

**Why the viewer only tells the truth.** Every interaction — focus, reach, routes, stories — is computed from authored nodes and edges. The alternative, inferring connections or impact, would make the picture lie in ways that are hard to detect. The same discipline shows in the receipts: comparisons classify what changed but refuse to claim risk, and reachability reports nodes and hops but never "blast radius."

**Where this sits relative to other parts of the system.** Graphify answers structural questions about code (what actually calls what); Archify answers communication questions about systems (how should this be presented so a human understands it). Neither depends on the other, and conflating them would degrade both. GStack's design-HTML skill occupies a different domain entirely (page/UI design). Governance tooling treats Archify like any other local tool: it is not a memory writer and has no dedicated policy; Cupcake's enforcement state is standing policy in [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) §Operational status — not fixed; re-check there.

**Why the update check is the only network surface.** A version reminder needs to know a latest version exists; everything else — rendering, validation, export — is deliberately local. The check is notification-only, transmits nothing about the project, and can be disabled. The design keeps the tool trustworthy as infrastructure while leaving the update decision entirely with the user.

### Why scoping comes first (`mb-archify-scope`)

Archify makes a promise: *the picture is only as viable as its scope.* That promise is enforced by a permanent front-of-pipe skill, `mb-archify-scope` (canonical specification [[[mb-archify-scope:mb-archify-scope|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md)). It runs before `/archify`, never instead of it, and splits the pipeline into two stages: scoping — deciding in advance what the eye must follow (type, one main path, density caps, corridors) — and drawing, where Archify consumes the approved scope and a failed feasibility probe returns work to scoping rather than past it. A dense, card-bearing subject cannot be authored well without that decision made first. The scoping mechanics, Scope Card conventions, and the subject evidence behind this reasoning live in the mb-archify-scope suite.

## What has to happen

- **The installed scoping copy tracks the canonical specification.** On every accepted specification change, the body is re-copied into the installed file — keeping the installed file's own frontmatter — so the executed skill never drifts from its spec.
- **MyBizz keeps this suite committed** (commit-all), so GBrain retrieval over it stays current.
- **Update decisions remain developer-owned:** archify notifies; it never downloads, installs, or executes an update.
- **The standing posture is detection and verification.** The tool is working well; present is not the same as working, and nothing is repaired without a developer gate decision.

## S.W.O.T.

**Strengths:** deterministic, schema-validated output with atomic delivery — a failed
candidate never destroys the last good artifact. Trustworthy as *communication*: every
node and edge traces to authored facts. Five distinct diagram semantics with strict
validation, one self-contained HTML artifact, portable export (PNG/SVG/WebM/Share Cards),
Mermaid intake, and a Before/Delta/After proof surface.

**Weaknesses:** authoring demands a schema discipline most humans won't adopt — the JSON
is the source of truth and there is no WYSIWYG editor. Desktop first-screen containment
is a hard gate that card-bearing artifacts can struggle to satisfy in the current viewer
build (see the reference's visual-review calibration note). No code-level analysis: reachability
says what the author wrote, never true blast radius.

**Opportunities:** the scoping skill already converts the tool's main adoption friction
(type choice, density, corridors) into a repeatable front-of-pipe discipline; further
graduations of run learnings into the reference keep the geometry rules current. Unique
fit for review artifacts and long-shelf-life system maps.

**Threats:** a wrong type choice at scope time is the highest-leverage failure —
scoping exists precisely to de-risk it. Cupcake's enforcement state is not fixed; the
standing policy pointer is [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) §Operational status.

## Companion documents

| Document | Purpose |
|---|---|
| [[[mybizz-config-docs:archify/archify-config\|Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) | State — what exists and what it is set to |
| [[[mybizz-config-docs:archify/archify-reference\|Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md) | Invocation, commands, authoring procedure, failure rules |
| [[[mybizz-config-docs:archify/archify-learnings\|Learnings]]](C:/mybizz/mybizz-config-docs/archify/archify-learnings.md) | What differs from the standard in this setup, and why |
| [[[mb-archify-scope:mb-archify-scope\|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md) | The scoping skill's canonical specification |
| `archify/output/` | Runtime output — one folder per project slug |
