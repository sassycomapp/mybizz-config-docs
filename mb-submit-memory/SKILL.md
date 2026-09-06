---
name: mb-submit-memory
description: |
  Submit one real file or folder's content through the memory governor's
  governed submission pipeline — never GBrain's raw sync/remember commands
  directly. One continuous skill run per invocation — learnings, backup,
  detect (query GBrain, form a genuine confidence/contradiction judgment),
  report, pause inline for approval, apply (submit), verify, log, learnings —
  the same single-run modus operandi as Docs Manager and mb-wikilinks.
  Invoked as /mb-submit-memory (path). Use only when explicitly invoked —
  never auto-trigger. A folder path is never submitted in one call; every
  real file inside it is enumerated and submitted individually, each with
  its own separately-formed judgment — never a shared or batched assessment.
---

# mb-submit-memory

Submits real, developer-authored content into durable GBrain memory through
the memory governor — the single, correct path for anything meant to be
checked before it becomes permanent. Never calls `gbrain remember` or
`gbrain sync` directly. Never assigns a placeholder confidence score or
skips the contradiction check to save time — a placeholder value here
would defeat the entire purpose of this skill existing.

**One continuous run — same modus operandi as Docs Manager and
mb-wikilinks.** `/mb-submit-memory (path)` is a single skill invocation
covering learnings → backup → detect → report → approve → apply → verify →
log → learnings. The run pauses in place at the report step and presents
findings; the moment the developer replies with approval in the same
conversational continuum, the same run resumes through apply, verify, log,
and learnings. The developer never has to re-invoke the skill to finish a
run already in progress.

---

## User-invocable

When the developer types `/mb-submit-memory (path)`, run the full Section 2
cycle for that exact path, start to finish, as one continuous run. The path
is always given explicitly by the developer — do not infer or guess which
file or folder is "probably what they mean."

Quote paths containing spaces.

---

## Section 0 — Prerequisites and hard rules. Do not deviate.

1. **The target path MUST already be inside a folder that is part of a
   registered GBrain source.** Confirm this before doing anything else:
   ```bash
   gbrain sources list
   ```
   If the path is not inside any listed source's registered path, STOP.
   Report this to the developer. Do not proceed, and do not offer to
   register a new source yourself — that is Step 11's job, not this
   skill's.

2. **The real memory-governor API address, needed for every call in this
   skill:**
   ```
   MEMORY_GOVERNOR_API_BASE = http://127.0.0.1:8321
   ```
   Confirmed live, 2026-08-25: a real `uvicorn` process serving `app.main:app`
   is running on this exact address inside WSL. This only works from
   inside the same WSL environment this process runs in — not reachable
   from outside it. If this skill is ever moved to run somewhere else,
   this address needs reconfirming, not assumed to still be correct.

3. **The credential used for every submission in this skill depends on how it was
   invoked — never hardcoded to one value:**
   - If a developer typed `/mb-submit-memory (path)` directly, themselves, right now:
     use the `manual_submission` writer credential.
   - If a PDLF step's own housekeeping instructions are the ones invoking this skill,
     as routine, automatic procedure at the end of a step: use the `pdlf_step_sync`
     writer credential instead. This is not the same situation as a developer asking
     for something specific — it is a PDLF step's own systematic submission of its own
     work, and the credential used should say so honestly in the governor's own
     records.
   Both credentials are read from wherever the developer has configured them —
   never hardcode either literal credential value into this file. If it is genuinely
   unclear which situation applies, ask the developer directly rather than guess.

4. **Never submit a folder path in a single API call.** If the target path
   is a folder, enumerate every real file inside it (excluding anything
   already excluded by this environment's standing content-scope rules —
   `obsolete`, `archive`, anything with `backup` in the name, dotfolders)
   and run the full Section 2 cycle's detect/report/approve/apply steps
   **once per file**, each with its own independently-formed judgment.
   Never share one confidence score or one contradiction assessment across
   multiple files.

5. **Never assign a fixed or default confidence score.** Section 2, Step 3
   below gives the exact, concrete method for forming a real one. There is
   no acceptable shortcut.

---

## Section 1 — What this skill never does

- Never calls `gbrain remember`, `gbrain sync`, or any other GBrain command
  directly. The memory governor's own API is the only thing this skill ever
  calls to get content into durable memory.
- Never proceeds past a needs-review outcome on the developer's behalf.
  If the governor reports that a submission needs review rather than
  auto-promoting it, that is not a failure of this skill — report it
  plainly and stop; the developer resolves it separately, through the
  governor's own review mechanism.
- Never re-attempts a submission with a different confidence value to
  "get past" a needs-review outcome. The number reported in Section 2,
  Step 3 is submitted once, exactly as formed.

---

## Section 2 — Per-invocation cycle (one continuous run)

### Step 1 — Learnings

Check this skill's own log location (see Step 8 below) for any prior
learnings relevant to the current path's source — a recurring pattern
already resolved, a naming convention already confirmed for that source.
Apply anything already-settled rather than re-deriving it.

### Step 2 — Backup

No backup step is needed. This skill never edits the target file — it only
reads it and submits a copy of its content elsewhere. The original file is
never modified.

### Step 3 — Detect (query, read, and form a real judgment — never skipped, never faked)

For the target file (or, per Section 0 item 4, for each file if given a
folder):

1. **Query GBrain for related existing content, using real search terms
   drawn from the file's actual content** — not the filename alone:
   ```bash
   gbrain call recall '{"grep": "<a real, specific phrase from the content>"}'
   ```
   Run more than one query if the content covers more than one real topic.
   A single vague query is not sufficient.

