---
title: "anvil-cli-reference"
doc-id: "mb-c30890dd"
updated: "2026-10-22"
---

# anvil-cli — Reference

State values live in [[[mybizz-config-docs:anvil-cli/anvil-cli-config]]](C:/mybizz/mybizz-config-docs/anvil-cli/anvil-cli-config.md). Reasons live in [[[mybizz-config-docs:anvil-cli/anvil-cli-explainer]]](C:/mybizz/mybizz-config-docs/anvil-cli/anvil-cli-explainer.md).
Differences from the issuer standard live in [[[mybizz-config-docs:anvil-cli/anvil-cli-learnings]]](C:/mybizz/mybizz-config-docs/anvil-cli/anvil-cli-learnings.md).

## Invocation

- `anvil` resolves on login-shell PATH only. From an agent's non-login shell, run
  `bash -lc 'anvil …'` or use the full binary path recorded in [[[mybizz-config-docs:anvil-cli/anvil-cli-config]]](C:/mybizz/mybizz-config-docs/anvil-cli/anvil-cli-config.md).

## Commands

Syntax below is from the installed 0.7.7 `anvil --help` unless a source is named.

- `anvil --json validate <path>` — validates by file or directory: `anvil.yaml`,
  `client_code/**/*.yaml`, `client_code/**/*.html`, `client_code/**/*.py`,
  `server_code/**/*.py`. Accepts a folder: verified live against an app folder,
  where it returned a per-file breakdown with a `count`.
  - Single-file success shape: `{"type":"result","success":true,"data":{"file":"anvil.yaml","type":"anvil.yaml","valid":true}}`
  - Folder success shape: the same envelope with `"file":"."`, `"valid":true`,
    `"count":N`, and a `files` array of per-file results.
  - Invalid input prints the fields needing attention and exits with an error.
- `anvil version` — version information (also the PDLF health check).
- `anvil config get <key>` | `anvil config list` | `anvil config set <key> <value>`
  | `anvil config delete <key>` (alias `unset`) | `anvil config reset`.
- `anvil login [anvil-server-url]` (option `-u, --url`), `anvil logout [anvil-server-url]`
  (options `-u, --url`, `-U, --user`).
- `anvil checkout|co [input] [directory]` — options `-O/--open`, `-b/--branch`,
  `--depth <N>`, `--single-branch`, `--origin <NAME>`, `--quiet`, `--verbose`,
  `-u/--url`, `-U/--user`, `-f/--force`, `-Q/--query`.
- `anvil watch|sync [path]` — options `-A/--appid`, `-f/--first`, `-s/--staged-only`,
  `--no-dependency-watch`, `-a/--auto`, `-O/--open`, `-u/--url`, `-U/--user`.
  Not used in PDLF; see Do not.
- `anvil deps fetch [--commit <commit>] [--exclude-docs]` | `anvil deps status`
  | `anvil deps clear`.
- `anvil tables fetch` | `anvil tables status` | `anvil tables clear`.
- `anvil convert-template <file>` — options `-o/--output`, `-f/--force`, `--keep-source`.
- `anvil git-auth doctor [--repo <PATH>]` — diagnoses why plain Git commands cannot
  authenticate to Anvil.
- `anvil configure` — guided setup for configuration and login.
- `anvil update` — see Do not.
- Hidden: `anvil git-credential <operation>` — Git credential-helper integration
  (present in installed source; not shown in help).

## Rules

1. Validate every `anvil.yaml` change with `anvil --json validate anvil.yaml`, and a
   whole app with `anvil --json validate .`; treat the machine-readable errors as
   authoritative.
2. Never run `anvil config set` or `anvil config delete` without the developer's
   instruction.
3. Read configuration only through `anvil config get` for individual non-secret keys;
   never request `authTokens` by any means.
4. Treat `anvil update` and `anvil watch` as out of bounds in every agent pipeline
   (see Do not).

## Authoritative sources

| Source | Link | Issuer version |
|---|---|---|
| Using Anvil from a Local IDE | https://anvil.works/docs/using-another-ide | current, unversioned; verified 2026-10-22 |
| Anvil CLI commands | https://anvil.works/docs/using-another-ide/commands | current, unversioned; verified 2026-10-22 |
| npm package page | https://www.npmjs.com/package/@anvil-works/anvil-cli | 0.7.7 is `latest` |
| Anvil agent references (skills and AGENTS.md template) | `C:\mybizz\anvil-agent-references\` | the clone's pin; see [[[mybizz-config-docs:anvil-cli/anvil-cli-explainer]]](C:/mybizz/mybizz-config-docs/anvil-cli/anvil-cli-explainer.md) |
| Installed CLI help and source | `anvil --help`, `anvil <command> --help` | 0.7.7 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `anvil version` | agent |
| `anvilUrl`, `verbose`, `preferredEditor`, `devMode` | `anvil config get <key>` for each key in turn | agent |
| Login account | `anvil login --verbose`; reports the logged-in account (reaches anvil.works) | developer |
| Works — file validate | inside an app folder: `bash -lc 'anvil --json validate anvil.yaml'`; success returns NDJSON with `valid:true` | agent |
| Works — app validate | inside an app folder: `bash -lc 'anvil --json validate .'`; success returns NDJSON with `valid:true` and a `count` | agent |

## Do not

- Do not run `anvil watch` in any PDLF pipeline.
- Do not run `anvil update` — the version is pinned; only the developer updates it.
- Do not run `anvil db apply-schema` — it does not exist in 0.7.7, and where it exists
  it can delete tables, columns or data.
- Do not run `anvil config reset` — it clears saved logins.
- Do not read `authTokens` through any command or file dump.
