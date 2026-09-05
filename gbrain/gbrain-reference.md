# GBrain Reference

## What is GBrain

GBrain is the advisory memory layer. It stores and searches project
documents (ADRs, specs, docs) and code (Python, YAML) as searchable vector
memories. GBrain does not override current repo files, ADRs, or OpenCode
rules — files are always authoritative.

**Engine:** PostgreSQL 16 + pgvector (self-hosted, WSL-native) | **Version:**
`0.46.1.0` | **Schema:** v128 | **Schema pack:** gbrain-everything (code-aware)

**Connection:** `postgresql://postgres:***@localhost:5432/gbrain`

For the exact current registered sources, MCP entry, credentials, and
scaffolded skills for the `mb-3-cs` project specifically, see
`gbrain-config.md`. This document covers general GBrain mechanics and
command behavior, applicable across projects.

---

## Command Reference

### Health & Status

| Command | Description |
|---|---|
| `gbrain doctor` | Full health check (score out of 100) |
| `gbrain doctor --fast` | Quick health check (skips DB probes) |
| `gbrain doctor --json --fast` | Machine-readable health output |
| `gbrain stats` | Page count, chunk count, embed coverage, source breakdown |
| `gbrain --version` | Show installed version |
| `gbrain sources list` | List all registered sources with paths and page counts |
| `gbrain sources list --json` | Machine-readable source list |

### Search & Query

| Command | Description |
|---|---|
| `gbrain search "<terms>"` | Keyword search (full-text) |
| `gbrain query "<question>"` | Hybrid search (vector + keyword + expansion) |
| `gbrain query "<q>" --source <id>` | Search scoped to one source |
| `gbrain query "<q>" --limit 10` | Limit results |
| `gbrain query "<q>" --lang typescript` | Filter by language |
| `gbrain query "<q>" --near-symbol <name>` | Anchor retrieval at a code symbol |
| `gbrain query "<q>" --adaptive-return` | Return tight result set for lookup questions |

### Code Analysis

| Command | Description |
|---|---|
| `gbrain code-def <symbol>` | Find where a symbol is defined |
| `gbrain code-refs <symbol>` | Find all references to a symbol |
| `gbrain code-callers <symbol>` | Find what calls a function |
| `gbrain code-callees <symbol>` | Find what a function calls |
| `gbrain code-blast <symbol>` | Full transitive caller tree (up to depth) |

**Confirmed limitation, verified two independent ways:** `code-callers`/
`code-callees` only resolve **same-file** symbol references by design
(confirmed via direct source read of `resolve-symbol-edges.ts` —
"within-file two-pass symbol resolution"); cross-file calls always show
`[unresolved]`. Separately: **no bundled or installed schema pack extracts
code-symbol call-graph edges at all** — the `code` page type is declared
`extractable: false` in every bundled pack (`gbrain-base`, `-recommended`,
`-creator`, `-investor`, `-engineer`, `-everything`, `-base-v2`), so
`code-callers`/`code-callees` return symbol names with `resolved: false` and
`to_chunk_id: null` universally, not just cross-file. Switching schema packs
does not fix this — it was investigated and confirmed a dead end. `code-def`/
`code-refs` are unaffected by either limitation. For anything requiring
resolved call/import/containment relationships, use Graphify's
`get_neighbors` instead (see `graphify-reference.md`) — it correctly returns
fully resolved, typed, cross-file edges.

### Sync & Import

| Command | Description |
|---|---|
| `gbrain sync --repo <path>` | Sync a repo's markdown files into gbrain |
| `gbrain sync --repo <path> --strategy code` | Sync code files (.py, .ts, .js, .yaml) |
| `gbrain sync --source <id>` | Sync one registered source |
| `gbrain sync --source <id> --strategy code` | Sync one source, forcing the code strategy |
| `gbrain sync --source <id> --no-pull` | Sync without an internal `git pull` — no working-tree interaction at all |
| `gbrain sync --source <id> --dry-run` | Preview what would sync, no writes |
| `gbrain sync --all` | Sync all registered sources |
| `gbrain sync --all --parallel 4 --workers 4 --skip-failed` | Recommended standing pattern for syncing every source at once |
| `gbrain sync --break-lock` | Break a stale sync lock |
| `gbrain embed --stale` | Embed chunks that are missing embeddings |
| `gbrain extract --stale` | Extract links and timelines from stale pages |

