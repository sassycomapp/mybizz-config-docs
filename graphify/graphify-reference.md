---
title: "graphify-reference"
doc-id: "mb-eda396e1"
updated: "2026-10-20"
---
# Graphify Reference

Execution reference for the installed Graphify CLI. State values:
[[[mybizz-config-docs:graphify/graphify-config|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md). Why each rule exists:
[[[mybizz-config-docs:graphify/graphify-explainer|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md). Differences from the issuer
standard: [[[mybizz-config-docs:graphify/graphify-learnings|Graphify Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md).

## Install

```bash
# Machine-wide package (once per machine)
pip install graphifyy --break-system-packages

# Per-repo activation — run from inside the target repo root
graphify install --platform opencode

# MCP extra — without it, `python3 -m graphify.serve` fails (ModuleNotFoundError: mcp)
python3 -m pip install --user "graphifyy[mcp]" --break-system-packages
```

Activation writes:

| Scope | Files |
|---|---|
| Global | `~/.config/opencode/skills/graphify/` — `SKILL.md`, `references/` |
| Repo-local | `.opencode/plugins/graphify.js` (bash-reminder hook; writes no files), `.opencode/opencode.json` (plugin registration), `.opencode/node_modules/` |

The OpenCode integration MyBizz uses is the manual `mcp.graphify` entry in
each repository's root `opencode.json` (L2) — not the plugin registration.

Confirm the working directory is the target repo root before running
`graphify install` — it writes repo-scoped files relative to cwd with no
warning. Wrong-directory recovery: delete the stray
`.opencode/plugins/graphify.js`; reset `"plugin"` to `[]` in the affected
`opencode.json` where a registration exists; `cd` into the intended repo root
and re-run.

Removal: `graphify uninstall` (all platforms; `--purge` also deletes
`graphify-out/`); per-platform: `graphify opencode uninstall`.

## Graph build

```bash
graphify extract <path> --force --code-only   # full deterministic rebuild
graphify update <path>                        # re-extract the repo's code files onto the graph; no LLM
graphify cluster-only <path>                  # (re)generate GRAPH_REPORT.md, graph.html, labels
```

`extract` flags: `--backend gemini|kimi|claude|openai|deepseek|ollama`,
`--model M`, `--mode deep`, `--force` (env `GRAPHIFY_FORCE=1`),
`--max-workers N`, `--token-budget N` (default 60000), `--max-concurrency N`
(default 4), `--api-timeout S` (default 600), `--out/--output DIR`
(writes `<DIR>/graphify-out/`), `--google-workspace`, `--no-gitignore`,
`--no-cluster`, `--code-only`, `--postgres DSN` (tables/views/functions + FK
edges; no column-level detail), `--cargo`, `--global` (+ `--as <tag>`).

`update` flags: `--force`, `--no-cluster`.

`cluster-only` flags: `--no-viz`, `--no-label`, `--backend=<name>`,
`--model=<name>`, `--max-concurrency=N`, `--batch-size=N`, `--graph <path>`.

Rules:

- Build and refresh with `--code-only` only; no AI backend and no API key is
  involved (L1).
- Refresh a repository's graph after every code commit:
  `cd <repo> && graphify update <repo>`.
- Run every `extract`/`update` from inside the target repo root — `extract`
  stamps `built_at_commit` from the invoking working directory's git repo,
  not the scanned path (L3).
- Pass `--force` whenever a legitimate rebuild would shrink the node count —
  without it the shrink-guard refuses and writes nothing.
- AST extraction needs no API key, ever. Only semantic (doc/paper/image)
  extraction uses one; none is configured here.
- `extract --help` prints one pointer line ("Run 'graphify --help' for full
  usage."); flags are listed under `graphify --help` — do not assume flags
  carry over across versions.

## Query surface

All accept `--graph <path>` (default `graphify-out/graph.json`):

```bash
graphify query "<question>" [--dfs] [--context R]... [--budget N]   # BFS default; --budget default 2000
graphify path "A" "B" [--directed|--undirected]
graphify explain "X"
graphify affected "X" [--relation R]... [--depth N]                 # reverse traversal; default depth 2
graphify god-nodes [--top N] [--json]
graphify tree [--root PATH] [--output HTML] [--max-children N] [--top-k-edges N] [--label NAME]
```

- Always pass `--undirected` to `path` for cross-file or reverse
  relationships; the directed default returns "no path found" on real edges.
- `path` matching is case-folded substring against node labels.
- Before trusting any answer for a current-state question, check
  `jq -r '.built_at_commit' graphify-out/graph.json` equals `git rev-parse
  HEAD`; if behind, run `graphify update .` first.
- Treat EXTRACTED edges as read; verify INFERRED edges before relying on
  them.

## Work memory

```bash
graphify save-result --question "Q" --answer "A" --nodes N1 N2 --outcome useful|dead_end|corrected [--correction TEXT]
graphify reflect [--out FILE] [--graph PATH] [--half-life-days N] [--min-corroboration N]
graphify check-update <path>    # cron-safe needs_update check
```

`check-update` is silent on success — the verdict comes from the exit code,
never stdout; its silence is not a currency claim. Graph-currency truth stays
with `built_at_commit` vs `git rev-parse HEAD`.

## Graph management

```bash
graphify merge-graphs <g1> <g2> [--out PATH]
graphify merge-driver <base> <current> <other>       # union merge; registered by hook install
graphify global add <graph.json> [--as TAG]          # merge a project graph into ~/.graphify/global-graph.json
graphify global remove <tag> | global list | global path
graphify diagnose multigraph [--json] [--max-examples N] [--directed|--undirected] [--extract-path PATH]
graphify benchmark [graph.json]
graphify export callflow-html
graphify clone <github-url> [--branch B] [--out DIR]
graphify add <url> [--author "Name"] [--contributor "Name"] [--dir <path>]
graphify watch <path>                                # rebuild on file changes
```

Platform registration: `graphify install [--platform P]`; per-platform
`<platform> install|uninstall` for `claude codex opencode cursor gemini aider
copilot vscode claw droid trae trae-cn codebuddy kilo antigravity hermes kiro
pi devin`. `install --platform` also accepts `windows amp agents` (no
per-platform subcommands). `graphify opencode install` writes an AGENTS.md
section + a `tool.execute.before` plugin — not used in this environment
(manual MCP entry instead; L2).

## Hooks and merge driver

```bash
graphify hook install | hook uninstall | hook status
```

`hook install` adds three things together, with no flag to split them:
post-commit hook (detached background rebuild; skips rebase/merge/cherry-pick,
linked worktrees; honors `GRAPHIFY_SKIP_HOOK=1`), post-checkout hook (full
rebuild on branch switches, only if `graphify-out/` exists), and a `graph.json`
union merge driver (registers `merge.graphify.*` in local git config and
creates/appends `.gitattributes`). The merge driver only ever matters if
`graph.json` is tracked — here it never is. Not installed (L4); reasons in
[[[mybizz-config-docs:graphify/graphify-explainer|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md).

## Ignore-file mechanics

- `.graphifyignore` uses gitignore syntax; merge order is `.gitignore` first,
  `.graphifyignore` last — it can only exclude more, never re-include.
- `.graphifyignore` is honored even under `--no-gitignore` — it is the
  reliable scoping lever regardless of how a run is configured.
- A persisted `{"gitignore": false}` in `.graphify_build.json` (present in
  mb-3-cs-app1) sticks across future `extract`/`update` runs until manually
  reset; `.graphifyignore` still applies.
- `node_modules/`, `graphify-out/`, `__pycache__/`, `.git/`, and common venv
  dirs are always skipped regardless of any ignore file.

## MCP server

```bash
python3 -m graphify.serve <repo>/graphify-out/graph.json
```

Exposes 10 tools (list in
[[[mybizz-config-docs:graphify/graphify-config|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md)); the 7 core tools need no API
key — pure networkx reads over the local `graph.json`. The CLI and the MCP
tools read the identical artifact and always agree; use either. After any add
or edit to an `mcp.*` entry, a full OpenCode process restart (quit and
relaunch, not a new chat session) is required for tools to appear.

## Procedures

Refresh after a commit (per repository):

1. `cd <repo>`
2. `graphify update <repo>`
3. Confirm `jq -r '.built_at_commit' <repo>/graphify-out/graph.json` equals
   `git -C <repo> rev-parse HEAD`.

Full deterministic rebuild (code-only):

1. Note `git rev-parse HEAD`.
2. From inside the target repo root: `graphify extract <repo-root> --force
   --code-only`
3. `graphify cluster-only <repo-root>` when the report, HTML or labels need
   regeneration.
4. Confirm `built_at_commit` equals HEAD. Mandatory, never optional.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| CLI help | `graphify --help` (local command) | 0.9.40 | 2026-10-20 |
| PyPI package page | https://pypi.org/project/graphifyy/ | 0.9.40 | 2026-10-20 |
| Source repository | https://github.com/Graphify-Labs/graphify (branch `v8`) | 0.9.40 | 2026-10-20 |
| Installed MCP server | `/home/dev-p/.local/lib/python3.12/site-packages/graphify/serve.py` | 0.9.40 | 2026-10-20 |
| Installed skill | `~/.config/opencode/skills/graphify/SKILL.md` | 0.9.40 | 2026-10-20 |
| MyBizz skills catalog | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills-catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | — | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `graphify --version` | agent |
| Scope artifacts (per repo) | `test -f` on `.graphifyignore`, `graphify-out/.graphify_root`, `graphify-out/graph.json`; `cat graphify-out/.graphify_root` | agent |
| Graph currency (per repo) | `jq -r '.built_at_commit' <repo>/graphify-out/graph.json` equals `git -C <repo> rev-parse HEAD` | agent |
| MCP entry (per repo) | `jq -c '.mcp.graphify' <repo>/opencode.json` | agent |
| Hooks not installed | `graphify hook status` (inside a repo) | agent |
| Works (CLI) | `graphify god-nodes --top 3 --graph <repo>/graphify-out/graph.json` | agent |
| Works (MCP) | Fully quit and relaunch OpenCode in a repository; the 10 `graphify_` tools appear | developer |

## Do not

- Do not run `graphify install` outside the target repo root.
- Do not build or refresh with any `--backend`/`--model` path, and do not run
  `graphify label` — the setup is code-only; those paths call LLM backends (L1).
- Do not run an `extract`/`update` from outside the target repo root (L3).
- Do not trust a `path` result without `--undirected` for cross-file
  relationships.
- Do not run a shrink rebuild without `--force` — it refuses and writes
  nothing.
- Do not treat INFERRED edges as settled fact.
- Do not add or edit an `mcp.*` entry and expect tools without a full
  OpenCode process restart.
- Do not install hooks or the merge driver (L4).
- Do not track `graphify-out/` in git (reasons in
  [[[mybizz-config-docs:graphify/graphify-explainer|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md)).
- Do not prompt for an API key for code-only work — none exists, none is
  needed (L1).
