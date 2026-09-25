---
title: "anvil-agent-references-reference"
doc-id: "anvil-agent-references-reference"
---
# anvil-agent-references — Reference: Install, Skills, and Technical Detail

Companion to [[anvil-agent-references-config|Configuration]] (state, inventory, open items)
and [[anvil-agent-references-explainer|Explainer]] (what this is and why). Agent-facing —
exact commands, exact per-skill rules, real technical constraints.
Config-management set: [[anvil-agent-references-exam-plan|Exam Plan]] (transient
job-spec — read second, every run), [[anvil-agent-references-exam-report|Exam Report]]
(last verified state), [[anvil-agent-references-log|Log]] (chronological events),
[[anvil-agent-learnings|Learnings]] (transient knowledge), [[anvil-agent-skill|Anvil Agent Skill]] (exam
skill canonical source). Architecture: [[config-manager-explainer|Explainer]].

---

## Installing the skills

### Codex

Full plugin (point a Codex plugin marketplace entry at the checkout), or manual per-skill symlink:
```sh
mkdir -p ~/.agents/skills
ln -s /mnt/c/mybizz/anvil-agent-references/skills/server-code ~/.agents/skills/server-code
ln -s /mnt/c/mybizz/anvil-agent-references/skills/client-forms ~/.agents/skills/client-forms
ln -s /mnt/c/mybizz/anvil-agent-references/skills/data-models ~/.agents/skills/data-models
```
Project-local: use `.agents/skills` instead of `~/.agents/skills`.

### Claude Code

```sh
claude --plugin-dir /mnt/c/mybizz/anvil-agent-references
```
Invoke plugin skills with the `anvil:` namespace: `/anvil:server-code`, `/anvil:client-forms`. Manual symlink alternative mirrors the Codex block above, into `~/.claude/skills/`.

### OpenCode (this environment's runtime)

Already installed: five symlinks in `~/.agents/skills/` (see config.md). Verify reachability:
```bash
cat ~/.agents/skills/<skill-name>/SKILL.md | head -5
```
Skills are invoked as slash commands (`/client-forms`, `/server-code`, …). **Do not create a second discovery path** — plugin/skill dedup is by discovery path; a duplicate path double-loads it.

### The required follow-up step, every app project

Installing the skills alone is not sufficient. Copy the resource section from the clone's `AGENTS.md` into the app project's own `AGENTS.md`. **This is a developer-run step** — standing policy prohibits AI writes to `AGENTS.md`/`CLAUDE.md`, and Cupcake's AI-governance-file rule blocks them when active (enforcement status per the qualifier in Universal editing boundaries).

