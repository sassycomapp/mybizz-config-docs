---
title: "archify-scope-skill"
doc-id: "mb-99f24066"
updated: "2026-10-01"
---
# mb-archify-scope — Front-of-pipe scoping for /archify

Turns a drawing request into an agreed **Scope Card** before any Archify
authoring begins. This skill scopes; it never draws. It produces the scope the
developer approves and the Archify run consumes. It is invoked *before*
`/archify`, never instead of it.

This file is the canonical specification — the reviewed source of truth.
The installed runnable copy lives at
`~/.config/opencode/skills/mb-archify-scope/SKILL.md` and is kept identical
to this document per the ecosystem's install pattern (the master explainer's
component-suite convention: repo holds the spec, WSL holds the runnable copy).
Change this file and the installed copy together.

---

## When this skill fires

A request to produce any visual diagram, map, pipeline, sequence, or lifecycle
picture — "map the X flows", "draw the architecture", "diagram this process",
"visualize this pipeline" — that would otherwise proceed straight into `/archify`.
Also fires on recovery: when a previous Archify run returned dense-route or
corridor failures, this skill re-scopes before authoring is retried.

A request that explicitly names a diagram type and a small, bounded source
("one sequence diagram of the checkout API") may fast-track: produce a minimal
Scope Card and gate once.

## Abort conditions — when this skill ends without an Archify run

The skill's hard rule: **the drawing is only as viable as its scope.** In any
phase, the honest verdict may be "do not draw this yet." Stop and report,
with the reason and, where possible, a reshaped alternative:

- **Intent not load-bearing** — the developer cannot name the one main path or
  the guarantee the picture must show; the picture would assert something nobody
  has decided.
- **Scope exceeds one drawing** — the source legitimately needs two or more
  diagrams (e.g., a system map *and* a pipeline spine). Split, don't compress.
- **Fenceposts too dense** — the node inventory cannot be brought to ≤12 primary
  nodes without a main-path that is no longer the subject.
- **Low technical intensity** — the subject is a single component or a tiny,
  unambiguous flow; Archify itself can author it. Hand back, do not add ceremony.
- **Type unchoosable** — the same source contradicts every plausible type; the
  request is asking one picture to do another picture's job.

Reshaping is the third move of the skill, always offered after an abort:
present one to two *more viable* plans for the developer to select from, rather
than ending on a refusal. A reshaped plan is a different scope, not a
re-wording of the rejected one.

---

## The nine phases

Each phase ends on a completion criterion — a checkable fact, not a feeling.
The skill is read-only until the gate: it never writes a draft, never authors a
candidate, never runs a probe. The first write anywhere is the approved Scope
Card in Phase 8, and it happens only in a write-allowed context.

### Phase 1 — Intent

Restate the developer's intent in **one paragraph**, not one sentence. The
paragraph carries: the subject, the audience, the guarantee the picture must
show, and the one load-bearing claim. The load-bearing claim is the sentence the
drawing must make people trust.

*Completion:* the one-paragraph restatement is confirmed by the developer before
Phase 2 begins.

### Phase 2 — ASK (a guiding interview)

Ask probing questions — bounded, at most five to seven — and only the ones that
change the drawing. Defaults exist for every question; ask only when the answer
is not derivable from the intent paragraph or the source. Each question must pass
this test: *a different answer produces a different picture.* If not, drop it.
Candidate questions:

- What must be *shown* versus *implied*? (Everything the picture must support is
  shown; everything that should not clutter the main path is implied or deferred.)
- How many layers of the system matter to this audience?
- What is the one main path the eye must follow left to right / top to bottom?
- Read the picture after a week away: which shapes must still be recognized?
- Density tolerance: is the load-bearing claim served by ≤12 nodes, or does a
  dense standard map genuinely serve it better?

*Completion:* the interview is finished; every asked question changed the plan.

### Phase 3 — Context

Determine the source material, per this project's mandatory-read rules: the
project `README.md`, the local `AGENTS.md`, the Archify skill, and the target
document itself. Read only what the task requires — never the whole skill suite.
Record, in the Scope Card: which source fact is the load-bearing claim, where it
lives, and what the picture must preserve exactly (product names, identifiers,
commands, protocols, API paths — they stay intact in any local language).

