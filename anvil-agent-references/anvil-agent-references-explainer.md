---
document: "anvil-agent-references — Explainer"
doc-id: anvil-agent-references-explainer
state: Live
date-created: 2026-09-06
---

# anvil-agent-references — Explainer

*Companion note: for current confirmed state (paths, versions, inventory,
policies, open items) see `anvil-agent-references-config.md`. For exact
commands, per-skill rules, and technical detail, see
`anvil-agent-references-reference.md`.*

---

## 1. What this actually is

Anvil apps have their own conventions an ordinary coding agent doesn't know out
of the box: a Form is a paired Python file plus template file, not a single
component file; `anvil.yaml` is a manifest controlling services, startup, and
database schema all at once; the client-side Python runtime isn't full CPython.
Without correction, an agent working on an Anvil app is guessing at a framework
it wasn't trained to know in detail — inventing plausible-sounding APIs,
missing the manifest implications of a schema change, or writing client-side
code that assumes stdlib modules that don't exist in the browser.

`anvil-agent-references` is Anvil's own official answer to that problem: a
generated package of skills, type stubs, and reference docs, published by Anvil
itself through an automated release workflow from Anvil's main source
repository, so an AI coding agent has an authoritative source to consult
instead of guessing. It makes an agent Anvil-literate for the duration of a
task, the same way a human developer consults Anvil's own docs before touching
an unfamiliar part of the framework.

## 2. What it can actually do

- Validate an `anvil.yaml` manifest change against real schema rules before it's trusted, including Data Tables and Users-table-specific shape checks.
- Identify which of four different Form/template shapes a given file is, and edit it according to the rules that actually apply to that shape.
- Convert a legacy YAML Form template to the current HTML template format, automatically, with validation before and after.
- Distinguish a Form file from an ordinary client-side module by a mechanical test, so the right editing rules apply to the right kind of file.
- Design a Data Table's model-class architecture (validation, derived properties, buffered/draft editing) rather than leaving that decision ad hoc per Form.
- Edit server modules under a discipline matching their real risks: timezone stamping across the client/server boundary, exception contracts that survive that boundary, and declarative auth decorators consistent with the app's own patterns.
- Warn against, and route around, real runtime mismatches — unsupported client-side stdlib modules, and the JavaScript-interop Promise behavior that looks synchronous but isn't handled the way it appears.
- Point to Material 3 component, layout, and API reference material when a task touches Anvil's M3 theme.

## 3. Suitability

**Best for:**
- Any direct edit to an Anvil app's `client_code/`, `server_code/`, or `anvil.yaml` — squarely what the skill set was built for.
- Anvil-specific structural decisions: which Form/template shape to use, how a Data Table should be modeled, whether something belongs client-side or server-side.
- Any task where the alternative is an agent guessing at an Anvil API it doesn't actually know — precisely the failure mode the skill set exists to prevent.

