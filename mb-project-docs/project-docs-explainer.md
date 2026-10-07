---
title: "project-docs-explainer"
doc-id: "mb-9730dd51"
updated: "2026-10-07"
---
# mb-project-docs — Explainer

*Companion note: current state in [[[mybizz-config-docs:mb-project-docs/project-docs-config]]](C:/mybizz/mybizz-config-docs/mb-project-docs/project-docs-config.md); usage and execution in [[[mybizz-config-docs:mb-project-docs/project-docs-reference]]](C:/mybizz/mybizz-config-docs/mb-project-docs/project-docs-reference.md).*

## 1. What this actually is

Every project needs a place where anyone — a developer, an agent, someone new — can learn what the project is, what state it is in, and how to work in it. `mb-project-docs` keeps that place current. It maintains three files in each repository: a config file that records the state, an `AGENTS.md` that tells agents how to work, and an explainer that says what the project is and why it is built the way it is. A short README points to all three as required reading.

The skill works on one project at a time, the one you are in. It does not hold anything about any particular project. It reads the project's real state and what the session changed, compares that with what the files say, and proposes the small changes that bring them up to date.

## 2. Feature summary

- Creates any of the three files that does not exist, and updates the ones that do.
- Checks what the files claim against the real state and lists what is no longer true.
- Adds what the session produced, each item to the one file that owns it.
- Keeps the README's summary and its pointers to the three files current.
- Prepares the project's `AGENTS.md` as a draft that you apply with one terminal line.
- Treats documentation repositories and code repositories differently, as they are different kinds of project.
- Works the same for every project, whatever the project builds.

## 3. Suitability

**Best for:** the end of a working session in one of the five projects, when the state, the rules or a decision may have changed and the three files should say so.

**Good for:** the first time a project is documented in this form, when you describe the project and the skill creates the files from that and from the real state.

**Not good for:** documenting a tool, a skill or a service (right tool: `mb-sysdoc-creator`); keeping documents consistent with each other or their links correct (the commit hook does that); repositories that are not one of the five projects; running across several projects at once.

## 4. Design reasoning

**Why three files and not one.** A project's state, its working rules and its reasons change at different speeds and answer different questions. State goes stale when a setting changes, rules go stale when practice changes, reasons go stale only when a decision changes. Keeping them apart means an update touches only the file that is wrong.

**Why the reference is the `AGENTS.md`.** An agent's rules and a project's execution reference are the same content. Two files would hold the same facts twice and drift apart. So there is one file, `AGENTS.md`, and the reference exists only as the draft the skill prepares.

**Why the agent does not write `AGENTS.md`.** The rules in that file govern the agent. A rule that blocks the agent from editing its own rules would mean little if a skill could route around it. So the skill drafts the change, you see the lines that will change, and your terminal line applies it. The reference file is deleted afterwards so that no duplicate remains.

**Why small edits, and why the explainer is never regenerated.** State can be rediscovered from the files and the machine. Reasons and decisions cannot. A rewrite from scratch would lose the reasoning that explains why the project is as it is. So the skill edits the lines that are wrong and adds what is new.

**Why verification comes before writing.** Files that describe a project age quickly, and an unchecked claim becomes a false fact that everyone then trusts. A fact the skill cannot check becomes an open item, so the gap is visible instead of hidden.

**Why code repositories use `theme\docs` and need an Anvil app.** A code repository is an Anvil app. Its files are uploaded to Anvil, and the folder `theme\assets` is the one Anvil serves on the app's website. The folder `theme\docs` is a separate folder that you chose for these files. If the Anvil app does not exist yet, there is nowhere right to put the files, so the skill ends and tells you to create the app first.

**Why it runs at close-out.** That is the moment when you know what changed in the session, and the one moment you already approve things. The skill's changes join the single approval of the close-out and need no gate of their own.

**Where it sits.** It is a consumer of `repo-organization` for the facts about repositories and of the three-file specification for what each file holds. Its output in documentation repositories is checked and linked by the commit hook; in code repositories it is not.

