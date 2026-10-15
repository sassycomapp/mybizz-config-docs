---
title: "config-manager-reference"
doc-id: "mb-8ddcefac"
updated: "2026-10-15"
---
# mb-config-manager — Reference

Agent-facing execution for running the configuration-management agent.

## Invocation

| Form | Meaning |
|---|---|
| `/mb-config-manager (system-name)` | Examine that one system |
| `/mb-config-manager` | List every Active system whose Last checked is empty, or earlier than its Last updated; ask the developer which to examine |

Select the mb-config-manager agent with Tab before running the command; the
command alone runs in whichever agent is selected.

## Running one exam

The procedure is `config-manager-agent.md`, sections **One run** and **Finding
kinds**. Never restate it here.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Orchestrator agent (the standard) | [[[mybizz-config-docs:mb-config-manager/config-manager-agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md) | `17e9046` | 2026-10-15 |
| Doc suite specification | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | current | 2026-10-15 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `git -C /mnt/c/mybizz/mybizz-config-docs log -1 --format="%h %ad" --date=short -- mb-config-manager/config-manager-agent.md` | agent |
| Works | Run `/mb-config-manager (system-name)` on a system with a suite; findings appear in chat in the six-kind order | developer |
| Agent installed | Read `/home/dev-p/.config/opencode/agents/mb-config-manager.md`; body below frontmatter matches the source | agent |
| Command wired | `/home/dev-p/.config/opencode/command/mb-config-manager.md` exists and names the agent | agent |

## Do not

- Do not install, upgrade or update anything.
- Do not research issuers or write document suites.
- Do not write a Cupcake rule.
- Do not commit; the developer runs commit-all.
- Do not grant access to yourself; never work around a block.
- Do not hold state about a system between runs.
