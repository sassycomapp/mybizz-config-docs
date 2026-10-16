---
title: "cupcake-config"
doc-id: "mb-afd0ad78"
updated: "2026-10-16"
---
# Cupcake — Configuration

Canonical current-state configuration record. Agent-facing. States facts, not
history or rules — reasoning in [[cupcake-explainer|Mechanical Policy
Enforcement for AI Coding Agents]]; procedures in
[[[mybizz-config-docs:cupcake/cupcake-reference|Cupcake Reference]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-reference.md).

## Identity

| Field | Value |
|---|---|
| Issuer | EQTYLab — engine, upstream documentation and releases; MyBizz — plugin amendments, custom rules, grant tools |
| Installed version | `0.3.0` (upstream release v0.3.0; corroborated by `cupcake --version`) |
| Standard taken from | `github.com/eqtylab/cupcake` at tag `v0.3.0` (README, LICENSE); releases page |
| Last researched | 2026-10-14 |

## Engine and install

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| License | MIT (v0.3.0 LICENSE) | MIT | github.com/eqtylab/cupcake/blob/v0.3.0/LICENSE | |
| Binary | — | `/home/dev-p/.cupcake/bin/cupcake`, symlinked at `/usr/local/bin/cupcake` | developer terminal verification | |
| Underlying engine | OPA/Rego, compiled to WASM | OPA `1.19.1` at `/usr/local/bin/opa` (real file); `~/.cupcake/bin/opa` symlinks to it | `opa version`; v0.3.0 README | |
| Harness | OpenCode fully supported, alongside Claude Code, Cursor, Factory AI | `opencode` | v0.3.0 README harness table | |
| Plugin file | — | `~/.config/opencode/plugin/cupcake.js` — exactly one copy, never a project-local copy or symlink | plugin-load log check | |
| Global policy folder | — | `~/.config/cupcake/policies/opencode/` | live inventory | |
| Fallback home | — | `~/.config/cupcake/fallback/.cupcake/` — global-only skeleton: `policies/opencode/cup-noop-fallback.rego` (input-gated, never fires), `system/evaluate.rego`, `helpers/commands.rego`, `rulebook.yml`, `opencode.json` | live inventory | |
| Evaluation failure default | `failMode` configurable per project; upstream default `closed` | `closed`: the plugin default; `~/.cupcake/opencode.json` and the fallback home's `opencode.json` also set `closed`; no project folder carries a skeleton that could override it | plugin source; v0.3.0 README security model; live fail-closed test 2026-10-16 | |
| Skeleton initialization | optional | none in any project folder: every OpenCode project evaluates through the fallback home. The one skeleton is `~/.cupcake` (the binaries' folder, and the session folder of `/home/dev-p`), holding the fallback home's four evaluator files and `opencode.json` = `{ "failMode": "closed" }` | live evaluation 2026-10-16: all 29 OpenCode project folders deny a non-allowlisted fetch; live probe in `mb-3-cs-app1` denied | |
| Spawn cwd | — | the checker boots from the session's `.cupcake` skeleton dir when one exists, else from the fallback home; rules evaluate against the session cwd carried in the event | plugin source (spawn call) | |

## Rule estate

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Rule source location | — | `C:\dev\project-library-global\rules-cupcake-global\` — 20 `.md` source documents | live folder listing | |
| Deployment target | `cupcake.policies.*` for project-local | all rules global — `cupcake.global.policies.*` package namespace | v0.3.0 docs structure; live files | |
| Source↔deployed correspondence | — | 21 sources ↔ 20 deployed rule files, each with its source; the bash-governance source compiles into the cross-project rule file | live listings, both sides | |
| cup-block-task-tool.rego | — | blocks the `task` tool and known spawn-tool equivalents (checked against the denylist) | deployed file; source doc | |
| cup-block-anvil-yaml-writes.rego | — | any write to `anvil.yaml`, any Anvil project | deployed file; source doc | |
| cup-no_test_tampering.rego | — | deleting, skipping or gutting a test file | deployed file; source doc | |
| cup-no_verification_tampering.rego | — | writes to CI/CD, test-runner, coverage-threshold config | deployed file; source doc | |
| cup-no_disabling_security_tooling.rego | — | writes to security-tooling config (audit, SAST, secret-scan, pre-commit) | deployed file; source doc | |
| cup-no_suppression_directives_without_approval.rego | — | adding a lint/type-check suppression directive | deployed file; source doc | |
| cup-no_dependency_or_lockfile_changes_without_explicit_approval.rego | — | writes to known lockfiles | deployed file; source doc | |
| cup-no_unverified_dependencies.rego | — | installing a new package via any of 10 package managers | deployed file; source doc | |
| cup-no_autonomous_commits_pushes_merges_releases_or_deployments.rego | — | git commit/push/merge grantable through commit allowances; publish and deploy deny absolutely | deployed file; source doc | |
| cup-no_rewriting_or_destroying_development_history.rego | — | force-push, rebase, amend, branch/tag deletion | deployed file; source doc | |
| cup-no_destructive_database_operations.rego | — | DROP (9 object types), unconditioned DELETE, TRUNCATE | deployed file; source doc | |
| cup-no_cross_project_filesystem_access_by_default.rego | — | writes outside the current project blocked unless `/tmp/`-exempt or granted; skills-dir writes require a grant from every session; bash-mediated write shapes feed the same boundary; reads never blocked | deployed file (read this run) | L3 |
| cup-no_access_to_secrets_unless_explicitly_required.rego | — | reading known secret-file patterns, via Read/Grep or bash | deployed file; source doc | |
| cup-outbound_network_access_is_allowlist_only.rego | — | fetch/curl/wget to a domain outside the allowlist, minus loopback and developer-issued network grants | deployed file (read this run) | |
| cup-no_autonomous_installation_or_connection_of_tools.rego | — | registering a new MCP server, plugin, or skill | deployed file; source doc | |
| cup-no_unapproved_executable_or_build_path_changes.rego | — | writes to CI workflows, Dockerfile, deploy config, `package.json` | deployed file; source doc | |
| cup-protected_ai_governance_files_may_not_be_modified.rego | — | any write to `AGENTS.md` or `CLAUDE.md` | deployed file; source doc | |
| cup-unexpected_instruction_shaped_files_must_be_treated_as_suspicious.rego | — | creating a new `SKILL.md` outside known skill locations | deployed file; source doc | |
| cup-the_ai_may_never_weaken_the_controls_governing_itself.rego | — | writes to `opencode.json` permissions and `spawn-tools-denylist.json` | deployed file; source doc | |
| cup-protect-cupcake-control-plane.rego | — | absolute, ungrantable block on the control plane: the live config folder, the plugin file, the rule-authoring source folder, any project `.cupcake/opencode.json`; denies invoking the grant tools by name in bash | deployed file | |
| builtin — system_protection.rego | shipped builtin | blocks access to critical system paths; bash indicators anchored to real path starts, `/dev/null` stream family exempted | deployed file | |
| builtin — sensitive_data_protection.rego | shipped builtin | blocks credential/secret-shaped files; SSH-key matching by exact basename | deployed file | |
| builtin — cupcake_exec_protection.rego | shipped builtin | blocks direct execution of the `cupcake` binary, including relative and wrapper forms; cannot see inside a script file's contents | deployed file | |
| Aggregator | — | `system/evaluate.rego` — not a rule | live inventory | |

## Governance configuration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Task tool at harness level | — | `"task": "deny"` in `~/.config/opencode/opencode.jsonc` | live config read | |
| Spawn-tool denylist | — | `["task", "delegate", "call_omo_agent", "agent_session_create"]` at `~/.config/opencode/spawn-tools-denylist.json` | live file read | |
| Third task-denial layer | — | standing skill-review habit in the global `AGENTS.md` — new tools checked for spawn capability before trust | `AGENTS.md` | |

## Grants

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Grant tools | — | `mg-grant`, `mg-revoke`, `git-grant`, `net-grant`, `net-revoke` at `~/.config/cupcake/bin/`; developer-terminal only; the agent requests and never executes them | live folder listing | L1 |
| Path grants | — | `mg-grant --path <folder> --count N` → `cup-grants-data.rego` (package `grants_data`); 30-minute expiry hardcoded | grant-paths procedure; live file | |
| Commit allowances | — | `git-grant --repo <folder> --count N --minutes M` (default 30) → `cup-git-grants-data.rego` (package `git_grants_data`); publish and deploy outside the channel; absent file means commits deny | live file | |
| Network grants | — | `net-grant --domain <domain> --count N` → `cup-network-grants-data.rego` (package `network_grants_data`); 30-minute expiry hardcoded; domains lowercase, exact, no wildcards | live file | |
| Grants schema | — | `grants := { "<key>": {"count": N, "expires_at_ns": <epoch-ns>} }` — path grants keyed by canonical WSL path; generated in full by the tools on every call, never hand-edited; the plugin prunes expired entries and decrements on allowed actions, under a shared mkdir lock | live files | L2 |
| Decrement scope | — | file-tool writes decrement per allowed call; git commit/push/merge decrement per allowed action; allowed fetches decrement per fetch; bash-mediated writes inside a granted path run without decrement until expiry; one allowed write decrements only its own path's entry; a write denied by another rule consumes no unit | plugin source; developer-accepted design; live test 2026-10-15 | |
| Outbound allowlist | — | exactly 11 domains: `github.com`, `api.github.com`, `codeload.github.com`, `raw.githubusercontent.com`, `pypi.org`, `files.pythonhosted.org`, `npmjs.com`, `registry.npmjs.org`, `registry.yarnpkg.com`, `cupcake.eqtylab.io`, `anvil.works`; loopback always allowed | rule file (read this run) | |
| Backup files | — | backup files present in the plugin, policy, builtins and grant-tools folders; never loaded. Plugin restore point: `cupcake.js.bak-20261016-known-good` | live inventories | |

## Operational status

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Enforcement state | — | Active and enforcing everywhere, with no per-folder preparation — standing policy, verified at the last research run (outbound-deny probe; plugin loads from the global path only) | exam evidence | |

## Open items

1. Skills-dir ancestor case: the skills-dir protection resolves scope against the session cwd, so a session started in an ancestor of the protected tree may treat writes into it as in-project. The carried two-step check runs developer-side from a session in `/home/dev-p`: first a cwd-independent liveness probe (an outbound-network deny on a non-allowlisted fetch), then an ungranted skills-dir write probe; only an allow under confirmed enforcement indicts the rule. Both probes are written as the reference's "Skills-dir ancestor case" check.
2. Protected-file rules (`AGENTS.md`, `CLAUDE.md`, `opencode.json`, `package.json`) block by default, including a developer-approved same-turn edit — accepted friction; revisit decision pending.
3. The deeper documentation under `docs/` at tag `v0.3.0` was not fetched this run; the standard is taken from the README, LICENSE and releases page actually fetched.