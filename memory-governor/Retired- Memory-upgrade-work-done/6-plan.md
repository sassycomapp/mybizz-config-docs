---
title: "6-plan"
doc-id: "mb-bf35d73f"
---
# Work Package 6 — Read-only Review of the Completed Graphify Graph

Read-only review of the completed `mb-3-cs` Graphify graph and its generated
outputs. No files modified; no extraction, no cluster-only, no GBrain/AGENTS.md/
hooks changes. Recommendation only.

---

## 1. Inspection (7 items)

| Item | Finding |
|---|---|
| `GRAPH_REPORT.md` | Present (6,480 B), current: 537 nodes · 434 edges · 155 communities, "Built from commit: `e29cbd1b`". Includes God Nodes, Surprising Connections, Import Cycles, Knowledge Gaps, Suggested Questions. |
| `graph.json` | 537 nodes / 434 edges. Top-level keys all expected (`directed`, `multigraph`, `graph`, `nodes`, `links`, `hyperedges`, `built_at_commit`) — no stray metadata. All `source_file` values repo-relative (0 absolute paths) → portable. |
| `graph.html` | Present (382,888 B), self-contained HTML; loads `vis-network@9.1.6` from unpkg CDN with an SRI integrity hash (rendering needs network; no secrets). |
| `.graphify_labels.json` | 155 entries: community ID → deterministic representative-node name (e.g. `patch`, `metrics.py`, `BlogListForm`). |
| `.graphify_labels.json.sig` | 155 entries: community ID → 16-hex fingerprint (tamper-evidence signature, not sensitive content). |
| `.graphifyignore` | Exactly `.opencode/` + `opencode.json` (verified). |
| Git status | `?? .graphifyignore`, `?? graphify-out/` — neither tracked nor ignored. `.gitignore` does not list `graphify-out/`. HEAD = `e29cbd1b…`. |

## 2. Assessment (9 questions)

1. **Is the report useful?** Yes. Surfaces the architectural core (God Nodes:
   `VaultDecryptionError`, `VaultError`, `encrypt()`, `decrypt()`,
   `get_vault_secret()`), surprising cross-file INFERRED edges, zero import
   cycles, and actionable questions. Caveat: cluster-only report ("file stats
   not available") with 92 thin communities omitted from display.
2. **Are the 155 labels acceptable as deterministic labels?** Yes. Honest
   representative-node names (deterministic, readable, no hallucination), not
   LLM-authored groupings.
3. **Do the 92 omitted thin communities create a material problem?** No.
   Omitted from report display only (still present in `graph.json`). Reflects a
   fragmented graph (code-only, many isolated form modules) — a known
   characteristic, not a defect.
4. **Do the 4% INFERRED edges require investigation?** No. 17 edges (avg
   confidence 0.69), localized to the vault/encryption test area
   (`TestEncryptionService`/`TestVaultService` → error classes; `patch` →
   mocks). Already flagged in the report's Suggested Questions for optional
   spot-check — not blocking.
5. **Secrets/sensitive info in `graph.html`/`graph.json`?** None. Scans found
   only benign code identifiers and docstrings (`PasswordResetForm`,
   `secret()`, `SecretNotFoundError`, "secret from the Vault table…"). No API
   keys, `sk-`/`AKIA` tokens, credentials, private keys, or emails. The
   `opencode.json` dangerous-command noise (`rm -rf`, `DROP TABLE`, …) is gone
   (excluded by `.graphifyignore`). No secret value and no `encryption_key`
   literal present — the key is fetched by name at runtime, never in source.
6. **Suitable for Git tracking?** Mixed. `.graphifyignore` = yes (source
   config). `graph.json` + `GRAPH_REPORT.md` = yes if a versioned deterministic
   snapshot is wanted. The rest = no (derived/machine-specific).
7. **Which files to commit:** `.graphifyignore` (definitely); optionally
   `graph.json` + `GRAPH_REPORT.md`.
8. **Which files to ignore:** the remainder of `graphify-out/` — `graph.html`
   (CDN dep), `cache/`, `.graphify_root` (absolute path), `manifest.json`
   (hashes), `.graphify_analysis.json`, `.graphify_labels.json*`,
   `.graphify_build.json`. Simplest: ignore the whole `graphify-out/` directory.
9. **Graph tied to current commit?** Yes — `built_at_commit` =
   `e29cbd1b959ff91812982cd71c45c3ae57da3df2` = `git rev-parse HEAD`.

## 3. Recommendation

- **Commit:** `.graphifyignore` — small, authoritative, governs all future
  rebuilds.
- **Track vs ignore — two options:**
  - **Recommended:** add `graphify-out/` to `.gitignore` (whole directory).
    The graph is deterministic and regenerable (`graphify extract --code-only`
    + `cluster-only`), and the directory contains machine-specific artifacts
    (`.graphify_root`, `cache/`, `manifest.json`) plus a 382 KB CDN-dependent
    HTML.
  - **Alternative** (if query-without-rebuild is wanted): commit only
    `graphify-out/graph.json` + `graphify-out/GRAPH_REPORT.md` as a versioned,
    commit-pinned snapshot; ignore everything else in `graphify-out/`.
- **Follow-up package (Build, on approval):** (a) append `graphify-out/` to
  `.gitignore`; (b) commit `.graphifyignore` (and, if the alternative is
  chosen, `graph.json` + `GRAPH_REPORT.md`). No other follow-up required. The
  17 INFERRED edges warrant only an optional spot-check, not a package.

---

## Stop condition

Review complete. No files modified. Package 6 is a recommendation only.

## Next steps

- Plan → none (Package 6 review closed).
- Build → on approval: add `graphify-out/` to `.gitignore` and commit
  `.graphifyignore` (plus optional `graph.json`/`GRAPH_REPORT.md`).
