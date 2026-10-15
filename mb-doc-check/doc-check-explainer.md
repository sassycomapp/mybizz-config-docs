---
title: "doc-check-explainer"
doc-id: "mb-632b78c3"
updated: "2026-10-15"
---
# mb-doc-check — Explainer

*Companion note: current state in [[[mybizz-config-docs:mb-doc-check/doc-check-config]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-config.md); commands, messages and procedures in [[[mybizz-config-docs:mb-doc-check/doc-check-reference]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-reference.md). The link system from the author's point of view is [[[mybizz-os-docs:os-reference-docs/documentation-linking-explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/documentation-linking-explainer.md); this document explains the program behind it.*

## What it is

`mb-doc-check` is a small program that runs at the moment you commit documents. Its job is to make sure that every document entering the history of the documentation repositories listed in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md) is correct: it has its frontmatter, every link in it is in one standard form and points to a document that exists, and links elsewhere that point to a document you just renamed or moved are repaired. It does this by editing the text of the documents themselves, and nothing else.

It is not an AI. It makes no judgments. For the same documents it always produces the same result, and that is deliberate: the documents are written by AI agents, and the checker must not be a second source of variation.

## What it can do

At every commit the program looks at two pictures of the repository: the committed state, and the state that is about to be committed. Comparing them tells it what is new, what moved and what was deleted.

**Identity comes from the `doc-id`.** Every document carries a permanent random code in its frontmatter. When a file appears under a new name or in a new folder, the program matches it to the old file by that code, not by the name and not by the content. So a document that was renamed and completely rewritten is still recognised as the same document. This holds across repositories too: a document cut from one covered repository and pasted into another keeps its `doc-id`, and every link to it follows it.

**Then, for every document in the commit,** it:

1. completes the frontmatter (title, `doc-id`, `updated`);
2. reads every link written in any accepted form (`[[name]]`, `[[folder/name]]`, `[[source-id:name]]`, an ordinary markdown link to a document, or a document path pasted into the text) and decides which document it means;
3. rewrites it in the standard form, with the source id and page name for GBrain and the full path for MarkText;
4. for links whose target moved, rewrites them to the new place, in every covered repository;
5. turns links to deleted documents into plain words;
6. stores the file with LF line endings.

**Deciding which document a link means.** A name is matched to a document's file name, ignoring upper and lower case. A name that exists in the linking document's own repository wins over the same name elsewhere. If the name still names several documents, or none, the link is not rewritten, and if you just typed it, the commit is stopped.

**Where the knowledge comes from.** A small settings file lists which folder is which GBrain source, so that the program can write the source id into every link.

## Suitability

- **Best for:** keeping a body of documentation, written mostly by AI agents across several repositories, consistent and navigable without anyone having to remember a rule.
- **Good for:** renaming and moving documents; retiring documents into `obsolete`; bringing an existing repository under the rules in one pass; checking a repository at any time without changing it.
- **Not good for:** documents outside the covered repositories; commits made from Windows programs (the hook only exists in WSL's Git); judging whether a document's content is right. It checks form and links, never meaning.

## Why it works this way

**It runs at commit, not on a schedule.** A document is correct at the moment it enters history, so errors never accumulate and no cleanup run is ever needed. A scheduled checker would find errors after the fact and leave someone to fix them.

**It edits text only and never moves, renames or deletes a file.** Where documents live is a decision for you. A program that reorganised files on its own would make surprises, and surprises in a documentation system cost far more than a link that has to be fixed by hand.

**It stops a commit only for what that commit introduced.** It compares the new state with the committed state. A broken link that already existed is reported and never blocks, because otherwise one old problem would stop all work. A broken link you just typed does block, because a mistake caught now costs one line, and later it costs a search.

**It fails open.** If the program itself breaks, it says so and lets the commit through. A helper's bug must never stop your work. The price is that one commit goes unchecked, and the next commit of those documents, or the `check` command, corrects it.

**It is repeatable.** Running it twice gives the same result as running it once. That makes every step safe to retry, and it is what allowed whole repositories to be converted in one pass and checked afterwards.

**The settings are files, not calls to GBrain.** The hook must be fast, work with no network and not depend on anything running. So the folder-to-source table lives in a file. `sources-check` compares that file with GBrain whenever you want to be sure it is true.

**The page-name rule is a copy of GBrain's, not a call to GBrain.** A copy answers in milliseconds for thousands of links and needs nothing else to be running. `slug-selftest` proves, on your real documents, that the copy gives exactly GBrain's answers; it is run after every GBrain upgrade.

**The `updated` date moves only on a real change.** The date is useful only if it can be trusted. A line-ending conversion, or a commit whose only effect would be the date itself, must not move it. So such documents are put back, and the commit says "NOTHING TO COMMIT".

**Exemptions are by name and by folder, never by judgment.** Files named `tmp-...`, folders such as `stencils`, `quarantine`, `backups`, `catalogue` and `logs`, Anvil app roots, `obsolete` folders and `SKILL.md` files are not part of the documentation to be kept consistent: they are scratch or generated material, retired material, or installed skills with their own format. Because the program applies the list mechanically, nobody has to decide case by case.

**Repaired files join the same commit.** When a rename in one repository makes a link in another repository wrong, the program corrects that file. The correction stays uncommitted in the other repository until that repository is committed, which is why one command commits all of them together.

**One program, one settings file, the repositories listed in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md).** Every repository behaves identically, because there is nothing local to configure and nothing to drift.

## What has to happen

- Commit in WSL, with `commit-all.sh`, and never with `--no-verify`.
- Keep `mb-doc-check.sources` true: after any change to GBrain's sources, run `sources-check`.
- After every GBrain upgrade, run `slug-selftest`.
- When a commit is stopped, read the message, fix the named line and commit again.
- Add a new repository by following the steps in [[[mybizz-config-docs:mb-doc-check/doc-check-reference]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-reference.md).
