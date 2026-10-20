---
title: "project-docs-reference"
doc-id: "mb-6950e749"
updated: "2026-10-20"
---
# mb-project-docs — Reference

Usage and execution for the `mb-project-docs` skill. The skill's source, `mb-project-docs.md` in `C:\mybizz\mb-project-docs\`, is the authoritative definition; this document is the operational form. Why it works this way: [[[mybizz-config-docs:mb-project-docs/project-docs-explainer]]](C:/mybizz/mybizz-config-docs/mb-project-docs/project-docs-explainer.md). Current state: [[[mybizz-config-docs:mb-project-docs/project-docs-config]]](C:/mybizz/mybizz-config-docs/mb-project-docs/project-docs-config.md).

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Skill source (the issuer standard) | [[[mb-project-docs:mb-project-docs]]](C:/mybizz/mb-project-docs/mb-project-docs.md) (`C:\mybizz\mb-project-docs\mb-project-docs.md`) | `66fb55a` | 2026-10-20 |
| Doc suite specification | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | `mb-f4adba8c` | 2026-10-20 |
| Repository organization | [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | `mb-f38fd0aa` | 2026-10-20 |

## Usage

1. Work in the project's repository (documentation or code). Run for one project at a time.
2. Invoke `/mb-project-docs`. At close-out, `/mb-close-out` invokes it for you (Step 3).
3. First time in a repository: give the skill your own description of what the project is and why it exists, in the same message. Otherwise it asks once.
4. Read the presentation: per file new, changed or unchanged, the lines that are no longer true, the open items, the README change, and the lines of `AGENTS.md` that will change.
5. Approve, correct or reject. Corrections are applied exactly.
6. Run the terminal line the skill hands you. It copies the reference over `AGENTS.md`.
7. Documentation repository: `commit-all.sh`. Code repository: commit it yourself.

## Procedure

1. Identify the project from the repository folder. Not in the project table: STOP, BLOCKED.
2. Destination. Documentation repository: the root. Code repository: `theme\assets\docs\appN`. `anvil.yaml` missing: STOP, BLOCKED, tell the developer to create the Anvil app. `theme\assets\docs\appN` missing: STOP, BLOCKED, give the developer the one-time setup: (1) on the hard drive, create a folder named `appN` (the app's number) holding one file, `pilot-doc.txt`; (2) in the Anvil editor, open Assets, create the folder `docs` if it is missing, and upload the `appN` folder into it with Add asset > Upload folder; (3) pull the code repository; (4) delete the folder from the hard drive. Create nothing.
3. Read the specification, the existing files, the agent file, `repo-organization.md`, the session and the real state.
4. Validate config, reference and explainer against the real state. Collect what the session changed. Place each item in the one file that owns it.
5. Draft only the changes. Self-check each file against its stray-line test.
6. Present once, then stop.
7. After approval: write config, explainer, README and the reference; hand over the copy line.
8. Report the files written and the copy line.

## The copy line

```
bash /mnt/c/mybizz/scripts/agents-from-reference.sh "<reference file>" "<AGENTS.md or agents.md>"
```

- The body of the reference replaces the body of the agent file. The agent file's own frontmatter is kept exactly.
- The old agent file is saved in `~/backups`.
- The reference file is deleted after the copy is checked.
- The target must be named `AGENTS.md` or `agents.md`. Use the name that exists; if neither exists, `AGENTS.md`.

## README rules

- Missing: create it with a title, a summary of three to five lines, and a "Required reading" list.
- Present: keep its content, update the summary, add or correct the "Required reading" list.
- The list names the config, `AGENTS.md` and the explainer. Documentation repository: `[[name]]` links. Code repository: relative paths.

## Hard rules

1. Current project only.
2. Verify live where possible; unverified claims become open items; never blend.
3. Each fact lives in one of the three files.
4. Small edits; never overwrite without saying so; the explainer changes only where a decision changed.
5. Never write `AGENTS.md` or `agents.md`.
6. Never touch `.gitignore`; never run a Git command that changes anything.
7. A policy block: stop, report it, hand over the grant line, wait.
8. One approval before anything is written.

## Grant lines

```
mg-grant --path <folder> --count N
net-grant --domain <domain> --count NN
```

Hand the exact line to the developer. Never run it. No grant exists for Git.

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `git -C /mnt/c/mybizz/mb-project-docs log -1 --format='%h %ad' --date=short` | agent |
| Source current with origin | `git -C /mnt/c/mybizz/mb-project-docs ls-remote origin HEAD` must equal the short sha from `git log -1` (exact match, one call) | agent |
| Two copies in sync | body-diff `~/.config/opencode/skills/mb-project-docs/SKILL.md` against [[[mb-project-docs:mb-project-docs]]](C:/mybizz/mb-project-docs/mb-project-docs.md) (file tools) | agent |
| Helper script present | read `C:\mybizz\scripts\agents-from-reference.sh` (file tools) | agent |
| Project table matches repo-organization | compare the source's Step 1 table against [[[mybizz-os-docs:os-reference-docs/repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) § Names | agent |
| Works | the installed `SKILL.md` carries `name` and `description` frontmatter and OpenCode lists the skill as available | agent |

## Completion statuses

| Status | When |
|---|---|
| DONE | Files written, approved, copy line handed over |
| BLOCKED | Not a covered project, specification missing, or no Anvil app in a code repository |
| PERMISSION_REQUIRED | A policy blocks an action; the grant line is handed over |
| CANCELLED | The developer declines at the presentation; nothing is written |

## Do not

- Do not run for more than one project.
- Do not write `AGENTS.md` or `agents.md`.
- Do not create `theme\assets\docs\appN` locally; it exists only after the developer uploads it through Anvil.
- Do not remove `pilot-doc.txt` from `theme\assets\docs\appN`.
- Do not copy repository paths, remotes or GBrain sources into the files; point to `repo-organization`.
- Do not regenerate the explainer.
- Do not put a rule in config or a reason in the reference.
- Do not use Git to change anything.
