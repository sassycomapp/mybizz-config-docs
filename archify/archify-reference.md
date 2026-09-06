# Archify — Reference

Invocation, commands, authoring procedure, and failure rules. Mid-task lookup.
For what Archify is and why it works this way: `archify-explainer.md`.

---

## Invocation

`/archify`

All `node bin/archify.mjs ...` commands run from the skill package root
(`/mnt/c/mybizz/archify/archify`); absolute paths work equally.

## The five diagram types

| Type | Use for |
|---|---|
| `architecture` | Components, services, storage, cloud/security boundaries, infrastructure |
| `workflow` | Processes, approval gates, tool calls, runbooks, CI/CD |
| `sequence` | API call chains, request lifecycles, async traces, returns |
| `dataflow` | Pipelines, ETL/ELT, lineage, governance, consumers |
| `lifecycle` | State/status transitions, retries, waiting and terminal states |

When ambiguous: `node bin/archify.mjs guide "<scenario>" --json`

## Mermaid input mapping

| Mermaid | Archify type |
|---|---|
| `flowchart` / `graph` | `workflow` (or `architecture` for a component map) |
| `sequenceDiagram` | `sequence` |
| `stateDiagram` | `lifecycle` |

Read the Mermaid for topology and meaning; author fresh Archify JSON. Never mechanically render Mermaid styling.

## Authoring procedure (ordered)

1. **Choose the type** (table above; `guide` when ambiguous).
2. **Read** the matching schema in `schemas/`, `schemas/common.schema.json`, and one matching example in `examples/` — read only those files. Use the example for field shape, not facts. New workflow sources use `schema_version: 2`; keep v1 only when preserving an existing workflow's fixed geometry.
3. **Write the candidate JSON** before inspecting renderer internals. Do not plan exact coordinates in prose. Start with one clear main path, short side branches, sparse labels, at most 12 primary nodes. Set `meta.quality_profile` to `"showcase"` unless the user explicitly requests a dense `standard` map. Start with automatic routes and labels — no `via`, `channelX`, `channelY`, or `labelAt` before a diagnostic calls for one; apply at most one diagnosed geometry control per repair.
4. **Validate after every candidate edit and immediately before handoff:**

   ```bash
   node bin/archify.mjs validate <type> <candidate.json> --quality showcase --json
   ```

   A showcase pass = all 9 artifact checks, 0 composition errors, 0 warnings. A receipt with only 4 artifact checks is basic validation, never showcase acceptance. If `meta.quality_profile` is omitted or misspelled, fix it before geometry. Workflow v2 geometry diagnosis: `node bin/archify.mjs validate workflow <candidate.json> --layout-json` — use the stable compiler receipt; solver internals are not authoring controls.
5. **Deliver — the final acceptance command, run once:**

   ```bash
   node bin/archify.mjs deliver <type> <input.json> <output.html> --quality showcase --json
   ```

   A non-zero exit can never be described as success. A failed delivery preserves any previous output — never run `visual-check` on that path; it would inspect the stale last-good artifact, not the failed candidate.
6. **After successful delivery, collect bounded browser evidence:**

   ```bash
   node bin/archify.mjs visual-check <output.html> --json
   ```

   Measures first-screen containment at 1440×900, 1600×1000, 1920×1080, and 2048×1320; the machine receipt remains `visualReview: "pending"`. Chrome absence reports `skipped`, never a false pass.
7. **Keep the three claims separate** and report each independently: `deliver` proves deterministic artifact checks; `visual-check` proves bounded behavior in a real browser; perceptual polish requires a human or image-capable reviewer.

### Correction rounds

Apply only each `diagnostics[]` subject's `supportedFixes`; change only the diagnosed subject, verify its evidence. Continue while the objective error count reaches a new minimum. If two consecutive rounds do not improve that best count, stop and report the unresolved diagnostics truthfully.

## Full command list

| Command | Purpose |
|---|---|
| `node bin/archify.mjs doctor` | Verify the runtime (run after install or update) |
| `node bin/archify.mjs demo <output-directory>` | Generate demo artifacts |
| `node bin/archify.mjs guide "<scenario>" [--json] [--lang en\|zh]` | Type router for ambiguous requests |
| `node bin/archify.mjs validate <type> <input.json> [--json] [--layout-json] --quality standard\|showcase` | Schema/layout/artifact checks during repair |
| `node bin/archify.mjs deliver <type> <input.json> <output.html> [--json] [--open] --quality standard\|showcase` | Render + atomic commit of a passing artifact; final acceptance |
| `node bin/archify.mjs visual-check <output.html> [--json]` | Bounded browser evidence on the delivered HTML |
| `node bin/archify.mjs preview <type> <input.json> <output.html> [--no-open] --quality standard\|showcase` | Optional loopback desktop watcher — never start by default |
| `node bin/archify.mjs compare architecture <base.json> <head.json> <output.html> [--receipt path] [--json]` | Before/Delta/After review proof |
| `node bin/archify.mjs migrate workflow <old.json> <new.json> --to-schema 2 [--json]` | Non-destructive workflow schema v1→v2 migration |
| `node bin/archify.mjs inspect <type> <input.json>` / `check <output.html>` / `examples` | Inspection utilities |
| `node bin/archify.mjs brands [name] [--json]` / `brands capture <url> [--json]` | Brand-mark discovery / digest-pinned capture |
| `node scripts/check-update.mjs [--ack "<eventKey>"]` | Update-awareness checker |

