---
document: "GBrain — Configuration"
doc-id: gbrain-config
state: Live
date-created: 2026-09-05
---

# GBrain — Configuration

Canonical current-state configuration record for GBrain as a division-wide
system component. Agent-facing. Reflects the live-verified state as of
2026-09-13. States facts, not history — where the reasoning matters, see
[[gbrain-explainer|Explainer]] and [[memory-master-explainer|Master Explainer]]; for commands and
procedures, see [[gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]].

**System context (developer-stated, 2026-09-06; architecture context unchanged):** GBrain is one of six
closely-related components — GBrain, gbrain-dream-cycle, gstack,
memory-governor, PostgreSQL, and the installed `mb-submit-memory` skill — that
are assessed together, not in isolation. Cross-component reasoning lives in
[[memory-master-explainer|Master Explainer]] (`mybizz-os-docs`), which owns the how-they-fit-
together layer; this suite owns GBrain-specific state, commands, and incidents.

---

## Identity

| Item | Value |
|---|---|
| Version | `0.46.1.0` — CLI and live install agree (`/home/dev-p/gbrain/VERSION`, re-verified 2026-09-13) |
| Version drift | **`0.50.0.0` available** (update banner, verified 2026-09-13). Standing policy: upgrade only on check failure — never on version-newness (open item) |
| Upstream | `github.com/garrytan/gbrain` — MIT; by Garry Tan; 29.6k stars / 1,061 commits (verified 2026-09-06). **Not distributed on npm** — the npm `gbrain` package is unrelated and shadows the binary (upstream warning; see [[gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]] Do-not) |
| Engine | PostgreSQL 16.14, self-hosted, WSL-native; pgvector 0.6.0 |
| Connection | `postgresql://postgres:***@localhost:5432/gbrain` |
| Boot behavior | Auto-starts on WSL boot (`service postgresql start` in `/etc/wsl.conf`) |
| Executable | `/home/dev-p/.bun/bin/gbrain` (bun-link → `/home/dev-p/gbrain/src/cli.ts`) |
| Install | **Live install:** `/home/dev-p/gbrain` (0.46.1.0 — authoritative for diagnosis; bun-global install, `~/.bun/bin/gbrain` → `src/cli.ts`). **The `/mnt/c/mybizz/gbrain` source clone (v0.25.0) was deleted 2026-09-13** per developer decision — not the running code, referenced nowhere; upstream public, re-clonable |
| Config file | `~/.gbrain/config.json` |
| Self-upgrade mode | **key absent from `config.json`** (developer-verified 2026-09-13, masked jq) — the documented `notify` behavior is the upstream default, not a verified key |
| Legacy artifact | `~/.gbrain/brain.pglite` — **removed** (confirmed absent 2026-09-12; live engine is Postgres; artifact no longer exists) |

## Backups

The **estate-wide backup convention** (all databases, both instances, both
locations, weekly exam-enforced cycle) is authoritative in
[[postgresql-config|Configuration]] §Backups — this database estate is one system. GBrain
facts within it: the `gbrain` database (51 MB dump, 62 tables verified) and the
`memory_governor` database (26 KB dump, 5 tables) are both covered in every
cycle, delivered to `/home/dev-p/backup-gbrain/` (default) and
`/mnt/c/backup-gbrain/` (security net); pairs hash-verified (current cycle
2026-09-13: `6a6d60d57df162a4` / `e20b5694af64cdb7`).

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
is the correct tool — full account in [[gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]] and
[[gbrain-explainer|Explainer]].

## Models

| Purpose | Model |
|---|---|
| Embedding | `openai:text-embedding-3-large` (1536 dims) |
| Chat / expansion | `openai:gpt-5.2` |

## Live database statistics (verified 2026-09-13 — point-in-time; grows with every sync)

- 1,880 pages / 5,581 chunks / 5,581 embedded (100%) / 692 links / 9 tags
- By type: concept 972, code 307, note 194, atom 164, extract_receipt 20, email 5, media 4

## Registered sources (14 — verified 2026-09-13)

