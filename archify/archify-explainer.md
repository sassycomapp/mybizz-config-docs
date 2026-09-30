---
title: "archify-explainer"
doc-id: "mb-7923ad74"
---
# Archify — Explainer

What Archify is, when to use it, and why it is built the way it is.
Current state: [[archify-config|Configuration]]. Mid-task commands and rules: [[archify-reference|Reference]].
Configuration-management exam set: [[archify-exam-plan|Exam Plan]] (run job-spec),
[[archify-exam-report|Exam Report]] (current verified state), [[archify-log|Log]] (events),
[[archify-learnings|Learnings]] (transient lessons), [[archify-skill|Archify Skill]] (the exam skill).

---

## What this actually is

Archify is a Node.js tool that turns a small, typed JSON description of a system into a polished, interactive HTML diagram — one self-contained file a person can open, explore, and share. It exists for a specific gap: when an AI coding agent is asked to "draw the architecture," the alternatives either produce throwaway pictures (a chat-rendered Mermaid block nobody can open, verify, or reuse) or demand manual work in a drawing editor that agents cannot perform. Archify sits in between: the agent authors a structured specification, the tool compiles it deterministically into a real artifact, and a validation pipeline refuses to hand over anything that fails structural checks.

The person it serves is the developer or reviewer who needs to read a system — at review time, in documentation, or in a presentation — and needs the picture to be honest: every node, edge, and label traceable back to something the author actually wrote, not invented by a layout engine.

## Feature summary (conceptual)

- Renders five distinct diagram semantics — component architecture, process workflow, message sequence, data flow, and state lifecycle — each with its own schema, so the shape of the picture matches the shape of the question.
- Validates before it delivers: schema, layout, HTML/SVG composition, route, and label-clearance checks must all pass before an artifact replaces the previous known-good output; a failed delivery never destroys the last good diagram.
- Produces interactive readers, not static pictures: the generated HTML carries search, focus, route tracing, upstream/downstream traversal, role comparison, guided stories, dark/light themes, and finite motion — all derived from the authored source.
- Exports a portable proof surface: PNG, SVG, WebM, and canonical 1200×630 share cards, with temporary viewer state stripped so the shared image says exactly what the artifact says.
- Accepts Mermaid input as a topology source — re-authored, not restyled — and supports an explicit, fail-closed deployment-ownership review profile when a production topology must name owners, regions, and boundary crossings.
- Compares two validated architecture snapshots (Before/Delta/After) with a machine receipt that classifies what was added, removed, changed, and moved — without inferring risk or merge safety.

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

## Design reasoning

**Why typed JSON IR instead of generating SVG directly.** A schema plus validators means every failure has a name, a subject, and a machine-readable repair — the agent fixes the diagnosed thing instead of re-rolling a prompt and hoping. It also makes the source reproducible: the JSON is the artifact's provenance, so iteration edits the source while unrelated structure stays stable. The cost is authoring discipline (reading a schema, writing JSON), which is exactly the work an agent is good at and a human rarely wants.

**Why validation gates delivery.** The pipeline's central promise is "the output was checked before you saw it." Atomic delivery — a candidate is rendered and verified in a same-directory snapshot and only then replaces the target — is what lets an agent iterate without ever leaving a broken diagram behind. This mirrors this environment's own verification discipline: a self-reported "should work" never substitutes for a checked artifact.

**Why the viewer only tells the truth.** Every interaction — focus, reach, routes, stories — is computed from authored nodes and edges. The alternative, inferring connections or impact, would make the picture lie in ways that are hard to detect. The same discipline shows in the receipts: comparisons classify what changed but refuse to claim risk, and reachability reports nodes and hops but never "blast radius."

