---
title: "project-docs-reference"
doc-id: "mb-6950e749"
updated: "2026-10-02"
---
# mb-project-docs — Reference

Usage and execution for the `mb-project-docs` skill. `skill.md` in this folder is the authoritative definition; this document is the operational form. Why it works this way: [[[mybizz-config-docs:mb-project-docs/project-docs-explainer]]](C:/mybizz/mybizz-config-docs/mb-project-docs/project-docs-explainer.md). Current state: [[[mybizz-config-docs:mb-project-docs/project-docs-config]]](C:/mybizz/mybizz-config-docs/mb-project-docs/project-docs-config.md).

## Usage

1. Work in the project's repository (documentation or code). Run for one project at a time.
2. Invoke `/mb-project-docs`. At close-out the close-out procedure invokes it for you (Step 2a).
3. First time in a repository: give the skill your own description of what the project is and why it exists, in the same message. Otherwise it asks once.
4. Read the presentation: per file new, changed or unchanged, the lines that were no longer true, the open items, the README change, and the lines of `AGENTS.md` that will change.
5. Approve, correct or reject. Corrections are applied exactly.
6. Run the terminal line the skill hands you. It copies the reference over `AGENTS.md`.
7. Documentation repository: `commit-all.sh`. Code repository: commit it yourself.

## Procedure

1. Identify the project from the repository folder. Not in the project table: STOP, BLOCKED.
2. Destination. Documentation repository: the root. Code repository: `anvil.yaml` and `theme\` must both exist, then `theme\docs`. Otherwise STOP, BLOCKED, tell the developer to create the Anvil app, create nothing.
3. Read the specification, the existing files, the agent file, `repo-organization.md`, the session and the real state.
4. Validate config, reference and explainer against the real state. Collect what the session changed. Place each item in the one file that owns it.
5. Draft only the changes. Self-check each file against its stray-line test.
6. Present once, then stop.
7. After approval: write config, explainer, README and the reference; hand over the copy line.
8. Report what was written and the copy line.

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

## Completion statuses

| Status | When |
|---|---|
| DONE | Files written, approved, copy line handed over |
| BLOCKED | Not a covered project, specification missing, or no Anvil app in a code repository |
| PERMISSION_REQUIRED | A policy blocked an action; the grant line was handed over |
| CANCELLED | The developer declined at the presentation; nothing was written |

## Do not

- Do not run for more than one project.
- Do not write `AGENTS.md` or `agents.md`.
- Do not create `theme\docs` in a repository that has no `anvil.yaml` or no `theme\`.
- Do not copy repository paths, remotes or GBrain sources into the files; point to `repo-organization`.
- Do not regenerate the explainer.
- Do not put a rule in config or a reason in the reference.
- Do not use Git to change anything.
