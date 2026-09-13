---
document: "Cupcake Configuration"
doc-id: cupcake-config
state: Live
date-created: 2026-09-05
---

# Cupcake Configuration

Canonical current-state configuration record. Agent-facing. Reflects the
live-verified state as of 2026-09-13. This document states facts, not history —
where a decision was made and the reasoning matters, see
`cupcake-explainer.md`; for operational commands and procedures, see
`cupcake-reference.md`.

---

## Current operational status — ACTIVE (verified 2026-09-12)

**Cupcake is active and enforcing.** Verified live 2026-09-12: exec-protection
blocked a real agent tool call immediately after session restart; every policy
file compiles cleanly; the full hook chain fires correctly on every tool call.

**Operational history — key events:**

| Date | Event |
|---|---|
| 2026-08-29 | 19 custom rules built, tested, and deployed in a single session |
| 2026-09-06 | Total evaluation crash during ordinary work — every tool call failed. Root cause: an unvalidated scaffold file in the project-local policy folder. Fail-open mode applied; scaffold removed. See `cupcake-explainer.md` §7F for the full account. |
| 2026-09-08 | Cross-folder rule amended (three-tier design); full 13/13 live test passed — record: `/mnt/c/mybizz/logs/cupcake-rule-test-record-2026-09-08.md` |
| 2026-09-12 | Root cause of silent fail-open found and fixed: the plugin was spawning the checker without a working directory, so the checker looked for its rules in OpenCode's launch folder (not the project). One-line plugin fix (`cwd: event.cwd` in Bun.spawn). Live block confirmed immediately after restart. |
| 2026-09-12 | **Bash-governance rule placed and live-verified** — the shell write channel (python/perl heredoc and -c/-e write execution, `sed -i`, `>`/`>>` redirects, `tee`, `cp`/`mv`/`ln` destination, `rm`/`touch`/`truncate` operands, `dd of=`) now feeds the same outside-project boundary, exempt list, grant slips, and first-instance deny. Final live run 35/35 — record: `/mnt/c/mybizz/logs/cupcake-rule-test-record-2026-09-12.md` |
| 2026-09-12 | `system_protection` builtin bash matcher corrected — its substring match on `/dev/` halted every command referencing the `/mnt/c/dev/` project tree, `/dev/null` redirects, and cross-project reads (6 false blocks proven by the same test sheet). Indicators now anchored to real path starts; `/dev/null` stream family exempted; sudo/doas and true system prefixes unchanged. Offline 27/27. |

The protected-file rules (AGENTS.md/CLAUDE.md/opencode.json/package.json)
are deliberately left strict — a revisit decision, not forgotten.

---

## Identity

| Item | Value |
|---|---|
| Version | `0.3.0` — recorded from the original build record; no upstream release listing is visible to corroborate it (binary installed 2026-08-27) |
| Upstream | `github.com/eqtylab/cupcake` — "A native policy enforcement layer for AI coding agents. Built on OPA/Rego."; Apache-2.0; Trail of Bits credited for agentic safety research support; OpenCode fully supported among multi-harness integrations (all verified upstream 2026-09-06) |
| Binary path | `/home/dev-p/.cupcake/bin/cupcake`, symlinked to `/usr/local/bin/cupcake` |
| Underlying engine | OPA (Open Policy Agent). Canonical binary: `/usr/local/bin/opa` (v1.19.1, real file). `/home/dev-p/.cupcake/bin/opa` is a symlink to it — both resolve to the same binary. |
| Harness | `opencode` |
| Global plugin | `~/.config/opencode/plugin/cupcake.js` — **active**. Backup set (all correctly non-`.js`-suffixed, never loaded): plugin `.bak-20260912` + `.bak-2026-08-31T095850+0200` (same folder); policy-folder `.bak-*` rego backups: cross-project ×4 (`.bak-2026-08-31T095850+0200`, `.bak-20260908`, `.bak-20260908-2`, `.bak-20260912`), outbound-network ×1 (`.bak-20260908`); builtins `system_protection.rego.bak-20260912` ×1. Inventoried live 2026-09-13 |
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

