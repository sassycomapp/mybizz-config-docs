---
title: "opencode-config"
doc-id: "mb-c7616d53"
updated: "2026-10-23"
---
# OpenCode Configuration

Settings sheet for the OpenCode agent harness. Execution lives in [[[mybizz-config-docs:opencode/opencode-reference|OpenCode Reference]]](C:/mybizz/mybizz-config-docs/opencode/opencode-reference.md), orientation in [[[mybizz-config-docs:opencode/opencode-explainer|OpenCode Explainer]]](C:/mybizz/mybizz-config-docs/opencode/opencode-explainer.md), differences from the standard in [[[mybizz-config-docs:opencode/opencode-learnings|OpenCode Learnings]]](C:/mybizz/mybizz-config-docs/opencode/opencode-learnings.md).

## Identity

| Field | Value |
|---|---|
| Issuer | OpenCode (`github.com/anomalyco/opencode`) |
| Installed version | 1.19.0 |
| Standard taken from | 1.19.0 — the issuer's documentation and configuration schema for the installed version |
| Last researched | 2026-10-20 |

## Global configuration (`~/.config/opencode/opencode.jsonc`)

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Global config file | the config directory holds the global config | `opencode.jsonc` — the only global config file | https://opencode.ai/docs/config | |
| `default_agent` | agent selection is configurable | `plan` | https://opencode.ai/config.json | |
| `permission.edit` | per-file-pattern write rule | `*: allow`; `**/anvil.yaml: deny` | https://opencode.ai/config.json | |
| `permission.webfetch` | fetch permission is configurable | `ask` | https://opencode.ai/config.json | |
| `permission.bash` | per-command-pattern rule | `*: ask` with 13 `deny` patterns (destructive git, `DROP`/`TRUNCATE` SQL, `curl`/`wget` piped to a shell) | https://opencode.ai/config.json | |
| `permission.task` | task-delegation permission is configurable | `deny` | https://opencode.ai/config.json | L1 |
| `permission.external_directory` | per-path-glob rule for work outside the project | `*: allow` | https://opencode.ai/config.json | |
| `agent.plan.permission.edit` | per-agent permission overrides | `deny` — the plan agent cannot write | https://opencode.ai/config.json | |
| `plugin` | the list accepts folder paths; a file path in it is rejected | no entry — plugins auto-load from the plugin folder | live global config | L7 |
| `instructions` | the issuer supports an instructions array | key absent | live global config | |
| `mcp.gbrain` | `mcp` entries define tool servers | `type: local`; command `gbrain serve`; `enabled: true`; environment passes `OPENAI_API_KEY` and `VOYAGE_API_KEY` as `{env:}` references and sets `GBRAIN_QUERY_EMBED_TIMEOUT_MS` to `15000` | https://opencode.ai/config.json | |

GBrain's own settings and version live in the gbrain suite: [[[mybizz-config-docs:gbrain/gbrain-config|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md).

## Paths and files

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Config directory | `~/.config/opencode` | same | `opencode debug paths` | |
| Data directory | `~/.local/share/opencode` | same | `opencode debug paths` | |
| Cache directory | `~/.cache/opencode` | same | `opencode debug paths` | |
| State directory | `~/.local/state/opencode` | same | `opencode debug paths` | |
| Temp directory | `/tmp/opencode` | same | `opencode debug paths` | |
| Log directory | under the data directory | `~/.local/share/opencode/log` | `opencode debug paths` | |
| Global rules file | the harness reads `AGENTS.md` from the config directory as global rules | `~/.config/opencode/AGENTS.md`, 17,999 bytes | live session banner | |
| Service password file | — | `~/.config/opencode/service.json`, mode 600 | developer-stated | |
| Server password variable | — | `OPENCODE_SERVER_PASSWORD`, set in `~/.bashrc` | developer-stated | |

## Plugins

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Plugin folder | plugins in the config directory's `plugin` folder load at process start; only `.js` files load | `~/.config/opencode/plugin/` | live plugin folder; developer-stated | L7 |
| `cupcake.js` | — | loaded from the plugin folder; byte-identical to its known-good restore point `cupcake.js.bak-20261016-known-good` | live check | |
| `i-have-adhd.js` | — | loaded from the plugin folder; always-on through the flag file `~/.config/opencode/.i-have-adhd-always` | developer-stated | |
| Backup files | — | dated `.bak` files beside the plugins are not discoverable — only `.js` files load | live plugin folder | |
| Deduplication | by discovery path, not file identity | every plugin keeps exactly one discoverable path | issuer behavior | |

## Skills discovery

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Discovery roots | skills are discovered from the configured skill directories | `~/.config/opencode/skills` (64 entries) and `~/.agents/skills` | live listings | L2 |
| Second name | — | `~/.config/skills` is a link to `~/.config/opencode/skills` — one folder, two names | live listing | L2 |
| Duplicate names | — | a skill found through more than one root logs a `duplicate skill name` warning; the `i-have-adhd` warning is harmless, because both of its entries resolve to one file | live log and listings | L2 |
| Install methods | any method that resolves correctly works | mixed: real folders (the `mb-*` skills, `minimax-*`, `graphify`, `wireframe`, `secure-software-engineering`, `security-audit-methodology`); symlinks to real folders (`archify`, most gstack skills, `i-have-adhd`); one hybrid (`gstack` — a real folder containing symlinks) | live listings | |
| Inventory | — | owned by the skills catalog | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|Skills Catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | |

