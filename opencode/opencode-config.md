---
title: "opencode-config"
doc-id: "mb-c7616d53"
updated: "2026-10-05"
---
# OpenCode Configuration

Canonical current-state configuration record. Agent-facing. Reflects the
verified live state as of 2026-09-09. This document is part one of the
five-part OpenCode suite; each file owns one scope:

| File | Owns |
|---|---|
| `opencode-config.md` (this file) | Configuration state, environment position, active projects |
| [[[mybizz-config-docs:opencode/opencode-reference\|Commands, Verification, Troubleshooting]]](C:/mybizz/mybizz-config-docs/opencode/opencode-reference.md) | Procedures: inspection, restart, verification, recovery |
| [[[mybizz-config-docs:opencode/opencode-permission-access-control-model\|Permission & Access Control Model]]](C:/mybizz/mybizz-config-docs/opencode/opencode-permission-access-control-model.md) | The permission layers and their verified behavior |
| [[[mybizz-config-docs:opencode/opencode-project-session-data-integrity\|Project & Session Data Integrity]]](C:/mybizz/mybizz-config-docs/opencode/opencode-project-session-data-integrity.md) | The session database and its maintenance |
| [[[mybizz-config-docs:opencode/opencode-explainer\|OpenCode Explainer]]](C:/mybizz/mybizz-config-docs/opencode/opencode-explainer.md) | Mechanics, real incidents, design reasoning |

---

## Identity

| Item | Value |
|---|---|
| Version | 1.15.12 (verified live 2026-09-09) |
| Upstream | `github.com/anomalyco/opencode` |
| Global config | `~/.config/opencode/opencode.jsonc` — the only global config file (consolidated from two, 2026-09-01) |
| Config precedence | **Verified 2026-09-09 against the upstream documentation and empirically via `opencode debug config`**: configs are **merged, not replaced** — project config overrides global only for conflicting keys, non-conflicting settings from both are preserved, and nested permission maps merge deeply (see the permission model document for the verified test). Project config has the highest precedence among standard config files. |
| Harness role | OpenCode is the harness spanning every environment layer (see [[[pdlf:pdlf-library/pdlf-explainer-docs/pdlf-environment-explainer\|the pre-makePDLF, makePDLF, PDLF, and shipped layers]]](C:/pdlf/pdlf-library/pdlf-explainer-docs/pdlf-environment-explainer.md)) — the pre-makePDLF supporting systems run inside or beside it, the makePDLF layer builds the PDLF application in it, and the PDLF layer builds the shipped estate through it |
| WSL distro (real, active) | `Ubuntu` — **not** the default (`Ubuntu-22.04`, stopped). Any Windows-triggered command invoking `wsl.exe` must explicitly pass `-d Ubuntu -u dev-p` |

## Global config — real, current content (verified key-by-key 2026-09-09; re-verified via run #1 developer bundle 2026-09-15)

| Key | Value |
|---|---|
| `default_agent` | `plan` |
| `instructions` | the instructions array does not reference any register file |
| `permission.task` | `deny` — Layer 1 of the three-layer `task`-denial system, see [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) |
| `permission.edit` | `ask` by default; `**/anvil.yaml` explicitly `deny` |
| `permission.webfetch` | `ask` |
| `permission.bash` | `ask` by default; explicit `deny` on destructive git operations, `DROP`/`TRUNCATE` SQL patterns, and `curl`/`wget` piped directly to a shell (13 patterns in the live map — verified 2026-09-15) |
| `permission.external_directory` | `allow` for `C:\mybizz\**`, `C:\dev\**`, `C:\pdlf\**`, `C:\data-mybizz-mgt\**` (4th root added to spec 2026-09-15 — developer-approved F-4 correction) |
| `agent.plan.permission.edit` | `deny` — Plan agent cannot write, by design |
| `mcp.gbrain` | Local MCP server, `gbrain serve`, real API keys passed via environment (`{env:...}` placeholders — no literals in config, verified 2026-09-15) |