**`--strategy` is a sync-time CLI flag, not a stored per-source config
field.** Verified directly against `sources list`, `sources status`, and
`sources --help`: no current version exposes or persists a `strategy` field
on a source. Whatever a project's documentation may say about a source being
"synced with strategy: code," treat that as a description of how the sync
was *run*, not a durable setting that governs future syncs automatically —
every sync that needs code files must pass `--strategy code` explicitly (or
`--repo`/`--source` sync will default to markdown-only, silently skipping
`.py`/`.ts`/`.js` files with no warning).

**`gbrain sync` reads git commits, not the working tree, by default.** A
file reported as "modified" by a sync dry-run refers to the *committed*
version being re-imported. A separate, pre-existing uncommitted change to
that same file is untouched by the sync. `--no-pull` additionally guarantees
zero git interaction (no internal `git pull` attempt at all) — use it
whenever a source repo has known uncommitted changes that must be preserved
during a sync.

**GBrain's frontmatter parser fails closed on invalid YAML.** A `document:`
value containing an unquoted `: ` (colon-space) or a bare backtick breaks
parsing and **blocks the entire sync** at that checkpoint, not just that one
file — the sync reports `BLOCKED` and does not advance `last_commit` or
`last_sync_at`. `--skip-failed` exists to bypass this, but the safer, cleaner
remedy is almost always to quote the offending value and re-sync — this
resolves the block completely rather than leaving files permanently
un-imported.

**A strategy change alone does not trigger a rescan** if the source's git
commit hasn't changed since the last sync — the sync will report "Already up
to date" even though the strategy is now different. The source's
`last_commit` must be cleared first to force a genuine full walk.

### Dream Cycle (Call Graph & Intelligence)

Dream Cycle invocation, phase order, and diagnostics now live in their own
dedicated document — see `gbrain-dream-cycle-reference.md`. The one fact
worth repeating here since it affects source management directly: dream
cycle phases (including `resolve_symbol_edges`, which the call-graph
limitation above depends on) only populate the call graph if the source
was synced with `strategy: code` — see Sync & Import above.

### Schema Packs

| Command | Description |
|---|---|
| `gbrain schema active` | Show which pack is active |
| `gbrain schema list` | List bundled + installed packs |
| `gbrain schema show <pack>` | Pretty-print a pack manifest |
| `gbrain schema use <pack>` | Switch active pack |
| `gbrain schema downgrade [--to <pack>]` | Revert to the prior (or a named) pack |
| `gbrain schema explain <type>` | Show a page type's extraction properties |
| `gbrain schema validate` / `lint` | Validate/lint the active pack |

Switching a pack is **reversible** and affects only future page-type
assignment (and, optionally, retyping existing pages via
`gbrain schema sync --apply`) — existing pages, chunks, embeddings, and
source registrations are untouched by a pack switch.

### Source Management

| Command | Description |
|---|---|
| `gbrain sources add <id> --path <dir>` | Register a local source |
| `gbrain sources remove <id> --confirm-destructive` | Remove a source and its data |
| `gbrain sources status <id>` | Diagnostic for a source |

Inactive projects' sources should generally stay registered and synced
opportunistically rather than removed — GBrain's advisory memory has
different value characteristics than a write-permission model; searchable
history from an inactive project remains useful. Remove a source only when
it is a genuine content-free scaffold with nothing worth retaining.

**Source resolution precedence, and why a source is often named `default`.**
Two orthogonal axes exist: a *brain* (the database) and a *source* (a named
repo of content inside that brain). Each axis resolves independently, via
its own layered precedence chain, documented in the upstream repo's
`docs/architecture/brains-and-sources.md`:

