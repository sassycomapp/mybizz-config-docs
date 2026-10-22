---
title: "anvil-cli-config"
doc-id: "mb-a95719e6"
updated: "2026-10-22"
---

# anvil-cli — Config

Anvil's command-line tool for working on Anvil apps from a local IDE.

## Identity

| Field | Value |
|---|---|
| Issuer | Anvil (npm owner `anvil-works`) |
| Installed version | 0.7.7 |
| Standard taken from | Anvil CLI docs, current unversioned pages, verified 2026-10-22; npm `@anvil-works/anvil-cli` dist-tag `latest` 0.7.7; the installed CLI's own `--help` output |
| Last researched | 2026-10-22 |

## Installation

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Install method | `curl -fsSL https://anvil.works/install-cli.sh \| sh`, or `npm install -g @anvil-works/anvil-cli@latest` | Anvil install script; self-contained npm prefix under `~/.anvil-cli/` | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md) | |
| Binary | — (installer-managed) | `~/.anvil-cli/npm-global/bin/anvil` | live verification | |
| PATH wiring | — | `$HOME/.anvil-cli/npm-global/bin` and `$HOME/.anvil-cli/node-v20/bin`, appended to `~/.bashrc` (line 147) and `~/.profile` (line 29) | live verification | L4 |
| Platform | macOS, Linux, Windows | Linux (WSL) x64; Node.js v24.15.0 as reported by `anvil version` | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md); live verification | |

## Login

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Server (`anvilUrl`) | `https://anvil.works` (default) | `https://anvil.works` | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md) | |
| Account | one OAuth device-login token per logged-in account, stored in the config file | `sassycomapp@gmail.com` (login verified live 2026-10-22) | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md) | |
| Config file location (Linux) | `~/.config/anvil-cli/config.json` | same | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md) | |

## CLI settings

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `preferredEditor` | user choice at `anvil configure`; the quickstart recommends None | `""` (none) | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md) | |
| `verbose` | user choice; the quickstart recommends False | `false` | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md) | |
| `devMode` | — (listed as a stored setting; no standard value documented) | `false` | [[[default:anvil-docs/using-another-ide/_index]]](C:/dev/project-library-global/anvil-docs/using-another-ide/_index.md) | |

## Version pin

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Stable release | `latest` = 0.7.7, released 2026-10-02 | 0.7.7 | npm dist-tags, verified 2026-10-22 | |
| Pre-releases | `dev` 0.8.0-dev.1 (2026-10-19); `canary` 0.8.0-canary.25 (2026-10-20) | not installed | npm dist-tags, verified 2026-10-22 | L1 |

## Installed surface versus issuer docs

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `create` command | documented, with `-d/--directory`, `--no-checkout`, `--tag` (up to 20 tags), `-u/--url`, `-U/--user`, `--git-url`, `-O/--open` | absent from 0.7.7 | [[[default:anvil-docs/using-another-ide/commands]]](C:/dev/project-library-global/anvil-docs/using-another-ide/commands.md); live `anvil --help` | L5 |
| `checkout --git-url` | documented | absent from 0.7.7 | [[[default:anvil-docs/using-another-ide/commands]]](C:/dev/project-library-global/anvil-docs/using-another-ide/commands.md); live `anvil checkout --help` | L5 |
| `config delete\|unset` | not documented | present in 0.7.7 | [[[default:anvil-docs/using-another-ide/commands]]](C:/dev/project-library-global/anvil-docs/using-another-ide/commands.md); live `anvil config --help` | L5 |
| `deps`, `tables`, `convert-template`, `git-auth` | not documented on the docs pages | present in 0.7.7 (`git-credential` also present, hidden) | [[[default:anvil-docs/using-another-ide/commands]]](C:/dev/project-library-global/anvil-docs/using-another-ide/commands.md); live `anvil --help` and installed source | L5 |
| `validate` file surface | docs pages: `anvil.yaml` and `.yaml` files under `client_code/`; Anvil's own AGENTS.md template: also HTML form templates and Python files under `client_code/` and `server_code/` | all five file groups | [[[default:anvil-docs/using-another-ide/commands]]](C:/dev/project-library-global/anvil-docs/using-another-ide/commands.md); `C:\mybizz\anvil-agent-references\AGENTS.md`; live `anvil validate --help` | L5 |
| `db apply-schema` | none in 0.7.7; registered only in the 0.8.0 pre-releases when `ANVIL_AGENT_HOST=1` (Anvil's hosted agent) | absent; `ANVIL_AGENT_HOST` unset on this machine | npm dist-tags, verified 2026-10-22; live `printenv` | L3 |

## Open items

None.