| Source ID | Path | Pages | Federated |
|---|---|---|---|
| `default` | `/mnt/c/dev/project-library-global` | 694 | **yes** |
| `dev-root-hub` | `/mnt/c/dev/dev-root` | 12 | **yes** |
| `mybizz-config-docs` | `/mnt/c/mybizz/mybizz-config-docs` | 172 | **yes** |
| `mybizz-os-docs` | `/mnt/c/mybizz/mybizz-os-docs` | 7 | **yes** |
| `pdlf` | `/mnt/c/pdlf` | 59 | **yes** |
| `anvil-agent-references-code` | `/mnt/c/mybizz/anvil-agent-references` | 34 | no |
| `makepdlf-project-library` | `/mnt/c/dev/dev-makepdlf/makepdlf-project-library` | 128 | no |
| `mb-3-cs-code` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` | 263 | no |
| `mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` | 437 | no |
| `mb4ecom-code` | `/mnt/c/dev/dev-mb4ecom/mb4ecom` | 5 | no |
| `mb4ecom-project-library` | `/mnt/c/dev/dev-mb4ecom/mb4ecom-project-library` | 5 | no |
| `mb5pdlf-code` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf` | 5 | no |
| `mb5pdlf-project-library` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf-project-library` | 12 | no |
| `memory-governor-code` | `/home/dev-p/memory-governor` | 47 | no |

Counts are per-source as-of each source's last sync (point-in-time — they lag
the live identity total mid-cycle; reconcile via per-source DB query). Sum
reconciles exactly to the identity total (1,880) as of 2026-09-13.

All sources synced 2026-09-05 → 2026-09-13. **The `pdlf` source was registered 2026-09-11** ("PDLF System", federated, 59 pages) — the 14th source, consistent with the pdlf project going live (see `projects-config-register.md`). The prior suite's
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
| **Sync path** | Standing script (`sync-gbrain.sh`: `gbrain sync` + `embed --stale`) + per-source `gbrain sync --source <id>`; daily-ops.md documents per-repo sync as the standing after-work workflow | **Pages/corpus** | Whole repos: vendor bypass sources (anvil-agent-references, magdoub-wireframe — permanent governor bypasses), developer doc repos, project code+library sources | 18+ logged runs (2026-07-28 → 2026-09-13); all 14 sources; the dominant path by volume |
| **Governed path** | Developer or PDLF step → `mb-submit-memory` → governor API → promote → async `gbrain_write` → `remember` (MEMORY_VERBS) | **Facts layer** (hot memory) | Individual judgment-bearing content meant to be checked before becoming durable | Exactly one real run (2026-08-27, promoted; its `gbrain_write` initially queued pending the dev-makepdlf source rename, since resolved); `pdlf_step_sync` writer parked pending PDLF go-live |

**The boundary (by design, from [[memory-governor-config|Memory Governor Configuration]]):** sync must
never carry governed content — it would ingest raw content regardless of
governor approval; `remember` never creates corpus pages. Neither path
supersedes the other — they write to different layers and cannot substitute
for each other. The script syncs **only the repo source** — a newly
registered source needs its own `gbrain sync --source <id>` (proven today).
`daily-ops.md` (located at
`C:\mybizz\mybizz-os-docs\operating-procedures\daily-ops.md`) documents the
sync path as the standing after-work workflow and predates the governed
path — its repo table was reconciled against the current source list
2026-09-18 (align-docs).

**GStack integration flow** (`/setup-gbrain`, 3-stage `/sync-gbrain`):
installed skills per upstream `USING_GBRAIN_WITH_GSTACK.md` — not this
environment's operational path; the custom script is (verified against
`logs/gbrain-logs/`).

## Scheduled jobs

| Item | Verified state |
|---|---|
| Crontab | A `gbrain autopilot` entry (every 5 minutes, targeting `--repo '/mnt/c/projects'`) was found **doubly inert** — cron daemon not running, target path from the pre-`C:\dev` layout no longer existing, log file never created — and was **deliberately removed 2026-09-06** |
| Design consequence | The Dream Cycle runs on-demand only; nothing GBrain-related is scheduled (see [[gbrain-dream-cycle-config|Configuration]]) |

## OpenCode MCP integration

| Item | Value |
|---|---|
| Scope | global `~/.config/opencode/opencode.jsonc`, entry `mcp.gbrain` |
| Type / command | `local`; `["/home/dev-p/.bun/bin/gbrain", "serve"]` |
| Enabled | `true` |
| Environment passed | `OPENAI_API_KEY`, `ZEROENTROPY_API_KEY` |
| MCP bootstrap | servers start once at OpenCode process boot, never per chat session — config changes need a full process restart |

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
| Bundle | tracks CLI (0.46.1.0); **65 entries inventoried 2026-09-13** — 60 skill directories + 4 underscore metadata files (`_AGENT_README.md`-class); `skillify` absent (regenerated bundle dropped it) |
| Destination | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` (project-local, gitignored) |
| Note | the bundle regenerates with the CLI — entry counts/shapes change per regeneration; exams compare against the last recorded state, not older snapshots |

## Master explainer maintenance rule (settled, 2026-09-06)

[[memory-master-explainer|Master Explainer]] is passed to every
memory-component run and must be updated by each such session to reflect
current verified state. At that run's close-out, the update is committed and
pushed to `mybizz-os-docs` as its own commit — standing authorization, not
re-decided per run.

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Upgrade policy: `0.46.1.0` in use while `0.50.0.0` is available (banner + releases verified 2026-09-13). Upgrade is **non-trivial**: coordinated queue cutover (pause → drain → stop → backup → install → review legacy jobs), old/new workers must not coexist, schema migrations apply. Prerequisites check: Bun 1.3.14 ≥ 1.3.11 minimum ✓; fresh DB backup now exists (2026-09-13, both locations — see Backups section). Policy: upgrade only on check failure or by developer decision. | Open |
| 2 | MEMORY_VERBS premise reconciled: [[memory-governor-config|Memory Governor Configuration]] records `mcp_surface: verbs` enabled as its Step 0.2 build prerequisite, while current `~/.gbrain/config.json` carries no `mcp_surface` key (re-verified 2026-09-13, masked jq) and the current version's default MCP surface includes the memory verbs (observed 2026-09-06). Both records stated with provenance; the verbs-only surface (`gbrain config set mcp_surface verbs`) remains available as a config choice. | Open |
| 3 | Source clone at `/mnt/c/mybizz/gbrain` (v0.25.0) **deleted 2026-09-13** per developer decision — verified not implemented (running code is the bun-global install; zero references in any config/script) and not pristine (local debris only: auto-managed `.gitignore` lines + a stray `pnpm-lock.yaml`; nothing unique — upstream public, re-clonable). | Resolved |
| 4 | Project [[agents|mb-3-cs]] managed-block decisions: whether to fold the Access Model bullets into the Graph Memory Guidance block, and whether the block should ever be committed — raised, never decided; do not act without explicit direction. | Open |
