# Graphify Reference

## What This Is

A local, deterministic code and document knowledge-graph builder —
`github.com/safishamsi/graphify`. Uses Tree-sitter for real code (AST
parsing, zero LLM calls) and subagent-dispatched semantic extraction for
documents (markdown, HTML-as-document). Independent of GStack, GBrain, Matt
Pocock's skills, and Anvil's skills.

For the exact current install paths, ignore-file contents, MCP entry, and
graph statistics for the `mb-3-cs` project specifically, see
`graphify-config.md`. This document covers general Graphify mechanics and
command behavior, applicable across projects.

---

## Real, Authoritative Sources

- **Source repo:** `github.com/safishamsi/graphify` — the only official
  repository (stated in the project's own README).
- **PyPI package:** `graphifyy` (double-y, deliberately, to distinguish from
  unofficial impersonator packages) — `pypi.org/project/graphifyy`.
- **Organization:** `github.com/Graphify-Labs/graphify`.
- **Independent security scan:** `skillsllm.com/skill/graphify` — passed, no
  high-severity issues.
- **Maintainer:** Safi Shamsi, Graphify Labs, London.

---

## Install — Two Separate Steps, Different Scope

### Step 1 — The package itself (machine-wide, once)

```bash
pip install graphifyy --break-system-packages
```

Installs the `graphify` CLI (e.g. `/home/dev-p/.local/bin/graphify`). Not
per-project — one install covers the whole machine.

### Step 2 — Per-repo activation (run once per repo that needs it)

**Run this from inside the target repo's root — not from your home
directory.** This is the single most important operational fact about
Graphify's install process: it writes real, repo-scoped files relative to
whatever the current directory happens to be, with no warning if that
directory isn't actually a real project.

```bash
cd <target-repo-root>
graphify install --platform opencode
```

This writes, in two different scopes:

| Scope | What gets written |
|---|---|
| Global (`~/.config/opencode/skills/graphify/`) | `SKILL.md`, `references/` — shared across every repo, not duplicated per-project |
| Repo-local (inside the target repo) | `.opencode/plugins/graphify.js` (a `tool.execute.before` hook), `.opencode/opencode.json` (plugin registration), a full `node_modules/` tree (needed to actually execute the plugin locally) |

**The plugin (`.opencode/plugins/graphify.js`) writes no files of its own.**
It only prepends a reminder string to bash commands passing through
`tool.execute.before`. Do not mistake it for an active graph-mutation
mechanism — it's a text hint, nothing more.

### MCP extra (separate step, needed for the MCP server)

```bash
python3 -m pip install --user "graphifyy[mcp]" --break-system-packages
```

Without this, `python3 -m graphify.serve <graph.json>` fails with
`ModuleNotFoundError: No module named 'mcp'`. `pip install` without
`--break-system-packages` will be rejected by PEP 668
(`externally-managed-environment`) on most modern distros — this flag is
expected and safe here, confined to the same user site-packages where
`graphifyy` itself already lives.

### Real incident, kept for recognition — installing from the wrong directory

Running the per-repo install command from the home directory instead of a
project folder writes its plugin registration directly into whatever
`~/.opencode/` happens to already contain — potentially a leftover,
unrelated OpenCode scaffold from months earlier. Confirm the working
directory before running `graphify install`, every time. If it happens
anyway: remove the erroneously-written `.opencode/plugins/graphify.js`, and
reset any dangling plugin reference in the affected `opencode.json` to an
empty array (`{"plugin": []}`).

---

## Real Finding — Graphify Is Not Code-Only

Graphify has **two genuinely different extraction paths**, not one:

| Path | Applies to | Mechanism | LLM cost |
|---|---|---|---|
| AST | Real code files | Tree-sitter structural parsing | None |
| Semantic | Markdown, HTML-as-document, images | Subagent dispatch (or a vision backend for images, if configured) | Real, per-file |

A repo with zero code files and only markdown/HTML/images can still produce
a real, substantive extraction plan — don't assume Graphify has nothing to
offer a docs-only repo just because it has no code. Without a
`GEMINI_API_KEY`/`GOOGLE_API_KEY`, image files are silently skipped (no
vision backend available), and markdown/HTML semantic extraction falls back
to the host agent's own subagent dispatch mechanism rather than a dedicated
model call.

`.html` and `.yaml`/`.yml` are always classified as **document (semantic)**
types, never code — there is no plain-HTML or YAML AST extractor (the
code-with-embedded-HTML extractors like `.cshtml`/`.razor`/`.vue`/`.astro`
are a different thing entirely, and don't apply to plain templates). Any UI
templating layer built on raw HTML/YAML (e.g. Anvil form templates) will
never appear as extracted, structured content under a `--code-only` run —
only as "ghost" name references pulled from whatever code does reference
them (e.g. a Python class name), with an empty `source_file`.

---

## Command Reference

### `extract` — headless full extraction (AST + optional semantic)

```
extract <path>
    --backend B              gemini|kimi|claude|openai|deepseek|ollama (default: whichever API key is set)
    --model M                override backend default model
    --mode deep              aggressive INFERRED-edge semantic extraction
    --force                  full re-scan and re-dispatch; required if the rebuild would shrink node count (bypasses a shrink-guard)
    --out DIR, --output DIR  output dir (default: <path>); writes <DIR>/graphify-out/
    --no-gitignore           ignore .gitignore and .git/info/exclude (prioritizes .graphifyignore, which is still honored)
    --no-cluster             skip clustering, write raw extraction only
    --code-only              index code (local AST, no API key) and skip doc/paper/image files entirely
    --postgres DSN           extract schema from a live PostgreSQL database
    --global                also merge the resulting graph into the global graph (mutates ~/.graphify/global-graph.json — use deliberately)
    --exclude <pattern>      repeatable exclude flag; functional but not shown in `extract --help`'s usage line
```

**AST extraction is deterministic and free — no LLM, no API key, at all**,
for a code-only corpus. Semantic extraction (markdown/HTML/images) is real
LLM work with real token cost.

**`extract` in current versions does NOT produce `GRAPH_REPORT.md` or
`graph.html`.** Only `graph.json` and `.graphify_analysis.json`. Run
`cluster-only` afterward for the human-facing report and HTML view.

### `update <path>` — realign an existing graph, cheaper than a full rebuild

Use after commits have advanced past the graph's stored `built_at_commit`,
when the underlying source hasn't changed enough to warrant a full
`extract --force` re-scan. Same flag surface as `extract` for the relevant
options.

### `cluster-only <path>` — generate report, HTML, and community labels

Re-clusters and labels an **existing** graph without re-extracting; does not
change node/edge counts. Produces `GRAPH_REPORT.md`, `graph.html`, updates
`graph.json` with labels, `.graphify_labels.json`,
`.graphify_labels.json.sig`.

LLM-based community labeling requires the backend's Python package to be
installed (e.g. `anthropic` for the `claude`/`anthropic` backend) — an
`ANTHROPIC_API_KEY` being present is not sufficient by itself if the package
isn't. Failure here is handled gracefully: it falls back to deterministic
representative-node names (the most-connected/most-cited node in each
community) at zero token cost, with no partial or corrupted output. This is
often an acceptable permanent state, not necessarily something to fix.

### `path "<source>" "<target>" [--graph path] [--directed|--undirected]`

**Defaults to directed traversal even when the underlying graph is stored
undirected** (`directed: false` in `graph.json`). This produces misleading
"No directed path found" results for relationships that are real but only
exist in reverse-structural form (e.g. `moduleA` → `contains` → `funcX`,
`moduleA` → `imports` → `funcY`, meaning `funcX` and `funcY` are related via
the shared module, but not by a direct call edge in either direction).
**Always pass `--undirected` explicitly** when checking a cross-file or
non-obvious relationship — confirmed via a real cross-check against source
(`get_vault_secret` → `encrypt`: directed search reported no path; the same
undirected search correctly returned the 2-hop `contains`/`imports` path
that matches the actual source code exactly).

Node matching is case-folded substring against node labels.

### `god-nodes` / `query` / `diagnose multigraph`

Structural sanity and hub-identification commands, run against an existing
`graph.json`. Version-dependent syntax — check `--help` before use on an
unfamiliar version rather than assuming flags carry over.

### `hook install` / `hook uninstall` / `hook status`

Installs (or removes) **three things together, unconditionally — no flag to
split them:**
1. A `post-commit` hook — detached background rebuild after every commit
   that touches non-`graphify-out/` files (skips rebase/merge/cherry-pick,
   skips linked worktrees, honors `GRAPHIFY_SKIP_HOOK=1`).
2. A `post-checkout` hook — detached full rebuild on branch switches (not
   file-level checkouts), only if `graphify-out/` already exists.
3. A `graph.json` union **merge driver** — registers `merge.graphify.*` in
   local git config and **appends a new line to `.gitattributes`**, creating
   that file if it doesn't exist.

Both hooks are non-blocking (detached background process; a watchdog caps
runaway rebuilds) and fail silently to stderr if Graphify's Python can't be
located — a commit or checkout is never blocked by a missing interpreter.

**Important: the merge driver is dead weight if `graphify-out/` is
gitignored** (the normal, recommended state — see `graphify-config.md`).
Since the tracked graph file this driver would resolve conflicts on is
never actually tracked, the driver can never fire — but installing it still
creates a new tracked `.gitattributes` file and local git-config entries for
no benefit. There's no flag to install the useful half (auto-refresh) without
the merge-driver half. Before installing hooks on any project, weigh this
tradeoff explicitly rather than installing by default.

`hook uninstall` removes both hook blocks (preserving any other, unrelated
hook content via marker-delimited sections), unregisters the merge driver,
and removes the `.gitattributes` line (deleting the file if left empty).

### Output folder

`graphify-out/` — `graph.html`, `GRAPH_REPORT.md`, `graph.json`,
`.graphify_analysis.json`, `manifest.json`, `.graphify_labels.json[.sig]`,
`.graphify_build.json`, `cache/` (per-machine AST cache), `.graphify_root`
(an absolute path — machine-specific). **Add this folder to `.gitignore`.**
It's fully reproducible from the committed source tree at zero API cost
(code-only path), and mixes machine-specific artifacts with derived output
that goes stale relative to future commits.

---

## `.graphifyignore` vs `.gitignore`

- `.graphifyignore` uses the full gitignore glob syntax (blank lines/`#`
  comments ignored, `!` negation with last-match-wins, `**` recursive, `/`
  anchoring, etc.).
- Merge order: `.gitignore` is read first, `.graphifyignore` last —
  `.graphifyignore` can only exclude *more*, never re-include something
  `.gitignore` excluded (standard parent-exclusion rule applies).
- **`.graphifyignore` is honored even when `--no-gitignore` is passed** —
  with `gitignore: false`, only `.graphifyignore` is read, not `.gitignore`.
  This means `.graphifyignore` is the correct, reliable lever for scoping a
  graph regardless of whatever `--no-gitignore` setting a given extraction
  run used.
- A persisted `{"gitignore": false}` in `.graphify_build.json` (from a prior
  `--no-gitignore` run) sticks across future runs of `extract`/`update`
  unless manually reset — `.graphifyignore` still applies regardless, so
  this is usually not worth actively correcting.
- `node_modules/`, `graphify-out/` itself, `__pycache__/`, `.git/`, and
  common venv directories are auto-excluded by Graphify's own hardcoded
  skip-list (`_SKIP_DIRS`) regardless of any ignore file — even
  `--no-gitignore` does not pull these back in.

---

## Security and Content Notes

- Graph output (`graph.json`, `graph.html`, `manifest.json`,
  `.graphify_analysis.json`, `.graphify_labels.json[.sig]`, `cache/`) should
  be scanned for secrets before ever considering it for git tracking — in
  practice, code identifiers containing words like "secret" or "password"
  (function names, class names, docstrings) are extremely common and almost
  always benign; look specifically for credential-shaped strings (`sk-`,
  `AKIA`, `ghp_`, `xoxb`, PEM headers, embedded URLs with passwords), not
  just the word "secret" itself.
- `source_file` fields in `graph.json` are repo-relative by design —
  portable. The only absolute-path leakage is in the machine-specific
  `.graphify_root` file and the human-readable header line of
  `GRAPH_REPORT.md`.
- `graph.html` is self-contained aside from one external CDN dependency
  (`unpkg.com/vis-network`), which is SRI-pinned — safe, but requires
  network access to actually render.

---

## OpenCode MCP Integration

Server command: `python3 -m graphify.serve <path>/graphify-out/graph.json`
(module `graphify/serve.py`). Exposes 10 tools: `graph_stats`, `get_node`,
`get_neighbors`, `get_community`, `god_nodes`, `shortest_path`,
`query_graph`, plus 3 PR-triage tools (`list_prs`, `get_pr_impact`,
`triage_prs` — require a GitHub CLI/token; unrelated to the core graph
queries). No API key required for the 7 core tools — pure `networkx` reads
over the local `graph.json`.

**MCP servers start once, at OpenCode process bootstrap — not per chat
session.** Adding a new `mcp.*` entry to config while OpenCode is already
running will not surface that server's tools in a new chat session within
the same running process. Confirmed directly via log analysis: a config
change made mid-session left the corresponding server entirely absent from
every subsequent chat session until the OpenCode process itself was fully
quit and relaunched. **A full process restart is required, every time a new
local MCP server is added or an existing one's command changes** — this is
a general OpenCode behavior, not specific to Graphify.

Two independent binaries provide the same underlying data by two different
paths — the CLI (`graphify path`, `graphify god-nodes`, etc., against
`graphify-out/graph.json` directly) and the MCP tools (`graph_stats`,
`get_node`, etc., against the same file via the running server). They will
always agree, since both read the identical artifact; use whichever is more
convenient in context.

---

## GBrain vs Graphify — Tool Boundary

No name overlap between the two tool sets (`gbrain_*` vs the Graphify MCP
tools). They read from entirely separate backends (Postgres DB vs a local
`graph.json` file) and never write to each other — Graphify never modifies
the GBrain database, and GBrain does not ingest `graphify-out/` content (it
is, appropriately, gitignored and not a GBrain source). For a full
explanation of when to use which, see `memory-explainer.md`; in short:
**Graphify is authoritative for current, resolved, structural code
relationships; GBrain is authoritative for decisions, rationale, history,
and cross-project search.**

---

*End of document*