## Authoring invariants (imperatives)

- One obvious main path; side branches leave the nearest main-path node. Remove low-value edges before adding routing controls.
- Omit `meta.visual_preset` by default so every diagram opens in `classic`; set `signal-flow`, `blueprint`, or `editorial` only on explicit request. Color mode and visual preset are independent — switching Light/Dark must preserve the current preset.
- Omit `meta.subtitle` by default. Never invent a subtitle that restates the title, nodes, or cards.
- Treat the artifact as a first-screen desktop deliverable: check 1440×900, 1600×1000, 1920×1080, plus 2048×1320 for large-desktop intent. Require `document.documentElement.scrollWidth <= window.innerWidth` and `scrollHeight <= window.innerHeight` at every checked size. Repair overflow by removing genuinely redundant content or compacting spacing — never with `overflow: hidden`, clipped content, an internal diagram scroller, stretched SVG height, or smaller typography.
- Omit `meta.legend` for the truthful `auto` default; when needed use only `mode: auto|all|hidden` with renderer-supported `entries.<kind>.label|visible` — labels never change semantics.
- Choose one primary authored language. `meta.locale` accepts only `"en"` or `"zh-CN"` (it localizes Viewer UI only — authored content is never translated). For every other language, omit `meta.locale` and explicitly disclose the English Viewer fallback.
- Preserve exact product names, code identifiers, commands, protocols, API paths, and environment names inside localized copy.
- Brand identity is optional and explicit: use built-in IDs discovered via `brands "<name>" --json`; for unknown official URLs supplied by the user, run `brands capture "<url>" --json` and author the returned digest-pinned object. Never infer a brand from a vague role such as "database"; never let a badge replace the semantic type, label, or relationship facts.
- Sequence diagrams: omit `meta.column_fit` for the stable `fixed` layout; set `"spread"` only when a wide viewBox would otherwise leave unused space or labels do not fit — never shorten semantic labels before trying `spread`.
- Component types: `frontend`, `backend`, `database`, `cloud`, `security`, `messagebus`, `external`; variants: `default`, `emphasis`, `security`, `dashed`.
- Relationship labels are semantic data. On collision: move the label, adjust route or spacing, then shorten wording while preserving meaning. Omit only wording already fully implied by both endpoints and containing no protocol, action, direction, sync/async behavior, or cross-boundary mechanism. Deleting a meaningful label is not a geometry repair.
- Omit `meta.engineering_profile` by default. Enable `deployment-ownership` only when the user explicitly asks for a production deployment topology, ownership handoff, or fail-closed deployment review and the source facts are known. Never remove the profile merely to pass validation — repair the facts or report the diagnostics truthfully.
- Spacing means clear gap, not center distance. A relationship label's clear gap must exceed its measured mask width; follow the label-preserving repair order.
- Automatic routes own their endpoint sides: the first and final segment must leave/enter perpendicular to that side. Never accept an edge crossing an unrelated opaque node, an ambiguous shared corridor, or a relationship label masking another route.
- Lifecycle: event/terminal column `N` in `0..2` aligns exactly beneath main column `N + 2`. A recoverable state uses `type: "failure"` plus a real transition back to the active state.
- Update awareness: after the first candidate exists, run `node scripts/check-update.mjs` once. `silent` → continue without mentioning it. `update_available` → show one compact notice (installed version, latest, the checker's fixed local summary, release-notes link; label `security` severity as a security update), then acknowledge by running the checker again with `--ack "<eventKey>"`. Never quote, summarize, or translate the remote manifest's summary; never download, install, or execute an update; silence is never consent.
- Do not read `renderers/shared/geometry.mjs`, renderer source, validator source, tests, or benchmarks before the first candidate exists. Inspect implementation only for an unsupported internal diagnostic or after two focused repairs fail.
- When shell access is unavailable: hand-place architecture SVG into `assets/template.html` using CSS semantic classes, and follow the visual review contract in `references/delivery-contract.md`.

## Deeper references (read only when needed)

| File | Read when |
|---|---|
| `references/authoring-contract.md` | You need field enums, spacing math, geometry repair rules, repository evidence, or mode-specific placement |
| `references/delivery-contract.md` | Using preview, repository evidence, export receipts, visual review, or post-commit opening |
| `references/viewer-runtime.md` | The user explicitly asks about Share Cards, Route/Reach cards, motion, guided stories, deep links, presentation, or search/focus |
| `references/brand-marks.md` | Authoring a brand for an unknown product with a user-provided URL |

## Do not

- Do not plan exact coordinates in prose — write the artifact first.
- Do not add `via`, `channelX`, `channelY`, or `labelAt` before a diagnostic calls for one; at most one diagnosed geometry control per repair.
- Do not edit a candidate after a passing final validation — it is frozen.
- Do not run `visual-check` on a failed delivery path.
- Do not describe a non-zero exit as success; do not claim visual inspection you did not perform.
- Do not exceed two correction rounds without a new minimum error count — stop and report.
- Do not delete semantic relationship labels as a geometry workaround.
- Do not invent subtitles, brands, topology, or viewer capabilities.
- Do not enable `deployment-ownership` without an explicit user request; do not remove it to pass validation.
- Do not start `preview` by default — it is an explicit opt-in desktop mode.
- Do not read renderer/validator source before the first candidate.
- Do not download, install, or execute updates — the user owns update decisions.
- Do not counterfeit viewport passes with `overflow: hidden`, clipping, internal scrollers, or shrunken typography.
