---
title: "mb-close-out-explainer"
doc-id: "mb-a72cf175"
updated: "2026-10-07"
---
# mb-close-out — Explainer

## What this actually is

A long session ends with everything that matters still trapped inside the
conversation: what was decided, what changed on disk, which facts are worth
trusting later. `/mb-close-out` is the one command that ends a session without
losing any of that. It is an orchestrator: it replaces no existing piece — it
walks the session page, the fact pipeline, the project documents, and the
commit procedure in one run, and it concentrates every decision the developer
must make into a single approval gate plus at most two terminal blocks to
paste.

The design premise is that memory lives outside conversations. The session
summary becomes a GBrain page; durable facts become numbered GBrain facts, the
governed ones through the memory governor's verification pipeline; and the
commit hook keeps every document correct as it enters history. After a
close-out, the conversation itself is never needed again — a future session
restores context by searching, not by scrolling back.

## What it can do (conceptually)

- Close any session, on demand, from any layer — an OpenCode session, a PDLF
  session, mid-project. Nothing closes without the developer asking.
- Sort the session's durable knowledge into two lanes — advisory (saved
  directly) and governed (saved through verification and contradiction
  checking) — and persist every governed fact also as a searchable document.
- Fold project-document maintenance into the same run when the session worked
  in one of the five projects, with that skill's approval folded into the
  same gate.
- Sweep every repository for uncommitted changes and surface anything that is
  not this session's work before anything is committed.
- Leave the memory system clean: every governed fact either landed or is
  explicitly pending the developer's promotion, and the governor review queue
  ends empty.

## Best for / good for / not good for

**Best for:** ending any working session — it is the standing close-out
procedure for the whole division, and the only path that saves governed facts.

**Good for:** saving facts outside a session's end — saying "save these as
facts" runs the same steps without the commit tail. A session that touched no
project and produced no facts also closes cleanly: the skill says so and
skips what does not apply.

**Not good for:** committing work — the agent never commits; the developer
pastes the commit command. Mid-session note-keeping — capture during work
belongs to GBrain capture, not to the close-out. Automatic end-of-session
triggering — close-out is on demand only, by standing decision.

## Why it is built this way

**One orchestrator over existing pieces, replacing none.** The division
already had every piece — the session-page convention, the fact pipeline, the
project-documents skill, the commit procedure, the governor queue. The
workflow-review decision was to compose them rather than build a parallel
system, so each piece keeps its own suite and this skill only sequences them
and concentrates the approvals.

**One gate, not three.** The fact pipeline (mb-submit-memory Step 5) and the
project-documents skill (its Step 6) each require an explicit approval. The
close-out gate is defined as satisfying both, so a close-out presents
everything once — session page, facts, routing, project-doc presentation,
flagged files — and one approval releases all of it. After the gate,
execution only.

**Terminal blocks instead of agent authority.** The agent holds no Git
authority, no credentials, and no grant-approval power — by standing rule and
by Cupcake enforcement. Every action that needs one of those becomes a fully
literal line the developer pastes: the commit, any grant, any blocked step,
and the governor promotion when a governed fact lands in review. The
known-values-only rule for terminal blocks exists because a block assembled
from remembered output is exactly where a wrong value would enter a
privileged command.

**The worker log is the record, not recall.** Agent-side GBrain recall cannot
see facts saved under other projects' scopes — a platform property, not a
fault. A governed fact confirmed by the worker log exists even when recall
misses it; re-submitting to "make it appear" would duplicate it. The same
logic makes `under_review` designed behaviour rather than an error: the
promotion is a developer decision through the review endpoint, never an
agent-side retry.

**An empty review queue is the end condition.** An open review item blocks
PDLF steps everywhere, so a close-out that leaves one pending would quietly
poison the next session. The queue-empty check is part of Step 9, and the
DONE_WITH_REVIEWS_PENDING status exists so a close-out can end honestly while
promotions are still outstanding.

**Why there are no log files anymore.** An earlier design kept a sessions log
and a facts log as readable indexes. The workflow-review retired both: the
session pages and the facts already live in GBrain and are found by search,
so the logs added ceremony without adding value, and neither had been written
since 2026-09-23. Reopening a session is now "open the last session about
<topic>", answered by searching `sessions/` pages.

## Where it sits

Upstream: any session in any layer. Downstream: the commit-all procedure
(developer-run terminal block), which carries the mb-doc-check hook that
keeps documents correct at entry. It calls: mb-submit-memory (governed
facts), mb-project-docs (project documents), GBrain `put_page` and
`remember`, and the memory-governor review endpoint (developer-run). The
pointer documents — opening-and-closing, fact-save-and-recall, daily-ops —
all defer to the skill's own file as the authoritative procedure.

## Open architectural questions

1. **What defines session numbers now?** Numbered page names (`001`, `002`,
   …) continued by convention after the sessions log was retired, but no
   current document states the rule. It matters because page-name uniqueness
   and ordering both depend on it. Resolution lands in the correction of the
   retired-log fact file (config open item 3).
2. **Stale pointers in the governance layer.** Global AGENTS.md (three
   spots), the data-mybizz-mgt README, and the dev-root docmap still describe
   the retired logs as current. Until those developer-owned edits land, two
   sources of truth for close-out exist; the skill's own file and this suite
   are the authoritative ones.