**Good for / adequate for:**
- General Material 3 theming questions, where the component reference is useful but actual UI decisions still require ordinary design judgment.
- Cross-referencing dependency component behavior — the skills point toward checking dependency docs/files but don't themselves document third-party dependencies beyond the platform's own (the Stripe stubs cover Anvil's Stripe service API surface).

**Not good for / wrong tool for:**
- Anything outside an Anvil app entirely — no relevance to `dev-makepdlf` tooling, GBrain, Memory Governor, or any non-Anvil part of this system.
- Deciding *whether* a feature should exist or how it should behave from a product standpoint — implementation-mechanics skills, not product-design skills.
- Actually *executing* `anvil.yaml` manifest changes in this environment — standing policy prohibits AI writes to that file, and Cupcake blocks them when active (enforcement status changeable — see §8); the skill's knowledge applies to reading, planning, and validating, while the write itself is a developer action either way.
- Anything the `anvil-yaml` skill itself declines to do unilaterally — dependency changes are routed back to the developer in the Anvil IDE.

## 4. Runtime applicability — confirmed, not assumed

Upstream documents install paths for Codex and Claude Code; OpenCode is not
mentioned anywhere in the vendor documentation. That gap turned out not to
matter: the repo also documents a generic manual method — symlinking skill
folders into `~/.agents/skills/` — with no host restriction, and that method is
what this system uses. It is now confirmed working, not merely plausible: all
five skills resolve through their symlinks and appear in OpenCode's own skill
catalog, with no duplicate discovery paths. The `.codex-plugin/`/`.claude-plugin/`
metadata describes vendor packaging for the other two runtimes and is inert here.

## 5. Why five skills, not one — the underlying logic

Each skill maps to a distinct artifact type in an Anvil app, and each artifact
type carries a genuinely different blast radius when an edit goes wrong:

| Skill | Artifact | Blast radius of a bad edit |
|---|---|---|
| `anvil-yaml` | The app manifest | Highest — controls services, startup, schema for the whole app |
| `data-models` | Data architecture decisions | High — a wrong trust boundary or table-access model is a security question, not a syntax question |
| `server-code` | Server modules | High — server code is the trust boundary itself; auth, data integrity, and error contracts live here |
| `client-forms` | UI (Form Python + template pairs) | Medium — visible, but scoped to one Form/component |
| `client-modules` | Plain client-side Python | Medium — scoped to one module |

A single unified skill would apply the same editing discipline to a manifest
change (which can silently break the whole app) and a button-handler tweak
(which can't). The split lets each skill carry editing discipline proportional
to its actual risk.

### `anvil-yaml` — why the manifest gets the most caution

`anvil.yaml` is the one file controlling services, startup behavior, and the
Data Tables schema simultaneously. A wrong field name here isn't necessarily a
syntax error the validator catches cleanly — it can be a structurally valid but
semantically wrong manifest, silently misconfiguring the app. That's why this
skill's discipline is the tightest in the set: never guess a field name, never
touch `dependencies` (kept IDE-only, deliberately out of an agent's reach),
always validate before trusting an edit. In this environment the caution is
also expressed as enforcement: Cupcake's anvil.yaml write block, when active,
makes the AI-side write mechanically impossible — the mechanical expression of
the same judgment the skill encodes as discipline (enforcement status is
changeable, not a permanent fact — see §8).

### `client-forms` — why it's the largest skill, and why the Load-By-Task table exists

A Form is always a Python file paired with exactly one template file, and Anvil
supports four different template shapes (Layout Form, explicit Container Form,
implicit `HtmlComponent` container, legacy `HtmlTemplate`) that behave
differently enough that an edit correct for one is often wrong for another. The
"first three moves" — inspect both halves together, identify the shape, pick the
smallest fitting edit — exist to stop an edit being applied under the wrong
shape's assumptions. The Load-By-Task table is a deliberate middle path between
loading Anvil's entire template-syntax reference for every trivial edit and
never loading deeper material for genuinely complex cases: the *complexity of
the task*, not a blanket policy, decides how much reference gets pulled in. The
`writeback:` gotcha is the clearest example of why inspect-before-editing
matters here: a real Anvil behavior that looks like it should propagate and
doesn't, failing silently rather than loudly.

### `client-modules` — why it's a narrow, almost mechanical skill

This skill answers one question correctly before anything else happens: is this
file a Form, or an ordinary module? The distinction is mechanical (a matching
`.html`/`.yaml` template means Form; its absence means module), which is exactly
why it's worth a dedicated skill rather than judgment — getting it wrong means
applying Form-editing assumptions to a file that has none, or the reverse. Its
other role is a pointer: before an unfamiliar import, defer to the Skulpt
constraint (below).

### `data-models` — why it's a design-time skill, not an editing-time skill

`client-forms` is consulted while editing something whose data shape is already
decided. `data-models` is consulted *before* that decision is made. Collapsing
them would mean a UI-editing task could silently carry data-architecture
authority it shouldn't have, and a skill meant to reason about trust boundaries
and server-method authorization would also carry template-syntax concerns
unrelated to that reasoning. Its central pattern — a model class extending
`app_tables.<table>.Row` directly — gives row-local behavior and validation one
home instead of loose dicts and re-implemented logic. Its server-method rule
(every non-`self` argument is untrusted) is the same server-is-the-trust-boundary
logic `server-code` encodes — two skills independently arriving at the same
security posture because it's the correct posture for this platform.

### `server-code` — why its rules look the way they do

Server code is where the platform's security model actually lives, so its skill
discipline is about boundaries rather than syntax. Three rules carry the weight.
Timezone stamping: a naive datetime silently acquires the timezone of wherever
it was created (server = UTC, client = browser), so cross-boundary time
arithmetic is wrong by hours, invisibly — `anvil.tz` exists because the default
behavior is a trap, not a feature. Exception contracts: ordinary Python
exceptions don't reliably survive the client/server boundary as the same type,
so encoding expected failures as result objects and raising only for unexpected
problems keeps client-side error handling honest about what it can actually
catch. Declarative auth: preferring `require_user=` (when the app already uses
that style) puts access control in the decorator, where it can't be forgotten
the way an in-body check can. None of these are style preferences — each one
compensates for a specific, silent failure mode of the client/server boundary.

## 6. Cross-cutting runtime constraints — why these aren't just "gotchas"

### The Skulpt constraint

It's natural to think of `client_code/` as ordinary Python running in an unusual
place. It isn't — it's Skulpt, a browser Python implementation with a fixed,
short stdlib subset, and availability doesn't even guarantee parity —
`collections` exists, `collections.abc` doesn't. That specific kind of gap is
the dangerous one: it imports cleanly, looks fine in a quick check, and only
fails when the code reaches the missing submodule. A task trivial in ordinary
Python may genuinely need to move to `server_code/` behind a callable — not
because the logic is wrong, but because the runtime executing it doesn't
support it.

### The JavaScript interop Promise boundary

The single most counter-intuitive behavior in the whole skill set. A JavaScript
call that returns a Promise doesn't hand Python a Promise to `await` — it
suspends execution and returns the *resolved value* directly, so the call reads
like ordinary synchronous Python. The natural defensive instinct — wrap it in
`await_promise()` "just in case" — is actively wrong here, and it doesn't fail
loudly: `await_promise()` genuinely is correct in a different, visually similar
case (when Python already holds a raw Promise object). The two cases look alike
and require opposite handling — that similarity is why this is explained rather
than listed as a rule.

## 7. Material 3 — why two layouts exist, and when each actually fits

The M3 theme's two layouts embody two different navigation philosophies, not two
stylistic options for the same use case. The Navigation Rail is built for a small
number of top-level destinations and degrades gracefully on small screens —
collapsing into either a modal drawer or an app bar, developer's choice. The
Navigation Drawer is built for a longer, more hierarchical destination list and
only ever collapses one way (modal drawer), because a drawer's whole purpose is
accommodating more structure than a rail can. Which fits a given app is a real
information-architecture decision: a few flat top-level sections genuinely wants
the Rail; nested admin-style navigation genuinely wants the Drawer.

## 8. Where this component sits relative to the rest of the system

- **Relative to GBrain:** a content source, now formally one — registered
  2026-09-06 as `anvil-agent-references-code` (non-federated, mirroring the
  `-code` pattern), so the ordinary-sync path that feeds it has a real
  registered target instead of being a policy with nothing attached. It remains
  a permanent Memory Governor bypass: vendor-published reference material with
  no genuine confidence/contradiction judgment to make about it.
- **Relative to Cupcake:** two rules bear on it directly, and both express in
  enforcement what the skills express as discipline. One standing caveat governs
  everything Cupcake-related in this suite: Cupcake's enforcement status is not
  fixed and should not be assumed current at any given time — check
  `cupcake-config.md`'s Current Operational Status before relying on any
  Cupcake-based statement here as active, mechanical enforcement. What follows
  describes standing policy and what enforcement blocks when active, not a
  guarantee that it is running now. The anvil.yaml write block, when active,
  makes the `anvil-yaml` skill's tightest rule mechanically impossible to
  violate; the AI-governance-file block makes the per-project `AGENTS.md` setup
  step a developer action when active. Both are the right discipline regardless
  of enforcement state. The rest of the skills' editing boundaries ("never edit
  this checkout," "never edit `.anvil/`") are self-imposed by the skills, not
  Cupcake-enforced.
- **Relative to PDLF:** the platform ground truth under every coding step —
  one of the working sources beneath the whole pipeline, supplying what the
  build steps actually build against while GStack and Matt Pocock's skills
  supply process and engineering discipline.
- **Relative to the ADR set:** the M3-only component policy, the HTMLTemplate
  ban, and the platform-constraints catalogue bound what the skills' outputs
  may propose in this environment — the skills describe what Anvil *can* do;
  the ADRs decide what this system *allows*.
- **One trust caveat:** the repo publishes no license. The publisher is the
  platform vendor itself and the checkout is generated read-only reference
  material, so the practical risk is low — but a supply-chain review formally
  requires the license axis, and it's unmet on record.

## 9. What's genuinely still open, and why

The skills' editing discipline — validate before trusting, never guess an API,
inspect before editing — is fully documented and doesn't depend on anything
below being resolved. What does depend on the open items:

- **The pending upstream update** determines whether this suite describes the
  current checkout or a slightly older one; the repo republishes
  automatically from Anvil's source, so drift recurs by design and the update
  cadence is an operational habit, not a one-time fix.
- **The three app roots without per-project setup** are the gap between
  "installed" and "usable with full resource-path awareness" — until closed,
  agents working in those projects have the skills but not the resource paths
  the skills assume.
- **The license and adoption-review record** is a governance loose end, not a
  functional one — closing it makes the trust decision auditable like every
  other adoption in this environment.
- **No confirmed run record exists** for any of the five skills here; like the
  wireframe skill's first run, the first real invocation in an app project is a
  verification event, not a routine use.
