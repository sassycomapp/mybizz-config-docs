---
title: "config-manager-config"
doc-id: "mb-48323f1a"
updated: "2026-10-15"
---
# mb-config-manager — Configuration

State of the configuration-management agent. Standard:
[[[mybizz-config-docs:mb-config-manager/config-manager-agent|Orchestrator Agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md).

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | `17e9046` (last commit of `config-manager-agent.md`) |
| Standard taken from | `config-manager-agent.md`, commit `17e9046`, 2026-10-14 |
| Last researched | 2026-10-15 |

## Settings — behaviour

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Trigger | On demand only | On demand only — developer-initiated | agent §Invocation | |
| Invocation, one system | `/mb-config-manager (system-name)` | as standard | agent §Invocation | |
| Invocation, no name | List Active systems whose Last checked is empty or earlier than Last updated; ask which | as standard | agent §Invocation | |
| Finding kinds | DOWN, UNHEALTHY, BEHIND, DRIFT, DEVIATION, GAP — in that report order | as standard | agent §Finding kinds | |
| Documents out of shape | One DEVIATION; its correction is a full mb-sysdoc-creator Refresh, and every other correction to the four documents folds into it | as standard | agent §1 Locate | |
| Register scope | Every system, `mb-config-manager` itself included | as standard | agent §The register | |
| Register columns | System · Kind · Docs folder · Installed version · Last updated · Last checked · State | as standard | agent §The register | |
| Kind values | skill, agent, script, plugin, application, service | as standard | agent §The register | |
| Register states | Active, Deferred | as standard | agent §The register | |
| Run record | Findings in chat; the register row is the only record | as standard | agent hard rules 3, 9 | |
| Learning writes | Config rows, learnings entries and the register row, only with developer approval | as standard | agent hard rule 3 | |
| Change discipline | One change at a time; replace-value recorded; stop on failed check with the way back | as standard | agent hard rule 5 | |
| On a block | Stop; give the exact grant line; never self-grant, never work around | as standard | agent hard rule 6 | |
| Issuer research | Never — `/mb-sysdoc-creator (system-name)` does it | as standard | agent hard rule 7 | |
| Cupcake rules | Never written — `/mb-compile-rules` does it | as standard | agent hard rule 8 | |
| Install/upgrade | Never — a newer version is a notice and a request | as standard | agent hard rule 4 | |
| Commit | Never — the developer runs commit-all | as standard | agent hard rule 10 | |

## Settings — files

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Register | `/mnt/c/mybizz/mybizz-config-docs/mb-config-manager/config-manager-register.md` | as standard | agent §Files | |
| Own learnings | `.../mb-config-manager/config-manager-learnings.md` | as standard | agent §Files | |
| Specification | `/mnt/c/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md` | as standard | agent §Files | |
| Grant forms | `/mnt/c/mybizz/mybizz-os-docs/operating-procedures/grant-paths.md` | as standard | agent §Files | |
| System folders | `/mnt/c/mybizz/mybizz-config-docs/{system}/` | as standard | agent §Files | |
| Working files | `config-manager-agent.md`, `config-manager-register.md` | as standard | doc-suite-specification §The folder | |

## Settings — installation

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Agent source | `config-manager-agent.md` in this folder | as standard | agent file itself | |
| Agent installed | Developer-set agent path | `/home/dev-p/.config/opencode/agents/mb-config-manager.md` | install verified 2026-10-15 | |
| Command wrapper | Developer-set command path | `/home/dev-p/.config/opencode/command/mb-config-manager.md` | install verified 2026-10-15 | |

## Open items

None.
