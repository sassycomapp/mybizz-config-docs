# GBrain Configuration — mb-3-cs

Canonical current-state configuration record. Agent-facing. Reflects the
working state of GBrain as integrated into the `mb-3-cs` project as of the
end of the setup/closeout sequence (2026-08-16). This document states facts,
not history — where a decision was made and the reasoning matters, see
`memory-explainer.md`.

---

## Identity

| Item | Value |
|---|---|
| Version | `0.46.1.0` |
| Schema version | `128` (latest, migrations current) |
| Engine | PostgreSQL (self-hosted, WSL-native) |
| Connection | `postgresql://postgres:***@localhost:5432/gbrain` |
| Boot behavior | Auto-starts on every WSL boot — `[boot]` section in `/etc/wsl.conf` runs `service postgresql start` |
| PostgreSQL server | 16.14 |
| pgvector | `0.6.0` |
| Executable | `/home/dev-p/.bun/bin/gbrain` (bun-link → `/home/dev-p/gbrain/src/cli.ts`) |
| Config file | `~/.gbrain/config.json` |
| Self-upgrade mode | `notify` (does not auto-apply) |
| Legacy artifact | `/home/dev-p/.gbrain/brain.pglite` — stale, unused; live engine is Postgres |

## Schema pack

| Item | Value |
|---|---|
| Active pack | `gbrain-everything@1.0.0` (sha8 `7021205a`) |
| Page types | 30 |
| Link types | 12 |
| Installed packs on disk | `gbrain-everything` only |
| Bundled but not installed | `gbrain-base`, `gbrain-recommended`, `gbrain-creator`, `gbrain-investor`, `gbrain-engineer`, `gbrain-base-v2` |

**Known limitation:** no bundled or installed pack extracts code-symbol
call-graph edges. The `code` page type is `extractable: false` in every
bundled pack, including `gbrain-engineer`. `code-callers`/`code-callees`
return symbol names but cannot resolve them to defining chunks
(`resolved: false`, `to_chunk_id: null`). This is not fixable by switching
packs within the bundled set. Graphify's `get_neighbors` is the correct tool
for resolved cross-file call/import/containment relationships — see
`graphify-config.md` and `graphify-reference.md`.

## Models

| Purpose | Model |
|---|---|
| Embedding | `openai:text-embedding-3-large` (1536 dims) |
| Chat / expansion | `openai:gpt-5.2` |

## Database statistics (last verified)

- 1142 pages / 2524 chunks / 2524 embedded / 469 links / 5 tags
- Pages by type: concept 554, code 254, atom 229, note 87, extract_receipt 18
- Embeddings 100%; RLS enabled on all 62/62 tables
- `brain_score` 57/100 — content-quality signal, not operational; not a target for remediation

## Registered sources

**Active (kept synced/cycled):**

