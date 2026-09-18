---
doc-id: 15-task-report
document: "Work Package 15 — Authoritative Environment Inventory"
date-created: 2026-08-14
title: Work Package 15 — Authoritative Environment Inventory
report: package15-task-report
date: 2026-08-14
time_utc_plus_2: 2026-08-14 17:46 +0200 (SAST)
state: Complete (read-only inventory — no blockers, zero changes)
repo: mb-3-cs (live) / mb-3-cs-project-library (test workspace)
---

# Work Package 15 — Authoritative Environment Inventory

Read-only environment map for the GBrain–Graphify–OpenCode completion work.
No install/upgrade, no migrations, no config or credential changes, no service
state changes, no Git hooks, no sync/dream/embed/extract/self-upgrade, no
skillpack scaffold, no file edits, no commit/push. Every fact established by a
read-only command.

---

## Executive status

**Green.** All core components of the GBrain–Graphify–OpenCode stack are
installed, configured, and healthy. No blocking failures. Two non-blocking
repair items (graph stale vs HEAD; GBrain update available) and one
informational item (project-library has a pre-existing uncommitted `agents.md`
change unrelated to this package).

## Authoritative path map

| Item | Path |
|---|---|
| Live app repo | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` (= `C:\dev\dev-mb-3-cs\mb-3-cs`) |
| Planning/test workspace | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` (= `C:\dev\dev-mb-3-cs\mb-3-cs-project-library`) |
| `C:\mybizz` | `/mnt/c/mybizz` (Mgt, WIP, anvil-agent-references, config, gbrain, gstack, logs, scripts, skills-collective) |
| WSL distro | Ubuntu 24.04.4 LTS (Noble), kernel `6.6.87.2-microsoft-standard-WSL2`, x86_64 |
| User / home | `dev-p` (uid 1000, sudo) / `/home/dev-p` |
| Shell | `/bin/bash`; startup files `~/.bashrc` (4775 B), `~/.profile` (807 B); no `~/.bash_profile`/`~/.zshrc` |
| CWD | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` |

## Repository status

| | mb-3-cs (LIVE) | mb-3-cs-project-library (test/planning) |
|---|---|---|
| Absolute path | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` |
| Git root | same | same |
| Branch | `master` | `main` |
| HEAD | `5ce243e12bc2775108c9ecad6da1e6c7f8f1614c` | `d92950712f3478a98f85b0988d3f568bff03d2da` |
| Remote | `https://github.com/sassycomapp/mb-3-cs` | `https://github.com/sassycomapp/mb-3-cs-project-library.git` |
| Porcelain | **clean** | **` M agents.md`** (pre-existing, Aug 12) |
| Package 15 target | **Live app repo** (subject of completion work) | Skillpack test target (WP14); planning authority |

The project-library ` M agents.md` change is a pre-existing, uncommitted
"Anvil Agent References" section (mtime Aug 12 21:59) — **not** caused by
Package 15, left untouched.

## OpenCode inventory

- **Version:** 1.15.12
- **Executable:** `/home/dev-p/.opencode/bin/opencode` (standalone 145 MB
  binary; not an npm-global install)
- **Running:** **Yes** — PID 22367, `opencode web --hostname 0.0.0.0` (since
  15:38)
- **Config paths:**
  - Global: `~/.config/opencode/opencode.jsonc` (default_agent `plan`, global
    `instructions`, permissions, and **`mcp.gbrain`** local)
  - Project: `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/opencode.json` (gitignored;
    `mcp.graphify` + graphify plugin + permissions) and
    `.opencode/opencode.json` (plugin only)
- **MCP config:**
  - `gbrain` — global jsonc, `type: local`,
    `["/home/dev-p/.bun/bin/gbrain","serve"]`, `enabled: true`, env
    `{OPENAI_API_KEY}`, `{ZEROENTROPY_API_KEY}`
  - `graphify` — project opencode.json, `type: local`,
    `["/usr/bin/python3","-m","graphify.serve","…/graphify-out/graph.json"]`,
    `enabled: true`
- **Skill-discovery paths:** `~/.config/opencode/skills/` (gstack set),
  `~/.claude/skills/` (gstack, wireframe), `~/.agents/skills/` (anvil +
  matt-pocock set), project `.opencode/skills/` (empty)

## GBrain inventory

- **Version:** 0.43.0.0 (latest available 0.45.12.0; `self_upgrade.mode =
  notify`, not applied)
- **Executable:** `/home/dev-p/.bun/bin/gbrain` (bun global → source
  `src/cli.ts`)
- **Source/install dir:** `/home/dev-p/gbrain` (dev checkout; package.json
  `name: gbrain`, `version: 0.43.0.0`)
- **Config:** `~/.gbrain/config.json` — `engine: postgres`,
  `embedding_model: openai:text-embedding-3-large`,
  `schema_pack: gbrain-everything`, `mcp.publish_skills: true`
- **DB target (password redacted):** `postgresql://postgres@localhost:5432/gbrain`
- **Active schema pack:** `gbrain-everything@1.0.0` (sha8 `7021205a`), 30 page
  types, 12 link types, `source_tier: home-config`
- **Registered sources (10):** `default` (federated,
  `/mnt/c/dev/project-library-global`, 192 pages), `mb-3-cs-code`
  (`/mnt/c/dev/dev-mb-3-cs/mb-3-cs`, 263 pages), `mb-3-cs-project-library`
  (419 pages), plus dev-makepdlf, dev-root-hub, mb4ecom-code/-library,
  mb5pdlf-code/-library, pdlf
- **Brain:** 1118 pages / 2269 chunks (via MCP, engine postgres)
- **Not run:** sync, dream, embed, extract, migrations, self-upgrade

