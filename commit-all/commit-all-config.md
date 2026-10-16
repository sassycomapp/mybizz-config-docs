---
title: "commit-all-config"
doc-id: "mb-67ad2aee"
updated: "2026-10-16"
---
# commit-all — Config

Settings of the `commit-all` script, governed by [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md).

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | `6dd62c8` — latest commit touching `commit-all.sh` (2026-10-16) |
| Standard taken from | `C:\mybizz\scripts\commit-all.sh` at commit `6dd62c8` (repository `mybizz-scripts`) |
| Last researched | 2026-10-16 |

## Component

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Kind | bash script in the `mybizz-scripts` repository | same | `commit-all.sh` line 1 | |
| Path | `/mnt/c/mybizz/scripts/commit-all.sh` | verified live 2026-10-16 | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Run by | the developer, in a WSL terminal | same | [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md) | |

## Invocation

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Full run | `bash /mnt/c/mybizz/scripts/commit-all.sh "message"` | same | `commit-all.sh` lines 3, 37–39 | |
| Commit message | required; prompted when missing; empty refused with `STOP: a commit message is needed.` and exit 1 | same | `commit-all.sh` lines 37–39 | |
| `--status` flag | prints per-repository changes or `(nothing to commit)`; changes nothing | verified live 2026-10-16 | `commit-all.sh` lines 29–35 | |

## Phase order

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Order | 1 commit → 2 GBrain → 3 push → summary; exit 0 only when no BLOCKED and no FAILED | same | `commit-all.sh` lines 44–84 | |
| Phase 1 — commit | `git add -A` then commit per repository that has changes; WARNING when the mb-doc-check hook is absent; a hook stop marks the repository BLOCKED, others continue | mb-doc-check hook verified present in all 18 repositories, 2026-10-16 | `commit-all.sh` lines 47–58 | |
| Phase 2 — GBrain | runs `sync-gbrain.sh`; counts its ERROR lines into FAILED; appends its output to the log; `SKIP_SYNC` skips the phase | same | `commit-all.sh` lines 60–66 | |
| Phase 3 — push | pushes every repository; reports `already up to date` when nothing new; marks FAILED and prints the remote's message on failure | same | `commit-all.sh` lines 68–74 | |
| Summary | one table of commit and push result per repository; prints `All done.` when clean, else the BLOCKED/FAILED count; prints the log path; exit 1 on any BLOCKED or FAILED | same | `commit-all.sh` lines 76–84 | |

## Repository list

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| List | the 17 documentation repositories and `mybizz-scripts` named in [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md), section "Commit hook and `commit-all.sh`" | identical, verified 2026-10-16 | `commit-all.sh` lines 7–26 | |
| Off the list | application code repositories, the Anvil reference clone, `project-template`, `gbrain-repo`, and the memory governor's code (committed by hand) | same | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |

## Logging

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Log file | `~/backups/commit-all-last.txt`, one log replaced on every run; the GBrain phase appends its output | present, last written 2026-10-16 15:50 | `commit-all.sh` lines 41–42 | |
| Log directory | `~/backups`, created when missing | same | `commit-all.sh` line 41 | |

## Environment overrides

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| `SYNC` | path of the GBrain sync script; default `/mnt/c/mybizz/scripts/sync-gbrain.sh` | default in use | `commit-all.sh` line 5 | |
| `REPOS_OVERRIDE` | space-separated repository list replacing the built-in array | unset | `commit-all.sh` line 6 | |
| `SKIP_SYNC` | any value skips phase 2 | unset | `commit-all.sh` line 61 | |
| `LOGDIR` | log directory; default `~/backups` | default in use | `commit-all.sh` line 41 | |

## Open items

None.
