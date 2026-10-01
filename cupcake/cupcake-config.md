---
title: "cupcake-config"
doc-id: "mb-afd0ad78"
updated: "2026-10-01"
---
# Cupcake Configuration

Canonical current-state configuration record. Agent-facing. Reflects the
live-verified state as of 2026-09-13. This document states facts, not history —
where a decision was made and the reasoning matters, see
[[[mybizz-config-docs:cupcake/cupcake-explainer|Mechanical Policy Enforcement for AI Coding Agents]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-explainer.md); for operational commands and procedures, see
[[[mybizz-config-docs:cupcake/cupcake-reference|Usage, Invocation, and Worked Examples]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-reference.md).

---

## Current operational status — ACTIVE (set-and-forget amendment live-verified 2026-09-22)

**Cupcake is active and enforcing everywhere, with no per-folder preparation.**
Verified live 2026-09-22: the set-and-forget amendment (fail-open default +
global-only fallback home) proven by ten consecutive tool calls from a
never-initialized folder, each evaluated clean under enforcement.

**Operational history — key events:**

| Date | Event |
|---|---|
| 2026-08-29 | 19 custom rules built, tested, and deployed in a single session |
| 2026-09-06 | Total evaluation crash during ordinary work — every tool call failed. Root cause: an unvalidated scaffold file in the project-local policy folder. Fail-open mode applied; scaffold removed. See [[[mybizz-config-docs:cupcake/cupcake-explainer\|Mechanical Policy Enforcement for AI Coding Agents]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-explainer.md) §7F for the full account. |
| 2026-09-08 | Cross-folder rule amended (three-tier design); full 13/13 live test passed — record: `/mnt/c/mybizz/logs/cupcake-rule-test-record-2026-09-08.md` |
| 2026-09-12 | Root cause of silent fail-open found and fixed: the plugin was spawning the checker without a working directory, so the checker looked for its rules in OpenCode's launch folder (not the project). One-line plugin fix (`cwd: event.cwd` in Bun.spawn). Live block confirmed immediately after restart. |
| 2026-09-12 | **Bash-governance rule placed and live-verified** — the shell write channel (python/perl heredoc and -c/-e write execution, `sed -i`, `>`/`>>` redirects, `tee`, `cp`/`mv`/`ln` destination, `rm`/`touch`/`truncate` operands, `dd of=`) now feeds the same outside-project boundary, exempt list, grant slips, and first-instance deny. Final live run 35/35 — record: `/mnt/c/mybizz/logs/cupcake-rule-test-record-2026-09-12.md` |
| 2026-09-12 | `system_protection` builtin bash matcher corrected — its substring match on `/dev/` halted every command referencing the `/mnt/c/dev/` project tree, `/dev/null` redirects, and cross-project reads (6 false blocks proven by the same test sheet). Indicators now anchored to real path starts; `/dev/null` stream family exempted; sudo/doas and true system prefixes unchanged. Offline 27/27. |
| 2026-09-22 | **Set-and-forget amendment — second total evaluation crash fixed permanently.** Launching from a never-initialized folder blocked every tool call (checker init failure; `failMode: closed` did not cover init). Plugin amended: `failMode: open` is the environment default; sessions in folders without a `.cupcake` skeleton fall back to the global-only home `~/.config/cupcake/fallback` (WARN-logged per call). Every skeleton guaranteed boot-safe by the input-gated `cup-noop-fallback.rego` placeholder (OPA v1.19.1 wasm compiler panics on an aggregator-only bundle — proven by controlled `opa build` tests). Live-verified: ten consecutive calls from the skeleton-less folder evaluated clean. |

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
| Global plugin | `~/.config/opencode/plugin/cupcake.js` — **active**, carrying the 2026-09-22 set-and-forget amendment (`failMode: open` default; missing-skeleton fallback to `~/.config/cupcake/fallback`). Backup set (all correctly non-`.js`-suffixed, never loaded): plugin `.bak-20260922-pre-amendment` + `.bak-20260912` + `.bak-2026-08-31T095850+0200` (same folder); policy-folder `.bak-*` rego backups: cross-project ×4 (`.bak-2026-08-31T095850+0200`, `.bak-20260908`, `.bak-20260908-2`, `.bak-20260912`), outbound-network ×1 (`.bak-20260908`); builtins `system_protection.rego.bak-20260912` ×1. Inventoried live 2026-09-13; plugin backup set updated 2026-09-22 |
| Global policy folder | `~/.config/cupcake/policies/opencode/` |
| Fallback home (2026-09-22) | `~/.config/cupcake/fallback/.cupcake/` — global-only skeleton (empty `policies/opencode` + input-gated `cup-noop-fallback.rego` placeholder, `system/evaluate.rego`, `helpers/commands.rego`, `rulebook.yml`, `opencode.json`), built by selective copy from the proven makepdlf scaffold after `cupcake init` stalled interactively; boot-verified live |
| Project-init status | Eight folders initialized (makepdlf-project-library, mb-3-cs, mb-3-cs-project-library, mb4ecom, mb4ecom-project-library, mb5pdlf, mb5pdlf-project-library, mybizz-config-docs); the set-and-forget amendment makes initialization **optional everywhere** — skeleton-less folders evaluate global policies only via the fallback home. Every skeleton guaranteed boot-safe by the input-gated placeholder (an empty `policies/opencode` panics the OPA wasm compiler on the aggregator-only bundle) |
| Rules-authoring skill | `mb-compile-rules`, corrected 2026-08-28 after live testing |
| Rule source location | `C:\dev\project-library-global\rules-cupcake-global\` |
| Grant commands | `mg-grant`, `mg-revoke` (path slips), `git-grant` (commit allowances, WP3 2026-09-22) — installed at `~/.config/cupcake/bin/`, on PATH; developer-terminal only, the agent never executes them |
| Grants data file | `~/.config/cupcake/policies/opencode/cup-grants-data.rego` — generated, never hand-edited; four active grants as of 2026-09-21 (data-mybizz-mgt, dev, pdlf, memory-governor; counts 40–60) |
| Git grants data file (WP3 2026-09-22) | `~/.config/cupcake/policies/opencode/cup-git-grants-data.rego` — commit allowances generated by `git-grant --repo <folder> --count N --minutes M`; same generated-never-hand-edited discipline; absent file = no allowances = commits deny (fail-closed) |
| Plugin file (single copy, required) | `~/.config/opencode/plugin/cupcake.js` only, once re-enabled — **WP3 amendment 2026-09-22:** prunes and decrements BOTH grants files (path slips and commit allowances). No project-local copy of any kind — see Known scope limitations. Backup set: `.bak-20260922-pre-wp3` (pre-G1 state), `.bak-20260922-pre-amendment`, `.bak-20260912`, `.bak-2026-08-31T095850+0200` |

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
| `cup-no_autonomous_commits_pushes_merges_releases_or_deployments.rego` | git commit/push/merge, publish, deploy-script execution. **Amended 2026-09-22 (G1, WP3):** git commit/push/merge are grantable through the commit-allowance channel — the policy checks `cup-git-grants-data.rego` (package `git_grants_data`) for a live, non-zero-count entry on the target repo (`git -C <path>` when named, else the session cwd) and allows when one exists; publish and deploy remain absolute deny with no allowance channel |
| `cup-no_rewriting_or_destroying_development_history.rego` | Force-push, rebase, amend, branch/tag deletion |
| `cup-no_destructive_database_operations.rego` | DROP, unconditioned DELETE, TRUNCATE (9 object types) |
| `cup-no_cross_project_filesystem_access_by_default.rego` | **Amended 2026-09-08, three-tier design, live-tested 13/13:** writes outside the current project are blocked unless the target is inside an always-open shared-library folder or an active, non-zero-count grant exists. **Reads are never blocked by this rule.** Restricted project folders are slip-gated. **Amended again 2026-09-12:** Bash-mediated write-shapes appended to the same file/package — same boundary, same grants, own rule id, first-instance deny. Live-tested 35/35 over three runs. **Amended again 2026-09-22 (WP3):** the stale `skills-collective` always-open entry removed (folder does not exist on disk — verified); `data-mybizz-mgt` documented as restricted-with-slip (G2; compiled treatment unchanged — it was already denied as an outside-cwd path) |
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

## Commit-allowance grants (WP3, 2026-09-22, decision G1)

The `no_autonomous_commits_pushes_merges_releases_or_deployments` rule
enforces git commit/push/merge through a second generated data file,
`cup-git-grants-data.rego` (package `cupcake.global.policies.git_grants_data`),
regenerated in full by `git-grant --repo <folder> --count N --minutes M`
on every call — never appended or patched. Same schema as path grants,
keyed by the repository path in canonical WSL form.

- **Repo resolution:** the compiled policy takes the repo from the
  command's `git -C <path>` argument when present (token-based; quoted
  paths with spaces are an accepted limitation), otherwise from the
  session working directory. A cwd inside the repo matches by prefix.
- **Publish and deploy carry no allowance** — `npm`/`yarn`/`pnpm publish`
  and the named deploy CLI invocations deny absolutely, with or without
  any grant.
- **Plugin mechanics, identical to path grants:** the plugin prunes
  expired commit allowances in `tool.execute.before` and decrements the
  matching repo's count in `tool.execute.after` after a successful git
  commit/push/merge bash call.
- **Fail-closed when absent:** before the first `git-grant` call the file
  does not exist, the package is undefined in the policy, and every git
  commit/push/merge denies exactly as before the amendment.

## Verified real cupcake eval invocation syntax

```
echo '{"hook_event_name": "PreToolUse", "session_id": "(any)", "cwd": "(real cwd)", "tool": "(tool name, lowercase)", "args": {(camelCase fields)}}' | cupcake eval --harness opencode
```

Confirmed field names for `args`: `filePath`, `oldString`, `newString`
(edit/write), `command` (bash), `url` (webfetch). NOT `tool_name`/`tool_input`
— those are Cupcake's internal, post-normalization names, invalid as raw input.

## Known scope limitations (accepted, not defects)

- **The checker boots from the folder it is launched from — resolved 2026-09-22 by the
  set-and-forget amendment.** The plugin spawns the checker with `cwd: event.cwd`
  (fixed 2026-09-12). A folder without a `.cupcake` skeleton previously failed checker
  init, which `failMode` does not cover, blocking every tool call (the 2026-09-22
  incident). The amendment: fail-open is now the environment default, and skeleton-less
  folders fall back to the global-only home `~/.config/cupcake/fallback` (WARN-logged
  per call). Project folders that carry a skeleton use it — including any project-local
  policies they define — so initialization remains an opt-in, never a requirement.
  Every skeleton must contain at least one real local policy module (the input-gated
  `cup-noop-fallback.rego` placeholder): OPA v1.19.1's wasm compiler panics on an
  aggregator-only bundle.

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
