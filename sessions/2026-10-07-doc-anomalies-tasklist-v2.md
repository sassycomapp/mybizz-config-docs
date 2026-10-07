---
title: "2026-10-07-doc-anomalies-tasklist-v2"
doc-id: "mb-3df77977"
updated: "2026-10-07"
---
# Session — 7 October 2026 — Documentation anomalies task list rebuilt

Closed out on 7 October 2026. The session worked in `C:\data-mybizz-mgt` (data-mybizz-mgt repository, on the commit-all list).

## What was done

`C:\data-mybizz-mgt\desktop\documentation-anomalies-task-list.md` was rebuilt from version 1 to version 2. Version 1 was a flat findings table — 39 documentation anomalies found while drafting the mybizz-os explainer, none yet fixed. Version 2 is an execution-ordered task list: every v1 item kept with its original number, ordered by dependency and effort.

- Section 1 — Dependencies: six decisions and verifications other tasks wait on (one home for the environment explainer; master memory explainer maintenance rule versus `/mb-close-out`; mb-3-cs design figures; three live-state verifications; frontmatter re-certification; two sysdoc-creator open items).
- Section 2 — Quick fixes: 12 tasks.
- Section 3 — Small edits: 13 tasks.
- Section 4 — Larger rewrites: 3 tasks (environment explainer, master memory explainer, PostgreSQL backup section).
- Section 5 — Done, plus a completeness check.

Working rule recorded in the document header: run commit all once at the end of each section, not after every task.

## Evidence

- data-mybizz-mgt git status at close-out: one modified file, `desktop/documentation-anomalies-task-list.md` (50 lines grew to 327). It lands in the close-out commit.
- Task 2.1 (retire the session-numbers fact) was already completed before the rewrite — commit 91b445c in data-mybizz-mgt.

## Decisions and standards

- Gate decisions (2026-10-07): the session page was approved as drafted and landed as a file under `sessions/` through a one-write grant; the flagged `daily-ops.md` blank line was reverted rather than kept.
- The ordering principle and section structure are stated in the task-list document header itself; execution starts at Section 1.
- Candidate fact set for this session: zero. Everything durable is stated in the committed document, so no fact files and no governed submissions.

## Quirks

- `put_page` was blocked two ways during close-out: the mybizz-config-docs brain source is outside the close-out connection's write grant (denial final, not retried), and the `default` source has no designated canonical owner (`gbrain sources writer status` shows `enabled: false` — an operator-level topology state left for review). The page therefore follows the on-disk `sessions/` file convention and reaches GBrain through commit-all's sync.
- Session instructions were not pasted into this session; the developer gave only the project context `C:\data-mybizz-mgt`.

## What is open

- The task list itself is open by design; execution begins at Section 1.1 (decide one home for the environment explainer).
- Where to look: `C:\data-mybizz-mgt\desktop\documentation-anomalies-task-list.md` holds the detail; this page records what happened.