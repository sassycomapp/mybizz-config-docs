---
title: "graphify-learnings"
doc-id: "mb-372fad08"
updated: "2026-10-23"
---
# Graphify — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | Graphs are built code-only: extraction runs with `--code-only`, with no AI backend, no API key and no model calls; community labels are deterministic representative-node names. | Code-side extraction is deterministic, free and offline; the semantic and LLM-labeling paths are unused in the MyBizz setup. | Approved configuration; `graphify --help` |
| L2 | The OpenCode integration is a manual `mcp.graphify` entry in each repository's root `opencode.json`; `.opencode/opencode.json` holds no MCP entry (it exists only in mb-3-cs-app1, holding `$schema` only). | An agent inspecting the install-time registration file would conclude the integration is gone and could "restore" the wrong surface. | Live verification across all six repositories |
| L3 | `graphify extract` stamps `built_at_commit` from the invoking working directory's git repository, not the scanned path; builds and refreshes run from inside the target repository root. | A run from another repository stamps that repository's HEAD onto the graph, and only the provenance check catches it. | Live rebuild observation |
| L4 | Git hooks and the graph merge driver are not installed; refresh runs manually after each commit. | Graph currency stays an explicit, verifiable act; the merge driver targets a file that is never tracked here. | Approved decision; reasons in [[[mybizz-config-docs:graphify/graphify-explainer\|Graphify Explainer]]](C:/mybizz/mybizz-config-docs/graphify/graphify-explainer.md) |