2. **Read the actual results returned.** Do not treat "a query was run" as
   equivalent to "the results were read." If nothing relevant comes back,
   that is itself a real finding — it means the content is likely new.

3. **Form the confidence score, using this concrete method — not
   free-form judgment:**
   - **0.85 or higher:** the content is clearly and unambiguously stated,
     and either nothing related was found, or what was found squarely
     agrees with it.
   - **0.5 to 0.85:** the content is understandable but has some genuine
     ambiguity in wording, or partially overlaps with existing content in
     a way that is not a clean, confirmed match.
   - **Below 0.5:** the content is vague, speculative, or you are
     genuinely uncertain what it is actually claiming.
   Use `"method": "model_based"` — this is a real reading-comprehension
   judgment, not a fixed rule and not something the developer has
   personally verified.

4. **Form the contradiction assessment, using this concrete method:**
   - **Nothing related found, or what was found agrees:** no contradiction
     — omit the `contradiction` field entirely.
   - **Related content was found and it appears to genuinely conflict**
     with the new content: contradiction detected. Set `cross_project` to
     `true` if the conflicting content belongs to a different project's
     GBrain source than the one being submitted to, `false` if it's within
     the same project. Set `resolution` to `null` — do not resolve a
     contradiction yourself.
   - **The new content is explicitly and deliberately replacing an old
     fact that is itself marked outdated or superseded** (not merely
     different from it): this is a supersession, not a contradiction — set
     `resolution` to `"closed_by_new_fact"`.

Do not submit anything in this step. This step only produces a judgment to
report in Step 4.

### Step 4 — Report

Present the findings inline, in the chat, before submitting anything:

- The real file path.
- A short, plain description of what the content actually says.
- What was found when GBrain was queried (or "nothing related found").
- The confidence score formed, and one sentence stating which of the three
  bands in Step 3 it falls into and why.
- Whether a contradiction was detected, and if so, against what.

After the report, stop and wait for the developer's reply in the same run.
Do not proceed to Step 6 in this pass.

### Step 5 — Approve (inline, same run, developer's next message)

The developer's reply is one of:
- Approval to proceed with the judgment exactly as reported.
- A correction to the confidence score or contradiction assessment — their
  correction is authoritative; submit exactly what they return, not the
  original judgment.
- A request for clarification, answered before any approval is treated as
  final.
- A rejection — do not submit anything for this file; move to the next
  file if one is pending, or end the run.

Step 6 never runs without an explicit approval on record for this exact
file, in this same run.

### Step 6 — Apply (submit through the governor)

Call the memory governor's real API:

```
POST http://127.0.0.1:8321/memory/candidate
Header: X-Governor-Credential: (the real credential value for whichever situation
applies, per Section 0 item 3 — manual_submission or pdlf_step_sync)
Body:
{
  "owning_project": "(the project slug this content belongs to)",
  "visibility": "project_local",
  "retention": "long_term",
  "memory_type": "fact",
  "source_type": "user",
  "source_ref": "<the real, full file path>",
  "policy_version": "v1",
  "confidence": {"score": (the number formed in Step 3), "method": "model_based"},
  "contradiction": <the object formed in Step 3, or omitted entirely if none>
}
```

Do not include the file's content directly in the request body — leave the
`content` field out entirely. The governor reads the real file itself from
`source_ref`. This is deliberate and already proven to work correctly;
do not "help" by pasting the content in as well.

### Step 7 — Verify

Read the API's real response. It reports one of two outcomes:

- **`"status": "promoted"`** — the content is now durable memory. Report
  this plainly to the developer, including the real `memory_id` returned.
- **`"status": "under_review"`** — the governor has determined this needs
  a human decision before it becomes permanent. This is not an error and
  not a failure of this skill. Report it plainly, including the real
  `memory_id`, and tell the developer it is waiting in the governor's own
  review queue. Do not attempt to resolve it, and do not resubmit it.

If the API call fails outright (a connection error, a non-2xx response
that isn't a normal review-queue outcome), STOP. Report the real error
message to the developer. Do not retry silently, and do not guess at what
went wrong.

### Step 8 — Log

Append to this skill's own log location — the real path is confirmed once,
the same way it was confirmed for `mb-wikilinks` (`/mnt/c/mybizz/logs/`,
in this skill's own subfolder): the file path submitted, the confidence
score and method used, whether a contradiction was detected, the real
outcome (`promoted` or `under_review`), and the real `memory_id`.

### Step 9 — Learnings

Record anything durable that would help next time — a search-term pattern
that worked well, a source where content tends to need a lower confidence
band, a naming convention confirmed for a specific project. Write to the
same learnings location checked in Step 1.

### End of run

If given a single file, the run ends here. If given a folder, per Section 0
item 4, return to Step 3 for the next file in the folder, until every real
file has been through its own complete cycle. Report a final summary: how
many files were submitted, how many were promoted, how many are waiting in
review, and any that were rejected by the developer at Step 5.

---

## Section 3 — Completion status protocol

Report one of the following at the end of a run:

- **DONE** — every file was submitted, and every outcome (promoted or
  under_review) was reported plainly.
- **DONE_WITH_REVIEWS_PENDING** — completed, but list every file whose
  outcome was `under_review`, with its `memory_id`, so the developer knows
  exactly what's waiting.
- **BLOCKED** — cannot proceed; state exactly what stopped the run (a
  missing GBrain source registration, an API error, a missing credential)
  and what was tried.
- **REPORT_REJECTED** — the developer rejected the Step 4 report for a
  given file; state what needs to change before it's redone. Other files
  in the same folder run may still proceed independently.

Never mark a run DONE if any file's Step 7 verification was skipped, and
never run Step 6 (apply) without a corresponding explicit approval on
record from within this same run.