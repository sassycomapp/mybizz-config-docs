---
title: "12-plan"
doc-id: "mb-790ba1ca"
updated: "2026-10-01"
---
# Work Package 12 — Graph Artifact and Git Suitability Review

Read-only review of the Graphify artifacts and Git state. No files modified,
no GBrain change, no AGENTS.md/agents.md change, no `.gitignore` change, no
install, no graph rebuild, no cluster-only, no commit/push, no sync-gbrain.

---

## Git suitability recommendation

**Keep `graphify-out/` fully ignored. No `.gitignore` change required.** The
directory is already ignored via `.gitignore:11` (`graphify-out/`). Everything
inside is either derived or machine-specific; nothing is authoritative source.
Committing it would add churn (382 KB `graph.json` + 382 KB `graph.html` +
~180 AST cache files) and immediately go stale (it is already one commit
behind HEAD).

## Exact files: track vs ignore

All under `graphify-out/`, none tracked:

| Class | Files | Action |
|---|---|---|
| **Authoritative (derived, MCP source-of-truth)** | `graph.json` (directed multigraph, 537 nodes / 434 links, `built_at_commit`) | ignore (reproducible) |
| **Derived / reproducible** | `graph.html`, `GRAPH_REPORT.md`, `manifest.json`, `.graphify_analysis.json`, `.graphify_labels.json`, `.graphify_labels.json.sig`, `.graphify_build.json` | ignore |
| **Machine-specific** | `.graphify_root` (absolute path `/mnt/c/dev/dev-mb-3-cs/mb-3-cs`), `cache/` (`stat-index.json`, `ast/v0.9.40/*` (180 hashed AST files), `last_query_stamp`) | ignore |

The actual source of truth is the **committed source tree** (`client_code/`,
`server_code/`, `tests/`), which is tracked. `graph.json` is "authoritative"
only in the narrow sense that the MCP serves from it.

## Security findings

- **No secrets.** Scanned `graph.json`, `graph.html`, `manifest.json`,
  `.graphify_analysis.json`, `.graphify_labels.json`, `.graphify_labels.json.sig`,
  `cache/`: zero `-----BEGIN`, `sk-`, `AKIA`, `ghp_`, `xoxb`, `api_key`,
  `credential`, `authorization`, `bearer`, emails (`@`), or private-key markers.
- **"secret" (95) / "password" (64) hits are benign identifiers** — vault
  function names (`get_vault_secret`, `save_vault_secret`),
  `PasswordResetForm` class names, and docstrings (e.g. "…key from Anvil
  Secrets" — a docstring, not a literal key).
- **No absolute paths in graph data.** Node `source_file` fields are
  repo-relative (`server_code/server_shared/exceptions.py`,
  `client_code/auth/…`). The only absolute path is in the machine-specific
  `.graphify_root` and in the `GRAPH_REPORT.md` header line
  (`/mnt/c/dev/dev-mb-3-cs/mb-3-cs`), plus the report's build date.
- **`graph.html`**: no embedded source bodies (0 `def ` matches; only node
  labels + docstrings inline). One external dependency —
  `unpkg.com/vis-network@9.1.6` — SRI-pinned (`sha384-…`) + `crossorigin`, so
  safe but network-dependent.

## Reproducibility findings

- **Reproducible:** the graph can be regenerated from the committed source via
  `graphify update .` (no API cost, per `GRAPH_REPORT.md`). No committed data
  is lost by ignoring `graphify-out/`.
- **Provenance is stale but content-equivalent.** `graph.json.built_at_commit =
  e29cbd1b959…`, while HEAD = `5ce243e12b…`. The HEAD commit (`chore: add
  Graphify scope configuration`) changed only `.gitignore` (+`graphify-out/`)
  and `.graphifyignore` (`.opencode/`, `opencode.json`) — **no source files**.
  So a rebuild would produce identical nodes/edges; only the `built_at_commit`
  label lags.
- **`.graphifyignore`** (committed at HEAD) lists `.opencode/` and
  `opencode.json`. It does **not** list mb-3-cs, which is `.gitignore`d but
  not `.graphifyignore`d — a minor inconsistency, harmless because Markdown
  isn't a code-extraction target (and the graph's `manifest.json` contains only
  `.py`/`__init__.py` paths anyway).

## mb-3-cs integrity (item 11)

Confirmed unchanged except the approved managed block: `BEGIN`/`END GRAPH
MEMORY GUIDANCE` markers each appear exactly once, `## Graph Memory Guidance`
once, and the two "Access Model" bullets intact. Git status clean.

## Required follow-up package

**None required.** No `.gitignore` change is needed, no tracked graph files
need removing, and the graph content is current (HEAD changed only
ignore/scope files).

**Optional (recommended, not required):** rebuild the graph to align
`built_at_commit` with HEAD (a cheap, API-free `graphify update .`) so
provenance is no longer one commit behind — useful for future `graph
provenance must match HEAD` checks in the new Graph Memory Guidance block.

## Next steps

- **Build →** none (read-only review; no follow-up required).
- **Plan/developer →** optional graph rebuild to HEAD, at your discretion.
- Housekeeping (asked separately): commit/push approval; GBrain sync approval.
