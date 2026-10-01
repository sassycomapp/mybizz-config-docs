---
title: "graphify-reference"
doc-id: "mb-eda396e1"
updated: "2026-10-01"
---
# Graphify Reference

Execution reference for the installed Graphify CLI (0.9.40), verified against
`graphify --help` and live state on 2026-09-08. Current state values:
[[[mybizz-config-docs:graphify/graphify-config|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md). Why each rule exists: [[[mybizz-config-docs:graphify/graphify-explainer|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md).
Standing configuration management (2026-09-14): exam plan
[[[mybizz-config-docs:graphify/graphify-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/graphify/graphify-exam-plan.md), current verified state [[[mybizz-config-docs:graphify/graphify-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/graphify/graphify-exam-report.md),
notable events [[[mybizz-config-docs:graphify/graphify-log|Log]]](C:/mybizz/mybizz-config-docs/graphify/graphify-log.md), transient exam knowledge
[[[mybizz-config-docs:graphify/graphify-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md), exam skill source [[[mybizz-config-docs:graphify/graphify-skill|Graphify Skill]]](C:/mybizz/mybizz-config-docs/graphify/graphify-skill.md) (the installed
copy at `~/.config/opencode/skills/mb-config-graphify/SKILL.md` is the only
executing one — copy, never move).

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
| Repo-local | `.opencode/plugins/graphify.js` (bash-reminder hook; writes no files), `.opencode/opencode.json`, `.opencode/node_modules/` |

Always confirm the working directory is the target repo root before running
`graphify install` — it writes repo-scoped files relative to cwd with no
warning. Wrong-directory recovery: delete the stray
`.opencode/plugins/graphify.js` and reset `"plugin"` to `[]` in the affected
`opencode.json`.

Removal: `graphify uninstall` (all platforms; `--purge` also deletes
`graphify-out/`); per-platform: `graphify opencode uninstall`.

## Graph build

```bash
graphify extract <path> --force --code-only   # full deterministic rebuild — the default for full rebuilds here
graphify update <path>                        # re-extract changed code files only; no LLM
graphify cluster-only <path>                  # (re)generate GRAPH_REPORT.md, graph.html, labels
```

`extract` flags (0.9.40): `--backend gemini|kimi|claude|openai|deepseek|ollama`,
`--model M`, `--mode deep`, `--force` (env `GRAPHIFY_FORCE=1`),
`--max-workers N`, `--token-budget N` (default 60000), `--max-concurrency N`
(default 4), `--api-timeout S` (default 600), `--out/--output DIR`
(writes `<DIR>/graphify-out/`), `--google-workspace`, `--no-gitignore`,
`--no-cluster`, `--code-only`, `--postgres DSN` (tables/views/functions + FK
edges; no column-level detail), `--cargo`, `--global` (+ `--as <tag>`).

`cluster-only` flags: `--no-viz`, `--no-label`, `--backend=<name>`,
`--model=<name>`, `--max-concurrency=N`, `--batch-size=N`, `--graph <path>`.

Rules:

- Pass `--force` whenever a legitimate rebuild would shrink the node count —
  without it the shrink-guard refuses and writes nothing.
- `extract`/`update` alone never produce `GRAPH_REPORT.md` or `graph.html`;
  run `cluster-only` afterwards when those are wanted.
- AST extraction needs no API key, ever. Only semantic (doc/paper/image)
  extraction uses one; none is configured here.
- `extract --help` prints nothing in 0.9.40 (flags are listed under
  `graphify --help`) — do not assume flags carry over across versions.

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
- Before trusting any answer for current-state questions, check
  `jq -r '.built_at_commit' graphify-out/graph.json` equals `git rev-parse
  HEAD`; if behind, run `graphify update .` first.
- Treat EXTRACTED edges as read; verify INFERRED edges before relying on them.

## Work memory

```bash
graphify save-result --question "Q" --answer "A" --nodes N1 N2 --outcome useful|dead_end|corrected [--correction TEXT]
graphify reflect [--out FILE] [--graph PATH] [--half-life-days N] [--min-corroboration N]
graphify check-update <path>    # cron-safe needs_update check
```

`check-update` (0.9.40) is silent on success — the verdict comes from the
exit code, never stdout; its silence is not a currency claim. Graph-currency
truth stays with `built_at_commit` vs `git rev-parse HEAD`.

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
copilot vscode claw droid trae trae-cn codebuddy kilo`. `graphify opencode
install` writes an AGENTS.md section + a `tool.execute.before` plugin — not
used in this environment (manual MCP entry instead; see
[[[mybizz-config-docs:graphify/graphify-config|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md)).

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
`graph.json` is tracked — here it never is. Standing decision: not installed.

## Ignore-file mechanics

- `.graphifyignore` uses gitignore syntax; merge order is `.gitignore` first,
  `.graphifyignore` last — it can only exclude more, never re-include.
- `.graphifyignore` is honored even under `--no-gitignore` — it is the
  reliable scoping lever regardless of how a run was configured.
- A persisted `{"gitignore": false}` in `.graphify_build.json` (present in
  mb-3-cs) sticks across future `extract`/`update` runs until manually reset;
  `.graphifyignore` still applies.
- `node_modules/`, `graphify-out/`, `__pycache__/`, `.git/`, and common venv
  dirs are always skipped regardless of any ignore file.

## MCP server

```bash
python3 -m graphify.serve <path>/graphify-out/graph.json
```

Exposes 10 tools in 0.9.40 (list in [[[mybizz-config-docs:graphify/graphify-config|Graphify Configuration]]](C:/mybizz/mybizz-config-docs/graphify/graphify-config.md)); the 7 core tools
need no API key — pure networkx reads over the local `graph.json`. The CLI and
the MCP tools read the identical artifact and always agree; use either. After
adding or changing any `mcp.*` entry, a full OpenCode process restart (quit
and relaunch, not a new chat session) is required for tools to appear.

## Procedures

Full deterministic rebuild (code-only):

1. Note `git rev-parse HEAD`.
2. `graphify extract <repo-root> --force --code-only`
3. `graphify cluster-only <repo-root>` (when report/HTML/labels are wanted)
4. Confirm `jq -r '.built_at_commit' <repo>/graphify-out/graph.json` equals HEAD.

**Run steps 2–3 from inside the target repo root — always.** `graphify
extract` stamps `built_at_commit` from the invoking working directory's git
repo, not the scanned path (proven live 2026-09-14: a rebuild run from
another repo stamped that repo's HEAD onto this graph; caught by step 4).
Step 4 is mandatory, never optional.

Realign after new commits: `graphify update <repo-root>` (then `cluster-only`
if the report is wanted). Rebuild only if the source changed materially.

Wrong-directory install recovery:

1. Delete the stray `.opencode/plugins/graphify.js`.
2. Reset the plugin registration in the affected `opencode.json` to
   `{"plugin": []}`.
3. `cd` into the real repo root before re-running `graphify install`.

## Do not

- Do not run `graphify install` outside the target repo root.
- Do not trust a `path` result without `--undirected` for cross-file
  relationships.
- Do not run a shrink rebuild without `--force` — it refuses and writes
  nothing.
- Do not assume `extract`/`update` produce `GRAPH_REPORT.md`/`graph.html`.
- Do not treat INFERRED edges as settled fact.
- Do not add or change any `mcp.*` entry and expect tools without a full
  OpenCode process restart.
- Do not install hooks or the merge driver without re-examining the
  gitignore premise ([[[mybizz-config-docs:graphify/graphify-explainer|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md)) — the standing decision is
  "not installed".
- Do not track `graphify-out/` without a fresh credential-shaped scan
  (`sk-`, `AKIA`, `ghp_`, `xoxb`, PEM headers) — the standing decision is
  "gitignored".
- Do not prompt for an API key for code-only work — none exists, none is
  needed.