*Completion:* source material identified and the load-bearing claim traced to a
specific place in it.

### Phase 4 — Preliminary scope

Present a basic pipeline as **single words with arrows**, before any topology:
`sources → write-paths → gate → store → read`. Include the decision tree used
to choose among the five types. This phase is deliberately crude: it forces the
main path out before any node appears.

The type decision tree (expand from `archify guide "<scenario>" --json`):
- **architecture** — components, services, boundaries, ownership. Forgives many
  edges; the default for "everything that exists and connects."
- **workflow** — processes, approvals, gates, runbooks. Strict lanes and columns.
- **sequence** — call chains, request lifecycles, returns. Ordered participants;
  vertical order is meaning. No Automatic Port Spread.
- **dataflow** — pipelines, ETL/ELT, lineage, governance, consumers. Strict
  stage/row grid; the most punishing type for dense crossing flows.
- **lifecycle** — state/status transitions, retries, waiting and terminal states.

State `type + why` explicitly; run the guide and record whether it agrees or the
developer's subject takes priority. Last session's lesson: type chosen by
keyword ("memory flows" → dataflow) produced a corridor-wall failure that a
`guide` call — which returned architecture — had already warned against.

*Completion:* the developer approves the type (and its cost), or the skill
reshapes.

### Phase 5 — Scope the source

Produce the **Node Inventory**, the **Main Path**, the **Deferred List**, and
the **Corridor Plan**.

- **Node Inventory** — at most 12 primary nodes. Every node earns its place by
  sitting on the main path or on a short side branch that the audience needs to
  see. Nodes that only context might explain become Deferred List entries.
- **Main Path** — exactly one. Side branches leave the nearest main-path node.
- **Deferred List** — explicitly named and explicitly removed:
  everything that is real but will live in Archify *cards* (prose) or in the
  viewer's guided views, not as nodes or edges. Deferral is the loving decision,
  not the lazy one — cards carry the prose a node count cannot.
- **Corridor Plan** — the prediction, per type budget, of where every flow
  crosses a stage or lane band. This is foresight, not after-the-fact repair:
  flows crossing a band where nodes are stacked are the wall that wastes a
  session. Plan each flow to cross at an empty band, or plan the node rows so
  the bands stay open.

*Completion:* inventory ≤12, main path named, deferral list explicit, corridor
plan recorded with the layout budget it was derived from.

### Phase 6 — Feasibility probe (executed, not authored here)

The probe — a stub `validate` of stages-plus-nodes **before** flows and labels —
runs during the **Archify execution phase**, because Plan mode does not write.
This skill's Phase 6 output is the *declaration*: the expected corridor for each
flow, and the abort conditions that a failed probe will trigger. The probe is
the cheap check that converts last session's heat-of-battle diagnostics into a
pre-flight pass. Declared here, executed there.

*Completion:* declaration recorded; the probe itself belongs to the Archify
execution handoff (Phase 8), not to this skill.

### Phase 7 — Report and gate

Present the **Scope Card** (markdown) for developer approval — the single hard
gate. Present also, when a plan was infeasible, one to two reshaped
alternatives. The gate is hard: no authoring until the developer approves type,
node inventory, main path, and corridor plan. Silence is never consent.

*Completion:* the developer approves or selects a reshaped plan.

### Phase 8 — Handoff contract

Write the approved Scope Card to `output/{subject}-scope.md` and the compact
machine header to `output/{subject}-header.json` without re-deriving anything —
the chat-approved text is copied verbatim. This is the **first write of the
whole run**. The Archify authoring run then consumes the header as its input
contract; a failed probe returns work to Phase 5 for reshaping, never proceeds
past it.

*Completion:* the four items the developer approved appear in the files
byte-for-byte; the header is schema-valid; the Archify run is handed the header.

### Phase 9 — Close-out (learnings, on developer approval)

After the authoring run finishes, **ask** — never assume — whether to record
learnings for this run in `output/learnings/{YYYY-MM-DD}-{subject}.md`. This is
the ecosystem's close-out pattern (mirrors `mb-align-docs`'s logger write-back):
a run produces judgment calls worth keeping, and nothing in the stack records
them unattended. On approval, write a run learnings file in the suite's
transient table format (learning | right action | destination), so notable
entries can later graduate into the skill or reference. Notable candidates:
repair-order sequences, geometry facts, calibration findings, automation
limits. Silence is never consent — if the developer does not ask, do not write.

