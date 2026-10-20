---
title: "mb-close-out-explainer"
doc-id: "mb-a72cf175"
updated: "2026-10-20"
---
# mb-close-out — Explainer

## What it is

A long session ends with everything that matters still trapped inside the conversation: the decisions taken, the files touched on disk, the facts worth trusting later. `/mb-close-out` is the one command that ends a session without losing any of that. It is an orchestrator: it replaces no existing piece — it walks the session page, the fact pipeline, the project documents, and the commit procedure in one run, and it concentrates every decision the developer must make into a single approval gate plus at most two terminal blocks to paste.

The design premise is that memory lives outside conversations. The session summary becomes a searchable page; durable facts become numbered facts, the governed ones through the memory governor's verification pipeline; and the commit hook keeps every document correct as it enters history. After a close-out, the conversation itself is never needed again — a future session restores context by searching, not by scrolling back.

## What it can do

- Close any session, on demand, from any layer — an OpenCode session, a PDLF session, mid-project. Nothing closes without the developer asking.
- Sort the session's durable knowledge into two lanes — advisory (saved directly) and governed (saved through verification and contradiction checking) — and persist every governed fact also as a searchable document.
- Fold project-document maintenance into the same run when the session worked in one of the four projects, with that skill's approval folded into the same gate.
- Sweep every repository for uncommitted changes and surface anything that is not this session's work before anything is committed.
- Leave the memory system clean: every governed fact either landed or is explicitly pending the developer's promotion, and the governor review queue ends empty.

## Suitability

**Best for:** ending any working session — it is the standing close-out procedure for the whole division, and the only path that saves governed facts.

**Good for:** saving facts outside a session's end — saying "save these as facts" runs the same steps without the commit tail. A session that touched no project and produced no facts also closes cleanly: the skill says so and skips what does not apply.

**Not good for:** committing work — the agent never commits; the developer pastes the commit command. Mid-session note-keeping — capture during work is not part of the close-out. Automatic end-of-session triggering — close-out is on demand only, by standing decision.

## Why it works this way

**One orchestrator over existing pieces, replacing none.** Every piece exists on its own — the session-page convention, the fact pipeline, the project-documents skill, the commit procedure, the governor queue. The standing workflow-review decision is composition over a parallel system: each piece keeps its own suite, and this skill only sequences them and concentrates the approvals.

**One gate, not three.** The fact pipeline (mb-submit-memory Step 5) and the project-documents skill (its Step 6) each require an explicit approval. The close-out gate is defined as satisfying both, so a close-out presents everything once and one approval releases all of it. After the gate, execution only.

**Terminal blocks instead of agent authority.** The agent holds no Git authority, no credentials, and no grant-approval power — by standing rule and by Cupcake enforcement. Every action that needs one of those becomes a fully literal line the developer pastes: the commit, any grant, any blocked step, and the governor promotion when a governed fact lands in review. The known-values-only rule for terminal blocks exists because a block assembled from remembered output is exactly where a wrong value would enter a privileged command.

**The worker log is the record, not recall.** Agent-side GBrain recall cannot see facts saved under other projects' scopes — a platform property, not a fault. A governed fact confirmed by the worker log exists even when recall misses it; re-submitting to "make it appear" would duplicate it. The same logic makes `under_review` designed behaviour rather than an error: the promotion is a developer decision through the review endpoint, never an agent-side retry.

**An empty review queue is the end condition.** An open review item blocks PDLF steps everywhere, so a close-out that leaves one pending would quietly poison the next session. The queue-empty check is part of the final step, and the DONE_WITH_REVIEWS_PENDING status exists so a close-out can end honestly while promotions are still outstanding.

**Why there are no log files.** The session pages and the facts live in GBrain and are found by search; a readable log on top of them would add ceremony without adding value. Reopening a session is "open the last session about \<topic\>", answered by searching the session pages.

**Why session pages are files, not GBrain writes.** Writing into a GBrain source's folder needs a source owner, and no source has one — such writes are refused. MyBizz does not adopt GBrain's writer model. Fact writes stored in the database are not affected.

## What has to happen

- The developer runs the gate decision and every terminal block; the agent holds none of that authority.
- Commit all must exist and its document hook must be installed — the close-out's session page, fact files and document updates all enter history and GBrain through it.
- The memory governor's API and worker must be running for the governed path: the queue-empty end condition and the landing record both depend on it.
- The pointer documents — opening and closing, fact save and recall, daily ops — defer to this suite as the authoritative close-out procedure; they must keep pointing here.
- Invocation stays explicit: nothing may auto-trigger a close-out.
