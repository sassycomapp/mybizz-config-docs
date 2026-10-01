---
title: "mb-submit-memory-reference"
doc-id: "mb-c96f4742"
updated: "2026-10-01"
---
# mb-submit-memory — Reference: Usage, Invocation, and the Full Cycle

Companion to [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-config.md) (current state) and
[[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-explainer.md) (the memory-system map and design
reasoning). **The subject skill's own `SKILL.md` is the authoritative
procedure.** Config-management set: [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-exam-plan.md)
(transient job-spec — read second, every run), [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-exam-report.md)
(last verified state), [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-log|Log]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-log.md) (chronological events),
[[[mybizz-config-docs:mb-submit-memory/submit-memory-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/submit-memory-learnings.md) (transient knowledge). Agent-facing.

## Invocation

```
/mb-submit-memory (path)
```

Quote paths containing spaces. The path is always given explicitly by the
developer — never inferred or guessed.

## Prerequisites — in order, before anything else

1. **Target path is inside a registered GBrain source:**
   ```bash
   gbrain sources list
   ```
   If not, STOP and report. This skill never registers The use of registers has been discontinued. Please review a source itself.
2. **The memory governor must be running** — both processes, API and worker
   (verified by a live check first; since 2026-09-15 they run as systemd user
   services, so they normally start by themselves):
   ```bash
   ss -tlnp | grep 8321
   systemctl --user is-active memory-governor-api memory-governor-worker
   ```
   If either is not active: `systemctl --user start memory-governor-api
   memory-governor-worker`. Manual fallback, only when the units are down (from
   the governor folder):
   ```bash
   cd /home/dev-p/memory-governor && set -a && source .env && set +a && setsid nohup .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321 >> /tmp/memory-governor.log 2>&1 < /dev/null &
   ```
   `.env` must be sourced first — without it the governor cannot reach its
   database and every submission 401s. Never read, print, or copy `.env`'s
   contents.
3. **Enforcement note:** with Cupcake active, the apply step's loopback API
   call is permitted by the outbound-network rule's loopback exemption
   (amended 2026-09-08, live-verified). Do not remove that exemption.

## The full cycle (one continuous run)

1. **Learnings** — check `/mnt/c/mybizz/logs/mb-submit-memory/learnings.md`
   for already-settled patterns relevant to the path's source; apply rather
   than re-derive.
2. **Backup** — none needed: the target file is only read; the original is
   never modified.
3. **Detect** — query GBrain for related content using real phrases from
   the file's actual content (verified working command form):
   ```bash
   gbrain call recall '{"grep": "<a real, specific phrase from the content>"}'
   ```
   More than one query if the content spans more than one topic.
   **Known recall gap (2026-09-30).** This search reads the source selected by
   the current folder (in GBrain 0.59.18.0 also every federated source). Governed
   facts are stored in the source `memory-governor-code`, which is not federated,
   so a zero result does not prove that no governed fact exists — the 2026-09-30
   run reported exactly this. A possible remedy, not adopted and not yet
   exercised: a second search restricted with `"source_id": "memory-governor-code"`
   (an input added in 0.59.18.0). The decision sits with the developer (governor
   configuration, Pending developer execution item 6); a change to the procedure
   belongs in the skill's own `SKILL.md`. Then form:
   - **Confidence** (`method: "model_based"`): 0.85+ clearly stated and
     nothing related found, or found content squarely agrees · 0.5–0.85
     understandable but genuinely ambiguous or partial unconfirmed overlap ·
     below 0.5 vague, speculative, or unclear.
   - **Contradiction**: nothing related or agreement → omit the field
     entirely · genuine conflict → `detected: true`, `cross_project` set by
     which project's source holds the conflict, `resolution: null` (never
     resolved by the skill) · deliberate replacement of known-outdated
     content → supersession: `resolution: "closed_by_new_fact"`.
4. **Report** — inline, before submitting: real file path, plain content
   description, query results, confidence score with band and why,
   contradiction outcome. Then stop and wait in the same run.
5. **Approve** — approval as-reported, a correction (authoritative — submit
   exactly what they return), a clarification request, or a rejection (skip
   this file). Apply never runs without this approval, for this exact file,
   in this same run.
6. **Apply** — submit through the governor's API:
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
     "contradiction": <Step 3 object, or omitted entirely>
   }
   ```
   Leave `content` out entirely — the governor reads the real file itself
   from `source_ref`. A `writer_identity` in the body is never trusted —
   provenance is derived from the authenticating credential.
7. **Verify** — read the real response: `"promoted"` (durable; report the
   real `memory_id`) or `"under_review"` (waiting in the governor's review
   queue — not an error; report plainly, do not resolve or resubmit). An
   outright failure (connection error, abnormal non-2xx) → STOP, report the
   real error, never retry silently or guess.
8. **Log** — append to `/mnt/c/mybizz/logs/mb-submit-memory/`: file path,
   confidence + method, contradiction outcome, real result, real
   `memory_id`.
9. **Learnings** — record anything durable to the same location.

**Folder given instead of a file:** repeat steps 3–9 once per real file
(excluding `obsolete`, `archive`, anything with `backup` in the name,
dotfolders), each with its own independent judgment. End with a summary:
submitted, promoted, under review, rejected at Step 5.

## Completion status protocol

| Status | Meaning |
|---|---|
| `DONE` | Every file submitted; every outcome reported plainly. |
| `DONE_WITH_REVIEWS_PENDING` | Completed; list every `under_review` file with its `memory_id`. |
| `BLOCKED` | State exactly what stopped it (governor not running, missing source registration, API error, missing credential) and what was tried. |
| `REPORT_REJECTED` | Developer rejected a Step 4 report — state what changes. Other files may proceed independently. |

Never mark a run `DONE` if any Step 7 verification was skipped. Never run
Step 6 without an explicit approval on record from within the same run.

## Do not

- Do not call `gbrain remember` or `gbrain sync` for anything meant to be
  governed — that is the ungoverned path this skill exists to replace.
- Do not submit a folder in one call, or share one judgment across files.
- Do not assign a placeholder or default confidence score, ever.
- Do not proceed past `under_review` on the developer's behalf, and do not
  resubmit with a different confidence to force promotion.
- Do not auto-trigger this skill — invocation is always explicit.
- Do not read, print, or copy `.env` or any credential value.
- Do not treat a zero result from the fact search as proof that no governed fact exists — governed facts sit in `memory-governor-code`, which that search does not read (Step 3).
- Do not conflate `mg-grant`/`mg-revoke` (Cupcake's cross-project grant
  tools) with anything in the memory-governor system.
