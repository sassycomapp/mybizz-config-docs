---
title: "gbrain-config"
doc-id: "mb-b677b7b4"
updated: "2026-10-23"
---
# GBrain — Configuration

Canonical current-state configuration record for GBrain as a division-wide
system component. Agent-facing. States what exists and what it is set to —
where the reasoning matters, see
[[[mybizz-config-docs:gbrain/gbrain-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-explainer.md) and
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md); for commands and
procedures, see [[[mybizz-config-docs:gbrain/gbrain-reference|Reference]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md).

**System context (developer-stated):** GBrain is one of six closely-related
components — GBrain, gbrain-dream-cycle, gstack, memory-governor, PostgreSQL,
and the installed `mb-submit-memory` skill — that are assessed together, not in
isolation. Cross-component reasoning lives in the Master Explainer
(`mybizz-os-docs`), which owns the how-they-fit-together layer; this suite owns
GBrain-specific state, commands, and incidents.

> **Standing decision — GBrain's writer and ownership model.** Not adopted.
> Adoption is decided together with the next GBrain upgrade, as one planned
> change. No GBrain source is claimed or activated, because claiming stops
> ordinary sync until activation is complete. Command-line page writes and
> deletes (`put_page`, `gbrain capture`) are therefore refused with
> `owner_unavailable`; session pages are written as files and imported by
> commit all. Database fact writes (`remember`, `forget`) work.

---

## Identity

| Item | Value |
|---|---|
| Issuer | Garry Tan — `github.com/garrytan/gbrain` (MIT) |
| Installed version | `0.59.18.0` (tag `v0.59.18.0`, commit `045a6138`) |
| Standard taken from | `0.59.18.0` |
| Last researched | 2026-10-20 |
| Upstream | `github.com/garrytan/gbrain` — MIT; by Garry Tan. **Not distributed on npm** — the npm `gbrain` package is unrelated and shadows the binary (upstream warning; see the Reference Do-not list) |
| Engine | PostgreSQL, self-hosted, WSL-native — the server version, extensions and this database's place in the estate are owned by [[[mybizz-config-docs:postgresql/postgresql-config\|PostgreSQL Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) |
| Connection | `postgresql://postgres:***@localhost:5432/gbrain` |
| Boot behavior | Auto-starts on WSL boot (`service postgresql start` in `/etc/wsl.conf`) |
| Executable | `/home/dev-p/.bun/bin/gbrain` → `~/.bun/install/global/node_modules/gbrain/src/cli.ts`; that global entry is a symlink to the checkout `/home/dev-p/gbrain` (bun link) |
| Install | **Live install:** `/home/dev-p/gbrain` — a Git checkout of `github.com/garrytan/gbrain`, in detached HEAD at tag `v0.59.18.0` (authoritative for diagnosis; linked, see Executable). Branch `master` sits at upstream `v0.46.1.0` plus one local commit `b6250c43` (a one-line diagnostic change in `src/core/cycle/extract-atoms.ts`, not on GitHub); the same commit is on branch `pre-upgrade-backup` |
| Database schema | 169 — no dangling aliases |
| Config file | `~/.gbrain/config.json` |
| MCP surface | `mcp_surface` = `verbs` in the **database** config plane (`gbrain config get mcp_surface` → `verbs`, `[config] source: db plane`); `~/.gbrain/config.json` carries no such key |
| Brain default source | `sources.default` = `default`. The memory governor's worker retargets the default to the owning project before every governed write; the standing sync script resets it to `default` before every run. A default that names a source that does not exist stops `gbrain sync` — fix: `gbrain sources default default` |
| Self-upgrade mode | `notify`, set explicitly in `config.json` (`{mode: "notify", mode_prompted: true}`) |
| Legacy artifact | None — `~/.gbrain/brain.pglite` is absent; the live engine is PostgreSQL |

## Backups

The **estate-wide backup convention** (all databases, both instances, both
locations, weekly cycle) is authoritative in
[[[mybizz-config-docs:postgresql/postgresql-config|PostgreSQL Configuration]]](C:/mybizz/mybizz-config-docs/postgresql/postgresql-config.md) §Backups — this database estate is one
system. GBrain's share of it: the `gbrain` database and the `memory_governor`
database are both covered in every cycle, delivered to
`/home/dev-p/backup-gbrain/` (default) and `/mnt/c/backup-gbrain/` (security
net); each pair is hash-verified after the run.

**Upgrade backups**, in `~/backups/` (private — the settings archive contains
keys): `db-gbrain-before-upgrade.dump`, `db-memory_governor-before-upgrade.dump`,
`dot-gbrain-before-upgrade.tgz` (the whole `~/.gbrain` folder),
`rollback-commit.txt` (the recorded checkout commit), the doctor reports
`doctor-before.txt` and `doctor-after*.txt`, the per-source fact snapshots
`recall-before-*.json` and `recall-after-*.json`, `sources-before.json` /
`sources-after.json`, and `cutover-block1.sh`. The rollback script restores the
dumps together with the old code.

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
is the correct tool — full account in the
[[[mybizz-config-docs:gbrain/gbrain-reference|Reference]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md) and
[[[mybizz-config-docs:gbrain/gbrain-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-explainer.md).

## Models

| Purpose | Model |
|---|---|
| Embedding | `openai:text-embedding-3-large` (1536 dims) |
| Chat / expansion | `openai:gpt-5.2` |

Also set in `config.json`: `engine: postgres`, `schema_pack:
gbrain-everything`, `mcp.publish_skills: true`.

### Providers

| Role          | Provider                        | Status                           |
| ------------- | ------------------------------- | -------------------------------- |
| Embedding     | OpenAI (text-embedding-3-large) | ✓ active                         |
| Chat / Expand | OpenAI (gpt-5.2)                | ✓ active, will move to Anthropic |
| Reranker      | Voyage (`voyage:rerank-2.5`)    | ✓ active                         |

## Search settings

| Setting | Value |
|---|---|
| `search.reranker.enabled` | `true` |
| `search.reranker.model` | `voyage:rerank-2.5` |
| `search.reranker.timeout_ms` | `20000` |
| `GBRAIN_QUERY_EMBED_TIMEOUT_MS` | `15000`, set in `~/.bashrc` and in the `gbrain` MCP environment in `~/.config/opencode/opencode.jsonc` |
| Voyage account | Payment method on the organization that holds the API key (standard limits for `rerank-2.5`: 2000 requests and 2M tokens per minute) |
| `/etc/gai.conf` | `precedence ::ffff:0:0/96  100` (IPv4 addresses are tried first) |
| `systemd-timesyncd` in WSL | Disabled; Windows keeps the WSL clock |

## Job expiry

| Setting | Value |
|---|---|
| `minions.ttl_waiting_hours.facts-absorb` | `24` (db plane) |
| `minions.ttl_waiting_hours.extract` | `24` (db plane) |
| GBrain worker | None runs. Waiting jobs from syncs simply expire after their TTL |

## Database statistics (point-in-time; grows with every sync)

- 2,244 pages / 6,384 chunks / 6,384 embedded (100%) / 2,695 links / 13 tags
- By type: concept 1,404, atom 564, note 182, code 45, extract_receipt 32, email 5, session 4, media 4, session-summary 2, session-log 1, learning 1
- Current values: `gbrain stats`

## Registered sources (18)

| Source ID | Path | Pages | Federation |
|---|---|---|---|
| `default` | `/mnt/c/dev/project-library-global` | 1,080 | **federated** |
| `anvil-agent-references-code` | `/mnt/c/mybizz/anvil-agent-references` | 34 | isolated (explicit) |
| `data-mybizz-mgt` | `/mnt/c/data-mybizz-mgt` | 12 | **federated** |
| `dev-root-hub` | `/mnt/c/dev/dev-root` | 12 | **federated** |
| `mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` | 564 | **federated** |
| `mb-4-ecom-project-library` | `/mnt/c/dev/dev-mb-4-ecom/mb-4-ecom-project-library` | 5 | **federated** |
| `mb-archify-scope` | `/mnt/c/mybizz/mb-archify-scope` | 1 | **federated** |
| `mb-close-out` | `/mnt/c/mybizz/mb-close-out` | 1 | **federated** |
| `mb-compile-rules` | `/mnt/c/mybizz/mb-compile-rules` | 1 | **federated** |
| `mb-memory-system-diagnostic` | `/mnt/c/mybizz/mb-memory-system-diagnostic` | 1 | **federated** |
| `mb-project-docs` | `/mnt/c/mybizz/mb-project-docs` | 1 | **federated** |
| `mb-sentinel-review` | `/mnt/c/mybizz/mb-sentinel-review` | 1 | **federated** |
| `mb-submit-memory` | `/mnt/c/mybizz/mb-submit-memory` | 1 | **federated** |
| `mb-sysdoc-creator` | `/mnt/c/mybizz/mb-sysdoc-creator` | 1 | **federated** |
| `memory-governor-code` | `/home/dev-p/memory-governor` | 46 | unset |
| `mybizz-config-docs` | `/mnt/c/mybizz/mybizz-config-docs` | 139 | **federated** |
| `mybizz-os-docs` | `/mnt/c/mybizz/mybizz-os-docs` | 26 | **federated** |
| `pdlf` | `/mnt/c/pdlf` | 309 | **federated** |

Counts are per-source as listed on the Last researched date (point-in-time;
re-list with `gbrain sources list` for current values). One source exists per
mb-* skill folder under `/mnt/c/mybizz/`.

**Federation states:** `federated` — appears in every other source's default
search and may write links into other sources; `unset` (never set) — stays out
of other sources' searches, but a session working inside it can still read the
federated sources; `isolated` (explicit `gbrain sources unfederate`) — cut off
in both directions. The Anvil clone is isolated and `memory-governor-code` is
unset — deliberately out of the federated search: Graphify handles code, and
every other source is federated. Application code is not indexed in GBrain at
all — agents read app code directly from the app folders
([[[mybizz-os-docs:os-reference-docs/repo-organization|repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md)).

**Source names:** the Anvil project names are `mb-3-cs` and `mb-4-ecom`;
`-code` occurs only in source ids.
`anvil-agent-references-code` is a read-only clone of Anvil's own public
repository `anvil-works/anvil-agent-references`; the developer has no GitHub
repository of his own for it. Its `-code` ending distinguishes it from the
developer's own `anvil-agent-references/` documentation folder in
`mybizz-config-docs`. It is separate from `anvil-docs` in the source
`default`, the developer's own compilation.

**Why a source is named `default`:** GBrain's own hardcoded fallback source ID
(upstream `docs/architecture/brains-and-sources.md`; resolution chain ends in
`fallback: 'default'`) — the first source this brain created. Not a
user-chosen name; do not rename.

## Content paths into GBrain

| Path | Mechanism | GBrain layer written | Carries | Real usage |
|---|---|---|---|---|
| **Sync path** | Standing script (`sync-gbrain.sh`: resets the brain default source, enumerates every registered source, runs `gbrain sync --source <id> --no-pull` for each, then `extract links --source db` and `embed --stale`; run with `bash /mnt/c/mybizz/scripts/sync-gbrain.sh`); [[[mybizz-os-docs:operating-procedures/daily-ops\|daily-ops]]](C:/mybizz/mybizz-os-docs/operating-procedures/daily-ops.md) documents per-repo sync as the standing after-work workflow | **Pages/corpus** | Whole repos: the Anvil clone (a permanent governor bypass), the developer doc repos, the project library sources, the mb-* skill folders | Runs with every commit all, over every registered source; the dominant path by volume |
| **Governed path** | Developer or PDLF step → `mb-submit-memory` → governor API → promote → async `gbrain_write` → `remember` (MEMORY_VERBS) | **Facts layer** (hot memory) | Individual judgment-bearing content meant to be checked before becoming durable | Governed facts land in the owning project's own documentation source — the worker names it on every write |

**The boundary (by design, from
[[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md)):** sync must
never carry governed content — it would ingest raw content regardless of
governor approval; `remember` never creates corpus pages. Neither path
supersedes the other — they write to different layers and cannot substitute
for each other. [[[mybizz-os-docs:operating-procedures/daily-ops|daily-ops]]](C:/mybizz/mybizz-os-docs/operating-procedures/daily-ops.md) (located at
`C:\mybizz\mybizz-os-docs\operating-procedures\daily-ops.md`) documents the
sync path as the standing after-work workflow.

**GStack integration flow** (`/setup-gbrain`, 3-stage `/sync-gbrain`):
installed skills per upstream `USING_GBRAIN_WITH_GSTACK.md` — not this
environment's operational path; the custom script is.

## Scheduled jobs

| Item | Verified state |
|---|---|
| Autopilot | Off by decision — no GBrain schedule exists in crontab or anywhere else |
| Dream cycle cadence | Runs by hand weekly, after the Sunday backup, through the memory diagnostic (`mb-memory-system-diagnostic`); see [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config\|Dream Cycle Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md) |
| Sync | Manual: `bash /mnt/c/mybizz/scripts/sync-gbrain.sh`, or as part of `commit-all.sh` (about two minutes, longer after many changes; log in `C:\mybizz\logs\gbrain-logs\sync-<timestamp>.log`) |
| GBrain job queue | No GBrain worker runs. The `facts-absorb` and `extract` jobs created by syncs wait and expire — see Job expiry above |

## OpenCode MCP integration

| Item | Value |
|---|---|
| Scope | global `~/.config/opencode/opencode.jsonc`, entry `mcp.gbrain` |
| Type / command | `local`; `["/home/dev-p/.bun/bin/gbrain", "serve"]` |
| Enabled | `true` |
| Environment passed | `OPENAI_API_KEY`, `VOYAGE_API_KEY`, `GBRAIN_QUERY_EMBED_TIMEOUT_MS` |
| MCP bootstrap | servers start once at OpenCode process boot, never per chat session — config changes need a full process restart |
| Server version | `gbrain serve` runs the installed version — it restarts with OpenCode |

## Credentials

**Masking decision (standing):** the database URL appears in this suite only
as `postgresql://postgres:***@localhost:5432/gbrain` — structure visible,
password always `***`, in every table and command example. The real value
appears nowhere in this suite.

| Variable | Status | Used for |
|---|---|---|
| `OPENAI_API_KEY` | required, present (env-only) | embeddings + default chat/expansion |
| `ANTHROPIC_API_KEY` | required, present (env-only) | Dream Cycle `extract_atoms` phase |
| `VOYAGE_API_KEY` | required, present (env-only, `~/.bashrc`) | reranker (`voyage:rerank-2.5`) |
| Database URL | in `~/.gbrain/config.json`, **masked everywhere in this suite** | local Postgres connection (local-dev value) |

API keys live in the environment only, never in `config.json`.
`config.json` does carry the database URL with the local password — stated
here precisely; masked per the standing decision above.

## OpenCode skills

| Item | Value |
|---|---|
| GBrain agent skills | Not installed. No project's `.opencode/skills` folder holds GBrain skills, and no global skill folder does. The installed-skill inventory is the [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) |

## Master explainer maintenance rule

[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) is passed to every
memory-component run and must be updated by each such session to reflect
current verified state. At that run's close-out, the update is committed and
pushed to `mybizz-os-docs` as its own commit — standing authorization, not
re-decided per run.

## Open items

None.
