---
title: "18-task-report"
doc-id: "mb-7b91d2e4"
updated: "2026-10-01"
---
# Work Package 18 — Graphify Installation and Runtime Validation

Independent Graphify validation against the live repo and existing artifact.
No reinstall, no upgrade, no hooks/merge driver, no tracked-file changes, no
GBrain/schema/credential changes, no commit/push, no secret exposure.

---

## Part A — Installation validation: PASS

| # | Check | Result |
|---|---|---|
| 1 | `graphify --version` | 0.9.40 ✓ |
| 2 | executable | `/home/dev-p/.local/bin/graphify` ✓ |
| 3 | MCP interpreter | `/usr/bin/python3` (3.12.3) ✓ |
| 4 | module path | `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` (Python 3.12.3) ✓ |
| 5 | distribution | `graphifyy` 0.9.40 ✓ |
| 6 | submodules | `graphify.serve`, `graphify.cli`, `graphify.watch` import OK ✓ |
| 7 | `mcp` import | OK ✓ |
| 8 | `pip check` | No broken requirements ✓ |

## Part B — Repository and artifact: PASS

- Repo root: `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` ✓
- Branch `master`, HEAD `5ce243e12bc2775108c9ecad6da1e6c7f8f1614c`, porcelain **clean** ✓
- `graphify-out/graph.json` gitignored ✓
- Artifact exists (413102 bytes) and readable ✓
- `built_at_commit` = `5ce243e12bc2775108c9ecad6da1e6c7f8f1614c` == HEAD ✓
- Top-level schema keys: `directed`, `multigraph`, `graph`, `nodes`, `links`,
  `hyperedges`, `built_at_commit` ✓

## Part C — Graph operation validation: PASS

- `graph_stats`: **574 nodes / 468 edges / 158 communities** (96% EXTRACTED, 4% INFERRED, 0% AMBIGUOUS) ✓
- Symbol definition query (`graphify_get_node "encrypt()"`): resolved to
  `server_code/server_shared/encryption_service.py:13`, type `code`, degree 8 ✓
- Relationship query (`graphify_get_neighbors "encrypt()"`): 8 neighbors, all
  EXTRACTED — `calls` (from `save_vault_secret()` and 4 test methods), `imports`
  (from `vault_service.py`), `contains` (from `encryption_service.py`),
  `rationale_for` (docstring) ✓

Note on caller/callee: Graphify exposes caller/callee relationships as typed
edges via `get_neighbors` (the `calls`/`imports`/`contains` edges above correctly
identify `encrypt()`'s callers). A dedicated `code-callers`/`code-callees`
command is a **GBrain** code-surface feature, not a Graphify feature — this is a
correct tooling boundary, not a Graphify failure.

- No output written outside the ignored `graphify-out/`; no source files modified ✓

## Part D — MCP validation: PASS

- Configured command: `["/usr/bin/python3","-m","graphify.serve","…/graphify-out/graph.json"]` ✓
- MCP server running (PID 30736) and serving the artifact ✓
- `graph_stats` returns 574 / 468 / 158 ✓
- Project `opencode.json` `mcp.graphify` points at the correct artifact ✓
- Graphify plugin (`.opencode/plugins/graphify.js`) present; it is the documented
  bash-reminder only (no file writes) ✓
- No OpenCode restart required (MCP already live and validated) ✓
- GBrain MCP unaffected: `gbrain_get_brain_identity` → 0.46.1.0, postgres, 1142 pages ✓

## Part E — Hooks and ownership: PASS

- `graphify hook status`: post-commit/post-checkout not installed; merge driver not registered ✓
- No `merge.graphify.*` git config ✓
- No `.gitattributes` ✓
- Active hooks: only `.sample` files ✓
- Ownership: Graphify owns only its configured `graphify-out/` + MCP integration;
  GBrain owns its DB + advisory memory; neither invokes the other ✓

## Part F — Final validation: PASS

- `graphify --version` 0.9.40; imports OK; `pip check` clean ✓
- Artifact readable; `built_at_commit` == HEAD ✓
- `graph_stats` 574 / 468 / 158 ✓
- Graphify MCP tool check: node + neighbors return correct data ✓
- Live repo `git status --porcelain`: clean ✓
- Test workspace: only the 4 authorized WP16.5.1 frontmatter edits + pre-existing
  ` M agents.md` (unchanged by this package) ✓
- GBrain MCP identity: 0.46.1.0 ✓
- No unexpected file changes ✓

## Repairs performed

**None.** Every check passed; no dependency, artifact, config, or MCP issue was
found.

## Final status

**READY.** Graphify 0.9.40 is installed, importable, dependency-healthy, its
artifact is aligned to HEAD, graph statistics are available, the Graphify MCP is
operational through the configured command, GBrain MCP remains operational, and
no hooks/merge drivers or tracked-file changes exist.