```
WHICH BRAIN (DB)?                    WHICH SOURCE (repo in DB)?
 1. --brain <id>                      1. --source <id>
 2. GBRAIN_BRAIN_ID env               2. GBRAIN_SOURCE env
 3. .gbrain-mount dotfile             3. .gbrain-source dotfile
 4. longest-prefix mount path match   4. longest-prefix source path match
 5. (reserved: brains.default v2)     5. sources.default config
 6. fallback: 'host'                  6. fallback: 'default'
```

`default` is therefore GBrain's own hardcoded fallback source ID — not a
name a user picks. It's what a command resolves to when no `--source` flag,
`GBRAIN_SOURCE` env var, `.gbrain-source` dotfile, or path match applies.
The repo's own reference topology for the simplest case (a single-person
developer, one brain, one source) shows exactly this: a single source
literally named `default`, `federated: true`, holding all pages. Seeing a
source named `default` in `sources list` is expected, standard behavior for
a first/primary source — not something to second-guess or rename.

### Skillpack

| Command | Description |
|---|---|
| `gbrain skillpack list` | List the bundled skill count for the installed CLI version |
| `gbrain skillpack scaffold <name>\|<source>\|--all [--workspace PATH] [--dry-run] [--trust] [--no-cache] [--json]` | Copy skills into a workspace's `skills/` directory |
| `gbrain skillpack reference --all --workspace <path>` | Confirm a local copy matches the bundle |

- Scaffold is **additive only** — refuses to overwrite existing files, so
  reruns are safe.
- **`RESOLVER.md` is never scaffolded**, by design — the scaffold contract
  explicitly states the host's RESOLVER.md/AGENTS.md stays untouched. This
  only matters for hosts that consume a resolver for trigger-based
  auto-dispatch; OpenCode does not (it routes skills by name/description
  through its own `skill` tool), so the missing resolver is a non-issue
  there specifically.
- There is **no `--exclude`/`--skip` flag**. To omit specific skills from an
  `--all` scaffold (e.g. to avoid a name collision with an existing skill),
  scaffold the wanted skills individually by name instead of using `--all`.
- Scaffold writes to `<workspace>/skills/` — for OpenCode auto-discovery,
  target `<repo>/.opencode/skills/` (via `--workspace <repo>/.opencode`) or
  another OpenCode-recognized discovery root; a plain workspace-root
  `skills/` directory is **not** auto-discovered by OpenCode.
- Bundle size and skill set track the installed CLI version and can change
  substantially between versions — always re-run a `--dry-run --json` to get
  the current exact file list before scaffolding, rather than assuming a
  count from a prior version.

### Knowledge Graph & Facts

| Command | Description |
|---|---|
| `gbrain think "<question>"` | Multi-hop synthesis across pages + takes + graph |
| `gbrain recall` | Query per-source hot memory (facts) |
| `gbrain takes-list` | List takes (claims with weight/confidence) |

### MCP & Server

| Command | Description |
|---|---|
| `gbrain serve` | Start MCP server (holds DB lock during CLI conflicts) |
| `gbrain self-upgrade` | Check for and apply pending version + schema migrations |
| `gbrain self-upgrade --check-only` | Report whether an upgrade is available, without applying it |
| `gbrain upgrade` | (bun-link installs) `git pull --ff-only` + `bun install` + post-upgrade; applies pending schema migrations automatically |
| `gbrain apply-migrations --yes` | Apply pending schema migrations directly |

**MEMORY_VERBS v1**: a cleaner, five-tool MCP surface (`recall`, `remember`,
`entity`, `synthesize`, `forget`) that replaces the full "op wall." Opt-in
via `gbrain config set mcp_surface verbs`. Confirm current adoption status
in the relevant project's `gbrain-config.md` before assuming it's active —
it defaults off.

**After upgrading a bun-link install (`gbrain upgrade`) while OpenCode is
already running:** the in-memory `gbrain serve` MCP process continues
serving the *old* binary version until OpenCode is restarted — the CLI
itself reports the new version immediately, but the MCP-served version lags
until the next process restart. This is the same underlying mechanism as the
general MCP bootstrap-timing behavior described in `graphify-reference.md`.

---

## Resolved Incidents — Kept for Fast Recognition

Everything below has already been found and fixed at least once. Kept here
so the same root cause, if it recurs, is a two-minute fix rather than a
rediscovery.

