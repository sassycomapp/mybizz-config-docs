# Graphify Configuration — mb-3-cs

Canonical current-state configuration record. Agent-facing. Reflects the
working state of Graphify as integrated into the `mb-3-cs` project as of the
end of the setup/closeout sequence (2026-08-16). This document states facts,
not history — where a decision was made and the reasoning matters, see
`memory-explainer.md`.

---

## Identity

| Item | Value |
|---|---|
| Version | `0.9.40` |
| PyPI distribution | `graphifyy` (double-y — deliberate, distinguishes from unofficial packages) |
| Source repo | `github.com/safishamsi/graphify` |
| Executable | `/home/dev-p/.local/bin/graphify` |
| Python module | `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` (Python 3.12.3) |

## Install (two-step — both required, in order)

1. Machine-wide (once per machine): `pip install graphifyy --break-system-packages`
2. Per-repo activation (once per repo, **must be run from inside the target repo root**):
   ```bash
   cd /mnt/c/dev/dev-mb-3-cs/mb-3-cs
   graphify install --platform opencode
   ```
   Running this from the wrong directory silently writes real repo-scoped
   files relative to the current directory with no warning — always confirm
   the working directory first.

MCP extra (separate, required for the MCP server to run):
```bash
python3 -m pip install --user "graphifyy[mcp]" --break-system-packages
```

### Files written by per-repo activation

| Scope | Location | Contents |
|---|---|---|
| Global | `~/.config/opencode/skills/graphify/` | `SKILL.md`, `references/` — shared across all repos |
| Repo-local | `.opencode/plugins/graphify.js` | `tool.execute.before` hook; **writes no files** — only prepends a bash-command reminder string |
| Repo-local | `.opencode/opencode.json` | plugin registration |
| Repo-local | `.opencode/node_modules/` | required to execute the plugin locally |

## Scope configuration (committed to the repo)

`.graphifyignore` — exactly two lines:
```
.opencode/
opencode.json
```

`.gitignore` — includes the line `graphify-out/` (added; whole output
directory untracked). `.graphifyignore` is honored regardless of whether
`.gitignore` itself is being honored by a given extraction run.

Only `.graphifyignore` is a tracked file. Nothing under `graphify-out/` is
committed.

## Canonical build commands

**Full deterministic rebuild** (code-only, no LLM, no API key — the default
command for any full rebuild):
```bash
graphify extract /mnt/c/dev/dev-mb-3-cs/mb-3-cs --force --code-only
```
`--force` is required whenever the rebuild would shrink the node count
(bypasses Graphify's shrink-guard). Output defaults to `<path>/graphify-out/`.

**Realign an existing graph to a new HEAD** (cheaper than a full rebuild when
the source hasn't materially changed):
```bash
graphify update /mnt/c/dev/dev-mb-3-cs/mb-3-cs
```

**Generate `GRAPH_REPORT.md` + `graph.html` + community labels** (does not
change node/edge counts; required after any `extract`/`update` if these two
files are wanted — they are not produced by `extract`/`update` alone in this
version):
```bash
graphify cluster-only /mnt/c/dev/dev-mb-3-cs/mb-3-cs
```
LLM community-name labeling requires the `anthropic` pip package (not
installed). Without it, this falls back cleanly to deterministic
representative-node names at zero token cost — accepted as-is.

## Current graph state (last verified)

| Item | Value |
|---|---|
| Nodes | 574 |
| Edges | 468 |
| Communities | 158 |
| Confidence | 96% EXTRACTED / 4% INFERRED / 0% AMBIGUOUS |
| `built_at_commit` | `5ce243e12bc2775108c9ecad6da1e6c7f8f1614c` |
| Directed | `false` (stored undirected) |
| Artifact path | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json` |

**Provenance check:** `built_at_commit` must equal the live repo's current
`git rev-parse HEAD` for the graph to be trusted as current. If the repo has
advanced past this commit, run `graphify update .` before relying on the
graph for anything current-state-dependent.

**Query note:** `graphify path`/`shortest_path` defaults to directed
traversal even though the graph is stored undirected. Always pass
`--undirected` explicitly when checking a cross-file or reverse relationship,
or a real, correctly-captured relationship can appear to return "no path
found." See `graphify-reference.md` for the confirmed example.

## Known scope limitations (accepted, not defects)

- **Anvil UI templates (`.html`/`.yaml` form templates) are not structurally
  extracted.** These are DOC types, not CODE types, in Graphify's detector;
  no plain-HTML/YAML AST extractor exists. ~95 graph nodes are "ghost"
  template-class references (empty `source_file`) as a direct, understood
  consequence. Including them would require switching to semantic (LLM)
  extraction — not currently in use; not required unless a future decision
  changes this.
- `tests/` **is** included in the graph even though it's git-ignored — this
  was a deliberate choice, not an oversight.

## OpenCode MCP integration

| Item | Value |
|---|---|
| Scope | project `opencode.json` (gitignored) |
| Entry | `mcp.graphify` |
| Type | `local` |
| Command | `["/usr/bin/python3", "-m", "graphify.serve", "/mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json"]` |
| Enabled | `true` |
| API key required | none for the 7 core tools |

Exposed MCP tools (10, prefixed `graphify_*` in OpenCode): `graph_stats`,
`get_node`, `get_neighbors`, `get_community`, `god_nodes`, `shortest_path`,
`query_graph`, plus 3 unused PR-triage tools (`list_prs`, `get_pr_impact`,
`triage_prs`).

**Mechanical note — MCP server startup timing:** OpenCode spawns configured
local MCP servers once, at process bootstrap, not per chat session. If
`mcp.graphify` is added or changed while OpenCode is already running, its
tools will **not** appear even in a brand-new chat session — a full process
restart (fully quit and relaunch `opencode web`) is required. This applies
to any future MCP configuration change, not just Graphify.

## Git hooks and merge driver

**Deliberately not installed.** `graphify hook install` would add a
post-commit hook, a post-checkout hook, and a `graph.json` union merge
driver (requiring a new tracked `.gitattributes` file plus local git-config
entries). Declined because the merge driver is dead weight — `graphify-out/
graph.json` is fully gitignored and can never actually be merged — yet
installing it still adds tracked-file and config-churn overhead with no
corresponding benefit. Standing practice: refresh manually with `graphify
update .` when currency matters. This decision was deliberate (not a
default/oversight) and should not be silently reversed.

## Do not

- Do not install `.git` hooks or the merge driver without re-confirming the WP13 reasoning above no longer applies — specifically, the reasoning depends on `graphify-out/` staying gitignored; if that ever changes (the artifact becomes tracked), the hooks decision must be explicitly re-examined, not silently left as-is or silently reversed.
- Do not run a rebuild without `--force` if it's expected to shrink the node count — it will refuse.
- Do not assume `graphify extract`/`update` alone produces `GRAPH_REPORT.md`/`graph.html` — run `cluster-only` afterward.
- Do not trust `graphify path` results without `--undirected` when checking cross-file relationships.
- Do not add `mcp.graphify` (or any MCP entry) and expect it to work without a full OpenCode process restart.
