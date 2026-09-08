# Graphify Configuration

Canonical current-state configuration record. Agent-facing. States facts, not
history or rules — reasoning in `graphify-explainer.md`, commands and rules in
`graphify-reference.md`. All values verified live 2026-09-08 unless noted.

## Identity (machine-wide install)

| Item | Value |
|---|---|
| Version | `0.9.40` (CLI and package agree) |
| Upstream latest (PyPI) | `0.9.56` — environment is behind; upgrade not performed |
| PyPI distribution | `graphifyy` (double-y; other `graphify*` packages unaffiliated) |
| Official repository | `github.com/Graphify-Labs/graphify` (default branch: `v8`) |
| Former URL | `github.com/safishamsi/graphify` — now serves the same org repo (alias) |
| Maintainer | Safi Shamsi (Graphify Labs) |
| Executable | `/home/dev-p/.local/bin/graphify` |
| Python module | `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` (Python 3.12.3) |
| Install method | `pip install --break-system-packages` (user site-packages) + `graphifyy[mcp]` extra (`mcp` 2.0.0) |
| Skill (OpenCode) | `~/.config/opencode/skills/graphify/` — `SKILL.md` + `references/`, version marker `.graphify_version` |
| Security scan | SkillsLLM: PASSED, no issues; scanned 2026-04-16 (pip-audit + npm-audit; no semgrep) |
| Python requirement | >= 3.10 (package metadata) |

## Install surface — what each step wrote

| Step | Wrote |
|---|---|
| Package install | CLI + module (paths above) |
| `graphify install --platform opencode`, run from mb-3-cs root | Global: `~/.config/opencode/skills/graphify/` (`SKILL.md`, `references/`). Repo-local: `.opencode/plugins/graphify.js`, `.opencode/opencode.json` (plugin registration), `.opencode/node_modules/` |
| MCP extra | `mcp` 2.0.0 into the same user site-packages |

`.opencode/plugins/graphify.js` is a `tool.execute.before` hook that prepends a
reminder string to bash commands; it writes no files of its own.

## Scope configuration — mb-3-cs

| File | Content |
|---|---|
| `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.graphifyignore` | `.opencode/` and `opencode.json` (exactly two lines; tracked in git) |
| Repo `.gitignore` (graphify-relevant lines) | `graphify-out/`, `.opencode/`, `agents.md`, `opencode.json`, `tests/` |
| `graphify-out/.graphify_build.json` | `{"gitignore": false}` — persisted from a prior `--no-gitignore` run; sticks until reset |
| `graphify-out/.graphify_root` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` (absolute, machine-specific) |

`.graphifyignore` does not list `agents.md` though `.gitignore` does — no
effect (markdown is not a code-extraction target).

## Current graph state — mb-3-cs (verified live 2026-09-08)

| Item | Value |
|---|---|
| Nodes / Edges | 574 / 468 |
| Communities | 158 |
| Confidence | 451 EXTRACTED (96%) / 17 INFERRED (4%) / 0 AMBIGUOUS |
| `built_at_commit` | `5ce243e12bc2775108c9ecad6da1e6c7f8f1614c` |
| Live HEAD at check | same commit — graph current |
| Directed | `false` (stored undirected) |
| Artifact | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json` |
| Ghost template nodes | 95 (empty `source_file`; Anvil UI templates — see explainer) |
| `tests/` | In the graph; gitignored |

## graphify-out/ inventory — mb-3-cs

| Entry | Kind |
|---|---|
| `graph.json`, `GRAPH_REPORT.md`, `graph.html`, `manifest.json` | Primary outputs |
| `.graphify_analysis.json`, `.graphify_build.json`, `.graphify_labels.json`, `.graphify_labels.json.sig`, `.graphify_root` | Build-state sidecars |
| `cache/` | Per-machine AST cache |
| `2026-08-15/` | Manual backup of the prior graph state (537 nodes, `built_at_commit` `e29cbd1b…`); machine-local, untracked |

## OpenCode MCP integration — mb-3-cs

| Item | Value |
|---|---|
| Scope | Project `opencode.json` (gitignored) |
| Entry | `mcp.graphify`, type `local`, enabled `true` |
| Command | `["/usr/bin/python3", "-m", "graphify.serve", "/mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json"]` |
| API key | None for the 7 core tools |
| Tools (10, verified in installed `serve.py`) | `graph_stats`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `shortest_path`, `query_graph` + 3 PR-triage (`list_prs`, `get_pr_impact`, `triage_prs`); prefixed `graphify_` in OpenCode |
| PR-triage tools | Unused here; require a GitHub CLI/token |

## Related integration facts

| Item | State |
|---|---|
| AGENTS.md (mb-3-cs) | `<!-- BEGIN GRAPH MEMORY GUIDANCE -->` … `<!-- END GRAPH MEMORY GUIDANCE -->` block, lines 102–126; encodes the graph-provenance check; single shared block for GBrain + Graphify guidance (owner: `mybizz-os-docs/memory-master-explainer.md`) |
| Git hooks / merge driver | Not installed, not registered — deliberate (decision record: `graphify-explainer.md`) |
| mb-3-cs project status | Paused (`opencode/opencode-config.md`) — deployment waits on PDLF completion |
| GBrain | Never ingests `graphify-out/`; no shared backend; separate MCP servers |
| Community labels | Deterministic representative-node names (LLM labeling package `anthropic` not installed) — accepted state |

## Open items

- `--exclude` flag: absent from 0.9.40 help; prior suite claimed it functional — unverified in this version.
- Upgrade decision open: upstream `0.9.56` / repo `v8` ships features absent in 0.9.40 (`graphify prs`, HTTP MCP transport, multi-project MCP) and recommends committing `graphify-out/` for team setups — incompatible with the standing local decision (see explainer) unless re-decided.
