---
title: "gbrain-config"
doc-id: "mb-b677b7b4"
updated: "2026-10-10"
---
# GBrain — Configuration

> **Decision — GBrain's writer and ownership model (2026-10-07).** Not adopted now. It is decided together with the next GBrain upgrade, as one planned change. Until then no GBrain source is claimed or activated, because claiming stops ordinary sync until activation is complete. Writes into a source's folder (`put_page`, `gbrain capture`) are refused with `owner_unavailable`, so session pages are written as files and imported by commit all. Fact writes stored in the database (`remember`, `forget`) are not affected.

Canonical current-state configuration record for GBrain as a division-wide
system component. Agent-facing. Reflects the live-verified state as of
2026-09-13, updated 2026-09-30 for the GBrain upgrade to 0.59.18.0 (rows and
sections that changed carry that date; the rest was not re-measured). States
facts, not history — where the reasoning matters, see
[[[mybizz-config-docs:gbrain/gbrain-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-explainer.md) and [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md); for commands and
procedures, see [[[mybizz-config-docs:gbrain/gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md).

**System context (developer-stated, 2026-09-06; architecture context unchanged):** GBrain is one of six
closely-related components — GBrain, gbrain-dream-cycle, gstack,
memory-governor, PostgreSQL, and the installed `mb-submit-memory` skill — that
are assessed together, not in isolation. Cross-component reasoning lives in
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) (`mybizz-os-docs`), which owns the how-they-fit-
together layer; this suite owns GBrain-specific state, commands, and incidents.

---

## Identity

| Item | Value |
|---|---|
| Version | `0.59.18.0` (tag `v0.59.18.0`, commit `045a6138`) — upgraded 2026-09-30 from `0.46.1.0`; database schema **169** (was 128) |
| Version drift | `0.60.25.0` is the newest release (update banner 2026-10-01; not installed). An upgrade is a developer decision, made with the procedure in [[[mybizz-config-docs:gbrain/gbrain-reference\|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) §Upgrading — never on version-newness alone |
| Upstream | `github.com/garrytan/gbrain` — MIT; by Garry Tan; 29.6k stars / 1,061 commits (verified 2026-09-06). **Not distributed on npm** — the npm `gbrain` package is unrelated and shadows the binary (upstream warning; see [[[mybizz-config-docs:gbrain/gbrain-reference\|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) Do-not) |
| Engine | PostgreSQL 16.14, self-hosted, WSL-native; pgvector 0.6.0 |
| Connection | `postgresql://postgres:***@localhost:5432/gbrain` |
| Boot behavior | Auto-starts on WSL boot (`service postgresql start` in `/etc/wsl.conf`) |
| Executable | `/home/dev-p/.bun/bin/gbrain` → `~/.bun/install/global/node_modules/gbrain/src/cli.ts`; that global entry is a symlink to the checkout `/home/dev-p/gbrain` (bun link; verified 2026-09-30) |
| Install | **Live install:** `/home/dev-p/gbrain` — a Git checkout of `github.com/garrytan/gbrain`, in detached HEAD at tag `v0.59.18.0` (authoritative for diagnosis; linked, see Executable). Branch `master` still holds the previous state: upstream `v0.46.1.0` plus one local commit `b6250c43` (2026-09-23, a one-line diagnostic change in `src/core/cycle/extract-atoms.ts`, not on GitHub); the same commit is also on branch `pre-upgrade-backup`. **The `/mnt/c/mybizz/gbrain` source clone (v0.25.0) was deleted 2026-09-13** per developer decision — not the running code, referenced nowhere; upstream public, re-clonable |
| Config file | `~/.gbrain/config.json` |
| MCP surface | `mcp_surface` = `verbs` in the **database** config plane (`gbrain config get mcp_surface` → `verbs`, `[config] source: db plane`; verified 2026-09-30, before and after the upgrade); `~/.gbrain/config.json` carries no such key |
| Brain default source | `sources.default` — changed by the memory governor's worker before every governed write (`mybizz-os-docs` on 2026-09-30). A default that names a source that does not exist stops `gbrain sync` under 0.59.18.0 (incident 2026-09-30, see the reference). Fix: `gbrain sources default default` |
| Self-upgrade mode | **key absent from `config.json`** (developer-verified 2026-09-13, masked jq) — the documented `notify` behavior is the upstream default, not a verified key |
| Legacy artifact | `~/.gbrain/brain.pglite` — **removed** (confirmed absent 2026-09-12; live engine is Postgres; artifact no longer exists) |

## Backups

The **estate-wide backup convention** (all databases, both instances, both
locations, weekly exam-enforced cycle) is authoritative in
[[[mybizz-config-docs:postgresql/postgresql-config|Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) §Backups — this database estate is one system. GBrain
facts within it: the `gbrain` database (51 MB dump, 62 tables verified) and the
`memory_governor` database (26 KB dump, 5 tables) are both covered in every
cycle, delivered to `/home/dev-p/backup-gbrain/` (default) and
`/mnt/c/backup-gbrain/` (security net); pairs hash-verified (current cycle
2026-09-13: `6a6d60d57df162a4` / `e20b5694af64cdb7`).

**Pre-upgrade backups (2026-09-30)**, in `~/backups/` (private — the settings archive contains keys): `db-gbrain-before-upgrade.dump` (69 MB), `db-memory_governor-before-upgrade.dump` (67 KB), `dot-gbrain-before-upgrade.tgz` (147 KB, the whole `~/.gbrain` folder), `rollback-commit.txt` (the recorded checkout commit `b6250c43…`), the doctor reports `doctor-before.txt` and `doctor-after*.txt`, the per-source fact snapshots `recall-before-*.json` and `recall-after-*.json`, and `sources-before.json` / `sources-after.json`. Both dumps were checked readable. The rollback script restores them together with the old code. Retention is an open item.

## Schema pack

| Item | Value |
|---|---|
| Active pack | `gbrain-everything@1.0.0` (sha8 `7021205a`) |
| Page types / link types | 30 / 12 |
| Installed packs on disk | `gbrain-everything` only |
| Bundled, not installed | `gbrain-base`, `gbrain-recommended`, `gbrain-creator`, `gbrain-investor`, `gbrain-engineer`, `gbrain-base-v2` |

Known permanent limitation: no bundled pack extracts code-symbol call-graph
edges (`code` type is `extractable: false` in every pack); `code-callers`/
`code-callees` cannot resolve to defining chunks. Graphify's `get_neighbors`
is the correct tool — full account in [[[mybizz-config-docs:gbrain/gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) and
[[[mybizz-config-docs:gbrain/gbrain-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-explainer.md).

## Models

| Purpose | Model |
|---|---|
| Embedding | `openai:text-embedding-3-large` (1536 dims) |
| Chat / expansion | `openai:gpt-5.2` |

### Providers

| Role          | Provider                        | Status                           |
| ------------- | ------------------------------- | -------------------------------- |
| Embedding     | OpenAI (text-embedding-3-large) | ✓ active                         |
| Chat / Expand | OpenAI (gpt-5.2)                | ✓ active, will move to Anthropic |
| Reranker      | ZeroEntropy                     | ✓ confirmed active               |

## Live database statistics (verified 2026-09-13 — point-in-time; grows with every sync)

- 1,880 pages / 5,581 chunks / 5,581 embedded (100%) / 692 links / 9 tags
- By type: concept 972, code 307, note 194, atom 164, extract_receipt 20, email 5, media 4
- Not re-measured after the upgrade (`gbrain stats` gives current values). Doctor 2026-09-30, before the upgrade: 2,450 pages

## Registered sources (15 — verified 2026-09-30; page counts as listed that day, before the upgrade)

| Source ID | Path | Pages | Federation |
|---|---|---|---|
| `default` | `/mnt/c/dev/project-library-global` | 1,004 | **federated** |
| `anvil-agent-references-code` | `/mnt/c/mybizz/anvil-agent-references` | 34 | isolated (explicit, set 2026-09-30) |
| `data-mybizz-mgt` | `/mnt/c/data-mybizz-mgt` | 15 | **federated** |
| `dev-root-hub` | `/mnt/c/dev/dev-root` | 12 | **federated** |
| `mb-3-cs-code` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` | 262 | unset |
| `mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` | 566 | **federated** |
| `mb4ecom-code` | `/mnt/c/dev/dev-mb4ecom/mb4ecom` | 5 | unset |
| `mb4ecom-project-library` | `/mnt/c/dev/dev-mb4ecom/mb4ecom-project-library` | 5 | **federated** (2026-09-30) |
| `mb5pdlf-code` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf` | 5 | unset |
| `mb5pdlf-project-library` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf-project-library` | 12 | **federated** (2026-09-30) |
| `memory-governor-code` | `/home/dev-p/memory-governor` | 46 | unset |
| `mybizz-config-docs` | `/mnt/c/mybizz/mybizz-config-docs` | 270 | **federated** |
| `mybizz-os-docs` | `/mnt/c/mybizz/mybizz-os-docs` | 17 | **federated** |
| `pdlf` | `/mnt/c/pdlf` | 58 | **federated** |

Counts are per-source as listed on 2026-09-30 before the upgrade (point-in-time; they sum to the 2,450 pages the doctor reported; re-list for current values). The 2026-09-13 counts and total (1,880) are superseded.

**Federation states:** `federated` — appears in every other source's default search and may write links into other sources; `unset` (never set) — stays out of other sources' searches, but a session working inside it can still read the federated sources; `isolated` (explicit `gbrain sources unfederate`) — cut off in both directions. The four code sources and the Anvil clone are deliberately kept out of the federated search (decided 2026-10-01): Graphify handles code, and every other source is federated.

**Source names:** the Anvil project names are `mb-3-cs`, `mb4ecom` and `mb5pdlf`; `-code` occurs only in some source ids. `anvil-agent-references-code` is a read-only clone of Anvil's own public repository `anvil-works/anvil-agent-references`; the developer has no GitHub repository of his own for it. Its `-code` ending distinguishes it from the developer's own `anvil-agent-references/` documentation folder in `mybizz-config-docs` (reason as stated by the developer, 2026-09-30). It is separate from `anvil-docs` in the source `default`, the developer's own compilation.

All sources synced 2026-09-05 → 2026-09-13. **The `pdlf` source was registered 2026-09-11** ("PDLF System", federated, 59 pages) — the 14th source, consistent with the pdlf project going live. `data-mybizz-mgt` was registered later (session record 2026-09-15); two documentation-skill sources registered after 2026-09-13 were removed by the developer (reported 2026-09-30); on 2026-09-30 the developer federated every documentation source. The prior suite's
"deferred sources" framing is obsolete — every registered source currently
holds real, recently-synced content. Inactive-project sources stay registered
rather than removed (advisory memory retains value); only a content-free
scaffold was ever removed.

**Why a source is named `default`:** GBrain's own hardcoded fallback source ID
(upstream `docs/architecture/brains-and-sources.md`; resolution chain ends in
`fallback: 'default'`) — the first source this brain created. Not a
user-chosen name; do not rename.

## Content paths into GBrain (verified division of labor, 2026-09-06)

| Path | Mechanism | GBrain layer written | Carries | Real usage |
|---|---|---|---|---|
| **Sync path** | Standing script (`sync-gbrain.sh`: enumerates every registered source, runs `gbrain sync --source <id> --no-pull` for each, then `extract links --source db` and `embed --stale`; run it with `bash /mnt/c/mybizz/scripts/sync-gbrain.sh`); daily-ops.md documents per-repo sync as the standing after-work workflow | **Pages/corpus** | Whole repos: vendor bypass sources (anvil-agent-references, magdoub-wireframe — permanent governor bypasses), developer doc repos, project code+library sources | 18+ logged runs (2026-07-28 → 2026-09-13), then the script runs of 2026-09-30; every registered source; the dominant path by volume |
| **Governed path** | Developer or PDLF step → `mb-submit-memory` → governor API → promote → async `gbrain_write` → `remember` (MEMORY_VERBS) | **Facts layer** (hot memory) | Individual judgment-bearing content meant to be checked before becoming durable | Real runs: 2026-08-27 (promoted; its `gbrain_write` initially queued pending the dev-makepdlf source rename, since resolved), 2026-09-14 (logged), and 2026-09-30 (proof after the GBrain upgrade: `environment-explainer.md` from `mybizz-os-docs` promoted, memory_id `2cb82774-957c-4772-be3e-8d421f030c4a`; that fact landed in `memory-governor-code`, before the change of 2026-10-01 that sends facts to the owning project's source); `pdlf_step_sync` writer parked pending PDLF go-live |

**The boundary (by design, from [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md)):** sync must
never carry governed content — it would ingest raw content regardless of
governor approval; `remember` never creates corpus pages. Neither path
supersedes the other — they write to different layers and cannot substitute
for each other. Since 2026-09-28 the script enumerates every registered source itself (the earlier statement, verified 2026-09-06, was that it synced only the repo source).
`daily-ops.md` (located at
`C:\mybizz\mybizz-os-docs\operating-procedures\daily-ops.md`) documents the
sync path as the standing after-work workflow and predates the governed
path — its repo table was reconciled against the current source list
2026-09-18.

**GStack integration flow** (`/setup-gbrain`, 3-stage `/sync-gbrain`):
installed skills per upstream `USING_GBRAIN_WITH_GSTACK.md` — not this
environment's operational path; the custom script is (verified against
`logs/gbrain-logs/`).

## Scheduled jobs

| Item | Verified state |
|---|---|
| Crontab | A `gbrain autopilot` entry (every 5 minutes, targeting `--repo '/mnt/c/projects'`) was found **doubly inert** — cron daemon not running, target path from the pre-`C:\dev` layout no longer existing, log file never created — and was **deliberately removed 2026-09-06** |
| Design consequence | The Dream Cycle runs on-demand only; nothing GBrain-related is scheduled (see [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config\|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md)) |
| Sync | Manual: `bash /mnt/c/mybizz/scripts/sync-gbrain.sh`, or as part of `commit-all.sh` (about two minutes, longer after many changes; log in `C:\mybizz\logs\gbrain-logs\sync-<timestamp>.log`) |
| GBrain job queue | No GBrain worker runs, so the `extract` and `facts-absorb` jobs created by syncs wait unprocessed (34 waiting jobs were cancelled 2026-09-30 before the upgrade). Under 0.59.18.0 every waiting job must be authorized or cancelled before a worker starts |

## Health baseline (2026-09-30, after the upgrade and a clean sync)

| Item | Value |
|---|---|
| `gbrain doctor` | Overall **30/100**. The only FAIL is `cycle_freshness` (most sources have never completed a dream cycle — accepted, by design). Scoring: minus 20 per FAIL, minus 5 per WARN. Saved as `~/backups/doctor-after-sync2.txt` |
| Embedding provider | `openai:text-embedding-3-large`, 1536 dimensions, database aligned (probe OK; one probe failed and one took 20 seconds earlier the same day — a network problem that cleared) |
| Known warnings, not upgrade faults | atoms with stale source hashes (the permanent-code migration changed page contents; a dream cycle rebuilds them); links between repositories are collected only by `extract links --source db`, which the sync script runs; `extract_atoms` backlog (no cycle has run); `backup_coverage` (new check, see `gbrain backup status`) |

## OpenCode MCP integration

| Item | Value |
|---|---|
| Scope | global `~/.config/opencode/opencode.jsonc`, entry `mcp.gbrain` |
| Type / command | `local`; `["/home/dev-p/.bun/bin/gbrain", "serve"]` |
| Enabled | `true` |
| Environment passed | `OPENAI_API_KEY`, `ZEROENTROPY_API_KEY` |
| MCP bootstrap | servers start once at OpenCode process boot, never per chat session — config changes need a full process restart |
| Server version | `gbrain serve` was restarted with OpenCode after the 2026-09-30 upgrade — one process running the new code |

## Credentials

**Masking decision (standing, 2026-09-06):** the database URL appears in this
suite only as `postgresql://postgres:***@localhost:5432/gbrain` — structure
visible, password always `***`, in every table and command example. The real
value appears nowhere in this suite.

| Variable | Status | Used for |
|---|---|---|
| `OPENAI_API_KEY` | required, present (env-only) | embeddings + default chat/expansion |
| `ANTHROPIC_API_KEY` | required, present (env-only) | Dream Cycle `extract_atoms` phase |
| `ZEROENTROPY_API_KEY` | present, reserved (env-only) | not the active embedding provider |
| Database URL | in `~/.gbrain/config.json`, **masked everywhere in this suite** | local Postgres connection (local-dev value) |

API keys live in the environment only, never in `config.json` (verified).
`config.json` does carry the database URL with the local password — stated
here precisely; masked per the standing decision above.

## OpenCode skills (GBrain skillpack — mb-3-cs)

| Item | Value |
|---|---|
| Bundle | tracks CLI (0.46.1.0 when inventoried; the CLI is now 0.59.18.0 — re-inventory before trusting the count); **65 entries inventoried 2026-09-13** — 60 skill directories + 4 underscore metadata files (`_AGENT_README.md`-class); `skillify` absent (regenerated bundle dropped it) |
| Destination | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` (project-local, gitignored) |
| Note | the bundle regenerates with the CLI — entry counts/shapes change per regeneration; exams compare against the last recorded state, not older snapshots |

## Master explainer maintenance rule (settled, 2026-09-06)

[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) is passed to every
memory-component run and must be updated by each such session to reflect
current verified state. At that run's close-out, the update is committed and
pushed to `mybizz-os-docs` as its own commit — standing authorization, not
re-decided per run.

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Upgrade decided by the developer and executed 2026-09-30: `0.46.1.0` → `0.59.18.0` (schema 128 → 169), for source-qualified cross-repository links. Backups first, services stopped in order, waiting jobs cancelled, schema-only migration; proof by a per-source fact comparison, a clean sync and a governed write. Procedure: [[[mybizz-config-docs:gbrain/gbrain-reference\|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) §Upgrading. Standing rule for future upgrades: a developer decision, never version-newness alone. | Resolved 2026-09-30 |
| 2 | MEMORY_VERBS premise reconciled: [[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) records `mcp_surface: verbs` enabled as its Step 0.2 build prerequisite, while current `~/.gbrain/config.json` carries no `mcp_surface` key (re-verified 2026-09-13, masked jq) and the current version's default MCP surface includes the memory verbs (observed 2026-09-06). Both records stated with provenance; the verbs-only surface (`gbrain config set mcp_surface verbs`) remains available as a config choice. **Resolved 2026-09-30:** `gbrain config get mcp_surface` prints `verbs` with `[config] source: db plane` — the setting lives in the database config plane, not in `config.json`. | Resolved 2026-09-30 |
| 3 | Source clone at `/mnt/c/mybizz/gbrain` (v0.25.0) **deleted 2026-09-13** per developer decision — verified not implemented (running code is the bun-global install; zero references in any config/script) and not pristine (local debris only: auto-managed `.gitignore` lines + a stray `pnpm-lock.yaml`; nothing unique — upstream public, re-clonable). | Resolved |
| 4 | Project mb-3-cs managed-block decisions: whether to fold the Access Model bullets into the Graph Memory Guidance block, and whether the block should ever be committed — raised, never decided; do not act without explicit direction. | Open |
| 5 | Governed facts land in the owning project's own documentation source (the worker names it on every write since 2026-10-01). Facts written before that date may still sit in `memory-governor-code`. | Resolved 2026-10-01 |
| 6 | Link rollout: every link in the documentation repositories listed in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md) is stored as `[[[source-id:page-name]]](C:/full/path.md)` (page name = GBrain slug). GBrain follows it across federated sources when links are collected with `gbrain extract links --source db`. Rolled out and verified on this brain 2026-10-01 (`operating-procedures/daily-ops` → 7 links into `mybizz-config-docs`). | Resolved 2026-10-01 |
| 7 | Retention of `~/backups` (the settings archive holds keys), and the parked commit `b6250c43` on `master` / `pre-upgrade-backup`. | Open |
| 8 | Code sources: decided 2026-10-01 — the four code sources and the Anvil clone stay outside the federated search, and Graphify handles code. `memory-governor-code` holds governed facts written before 2026-10-01 and stays. | Closed 2026-10-01 |