## Live policy inventory — `~/.config/cupcake/policies/opencode/` (counts inventoried 2026-09-13)

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
| `cup-no_cross_project_filesystem_access_by_default.rego` | **Amended 2026-09-08, three-tier design, live-tested 13/13:** writes outside the current project are blocked unless the target is inside an always-open shared-library folder (project-library-global, dev-root, mybizz-config-docs, mybizz-os-docs, `/mnt/c/mybizz/logs`, `/tmp`, the Cupcake/OpenCode config plane, skills-collective) or an active, non-zero-count grant exists. **Reads are never blocked by this rule.** Restricted project folders (the seven projects + `/home/dev-p/memory-governor`) are slip-gated. **Amended again 2026-09-12:** Bash-mediated write-shapes appended to the same file/package (python/perl heredoc and -c/-e write execution, `sed -i`, `>`/`>>` redirects, `tee`, `cp`/`mv`/`ln` destination, `rm`/`touch`/`truncate` operands, `dd of=`) — same boundary, same grants, own rule id, first-instance deny. Live-tested 35/35 over three runs |
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
| `system_protection.rego` | Blocks access to critical system paths | **Bash matcher corrected 2026-09-12** — indicators anchored to real path starts; `/dev/null` stream family exempted; the file-tool path check is unchanged. Backup `.bak-20260912` |
| `sensitive_data_protection.rego` | Blocks access to credential/secret-shaped files | **Corrected 2026-08-29** — SSH-key matching changed from substring to exact-basename, closing a real false positive on `*.pub` public keys |
| `cupcake_exec_protection.rego` | Blocks the agent from directly executing the `cupcake` binary | **Corrected 2026-08-29** — added relative-execution and shell-function-wrapper matching. See Known scope limitations for what remains open |

## The three-layer `task` denial — with current per-layer status

| Layer | Mechanism | Coverage | Status 2026-09-06 |
|---|---|---|---|
| 1 | OpenCode config (`~/.config/opencode/opencode.jsonc` — note `.jsonc`): `"task": "deny"` | Exact tool name `task` | **ACTIVE** (verified in config) |
| 2 | `cup-block-task-tool.rego`, checked against `spawn-tools-denylist.json` | Maintained list of known spawn-tool names | **ACTIVE** |
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
  outside any grant. **Scope clarified 2026-09-13, developer-accepted as intended
  design:** decrement fires for **file-tool writes** (proven live: count 2→1→0,
  then denial at exhaustion); **Bash-mediated writes within a granted path are
  permitted WITHOUT decrement until grant expiry** — the bash-governance rule
  still enforces the boundary via denial for ungranted paths, and grant expiry
  bounds exposure. Verified live 2026-09-13 (three bash redirects left count
  untouched; file-tool writes decremented correctly).

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

- **The checker requires a project skeleton in the folder it is launched from.**
  The plugin spawns the checker with `cwd: event.cwd` (the session's project
  directory) — fixed 2026-09-12. Before the fix, the checker used OpenCode's
  launch directory instead, which lacked the skeleton and crashed every call.
  Every project folder an agent session runs in still needs the
  `.cupcake/policies/opencode` + `.cupcake/system` skeleton — create it before
  working in any new project. **failMode does not cover an init failure** —
  it only covers evaluation crashes that happen after the engine boots.

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
| 1 | Protected-file rules (AGENTS.md/CLAUDE.md/opencode.json/package.json) block by default — including developer-approved edits made in the same chat turn. Friction accepted as a deliberate revisit decision. | Partially open |
| 2 | Plugin silent-fail root cause found and fixed 2026-09-12: checker was spawned without a working directory. Fix: `cwd: event.cwd` in Bun.spawn. Live block confirmed. | Resolved |
| 3 | Version `0.3.0` has no visible upstream release listing to corroborate it. | Open |
| 4 | Full uninstall prepared — superseded by the reactivation decision. Held as a record only. | Retired |
