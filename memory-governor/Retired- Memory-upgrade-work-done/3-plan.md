---
title: "3-plan"
doc-id: "3-plan"
---
# Work Package 3 — Cross-file Graphify Adequacy Test

Read-only adequacy test against the existing Graphify graph
(`graphify-out/graph.json`). Verifies that Graphify 0.9.40 correctly captures the
cross-file relationship between two symbols (`get_vault_secret` and `encrypt`)
that live in different source files. No graph rebuild, no clustering, no
.gitignore / AGENTS.md / GBrain changes, no hooks, no package changes, no
PostgreSQL, no commit/push, no sync-gbrain. No files changed.

**Result: PASS** (relationship correctly captured, EXTRACTED, cross-file).

---

## 1. Source files inspected

| Symbol | File | Line |
|---|---|---|
| `get_vault_secret` | `server_code/server_shared/vault_service.py` | L15 |
| `encrypt` | `server_code/server_shared/encryption_service.py` | L13 |

### Actual source-level relationship (direct inspection)

- `vault_service.py` L13: `from .encryption_service import encrypt, decrypt` —
  the module imports both functions.
- `get_vault_secret` (L15) calls `decrypt(encrypted_value)` at **L43** — it does
  **not** call `encrypt` directly.
- `save_vault_secret` (L65, same file) calls `encrypt(secret_value)` at **L82**.
- Conclusion: `get_vault_secret` and `encrypt` are in different files and are
  **not** joined by a direct call edge; the cross-file link is
  module-`imports` + module-`contains`. The only function that actually *calls*
  `encrypt` is `save_vault_secret`.

## 2. Graphify tooling

- Version: **graphify 0.9.40** (`/home/dev-p/.local/bin/graphify`).
- Top-level `graphify --help` lists `path "A" "B"` with only `--graph`. The
  `--directed|--undirected` flags are hidden from the top-level help but revealed
  by `graphify path --help`:
  ```
  Usage: graphify path "<source>" "<target>" [--graph path] [--directed|--undirected]
  ```
- Node matching is case-folded substring against node labels (both names resolved).

## 3. Commands run (all read-only)

- `git rev-parse HEAD`
- `graphify --version` / `graphify --help` / `graphify path --help`
- `graphify path "get_vault_secret" "encrypt" --graph graphify-out/graph.json`
- `graphify path "get_vault_secret" "encrypt" --undirected --graph graphify-out/graph.json`
- `git status --porcelain`
- (plus read-only `python3` JSON loads of `graph.json` and `.graphify_*.json`,
  and `read` of the two source files)

## 4. Raw Graphify result

Default (directed):

```
No directed path found between 'get_vault_secret' and 'encrypt'. Re-run with --undirected to search ignoring edge direction.
```

Undirected (graph.json is stored with `directed: false`):

```
Shortest path (2 hops):
  get_vault_secret() <--contains [EXTRACTED]-- server_shared/vault_service.py --imports [EXTRACTED]--> encrypt()
```

## 5. Graph path

`get_vault_secret() --[contains, EXTRACTED]--> vault_service.py --[imports, EXTRACTED]--> encrypt()`

Supporting edges present in `graph.json` (all `_origin: ast`, `confidence_score: 1.0`):

| Edge | Source → Target | Loc | Matches source |
|---|---|---|---|
| `calls` | get_vault_secret → decrypt | L43 | Yes |
| `calls` | save_vault_secret → encrypt | L82 | Yes |
| `imports` | vault_service → encrypt | L13 | Yes |
| `imports` | vault_service → decrypt | L13 | Yes |
| `contains` | vault_service → get_vault_secret | L15 | Yes |
| `contains` | vault_service → save_vault_secret | L65 | Yes |

## 6. Confidence / provenance

- Both path edges: `EXTRACTED`, `confidence_score: 1.0`, `_origin: ast`
  (deterministic structural extraction).
- No edge in this relationship is `INFERRED`, `AMBIGUOUS`, or `UNRESOLVED`.

## 7. Verification (6 checks)

1. **Both symbols resolve** — PASS. `get_vault_secret()` and `encrypt()` both
   present as `_callable` nodes.
2. **Path crosses files** — PASS. `vault_service.py` → `encryption_service.py`.
3. **Marked EXTRACTED** — PASS.
4. **Agrees with source inspection** — PASS. Graph correctly models that
   `get_vault_secret` calls `decrypt`, `save_vault_secret` calls `encrypt`, and
   the module imports `encrypt`; it correctly does **not** invent a direct
   `get_vault_secret → encrypt` call edge.
5. **Graph commit matches HEAD** — PASS. `built_at_commit:
   e29cbd1b959ff91812982cd71c45c3ae57da3df2` == `git rev-parse HEAD`.
6. **No files changed** — PASS. `git status --porcelain` shows only the
   pre-existing untracked `?? graphify-out/`; zero tracked files modified.

## 8. Limitation / observation (not a workaround)

The default `graphify path` invocation performs **directed** traversal even
though `graph.json` is stored undirected (`directed: false`). Because the
structural `contains` and `imports` edges point *away* from the function node
(`module → function`, `module → imported symbol`), the directed run reports "No
directed path found" for `get_vault_secret → encrypt`. The `--undirected` flag is
the documented, supported way to trace this (per `graphify path --help`) and
produces the correct 2-hop EXTRACTED path. This is a CLI default-behavior quirk,
not a data-adequacy defect: the graph data itself fully and correctly captures
the cross-file relationship.

---

## Stop condition

Adequacy test complete. Relationship resolved, EXTRACTED, cross-file, and
consistent with source. No mutation performed. Package 3 closed.

## Next steps

- None required. Package 3 closed.
