---
title: "opencode-permission-access-control-model"
doc-id: "mb-cefaa6e8"
updated: "2026-10-01"
---
# OpenCode — Permission & Access Control Model

## What this covers

OpenCode's permission system, the second enforcement layer above it
(Cupcake), and the verified per-project configuration across every project
in this ecosystem. This is the access-control layer only. It does not
cover session/database data integrity — see
[[[mybizz-config-docs:opencode/opencode-project-session-data-integrity|Project & Session Data Integrity]]](C:/mybizz/mybizz-config-docs/opencode/opencode-project-session-data-integrity.md) for that.

## The two permission layers — both active, verified 2026-09-09

Two independent enforcement layers sit above the agent's tool calls, and
both were observed firing on real commands on 2026-09-09:

**Layer A — OpenCode's own permission system.** Configured in
`opencode.jsonc` / per-project `opencode.json` via the `permission` keys.
Observed live: an agent bash command matching the `*` pattern was
evaluated and routed to `ask` (the developer's own approval flow), and a
command matching a deny pattern (`rm -rf *`) was refused before execution.

**Layer B — Cupcake.** The policy-enforcement plugin, evaluating every
tool call against the 19 compiled rules — reactivated 2026-09-08 (see
[[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) for the enforcement history and status).

**The division of labor, stated plainly:** OpenCode's permission system is
the interaction gate — it asks the developer or blocks by pattern.
Cupcake is the policy layer — it enforces the written rules
mechanically. Both fire on the same tool call; a command can be denied by
either. Neither is a substitute for the other, and neither was designed to
be.

## The permission model

Each `opencode.json` (one global, one per project) can set:

- **`edit`** — per-file-pattern rule: `"ask"`, `"deny"`. Applies to file
  writes/edits.
- **`webfetch`** — `"ask"` (the global posture).
- **`bash`** — per-command-pattern rule: `"ask"`, `"deny"`, `"allow"`. A
  `"deny"` match is a genuine, verified hard block — confirmed live:
  OpenCode refused an `rm -rf` attempt on a real file, and the file was
  physically confirmed to survive. A `"deny"` pattern also matches the
  COMMAND TEXT itself: a harmless command that merely mentions a deny
  pattern (e.g. listing a folder whose name contains a denied string) is
  refused too (confirmed live 2026-09-09) — rephrase the command rather
  than working around it.
- **`external_directory`** — grants a session access to read/write
  outside its own project folder, per path glob, `"allow"`/`"ask"`/`"deny"`.
- **`agent`** — per-agent overrides. The `plan` agent has `edit: "deny"`
  globally, enforcing the plan/build split. A second configured agent exists:
  `agent.docs-manager`, a read-only docs-scan subagent (mode `subagent`, model
  `openrouter/qwen/qwen3.6-plus`) with `permission.edit: deny` and
  `permission.bash: deny` — it scans, never writes (added to the spec 2026-09-15;
  developer-approved F-5 correction).

## Config precedence — VERIFIED 2026-09-09 (the caveat is closed)

**Configs are merged, not replaced.** Per the upstream documentation
(opencode.ai/docs/config) and verified empirically with `opencode debug
config`: project config overrides global config **only for conflicting
keys**; non-conflicting settings from both survive; nested permission maps
**merge deeply**.

Verified empirically: with the global `permission.bash` map carrying 13
deny patterns and a test project setting `permission.bash: {"*":
"allow"}`, the resolved map contained the project's allow override **and
all 13 global deny patterns** — the deny-list cannot be silently weakened
by a project config.

**One named residue:** a project config *could* explicitly re-declare a
deny pattern (e.g. `"rm -rf *": "allow"`) — that is an explicit, visible
act in a config file, not a silent merge behavior, and it would be a
security review finding if found. No project config in this ecosystem does
this (verified 2026-09-09).

## Current per-project configuration — verified live 2026-09-17

| Project | Status | `opencode.json` | What it carries |
|---|---|---|---|
| `makepdlf-project-library` | Active | Present, verified | plan default; `README.md` instructions; edit ask + anvil.yaml deny; the standard bash deny-list |
| `mb-3-cs` | **Paused** | Present, verified | build default; **project-local Graphify MCP entry**; edit rules incl. **theme/template protections** (`form_template.yaml` deny, `parameters.yaml` deny, `templates.yaml` deny, `theme.css` ask, `standard-page.html` ask); the standard bash deny-list; `external_directory` scoped to `mb-3-cs-project-library` only |
| `mb4ecom`, `mb5pdlf` | **Scaffolding only** | **None** — correct | The folders exist as scaffolding, but the projects do not exist and there is not even a plan for them (developer-confirmed 2026-09-09). Off OpenCode's radar; config is created when a project becomes real |

**Correction history:** the previous version of this document claimed "all
three code repos carry the full deny-list" — false as of this
verification: `mb4ecom` and `mb5pdlf` have no config at all (correct per
the Active Project Standard; the deny-list applies when they start).

## Global configuration — verified live 2026-09-17

Full path: `~/.config/opencode/opencode.jsonc` (WSL path). Verified
key-by-key against [[[mybizz-config-docs:opencode/opencode-config|OpenCode Configuration]]](C:/mybizz/mybizz-config-docs/opencode/opencode-config.md)'s table — exact match. The
`instructions` array points at
`C:/dev/project-library-global/register-global/register-global.md` The use of registers has been discontinued. Please review
(resolves; corrected 2026-09-01 from four deleted index files).

## Problem / remedy reference

**Symptom:** a permission grant or index-file pointer silently has no
effect, even though the JSON looks syntactically correct.
**Cause:** the path in the config points at a folder that no longer
exists (e.g. a stale root like `C:\projects\...` after a rename to
`C:\dev\...`).
**Remedy:** always verify a path in `opencode.json` actually resolves
(`Test-Path` in PowerShell, or `[ -d ... ]` in WSL bash) before trusting
that the permission/instruction it configures is active. A config file
saving correctly is not evidence that its content is correct.

**Symptom:** a command is refused and the denial names an OpenCode
permission pattern, though the action seemed legitimate.
**Cause:** the deny patterns match the command TEXT — a harmless command
that merely mentions a denied string (a path name, a file listing) is
refused too (confirmed live 2026-09-09).
**Remedy:** rephrase the command so its text no longer matches the deny
pattern — this is legitimate, because the pattern matched only
incidentally and no forbidden action was intended. If the pattern match
was on the action's real substance, the refusal is correct: stop.

**Symptom:** inconsistent per-project permission coverage across repos.
**Cause:** deny-lists were added ad hoc per repo over time without a
shared baseline.
**Remedy:** any new project added to this ecosystem gets the standard
bash deny-list and external_directory scoping at creation — the
`makepdlf-project-library` config is the working template.

---

*End of document*
