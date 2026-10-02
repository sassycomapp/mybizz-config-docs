---
name: mb-project-docs
description: |
  Keeps a project's three canonical files current: config (state), reference
  (which becomes the project's AGENTS.md) and explainer (what the project is
  and why), and the README that points to them. Creates any file that is
  missing; updates any file that exists by validating what it says against the
  real state and adding what the session changed. Works on the current project
  only. Invoked as /mb-project-docs, normally at close-out. Use only when
  explicitly invoked — never auto-trigger.
---

# mb-project-docs

Keeps the three canonical files of the project you are working in current, and the README that points to them. Governing specification for what each file holds: `C:\mybizz\mybizz-config-docs\mb-sysdoc-creator\doc-suite-specification.md`. This skill does not improvise a different structure.

Files, per repository:

- `{slug}-config.md` — state only.
- `{slug}-reference.md` — execution. At close-out its body becomes the repository's `AGENTS.md`, and the reference file is then deleted.
- `{slug}-explainer.md` — what the project is, what it is for, why it is built this way.
- `README.md` — a brief summary and pointers to the three files as required reading.

---

## Section 0 — Hard rules. Do not deviate.

1. **Current project only.** Never read for the purpose of writing, or write, in another project's repository.
2. **Verify before writing.** A fact is checked live (file read, GBrain query, read-only command) wherever it can be. A claim that cannot be verified becomes an open item. Verified and unverified facts are never blended.
3. **One fact, one home.** Config holds state, reference holds execution, explainer holds reasoning. A fact written in two of them is an error.
4. **Small edits.** Never overwrite a file without saying so. Change only the lines that are wrong or new. The explainer changes only where a decision changed, and is never regenerated.
5. **Never write `AGENTS.md` or `agents.md`.** The reference file is the draft of it. The developer's terminal block copies it (Step 7).
6. **Never touch `.gitignore`.** Never run a Git command that changes anything. Read-only `git status`, `git log` and `git diff` are allowed.
7. **A policy block stops the run.** Report the exact block, hand the developer the exact grant line, and wait. The two formats are `mg-grant --path <folder> --count N` and `net-grant --domain <domain> --count NN`. Never run a grant or any permission-altering command yourself. No grant exists for Git.
8. **One approval.** Nothing is written before the developer approves the presentation of Step 6. At close-out, that approval is the close-out gate.

---

## Section 1 — Procedure

### Step 1 — Identify the project and the repository

Run `git rev-parse --show-toplevel` and match the folder name:

| Project | Documentation repository | Code repository |
|---|---|---|
| `makepdlf` | `makepdlf-project-library` (`C:\dev\dev-makepdlf\makepdlf-project-library`) | `makepdlf` (`C:\dev\dev-makepdlf\makepdlf`) |
| `mb-3-cs` | `mb-3-cs-project-library` (`C:\dev\dev-mb-3-cs\mb-3-cs-project-library`) | `mb-3-cs` (`C:\dev\dev-mb-3-cs\mb-3-cs`) |
| `mb4ecom` | `mb4ecom-project-library` (`C:\dev\dev-mb4ecom\mb4ecom-project-library`) | `mb4ecom` (`C:\dev\dev-mb4ecom\mb4ecom`) |
| `mb5pdlf` | `mb5pdlf-project-library` (`C:\dev\dev-mb5pdlf\mb5pdlf-project-library`) | `mb5pdlf` (`C:\dev\dev-mb5pdlf\mb5pdlf`) |
| `pdlf` | `pdlf` (`C:\pdlf`) | none |

The current repository is the one whose folder you are in. The `{slug}` is the project name from the first column. If the folder is not in this table: STOP, status BLOCKED, say that the folder is not a covered project.

### Step 2 — Destination

