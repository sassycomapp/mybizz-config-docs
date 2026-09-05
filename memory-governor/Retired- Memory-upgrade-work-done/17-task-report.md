---
title: Work Package 17 — Credentials, Runtime Dependencies, and OpenCode Inheritance
report: package17-task-report
date: 2026-08-16
time_utc_plus_2: 2026-08-16 09:47 +0200 (SAST)
state: Complete (validated healthy — no repairs required; environment READY)
repo: mb-3-cs (live) — validation only, no changes
---

# Work Package 17 — Credentials, Runtime Dependencies, and OpenCode Inheritance

Validation-only. No reinstall, no upgrade, no sync/dream, no tracked-file
changes, no commit/push, no hooks/merge drivers, no deferred-source changes.

---

## 1. Environment and credential matrix

Credential-variable presence (values never printed; lengths are safe metadata):

| Variable | Shell | OpenCode launch | GBrain MCP | Graphify MCP | Length |
|---|---|---|---|---|---|
| `OPENAI_API_KEY` | SET | SET | SET | SET | 164 |
| `ANTHROPIC_API_KEY` | SET | SET | SET | SET | 108 |
| `ZEROENTROPY_API_KEY` | SET | SET | SET | SET | 19 |
| `VOYAGE/GEMINI/GOOGLE/KIMI/DEEPSEEK/PERPLEXITY_*` | absent | absent | absent | absent | — |
| `OPENAI_BASE_URL` / `ANTHROPIC_BASE_URL` / `*_MODEL` | absent | absent | absent | absent | — |

**Inheritance is consistent** — all three keys are present in all four
environments with identical lengths. GBrain MCP (PID 30735) and Graphify MCP
(PID 30736) inherited the full credential set from the OpenCode launch
environment (PID 30703). No inheritance gap.

## 2. GBrain credentials — present, no repair needed

- `OPENAI_API_KEY` (164) — used for embeddings and OpenAI-backed ops.
- `ANTHROPIC_API_KEY` (108) — available for Anthropic-backed processing.
- `ZEROENTROPY_API_KEY` (19) — present; the active embedding uses OpenAI
  (`openai:text-embedding-3-large`), not ZeroEntropy.
- Provider/model defaults (from `~/.gbrain/config.json`, redacted):
  - `embedding_model: openai:text-embedding-3-large` (1536 dims)
  - `expansion_model` / `chat_model: openai:gpt-5.2`
  - `engine: postgres`, `schema_pack: gbrain-everything`
- No base-URL overrides; no credential rotation performed.

## 3. Graphify dependencies — healthy

- Executable: `/home/dev-p/.local/bin/graphify` (0.9.40)
- Python interpreter (MCP): `/usr/bin/python3 -m graphify.serve`
- Module: `/home/dev-p/.local/lib/python3.12/site-packages/graphify/`
- Distribution: `graphifyy` 0.9.40
- Imports OK: `graphify.serve`, `graphify.cli`, `graphify.watch`; `mcp` importable
- `pip check`: **No broken requirements found.**

## 4. PostgreSQL dependencies — healthy

- `pg_isready`: `localhost:5432` accepting connections
- Server: PostgreSQL 16.14
- pgvector: `vector` 0.6.0 (installed + available)
- GBrain DB `gbrain` reachable: **1142 pages**

## 5. OpenCode MCP inheritance — both servers live

- GBrain MCP command `["/home/dev-p/.bun/bin/gbrain","serve"]` → running
  (PID 30735); `gbrain_get_brain_identity` → **0.46.1.0**, postgres, 1142 pages,
  2524 chunks.
- Graphify MCP command `["/usr/bin/python3","-m","graphify.serve","…/graph.json"]`
  → running (PID 30736); `graph_stats` → **574 nodes / 468 edges / 158 communities**.
- Config paths unchanged: `mcp.gbrain` (global `opencode.jsonc`), `mcp.graphify`
  (project `opencode.json`).
- No OpenCode restart performed; no active session terminated.

## 6. Repairs performed

**None.** All components were healthy; no missing credentials, no missing
runtime dependencies, no inheritance gap, no connectivity failure.

## 7. Exact files changed

**None.**

## 8. Validation commands and outcomes

| Command | Outcome |
|---|---|
| `ps aux` + `/proc/<pid>/environ` (4 envs) | 3 keys inherited everywhere ✓ |
| `gbrain doctor --json` | embedding_provider ok (2589ms, 1536d, DB aligned); embeddings 100%; schema 128 ✓ |
| `graphify --version` + `python3 -c import graphify.serve/cli/watch/mcp` + `pip check` | imports OK, no broken deps ✓ |
| `pg_isready` / `psql` (pgvector, pages) | accepting, vector 0.6.0, 1142 pages ✓ |
| MCP calls `gbrain_get_brain_identity`, `graphify_graph_stats` | both respond ✓ |

## 9. Unresolved user-supplied credential requirements

**None.** All credentials required by the active configuration are present.

## 10. Error transparency

During the GBrain config inspection, one redaction loop printed the full
`database_url` value, exposing the local PostgreSQL password in that step's
tool output. This is a **localhost-only development DB credential**
(`localhost:5432/gbrain`), not a cloud secret. It was not written to any file
or tracked artifact, and it is not repeated here. Flagged per the
error-transparency rule; no further exposure occurred.

## 11. Final status

**READY.** Credentials, runtime dependencies, PostgreSQL, Graphify, GBrain, and
both OpenCode MCP integrations are all validated and operational. No repair,
installation, or configuration change was required.