### A registered code source never actually ingests `.py` files

**Symptom:** `resolve_symbol_edges` reports "no chunks needed symbol
resolution," or a source's page count is far lower than the real file count
in its repo, and the pages that do exist are only README/theme/metadata
content.

**Cause:** the source was synced without `--strategy code` at least once
(remember: strategy is a sync-time flag, not a stored setting — see Sync &
Import above), so sync defaulted to markdown-only, skipping every code file
indefinitely, with no warning.

**Fix — three steps, in order, all required:**
```bash
psql "postgresql://postgres:***@localhost:5432/gbrain" -c "UPDATE sources SET config = config || '{\"strategy\": \"code\"}'::jsonb WHERE id = '<source-id>';"
psql "postgresql://postgres:***@localhost:5432/gbrain" -c "UPDATE sources SET last_commit = NULL WHERE id = '<source-id>';"
gbrain sync --source <source-id> --strategy code
```
(The `UPDATE ... config` step is a direct DB write and does not imply
`strategy` is normally read back from that field on future syncs — it's a
one-time correction; the `--strategy code` flag must still be passed on
every future sync that needs code content.)

### A stuck migration keeps showing in `doctor` after being fixed

**Symptom:** `gbrain doctor` shows `upgrade_errors: WARN` referencing an
old, already-resolved post-upgrade failure.

**Cause:** this check reads only the *last line* of a permanent, append-only
log (`~/.gbrain/upgrade-errors.jsonl`) — it does not re-check live migration
state, so a resolved issue keeps showing forever.

**Fix:**
```bash
gbrain apply-migrations --yes
mv ~/.gbrain/upgrade-errors.jsonl ~/.gbrain/upgrade-errors.jsonl.resolved-<date>
```

### Embedding/chat calls fail with "API key is invalid"

This is a Dream Cycle `extract_atoms`-phase issue — full symptom, cause,
and diagnostic commands now live in `gbrain-dream-cycle-reference.md`.

### A sync gets BLOCKED on invalid frontmatter, and doesn't advance

**Symptom:** `gbrain sync --source <id>` exits 0 but reports
`Sync blocked: N file(s) failed to parse: UNKNOWN: N`, and `last_commit`/
`last_sync_at` do not advance even though some files were banked at a
checkpoint.

**Cause:** one or more source files have a `document:` frontmatter value
containing an unquoted `: ` or a bare backtick — invalid YAML, and GBrain's
parser fails closed rather than skipping just the bad file.

**Fix:** quote the offending value(s) — minimal, single-line edits, e.g.
`document: Issue tracker: GitHub` → `document: "Issue tracker: GitHub"` —
then re-run the same sync command. Avoid `--skip-failed` unless a partial
result is explicitly acceptable; quoting the value is almost always a
one-line fix that resolves the block completely.

### A resolved sync-failure record keeps showing as unresolved

**Symptom:** `~/.gbrain/sync-failures.jsonl` retains a stale `open` record
for a file that has already been fixed and re-synced successfully.

**Cause:** the failure record's filename was a git **rename destination**.
GBrain processes renames by moving the page slug without re-parsing content,
so the brain's stored copy keeps the pre-rename (broken) frontmatter even
after the source file itself is fixed, until a future *content* change (not
just a rename) or a full re-sync actually re-parses that file.

**Fix:** not urgent — the record clears on the next sync that involves a
genuine content change to that file. It does not indicate a live, current
failure.

### A credentials-looking file turns out to describe an already-superseded setup

**Symptom:** an old, untracked documentation file in a tooling repo (not the
project repo itself) contains what look like live database URLs, API keys,
or personal access tokens.

**Cause found in this project:** a leftover doc from a prior GBrain
installation generation (Supabase + OpenRouter) that predated the current
local-PostgreSQL + OpenAI setup by several versions. The file was never
committed but wasn't gitignored either — meaning a routine `git add .` in
that repo would have swept it into history.

**Standing practice:** before assuming any credentials-looking file in a
tooling/config repo is current, check it against the *actual* live
configuration (`gbrain --version`, `~/.gbrain/config.json` engine/embedding
fields) rather than trusting the file's own claims. If it's confirmed stale
and describes a superseded setup, delete it (if untracked) or gitignore it
(if it must be retained for reference), and flag any real-looking credential
values for rotation — never print, copy, or archive the values themselves
while doing so.