## The global `AGENTS.md`

`~/.config/opencode/AGENTS.md` (~16.2 KB, measured 2026-09-15; the 14.4 KB figure of
2026-09-09 grew with the session-close routine and fact-save guidance) — the
global behavioral-rules file OpenCode loads for every session. Present and
verified 2026-09-09; re-verified 2026-09-15.

## Plugin state

| Plugin | State 2026-09-09 |
|---|---|
| `cupcake.js` | **Active** (reactivated 2026-09-08 from `.disabled`; exactly one discoverable copy; a non-discovered `.bak` alongside — see the permission model document for the dedup rule) |

## Skill discovery — real, confirmed methods (not uniform)

| Skill-set | Real install method |
|---|---|
| Custom skills (`mb-*`) | Plain, real folders — no symlink |
| Anvil, Archify, most GStack skills | Symlink to a real folder elsewhere on the same drive |
| GStack (top-level) | Hybrid — real folder containing further symlinks to individual skills |
| Magdoub wireframe skill | Two-hop — empty intermediate folder pointing to real content in `~/.claude/skills/` |
| `secure-software-engineering` | Plain, real folder (installed 2026-09-09 from `github.com/magnus919/agent-skills`) |

Full, current skill inventory by owner: [[[mybizz-os-docs:os-reference-docs/skills-catalog|Skills Catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md). Full GStack-specific detail: [[[mybizz-config-docs:gstack/gstack-config|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md).

## Active Project Standard

| Status | Meaning | Config expectation |
|---|---|---|
| **Active** | Currently being built | Full, real `opencode.json` |
| **Paused** | Real, deliberate prior work exists; correctly waiting on a known, real prerequisite before resuming | Real config retained — represents genuine prior work, not mistaken for the current active standard |
| **Never started** | No real work has begun; **scaffolding only** (e.g. `mb4ecom`, `mb5pdlf` — folders present, no plan, off OpenCode's radar) | Zero configuration — any config found here is presumed stale by default |

**Current real project status:**

| Project | Status | Notes |
|---|---|---|
| `makepdlf-project-library` | Active | |
| `mb-3-cs` / `mb-3-cs-project-library` | **Paused** | Real, deliberate — genuine prior setup exists (including a project-local Graphify MCP entry and theme/template edit protections), correctly waiting on PDLF's own completion before resuming |
| `mb4ecom`, `mb5pdlf` | **Scaffolding only — off OpenCode's radar** | Developer-confirmed 2026-09-09: the folders exist as scaffolding, but the projects do not exist and there is not even a plan for them. No config present (verified), and none should be created until the projects become real |
| `project-template` | Template scaffold | Contains literal, unsubstituted `{SLUG}` placeholders by design — not a real project |

## Known scope limitations

- **No native session-start hook.** The session-start checklist is human-run, pasted manually — not a technical OpenCode mechanism.
- **No skill-identity field reaches any plugin.** Per-skill permission rules are not currently possible — confirmed against OpenCode's own real source, not assumed.
- **Plugin deduplication is by discovery path, not file identity.** A plugin must be discoverable from exactly one path.

## Do not

- Do not edit a plugin's code and expect it to take effect without a
  full OpenCode restart — changes are only read at process start.
- Do not create a second discoverable path for any plugin already
  installed — even a symlink to the identical file causes double-loading.
- Do not create a WSL-side symlink pointing at a Windows-drive target —
  confirmed unreadable by Windows Explorer. Create it from the Windows
  side instead (`mklink /D`), with Developer Mode enabled.
- Do not invoke `wsl.exe` from a Windows-triggered command without
  explicitly specifying `-d <distro> -u dev-p` — this machine has two
  WSL distributions installed.
- Do not treat a "Paused" project's existing configuration as stale —
  only "Never started" projects default to zero configuration.
- Do not assume project config replaces global config — they merge;
  conflicting keys go to the project, non-conflicting keys from both
  survive (verified 2026-09-09).
