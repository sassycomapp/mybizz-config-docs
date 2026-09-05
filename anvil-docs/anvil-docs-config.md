# Anvil Docs — Configuration

Canonical current-state configuration record. Agent-facing. States facts
about this specific corpus, not general Anvil knowledge — see
`anvil-docs-explainer.md` for narrative and real incident history.

---

## Identity

| Item | Value |
|---|---|
| Real location | `C:\mybizz\config\anvil\anvil-docs` |
| Prior name | `anvil-synthesized-reference` (renamed) |
| Source clone (now deleted) | `anvil-runtime-reference`, cloned from `github.com/anvil-works/anvil-runtime` |
| Composition | Two absorbed sources: (1) scraped `anvil.works/docs`, 298 real pages across 19 top-level areas; (2) real runtime source code, absorbed from the clone's `doc/`, `services/`, `database/`, `html-form-parser/`, `client/`, `downlink/`, `uplink/`, `server/` |
| GBrain registration | **Not yet registered.** No source under `C:\mybizz` is currently registered with GBrain. Registration is a real, separate, still-open task. |
| Cupcake access | Cross-project read/write/delete whitelisted for this path, plus a `*.clj`/`*.cljc`/`*.cljs`/`*.edn` sensitive-file exemption (both applied during the absorption task) |

## Folder structure — real conventions

| Convention | Rule |
|---|---|
| URL-slug naming | Folder/file name = exact last path segment of the real `anvil.works/docs/...` URL |
| Parent vs. leaf | A page with children is a directory; a page with no children is `{slug}.md` |
| `_index.md` | Every directory's own page content lives in `_index.md` inside it |
| Frontmatter | Every scraped page starts with a 3-line YAML stub: `title`, `url` |
| Runtime source placement | Not a 1:1 mirror of the runtime clone's own folder structure — absorbed **by subject**, alongside the matching documentation topic (e.g. Stripe source sits in `integrations/stripe/`, not in a separate `services/` tree) |

## Five topic folders with no official-site equivalent

Created specifically to hold real runtime source with no natural documentation-page home:

| Folder | Real content |
|---|---|
| `app-structure/` | The real `anvil.yaml` schema and app directory layout (from the clone's `doc/app-structure.md`) |
| `integrations/segment/` | Segment analytics integration source |
| `integrations/airtable/` | Airtable integration source |
| `integrations/oauth/` | Shared OAuth protocol engine (`oauth.clj`) — used underneath Google/Facebook/Microsoft, not specific to any one of them |
| `client/forms/html-form-parser/` | Real `.cljc`/`.cljs` source for parsing `.html` form templates into Anvil forms |

## `tests/` — a real, preserved example application

`tests/apps/SmokeTest/` is a genuine, complete, minimal working Anvil application — real `anvil.yaml` with a real `db_schema`, real client/server code, real theme configuration. Kept deliberately as concrete, working reference material, not deleted as test scaffolding. The surrounding CI/test-harness files (`run_tests`, `Dockerfile*`, `py_tests/`, `configs/`) were also kept, by explicit developer decision, rather than the originally-planned selective extraction.

## Known, confirmed content gaps

- **`_components.py`** — two real files (originally symlinks, converted to plain-text notes during absorption prep) reference a source that was confirmed, directly, not to exist anywhere in the real clone. Genuinely orphaned — not a processing error.
- **91 files deliberately excluded from `server/`** — confirmed platform-operations code (worker pools, accounting, metrics, SSO protocol internals below what app code touches, the Runtime's own build/test tooling). Real, deliberate exclusion, not an oversight — see `anvil-docs-explainer.md` for the reasoning.
- **16 "Group C" files** (in `downlink/`/`uplink/`, dereferenced from symlinks before absorption) — confirmed byte-identical to their real counterparts already present elsewhere in this corpus via the `services/`/`client/` absorption, then deleted as genuine duplicates. Not unique content.

## Real, confirmed absorption source (for provenance/audit)

| Item | Value |
|---|---|
| Real upstream commit | `34067eb` — "Anvil App Server v1.17.0" |
| Real upstream branch | `master` |

## Do not

- Do not assume this corpus's folder structure is a 1:1 mirror of the
  Anvil Runtime's own source tree — it's reorganized by subject.
- Do not assume GBrain can already search this corpus — registration
  has not happened yet.
- Do not treat the 91 excluded `server/` files as missing by accident —
  they were deliberately judged non-content. See the explainer for the
  real reasoning per category.
- Do not attempt to resolve `_components.py` — confirmed, directly, to
  have no real source anywhere in the original clone.