Section to copy (current, from the clone's `AGENTS.md`, 5 roles):

```markdown
## Shared Anvil Resources

When a skill refers to host-provided Anvil resources, use the resources from this generated checkout:

- Anvil client stubs: `stubs/client/` - read-only Anvil API `.pyi` files for `client_code/`.
- Anvil server stubs: `stubs/server/` - read-only Anvil API `.pyi` files for `server_code/`.
- Anvil type references: `reference/types/` - generated `.d.ts` reference material for `anvil.yaml` and form templates.
- Anvil docs: `docs/` - agent-oriented Anvil docs, including dependency docs when present.
- Anvil skills: `skills/` - public workflows for common Anvil app-editing tasks.
```

(Adjust paths to the checkout location in the target project's context.) Skill-local `references/...` paths resolve relative to the active skill directory.

---

## Universal validation command

```sh
anvil --json validate <path>
```
Works against `anvil.yaml`, HTML/YAML form templates under `client_code/`, and Python files under `client_code/` or `server_code/`. Validate the whole app with `anvil --json validate .` when a change spans multiple file types or shared configuration. **Validation checks syntax and template generation — it does not prove runtime Anvil API names or dependency component properties actually exist.** Treat validation warnings as actionable even when validation succeeds overall.

---

## Universal editing boundaries

**Cupcake qualifier:** Cupcake's enforcement status is not fixed and should not
be assumed current at any given time — check [[cupcake-config|Cupcake Configuration]]'s Current
Operational Status before relying on any Cupcake-based statement below as
active, mechanical enforcement. The rules described here are standing policy
and what enforcement blocks when active; whether that enforcement is currently
running is a separate, changeable fact. The boundaries below remain the right
discipline regardless of enforcement status.

- Treat the app checkout as user-owned code.
- Never edit this generated `anvil-agent-references` checkout while working on an app.
- Never edit `.anvil/` dependency material inside an app checkout.
- Inspect `.anvil/deps/<package>/anvil.yaml` and dependency docs before guessing dependency APIs.
- Never guess unfamiliar `anvil.*` symbols, component properties, roles, or CSS hooks — confirm from stubs, dependency docs/files, or working examples.
- **Never AI-write `anvil.yaml`** — standing policy regardless of enforcement status; `cup-block-anvil-yaml-writes.rego` enforces it mechanically when Cupcake is active (status: qualifier above and [[cupcake-config|Cupcake Configuration]]). Stop and hand the change to the developer either way. The `anvil-yaml` skill's type reference and validation knowledge still apply for *reading, planning, and validating* manifest changes.

---

## Skill: `anvil-yaml`

**Purpose:** update `anvil.yaml` — services, app metadata, `db_schema`.

**Workflow:** read `anvil.yaml` + the Anvil YAML type reference (`reference/types/anvil-yaml.d.ts`) → make the smallest manifest change → `anvil --json validate anvil.yaml` → treat validation errors as authoritative.

**Rules:**
- Never guess field names.
- Never update `dependencies` directly — ask the user to do it in the Anvil IDE.
- `anvil.yaml` may get auto-formatted/re-ordered after edits.

**Data Tables specifics:**
- `client_config.enable_v2: true` = Accelerated Data Tables; missing/false = legacy.
- New `/runtime/services/tables.yml` entries should set `client_config.enable_v2: true`.
- Preserve an existing table's `client_config` unless the user explicitly asks to migrate.
- Default new tables to `client: none`. Use `search` only for intentional direct client searches; `full` only when the user explicitly requests unrestricted client table writes.
- Preserve non-empty `db_schema.*.indexes`; don't add new indexes unless explicitly asked and the plan supports them. New tables: omit [[indexes|Indexes]] or use `indexes: []`.

**Users table specifics:**
- Adding the Users service requires a matching `db_schema` Users table if `server_config.user_table` is set to a string key.
- Standard shape: `email` (string), `enabled` (bool), `signed_up` (datetime), `password_hash` (string), `confirmed_email` (bool), `remembered_logins` (simpleObject). May also include service-managed `last_login`, `n_password_failures`, `mfa` — never remove these if present.
- If `server_config.user_table` is a **number**, it's a legacy table id — never create a numeric `db_schema` key for it. Only edit an existing table if `table_id_hints` unambiguously maps the id to a table name; otherwise ask the user.

**Environment note:** the manifest *write* itself is Cupcake-blocked for AI when enforcement is active (see Universal editing boundaries) — use this skill to read, plan, and validate manifest changes; hand execution to the developer.

**Required user follow-up when `db_schema` changes:**
> Validation does not update the live database. You must resolve or apply schema changes in **Data Tables schema** in the IDE.

---

## Skill: `client-forms`

**Purpose:** create/inspect/edit/style/validate/convert Anvil client Forms.

**Native Libraries:** app-wide browser libraries and page-head assets are declared in `anvil.yaml`, at `native_deps.head_html` — the mechanism for a library the whole app needs (not per-Form).

**Core model:** a Form = one Python file + exactly one template file. Package Form: `client_code/**/<Form>/__init__.py` + `form_template.html`. Module Form: `client_code/**/<Form>.py` + `<Form>.html`. Legacy versions use `.yaml` instead of `.html`.

**Template kinds:** Layout Form (root `<anvil-form layout="...">`), Container Form (root `<anvil-form container="...">`, or implicit `HtmlComponent` container when no root tag is present). Legacy `HtmlTemplate` is a migration/compatibility case, not the default model — do not confuse it with modern `HtmlComponent`.

**First three moves, every time:**
1. Inspect the Form's Python and its one template together (also inspect the RepeatingPanel item-template Form if the task involves a parent list/table).
2. Identify the template kind before editing structure.
3. Choose the smallest normal pattern; load deeper reference/example files only when the task actually needs them (table below).

Before behavior changes, inspect enough of `anvil.yaml` to identify `startup_form`/`startup`. If the changed Form isn't startup-reachable and no nearby navigation path is evident, mention that in the handoff.

**Do:**
- Inspect Python + template together before changing components, handlers, bindings, or container/layout shape.
- Identify Layout Form vs. Container Form before editing template structure.
- Use `RepeatingPanel` + item-template Form for repeated rows, cards, list items, search results, order lines, notifications, and similar data-driven UI.
- Use `@handle(...)` for new component events unless preserving existing markup-wired style.
- Validate changed files before finishing.

**Don't:**
- Never render repeated data with raw DOM loops, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `createElement`, cloned DOM nodes, or HTML-string helper functions.
- Never guess unfamiliar `anvil.*` symbols, dependency component APIs, properties, roles, or CSS hooks — confirm from stubs, dependency docs/files, or working examples.
- Never hand-edit legacy YAML templates by default — convert to HTML unless the user explicitly wants YAML kept.
- Never wrap submit/save/server-call/Data Table paths in broad exception handlers — let unexpected errors raise; use `finally` only to restore UI state (e.g. button enabled/text).
- Never mix native DOM event signatures (`def handler(self, event)`) with Anvil component event signatures (`def handler(self, **event_args)`).

**Load-By-Task table:**

| Task trigger | Load |
|---|---|
| New or simple container Form | [[basic-container-form|Basic Container Form]] |
| Existing button/input handler edit | stay in the skill file; load [[dom-event-vs-component-event|Dom Event Vs Component Event]] only if event source is unclear |
| No root `<anvil-form>` / implicit `HtmlComponent` container | [[template-shapes|Template Shapes]], then [[htmlcomponent-container|Htmlcomponent Container]] |
| Form using a layout with `<anvil-block>` | [[template-shapes|Template Shapes]], then [[layout-using-form|Layout Using Form]] |
| Form defining slots with `<anvil-slot>` | [[layout-defining-html-form|Layout Defining Html Form]], plus [[html-frontmatter|Html Frontmatter]] if custom properties/events are involved |
| Root shape, attribute prefixes, bindings, blocks, slots, dropzones, or event signature lookup | [[cheat-sheet|Cheat Sheet]] |
| `anvil:name`, `anvil:dom-node`, native DOM events, direct DOM access, runtime class/style helpers on plain HTML | [[html-dom|Html Dom]]; use [[dom-event-vs-component-event|Dom Event Vs Component Event]] for a concrete recipe |
| RepeatingPanel item templates, `writeback:`, or item refresh behavior | [[repeating-panel-item-template|Repeating Panel Item Template]] |
| Reusable component Form | [[custom-component|Custom Component]]; also [[html-frontmatter|Html Frontmatter]] for custom API metadata |
| Custom component container or `<anvil-dropzone>` | [[custom-component-container|Custom Component Container]] and [[html-frontmatter|Html Frontmatter]] |
| Legacy YAML template or converted `HtmlTemplate` | [[yaml-template|Yaml Template]], [[template-shapes|Template Shapes]], then [[yaml-htmltemplate-conversion|Yaml Htmltemplate Conversion]] |
| M3 or dependency component specs | inspect `anvil.yaml` and dependency docs/files first, then [[dependency-component|Dependency Component]] |
| Form Python class shape, handler signatures, lifecycle, client runtime caveats, dynamic updates | [[python|Python]] |
| `anvil.js`, `anvil.js.window`, browser APIs, JS proxies, Promises | the [[javascript-interop|Javascript Interop]] reference (below) |
| Roles, theme CSS, generated component DOM, dependency styling internals | [[styling|Styling]], [[styling-examples|Styling Examples]], [[component-dom|Component Dom]] |

**Simple event edits stay on the normal path** — adding/changing simple event wiring, matching handlers, fixed button/input behavior, or item-template bindings doesn't need the table, unless the task expands into layout restructuring, new Forms, YAML conversion, frontmatter, custom components, styling, data modeling, dependency APIs, reusable Forms, or raw DOM work. For newly added component events, prefer `@handle(...)`; use `on:<event>` only when preserving/extending existing markup-wired events.

**Form Python shape** — every Form file must define the Form class matching the last path segment, inheriting from its generated template class:
```python
from ._anvil_designer import Form1Template

class Form1(Form1Template):
    def __init__(self, **properties):
        super().__init__(**properties)
```
Decorator gotcha: use `@handle(...)` when the module has `from anvil import *`; use `@anvil.handle(...)` (or add the import) when the module has `import anvil`.

**Data Bindings and repeated items:** in item templates, prefer Data Bindings (`bind:text="self.item['name']"`, `writeback:text="self.item['name']"`) over Python assignments copying row fields into component properties. Keep repeated interactive elements and their handlers in the item template Form itself.

**Styling, by what's being styled:**
- Raw HTML elements: stable domain-specific classes in the template + selectors in `theme/assets/theme.css`.
- Dynamic raw HTML state: read [[html-dom|Html Dom]] before using plain-HTML runtime style/class helpers.
- Anvil components: component properties, roles, documented dependency APIs, `.anvil-role-<role-name>` CSS selectors.
- M3 or dependency components: inspect docs/dependency files before guessing properties, layout behavior, or CSS hooks.

**Legacy YAML → HTML conversion procedure:**
1. Check for a sibling HTML template first.
2. If sibling HTML exists, validate and use it; remove redundant YAML only after the HTML validates (unless the user wants YAML kept).
3. If no sibling HTML exists, run `anvil convert-template <path-to-yaml>` — validates the YAML, writes HTML, and deletes the source YAML on success.
4. Read the generated HTML, validate it, then continue editing the HTML template.

**Validation, precisely:**
```sh
anvil --json validate client_code/<Form>/__init__.py
anvil --json validate client_code/<Form>/form_template.html
```
Validate one changed file at a time, or a shared parent when changes span multiple file types. Treat validation *warnings* as actionable even on overall success. Before finishing: re-check component names, Python references, event handlers, plain HTML names, slot names, frontmatter boundaries, CSS selectors, and template paths. Suggest checking the changed Form in the IDE designer if layout/appearance changed.

**Gotcha:** `writeback:` mutates the bound target but does **not** refresh sibling Data Bindings — refresh explicitly when an editable field must update related bound UI immediately.

---

## Skill: `client-modules`

**Purpose:** edit non-Form client-side Python under `client_code/`.

**Scope test:** a module path (`client_code/**/<Module>.py`) or package path (`__init__.py`) with **no** matching `.yaml`/`.html` template — that's the line between a module and a Form.

**Rules:**
- Never create `client_code/__init__.py` — `client_code/` is an Anvil code root, not a Python package.
- Prefer relative imports for app-local references.
- Check the Skulpt client runtime reference (below) before adding stdlib or external imports.
- Use [[javascript-interop|Javascript Interop]] reference before touching `anvil.js`/`anvil.js.window`/browser APIs.

**Validate:** `anvil --json validate client_code/<Module>.py` (or the package's `__init__.py`).

---

## Skill: `data-models`

**Purpose:** design Anvil data architecture — model classes, buffering/drafts, Data Bindings, server methods — for persisted domain data.

**Defaults:**
- Prefer live Data Table rows / model classes over dict DTOs passed through server callables.
- Default tables to `client: none`; return rows/search results from server code. Client-writable saves use model `client_*` flags + checked `_do_*` hooks, never blanket `client: full`.
- For client-readable/writable views, return `client_readable(...)`/`client_writable(...)` directly, with `q.only_cols(...)` to restrict visibility as needed.

**Model class pattern** (a built-in Anvil feature, not a dependency):
```python
from datetime import date
from anvil.tables import app_tables

class TodoItem(app_tables.todo_items.Row, buffered=True):
    @property
    def is_overdue(self):
        return self["due_date"] < date.today()
```
Define in a client Module (importable from both client and server); import from app startup code and any server module touching that table.

**Editing flows:** bind components directly to row/model objects, especially in RepeatingPanel item templates. Use `buffered=True` or `row.buffer_changes()` when users can save/discard. Use draft rows for create flows — never grant `client: full` just to make creation work client-side.

**Server behavior:** `@anvil.server.server_method` for privileged instance/collection operations. Treat all non-`self` arguments to server methods as untrusted client input. Enforce ownership/identity checks in trusted server code, not client-supplied fields.

**When dicts are fine:** transient UI state, document-shaped API payloads, form scratch data with no backing row — never as the default transport for rows Anvil can pass directly.

---

## Skill: `server-code`

**Purpose:** edit Anvil server code Python modules under `server_code/` — server-callable functions, background logic, server packages — keeping changes isolated to the app workspace.

**Scope:** `server_code/**/<Module>.py`; `server_code/**/<Package>/__init__.py`.

**Rules:**
- Make server code changes under `server_code/`; do not edit `.anvil/`.
- Never create `server_code/__init__.py` — `server_code/` is an Anvil code root, not a Python package.
- Keep imports and package structure consistent with the app.
- Use the Anvil server API stubs (`stubs/server/`) for Anvil API references.
- For protected `@anvil.server.callable` functions, prefer declarative decorator arguments such as `require_user=` when existing server modules in this app already use that style for the same kind of access control.

**Datetimes and timezones:**
- Use Python's `datetime` for current timestamps.
- Anvil preserves timezone-aware `datetime` values across clients, server code, and Data Tables. A naive `datetime` crossing a boundary is stamped with the timezone where it was created: `datetime.now()` in server code is treated as UTC; in client code, as browser timezone.
- When an explicitly timezone-aware value is required, use `anvil.tz`.

**Validation and error handling:**
- For expected user-fixable validation failures that client code must display inline, prefer an explicit result object for simple form flows: `{"ok": False, "message": "Message is required"}` or `{"ok": True}`. Raise normally for unexpected Data Table, service, schema, or implementation errors; do not encode unexpected failures as `{"ok": False, ...}`.
- Do not rely on ordinary Python built-in exceptions raised by server callables (e.g. `ValueError`, `TypeError`) being catchable on the browser client as the same exception type. Cross the client/server boundary with exceptions only when the type is already a documented/catchable Anvil or app domain exception, or when deliberately adding a registered exception contract matching an existing app/runtime pattern.

**Workflow:**
1. Identify the target module or package.
2. Read nearby modules if the change touches shared logic or existing call patterns.
3. Make the smallest change that satisfies the task.
4. Validate changed Python files (below).

**Testing:**
```sh
anvil --json validate server_code/<Module>.py
anvil --json validate server_code/<Package>/__init__.py
```
No general automated server test path exists in this template — suggest testing the changed callable or background-task workflow in the app.

**Notes:**
- Server Python is typically 3.10.
- External server Python libraries go in `server_code/requirements.txt`.
- Server code can import client modules only when existing server code in this app already does so; otherwise keep shared server logic under `server_code/`.

---

## Supporting technical references

### Skulpt client runtime — real stdlib constraint

Client-side Python (`client_code/`) runs on **Skulpt in the browser, not full CPython.** Confirmed supported top-level stdlib imports:

`array`, `builtins`, `calendar`, `collections`, `datetime`, `fractions`, `functools`, `itertools`, `json`, `keyword`, `math`, `operator`, `platform`, `random`, `re`, `signal`, `string`, `sys`, `time`, `turtle`, [[types|1 represents the data is cached, 0 otherwise]], `typing`, `urllib`, `uuid`.

**Top-level availability doesn't guarantee submodule parity** — `collections` is available, `collections.abc` is not. External packages generally aren't available client-side unless the app or a dependency ships browser-compatible code. When client code needs unsupported behavior: move it to `server_code/` behind `@anvil.server.callable`, use Anvil/browser APIs via `anvil.js`, or use an already-present app-local/dependency client module.

### JavaScript interop — real conversion rules

**Imports:** browser global → `from anvil.js.window import Foo`; dynamic global → `import anvil.js` then `anvil.js.window[name]`; ES module → `anvil.js.import_from(url)`; theme ES module → `anvil.js.import_from("./_/theme/<path>")`.

**Type conversions:** JS string/number/bool/BigInt → Python primitives; `null`/`undefined` → `None`; `Symbol` stays wrapped. Mutable `Array` → backed `ProxyList` (shared mutation); frozen `Array` → copied `list`. `Map`/`Set` → `ProxyMap`/`ProxySet`. `Uint8Array` → `bytes`; other typed arrays/`ArrayBuffer` stay proxies. Python `list`/`tuple` → `Array`; `dict` → object literal; `set` → `Set`; `bytes` → `Uint8Array`. Other objects stay proxies. **JS calls accept positional arguments only.** Class-instance proxies never serialize to server code — extract data into plain serializable values first.

**Promise boundary:** a regular JS call returning a Promise **suspends Python execution and returns the resolved value directly** — write it like synchronous code:
```python
response = fetch(url)
data = response.json()
```
Never use `.then()`, `await_promise()`, or Python `async`/`await` for these. Use `await_promise()` only when Python already holds a raw Promise (a property, or a constructed `Promise(executor)`).

**Constructors:** call `Foo(...)` normally — interop auto-detects call vs. construct. Use `anvil.js.new(Foo, ...)`/`anvil.js.call(Foo, ...)` only to override incorrect detection.

**DOM/callbacks:** `anvil.js.get_dom_node(component)` for a component's DOM node; `anvil:dom-node="name"` → `self.dom_nodes["name"]`. JS errors surface as `anvil.js.ExternalError` (original at `.original_error`). Wrap Python callbacks with `anvil.js.report_exceptions` when a library might swallow callback errors. A suspending Python callback returns a JS Promise — confirm the called API accepts async callbacks.

---

## Material 3 theme reference (`docs/m3/`)

Not a skill — a component/theme reference inside `docs/m3/`: [[api|Api]] (generated API/attribute reference for the `m3` module), `components/` (`_index.md`, `components.md`, `layouts.md`, `colour-schemes.md`, `img/`), and `layouts.md`. Relevant whenever a task touches M3 components or layouts (see the `client-forms` Load-By-Task entry).

**What it is:** an open-source Anvil theme (`github.com/anvil-works/material-3-theme`) implementing Google's Material 3 design system. Currently in beta — not every M3 component is supported yet; components without a direct M3 counterpart are styled to match the M3 spec as closely as possible. Add via **Settings → Dependencies → Third Party**, dependency ID `4UK6WHQ6UX7AKELK`. Caution: an app with an existing theme may have CSS that conflicts with M3's — if styling looks wrong, try a blank M3 app to isolate the cause.

**Component index, by category:**

| Category | Components |
|---|---|
| Typography | Text, Heading, Link |
| Buttons | Button, Icon Button, Toggle Icon Button, Button Menu |
| Display | Card, InteractiveCard, Divider |
| Navigation | NavigationLink (pairs with the M3 Layouts) |
| Menus | ButtonMenu, MenuItem |
| Form Input | Checkbox, RadioButton, TextBox, TextArea, DropdownMenu, Switch, FileLoader, Slider |
| Feedback | LinearProgressIndicator, CircularProgressIndicator |

**The two M3 layouts:**
- **`NavigationRailLayout`** — Material 3 navigation rail; small number of app destinations. Notable properties: `navigation_rail_vertical_align`, `navigation_rail_collapse_to` (modal drawer or app bar).
- **`NavigationDrawerLayout`** — Material 3 navigation drawer; longer/hierarchical destination lists. Always collapses into a modal drawer on smaller screens.

Both expose a `show_sidesheet` boolean property:
```python
def m3_button_click(self, **event_args):
    self.layout.show_sidesheet = True
```

Full property/event references: [[api|Api]] in this checkout, plus Anvil's own docs. **`colour-schemes.md` is currently an empty draft stub** (`draft: true`, verified 2026-09-06) — nothing to document until Anvil publishes real content.

**Standing constraints in this environment:** [[adr-anvil-extras-exclusion|Anvil Extras Exclusion]] excludes Anvil Extras (M3 conflict) and limits UI to M3-dependency components; [[adr-htmltemplate-use|HTMLTemplate Use]] bans `HTMLTemplate` — prefer the two native M3 Layouts.

---

## Update procedure (developer-run only)

```bash
git -C /mnt/c/mybizz/anvil-agent-references pull
```

- Developer-run only, from a terminal — never AI-invoked (the clone sits outside every project root; an AI-run write there is a cross-project write, which Cupcake's cross-project-write rule blocks when active — enforcement status per the qualifier in Universal editing boundaries and [[cupcake-config|Cupcake Configuration]]'s Current Operational Status).
- Symlinked skills update automatically — nothing to re-link for existing skills.
- After an update, check for new/renamed skills (content is generated; names could change between releases):
```bash
ls /mnt/c/mybizz/anvil-agent-references/skills/
ls ~/.agents/skills/ | grep -E "anvil-yaml|client-forms|client-modules|data-models|server-code"
```
If the first list shows names not in the second, symlink the new ones:
```bash
ln -s /mnt/c/mybizz/anvil-agent-references/skills/<new-name> ~/.agents/skills/<new-name>
```
- After any update, re-verify this doc suite against the new HEAD (config.md records the drift status to check).

## GBrain sync

The clone is registered as GBrain source `anvil-agent-references-code` (non-federated). Content reaches GBrain by ordinary `gbrain sync` only — **never through Memory Governor's API** (permanent vendor-material bypass). Keeping the source current is the developer's own responsibility, alongside the update above.

---

## Do not

- Do not AI-write `anvil.yaml`, ever, in any project — standing policy regardless of enforcement status (Cupcake's anvil.yaml block enforces it mechanically when active); route the change to the developer.
- Do not AI-write any project's `AGENTS.md`/`CLAUDE.md` (including the per-project setup step) — standing policy (Cupcake's AI-governance-file rule enforces it when active); developer-run.
- Do not run the update `git pull` via AI/bash — developer-run only.
- Do not submit this source's content through Memory Governor — permanent bypass; ordinary `gbrain sync` only.
- Do not edit the generated checkout, or `.anvil/` dependency material in an app.
- Do not create a second discovery path for any of these skills — dedup is by discovery path; duplicates double-load.
- Do not guess unfamiliar `anvil.*` symbols, dependency properties, roles, or CSS hooks — confirm from stubs/docs/examples.
- Do not edit `dependencies` in `anvil.yaml` — IDE-only action, even for the developer-assisted path.
- Do not treat a successful `anvil --json validate` as proof a runtime API or dependency property exists — syntax and template generation only.
- Do not reference `docs/material-3/` or `C:\mybizz\skills-collective\` — both stale; real paths are `docs/m3/` and the clone directly.