| Source ID | Path | Pages | Federated |
|---|---|---|---|
| `default` | `/mnt/c/dev/project-library-global` | 200 | **yes** — only federated source |
| `mb-3-cs-code` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` | 263 | no |
| `mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` | 435 | no |
| `dev-makepdlf` | `/mnt/c/dev/dev-makepdlf/makepdlf-project-library` | 181 | no |
| `dev-root-hub` | `/mnt/c/dev/dev-root` | 20 | no |

**Deferred (registered, data intact, intentionally left stale — not a fault
condition, do not refresh without explicit instruction):**

| Source ID | Path | Pages |
|---|---|---|
| `mb4ecom-code` | `/mnt/c/dev/dev-mb4ecom/mb4ecom` | 5 |
| `mb4ecom-project-library` | `/mnt/c/dev/dev-mb4ecom/mb4ecom-project-library` | 6 |
| `mb5pdlf-code` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf` | 5 |
| `mb5pdlf-project-library` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf-project-library` | 13 |
| `pdlf` | `/mnt/c/pdlf` | 14 |

Policy: inactive-project sources stay registered rather than removed. The
only source ever removed was `template-project-library` (a content-free
scaffold). Deferred sources' `sync_freshness`/`cycle_freshness` doctor checks
are expected to fail and are excluded from health scope.

**Why the source is named `default`:** this is not an arbitrary or
user-chosen name — it is GBrain's own hardcoded fallback source ID.
Confirmed in the upstream repo's `docs/architecture/brains-and-sources.md`:
the documented source-resolution precedence chain ends in
`6. fallback: 'default'`, and the doc's reference topology for a
single-person developer setup shows exactly one source, named `default`,
`federated: true` — the same shape as this registration. Directly queried
from the live `sources` table: `id='default'`, `created_at = 2026-08-01
11:12:32+02`, `config = {"federated": true, ...}` — the earliest
`created_at` of any registered source (next-earliest is 2026-08-10),
consistent with it being the first source GBrain created/accepted when
this brain was first initialized, before any project-specific source
existed to need a distinguishing name. See `gbrain-reference.md` §
"Source Management" for the full resolution-precedence mechanics.

`mb-3-cs-code`'s sync strategy is `code` (confirmed real Python content
indexed — 254 code files). Note: `strategy` is applied as a **sync-time CLI
flag** (`gbrain sync --strategy code`), not a field persisted in and read
back from the source's stored config — see `gbrain-reference.md` for the
mechanics.

## OpenCode MCP integration

| Item | Value |
|---|---|
| Scope | global `~/.config/opencode/opencode.jsonc` |
| Entry | `mcp.gbrain` |
| Type | `local` |
| Command | `["/home/dev-p/.bun/bin/gbrain", "serve"]` |
| Enabled | `true` |
| Environment passed | `OPENAI_API_KEY`, `ZEROENTROPY_API_KEY` |

## Credentials required

| Variable | Status | Used for |
|---|---|---|
| `OPENAI_API_KEY` | required, present | embeddings + default chat/expansion |
| `ANTHROPIC_API_KEY` | required, present | Dream Cycle `extract_atoms` phase — see `gbrain-dream-cycle-config.md` |
| `ZEROENTROPY_API_KEY` | present, not currently the active embedding provider | reserved |

Not present, not required by current config: `VOYAGE_API_KEY`,
`GEMINI_API_KEY`/`GOOGLE_API_KEY`, `KIMI_API_KEY`, `DEEPSEEK_API_KEY`,
`PERPLEXITY_API_KEY`.

**All credentials live in the environment (`~/.bashrc`) only — never in
`~/.gbrain/config.json`.** Confirmed and verified directly against the
live system: `config.json` carries no `openai_api_key`,
`zeroentropy_api_key`, or `anthropic_api_key` fields, and each key is
genuinely present in the actual spawned `gbrain` process's own
environment (`/proc/<PID>/environ`), not just the shell.

## OpenCode skills (GBrain skillpack)

| Item | Value |
|---|---|
| Bundle version | tracks CLI (`0.46.1.0`), 61 skills total |
| Scaffolded | 60 of 61 — `skillify` deliberately excluded (name collision with a pre-existing GStack skill) |
| Destination | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` (project-local, gitignored) |
| Total files | 119 — 60 `SKILL.md` + 38 `routing-eval.jsonl` + 20 shared deps (16 `conventions/*` + 4 root `_` files) + 1 extra skill file (`bulk-ingestion/MANIFEST-PATTERN.md`) |
| `RESOLVER.md` | not scaffolded (never is, by design — irrelevant to OpenCode, which routes skills by name/description, not a resolver) |
| Confirmed post-restart | exactly 60 GBrain skills + exactly one `skillify` (the original GStack skill, unmodified) |

Scaffold command used (per-skill, not `--all`, to exclude `skillify`):
```bash
gbrain skillpack scaffold <name> --workspace /mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode --trust --json
```
(run once for each of the 60 approved skill names)

## agents.md / AGENTS.md

- Physical file: `agents.md` at the project root (case-insensitive filesystem
  makes this identical to `AGENTS.md`). Gitignored, local-only, never
  committed.
- Contains: an "Access Model" section (pre-existing) plus a managed
  `<!-- BEGIN GRAPH MEMORY GUIDANCE -->` … `<!-- END GRAPH MEMORY GUIDANCE -->`
  block. Full block text and authority model: see `memory-explainer.md`.
- The **global** `~/.config/opencode/AGENTS.md` is a separate file with its
  own `## GBrain Search Guidance` managed block (different markers) — not to
  be confused with the project file.
- **Open, unresolved as of last review:** whether to fold the Access Model
  bullets into the Graph Memory Guidance block, and whether the block/config
  should ever be committed vs. staying local-only. No instruction has been
  given either way — do not act on either without explicit direction.

## Health baseline (last known-good)

- `sync_freshness`: pass for all 5 active sources; `sync-failures.jsonl` empty.
- `cycle_freshness`: pass for all 5 active sources; fails (by design, excluded from scope) for all 5 deferred sources.
- `schema_version`, `connection`, `pgvector`: green.
- Known non-blocking, out-of-scope signals: `brain_score` 57/100; one queued `embed-backfill` job (targets deferred source `mb4ecom-code`); one queued `facts-absorb` job (targets deferred source `pdlf`); `graph_signals_coverage` 9.6%; `contextual_retrieval_coverage` 670 pages.

## Do not

- Do not switch or install a different schema pack expecting it to fix the call-graph limitation — investigated and confirmed not possible with any bundled pack.
- Do not run `gbrain sync --skip-failed` as a default remedy for a parse failure — fix the offending file's YAML frontmatter (usually: quote a `document:` value containing `: ` or a backtick) and re-sync cleanly instead.
- Do not refresh the 5 deferred sources without explicit instruction.
- Do not edit `agents.md`'s Access Model / Graph Memory Guidance sections without explicit instruction — the fold/commit decisions are open.
- Do not enable `MEMORY_VERBS` (`mcp_surface: verbs`) — never evaluated or enabled in this project; the full tool surface is what's in active use.
- **Open item:** `0.46.1.0` is in use while `0.46.6.0` was already available as of the close of the last upgrade sequence, under a standing "upgrade only on check failure" policy that was never explicitly re-affirmed as ongoing. Do not upgrade on the strength of a newer version alone — confirm the policy first.
