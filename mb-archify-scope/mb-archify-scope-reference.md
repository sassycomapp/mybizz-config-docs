---
title: "mb-archify-scope-reference"
doc-id: "mb-09517645"
updated: "2026-10-20"
---

# mb-archify-scope — Reference

Invocation, the nine phases, aborts, outputs, and failure rules. Mid-task
lookup. What the skill is and why:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-explainer.md).
Current state:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md).
Learnings:
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md).
The canonical contract is the spec itself
([[[mb-archify-scope:mb-archify-scope|Scoping Skill Specification]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md)) —
change spec and installed copy together.

## Invocation

`/mb-archify-scope`

- Invoke **before** `/archify`, never instead of it. Model-invoked: any drawing
  request — "map the X flows", "draw the architecture", "diagram this process",
  "visualize this pipeline" — routes through scoping first.
- Also fire on recovery: after a dense-route or corridor failure, re-scope
  before authoring is retried.
- Fast-track: a request naming a diagram type and a small bounded source ("one
  sequence diagram of the checkout API") may produce a minimal Scope Card and
  gate once.
- The skill is read-only until Phase 8: never write a draft, never author a
  candidate, never run a probe. The first write of the whole run is the
  approved Scope Card.

## The nine phases (ordered)

1. **Intent** — restate the intent in one paragraph, not one sentence: subject,
   audience, the guarantee the picture must show, the one load-bearing claim.
   *Completion: the developer confirms the paragraph before Phase 2 begins.*
2. **ASK** — a bounded interview, at most five to seven questions, and only
   ones that change the drawing. Defaults exist; ask only what is not derivable
   from the intent paragraph or the source. Drop any question where a different
   answer would produce the same picture. *Completion: every asked question
   changed the plan.*
3. **Context** — identify the source material (project `README.md`, local
   `AGENTS.md`, the Archify skill, the target document — only what the task
   requires). Record which source fact is the load-bearing claim, where it
   lives, and what must be preserved exactly: product names, identifiers,
   commands, protocols, API paths. *Completion: the claim is traced to a
   specific place in the source.*
4. **Preliminary scope** — present the pipeline as single words with arrows
   before any topology. Choose the type via the decision tree (below) and its
   guide check; state `type + why`; record whether the guide agrees.
   *Completion: the developer approves the type (and its cost) or the skill
   reshapes.*
5. **Scope the source** — produce the **Node Inventory** (at most 12 primary
   nodes; every node earns its place on the main path or a short needed side
   branch), exactly **one Main Path**, the **Deferred List** (explicitly named
   and explicitly removed — cards carry the prose a node count cannot), and the
   **Corridor Plan** (each flow's expected band, derived from the type's layout
   budget read fresh from the renderer, never from memory). *Completion:
   inventory ≤12, main path named, deferral explicit, corridor plan recorded
   with its budget source.*
6. **Feasibility probe declaration** — declare the expected corridor per flow
   and the abort conditions a failed probe triggers. The probe (a stub
   `validate` of stages-plus-nodes before flows and labels) executes in the
   Archify run, never here. *Completion: declaration recorded.*
7. **Report and gate** — present the Scope Card (fields below) for approval;
   when the plan was infeasible, present one to two reshaped alternatives that
   are different scopes, not re-wordings. **Hard stop: no authoring until the
   developer approves type, node inventory, main path, and corridor plan.
   Silence is never consent.** *Completion: approval, or a reshaped plan
   selected.*
8. **Handoff contract** — write the approved Scope Card to
   `output/{slug}/{subject}-scope.md` and the machine header to
   `output/{slug}/{subject}-header.json`, copied verbatim, never re-derived.
   This is the first write of the whole run. *Completion: the approved content
   appears in the files byte-for-byte; the header is schema-valid; the Archify
   run is handed the header.*
9. **Close-out** — after the authoring run finishes, ask whether to record run
   learnings in `output/{slug}/learnings/{YYYY-MM-DD}-{subject}.md` (transient
   table: learning | right action | destination; notable entries graduate into
   this skill or the archify reference, then are deleted). Silence is never
   consent. *Completion: recorded (approved) or deliberately declined.*

## Abort conditions — end without an Archify run

The drawing is only as viable as its scope. In any phase, the honest verdict
may be "do not draw this yet" — stop and report the reason:

- Intent not load-bearing — no one can name the main path or the guarantee.
- Scope exceeds one drawing — split, never compress.
- Fenceposts too dense — ≤12 primary nodes unreachable without losing the subject.
- Low technical intensity — a single component or tiny unambiguous flow; hand
  back to `/archify`, no ceremony.
- Type unchoosable — the source contradicts every plausible type.

After any abort, always offer one to two reshaped plans — a different scope,
not a re-wording. Never end on a refusal.

## Type decision tree

Run `node /home/dev-p/.config/skills/archify/bin/archify.mjs guide "<scenario>" --json`
when ambiguous — the `archify` binary is not on PATH, so invoke the CLI through
node. State `type + why` regardless. The developer's subject takes priority
over the guide — record any disagreement.

| Type | Use for |
|---|---|
| architecture | components, services, boundaries, ownership; forgives many edges; default for "everything that exists and connects" |
| workflow | processes, approvals, gates, runbooks; strict lanes and columns |
| sequence | call chains, request lifecycles, returns; ordered participants, vertical order is meaning; no Automatic Port Spread |
| dataflow | pipelines, ETL/ELT, lineage, governance, consumers; strict stage/row grid; the most punishing type for dense crossing flows |
| lifecycle | state/status transitions, retries, waiting and terminal states |

## Scope Card fields (markdown)

intent · type (+ why) · quality_profile · node inventory (≤12, role per node) ·
main path · deferred-to-cards list · corridor plan (per-flow expected band) ·
layout budget source · probe declaration (expected corridors + abort
conditions) · decisions (what the developer approved, verbatim)

## Machine header (Phase 8, JSON)

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

## Layout budget

The authoritative per-type budget lives in the Archify package at
`renderers/<type>/README.md` — read it at Phase 5, never from memory. The
verified values live in the
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md)
§Layout budget (dataflow).

**Corridor rule (all grid types):** a flow crossing a stage/lane band must pass
through a row band empty of nodes. Plan each crossing at an empty band, or plan
the node rows so the bands stay open. A plan routing every flow at its source's
own row through an occupied column is a wall — reshape the rows; do not
hand-route around them.

## Keeping spec and installed copy in sync

1. Edit the body of `/mnt/c/mybizz/mb-archify-scope/mb-archify-scope.md`.
2. Apply the identical body change to
   `~/.config/opencode/skills/mb-archify-scope/SKILL.md`.
3. Verify with `diff` that only the frontmatter blocks differ (repo: doc
   frontmatter; installed: skill frontmatter).
4. The installed-copy write touches `~/.config/opencode/skills/` — grant-required
   under standing Cupcake policy; run it developer-side or under an explicit
   grant. Enforcement state per
   [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)
   §Operational status.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Scoping Skill Specification (repo) | [[[mb-archify-scope:mb-archify-scope\|mb-archify-scope.md]]](C:/mybizz/mb-archify-scope/mb-archify-scope.md) | commit `cfcf0fa` (branch `main`) | 2026-10-20 |
| Archify per-type layout budgets | `renderers/<type>/README.md` in the installed archify package (`~/.config/skills/archify/`) | archify 2.16.0 | 2026-10-20 |
| archify CLI | `~/.config/skills/archify/bin/archify.mjs` (invoke through `node`; not on PATH) | archify 2.16.0 | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Body equality | `diff` of `/mnt/c/mybizz/mb-archify-scope/mb-archify-scope.md` and `~/.config/opencode/skills/mb-archify-scope/SKILL.md` after deleting each frontmatter block (first `---` through the closing `---`) — the bodies must be identical | agent |
| Installed version | `git -C /mnt/c/mybizz/mb-archify-scope log -1 --format="%h %s"` | agent |
| Works (dependency health) | `node /home/dev-p/.config/skills/archify/bin/archify.mjs doctor` — expects every check ok, "Archify is ready" | agent |
| Works (end to end) | a live `/mb-archify-scope` scoping run on a small subject — the skill's own Phase 7 gate makes this developer-run | developer |
| GBrain source | `gbrain sources list` — `mb-archify-scope` listed, federated, 1 page | agent |
| Layout budget current | compare the Configuration §Layout budget (dataflow) rows against `renderers/dataflow/README.md` in the installed archify package | agent |

## Do not

- Do not draw, author candidate JSON, or run the probe inside this skill — it
  scopes only; the probe executes in the Archify run.
- Do not proceed past Phase 7 without the developer's explicit approval.
- Do not copy the repo spec over the installed SKILL.md — it replaces the
  skill frontmatter (`name`/`description`) with doc frontmatter; sync is
  body-to-body (proven by the Body equality check above).
- Do not proceed past a failed probe — work returns to Phase 5 for reshaping,
  never onward.
- Do not write Phase 9 learnings unasked.
- Do not restate the Archify skill's authoring procedure, command reference, or
  checker workflow here — those live in the Archify skill and its suite; this
  skill is front-of-pipe only.
- Do not end an abort on a refusal — always offer reshaped plans.