**Where this sits relative to other parts of the system.** Graphify answers structural questions about code (what actually calls what); Archify answers communication questions about systems (how should this be presented so a human understands it). Neither depends on the other, and conflating them would degrade both. GStack's design-HTML skill occupies a different domain entirely (page/UI design). Governance tooling treats Archify no differently from any other local tool: it is not a memory writer and has no dedicated policy — with one standing caveat: Cupcake's enforcement status is not fixed and should not be assumed current at any given time (check [[cupcake-config|Cupcake Configuration]]'s Current Operational Status); it was disabled environment-wide at research time (2026-09-06), so any "no rule applies" conclusion is provisional and must be re-verified whenever enforcement state changes.

**Why the update check is the only network surface.** A version reminder needs to know a latest version exists; everything else — rendering, validation, export — is deliberately local. The check is notification-only, transmits nothing about the project, and can be disabled. The design keeps the tool trustworthy as infrastructure while leaving the update decision entirely with the user.

## Why scoping comes first (`mb-archify-scope`)

Archify makes a promise: *the picture is only as viable as its scope.* That
promise is enforced by a permanent front-of-pipe skill, `mb-archify-scope`
(canonical spec [[archify-scope-skill|Scoping Skill Specification]]; installed at
`~/.config/opencode/skills/mb-archify-scope/SKILL.md`). It runs before `/archify`,
never instead of it, and it changes the authoring pipeline into two stages:

1. **Scope** — restate the intent in one paragraph, run a bounded interview, name
   the diagram type and why, cap the Node Inventory at ≤12 primary nodes, fix
   exactly one main path, write an explicit Deferred List, and plan the corridors.
   Nothing is drawn here; the output is an approved Scope Card (`output/{slug}-scope.md`)
   and its machine header (`output/{slug}-header.json`).
2. **Draw** — Archify consumes the approved header as its input contract. A failed
   feasibility probe returns work to scoping for reshaping, never proceeds past it.

Verified live on the memory-ecosystem subject (2026-09-15): the scoping skill's
type decision upgraded a keyword-driven `dataflow` choice (which had produced
repeated corridor-wall failures) to [[architecture|Architecture]] — the guide-consistent type —
and the same subject then validated clean in two repair rounds. The scoping skill
exists because a dense, card-bearing subject cannot be authored well without
deciding, in advance, what the eye must follow.

## Config maintenance — how this system is examined and kept healthy

This suite participates in `mb-config-manager`: the estate's configuration-management
system exams each live system against its `{system}-config.md` spec. For Archify:

- **Exam set:** [[archify-exam-plan|Exam Plan]] (run job-spec), [[archify-exam-report|Exam Report]]
  (verified current state, no history), [[archify-log|Log]] (events), [[archify-learnings|Learnings]]
  (transient), [[archify-skill|Archify Skill]] (the standing check inventory and procedure).
- **Spec doc:** [[archify-config|Configuration]] — the single source of expected values; read
  fresh at every run start.
- **Scope of the exam:** the discovery symlink, the clone/package identity, the
  schemas/references/renderers inventory, the update-notice contract, the installed
  scope-skill copy (kept byte-identical to [[archify-scope-skill|Scoping Skill Specification]]), and the runtime
  output convention (one folder per project slug under `output/<slug>/`).
- **Philosophy:** the tool is working well — detection and verification only;
  the exam catches silent failures (present ≠ working) and repairs nothing without
  a developer gate decision.

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

**Threats:** a wrong type choice at scope time is the highest-leverage failure — the
guide (`archify guide "<scenario>" --json`) exists precisely to de-risk it. Cupcake's
enforcement status is not fixed and should not be assumed current at any given time
(check [[cupcake-config|Cupcake Configuration]]'s Current Operational Status); any "no rule applies"
conclusion is provisional. The update-check manifest URL is deliberately not fetched
or verified — a standing, documented out-of-scope item.

## Companion documents

| Document | Purpose |
|---|---|
| [[archify-config|Configuration]] | Canonical current-state configuration — the spec the exam runs against |
| [[archify-reference|Reference]] | Invocation, commands, authoring procedure, failure rules |
| [[archify-scope-skill|Scoping Skill Specification]] | The scoping skill's canonical specification (installed as `mb-archify-scope`) |
| [[archify-skill|Archify Skill]] | The config-management exam skill (standing check inventory) |
| [[archify-exam-plan|Exam Plan]] | Transient job-spec for the latest exam run |
| [[archify-exam-report|Exam Report]] | Verified current state after each exam run |
| [[archify-log|Log]] | Chronological record of events and exam runs |
| [[archify-learnings|Learnings]] | Transient lessons; entries graduate into a permanent home then delete |
| `archify/output/` | Runtime output — one folder per project slug |

## Open questions

- Install-link provenance is an open item in [[archify-config|Configuration]]. Why it matters: the documented Windows/WSL symlink incompatibility means a wrongly-created link can work from WSL while being invisible to Windows Explorer — a half-broken install that only surfaces on one side. Until verified, treat the link as functional (doctor passed) but not proven correct from both directions.
- No GBrain knowledge page exists for Archify yet. Why it matters: agent orientation relies on GBrain for "what is this tool" questions, and those searches currently return unrelated content. This doc suite is the intended fix; it takes effect for retrieval only after a sync.

*End of document*