*Completion:* learnings either recorded (approved) or deliberately skipped
(declined); the run is closed.

---

## The Scope Card

### Fields (markdown)

intent · type (+ why) · quality_profile · node inventory (≤12, with role per
node) · main path · deferred-to-cards list · corridor plan (per-flow expected
band) · layout budget source · probe declaration (expected corridors + abort
conditions) · decisions (what the developer approved, verbatim)

### The machine header (JSON) — written in Phase 8

```json
{
  "subject": "<kebab-case>",
  "intent": "<one paragraph>",
  "type": "architecture | workflow | sequence | dataflow | lifecycle",
  "type_reason": "<one sentence>",
  "quality_profile": "showcase | standard",
  "nodes": ["<id>", "... up to 12"],
  "node_roles": { "<id>": "<role/one-liner>" },
  "main_path": ["<id>", "<id>", "..."],
  "deferred_to_cards": ["<item>", "..."],
  "stages_or_lanes": ["<label>", "..."],
  "expected_corridors": [["<from>", "<to>", "<band>"], "..."],
  "layout_budget_read": "<renderers/<type>/README.md>",
  "quality_gate": "showcase accepted only at 9 artifact checks, 0 composition errors, 0 warnings",
  "abort_conditions": ["<condition>", "..."],
  "status": "approved"
}
```

### File conventions

All outputs go to the dedicated Archify output folder:

| File | Purpose |
|---|---|
| `output/{subject}-scope.md` | the Scope Card, reviewable |
| `output/{subject}-header.json` | the machine contract for the Archify run |
| `output/{subject}-draft.json` | the Archify candidate spec (authored by Archify, not this skill) |
| `output/{subject}-render.html` | the delivered artifact (plus `deliver`'s private snapshot sidecar) |
| `output/learnings/{YYYY-MM-DD}-{subject}.md` | run learnings, written on developer approval (Phase 9) |

---

## The layout budgets (reference — authoritative numbers live in the renderer)

The exact per-type budget is defined in the Archify package at
`renderers/<type>/README.md`; read it at Phase 5, never from memory. The
dataflow budget is the worked example that justified this skill and the one
trap most likely to recur:

| Constant | Value (dataflow) |
|---|---|
| Stages (2–5) | centers `x = 100 + stage×215`, band 168 wide, header `y=46` |
| Row tops (`row` 0–4) | `y = 128, 242, 356, 470, 584` (+ `yOffset`) |
| Default node | 112×58 |
| Node spacing | ≥10px between any two nodes |
| Flow length | ≥34px between endpoints |
| Showcase rhythm | every nonzero segment ≥8px; interior turns ≥16px |
| Automatic Port Spread | default; **skipped** for explicit `via`/`channelX`/`channelY`/`labelAt`/non-auto routes |
| Repair order | quality_profile → node overlap → edge-through-node/endpoint-direction → crossings/corridors/rhythm → label clearance |

Corridor rule of thumb (all grid types): a flow crossing a stage/lane band must
pass through a **row band that is empty of nodes**, and the corridor plan names
those bands by row. A plan that routes every flow at its source's own row,
through a column where that row is occupied, is a wall — reshape the rows, do
not hand-route around them.

---

## Skill mechanics

- **Invocation:** model-invoked — the description carries the trigger branches so
  any drawing request routes through scoping first; it never disables model
  invocation, because a drawing request arriving bare ("map this") must still
  reach this skill before `/archify`.
- **Anti-duplication:** this skill is the front of the pipe only. It does not
  restate the Archify skill's authoring procedure, command reference, checker
  workflow, or update-notice contract — those live in the Archify skill itself
  and in [[[mybizz-config-docs:archify/archify-reference|Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md). It does not restate this repo's
  docs-management rules (own your commits, learnings, docs-manager cycle):
  this skill is deliberately lightweight, front-of-pipe, and produces no log
  and no governance loop of its own beyond the Phase 9 close-out learnings
  file, which is the one documented output the skill itself owns.
- **Gates are hard stops:** the single gate in Phase 7 is a hard stop per the
  global rule; no authoring proceeds without the developer's explicit approval.

*End of document*
