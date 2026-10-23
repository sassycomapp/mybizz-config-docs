---
title: "graphify-config"
doc-id: "mb-765e162c"
updated: "2026-10-23"
---
# Graphify Configuration

Canonical current-state record: what exists and what each thing is set to.
Commands and rules: [[[mybizz-config-docs:graphify/graphify-reference|Graphify Reference]]](C:/mybizz/mybizz-config-docs/graphify/graphify-reference.md). Reasons:
[[[mybizz-config-docs:graphify/graphify-explainer|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md). Differences from the issuer
standard: [[[mybizz-config-docs:graphify/graphify-learnings|Graphify Learnings]]](C:/mybizz/mybizz-config-docs/graphify/graphify-learnings.md).

## Identity

| Field | Value |
|---|---|
| Issuer | Graphify Labs |
| Installed version | `0.9.40` (CLI and package agree) |
| Standard taken from | 0.9.40 |
| Last researched | 2026-10-20 |

## Install

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| PyPI distribution | `graphifyy` (other `graphify*` packages are unaffiliated) | `graphifyy` | https://pypi.org/project/graphifyy/ | |
| Official repository | `github.com/Graphify-Labs/graphify` (default branch `v8`) | Same | https://github.com/Graphify-Labs/graphify | |
| Maintainer | Safi Shamsi (Graphify Labs) | Same | https://github.com/Graphify-Labs | |
| Executable | — | `/home/dev-p/.local/bin/graphify` | — | |
| Python module | — | `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` (Python 3.12.3) | — | |
| Install method | — | `pip install graphifyy --break-system-packages` (user site-packages) + `graphifyy[mcp]` extra (`mcp` 2.0.0) | — | |
| Python requirement | >= 3.10 | 3.12.3 in use | Package metadata | |
| OpenCode skill | `~/.config/opencode/skills/graphify/` — `SKILL.md`, `references/`, version marker `.graphify_version` | Present at the standard location | `graphify install --platform opencode` | |
| Skills catalog row | — | Vendor skill, Operational; the installed copy is its own source | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills-catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | |
| API key | Needed only for semantic (doc/paper/image) extraction | None configured | `graphify --help` (extract) | L1 |

## Scope — repositories

Scope is six app repositories, three per project. Each repository holds a
code graph under `graphify-out/`, its own `.graphifyignore`, and a
`.graphify_root` marker holding its own absolute path.

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| mb-3-cs repositories | — | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-app1`, `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-app3`, `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-app5` | — | |
| mb-4-ecom repositories | — | `/mnt/c/dev/dev-mb-4-ecom/mb-4-ecom-app1`, `/mnt/c/dev/dev-mb-4-ecom/mb-4-ecom-app3`, `/mnt/c/dev/dev-mb-4-ecom/mb-4-ecom-app5` | — | |
| Repositories outside scope | — | The `app2` repository of each project (holds no graphify artifacts) | — | |
| `.graphifyignore` (all six) | gitignore syntax, user-defined | `.opencode/` and `opencode.json` (two lines; tracked in git) | — | |
| `.graphify_root` (all six) | — | Holds the repository's own absolute path | — | |
| Repository `.gitignore` (graphify lines) | — | `.opencode/`, `agents.md`, `opencode.json`, `graphify-out/`; mb-3-cs-app1 also `tests/` | — | |
| `graphify-out/.graphify_build.json` | — | `{"gitignore": false}` in mb-3-cs-app1; absent in the other five | — | |

## Build

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Extraction mode | `--backend` auto-detects from API keys; semantic extraction available | `--code-only`: local AST extraction, no AI backend, no API key, no model calls | `graphify --help` (extract) | L1 |
| Community labels | LLM naming via `--backend`/`--model` (`label`, `cluster-only`) | Deterministic representative-node names (no labeling backend installed) | `graphify --help` | L1 |
| Graph refresh | Manual command; optional `watch` or post-commit-hook automation | Manual refresh after every code commit in the repository | `graphify --help` | L4 |
| Storage | — | `directed: false` (undirected) in all six graphs | — | |

## Graph state — six repositories

`built_at_commit` equals the repository HEAD in all six graphs. Confidence
labels: EXTRACTED (read from syntax), INFERRED (the tool's guess), AMBIGUOUS
(unresolved). Ghost nodes are empty-`source_file` name references from Anvil
UI templates the extractor cannot structurally parse.

| Repository | Nodes | Links | Confidence | Communities | Ghost nodes |
|---|---|---|---|---|---|
| mb-3-cs-app1 | 566 | 460 | 443 EXTRACTED / 17 INFERRED | 158 | 96 |
| mb-3-cs-app3 | 10 | 6 | 6 EXTRACTED | 4 | 2 |
| mb-3-cs-app5 | 10 | 6 | 6 EXTRACTED | 4 | 2 |
| mb-4-ecom-app1 | 10 | 6 | 6 EXTRACTED | 4 | 2 |
| mb-4-ecom-app3 | 10 | 6 | 6 EXTRACTED | 4 | 2 |
| mb-4-ecom-app5 | 10 | 6 | 6 EXTRACTED | 4 | 2 |

## graphify-out/ contents

| Entry | Presence |
|---|---|
| `graph.json`, `GRAPH_REPORT.md`, `manifest.json`, `cache/`, `.graphify_analysis.json`, `.graphify_root` | All six repositories |
| `graph.html` | mb-3-cs-app1 |
| `.graphify_build.json` (`{"gitignore": false}`) | mb-3-cs-app1 |
| `.graphify_labels.json` + `.graphify_labels.json.sig` (community labels) | mb-3-cs-app1 |
| Machine-local dated backup folders (untracked) | mb-3-cs-app1 (four) |

## OpenCode integration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| MCP entry | `graphify opencode install` writes an AGENTS.md section + a `tool.execute.before` plugin | Manual `mcp.graphify` entry in each repository's root `opencode.json`: type `local`, enabled `true`, command `["/usr/bin/python3", "-m", "graphify.serve", "<repo>/graphify-out/graph.json"]` | `graphify --help` | L2 |
| MCP tools | 10 in the installed `serve.py`: `graph_stats`, `get_node`, `get_neighbors`, `get_community`, `god_nodes`, `shortest_path`, `query_graph`, `list_prs`, `get_pr_impact`, `triage_prs` (prefixed `graphify_` in OpenCode) | Same | Installed `serve.py` | |
| PR-triage tools | — | Present but unused (require a GitHub CLI/token) | — | |
| API key for MCP | — | None; the 7 core tools need none | Installed `serve.py` | |
| Global OpenCode config | — | No graphify entry | — | |
| `.opencode/opencode.json` | Plugin registration written by `graphify opencode install` | Present only in mb-3-cs-app1, holding `$schema` only; absent in the other five | — | |
| `.opencode/plugins/graphify.js` | `tool.execute.before` hook that prepends a reminder string to bash commands; writes no files | Present in all six | — | |
| AGENTS.md guidance block | — | `<!-- BEGIN GRAPH MEMORY GUIDANCE -->` … `<!-- END GRAPH MEMORY GUIDANCE -->` shared GBrain + Graphify block in mb-3-cs-app1 only; owner [[[mybizz-os-docs:os-reference-docs/memory-master-explainer\|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) | — | |

## Related facts

| Item | State |
|---|---|
| Git hooks / merge driver | Not installed, not registered (L4) |
| GBrain | Never ingests `graphify-out/`; no shared backend; separate MCP servers |

## Open items

None.
