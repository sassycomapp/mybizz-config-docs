# mb-submit-memory — Reference: Usage, Invocation, and the Full Cycle

Companion to `mb-submit-memory-config.md` (current installed state, prerequisites,
open items) and `mb-submit-memory-explainer.md` (design rationale and the one
confirmed real incident). Agent-facing.

---

## Invocation

```
/mb-submit-memory (path)
```

Quote paths containing spaces. The path is always given explicitly by the
developer — never inferred or guessed.

## Before anything else — confirm the path is in scope

```bash
gbrain sources list
```
If the target path is not inside any listed source's registered path, STOP
and report it. This skill never registers a new source on its own.

## The full cycle (one continuous run)

1. **Learnings** — check `/mnt/c/mybizz/logs/mb-submit-memory/learnings.md` for
   any already-settled pattern relevant to this path's source; apply rather
   than re-derive.
2. **Backup** — none needed. The skill only reads the target file and submits
   a copy of its content elsewhere; the original is never modified.
3. **Detect** — query GBrain for related content using real phrases from the
   file's actual content (not just the filename):
   ```bash
   gbrain call recall '{"grep": "<a real, specific phrase from the content>"}'
   ```
   Run more than one query if the content spans more than one real topic.
   Then form:
   - **Confidence** (`method: "model_based"`):
     - **0.85+** — clearly/unambiguously stated, and either nothing related
       was found or what was found squarely agrees.
     - **0.5–0.85** — understandable but genuinely ambiguous, or partial,
       unconfirmed overlap with existing content.
     - **below 0.5** — vague, speculative, or genuinely unclear what it claims.
   - **Contradiction**:
     - nothing related, or agreement → omit the `contradiction` field entirely.
     - genuine conflict found → `detected: true`, `cross_project` set per
       whether the conflicting content belongs to a different project's
       source, `resolution: null` (never resolved by the skill itself).
     - deliberate replacement of already-outdated content → **supersession**,
       not contradiction — `resolution: "closed_by_new_fact"`.
4. **Report** — present inline, before submitting anything: the real file
   path, a plain description of the content, what GBrain's query returned,
   the confidence score with which band and why, and any contradiction found.
   Then stop and wait for the developer's reply in the same run.
5. **Approve** — the developer's reply is one of: approval as-reported, a
   correction (authoritative — submit exactly what they return), a
   clarification request, or a rejection (skip this file, no submission).
   Step 6 never runs without an explicit approval on record for this file,
   in this same run.
6. **Apply** — submit through the governor's real API:
   ```
   POST http://127.0.0.1:8321/memory/candidate
   Header: X-Governor-Credential: <manual_submission or pdlf_step_sync>
   Body:
   {
     "owning_project": "<project slug>",
     "visibility": "project_local",
     "retention": "long_term",
     "memory_type": "fact",
     "source_type": "user",
     "source_ref": "<real, full file path>",
     "policy_version": "v1",
     "confidence": {"score": <Step 3 number>, "method": "model_based"},
     "contradiction": <Step 3 object, or omit entirely if none>
   }
   ```
   Leave `content` out entirely — the governor reads the real file itself
   from `source_ref`. Do not paste the content in as well.
7. **Verify** — read the real response:
   - `"status": "promoted"` — now durable memory. Report plainly with the
     real `memory_id`.
   - `"status": "under_review"` — waiting in the governor's review queue.
     Not an error. Report plainly with the `memory_id`; do not attempt to
     resolve it or resubmit.
   - Outright failure (connection error, abnormal non-2xx) → STOP, report the
     real error message, do not retry silently or guess at the cause.
8. **Log** — append to `/mnt/c/mybizz/logs/mb-submit-memory/`: file path,
   confidence score + method, contradiction outcome, real result
   (`promoted`/`under_review`), real `memory_id`.
9. **Learnings** — record anything durable for next time (a search-term
   pattern that worked, a source that tends to need a lower confidence band,
   a naming convention confirmed for a project) to the same learnings file.

**Folder given instead of a file:** repeat steps 3–8 once per real file
inside (excluding `obsolete`, `archive`, anything with `backup` in the name,
and dotfolders), each with its own independent judgment. End with a summary:
files submitted, promoted, under review, and any the developer rejected at
Step 5.

## Completion status protocol

Reported at the end of every run:

| Status | Meaning |
|---|---|
| `DONE` | Every file submitted; every outcome reported plainly. |
| `DONE_WITH_REVIEWS_PENDING` | Completed, but list every `under_review` file with its `memory_id`. |
| `BLOCKED` | Cannot proceed — state exactly what stopped it (missing source registration, API error, missing credential) and what was tried. |
| `REPORT_REJECTED` | Developer rejected a Step 4 report for a given file — state what needs to change. Other files in the same folder run may still proceed independently. |

Never mark a run `DONE` if any file's Step 7 verification was skipped. Never
run Step 6 without an explicit approval on record from within the same run.

## Real confirmed example (2026-08-27 run)

See `mb-submit-memory-explainer.md` §5 for the full worked incident —
`spec-postgres-ledger.md`, confidence 0.85, correctly judged a supersession
rather than a contradiction, `memory_id 22e49b30-e023-4979-904a-2c1a27ec7513`,
outcome `promoted`.
