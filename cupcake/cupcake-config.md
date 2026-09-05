# Cupcake Configuration — dev-makepdlf

Canonical current-state configuration record. Agent-facing. Reflects the working
state of Cupcake as integrated into the `dev-makepdlf` project as of 2026-08-29.
This document states facts, not history — where a decision was made and the
reasoning matters, see `cupcake-explainer.md`.

---

## Identity

| Item | Value |
|---|---|
| Version | `0.3.0` |
| Binary path | `/home/dev-p/.cupcake/bin/cupcake`, symlinked to `/usr/local/bin/cupcake` |
| Underlying engine | OPA (Open Policy Agent), via `opa` binary at `/usr/local/bin/opa` |
| Harness | `opencode` |
| Global plugin | `~/.config/opencode/plugin/cupcake.js` |
| Global policy folder | `~/.config/cupcake/policies/opencode/` |
| Project-init status | `makepdlf-project-library` only. `mb-3-cs`, `mb4ecom`, `mb5pdlf` deliberately not yet initialized — each will run its own `cupcake init` as part of its own real Step 11, when that project actually starts. |
| Rules-authoring skill | `mb-compile-rules`, corrected 2026-08-28 after live testing |
| Rule source location | `C:\dev\project-library-global\rules-cupcake-global\` |
| Grant commands | `mg-grant`, `mg-revoke` — installed at `~/.config/cupcake/bin/`, on PATH |
| Grants data file | `~/.config/cupcake/policies/opencode/cup-grants-data.rego` — generated, never hand-edited |
| Plugin file (single copy, required) | `~/.config/opencode/plugin/cupcake.js` only. No project-local copy of any kind — see Known scope limitations. |

## Rule library location

| Item | Value |
|---|---|
| Root | `C:\dev\project-library-global\rules-cupcake-global\` |
| File prefix | `cup-` |
| Deployment target (all current rules) | Global — `cupcake.global.policies.(name)` package namespace |

## Live policy inventory — `~/.config/cupcake/policies/opencode/`

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
| `cup-no_cross_project_filesystem_access_by_default.rego` | Writes outside the current project root and outside all permanent exemptions, unless an active, unexpired, non-zero-count grant exists for that folder. Reads outside the project are unrestricted (this rule does not evaluate Read/Grep at all). |
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
| `cupcake_exec_protection.rego` | Blocks the agent from directly executing the `cupcake` binary | **Corrected 2026-08-29** — added `./script.sh` relative-execution matching and shell-function-wrapper matching. See Known scope limitations below for what remains open. |

## The three-layer `task` denial

| Layer | Mechanism | Coverage |
|---|---|---|
| 1 | `opencode.json`: `{"permission": {"task": "deny"}}` | Exact tool name `task` only |
| 2 | `cup-block-task-tool.rego`, checked against `spawn-tools-denylist.json` | Maintained list of known spawn-tool names |
| 3 | Standing skill-review habit, `AGENTS.md` Global safety rules | New/unrecognized spawn-capable tools, human-reviewed before trust |

`spawn-tools-denylist.json` currently lists: `task`, `delegate`, `call_omo_agent`, `agent_session_create`.

## Cross-project access grants — real mechanics

The `no_cross_project_filesystem_access_by_default` rule enforces writes
outside the project via a generated data file, `cup-grants-data.rego`,
regenerated in full by `mg-grant`/`mg-revoke` on every call — never
appended or patched.

**Schema:**
```rego
grants := {
  "<wsl-path>": {"count": N, "expires_at_ns": <epoch-ns, wall-clock>}
}
```

**Division of responsibility, by design:**
- The Rego rule itself does **existence and count checks only** — no time
  comparison happens inside Rego. Reads to a granted folder are allowed
  purely by the entry's existence; writes additionally require `count >
  0`.
- **Expiry is enforced entirely outside Rego**, in the OpenCode plugin's
  `tool.execute.before` hook, using JavaScript's `Date.now()`. Before
  every tool call, the plugin prunes any grant whose `expires_at_ns` has
  passed, regenerating the grants file (with the same `opa check`-before-
  overwrite safety as `mg-grant`/`mg-revoke`) if anything expired.
- **Count decrement happens in the plugin's `tool.execute.after` hook**,
  for write-type tools only (`Write`, `Edit`, `MultiEdit`,
  `NotebookEdit`), after a successful execution — never on a read, never
  on a call outside any grant.

**Safety discipline, applied identically everywhere a grant file is
written** (`mg-grant`, `mg-revoke`, the plugin's prune step, the plugin's
decrement step): write to a `.rego`-suffixed temp file, run `opa check`
on it, only then move it into place. On failure, abort and leave the
previous, known-good file untouched.

## Verified real cupcake eval invocation syntax

```
echo '{"hook_event_name": "PreToolUse", "session_id": "(any)", "cwd": "(real cwd)", "tool": "(tool name, lowercase)", "args": {(camelCase fields)}}' | cupcake eval --harness opencode
```

Confirmed field names for `args`: `filePath`, `oldString`, `newString` (edit/write), `command` (bash), `url` (webfetch/curl target). NOT `tool_name`/`tool_input` — those are Cupcake's internal, post-normalization names, invalid as raw input.

## Known scope limitations (accepted, not defects)

- **`cupcake_exec_protection` cannot see inside a script file's own contents.**
  Only the outer command string is inspected. A forbidden command hidden inside
  a script's body, invoked via `bash script.sh`, is invisible to this builtin.
  Demonstrated live, 2026-08-29. Standing rule recorded in
  `pdlf/judgement-trail.md`: when execution is blocked, stop and hand the
  command to the developer — never construct an indirect path around it.
- **A bare `cupcake` command, no subcommand, is not blocked.** Pre-existing
  gap in `cupcake_exec_protection`, confirmed 2026-08-29, deliberately left
  out of scope pending a dedicated future fix.
- **`AGENTS.md`/`CLAUDE.md`/governance-config protection rules block by
  default, unconditionally** — including a developer-approved edit made in
  the same chat turn. Cupcake cannot verify conversational approval from a
  tool call alone. A genuinely approved edit requires the developer to make
  it directly, or temporarily remove the rule.
- **`package.json` and `opencode.json` protections are whole-file, not
  content-scoped**, except where a rule explicitly targets a specific key
  (e.g. the `mcp` or `permission` blocks). An edit to an unrelated section of
  an otherwise-protected file is still blocked at the file level unless the
  rule specifically excludes it.
- **The offline `opa eval` test harness does not always predict real
  behavior.** Confirmed multiple times, directly: a rule using
  `regex.replace` passed 17/17 offline and failed live (6 of 7 block cases
  silently allowed). Real `cupcake eval` output, run by the developer, is
  the only authoritative test.
- **`opa.runtime().env` and `time.now_ns()` both fail silently in the live
  engine, despite working correctly in the standalone `opa` CLI.** Two
  separate, confirmed instances of the same pattern as `regex.replace`
  above — a rule referencing either produces zero decisions, no error, no
  crash. Neither builtin is usable in any rule targeting this environment.
  Only functions already proven live elsewhere (`regex.match`, `split`,
  `concat`, `startswith`, `endswith`, `contains`, `lower`, plain
  iteration) should be relied on.
- **The OpenCode plugin must exist in exactly one discoverable location.**
  OpenCode's plugin loader does not deduplicate by file identity — a
  symlinked second copy at a project-local path still triggers a second,
  independent load, causing every hook (including the grant
  decrement/prune logic) to fire twice per real event. Confirmed live: a
  byte-identical symlink still produced a double decrement. The only
  correct state is a single real file at
  `~/.config/opencode/plugin/cupcake.js`, with no file or symlink of any
  kind at the project-local `.opencode/plugin/cupcake.js` path.
- **`opa check` silently passes non-`.rego`-suffixed files, even with
  invalid content inside.** Any temp file used to validate generated Rego
  before deployment must end in `.rego`, or the validation step itself
  provides no real protection.

## Do not

- Do not treat an offline `opa eval` pass as sufficient — confirm with real,
  live `cupcake eval` output before marking any rule kept.
- Do not attempt to run `cupcake eval`, `cupcake --debug`, or any direct
  invocation from the agent's own tool context — `cupcake_exec_protection`
  blocks it by design. Hand the exact command to the developer instead.
- Do not construct an indirect path around a `cupcake_exec_protection`
  block — via a wrapper script, shell function, or any other means — for
  any reason, including testing or diagnosis.
- Do not place a drafted `.rego` file at a path whose package name doesn't
  match — a global-namespaced rule in a project-local folder (or vice
  versa) loads without ever firing, silently.
- Do not run `cupcake init` in `mb-3-cs`, `mb4ecom`, or `mb5pdlf` — each
  gets its own real Step 11 when that project actually starts, not before.
- Do not create a project-local copy of `cupcake.js`, symlinked or
  otherwise — exactly one copy must exist, at the global path.
- Do not use `time.*` or `opa.runtime().env` in any rule — both fail
  silently in the live engine.
- Do not hand-edit `cup-grants-data.rego` — always use `mg-grant`/
  `mg-revoke`, which carry the required validate-before-overwrite safety
  check.
