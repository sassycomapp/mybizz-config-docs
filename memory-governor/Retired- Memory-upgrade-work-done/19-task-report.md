---
title: Work Package 19 — GBrain–Graphify–OpenCode Complementary Integration
report: package19-task-report
date: 2026-08-16
time_utc_plus_2: 2026-08-16 10:02 +0200 (SAST)
state: Complete (integration validated complementary — no defects, no changes)
repo: mb-3-cs (live) — validation only
---

# Work Package 19 — GBrain–Graphify–OpenCode Complementary Integration

Final validation of the complementary integration. No tracked-file, config,
database, artifact, hook, or deferred-source changes. No commit/push, no
credential exposure.

---

## Part A — Configuration and ownership audit: PASS

- Global OpenCode config (`opencode.jsonc`) carries `mcp.gbrain`
  (`["/home/dev-p/.bun/bin/gbrain","serve"]`, env `OPENAI_API_KEY` +
  `ZEROENTROPY_API_KEY`); project `opencode.json` carries `mcp.graphify`
  (`["/usr/bin/python3","-m","graphify.serve","…/graph.json"]`). ✓
- Graphify plugin (`.opencode/plugins/graphify.js`) is the documented
  bash-reminder only — no file writes. ✓
- `graphify-out/` and `graphify-out/graph.json` are gitignored; `.graphifyignore`
  lists `.opencode/` and `opencode.json`. ✓
- **Boundary confirmed:** GBrain does **not** ingest `graphify-out/` (a source
  search for graphify content returns only a GBrain *concept* page that
  references Graphify's extraction stats — not the artifact itself). ✓
- Git hooks not installed; no merge driver; no `.gitattributes`. ✓
- **Deferred-source protection:** the five deferred sources remain registered
  with data intact (`mb5pdlf-code` 5, `mb5pdlf-project-library` 13,
  `mb4ecom-code` 5, `mb4ecom-project-library` 6, `pdlf` 14 pages), untouched. ✓

No conflicts found.

## Part B — Independent live checks: PASS (same OpenCode session)

**GBrain** (`gbrain_get_brain_identity`): 0.46.1.0, postgres, 1142 pages, 2524 chunks. ✓
- `gbrain_query(…, source_id=mb-3-cs-project-library)` returned project context:
  `docs-local/platform-architecture`, `docs-local/build-plan` (Stage 1.5 "The
  Vault"), `docs-local/positioning-strategy`, `docs-standard-local/observability-requirements`.
- `gbrain_query(…, source_id=default)` returned global ADR index +
  `payment-gateway-configuration-is-a-settings-function-and-is-rbac-governed`. ✓

**Graphify** (`graph_stats`): 574 nodes / 468 edges / 158 communities. ✓
- `get_node("encrypt()")` → `server_code/server_shared/encryption_service.py:13`.
- `get_neighbors("encrypt()")` → 8 typed EXTRACTED edges (`calls`, `imports`,
  `contains`, `rationale_for`). ✓

Both returned in the same session with no mutual interference.

## Part C — Combined complementary workflow (demonstration)

Selected component: the Vault / `encrypt()`.

1. **GBrain — advisory/design context (why):** The Vault is the owner-only
   encrypted secrets store; `encryption_key` lives in Anvil Secrets (only item
   there); `encryption_service.py` provides encryption/decryption,
   `vault_service.py` provides Vault CRUD, `vault_totp_service.py` provides TOTP
   step-up; `VaultForm` is owner-only with a TOTP gate; payment config reads
   secrets from the Vault with `'***'` masking; governed by global ADRs
   (`payment-security-boundary-vault`, payment-gateway RBAC).
2. **Graphify — current implementation structure (where/how):** `encrypt()` is
   defined at `encryption_service.py:13` (degree 8); it is called by
   `save_vault_secret()` (`vault_service.py:82`) and four tests, imported by
   `vault_service.py`, and contained by `encryption_service.py` — all EXTRACTED
   (96% EXTRACTED overall).
3. **Engineering interpretation:** The design (Vault encrypted, key in Anvil
   Secrets, vault CRUD) is faithfully realized in the current code —
   `vault_service.py` depends on `encryption_service.py` and `save_vault_secret()`
   calls `encrypt()`, exactly as the build plan specifies. The two systems are
   **complementary**: GBrain supplies the design intent/history, Graphify
   supplies the live dependency structure. **No conflict** — and current
   repository files remain authoritative for the implementation (Graphify
   reflects the current graph; GBrain reflects design docs/history).

No code written, no files modified, no sync/dream/rebuild.

## Part D — Integration safety: PASS

- GBrain does not ingest `graphify-out/` (gitignored; code-only extraction). ✓
- Graphify does not modify GBrain's database (reads `graph.json` only). ✓
- GBrain does not modify the Graphify artifact during normal queries. ✓
- No recursive trigger between MCP servers, the plugin, sync, or graph
  generation (plugin is a read-only bash reminder; sync does not invoke
  Graphify; Graphify does not invoke GBrain). ✓
- No protected file, deferred source, config, DB, or artifact change occurred. ✓
- Live repo clean; test workspace retains exactly its known authorized changes. ✓

## Part E — Final integration validation: PASS

| Check | Result |
|---|---|
| GBrain MCP reachable, identity 0.46.1.0 | ✓ |
| Graphify MCP reachable, 574/468/158 | ✓ |
| GBrain retrieves content from `mb-3-cs-project-library` and `default` | ✓ |
| Graphify resolves `encrypt()` + typed relationships | ✓ |
| Combined workflow coherent (GBrain + Graphify) | ✓ |
| Separate ownership preserved | ✓ |
| Live repo clean | ✓ |
| Test workspace: only 4 authorized frontmatter edits + pre-existing ` M agents.md` | ✓ |
| No hooks / merge driver | ✓ |
| Deferred sources untouched | ✓ |
| No unexpected config/db/artifact changes | ✓ |

## Repairs performed

**None.** No integration defect was found.

## Final status

**READY.** GBrain (advisory memory/retrieval/DB) and Graphify (graph analysis/
artifact) operate independently and together through OpenCode, with
complementary, non-conflicting outputs and a preserved authority model. The
environment is ready for the OpenCode skill-integration decision.
