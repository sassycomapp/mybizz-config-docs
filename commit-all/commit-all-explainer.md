---
title: "commit-all-explainer"
doc-id: "mb-a85c9c4f"
updated: "2026-10-16"
---
# commit-all — Explainer

## What it is

Commit-all is the one command that closes the books after any work: it commits every documentation repository and the scripts repository with a single message, refreshes GBrain so the changed documents are searchable, pushes everything to GitHub, and prints one summary table. It solves a bookkeeping problem: with more than a dozen repositories, ending work means many commits that must not be forgotten, in an order that keeps the search index and the remote copy in step with what is on disk.

## What it can do

- Commit every repository that has changes under one shared message, while reporting per repository.
- Show what would be committed, changing nothing.
- Keep one log that always reflects the last run.
- Warn when a repository has lost its commit hook, and surface any repository the hook stopped.
- Update GBrain and push to GitHub in the same pass, reporting either phase's failures in the summary.

## Suitability

Best for ending any documentation or skill work anywhere in the division, and for the last step of a close-out. Good for a catch-up run when a previous ending was skipped. Not good for application code repositories, where a commit is a deliberate code change; not for the memory governor's code, which is committed by hand; not for the Anvil reference clone, which is never pushed. When the whole end-of-session sequence is wanted — session page, facts, project documents, then the commit — mb-close-out orchestrates it and calls commit-all as its last step.

## Why it works this way

One message covers all repositories because real work usually spans several, and the per-repository summary maps the shared message back to each result. Document quality is not this script's job: the mb-doc-check hook runs inside each commit, so the script only orchestrates and relays what the hook decides. The log is replaced rather than accumulated because the last run is the one being diagnosed and git already keeps history; the log answers "what happened just then", not "what ever happened". The hook check inside phase 1 exists because a lost hook fails silently — every commit would simply succeed unchecked — so the run itself makes the loss visible. GBrain runs before the push so the search index and the remote copy move together, and a failure in either is counted, not swallowed: the closing line distinguishes a clean run from one needing attention.

## What has to happen

The developer runs it after work — agents never do, by standing policy. Every repository on the list keeps its mb-doc-check hook. A new repository is added in the documented order: GitHub, GBrain, the hook, the register row, then the script's list — so the register and the script never disagree. The how-to page is updated whenever the script's behaviour changes. mb-close-out keeps calling it as its last step, and its documents point here for commit-all's own behaviour.