- **Documentation repository:** the repository root.
- **Code repository:** check that `anvil.yaml` and the folder `theme` both exist at the repository root.
  - Both exist: the destination is `theme\docs`. Create the folder if it is missing. Do not ask.
  - Either is missing: the Anvil code repository does not exist. STOP. Tell the developer that the Anvil app must be created in Anvil first, then end the run with status BLOCKED. Create nothing.

### Step 3 — Read

- The specification named above. If it is missing: STOP, BLOCKED.
- Whichever of the three files and the README exist in the destination, in full.
- The repository's `AGENTS.md` or `agents.md`, if it exists.
- `C:\mybizz\mybizz-os-docs\os-reference-docs\repo-organization.md`. It holds paths, GitHub repositories and GBrain sources. The three files point to it and never repeat it.
- The work of the current session, and the real state of the repository (files, `opencode.json`, agent role files, commands folder, installed tools).

### Step 4 — Validate and collect

- **Config:** check every stated fact against the real state. List each fact that is no longer true. Add each new state fact the session produced.
- **Reference:** the starting content is the existing `AGENTS.md` (or the existing reference file). Check that its commands and rules still hold. Add each new rule, command or procedure the session produced.
- **Explainer:** compare its decisions with the decisions of the session. Change a statement only where a decision changed, and add reasoning for a new decision.
- **A file is missing:** create it. The reference starts from `AGENTS.md`. For a missing config or explainer you need the developer's own description of what the project is and why it exists. If it was not given with the invocation, ask for it once, and nothing else.
- Place every item in the one file that owns it.

### Step 5 — Draft

Draft only the changes. Each file must pass its stray-line test from the specification before it is presented.

- **Config:** identity (project, slug, repository type, status), the repositories (a pointer to `repo-organization`, with one sentence saying what it holds), agent setup (`opencode.json`, role files, commands folder, the `AGENTS.md` file), installed tools, key documents, open items.
- **Reference:** imperative rules, exact commands, procedures as ordered steps, a closing "Do not" list.
- **Explainer:** what the project is; what it can do; what it is for, good for and not for; why it is built this way; open questions framed as why they matter.
- **README:**
  - Missing: create it with a title, a summary of three to five lines (from the explainer's first section) and a "Required reading" list.
  - Present: keep its content, bring the summary up to date, and add or correct the "Required reading" list.
  - The list names the config, `AGENTS.md` and the explainer. In a documentation repository write each as `[[name]]`. In a code repository write relative paths (`theme/docs/{slug}-config.md`), because no commit hook converts links there.

### Step 6 — Present, then stop

Present once, in one message:

1. For each of config, explainer and README: new, changed or unchanged, with the exact lines changed.
2. The statements that were no longer true, and what replaced them.
3. The open items found.
4. The lines of `AGENTS.md` that will change, shown as a diff between the current file and the reference draft.

Wait for the approval. The developer may correct anything; apply corrections exactly. On rejection of a file, redraft only that file.

### Step 7 — After the approval

1. Write config, explainer and the README to the destination. Write the reference file to the destination.
2. Hand the developer this line for the terminal. It copies the reference over the repository's agent file, keeps that file's own frontmatter, saves the old file in `~/backups`, and then deletes the reference file:

```
bash /mnt/c/mybizz/scripts/agents-from-reference.sh "<full path of the reference file>" "<full path of AGENTS.md or agents.md>"
```

   Use the file name that exists. If neither exists, use `AGENTS.md`.
3. In a documentation repository the files are committed with the other documents (`commit-all.sh`). In a code repository the developer commits them.

### Step 8 — Report

Say what was written, what was left unchanged, and the exact terminal line of Step 7.

---

## Section 2 — Completion statuses

- **DONE** — files written, approved, and the copy line handed over.
- **BLOCKED** — the folder is not a covered project, the specification is missing, or the Anvil code repository does not exist (Step 2). State what is needed.
- **PERMISSION_REQUIRED** — a policy blocked an action. State the exact block and the grant line.
- **CANCELLED** — the developer declined at the presentation. Nothing was written.
