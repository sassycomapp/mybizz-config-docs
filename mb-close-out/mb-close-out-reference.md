---
title: "mb-close-out-reference"
doc-id: "mb-4b40508e"
updated: "2026-10-10"
---
# mb-close-out — Reference

Execution procedure for `/mb-close-out`. Run only on explicit developer
invocation. Why it is built this way: [[[mybizz-config-docs:mb-close-out/mb-close-out-explainer]]](C:/mybizz/mybizz-config-docs/mb-close-out/mb-close-out-explainer.md).

## Rules (always in force during a run)

1. Never commit, push, run a Git command that changes anything, or use credentials. Each such action becomes a numbered line in the developer's terminal block.
2. Never approve a grant. When a read or write is blocked, hand the developer exactly `mg-grant --path <folder> --count N`, with the count the work needs.
3. A denial is final. Never retry, reshape or route around it; it becomes a developer-run line.
4. One approval gate (Step 5). After it, execution only.
5. A terminal block contains only known values. A value that exists only in an earlier block's output goes into a second, fully literal block.
6. Nothing is left open. A step that cannot be completed becomes a numbered line in the developer's block.
7. Credentials are referenced by variable name only; never printed, logged or copied.

## Procedure

### Step 1 — Session page

Write the session summary as a file, `sessions/<YYYY-MM-DD>-<short-slug>.md`: in the current repository when it is on the commit-all list, otherwise in `C:\mybizz\mybizz-config-docs\sessions\`. Body only; the commit hook adds the frontmatter, and commit all imports the page into GBrain. Never use `put_page` or `gbrain capture` for it (see the decision in the explainer).

### Step 2 — Candidate facts

1. List durable rules, decisions and gotchas only. One claim each. Skip any fact a committed document already states. A session with no facts says so.
2. Route each fact: **advisory** (default — context, pointers, findings that only need to be found again) or **governed** (rules, decisions and procedures that must be trusted later without re-checking). When unclear, ask one focused question at the gate.
3. For each governed fact, write one fact file named `<YYYY-MM-DD>-<slug>.md`:
   - Current repository on the commit-all list → `<current-repo>/facts/`
   - Otherwise → `C:\mybizz\mybizz-config-docs\facts\`
   - Body only; the commit hook adds the frontmatter.
4. For each fact file, run `mb-submit-memory` Steps 1–4. Its reports go into the gate message.

### Step 3 — Project documents

When the session worked in one of the four projects (`mb-3-cs`, `mb4ecom`, `mb5pdlf`, `pdlf`), run `/mb-project-docs` up to its Step 6. Its presentation goes into the gate message. Otherwise skip this step.

### Step 4 — Changed files

```
bash /mnt/c/mybizz/scripts/commit-all.sh --status
```

Flag any change that is not this session's work; the developer decides at the gate whether it is kept.

### Step 5 — The gate

Present once, in one message: the session page title; the candidate facts (subject, fact, routing); the `mb-submit-memory` report for each governed fact; the project-document presentation; the flagged files. Then STOP.

The developer may cancel, amend, reword or re-route; the amended set is final. This approval is the approval that `mb-submit-memory` Step 5 and `mb-project-docs` Step 6 require.

### Step 6 — After the approval

1. Advisory facts: save each with `remember` — visibility `world`, provenance naming the session, entity set when the fact has a subject. Keep each returned `fact-NN`.
2. Governed facts: run `mb-submit-memory` Steps 6–9 for each approved fact file, exactly as that skill defines them.
3. Project documents: run `/mb-project-docs` Step 7.

### Step 7 — Terminal block 1 (developer)

Produce one fully literal block, in this order:

1. The `AGENTS.md` copy line from Step 6.3, when there is one.
2. Any line produced by Rules 1, 2 or 6.
3. `bash /mnt/c/mybizz/scripts/commit-all.sh "close-out: <topic>"`

The developer pastes the output back.

### Step 8 — Terminal block 2 (developer; only when a governed fact is under review)

One literal promote per memory id reported `under_review` in Step 6.2:

```bash
cd /home/dev-p/memory-governor && set -a && source .env && set +a
curl -s -X POST http://127.0.0.1:8321/memory/<memory-id>/review \
  -H "X-Governor-Credential: $MEMORY_GOVERNOR_WRITER_MANUAL_SUBMISSION" \
  -H "Content-Type: application/json" \
  -d '{"decision": "promote", "reason": "approved at the <date> close-out gate", "reviewer": "dev-p"}'
```

### Step 9 — Verify and report

- Commit all: every repository `committed` or `nothing to commit`, `pushed` or `already up to date`, ending `All done.` Any "the mb-doc-check hook is not installed" warning or BLOCKED repository: STOP; the developer fixes it and runs the same command again.
- Governed facts: `grep "remembered as fact" /tmp/memory-governor-worker.log | tail -10` is the record of what landed and its fact numbers. If recall shows nothing but the worker log confirms the write, the fact exists; never re-submit.
- The governor review queue must be empty before the close-out ends.
- Report: the session page, facts with their numbers, project documents, the commit summary, anything flagged.

## Completion status

| Status | When |
|---|---|
| DONE | Every step verified; review queue empty |
| DONE_WITH_REVIEWS_PENDING | Governed facts still `under_review` — list each open memory id |
| BLOCKED | State what stopped the run and what was tried |

Never report DONE with an unverified step.

## Do not

- Never auto-trigger; `/mb-close-out` runs only on explicit invocation.
- Never commit, push, or run any Git command that changes anything (Rule 1).
- Never approve a grant, and never re-ask a denied one in a new shape (Rules 2–3).
- Never proceed past the gate on anything but the developer's explicit approval (Rule 4).
- Never put a value from earlier output into terminal block 1 — use a second literal block (Rule 5).
- Never leave a failed step unreported; it becomes a developer line (Rule 6).
- Never print, log or copy a credential value (Rule 7).
- Never resolve `under_review` by re-submitting with a different confidence — resolve through Step 8 only.
- Never treat an agent-side recall miss as evidence a governed fact is lost — the worker log is the record.
- Never end a close-out with a non-empty governor review queue.
- Never write to the retired sessions-log or facts-log — they no longer exist (retired by decision, workflow-review Task 1.7).

Sub-procedure detail is owned by its own suite: `mb-submit-memory` Steps 1–4/6–9 → [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-reference]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-reference.md); commit-all behavior → [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md); the five projects and mb-project-docs → [[[mb-project-docs:mb-project-docs]]](C:/mybizz/mb-project-docs/mb-project-docs.md).