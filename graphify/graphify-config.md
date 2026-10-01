---
title: "graphify-config"
doc-id: "mb-765e162c"
updated: "2026-10-01"
---
# Graphify Configuration

Canonical current-state configuration record. Agent-facing. States facts, not
history or rules — reasoning in [[[mybizz-config-docs:graphify/graphify-explainer|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md), commands and rules in
[[[mybizz-config-docs:graphify/graphify-reference|Graphify Reference]]](C:/mybizz/mybizz-config-docs/graphify/graphify-reference.md). All values verified live 2026-09-14 (config-management
run #1; earlier full verification 2026-09-08) unless noted.

## Identity (machine-wide install)

| Item | Value |
|---|---|
| Version | `0.9.40` (CLI and package agree) |
| Upstream latest (PyPI) | `0.9.61` (verified live 2026-09-14) — environment is behind; upgrade not performed |
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
| Repo `.gitignore` (graphify-relevant lines) | `graphify-out/`, `.opencode/`, mb-3-cs, `opencode.json`, `tests/` |
| `graphify-out/.graphify_build.json` | `{"gitignore": false}` — persisted from a prior `--no-gitignore` run; sticks until reset |
| `graphify-out/.graphify_root` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` (absolute, machine-specific) |

`.graphifyignore` does not list mb-3-cs though `.gitignore` does — no
effect (markdown is not a code-extraction target).

## Current graph state — mb-3-cs (verified live 2026-09-08)

| Item | Value |
|---|---|
| Nodes / Edges | 537 / 434 |
| Communities | 155 |
| Confidence | 417 EXTRACTED (96%) / 17 INFERRED (4%) / 0 AMBIGUOUS |
| `built_at_commit` | `59175d9e504808ab278336e70b189066a2eae7e2` |
| Live HEAD at check | same commit — graph current (rebuilt 2026-09-14 via the documented full code-only rebuild: `extract --force --code-only` + `cluster-only`, run from the repo root — see the cwd note under §Open items) |
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
| `2026-09-14/` | Auto-backup refreshed during the 2026-09-14 Tier 3 run (surviving snapshot: the post-realign, pre-rebuild state — 562 nodes; the earlier 574-node pre-realign state was overwritten by the same-day backups); machine-local, untracked |

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
| AGENTS.md (mb-3-cs) | `<!-- BEGIN GRAPH MEMORY GUIDANCE -->` … `<!-- END GRAPH MEMORY GUIDANCE -->` block, lines 102–126; encodes the graph-provenance check; single shared block for GBrain + Graphify guidance (owner: [[[mybizz-os-docs:os-reference-docs/memory-master-explainer\|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md)) |
| Git hooks / merge driver | Not installed, not registered — deliberate (decision record: [[[mybizz-config-docs:graphify/graphify-explainer\|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md)) |
| mb-3-cs project status | Paused ([[[mybizz-config-docs:opencode/opencode-config\|OpenCode Configuration]]](C:/mybizz/mybizz-config-docs/opencode/opencode-config.md)) — deployment waits on PDLF completion |
| GBrain | Never ingests `graphify-out/`; no shared backend; separate MCP servers |
| Community labels | Deterministic representative-node names (LLM labeling package `anthropic` not installed) — accepted state |

## Open items

- `--exclude` flag: absent from 0.9.40 help (re-confirmed 2026-09-14); prior suite claimed it functional — unverified in this version.
- **`built_at_commit` cwd quirk (found by the 2026-09-14 full rebuild):** `graphify extract` stamps the commit from the invoking working directory's git repo, not the scanned path — a rebuild run from another repo stamped that repo's HEAD onto this graph (caught by the procedure's provenance-confirmation step, fixed by re-running from the repo root). Rebuilds here always run from the target repo root.
- Upgrade decision open: upstream `0.9.61` / repo `v8` ships features absent in 0.9.40 (`graphify prs`, HTTP MCP transport, multi-project MCP) and recommends committing `graphify-out/` for team setups — incompatible with the standing local decision (see explainer) unless re-decided. Exam GF3-2 outcome 2026-09-14: stay on 0.9.40 (no check failed).
