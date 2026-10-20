---
title: "commit-all-reference"
doc-id: "mb-52b1ef35"
updated: "2026-10-20"
---
# commit-all — Reference

Execution reference for `commit-all`. Values live in the config. Why it is built this way: [[[mybizz-config-docs:commit-all/commit-all-explainer]]](C:/mybizz/mybizz-config-docs/commit-all/commit-all-explainer.md).

## Invocation

```
bash /mnt/c/mybizz/scripts/commit-all.sh              # full run — developer only
bash /mnt/c/mybizz/scripts/commit-all.sh --status     # read-only preview — agent or developer
```

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| The script (the issuer standard) | `C:\mybizz\scripts\commit-all.sh` | `6dd62c8` | 2026-10-20 |
| Repository register | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) — section "Commit hook and `commit-all.sh`" | — | 2026-10-20 |
| Developer how-to | [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md) | — | 2026-10-20 |
| Governing policy for who runs it | [[[default:rules-cupcake-global/no_autonomous_commits_pushes_merges_releases_or_deployments]]](C:/dev/project-library-global/rules-cupcake-global/no_autonomous_commits_pushes_merges_releases_or_deployments.md) · [[[mybizz-config-docs:cupcake/cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) §Operational status | — | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `git -C /mnt/c/mybizz/scripts log -1 --format='%h %ad %s' --date=short -- commit-all.sh` | agent |
| Repository list | read the `REPOS` array in the script and the register section; both name the same 18 folders | agent |
| Phase 1 — commit hook | `grep -q mb-doc-check <repo>/.git/hooks/pre-commit` for each of the 18; the full run also prints a WARNING per missing hook | agent |
| Log file | `ls -la /home/dev-p/backups/commit-all-last.txt` — present, dated the last run | agent |
| Works (read-only) | `--status` prints 18 sections, each with changes or `(nothing to commit)` | agent |
| Works (full) | the summary ends `All done.`; a BLOCKED or FAILED count means work first, then run the same command again | developer |

## Procedure — reading a run's result

1. Read the summary table: every repository should say `committed` or `nothing to commit`, and `pushed` or `already up to date`.
2. BLOCKED on a repository: the commit hook stopped it and printed the reason. Fix the cause, run the same command again. Handling per message: [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md), section "If a repository says BLOCKED".
3. FAILED on push: GitHub has commits this machine does not. Never force. Paste the summary for help.
4. The full output of the last run is in `~/backups/commit-all-last.txt`.

## Do not

- Do not run the full command as an agent. The developer runs it in the WSL terminal (standing policy; see the authoritative sources).
- Do not use `git commit --no-verify`. It switches the hook off.
- Do not force a push.
- Do not interrupt a run; the GBrain phase can take minutes.
- Do not edit the `REPOS` array without the matching [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) row, nor the register without the array; the full order is in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md), "Adding a new documentation repository".
