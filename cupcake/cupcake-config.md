# Cupcake Configuration

Canonical current-state configuration record. Agent-facing. Reflects the
live-verified state as of 2026-09-06. This document states facts, not history —
where a decision was made and the reasoning matters, see
`cupcake-explainer.md`; for operational commands and procedures, see
`cupcake-reference.md`.

---

## Current operational status — SUSPENDED, total (verified 2026-09-06)

**Cupcake enforcement is currently OFF.** The plugin file was renamed out of
its discoverable location:

```
~/.config/opencode/plugin/cupcake.js → ~/.config/opencode/plugin/cupcake.js.disabled
```

OpenCode no longer loads the plugin — no tool call is intercepted or evaluated.
**None of the protections below (the 19 custom rules, the 3 builtins, the
Cupcake half of the task-tool denial, the cross-project grant system) are
currently active.** Every tool call proceeds with no Cupcake check of any kind.

**Verified component state (nothing deleted):**

| Component | Verified state 2026-09-06 |
|---|---|
| Plugin | `cupcake.js.disabled` (19,601 B, modified 2026-08-31) at the plugin path; an earlier backup `cupcake.js.bak-2026-08-31T095850+0200` (11,155 B) alongside it |
| Binaries | `cupcake` (18.4 MB) and `opa` (47.4 MB) at `~/.cupcake/bin/`; `/usr/local/bin/cupcake` symlink intact |
| Global policy folder | Intact — 19 custom rules + `cup-grants-data.rego` + `builtins/` (3) + `system/` (aggregator) |
| Rule sources | 19 `.md` source documents at `C:\dev\project-library-global\rules-cupcake-global\` |
| Grant commands | `mg-grant` / `mg-revoke` present at `~/.config/cupcake/bin/` |
| Grants data | **Empty** — `grants := {}` (verified 2026-09-06) |
| Layer-1 `task: deny` | **Still active** — `"task": "deny"` in OpenCode config (independent of the suspended plugin) |
| Suspected crash cause | `.cupcake/policies/opencode/example.rego` (923 B, `cupcake init` scaffold, never validated) **confirmed present** in `makepdlf-project-library`, alongside the full init scaffold |

**Re-enable is a one-line reverse of the rename:**

```bash
mv ~/.config/opencode/plugin/cupcake.js.disabled ~/.config/opencode/plugin/cupcake.js
```

**A full, permanent uninstall has been prepared but NOT executed** — see
`cupcake-reference.md`'s "Full uninstall" section, held pending an explicit
developer decision on restore, repair, or permanent removal.

**Standing context (developer-stated, 2026-09-06):** the current setup proved
too restrictive — hampering work to the point of totally arresting
productivity; this is a real issue. The suspension is a **temporary state**
until the setup can be optimized so that security and productivity coincide.
As of this writing:

> No reasonable solution has been found and applied yet — Cupcake remains in
> total suspension. A candidate fix (fail-open mode + project-local scaffold
> cleanup) has been identified and is now confirmed to exist in the installed
> plugin's actual code, not merely claimed by vendor documentation — but it
> has not been applied or tested against the real crash. Until it is, this
> remains an open problem, not a resolved one.

**Everything below this point describes the configuration as it stood while
Cupcake was active** (as of 2026-08-29) — retained as a real record of what
would need to be restored if re-enabled, not as a description of current live
behavior.

---

## Identity

| Item | Value |
|---|---|
| Version | `0.3.0` — recorded from the original build record; no upstream release listing is visible to corroborate it (binary installed 2026-08-27) |
| Upstream | `github.com/eqtylab/cupcake` — "A native policy enforcement layer for AI coding agents. Built on OPA/Rego."; Apache-2.0; Trail of Bits credited for agentic safety research support; OpenCode fully supported among multi-harness integrations (all verified upstream 2026-09-06) |
| Binary path | `/home/dev-p/.cupcake/bin/cupcake`, symlinked to `/usr/local/bin/cupcake` |
| Underlying engine | OPA (Open Policy Agent), via `opa` binary at `/usr/local/bin/opa` |
| Harness | `opencode` |
| Global plugin | `~/.config/opencode/plugin/cupcake.js` — **currently renamed `.disabled`** (see status above) |
| Global policy folder | `~/.config/cupcake/policies/opencode/` |
| Project-init status | `makepdlf-project-library` only. `mb-3-cs`, `mb4ecom`, `mb5pdlf` deliberately not yet initialized — each gets its own real Step 11 when that project actually starts |
| Rules-authoring skill | `mb-compile-rules`, corrected 2026-08-28 after live testing |
| Rule source location | `C:\dev\project-library-global\rules-cupcake-global\` |
| Grant commands | `mg-grant`, `mg-revoke` — installed at `~/.config/cupcake/bin/`, on PATH |
| Grants data file | `~/.config/cupcake/policies/opencode/cup-grants-data.rego` — generated, never hand-edited; currently empty |
| Plugin file (single copy, required) | `~/.config/opencode/plugin/cupcake.js` only, once re-enabled. No project-local copy of any kind — see Known scope limitations |

## Rule library location

| Item | Value |
|---|---|
| Root | `C:\dev\project-library-global\rules-cupcake-global\` |
| File prefix | `cup-` |
| Deployment target (all current rules) | Global — `cupcake.global.policies.(name)` package namespace |

## Live policy inventory — `~/.config/cupcake/policies/opencode/` (counts verified 2026-09-06)

| Item | Count |
|---|---|
| Custom rules, total | 19 |
| — Pre-existing (before 2026-08-29) | 2 |
| — Built and deployed 2026-08-29 | 17 |
| Builtins | 3 |
| Aggregator (not a rule) | `system/evaluate.rego` |

### Custom rules — pre-existing

| File | Blocks |
|---|---|
| `cup-block-task-tool.rego` | The `task` tool and known spawn-tool equivalents |
| `cup-block-anvil-yaml-writes.rego` | Any write to `anvil.yaml`, any Anvil project |

### Custom rules — built 2026-08-29

| File | Blocks |
|---|---|
| `cup-no_test_tampering.rego` | Deleting/skipping/gutting a test file |
| `cup-no_verification_tampering.rego` | Writes to CI/CD, test-runner, coverage-threshold config |
| `cup-no_disabling_security_tooling.rego` | Writes to security-tooling config (audit, SAST, secret-scan, pre-commit) |
| `cup-no_suppression_directives_without_approval.rego` | Adding a lint/type-check suppression directive |
| `cup-no_dependency_or_lockfile_changes_without_explicit_approval.rego` | Writes to known lockfiles |
| `cup-no_unverified_dependencies.rego` | Installing a new package via any of 10 package managers |
| `cup-no_autonomous_commits_pushes_merges_releases_or_deployments.rego` | git commit/push/merge, publish, deploy-script execution |
| `cup-no_rewriting_or_destroying_development_history.rego` | Force-push, rebase, amend, branch/tag deletion |
| `cup-no_destructive_database_operations.rego` | DROP, unconditioned DELETE, TRUNCATE (9 object types) |
| `cup-no_cross_project_filesystem_access_by_default.rego` | Writes outside the current project root and outside all permanent exemptions, unless an active, unexpired, non-zero-count grant exists for that folder. Reads outside the project are unrestricted |
| `cup-no_access_to_secrets_unless_explicitly_required.rego` | Reading known secret-file patterns, via Read/Grep or bash |
| `cup-outbound_network_access_is_allowlist_only.rego` | Fetch/curl/wget to a domain not on the 10-domain allowlist |
| `cup-no_autonomous_installation_or_connection_of_tools.rego` | Registering a new MCP server, plugin, or skill |
| `cup-no_unapproved_executable_or_build_path_changes.rego` | Writes to CI workflows, Dockerfile, deploy config, `package.json` |
| `cup-protected_ai_governance_files_may_not_be_modified.rego` | Any write to `AGENTS.md` or `CLAUDE.md` |
| `cup-unexpected_instruction_shaped_files_must_be_treated_as_suspicious.rego` | Creating a new `SKILL.md` outside known skill locations |
| `cup-the_ai_may_never_weaken_the_controls_governing_itself.rego` | Writes to `opencode.json` permissions, `spawn-tools-denylist.json` |

### Builtins

| File | Purpose | Status |
|---|---|---|
| `system_protection.rego` | Blocks access to critical system paths | Default, unmodified |
| `sensitive_data_protection.rego` | Blocks access to credential/secret-shaped files | **Corrected 2026-08-29** — SSH-key matching changed from substring to exact-basename, closing a real false positive on `*.pub` public keys |
| `cupcake_exec_protection.rego` | Blocks the agent from directly executing the `cupcake` binary | **Corrected 2026-08-29** — added relative-execution and shell-function-wrapper matching. See Known scope limitations for what remains open |

## The three-layer `task` denial — with current per-layer status

| Layer | Mechanism | Coverage | Status 2026-09-06 |
|---|---|---|---|
| 1 | OpenCode config: `"task": "deny"` | Exact tool name `task` | **ACTIVE** (verified in config) |
| 2 | `cup-block-task-tool.rego`, checked against `spawn-tools-denylist.json` | Maintained list of known spawn-tool names | **INACTIVE** while Cupcake is suspended |
| 3 | Standing skill-review habit, `AGENTS.md` Global safety rules | New/unrecognized spawn-capable tools, human-reviewed before trust | **STANDING** |

`spawn-tools-denylist.json` currently lists: `task`, `delegate`, `call_omo_agent`, `agent_session_create`.

## Cross-project access grants — real mechanics

The `no_cross_project_filesystem_access_by_default` rule enforces writes
outside the project via a generated data file, `cup-grants-data.rego`,
regenerated in full by `mg-grant`/`mg-revoke` on every call — never appended
or patched.

**Schema:**
```rego
grants := {
  "<wsl-path>": {"count": N, "expires_at_ns": <epoch-ns, wall-clock>}
}
```

**Division of responsibility, by design:**
- The Rego rule itself does **existence and count checks only** — no time
  comparison happens inside Rego. Reads to a granted folder are allowed
  purely by the entry's existence; writes additionally require `count > 0`.
- **Expiry is enforced entirely outside Rego**, in the OpenCode plugin's
  `tool.execute.before` hook, using JavaScript's `Date.now()`. Before every
  tool call, the plugin prunes any expired grant, regenerating the grants
  file (with the same `opa check`-before-overwrite safety as
  `mg-grant`/`mg-revoke`) if anything expired.
- **Count decrement happens in the plugin's `tool.execute.after` hook**, for
  write-type tools only, after successful execution — never on a read, never
  outside any grant.

**Safety discipline, applied identically everywhere a grant file is written:**
write to a `.rego`-suffixed temp file, run `opa check` on it, only then move
it into place. On failure, abort and leave the previous, known-good file
untouched.

## Verified real cupcake eval invocation syntax

```
echo '{"hook_event_name": "PreToolUse", "session_id": "(any)", "cwd": "(real cwd)", "tool": "(tool name, lowercase)", "args": {(camelCase fields)}}' | cupcake eval --harness opencode
```

Confirmed field names for `args`: `filePath`, `oldString`, `newString`
(edit/write), `command` (bash), `url` (webfetch). NOT `tool_name`/`tool_input`
— those are Cupcake's internal, post-normalization names, invalid as raw input.

## Known scope limitations (accepted, not defects)

- **`cupcake_exec_protection` cannot see inside a script file's own contents.**
  Only the outer command string is inspected. A forbidden command hidden
  inside a script's body, invoked via `bash script.sh`, is invisible.
  Demonstrated live, 2026-08-29. Standing rule recorded in the judgment trail:
  when execution is blocked, stop and hand the command to the developer —
  never construct an indirect path around it.
- **A bare `cupcake` command, no subcommand, is not blocked.** Pre-existing
  gap, confirmed 2026-08-29, deliberately left out of scope.
- **`AGENTS.md`/`CLAUDE.md`/governance-config protection rules block by
  default, unconditionally** — including a developer-approved edit made in the
  same chat turn. Cupcake cannot verify conversational approval from a tool
  call alone.
- **`package.json` and `opencode.json` protections are whole-file, not
  content-scoped**, except where a rule explicitly targets a specific key.
- **The offline `opa eval` test harness does not always predict real
  behavior** — `regex.replace` passed 17/17 offline and failed live. Real
  `cupcake eval` output, run by the developer, is the only authoritative test.
- **`opa.runtime().env` and `time.now_ns()` fail silently in the live engine**,
  despite working in the standalone `opa` CLI. Only functions already proven
  live elsewhere should be relied on in any new rule.
- **The OpenCode plugin must exist in exactly one discoverable location** —
  the loader does not deduplicate by file identity; even a symlinked second
  copy loads independently and double-fires every hook. Confirmed live.
- **`opa check` silently passes non-`.rego`-suffixed files** — any validation
  temp file must end in `.rego`.

## Open items

| # | Item | Status |
|---|---|---|
| 1 | The standing design problem: a Cupcake configuration where security and productivity coincide. No reasonable solution has been found and applied yet — Cupcake remains in total suspension (developer-stated, 2026-09-06). | Open |
| 2 | Candidate fix — `failMode: "open"` via `.cupcake/opencode.json` plus project-local scaffold cleanup: **code-verified to exist** in the installed plugin (`failMode` in its default config and real `"open"` handling; config path `.cupcake/opencode.json` verified in its `loadConfig`), but **not applied or tested against the real crash**. | Open |
| 3 | Version `0.3.0` has no visible upstream release listing to corroborate it. | Open |
| 4 | Full uninstall prepared, not executed — restore/repair/remove decision pending. | Open |
