---
title: "mb-form-builder-reference"
doc-id: "mb-d971c150"
updated: "2026-11-12"
---

# mb-form-builder — Reference

Invocation, the eight sections, the gate, outputs, checks, and failure rules.
Mid-task lookup. What the skill is and why:
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-explainer.md).
Current state:
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-config.md).
Learnings:
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-learnings.md).
The canonical contract is the spec itself
([[[mb-form-builder:mb-form-builder|Form-Builder Skill Specification]]](C:/mybizz/mb-form-builder/mb-form-builder.md)) —
change spec and installed copy together.

## Invocation

Run in build mode, when the developer asks to build or rebuild one feature's
forms, naming the application and the feature (for example "mb-3-cs App 1,
feature `bookings`"). Model-invoked: the description carries the trigger
(mo-ui-production section 4, step 9).

## The eight sections (ordered)

1. **Rules it follows** — read the six sources before writing anything:
   spec-ui-standards; mo-ui-production section 5; spec-component-properties;
   spec-nomenclature section 1.6; spec-translation; Anvil's own `client-forms`
   skill. Where they and the skill differ, they win and the skill is corrected.
2. **Input** — read: every screen requirement of the feature
   (`{slug}-project-library/ui/<package path>/<FormName>/<FormName>-requirement.md`);
   the scaffold specification, user flows, authoritative schema and SRS from the
   project library; the theme's component documentation (`base-inventory.md`,
   `docs/components/<Component>.md`, the application's `docs/component-inventory.yaml`
   in `tests/`); `approved_components` in the application's `tests/ts-config.yaml`;
   the feature's server module in `server_code/`; the application's
   `access-matrix.yaml` and `client_code/shared/translations/en.py`.
3. **Gate** — stop and report, writing nothing, when: a form has no screen
   requirement or its front matter is not `status: approved`; the feature's server
   module does not exist; a server function a screen requirement names does not
   exist in that module; the application's `tests/component-inventory.yaml` is
   missing or differs from the theme library's; a screen requirement asks for a
   component, property, event or slot that is not in the inventory and is not an
   Anvil component in `approved_components`. The report names each failed
   condition and its file. Never guess a missing fact.
4. **Output per form** — write, at the form's module path: `form_template.html`
   (root per layout kind; every theme component as `type="m3.<inventory path>"`,
   never the legacy `form:dep_<id>:...` spec; every property as
   `prop:<name>="<JSON value>"` the inventory allows; every visible text and
   tooltip a phrase key; every editing input's writeback bound to
   `self.item['<key>']`; no `on:` attributes; no colour value; no sample data; no
   hyphen in any name; every element closed with its own closing tag, never
   `/>`); `__init__.py` (`from anvil import *`, the form class with
   `self.init_components(**properties)` then `translate_form(self)`, one
   `@handle` per event the screen requirement uses, body `pass`, one-line
   docstring naming the server function, no other logic); the spec sheet at
   `theme/assets/docs/app1/<package path>/<FormName>.md` with the six contents
   spec-ui-standards section 14.2 lists, holding no secret, key, password or user
   data; the form's entry in `access-matrix.yaml` under `forms`, keyed by module
   path, with every role's scope; the form's phrase keys in `en.py`.
5. **Old forms** — a new form at the same module path replaces the old files in
   place; an old form with no new form at its module path is removed with its
   spec sheet and its `access-matrix.yaml` entry; every reference to a removed
   form is updated, including `startup` in `anvil.yaml`, routes and navigation
   code; package folders and their `__init__.py` files are never removed.
6. **Checks** — from the application folder run `anvil --json validate
   client_code` and `python3 <project-library-global>/test-suite/tools/ts_scan.py
   . --config tests/ts-config.yaml`; fix every failure in the feature's files and
   rerun both until both pass; stop and report when the same failure happens
   twice, or when a fix would touch a file outside the feature.
7. **Report** — end with the forms written, replaced and removed by module path;
   the other files changed; the result line of each check; anything the screen
   requirements left open.
8. **Never** — never fill an event handler body (that is the Anvil agent's
   task); never change server code, the data table schema or another feature's
   files; never commit; never use `Label`, `HtmlTemplate`, `HtmlPanel`, Anvil
   Extras, a YAML form template, or a component, property or value that is not in
   the theme's documentation.

## Keeping spec and installed copy in sync

1. Edit the body of `/mnt/c/mybizz/mb-form-builder/mb-form-builder.md`.
2. Apply the identical body change to
   `~/.config/opencode/skills/mb-form-builder/SKILL.md`.
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
| Form-Builder Skill Specification (repo) | [[[mb-form-builder:mb-form-builder\|mb-form-builder.md]]](C:/mybizz/mb-form-builder/mb-form-builder.md) | spec body, uncommitted (branch `main`) | 2026-11-12 |
| spec-ui-standards | [[[default:specifications-global/spec-ui-standards\|spec-ui-standards]]](C:/dev/project-library-global/specifications-global/spec-ui-standards.md) | current | 2026-11-12 |
| mo-ui-production | [[[default:specifications-global/mo-ui-production\|mo-ui-production]]](C:/dev/project-library-global/specifications-global/mo-ui-production.md) | current | 2026-11-12 |
| spec-component-properties | [[[default:specifications-global/spec-component-properties\|spec-component-properties]]](C:/dev/project-library-global/specifications-global/spec-component-properties.md) | current | 2026-11-12 |
| spec-nomenclature | [[[default:specifications-global/spec-nomenclature\|spec-nomenclature]]](C:/dev/project-library-global/specifications-global/spec-nomenclature.md) | current | 2026-11-12 |
| spec-translation | [[[default:specifications-global/spec-translation\|spec-translation]]](C:/dev/project-library-global/specifications-global/spec-translation.md) | current | 2026-11-12 |
| Anvil client-forms skill | installed OpenCode skill | current | 2026-11-12 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Body equality | `diff` of `/mnt/c/mybizz/mb-form-builder/mb-form-builder.md` and `~/.config/opencode/skills/mb-form-builder/SKILL.md` after deleting each frontmatter block (first `---` through the closing `---`) — the bodies must be identical | agent |
| Installed version | `git -C /mnt/c/mybizz/mb-form-builder log -1 --format="%h %s"` | agent |
| Works (form checks) | the skill's own section 6, inside a real build: `anvil --json validate client_code` and `ts_scan.py` pass from the application folder | developer |
| Works (catalog) | the skill appears in OpenCode's skill list from the next session start | developer |
| GBrain source | `gbrain sources list` — `mb-form-builder` listed, federated, 1 page after the first commit | agent |
| Registrations | `python3 /mnt/c/mybizz/scripts/mb-doc-check.py sources-check` — everything matches | agent |

## Do not

- Do not fill an event handler body — empty handlers with docstrings only; the
  Anvil agent wires them (mo-ui-production section 2).
- Do not change server code, the data table schema, or another feature's files.
- Do not use `Label`, `HtmlTemplate`, `HtmlPanel`, Anvil Extras, a YAML form
  template, or anything not in the theme's documentation.
- Do not copy the repo spec over the installed SKILL.md — it replaces the skill
  frontmatter with doc frontmatter; sync is body-to-body (proven by the Body
  equality check above).
- Do not commit — only the developer commits, with commit-all.
- Do not guess a missing fact — the gate stops and reports instead.
- Do not proceed past the gate while any condition fails.
