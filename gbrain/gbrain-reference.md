---
document: "GBrain — Reference: Commands, Mechanics, Incidents, Troubleshooting"
doc-id: gbrain-reference
state: Live
date-created: 2026-09-05
---

# GBrain — Reference: Commands, Mechanics, Incidents, Troubleshooting

Companion to [[gbrain-config|Configuration]] (the spec — current state) and
[[gbrain-explainer|Explainer]] (what it is and why — the authoritative whole-system
narrative). Exam companions: [[gbrain-exam-plan|Exam Plan]] (next run's job-spec),
[[gbrain-exam-report|Exam Report]] (current verified state), [[gbrain-log|Log]] (notable
events), [[gbrain-learnings|Learnings]] (transient exam knowledge). Agent-facing.
Division-scoped — applies across all projects.

---

## What GBrain is (one paragraph)

GBrain is the advisory memory layer. It stores and searches project documents
and code as searchable vector memories. GBrain does not override repo files,
ADRs, or OpenCode rules — files are always authoritative.

**Engine:** PostgreSQL 16 + pgvector (WSL-native) | **Version:** `0.46.1.0`
(upgrade available: 0.48.2.0) | **Schema:** v128 | **Pack:** gbrain-everything
**Connection:** `postgresql://postgres:***@localhost:5432/gbrain`

Current sources, credentials, and MCP entry: [[gbrain-config|Configuration]]. Cross-
component reasoning (Graphify, Dream Cycle, Memory Governor, the authority
model): [[memory-master-explainer|Master Explainer]].

---

## Command Reference

### Health & Status

| Command | Description |
|---|---|
| `gbrain doctor` | Full health check (score out of 100) |
| `gbrain doctor --fast` / `--json --fast` | Quick / machine-readable health |
| `gbrain stats` | Pages, chunks, embed coverage, type breakdown |
| `gbrain --version` | Installed version |
| `gbrain sources list` / `--json` | Registered sources with paths and page counts |

### Search & Query

| Command | Description |
|---|---|
| `gbrain search "<terms>"` | Keyword search (full-text) |
| `gbrain query "<question>"` | Hybrid search (vector + keyword + expansion) |
| `gbrain query "<q>" --source <id>` | Scope to one source |
| `gbrain query "<q>" --limit N` / `--lang <lang>` / `--near-symbol <name>` | Limit / language filter / symbol anchor |
| `gbrain query "<q>" --adaptive-return` | Tight result set for lookup questions |

### Code Analysis

| Command | Description |
|---|---|
| `gbrain code-def <symbol>` | Where a symbol is defined |
| `gbrain code-refs <symbol>` | All references to a symbol |
| `gbrain code-callers <symbol>` / `code-callees <symbol>` | Callers / callees |
| `gbrain code-blast <symbol>` | Transitive caller tree |

**Permanent limitation, double-verified:** `code-callers`/`code-callees`
resolve same-file references only (confirmed via source read of
`resolve-symbol-edges.ts`), AND no bundled schema pack extracts call-graph
edges at all (`code` is `extractable: false` in every pack). Returns symbol
names with `resolved: false` universally. Pack-switching does not fix it.
`code-def`/`code-refs` are unaffected. For resolved cross-file call/import/
containment relationships use Graphify's `get_neighbors`.

### Sync & Import

| Command | Description |
|---|---|
| `gbrain sync --repo <path>` | Sync a repo (markdown by default) |
| `gbrain sync --repo <path> --strategy code` | Include code files (.py/.ts/.js/.yaml) |
| `gbrain sync --source <id>` | Sync one registered source |
| `gbrain sync --source <id> --no-pull` | Sync without any git interaction |
| `gbrain sync --source <id> --dry-run` | Preview, no writes |
| `gbrain sync --all` | Sync all registered sources |
| `gbrain sync --break-lock` | Break a stale sync lock |
| `gbrain embed --stale` | Embed chunks missing embeddings |
| `gbrain extract --stale` | Extract links/timelines from stale pages |

**`--strategy` is a sync-time flag, not a stored setting** — every sync that
needs code files must pass `--strategy code` explicitly, or code files are
silently skipped.

**`gbrain sync` reads git commits, not the working tree, by default.**
`--no-pull` guarantees zero git interaction — use it when a source repo has
uncommitted changes that must be preserved.

**Frontmatter parsing fails closed** on invalid YAML (a `document:` value
with an unquoted `: ` or a bare backtick) and **blocks the entire sync** at
that checkpoint — `last_commit`/`last_sync_at` do not advance. Remedy: quote
the offending value and re-sync. `--skip-failed` exists but leaves files
permanently un-imported; prefer the quote fix.

**A strategy change alone does not trigger a rescan** if the source's git
commit hasn't changed — clear `last_commit` first to force a full walk.

**New sources are not covered by the standing sync script** — verified
2026-09-06: `sync-gbrain.sh` syncs the repo source only; a newly registered
source needs `gbrain sync --source <id>` for its first import.

**Two content paths, two layers (do not mix):** sync writes the pages/corpus
layer; it must never be used to move governed content into GBrain — only the
governor's own async `remember` path counts as governed
([[memory-governor-config|Memory Governor Configuration]], GBrain integration). Symmetrically, the
governed path writes facts, never corpus pages. See [[gbrain-config|Configuration]]'s
"Content paths into GBrain."

### Dream Cycle

Invocation, phase order, and diagnostics: [[gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]].
Fact that affects source management: dream phases (including
`resolve_symbol_edges`) only populate the call graph if the source was synced
with `--strategy code`.

### Schema Packs

| Command | Description |
|---|---|
| `gbrain schema active` / `list` / `show <pack>` | Inspect packs |
| `gbrain schema use <pack>` / `downgrade` | Switch / revert (reversible; existing pages, chunks, embeddings, and sources untouched) |
| `gbrain schema explain <type>` / `validate` / `lint` | Type properties / validation |

### Source Management

| Command | Description |
|---|---|
| `gbrain sources add <id> --path <dir>` | Register a local source |
| `gbrain sources remove <id> --confirm-destructive` | Remove source and data |
| `gbrain sources status <id>` | Per-source diagnostic |

Overlapping source paths are refused (child under a registered parent or vice
versa). Inactive projects' sources stay registered — searchable history from
an inactive project retains value; remove only content-free scaffolds.

**Source resolution precedence** (upstream `docs/architecture/brains-and-sources.md`):

```
WHICH BRAIN (DB)?                    WHICH SOURCE (repo in DB)?
 1. --brain <id>                      1. --source <id>
 2. GBRAIN_BRAIN_ID env               2. GBRAIN_SOURCE env
 3. .gbrain-mount dotfile             3. .gbrain-source dotfile
 4. longest-prefix mount path match   4. longest-prefix source path match
 5. (reserved: brains.default v2)     5. sources.default config
 6. fallback: 'host'                  6. fallback: 'default'
```

### Skillpack

| Command | Description |
|---|---|
| `gbrain skillpack list` | Bundled skill count for the installed version |
| `gbrain skillpack scaffold <name>|<source>|--all [--workspace PATH] [--dry-run] [--trust] [--json]` | Copy skills into `<workspace>/skills/` |
| `gbrain skillpack reference --all --workspace <path>` | Confirm a local copy matches the bundle |

Additive only (refuses overwrites). `RESOLVER.md` is never scaffolded (by
design; irrelevant to OpenCode). **No `--exclude` flag** — omit skills by
scaffolding individually by name. Target `<repo>/.opencode/skills/` for
OpenCode auto-discovery. Bundle content tracks the CLI version — always
`--dry-run --json` before scaffolding rather than assuming prior counts.

### Knowledge Graph & Facts / MCP & Server

| Command | Description |
|---|---|
| `gbrain think "<question>"` | Multi-hop synthesis across pages + takes + graph |
| `gbrain recall` / `gbrain takes-list` | Hot-memory facts / weighted claims |
| `gbrain serve` | Start MCP server |
| `gbrain self-upgrade --check-only` | Report available upgrade without applying |
| `gbrain upgrade` | (bun-link) pull + install + migrations |
| `gbrain apply-migrations --yes` | Apply pending migrations directly |

**MEMORY_VERBS:** the memory verbs (`remember`, `recall`, `entity`,
`forget`, `synthesize`, `context_pack`, `delta`) are present in the current
version's default MCP surface — no `mcp_surface` config is set in this
environment (verified 2026-09-06). A verbs-only surface (`gbrain config set
mcp_surface verbs`) remains available as a config choice.

**After upgrading a bun-link install while OpenCode is running:** the
in-memory `gbrain serve` keeps serving the old version until a full process
restart — the CLI reports the new version immediately.

---

## Resolved Incidents — kept for fast recognition

### A registered code source never ingests `.py` files

Symptom: `resolve_symbol_edges` reports nothing to resolve; page count far
below real file count; only metadata pages exist. Cause: synced without
`--strategy code` at least once (flag, not setting). Fix, in order:
```bash
psql "postgresql://postgres:***@localhost:5432/gbrain" -c "UPDATE sources SET config = config || '{\"strategy\": \"code\"}'::jsonb WHERE id = '<source-id>';"
psql "postgresql://postgres:***@localhost:5432/gbrain" -c "UPDATE sources SET last_commit = NULL WHERE id = '<source-id>';"
gbrain sync --source <source-id> --strategy code
```

### A stuck migration keeps showing in `doctor` after being fixed

The check reads only the last line of the append-only
`~/.gbrain/upgrade-errors.jsonl`. Fix:
```bash
gbrain apply-migrations --yes
mv ~/.gbrain/upgrade-errors.jsonl ~/.gbrain/upgrade-errors.jsonl.resolved-<date>
```

### Embedding/chat calls fail with "API key is invalid"

Dream Cycle `extract_atoms`-phase issue — see [[gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]].

### A sync gets BLOCKED on invalid frontmatter, and doesn't advance

See Sync & Import above. Quote the offending `document:` value; re-run the
same sync. Avoid `--skip-failed` unless partial results are acceptable.

### A resolved sync-failure record keeps showing as unresolved

The failure record's filename was a git rename destination — GBrain moves the
slug without re-parsing content, so the stored copy keeps pre-rename
frontmatter until a genuine content change re-parses it. Not urgent; clears on
the next content-touching sync.

### A credentials-looking file describes a superseded setup

Check any credentials-looking file against the *actual* live configuration
(`gbrain --version`, `~/.gbrain/config.json` engine/embedding fields) before
trusting its own claims. If confirmed stale: delete (untracked) or gitignore
(retained for reference); flag real-looking credential values for rotation —
never print, copy, or archive the values.

---

## Authority Model

1. User decision in the current session
2. Authoritative repo files and ADRs
3. OpenCode rules and validated outputs
4. GBrain memory (advisory only)

When GBrain recall conflicts with current files, the files win. Cross-tool
authority ordering (including Graphify confidence tiers): see
[[memory-master-explainer|Master Explainer]] §7.

---

## OpenCode Integration

GBrain is reached via the local MCP server (`gbrain serve`) — global
`opencode.jsonc` entry (see config.md). **MCP servers start once at OpenCode
process bootstrap** — config changes need a full process restart, not a new
chat session.

Installed skills: `/sync-gbrain` (incremental sync; `--dream` call graph;
`--code-only`; `--dry-run`) and `/setup-gbrain` (one-time setup). These follow
upstream gstack's integration shape; this environment's actual standing sync
path is the custom script (config.md).

The gstack orchestrator behind `/sync-gbrain --dream` derives its own source
IDs (`gstack-code-<slug>-<hash8>`) and fails on path overlap with a manually
registered source — bypass the code stage and run `gbrain dream --source <id>`
directly instead.

---

## File Locations

| Item | Location |
|---|---|
| GBrain CLI | `~/.bun/bin/gbrain` (on PATH) |
| Config | `~/.gbrain/config.json` |
| Live install (diagnosis) | `/home/dev-p/gbrain/src/` |
| Source clone (stale, v0.25.0) | `/mnt/c/mybizz/gbrain` — see config.md open items |
| Schema packs | `~/.gbrain/schema-packs/` |
| Legacy PGLite (retained, unused) | `~/.gbrain/brain.pglite` |
| Sync failure / upgrade error logs | `~/.gbrain/sync-failures.jsonl` / `~/.gbrain/upgrade-errors.jsonl` |
| Standing sync script | `/mnt/c/mybizz/scripts/sync-gbrain.sh` |

---

## Troubleshooting

**Stale sync lock:** `gbrain sync --break-lock`.

**Embedding fails (API key error):** source `~/.bashrc`, retry; see the
Dream Cycle reference if unresolved.

**`doctor` fails `sync_freshness` even after `gbrain sync --all`:** a source
reporting `up_to_date` gets no timestamp update; doctor's short-circuit fires
only when the working tree is clean — commit and push uncommitted changes,
then re-sync.

**MCP not responding in OpenCode:** full process restart first (see above):
```bash
pkill -f "opencode web"
cd <project-root>
opencode web --hostname 0.0.0.0
```

---

## Do not

- Do not install or upgrade GBrain via npm — the npm `gbrain` package is unrelated and shadows the binary (upstream warning). Install/upgrade only via the documented GitHub paths.
- Do not switch or install a different schema pack expecting it to fix the call-graph limitation — confirmed impossible with any bundled pack.
- Do not run `gbrain sync --skip-failed` as a default remedy — fix the offending frontmatter and re-sync cleanly.
- Do not rely on `strategy` being stored per source — pass `--strategy code` explicitly on every sync that needs code files.
- Do not call `gbrain sync` to move governed content into GBrain — only the governor's async `remember` path counts as governed ([[memory-governor-config|Memory Governor Configuration]]). Sync is for the pages layer; the governed path is for the facts layer.
- Do not treat an offline test pass as live verification for anything GBrain-adjacent — the same evidence-not-proof standard as everywhere else.
- Do not upgrade GBrain on version-newness alone — the standing policy is upgrade-only-on-check-failure and is an open item (config.md).
- Do not assume the standing sync script covers newly registered sources — run `gbrain sync --source <id>` for a new source's first import.
- Do not re-enable the `gbrain autopilot` schedule or put the dream cycle on a scheduler — on-demand invocation is the deliberate design; the autopilot was found inert and removed 2026-09-06 (see [[gbrain-dream-cycle-config|Configuration]]).
