---
title: "mb-form-builder-explainer"
doc-id: "mb-6a95aa88"
updated: "2026-11-12"
---

# mb-form-builder — Explainer

Orientation, suitability, and reasoning for the `mb-form-builder` form-building
skill. State:
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-config.md).
Procedure:
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-reference.md).
Learnings:
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-learnings.md).

## What it is

The UI-production method rests on one idea: the written form is the wireframe.
A form's screen requirement is the design the developer approves; the form the
application ships must be that design, exactly. `mb-form-builder` is the step
that makes that true mechanically: it takes one feature's approved screen
requirements and writes every form of the feature as a real Anvil form — the
HTML template built from the theme's documented components, the empty Python
form class, the spec sheet the Anvil agent reads, the access-matrix entry and
the phrase keys. It is the only way forms are produced, so a form cannot drift
from its approved design, the theme's component inventory, or the access model.
It builds; it never wires — the Anvil agent fills the event handlers afterwards.

## What it can do

- Turns a feature's approved screen requirements into complete, checkable forms
  in one run, replacing or removing old forms of the same feature as the design
  changed.
- Holds every form to the theme's component inventory: only documented
  components, properties and values, plus the approved Anvil components.
- Produces the spec sheet — the same design restated for the Anvil agent, in
  the only place in the application the agent reads documents from.
- Keeps the access matrix and the phrase keys in step with the forms it writes.
- Repairs the references a removed form leaves behind, including `startup` in
  `anvil.yaml`, routes and navigation code.
- Closes its own loop: the platform validator and the UI-standards scanner must
  both pass before the run reports done.

## Suitability

**Best for:** a feature whose screen requirements are approved and whose server
module and functions already exist — the run then writes the whole feature's
forms, old and new, in one pass.

**Not good for:** anything the gate excludes — a form without an approved
screen requirement, a missing server module or function, an inventory out of
step with the theme. Also not the tool for wiring handler bodies (the Anvil
agent's task), for server code or schema changes, or for a one-off form change
outside a feature — that route goes through the screen requirement first. The
skill never commits.

## Why it works this way

**Why the gate comes first.** Only an approved screen requirement is built —
the requirement is the design the developer approved, so building from anything
else invents design. The gate also refuses a missing server module or an
inventory drift, because both would force the skill to guess, and guessing is
the one thing a production path must not do.

**Why HTML templates from the inventory.** The theme's component inventory is
the contract between design and code: every component, property and value a
form uses must be documented there, or be an approved Anvil component. Writing
the template against the inventory — never a legacy YAML template — is what
makes the Anvil editor view, the checks and the theme upgrades all agree.

**Why the handlers stay empty.** Building and wiring are separate reviews: the
skill writes the shape of every handler with a docstring naming its server
function, and the Anvil agent fills the bodies. A body written here would be
un-reviewed logic smuggled past both reviews.

**Why the spec sheet is public and secret-free.** It lives in `theme/assets/`,
which is public by position — so the skill itself requires it to hold no
secret, key, password or user data, and security-global's HTMLTemplate ban
holds twice over: the skill never emits one, and user text never reaches one.

**Why the checks stop on a repeat failure.** A fix-loop that fails the same way
twice, or that reaches outside the feature's files, is no longer fixing — it is
spreading. Stopping turns that into a report instead of a mess.

## What has to happen

- Every screen requirement reaches `status: approved`, and the server module
  and its functions exist, before a run — the gate enforces it, but only the
  method around the skill produces them.
- The application's `tests/component-inventory.yaml` stays identical to the
  theme library's `docs/component-inventory.yaml`; when the theme moves, the
  copy moves with it.
- Spec and installed copy move together, body-to-body, by hand (Reference
  §Keeping spec and installed copy in sync); the installed-copy write is
  grant-gated.
- Commit all runs at every close-out; its GBrain sync is what keeps the
  `mb-form-builder` source current.

## S.W.O.T.

**Strengths.** One production path for every form; the gate stops fabrication
before it starts; the checks close the loop inside the run; old forms and their
references are repaired in the same pass.

**Weaknesses.** No real run yet — proven by design and by the verified live
setup; spec and installed copy have no mechanical sync, so the
spec-edited-after-install drift class stays real and is caught only by the
Body equality check.

**Opportunities.** The first feature run feeds the learnings table and calibrates
the gate against real screen requirements.

**Threats.** Inventory drift between the theme library and the application
copy — caught by the gate; a screen requirement that outgrows the inventory —
caught by the gate and resolved in the theme, not in the form.

---

*Companion documents:
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-config.md) (current state),
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-reference.md) (procedures),
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-learnings.md),
and the canonical spec
([[[mb-form-builder:mb-form-builder|Form-Builder Skill Specification]]](C:/mybizz/mb-form-builder/mb-form-builder.md), repo).*

*End of document*