## Projects

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| What a project is | an opened folder becomes a project | every repository an agent works in is an OpenCode project; the project list and per-project status are owned by repo-organization | [[[mybizz-os-docs:os-reference-docs/repo-organization\|Repo Organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Bind mounts | — | every project is reachable at `~/projects/<name>` through an `/etc/fstab` line with `bind,nofail`; a new project gets a new line | developer-stated; live `~/projects` listing | |
| Registration | opening a folder registers it | `opencode debug config` run from the project folder; it calls no AI model | live check | L6 |
| Per-repo config files | an `opencode.json` in a project root merges with the global config | 7 files: `mb-3-cs-app1`, `mb-3-cs-app3`, `mb-3-cs-app5`, `mb-3-cs-project-library`, `mb-4-ecom-app1`, `mb-4-ecom-app3`, `mb-4-ecom-app5` | live listings | |
| App-repo baseline | — | `default_agent: build`; edit `*: allow` plus `**/anvil.yaml: deny` and theme/template protections (`form_template.yaml`, `parameters.yaml`, `templates.yaml`: `deny`; `theme.css`, `standard-page.html`: `ask`); the 13-pattern bash deny-list; `external_directory *: allow`; a project-local `mcp.graphify` entry pointing at that repo's `graphify-out/graph.json`; `agent.plan.permission.edit: deny` | live project configs | L4 |
| `mb-3-cs-project-library` | — | minimal: `default_agent: plan`; edit `*: allow`; the 13-pattern bash deny-list; `external_directory *: allow`; `agent.plan.permission.edit: deny`; no theme rows, no MCP entry | live project config | L4 |
| No-config repos | — | `mb-4-ecom-project-library` and `pdlf` carry no `opencode.json` | live listings | L4 |
| Merge semantics | configs are merged, not replaced — a project overrides the global config only for conflicting keys, and nested permission maps merge deeply | relied on throughout; a project config cannot silently weaken the global deny-list | https://opencode.ai/docs/config | |

## Web UI

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Start folder | — | the home folder, with `--hostname 0.0.0.0` | developer-stated | |
| Protection | — | `OPENCODE_SERVER_PASSWORD`; the password file is `~/.config/opencode/service.json` (mode 600) and the variable is set in `~/.bashrc` | developer-stated | |
| Project list | — | only real folders inside `/home/dev-p`; links are ignored | developer-stated | L5 |
| Last project | — | reopened whatever folder the server starts from | developer-approved finding | L5 |
| Recents | — | remembered by the browser, not by OpenCode; reset by clearing the browser's site data for `localhost:4096` | developer-approved finding | L5 |

## Session database and maintenance

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Database file | `~/.local/share/opencode/opencode.db` | present, with its `-shm` and `-wal` files | live listing | |
| `workspace` table | the 1.19.0 layout | in the 1.19.0 layout | developer-approved finding | L3 |
| `workspace_v2_layout` table | — | the version-2 layout kept under this name | developer-approved finding | L3 |
| Built-in cleanup | none — the issuer ships no command that deletes stale project rows | MyBizz compensates with `opencode-db-cleanup.sh` (below) | https://github.com/anomalyco/opencode/issues/25004 | |
| Orphaned sessions | sessions keep referencing a renamed or moved folder | MyBizz compensates with the same script | https://github.com/anomalyco/opencode/issues/23248 | |
| `opencode-db-cleanup.sh` | — | `/mnt/c/mybizz/scripts/opencode-db-cleanup.sh`; manual, on demand; full-database backup first; requires a typed capital `YES`; backups to `/mnt/c/backup-wsl/opencode-db-cleanup/<timestamp>/` | developer-approved finding | |
| `opencode-session-prune.sh` | — | `/mnt/c/mybizz/scripts/opencode-session-prune.sh`; Task Scheduler task `OpenCodeSessionPrune`, daily at 17:05; deletes sessions older than 60 days; full-database backup first, dependent rows cleaned through foreign-key discovery, then `VACUUM`; backups to `/mnt/c/backup-wsl/opencode-session-prune/<timestamp>/` | developer-approved finding | |

## WSL hosting

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| WSL distributions | — | one: `Ubuntu`, running, the default | `wsl.exe -l -v` | |
| Windows-triggered commands | — | always pass `-d Ubuntu -u dev-p` to `wsl.exe` | — | |

## Access control

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Read anywhere | governed by `external_directory` | allowed, no prompt — the OpenCode layer | https://opencode.ai/docs/config | |
| Secret-file reads | — | blocked — Cupcake's sensitive-data rules, as standing policy | [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | |
| Write inside the session's project | governed by `edit` | allowed, no prompt — the OpenCode layer | https://opencode.ai/docs/config | |
| Write outside the project | governed by `external_directory` | blocked without a grant; a grant (`mg-grant --path <folder> --count N`) allows it — the Cupcake cross-project rule, as standing policy | [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | |
| Governance writes | — | `AGENTS.md`, `CLAUDE.md`, `opencode.json`, the plugin tree and Cupcake's control plane: blocked, with no grant possible — Cupcake's governance rules, as standing policy | [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | |

## Open items

None.