---

## Authority Model

1. User decision in the current session
2. Authoritative repo files and ADRs
3. OpenCode rules and validated outputs
4. GBrain memory (advisory only)

When GBrain recall conflicts with current files, the files win. See
`memory-explainer.md` for how this interacts with Graphify's authority over
current code structure specifically.

---

## OpenCode Integration

GBrain is available in OpenCode via a local MCP server (`gbrain serve`).

**Important — MCP servers start once, at OpenCode process bootstrap, not per
chat session.** Adding or changing an `mcp.*` config entry while OpenCode is
already running does not make the change take effect in a new chat session
within that same running process — a full process restart (fully quit and
relaunch, not just a new conversation) is required before the change is
live. This applies equally to GBrain and to any other MCP integration (e.g.
Graphify).

The `/sync-gbrain` skill, where available, syncs and updates a project's
`AGENTS.md`/`agents.md` guidance block (append-only, its own delimiter
markers — does not conflict with any other managed block already in that
file, provided the other block uses different markers and does not attempt
to own the same section).

| OpenCode Command | Description |
|---|---|
| `/sync-gbrain` | Incremental sync (default) |
| `/sync-gbrain --dream` | Build call graph via dream cycle |
| `/sync-gbrain --code-only` | Only run the code stage |
| `/setup-gbrain` | One-time setup |

The GStack orchestrator behind `/sync-gbrain --dream` derives its source IDs
deterministically (`gstack-code-<slug>-<hostpathhash8>`) and has no option
to reuse an existing, directly-registered source of the same underlying
path — if a source was already registered manually (e.g. via
`gbrain sources add`), the orchestrator's code stage will fail on a path
overlap rather than reusing it. The least-destructive workaround is to
bypass the orchestrator's code stage and run `gbrain dream --source <id>`
directly against the existing source.

---

## File Locations

| Item | Location |
|---|---|
| GBrain CLI | `~/.bun/bin/gbrain` (on PATH) |
| Config | `~/.gbrain/config.json` |
| GBrain source (for direct diagnosis) | `/home/dev-p/gbrain/src/` |
| Schema packs | `~/.gbrain/schema-packs/` |
| Legacy PGLite database (retained, not in use) | `/home/dev-p/.gbrain/brain.pglite` |
| Sync failure log | `~/.gbrain/sync-failures.jsonl` |
| Upgrade error log | `~/.gbrain/upgrade-errors.jsonl` |

---

## Troubleshooting

**Overlapping source paths:** GBrain doesn't allow a child directory to be
registered when its parent is already a source (or vice versa). Remove the
conflicting source first.

**Stale sync lock:** `gbrain sync --break-lock`

**Embedding fails (API key error):** `source ~/.bashrc`, then retry — see
"Embedding/chat calls fail" above if this doesn't resolve it.

**Sync says "no allowlisted changes":** normal — nothing new to sync from
the relevant orchestrator's internal working state.

**`doctor` fails `sync_freshness` even after `gbrain sync --all`:**
`sync --all` only stamps a source's `last_sync_at` when there's a new
commit to advance to — a source reporting `up_to_date (added=0,
modified=0, deleted=0)` gets no timestamp update, even though sync ran
correctly. `doctor` has its own short-circuit for this ("nothing
changed, don't complain") — but it only fires when the repo's working
tree has no uncommitted tracked changes. Any local edit sitting
uncommitted defeats the short-circuit and lets the plain time-based
check fail once it passes 72h. Fix: commit and push whatever's
uncommitted (`git status --porcelain` to check), then re-run `gbrain
sync --source <id>`.

**Sync says "Sync blocked":** see "A sync gets BLOCKED on invalid
frontmatter" above.

**MCP not responding in OpenCode:** a full process restart is very likely
the fix — see "OpenCode Integration" above before assuming a config error.
```
pkill -f "opencode web"
cd <project-root>
opencode web --hostname 0.0.0.0
```

---

*End of document*
