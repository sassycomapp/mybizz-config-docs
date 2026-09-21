---
doc-id: 1-plan
document: "Work Package 1 — Read-only Baseline Inspection"
date-created: 2026-08-14
title: Work Package 1 — Read-only Baseline Inspection
report: package-1-plan
date: 2026-08-14
time_utc_plus_2: 2026-08-14 12:48 +0200 (SAST)
state: Complete (read-only gate)
repo: mb-3-cs
---

# Work Package 1 — Read-only Baseline Inspection

Read-only baseline inspection of `mb-3-cs` covering Git, GBrain, Graphify,
AGENTS.md references, and Graphify output/ignore files. No files, databases,
hooks, configs, packages, or agent instructions were modified.

---

## 1. Git state — `mb-3-cs`

- **Status:** clean working tree, `## master...origin/master` (in sync, no
  unpushed commits)
- **HEAD:** `e29cbd1b959ff91812982cd71c45c3ae57da3df2` — "Edited settings"
- **Recent log (10):**
  - `e29cbd1` Edited settings
  - `e8f7279` Edited theme/parameters.yaml
  - `4592e48` Edited settings
  - `93ecd14` Edited analytics/auth + 49 more forms
  - `cd7f0b9` Edited theme.css
  - `a8f19f4` Created anvil-ui-build-standard-v1.md
  - `aa439d1` Edited settings
  - `db2e46a` Edited theme.css, BookingViewerForm, .gitignore
  - `5b6734f` Created blog.CommentModerationForm + template
  - `a752393` Edited blog.CategoryManagementForm
- **Remote:** `origin https://github.com/sassycomapp/mb-3-cs`

## 2. GBrain

- **Binary:** `/home/dev-p/.bun/bin/gbrain`
- **Version:** `0.43.0.0` — **update available: `0.45.12.0`** (not applied;
  self-upgrade is forbidden)
- **Engine:** `postgres` (config `postgresql://postgres:***@localhost:5432/gbrain`);
  config also carries `database_path: /home/dev-p/.gbrain/brain.pglite`
- **Schema pack (active):** `gbrain-everything@1.0.0+7021205a`
  (source_tier `home-config`); 30 page types, 12 link types
  - primitives: temporal 9 / media 9 / concept 5 / entity 4 / annotation 3
- **Installed packs:** `gbrain-everything` (bundled also present: base,
  recommended, creator, investor, engineer, everything, base-v2)
- **Stats:** 1118 pages · 2269 chunks · 2269 embedded · 382 links · 5 tags ·
  0 timeline entries
- **Pages by type:** concept 548 · code 254 · atom 217 · note 85 ·
  extract_receipt 14
- **Embedding:** `openai:text-embedding-3-large` (1536 dims);
  expansion/chat `openai:gpt-5.2`
- **Sources (10):** all local paths, none remote.
  - `mb-3-cs-code` → 263 pages, last sync `2026-08-11 07:43`
  - Only `default` is `federated: true`
- **Source strategies:** no per-source `strategy` field stored or exposed
  (verified via `sources list`, `sources status`, `sources --help`). Strategy is
  a **sync-time flag** (`sync --strategy code`). The AGENTS.md claim "synced with
  `strategy: code`" describes how the sync was run, not a stored config.
- **Sources health:** all embed 100%, mostly idle. **`mb4ecom-code` shows
  `queued(1)` (1 job in queue).**

## 3. Graphify

- **Binary:** `/home/dev-p/.local/bin/graphify` (Python script, ASCII text
  executable)
- **Version:** `0.9.40` (matches `.graphify_version`)
- **Skill:** `/home/dev-p/.config/opencode/skills/graphify/` — `SKILL.md`
  (40 KB) + `references/` (add-watch, exports, extraction-spec,
  github-and-merge, hooks, query, transcribe, update)
- **OpenCode plugin:** `.opencode/plugins/graphify.js` present and registered in
  `.opencode/opencode.json`
- **Git hooks:** **NOT installed** (post-commit / post-checkout / merge driver
  all absent)
- **Graph output:** **none** — no `graphify-out/` in either repo, no
  `.graphifyignore`, global graph empty (`~/.graphify/` does not exist)

## 4. AGENTS.md mentions (GBrain / Graphify)

- Lines 71–77, "Access Model" section only:
  - `mb-3-cs-code` synced with `strategy: code`, real Python indexed
  - Graphify "installed and configured … Tree-sitter parsing …
    master-task-list.md Task 3.7"
- No Graphify `opencode install` section exists in AGENTS.md; the only reference
  is the Access Model bullet.

## 5. Graphify output / ignore files

- **None present.** No `graphify-out/`, no `.graphifyignore`, no `graph.json`
  anywhere under either repo.

---

## Anomalies

1. **GBrain version drift:** `0.43.0.0` vs available `0.45.12.0` (self-upgrade
   forbidden — do not resolve).
2. **Graphify tooling installed but graph never built:** skill + plugin present,
   but zero `graphify-out/`, zero git hooks, empty global graph. "Installed and
   configured" is accurate at the tooling layer only; the knowledge graph
   artifact for this repo does not exist yet.
3. **PGLite vs Postgres ambiguity:** config reports `engine: postgres` +
   `database_url` (Postgres), yet `database_path: /home/dev-p/.gbrain/brain.pglite`
   and a `brain.pglite/` directory exist. Likely a legacy/stale PGLite data dir
   from a prior engine; the live engine is Postgres. Not verified against the DB
   directly.
4. **Pending backfill:** `mb4ecom-code` source has 1 queued backfill job.
5. **AGENTS.md cross-reference unverified:** the `master-task-list.md Task 3.7`
   reference for Graphify's role was not inspected (out of scope for this gate).
6. **Missing timestamp-standard ADR:** the [[adr-timezone-utc-storage-display-conversion|Client Timezone: IANA String, UTC Storage, Display-Time Conversion]]
   ADR referenced by both AGENTS.md files is not present on disk under
   `mb-3-cs-project-library`. The timestamp header on this report uses a plain
   UTC+2 (SAST) ISO-8601 value as a fallback because the authoritative
   conversion method could not be read.

## Unknowns

- Whether `brain.pglite/` is genuinely stale or still referenced by anything
  (would require read-only DB inspection — outside approved scope).
- Confirmation that `mb-3-cs-code` was actually synced with `strategy: code`
  rests solely on AGENTS.md; the 254 code pages are consistent with but do not
  prove it.

## Recommended next work package

This was the first gate — nothing to fix. The natural next step is a
**planning work package** to (a) build the Graphify graph for `mb-3-cs`
(`graphify extract`) if the Task 3.7 dependency-check objective is still active,
and/or (b) reconcile AGENTS.md's Graphify wording with reality (graph not yet
built, hooks not installed). Both are mutations and require explicit developer
approval before the Build agent acts.

---

## Housekeeping (asked separately at task completion)

1. **Commit/push** — read-only task, no files changed; nothing to commit/push.
2. **GBrain sync** — no code/docs changed in this repo; sync would be a no-op.
