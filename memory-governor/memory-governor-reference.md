---
document: "Memory Governor Reference — Usage, Invocation, and Incident Response"
doc-id: memory-governor-reference
state: Live
date-created: 2026-09-05
---

# Memory Governor Reference — Usage, Invocation, and Incident Response

Companion to `memory-governor-config.md` (the spec — current state — ACTIVE, all
defects resolved 2026-09-08) and `memory-governor-explainer.md` (the
authoritative whole-system narrative — design, mechanics, and real incidents).
Exam companions: `memory-governor-exam-plan.md` (next run's job-spec),
`memory-governor-exam-report.md` (current verified state),
`memory-governor-log.md` (notable events), `memory-governor-learnings.md`
(transient exam knowledge). The architecture standard:
`mb-config-manager/config-manager-explainer.md`. Agent-facing.

---

## Starting and stopping the system (two processes, both required)

Start (from the app folder, `.env` sourced first — no dotenv autoload):

```bash
cd /home/dev-p/memory-governor && set -a && source .env && set +a
setsid .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321 >> /tmp/memory-governor.log 2>&1 < /dev/null &
setsid .venv/bin/python -m app.worker >> /tmp/memory-governor-worker.log 2>&1 < /dev/null &
```

- `setsid` + full redirection is required: a plain `nohup &` child dies
  when the launching shell's process group is terminated (confirmed live).
- **Both processes are required.** The API decides; the worker delivers
  (GBrain writes + register/payload writes). An API without a worker means
  promoted candidates silently never leave the outbox.
- Health checks: `ss -tlnp | grep 8321` (API listening); `ps aux | grep
  app.worker` (worker alive); unauthenticated `curl
  http://127.0.0.1:8321/memory/review-queue` must return HTTP 422
  (credential-required — proves the API is up AND auth-gating).

Stop: `pkill -f "uvicorn app.main:app"` and `pkill -f "app.worker"` —
**run from a command that does not itself contain those patterns in a
matching context, or the shell will kill itself** (confirmed live). Safest:
kill by PID from `ps aux` output.

Permanent auto-start (approved, pending execution): WSL systemd migration
+ two user units (`memory-governor-api`, `memory-governor-worker`) —
sequence in the 2026-09-08 run record.

## Submitting a candidate — the real, correct paths

**Manual submission (the normal, real-world path):**
```
/mb-submit-memory <path>
```
Not a raw API call. Confirms the target is inside a registered GBrain
source, queries GBrain for related content and reads it, then submits with
a genuinely reasoned confidence/contradiction assessment — never a
placeholder.

**Direct API** (used by PDLF's step-completion writer, and available for
any future writer):
```
POST /memory/candidate
```
`writer_identity` is never supplied in the payload — it is derived from the
authenticating credential. A `writer_identity` value present in the body is
ignored or rejected, never trusted.

## The decision chain (source-verified, six review classifications)

Evaluated in order; `auto_promote` only if nothing triggers:

1. `provenance_failure` — writer identity fails server verification
   (recommended action: reject)
2. `scope_invalid` — visibility/`shared_with` inconsistent (recommended
   action: quarantine)
3. `unresolved_contradiction` — cross-project, unresolved, or
   `manual_review` (recommended action: none — never auto-decided)
4. `high_risk_type` — memory type is one of the five spec categories:
   `policy`, `credential`, `identity`, `architecture`, `security`
5. `low_confidence` — confidence below the review threshold (default 0.65)
6. `medium_risk_moderate_confidence` — any sharing, or confidence < 0.5,
   with confidence below the auto-promote threshold (default 0.85)

Thresholds are read live from the active `policy_versions` row — policy
changes are data changes, not code changes. The five high-risk categories
became fully implementable on 2026-09-08 (MemoryType enum extended;
previously only `policy` was representable — the resolved spec
inconsistency).

## Checking and resolving the review queue

```
GET /memory/review-queue
```
Returns every candidate currently `under_review`, each with its
`ReviewPresentation` block (recommendation, validation, ramifications) and
any suggested `classification`/`recommended_action`. Empty list = nothing
blocking; non-empty = a decision is genuinely required before certain other
work may proceed (the PDLF step-continuation rule below).

```
POST /memory/{memory_id}/review
{"decision": "promote" | "quarantine" | "reject", "reason": "...", "reviewer": "..."}
```
The only path that resolves a `needs_review` candidate. The system's own
`recommended_action` is always a suggestion; the disposition is always the
developer's explicit decision.

## The PDLF step-continuation rule

**No PDLF step may begin while any review item is open anywhere in the
system** — not scoped to the immediately-preceding step. `GET
/memory/review-queue` is the real, sufficient primitive: empty means clear,
non-empty means block. Confirmed live across the full before/during/after
sequence for `pdlf_step_sync` submissions.

## Superseding a candidate

```
POST /memory/{memory_id}/supersede
```
Atomically sets `valid_until` and `valid_until_reason: superseded` on the
old record, in the same transaction as creating the new one. Use this,
never manual editing, whenever a fact has been deliberately and correctly
replaced.

## Cross-project sharing — real mechanics

A candidate's `scope.visibility` and `scope.shared_with` must be internally
consistent:

| `visibility` | Required `shared_with` |
|---|---|
| `project_local` | `[]` |
| `shared_all` | exactly `["all"]` |
| `shared_specific` | a real, non-empty, explicit project list (never `["all"]`) |

Read-time visibility is resolved against the requesting project (built
deliberately after the read-time gap was found — see the explainer §5).
The same scope drives the GBrain-write visibility mapping: `shared_all` →
world; everything else → private.

## Worked example — a real cross-project contradiction

A candidate submitted with `contradiction.detected: true` and
`contradiction.cross_project: true` always routes to `needs_review` — no
exception path, regardless of confidence or type. The review presentation
carries `classification: unresolved_contradiction` and no automatic
`recommended_action`: the governor never decides which of two conflicting
cross-project claims is correct.

## Recovering from an accidental GBrain write — real, confirmed procedure

This procedure exists because it has already happened once. Follow it
exactly; do not improvise a shortcut.

**1. Stop immediately.** Do not run anything further until the real,
current state is understood.

**2. Find the real fact using `recall` — not `search`.** `search` operates
over pages/chunks and returns unrelated content by semantic similarity;
`recall` is the paired read-verb to `remember`:
```
gbrain call recall '{"grep": "<unique marker text from the mistaken fact>"}'
```
Confirm exactly one result matches and its provenance unambiguously
identifies it as the mistaken write.

**3. Correct it with `forget`, never a guessed argument.** `forget` takes
the opaque `fact_id` from the recall result — never a page slug, never a
guessed number:
```
gbrain call forget '{"id": "<fact_id>", "reason": "<full, honest explanation>"}'
```
This expires the fact and keeps its full audit trail — it does not delete.

**4. Verify the correction took effect — do not trust the success response
alone:**
```
gbrain call recall '{"grep": "<same marker>", "include_expired": true}'
```
Confirm `expired_at` is a real, non-null timestamp.

**5. Fix the actual root cause before retrying.** The confirmed real cause:
a bash script chained commands without verifying each result. Build test
fixtures so a failed step genuinely halts (`subprocess.run(..., check=True)`),
with a `try`/`finally` that unconditionally restores the original state.

**6. Add a permanent standing test for the specific failure mode.**

## `remember`, `recall`, `forget` — real MEMORY_VERBS mechanics

- **MCP-protocol verbs, not standalone CLI subcommands** — `gbrain recall
  --help` returns a generic usage line; expected, not an error.
- **The correct invocation is `gbrain call <verb> '<json>'`** — confirmed
  live (2026-09-08, protocol v1 JSON).
- **Real parameter schema via `--tools-json`**, saved to a file first:
  ```
  gbrain --tools-json > /tmp/gbrain-tools.json
  ```
  Read-only; safe at any time. `remember` accepts: `fact`, `provenance`
  (required), `ttl`, `entity`, `kind`, `visibility` (`world`|`private`).

## Isolation boundary — stated honestly (2026-09-08)

GBrain's facts layer is brain-global: an unscoped grep finds any fact from
any context, and no GBrain mechanism scopes recall to the active source.
Project isolation for governed memories is therefore enforced by (a) the
governor's own API (read-time visibility resolution against the requesting
project) and (b) the write-path stamping added 2026-09-08 (entity =
owning_project; visibility mapped from declared scope). The former
recall-level cross-project assertion tested a property GBrain does not
provide; the corrected test asserts the guarantees that genuinely hold.
This boundary is a property of GBrain's facts layer — reported, not
silently worked around.

## Do not

- Do not assume `gbrain sync` moves governed content into GBrain — only
  `remember` does; `sync` ingests raw content regardless of governor
  approval.
- Do not chain shell commands without verifying each result — the
  confirmed real cost is an accidental write into live memory.
- Do not guess at a `forget`/`recall` argument — confirm the schema via
  `--tools-json`, confirm the real `fact_id` via `recall` first.
- Do not treat GBrain dreaming's output as something that will ever appear
  in the review queue — it cannot, by design.
- Do not assume test fixtures are shared across test files.
- Do not run only the API without the worker — promoted candidates then
  silently never leave the outbox.
- Do not kill the processes with a `pkill -f` pattern that appears in your
  own command line — the shell kills itself (confirmed live).
