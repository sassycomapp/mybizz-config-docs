---
title: "gbrain-reference"
doc-id: "mb-bb4cbd8d"
updated: "2026-10-20"
---
# GBrain — Reference: Commands, Mechanics, Incidents, Troubleshooting

Companion to [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) (current state — every value lives there),
[[[mybizz-config-docs:gbrain/gbrain-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-explainer.md) (what it is and why) and
[[[mybizz-config-docs:gbrain/gbrain-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-learnings.md) (what differs from the standard in this setup).
Agent-facing. Division-scoped — applies across all projects.

---

## What GBrain is (one paragraph)

GBrain is the advisory memory layer. It stores and searches project documents
and code as searchable vector memories. GBrain does not override repo files,
ADRs, or OpenCode rules — files are always authoritative.

Version, engine, schema, pack, connection, sources and credentials:
[[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md). Cross-component reasoning (Graphify,
Dream Cycle, Memory Governor, the authority model):
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md).

---

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Upstream repository and docs | `https://github.com/garrytan/gbrain` (docs/ in the checkout) | 0.59.18.0 | 2026-10-20 |
| Brains-and-sources architecture | `https://github.com/garrytan/gbrain/blob/master/docs/architecture/brains-and-sources.md` | 0.59.18.0 | 2026-10-20 |
| Authorization upgrade guide | `https://github.com/garrytan/gbrain/blob/master/docs/guides/authorization-upgrade.md` | 0.59.18.0 | 2026-10-20 |
| Installed source code | `/home/dev-p/gbrain/src` (at tag `v0.59.18.0`) | 0.59.18.0 | 2026-10-20 |
| MyBizz source-repo organization | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | — | 2026-10-20 |

---

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `gbrain --version` | agent |
| Works | `gbrain doctor --fast` | agent |
| `mcp_surface` | `gbrain config get mcp_surface` | agent |
| Brain default source | `gbrain config get sources.default` | agent |
| `search.reranker.enabled` | `gbrain config get search.reranker.enabled` | agent |
| Job expiry | `gbrain config get minions.ttl_waiting_hours.facts-absorb` | agent |
| Registered sources and states | `gbrain sources list` | agent |
| Reranker health | `gbrain doctor 2>&1 \| grep reranker_health` | agent |
| `config.json` content | masked read of `~/.gbrain/config.json` (sensitive-data guard) | developer |
| Full sync sample | run the standing sync script (content-changing) | developer |
| MCP restart behavior | full OpenCode process restart | developer |
| Upgrade decision | the procedure in §Upgrading | developer |

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
| `gbrain backup status` | Per-source backup and git-remote recovery evidence |

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
| `gbrain sync --source <id> --full --no-pull` | Full resync — **drops pages of files that were moved or deleted**; run it after renaming or removing files, or they linger |
| `gbrain sync --source <id> --dry-run` | Preview, no writes |
| `gbrain sync --source <id> --exclude '<glob>'` | Skip files matching the glob (repeatable) — the standing script excludes `obsolete/**` and `**/obsolete/**` |
| `gbrain sync --all` | Sync all registered sources |
| `gbrain sync --break-lock` | Break a stale sync lock |
| `gbrain embed --stale` | Embed chunks missing embeddings |
| `gbrain extract --stale` | Extract links/timelines from stale pages — **misses links into other sources** (the sync already marks its pages as done) |
| `gbrain extract links --source db` | Read every page from the database and write all its links, including links into other sources. The standing sync script uses this form |

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
permanently un-imported; prefer the quote fix. `gbrain frontmatter validate
<path>` pinpoints the file; its `--fix` repairs only NULL_BYTES, MISSING_CLOSE,
NESTED_QUOTES and SLUG_MISMATCH (backups under `~/.gbrain/backups/frontmatter/`)
— an unquoted colon (YAML_PARSE) needs the manual quote. A file that keeps
failing is skipped automatically after 3 consecutive syncs.

**Frontmatter conventions:** frontmatter is parsed as YAML, so
`title: "Example"` and `title: Example` produce the same title — the quotes
are syntax, not content. Title precedence: frontmatter `title`, then the
first body H1, then the filename/slug-derived title. `title` and `type` are
required by the documented page convention and linting, while the parser
itself tolerates their absence (it has fallbacks and can infer `type`);
`tags` is optional (missing becomes `[]`); a custom field such as `doc-id`
is safe — unknown frontmatter fields are preserved.

**A strategy change alone does not trigger a rescan** if the source's git
commit hasn't changed — clear `last_commit` first to force a full walk.

**The standing sync script enumerates every registered source** (`gbrain
sources list --json | jq`) and runs `gbrain sync --source <id>
--no-pull --exclude 'obsolete/**' --exclude '**/obsolete/**'` for each, then
`gbrain extract links --source db` and `gbrain embed --stale`. Before that it
resets the brain default source (`gbrain sources default default`) — the
memory governor retargets the default to the owning project on every governed
write, and a default naming a missing source stops every sync. Run it with
`bash /mnt/c/mybizz/scripts/sync-gbrain.sh`; it logs to
`C:\mybizz\logs\gbrain-logs\` and exits with an error if any step fails. The
link step must be the full database read: a sync already marks the pages it
imported as done, so `gbrain extract --stale` finds nothing and links between
repositories stay missing. A bare `gbrain sync` syncs only the source of the
current folder. `--no-pull` is standing policy: the repositories are edited
and committed only in WSL, so there is nothing to pull, and a network hiccup
("Could not resolve host") would otherwise leave a sync incomplete. Changes
made outside WSL are not picked up. The one clone that follows an upstream
project (`anvil-agent-references`) is updated by hand:
`git -C /mnt/c/mybizz/anvil-agent-references pull`.

**Two content paths, two layers (do not mix):** sync writes the pages/corpus
layer; it must never be used to move governed content into GBrain — only the
governor's own async `remember` path counts as governed
([[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md),
GBrain integration). Symmetrically, the governed path writes facts, never
corpus pages. See the
[[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) "Content paths into GBrain".

### Dream Cycle

Runs by hand weekly, after the Sunday backup, through the memory diagnostic
(`mb-memory-system-diagnostic`). Invocation, phase order, and diagnostics:
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Dream Cycle Reference]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md).
Fact that affects source management: dream phases (including
`resolve_symbol_edges`) only populate the call graph for a source synced
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
| `gbrain sources default <id>` | Set the brain-level default source (`sources.default`). The id must exist — a default that names a deleted source stops every sync |
| `gbrain sources federate <id>` / `unfederate <id>` | Include a source in cross-source default search (and let it write links into other sources) / isolate it explicitly. A source never set shows as `unset` |

Overlapping source paths are refused (child under a registered parent or vice
versa). Inactive projects' sources stay registered — searchable history from
an inactive project retains value; remove only content-free scaffolds.
`gbrain sources add --path` requires the target to be a git repository with
at least one committed (tracked) file — an empty commit is refused by design
(write a placeholder file and commit first). `--force` skips that check and
registers a folder before its first commit.

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

Facts follow the same order: `remember` writes into the selected source and
`recall` reads the facts of that one source. Details for the memory governor:
[[[mybizz-config-docs:memory-governor/memory-governor-reference|Memory Governor Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md).

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
| `gbrain call forget '{"id": "<n>"}'` | Forget a fact by its id |
| `gbrain serve` | Start MCP server |
| `gbrain self-upgrade --check-only` | Report available upgrade without applying |
| `gbrain upgrade` | Upstream's one-step upgrade. **Not used for this install** — see §Upgrading (upstream's guide says it can run setup phases that start autopilot) |
| `gbrain apply-migrations --force-schema --yes` | Apply schema migrations only — the cutover form. Plain `--yes` can also run setup phases |
| `gbrain jobs list [--status S]` / `stats` / `cancel <id>` | Job queue: inspect / cancel |
| `gbrain jobs authorize-legacy --ids <ids> [--expect <digest>] --yes` | Authorize pre-upgrade waiting jobs after review — read the preview, pass the digest it prints |

**MEMORY_VERBS:** the memory verbs (`remember`, `recall`, `entity`,
`forget`, `synthesize`, `context_pack`, `delta`) are present in the MCP
surface. `mcp_surface` is `verbs` in the **database** config plane (`gbrain
config get mcp_surface` → `verbs`, `[config] source: db plane`);
`~/.gbrain/config.json` carries no such key. Change it with
`gbrain config set mcp_surface <verbs|starter|full>`. The
writer/ownership model behind page writes is not adopted — see the
[[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) standing decision.

**After upgrading a bun-link install while OpenCode is running:** the
in-memory `gbrain serve` keeps serving the old version until a full process
restart — the CLI reports the new version immediately.

---

## Upgrading GBrain (this install: a linked Git checkout)

Rules (upstream's authorization-upgrade guide plus this environment's policy):
the decision and its reason are the developer's, recorded before the work
starts; never install from npm; do not run `gbrain upgrade`, `gbrain
self-upgrade`, `gbrain post-upgrade` or plain `gbrain apply-migrations --yes`
for the cutover (they can run setup phases that start autopilot); never run
old and new workers together; every waiting job must be authorized or
cancelled before a worker starts; keep backups and job previews private (they
can contain secrets and job payloads); if any step prints something this
procedure does not describe, stop.

1. **Prepare.** Bun ≥ 1.3.11; the checkout clean; `git -C /home/dev-p/gbrain branch pre-upgrade-backup HEAD`; compare the old and the new release in a sandbox first — the names and inputs of commands and agent tools (this does not cover behavior, permissions, queued jobs or database layout); save `gbrain doctor` and a per-source fact snapshot (from the home folder: `GBRAIN_SOURCE=<id> gbrain call recall '{"limit": 500}'` for every source).
2. **Stop everything that uses GBrain.** OpenCode (it starts `gbrain serve`); the memory governor (API first, wait 60 seconds, then the worker); cancel or authorize the waiting jobs (`gbrain jobs list --status waiting`; `gbrain jobs cancel <id>`, or preview then `gbrain jobs authorize-legacy --ids <ids> --expect <digest> --yes`).
3. **Back up.** Every database (`sudo -u postgres pg_dump -Fc <db>`) and `~/.gbrain`; check each dump with `pg_restore -l`.
4. **Install.** Fetch only the release tag (a plain `git fetch --tags` returns an error because the floating tag `latest-stable` has moved), check that it is the tested commit, `git checkout <tag>`, `bun install --ignore-scripts`, confirm `gbrain --version`.
5. **Migrate.** `gbrain apply-migrations --force-schema --yes`.
6. **Prove.** Doctor before and after; start the governor and check it: port 8321 held by a single listener (`ss -tlnp | grep 8321`), `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8321/memory/review-queue` prints 422, and the worker unit still carries its `~/.bun/bin` PATH line (without it every delivery fails); per-source fact comparison; a full sync, then confirm the script still ends with the full link read (`grep -n "extract links --source db" /mnt/c/mybizz/scripts/sync-gbrain.sh` prints one line) and that the sources' federation states are unchanged; `python3 /mnt/c/mybizz/scripts/mb-doc-check.py slug-selftest` reports 0 differences and `python3 /mnt/c/mybizz/scripts/mb-doc-check.py sources-check` says everything matches (the `mb-doc-check` page-name rule must equal GBrain's own); one real `/mb-submit-memory` run; `gbrain config get sources.default` must name an existing source.

Rollback: `cutover-rollback.sh --yes` (checks out `master`, runs `bun install
--ignore-scripts`, restores every dump). Scripts: `cutover-block1.sh` (in
`~/backups/`), `cutover-block2.sh`, `cutover-block3.sh` and
`cutover-rollback.sh` (in `C:\mybizz\scripts\`) run the stop/back-up,
install/migrate, start/prove stages and the rollback with checks at every
stage. They were written for one specific upgrade — before reuse, change the
tag, the expected commit and the version text at the top of
`cutover-block2.sh`, and read the rollback script, which returns to the saved
commit and prints the version it expects. After an upgrade the checkout stays
in detached HEAD on the release tag; `master` holds the prior release state.

---

## Incidents — symptom, cause, fix

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
mv ~/.gbrain/upgrade-errors.jsonl ~/.gbrain/upgrade-errors.jsonl.resolved
```

### Embedding/chat calls fail with "API key is invalid"

Dream Cycle `extract_atoms`-phase issue — see
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Dream Cycle Reference]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md).

### A sync gets BLOCKED on invalid frontmatter, and doesn't advance

See Sync & Import above. Quote the offending `document:` value; re-run the
same sync. Avoid `--skip-failed` unless partial results are acceptable.

### A resolved sync-failure record keeps showing as unresolved

The failure record's filename is a git rename destination — GBrain moves the
slug without re-parsing content, so the stored copy keeps pre-rename
frontmatter until a genuine content change re-parses it. Not urgent; clears on
the next content-touching sync.

### Every sync ends with `Source "<id>" not found or is archived`

Cause: `sources.default` names a source that no longer exists (the memory
governor's worker changes the default before every write). Under the
installed version every sync then fails, for all sources. Check and fix:
```bash
gbrain config get sources.default
gbrain sources list
gbrain sources default default
```

### A sync says `git pull failed … Could not resolve host: github.com`

A passing network problem. GBrain reports the sync as incomplete and leaves its
position unchanged, so a retry is safe. The standing script passes
`--no-pull`, so it does not depend on GitHub.

### One invalid-frontmatter file blocks a whole source

An unquoted `document:` value with a colon inside (for example
`document: Issue tracker: Local markdown`) blocks the sync. Fix: quote the
value, commit, push, sync. `gbrain frontmatter validate <repo>` finds such
files without changing anything.

### `git fetch --tags` refuses to overwrite `latest-stable`

Harmless: the floating tag moved upstream. Fetch only the release tag instead
(see §Upgrading).

### The sync finished, but links between repositories are missing

Symptom: `gbrain backlinks <page> --source <id>` lists no page from another source,
and `GBRAIN_SOURCE=<id> gbrain call get_links '{"slug":"<page>"}'` shows no link into
another source, although the documents contain `[[[source-id:slug]]](path)` links.
`gbrain extract --stale` answers "No stale pages". Cause: the sync marks the pages it
imports as already extracted, and that step cannot resolve links into other sources, so
the later `--stale` pass skips them. Fix:
```bash
gbrain extract links --source db
```
The setting `link_resolution.cross_source` is not needed when the linking
sources are federated. The full read takes longer than `--stale`.

### A credentials-looking file describes a superseded setup

Check any credentials-looking file against the *actual* live configuration
(`gbrain --version`, `~/.gbrain/config.json` engine/embedding fields) before
trusting its own claims. If confirmed stale: delete (untracked) or gitignore
(retained for reference); flag real-looking credential values for rotation —
never print, copy, or archive the values.

---

## Reranker and search timing

**Read the settings:**
`gbrain config get search.reranker.enabled`, `gbrain config get search.reranker.model`, `gbrain config get search.reranker.timeout_ms`, `echo $GBRAIN_QUERY_EMBED_TIMEOUT_MS`.

**Health:** `gbrain doctor 2>&1 | grep reranker_health`.

**Failure log:** `~/.gbrain/audit/rerank-failures-<year>-W<week>.jsonl`. Read the latest reasons with `tail -3 <file> | jq -r '.ts + "  " + .reason + "  " + .error_summary'`.

**Works test:** run eight searches and count new lines in the failure log. Pass is 0 new lines.

```bash
F=$(ls -t ~/.gbrain/audit/rerank-failures-*.jsonl | head -1); b=$(wc -l < $F); for q in "memory governor review queue" "cupcake grant rules" "graphify code graph" "postgres ledger port" "mb-close-out steps" "dream cycle purge" "opencode plugin loading" "sentinel review steps"; do gbrain search "$q" >/dev/null 2>&1; done; echo "new rerank failures: $(( $(wc -l < $F) - b ))"
```

**Fix by reason:**
1. `rate_limit` with "payment method": add the payment method on the billing page of the Voyage organization that holds the API key (dashboard.voyageai.com/organization/billing/payment-methods). Confirm on dashboard.voyageai.com/organization/rate-limits that `rerank-2.5` shows 2000 RPM.
2. `network` or "timed out": check the clock with `journalctl --since '-5min' --no-pager | grep -c 'Clock change detected'` (pass is 0), and check `grep '^precedence' /etc/gai.conf` shows the IPv4 line.
3. "query embed deadline exceeded": check `echo $GBRAIN_QUERY_EMBED_TIMEOUT_MS` shows `15000`.

**Do not** lower `search.reranker.timeout_ms` below `20000` or `GBRAIN_QUERY_EMBED_TIMEOUT_MS` below `15000`. **Do not** re-enable `systemd-timesyncd` in WSL.

## Authority Model

1. User decision in the current session
2. Authoritative repo files and ADRs
3. OpenCode rules and validated outputs
4. GBrain memory (advisory only)

When GBrain recall conflicts with current files, the files win. Cross-tool
authority ordering (including Graphify confidence tiers): see
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) §7.

---

## OpenCode Integration

GBrain is reached via the local MCP server (`gbrain serve`) — global
`opencode.jsonc` entry (see config.md). **MCP servers start once at OpenCode
process bootstrap** — config changes need a full process restart, not a new
chat session.

Installed skills: `/sync-gbrain` (incremental sync; `--dream` call graph;
`--code-only`; `--dry-run`) and `/setup-gbrain` (one-time setup). These follow
upstream gstack's integration shape; this environment's actual standing sync
path is the custom script (config.md). The full installed-skill inventory:
[[[mybizz-os-docs:os-reference-docs/skills-catalog|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md).

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
| Upgrade backups | `~/backups/` (private — the settings archive holds keys) |
| Cutover scripts | `C:\mybizz\scripts\cutover-block2.sh`, `cutover-block3.sh`, `cutover-rollback.sh`; `cutover-block1.sh` in `~/backups/` |
| Sync logs | `C:\mybizz\logs\gbrain-logs\sync-<timestamp>.log` |
| Frontmatter repair backups | `~/.gbrain/backups/frontmatter/` (created on first repair) |
| Schema packs | `~/.gbrain/schema-packs/` |
| Sync failure log | `~/.gbrain/sync-failures.jsonl` |
| Migration error log | `~/.gbrain/upgrade-errors.jsonl` — exists only while a migration error is pending |
| Standing sync script | `/mnt/c/mybizz/scripts/sync-gbrain.sh` |

---

## Troubleshooting

**Stale sync lock:** `gbrain sync --break-lock`.

**Links between repositories are missing after a sync:** run `gbrain extract links --source db` (see Incidents).

**Embedding fails (API key error):** source `~/.bashrc`, retry; see the
Dream Cycle reference if unresolved.

**`doctor` fails `sync_freshness` even after `gbrain sync --all`:** a source
reporting `up_to_date` gets no timestamp update; doctor's short-circuit fires
only when the working tree is clean — commit and push uncommitted changes,
then re-sync.

**Every sync ends with `Source "<id>" not found or is archived`:** the brain default names a deleted source — `gbrain config get sources.default`, then `gbrain sources default default`.

**A sync says `Could not resolve host`, or an embedding probe cannot connect:** a passing network problem; retry after a minute. The standing script does not pull.

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
- Do not call `gbrain sync` to move governed content into GBrain — only the governor's async `remember` path counts as governed ([[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md)). Sync is for the pages layer; the governed path is for the facts layer.
- Do not treat an offline test pass as live verification for anything GBrain-adjacent — the same evidence-not-proof standard as everywhere else.
- Do not upgrade GBrain on version-newness alone — an upgrade is a developer decision and follows the procedure above.
- Do not run a bare `gbrain sync` — it syncs only the source of the current folder; use `bash /mnt/c/mybizz/scripts/sync-gbrain.sh`.
- Do not rely on `gbrain extract --stale` for links between repositories — use `gbrain extract links --source db`.
- Do not use `gbrain upgrade`, `gbrain self-upgrade` or plain `gbrain apply-migrations --yes` for this install — use the procedure above.
- Do not leave `sources.default` naming a source that does not exist — every sync then fails.
- Do not remove `memory-governor-code` before the facts stored in it are understood.
- Do not re-enable the `gbrain autopilot` schedule or put the dream cycle on a scheduler — autopilot is off by decision; the dream cycle runs by hand weekly, after the Sunday backup, through the memory diagnostic ([[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Dream Cycle Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md)).
