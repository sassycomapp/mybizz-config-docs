# Memory Governor Reference — Usage, Invocation, and Incident Response

Companion to `memory-governor-config.md` (current installed state — including a
verified 2026-09-05 record of the real local clone path, live database check,
and GBrain-source recommendation, under "Local installation & infrastructure")
and `memory-governor-explainer.md` (mechanics, design, and real incidents). Agent-facing.

---

## Submitting a candidate — the real, correct paths

**Manual submission (the normal, real-world path):**
```
/mb-submit-memory <path>
```
Not a raw API call. Confirms the target is a real file or folder already inside a registered GBrain source, queries GBrain for related content and reads it, then submits with a genuinely reasoned confidence/contradiction assessment — never a placeholder.

**Direct API** (used by PDLF's step-completion writer, and available for any future writer):
```
POST /memory/candidate
```
`writer_identity` is never supplied in the payload — it's derived from the authenticating credential. A `writer_identity` value present in the request body is ignored or rejected, never trusted.

## Checking and resolving the review queue

```
GET /memory/review-queue
```
Returns every candidate currently `under_review`, each with its `ReviewPresentation` block (recommendation, validation, ramifications) and any suggested `classification`/`recommended_action`. An empty list means nothing is blocking; any non-empty list means a decision is genuinely required before certain other work may proceed (see the PDLF step-continuation rule below).

```
POST /memory/{memory_id}/review
{"decision": "promote" | "quarantine" | "reject", "reason": "...", "reviewer": "..."}
```
The only path that resolves a `needs_review` candidate. The system's own `recommended_action` is always a suggestion; the actual disposition is always the developer's explicit decision.

## The PDLF step-continuation rule

**No PDLF step may begin while any review item is open anywhere in the system** — not scoped to the immediately-preceding step. `GET /memory/review-queue` is the real, sufficient primitive for this check: empty means clear to proceed, non-empty means block. No separate "yes/no" endpoint exists or is needed — confirmed live, proven correct specifically for `pdlf_step_sync` submissions across the full before/during/after sequence.

## Superseding a candidate

```
POST /memory/{memory_id}/supersede
```
Atomically sets `valid_until` and `valid_until_reason: superseded` on the old record, in the same transaction as creating the new one. Use this, not manual editing, whenever a fact has been deliberately and correctly replaced — this is the mechanism that keeps a genuine update from being mistaken for a contradiction.

## Cross-project sharing — real mechanics

A candidate's `scope.visibility` and `scope.shared_with` must be internally consistent:

| `visibility` | Required `shared_with` |
|---|---|
| `project_local` | `[]` |
| `shared_all` | exactly `["all"]` |
| `shared_specific` | a real, non-empty, explicit project list (never `["all"]`) |

Read-time visibility is resolved against the requesting project — a request must identify which project is asking for a `shared_specific` candidate to correctly appear. This is genuinely built and tested; it did not exist for a real stretch of this project's build and had to be added deliberately (see the explainer, Section 5).

## Worked example — a real cross-project contradiction

A candidate is submitted with `contradiction.detected: true` and `contradiction.cross_project: true`. Regardless of confidence score, regardless of memory type, this always routes to `needs_review` — there is no exception path. The review presentation will carry a `classification` of `unresolved_contradiction` and no automatic `recommended_action`, since the governor never decides on its own which of two conflicting cross-project claims is correct.

## Recovering from an accidental GBrain write — real, confirmed procedure

This procedure exists because it has already happened once, and is recorded here because it will happen again. Follow it exactly; do not improvise a shortcut.

**1. Stop immediately.** Do not run anything further until the real, current state is understood. Do not attempt to guess at a fix.

**2. Find the real fact, using `recall` — not `search`.** `search` operates over pages/chunks and can return unrelated content by semantic similarity. `recall` is the actual paired read-verb to `remember` and is the correct tool:
```
gbrain call recall '{"grep": "<unique marker text from the mistaken fact>"}'
```
This is read-only. Confirm exactly one result matches, and that its `source`/`provenance` field unambiguously identifies it as the mistaken write, not something else with similar content.

**3. Correct it with `forget`, never a guessed argument.** `forget` takes an opaque `id` — the `fact_id` field from the `recall` result above, never a page slug, never a human-facing number guessed from a prior command's output:
```
gbrain call forget '{"id": "<fact_id>", "reason": "<full, honest explanation of what happened and why>"}'
```
**This expires the fact and keeps its full audit trail — it does not delete it.** The reason field becomes a permanent part of that record; write a complete, honest explanation, not a brief note.

**4. Verify the correction actually took effect — do not trust the tool's own success response alone.**
```
gbrain call recall '{"grep": "<same marker text>", "include_expired": true}'
```
Confirm `expired_at` is now a real, non-null timestamp.

**5. Find and fix the actual root cause before retrying anything.** The confirmed real cause, the one time this happened: a bash script chained several commands together without `set -e` and without checking each command's real result before letting the next one run — a failed step didn't stop the ones after it. If building a disposable-resource test fixture (a throwaway GBrain source, or similar), build it so a failed setup step genuinely halts execution — in Python, `subprocess.run(..., check=True)`, not an unguarded shell chain — and use a `try`/`finally` block that unconditionally restores the real, original state, regardless of whether the rest of the test succeeds or fails.

**6. Add a permanent, standing test for the specific failure mode**, not just a one-off fix — e.g., a test confirming no leftover disposable resources survive from a prior run, so a future silent cleanup failure is caught immediately rather than discovered by accident.

## `remember`, `recall`, `forget` — real, confirmed MEMORY_VERBS mechanics

- **These are MCP-protocol verbs, not standalone CLI subcommands** with their own flag parser. `gbrain forget --help` and `gbrain recall --help` both return a generic, unhelpful usage line rather than real flag documentation — this is expected, not an error.
- **The correct invocation is `gbrain call <verb> '<json>'`** — confirmed as the real, working "raw tool invocation" path listed in `gbrain --help`.
- **Get the real, complete parameter schema for any verb via `--tools-json`**, saved to a file first rather than piped directly into a parser:
  ```
  gbrain --tools-json > /tmp/gbrain-tools.json
  ```
  This is read-only and safe to run at any time to confirm a verb's real parameters before using it.

## Do not

- Do not assume `gbrain sync` moves governed content into GBrain — only `remember` does; `sync` ingests raw content regardless of governor approval and would silently defeat governance for anything sitting in a synced folder.
- Do not chain shell commands without verifying each one's real result before the next runs — see the incident-response procedure above for the confirmed, real cost of this mistake.
- Do not guess at a `forget` or `recall` argument — always confirm the real parameter schema via `--tools-json` first, and always confirm the real `fact_id` via `recall` before calling `forget`.
- Do not treat GBrain dreaming's output as something that will ever appear in `GET /memory/review-queue` — it cannot, by design; see `memory-governor-config.md`'s Known Scope Limitations.
- Do not assume test fixtures are shared across test files — `api_client` and `real_credential_headers` exist only in `test_api.py`; this exact mistake was made twice in this project's own build.