## PostgreSQL inventory

- **Service/process:** running — cluster `16/main` **online**, port **5432**,
  owner `postgres`, data dir `/var/lib/postgresql/16/main`
- **Version:** PostgreSQL **16.14** (Ubuntu 16.14-0ubuntu0.24.04.1)
- **pgvector:** **0.6.0** (extension `vector` installed and available)
- **GBrain DB reachable:** **Yes** — `pg_isready` accepting connections;
  `psql -U postgres -d gbrain` round-trip succeeded; GBrain MCP
  `get_brain_identity` live

## Graphify inventory

- **Status:** **Fully installed** (version **0.9.40**)
- **Executable:** `/home/dev-p/.local/bin/graphify`
- **Package:** PyPI dist **`graphifyy` 0.9.40**, module at
  `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` (module name
  `graphify`, dist name `graphifyy`)
- **Integration mechanism:** OpenCode **local MCP**
  (`python3 -m graphify.serve <graph.json>`), enabled in project
  `opencode.json`; plus a `tool.execute.before` plugin
  (`.opencode/plugins/graphify.js`) that only injects a bash reminder
- **Git hooks:** `graphify hook status` → post-commit/post-checkout **not
  installed**, merge driver **not registered** (WP13: do not install)
- **Graph artifact:** `graphify-out/graph.json` present (386 KB),
  `built_at_commit e29cbd1b` vs HEAD `5ce243e` (**one commit stale,
  content-equivalent** — see WP12)
- **No Graphify write operation was run**

## Credentials and dependency status

Present (values never printed):

| Variable | Status | Value length |
|---|---|---|
| `OPENAI_API_KEY` | SET | 164 |
| `ANTHROPIC_API_KEY` | SET | 108 |
| `ZEROENTROPY_API_KEY` | SET | 19 |
| `VOYAGE_API_KEY` | ABSENT | — |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | ABSENT | — |
| `KIMI_API_KEY` / `DEEPSEEK_API_KEY` / `PERPLEXITY_API_KEY` | ABSENT | — |
| `OPENAI_BASE_URL` / `ANTHROPIC_BASE_URL` / `*_MODEL` | ABSENT (defaults) | — |

- **Required keys for the current setup are all present** (OpenAI for
  embeddings/chat; Anthropic; ZeroEntropy). Absent keys (Voyage, Gemini,
  Google, Kimi, DeepSeek, Perplexity) are **not required** by the active config
  (embeddings use `openai:text-embedding-3-large`).
- **Runtime dependencies:** none missing — `graphifyy` 0.9.40 installed;
  GBrain bun-global present; PostgreSQL 16 + pgvector 0.6.0 present.

## Existing integration and ownership

| File | Owner / state |
|---|---|
| root `agents.md` (== `AGENTS.md`, gitignored, local-only) | Contains GBrain + Graphify "Access Model" and the managed `GRAPH MEMORY GUIDANCE` block (WP11) |
| root `opencode.json` (gitignored) | `mcp.graphify`, graphify plugin, permissions |
| `.opencode/plugins/graphify.js` | bash-reminder plugin (no file writes) |
| `.graphifyignore` | `.opencode/`, `opencode.json` |
| `.gitignore` | ignores `graphify-out/`, `agents.md`, `opencode.json`, `.opencode/`, `tests/`, `__pycache__`, etc. |
| Global `~/.config/opencode/opencode.jsonc` + `AGENTS.md` | `mcp.gbrain`, global instructions |
| Git hooks | none active (only `.sample` files) |

**Conflicts:** none blocking. Note `agents.md`/`opencode.json`/`graphify-out/`
are all local-only (gitignored), so Graphify config travels with neither repo;
this is intentional per WP11/WP12/WP13.

## Blocking items requiring repair

**None.** Two non-blocking items:

1. **Graph provenance stale** — `graph.json` built from `e29cbd1b`, HEAD
   `5ce243e`. Content-equivalent (HEAD only changed
   `.gitignore`/`.graphifyignore`), so optional: `graphify update .` to realign
   `built_at_commit`.
2. **GBrain update available** — 0.43.0.0 → 0.45.12.0 (currently `notify`
   mode, not applied). Optional, deferred.

## Information required from the user

Minimal. Confirm:

1. Whether the **Package 16** target is the live `mb-3-cs` repo (recommended)
   or the `mb-3-cs-project-library` skillpack test workspace.
2. Whether to act on the two optional repair items (rebuild graph to HEAD;
   `gbrain self-upgrade`), or leave them deferred.

## Exact recommended next package

**Package 16 — Completion/Repair.** With no blockers, this is small and
optional:

1. (Optional) Rebuild the Graphify graph to HEAD:
   `graphify update /mnt/c/dev/dev-mb-3-cs/mb-3-cs`.
2. (Optional) GBrain `self-upgrade` 0.43.0.0 → 0.45.12.0 (or leave on
   `notify`).
3. Verify both MCP servers (`graph_stats` = 537/434/155; `gbrain_get_stats` =
   1118/2269/382) post-any change.
4. Confirm zero config changes are needed — the stack is already integrated.

## Explicit confirmation of zero changes

Package 15 performed **no** filesystem, database, service, Git-hook, or
configuration changes. All commands were read-only. The only Git delta observed
is the **pre-existing** ` M agents.md` in `mb-3-cs-project-library` (Aug 12,
"Anvil Agent References"), present before this package began and left untouched.
Live repo `mb-3-cs` porcelain remained clean throughout.

## Next steps

- **Build →** none (read-only inventory).
- **Plan/developer →** decide Package 16 target and whether to act on the two
  optional repair items.
- Housekeeping (asked separately): commit/push approval; GBrain sync approval.
