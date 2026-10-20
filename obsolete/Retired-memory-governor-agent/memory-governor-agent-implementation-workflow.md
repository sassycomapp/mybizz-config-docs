---
title: "memory-governor-agent-implementation-workflow"
doc-id: "mb-aa9bfa8d"
updated: "2026-10-10"
---
# Memory Governor Agent — Stepwise Implementation Workflow

Ordered by dependency, matching Architecture & Specification §9's build
order, expanded into discrete, independently verifiable steps. Each step
states its objective, prerequisites, actions, deliverable, and exit
criteria. **No step begins until the prior step's exit criteria are met.**
This mirrors the verification discipline already standard in this
environment (backup → detect → report → approve → apply → verify, per
`mb-align-docs`/`mb-wikilinks`) — nothing here is a new process, it's the
same discipline applied to code instead of documents.

---

## Phase 0 — Infrastructure Prerequisites

Nothing in Phase 1 onward can be tested meaningfully without these. This
phase resolves the outstanding dependencies flagged in Scope Doc §16.

**Step 0.1 — Provision dedicated Postgres database and role**
- Action: create the new database (same instance as GBrain's, distinct
  name) and the scoped role `memory_governor_svc`, per Architecture §1.2.
- Exit criteria: role can connect to the new database only; connecting to
  the existing `gbrain` database with this role fails.

**Step 0.2 — Enable GBrain `MEMORY_VERBS`**
- Action: `gbrain config set mcp_surface verbs`, per Scope Doc §16.
- Exit criteria: `remember`/`recall`/`entity`/`synthesize`/`forget` tools
  confirmed reachable via GBrain MCP.

**Step 0.3 — Provision per-writer API credentials**
- Action: issue a credential for at least the GBrain-dreaming writer and
  one for manual developer submission (Architecture §3.3).
- Exit criteria: two distinct credential values exist and are recorded
  somewhere retrievable (not hardcoded into any file that will be
  committed).

**Step 0.4 — Scaffold the repository, including the register store**
- Action: create the directory structure from Architecture §9 in one pass —
  this now includes `registers/` (with an empty `candidates/` subfolder)
  as a normal part of the application repo, not a separately provisioned
  location. Initialize the repo with a remote configured.
- Exit criteria: `pip install -e .` succeeds; empty test suite runs (0
  tests, 0 failures); `git push` to the configured remote succeeds from a
  trivial test commit.

**Phase 0 exit gate:** all four steps verified before any code beyond
scaffolding is written.

---

## Phase 1 — Deterministic Core

No database, no network, no infrastructure dependency. Fully unit-testable
in isolation — this is deliberate, matching the "deterministic-core-first"
principle in Architecture §9.

**Step 1.1 — `models.py`**
- Action: implement the Pydantic models exactly as specified in
  Architecture §1.1.
- Deliverable: `app/models.py`, `tests/test_models.py`.
- Exit criteria: every field/type from §1.1 has at least one construction
  test; invalid values (e.g. confidence score outside 0–1) are rejected.

**Step 1.2 — `state_machine.py`**
- Action: implement `ALLOWED_TRANSITIONS` and `apply_decision()` exactly as
  specified in Architecture §2, including the "none → proposed" virtual
  transition for creation.
- Deliverable: `app/state_machine.py`, `tests/test_state_machine.py`.
- Exit criteria: Architecture §10 test #1 passes — resubmitting an existing
  `memory_id` cannot bypass `ALLOWED_TRANSITIONS` under any code path in
  this module.

**Step 1.3 — `policy.py`**
- Action: implement `decide_path()` per Architecture §2. At this stage,
  `REVIEW_THRESHOLD`/`AUTO_PROMOTE_THRESHOLD` are read from an in-memory
  stub, not real Postgres yet — that wiring happens in Phase 2.
- Deliverable: `app/policy.py`, `tests/test_policy.py`.
- Exit criteria: Architecture §10 test #2 passes — a contradiction on a
  `fact`/`preference` candidate blocks auto-promotion, not gated to
  high-risk types.

**Phase 1 exit gate:** full unit test suite for models, state machine, and
policy passes with zero infrastructure running. This is the point at which
the deterministic-decision-engine principle (Scope Doc §3, principle 1) is
concretely verifiable, independent of everything built afterward.

---

## Phase 2 — Persistence Layer

**Step 2.1 — Apply Postgres schema**
- Action: run the migration for the schema in Architecture §1.2 against
  the Phase 0.1 database, including the `attempt_count`/`last_error`
  columns on `memory_events`.
- Exit criteria: all five tables exist with correct constraints
  (`memory_candidates.owning_project` FK to `projects`, etc.).

**Step 2.2 — `storage.py`**
- Action: implement real Postgres-backed storage functions, replacing any
  in-memory stub. This directly closes the v1 defect noted in Architecture
  §9 (unsynchronized in-memory dicts).
- Deliverable: `app/storage.py`.
- Exit criteria: candidate submitted via `state_machine`/`policy` from
  Phase 1 persists correctly and is retrievable after a process restart.

**Step 2.3 — Re-run Phase 1 tests against real storage**
- Action: re-point `test_state_machine.py`/`test_policy.py` at the real
  database (test schema, not production).
- Exit criteria: identical pass/fail results as Phase 1 — confirms storage
  wiring introduced no behavioral change to the deterministic core.

**Phase 2 exit gate:** a candidate can be created, transitioned, and
retrieved from real Postgres, with Phase 1's test guarantees still holding.

---

## Phase 3 — Provenance & Audit

**Step 3.1 — `provenance.py`**
- Action: implement credential → `writer_identity` resolution
  (Architecture §3.3), lineage utilities.
- Exit criteria: Architecture §10 test #3 passes — a `writer_identity`
  value present in the request payload is provably ignored; only the
  credential-derived value is ever stored.

**Step 3.2 — `audit.py`**
- Action: implement the immutable audit-record writer with one consistent
  field set used by every call site (a v1 defect — inconsistent per-endpoint
  audit fields — is closed here by having exactly one function that writes
  audit entries).
- Exit criteria: every state transition in `state_machine.py` produces
  exactly one audit record, with all fields populated, no call site
  constructing its own ad hoc entry.

**Phase 3 exit gate:** no code path can write a candidate or change its
status without a corresponding, correctly-attributed audit record.

---

## Phase 4 — Event Backbone

**Step 4.1 — `outbox.py`**
- Action: implement `memory_events` inserts + `NOTIFY`, called from inside
  `apply_decision()`'s own transaction (Architecture §4) — the event insert
  and the state change must commit together or not at all.
- Exit criteria: a transition that fails partway (simulated) leaves neither
  a status change nor an orphaned event row.

**Step 4.2 — `worker.py` (skeleton)**
- Action: implement the `LISTEN` loop and the polling fallback, with no-op/
  logging-only event handlers for now.
- Exit criteria: a manually inserted `memory_events` row is picked up and
  logged within one second via `NOTIFY`, and within the polling interval if
  `NOTIFY` is deliberately suppressed (simulating a missed notification).

**Step 4.3 — Retry/backoff mechanism**
- Action: implement the generic retry wrapper the worker uses for any event
  handler — increments `attempt_count`, records `last_error`, applies
  exponential backoff, and stops after 5 consecutive failures, surfacing
  the failure rather than retrying silently forever (Architecture §8.3).
  Built here, generically, so Phase 7 (register writes) and Phase 12
  (GBrain writes) both consume it rather than each implementing their own.
- Exit criteria: a deliberately-failing test handler is retried with
  increasing delay and stops after the 5th failure, with the failure
  recorded and retrievable.

**Phase 4 exit gate:** the event backbone, including its retry behavior, is
proven reliable before any real handler logic is attached to it.

---

## Phase 5 — API Surface

**Step 5.1 — `api.py`**
- Action: implement every endpoint from Architecture §3.2, wired to the
  now-real `state_machine`/`policy`/`storage`.

**Step 5.2 — `main.py`**
- Action: assemble the FastAPI app; confirm `/openapi.json` is generated
  live, matching implemented routes exactly (Architecture §3.1 — this is
  the structural fix for the v1 spec/implementation drift defect).
- Exit criteria: every route in `/openapi.json` corresponds to an actually
  implemented endpoint, and vice versa — checked programmatically, not by
  eye.

**Step 5.3 — Contract testing**
- Action: run a contract-testing tool (e.g. Schemathesis) against the live
  `/openapi.json`.
- Exit criteria: no contract violations on any endpoint.

**Phase 5 exit gate:** the API is reachable, self-describing, and its
description is provably accurate.

---

## Phase 6 — Manual Submission (Path-Based Ingestion)

**Step 6.1 — Path-reading in candidate submission**
- Action: implement the behavior in Architecture §5 — when
  `provenance.source_ref` is a filesystem path and `content.text` is
  absent, read the file(s) and populate content before proceeding.

**Step 6.2 — Test**
- Action: submit a real file path (e.g. an ADR from
  `mb-3-cs-project-library`), confirm correct ingestion.
- Exit criteria: submitted candidate's `content.text` exactly matches the
  source file; a folder path produces one candidate per file within it.

---

## Phase 6.5 — Realign Already-Built Code to the Two-Outcome Model

Real, necessary rework, not part of the original phase sequence. A later
design review revised Architecture §2's `decide_path()` after Phases 1–6
were already built and correctly tested against the original four-outcome
design. This phase brings the real, running code in line with that
revision before Phase 7 builds anything further on top of it — consistent
with this project's own "do it right, do it once" standard.

**Step 6.5.1 — Rewrite `decide_path()`**
- Action: update `app/policy.py`'s `decide_path()` to the two-outcome
  version in Architecture §2 — every non-passing case returns
  `needs_review` carrying a `classification` and, where applicable, a
  `recommended_action`; the function itself never returns `"quarantine"`
  or `"reject"` as its own decision.
- Exit criteria: `test_policy.py` rewritten to match; no test asserts
  `decide_path()` itself returns `"quarantine"` or `"reject"`.

**Step 6.5.2 — Add `classification`/`recommended_action` to `models.py`**
- Action: add the two new `Policy` fields from Architecture §1.1.
- Exit criteria: existing model tests still pass; both new fields covered
  by at least one construction test.

**Step 6.5.3 — Full regression**
- Action: re-run the complete existing test suite from Phases 1–6 against
  the reworked code.
- Exit criteria: full suite passes; any test that asserted the old
  four-outcome behavior has been deliberately updated, not silently
  broken or deleted without explanation.

**Phase 6.5 exit gate:** the real, running code matches Architecture §2's
two-outcome model exactly, with the full existing test suite passing
against the corrected version, before Phase 7 begins.

---

## Phase 7 — Register + Payload Mirroring (Backup / Disaster Recovery)

Rebuilt against the resolved design in Architecture §8. No open questions
remain in this phase — all three prior open items are answered by the
referenced sections.

**Step 7.1 — `registers.py`**
- Action: implement the writer that, given a promoted candidate, produces
  both the register row (`register-memory-governor.md`) and the full JSON
  payload (`registers/candidates/<memory_id>.json`), and commits both
  together in the app repo (Architecture §8.1, §8.2).

**Step 7.2 — Wire as a `register_write` event consumer**
- Action: in `state_machine.py`'s `apply_decision()`, a transition into
  `promoted` inserts a `register_write` event in the same transaction
  (extending `outbox.py` from Phase 4). In `worker.py`, consume this event
  using the Phase 4.3 retry wrapper — never a synchronous call inside the
  promotion request (Architecture §8.3).
- Exit criteria: promoting a candidate returns immediately; the register
  row and JSON payload appear shortly afterward, written by the worker, not
  the request handler.

**Step 7.3 — Failure-path test**
- Action: simulate a register-write failure (e.g. temporarily point the
  repo remote at an unreachable location), confirm retry/backoff behavior
  from Phase 4.3 engages, and confirm the candidate's `promoted` status in
  Postgres is unaffected by the failure.
- Exit criteria: Architecture §10 test #9 passes.

**Step 7.4 — Normal-path test**
- Action: promote a candidate under normal conditions, confirm the register
  row and JSON payload both commit correctly.

**Step 7.5 — Disaster-recovery drill**
- Action: with a small set of test candidates promoted, deliberately drop
  the test Postgres database, reconstruct `memory_candidates` state from
  `registers/candidates/*.json` alone.
- Exit criteria: Architecture §10 test #10 passes — every field of the
  original candidate is recovered, not just what the register's own nine
  columns can represent.

**Phase 7 exit gate:** both the normal-path and failure-path tests pass,
and the disaster-recovery drill fully reconstructs candidate state from the
JSON payload store with no data loss.

---

## Phase 8 — Project Onboarding & Dormant Handling

**Step 8.1 — `projects.py`**
- Action: implement `POST /memory/projects` and the dormant toggle
  (`PATCH /memory/projects/{project_id}`).

**Step 8.2 — Worker exclusion logic**
- Action: `worker.py`'s scheduled-sweep logic excludes any project with
  `dormant = true`.

**Step 8.3 — Onboarding test**
- Action: register a new test project end-to-end, submit a candidate
  scoped to it.
- Exit criteria: candidate correctly scoped; no code change was required to
  support the new project.

**Step 8.4 — Dormancy test**
- Action: mark a project dormant, confirm it's excluded from the next
  scheduled sweep; reactivate, confirm it resumes without data loss or
  migration.

---

## Phase 9 — Cross-Project Sharing & Contradiction

**Step 9.1 — `shared_with` resolution**
- Action: implement scope-check logic honoring `[]` / `["all"]` / explicit
  project lists (Scope Doc §6).

**Step 9.2 — Cross-project contradiction enforcement**
- Action: implement `Contradiction.cross_project` forcing `needs_review`
  unconditionally, per Architecture §2's `decide_path`.
- Exit criteria: Architecture §10 test #7 passes.

---

## Phase 10 — Review Presentation Integration

**Step 10.1 — `GET /memory/review-queue`**
- Action: implement per Architecture §3.2.

**Step 10.2 — OpenCode-side rendering**
- Action: wire the Q&A sheet format from Architecture §6 into the relevant
  OpenCode task-report convention.

**Step 10.3 — End-to-end review test**
- Action: force a `needs_review` candidate (e.g. a `policy`-type
  submission), confirm it blocks correctly, confirm the Q&A sheet renders
  with all three fields populated, confirm `POST /memory/{id}/review`
  correctly resolves it and only then does it become retrievable as
  durable memory.

---

## Phase 11 — Self-Healing Loop

**Step 11.1 — Observation pass**
- Action: implement the read-only pattern-detection logic in `worker.py`'s
  `scheduled_consolidation_window` handler (Architecture §7).

**Step 11.2 — Procedural candidate generation**
- Action: wire detected patterns to `procedural`-type candidate submission
  through the normal `/memory/candidate` path — no special-cased write
  path.

**Step 11.3 — Policy update path**
- Action: implement the approved-change flow: new `policy_versions` row,
  previous row's `active` flag cleared, register mirror updated via the
  same `register_write` event consumer built in Phase 7.

**Step 11.4 — Test**
- Action: Architecture §10 test #8 — confirm a self-generated policy-change
  candidate cannot reach `promoted` without a recorded human `reviewer`.

---

## Phase 12 — GBrain Write Integration

**Step 12.1 — Implement the promotion → GBrain write**
- Action: on a candidate reaching `promoted`, insert a `gbrain_write` event
  (same outbox pattern as `register_write`); the worker consumes it via the
  Phase 4.3 retry wrapper and calls GBrain's `remember` tool (via the
  `MEMORY_VERBS` surface enabled in Step 0.2).

**Step 12.2 — Test**
- Action: promote a candidate, confirm it's retrievable via GBrain's
  `recall`/`gbrain_query` shortly afterward.
- Exit criteria: content, provenance, and `owning_project` scoping are all
  correctly reflected in what GBrain stores.

---

## Phase 13 — PDLF Step-Completion Writer

Per Scope Doc §13A. This closes the more consequential of the two
ungoverned-writer gaps found during design review — PDLF's own
step-completion sync currently writes into GBrain directly, at the end of
every one of PDLF's 46 steps, with nothing checking it first. This is the
busier of the two gaps this project exists to close; GBrain dreaming's own
cutover is Phase 16.

**Step 13.1 — Provision the `pdlf_step_sync` credential**
- Action: issue a distinct writer credential for this path, following the
  same pattern as Step 0.3.
- Exit criteria: credential recorded, distinct from both existing writer
  credentials.

**Step 13.2 — Build the governed step-completion sequence**
- Action: implement the final step of the five-point due diligence
  sequence ([[[pdlf:obsolete/system-description|System Description]]](C:/pdlf/obsolete/system-description.md), "The five-point due diligence
  process") — for each real artifact a finished PDLF step produced, the
  OpenCode agent queries GBrain for related content, reads it, forms a
  genuine confidence/contradiction assessment (Scope Doc §11A), and
  submits via `POST /memory/candidate` using the `pdlf_step_sync`
  credential.
- Exit criteria: a real PDLF step's real artifacts are each submitted and
  independently decided — never batched together as a single candidate.

**Step 13.3 — Step-continuation behavior (Resolved)**
- Decided: no PDLF step may begin while any review item is open anywhere
  in the system, regardless of which step originally produced it — not
  scoped to only the item(s) the immediately-preceding step produced.
  Two reasons settled this, not just a general preference for caution.
  First, PDLF's own execution discipline queries GBrain at the start of
  every step; if the next step began before an earlier step's review item
  was resolved, that query would silently return an incomplete picture of
  what had actually just been decided, with nothing flagging the gap.
  Second, checked directly against this project's own stated policy and
  working method — "never defer what can be done now" and "linear
  progression" — a rule that only blocked on the current step's own items
  while letting older, unresolved ones trail along in the background
  would itself be exactly the kind of deferral the policy forbids, and
  would not actually be linear. The system must never allow a hidden
  backlog of open review items to accumulate behind the work in progress.
- Action: implement this as a hard precondition check at the start of
  every step's execution sequence — before Step 1 of the existing
  thirteen-point sequence runs, confirm zero open review items exist
  anywhere in the governor; if any exist, the step does not begin.
- Exit criteria: a real review item, deliberately left open, is confirmed
  to block the next step from starting; resolving it is confirmed to
  unblock that same step immediately, with no other action required.

**Step 13.4 — Test**
- Action: run one real PDLF step end-to-end through the full sequence,
  confirm every one of its real artifacts reaches the governor
  individually, and confirm at least one deliberately-engineered review
  case surfaces and behaves correctly per Step 13.3's resolved decision.

**Closed for now, 2026-08-25, by deliberate developer decision — not
completed, and not to be treated as equivalent to completion.** Steps
13.1 through 13.3 are complete and proven live. Step 13.4 itself requires
a genuinely real PDLF step to run, end to end, through the actual `/pdlf`
orchestrator — confirmed this cannot happen yet: Step 11 and other steps
still have components outstanding (a Sentinel Security system among
them), and `/pdlf` runs the full pipeline from `C:\pdlf`, not individual
step files run in isolation. A narrower substitute — invoking
`mb-submit-memory` directly, outside a real step's own genuine context —
was considered and explicitly rejected: it would prove the skill works
alone, already established elsewhere, not that a real step genuinely and
correctly triggers this behavior in its natural setting. Confidence to
close this without that proof rests on what has already been tested
live: every governed writer, the GBrain write path (including full
disaster-recovery drills), cross-project isolation, and every credential
and review-queue behavior. Reopen and actually run this test the first
time a real project genuinely goes through a retrofitted step after
PDLF's real go-live — not before.

**Phase 13 exit gate:** a real PDLF step's completion routes every one of
its real artifacts through the governor, with the Step 13.3 precondition
check enforced in the running system, not merely documented. **Not yet
met — intentionally deferred to PDLF's real go-live, per the decision
above, not missing or forgotten.**

---

## Phase 14 — mb-submit-memory (OpenCode-Side Skill)

Per Scope Doc §13. This is OpenCode-side skill work, not memory-governor
application code — no new endpoint, no schema change. Placed here, after
GBrain write integration and the PDLF writer, because its own
query-and-compare step has no genuine target to query against until
governor-approved writes actually reach GBrain.

**Step 14.1 — Build the skill**
- Action: implement `/mb-submit-memory <path>`, following the same
  learnings → backup → detect → report → approve → apply → verify →
  commit/push → log → learnings rhythm already used by `docs-manager`,
  `mb-align-docs`, and `mb-wikilinks` — not a new interaction pattern.
  Concretely: confirm the target path is a real file or folder already
  inside a folder that is part of a registered GBrain source; query GBrain
  for related existing content and read what comes back (Scope Doc §11A —
  this is the step that supplies a genuine, non-placeholder
  `confidence`/`contradiction` assessment, not an optional add-on); call
  `POST /memory/candidate` with the real path and the reasoned values;
  report the real result back in the same plain-language tone as every
  other skill's own report step — auto-accepted, or a review needed via
  the existing Q&A sheet format (Architecture §6).

**Step 14.2 — Live test with real content**
- Action: submit one real, genuinely new markdown document through the
  full pipeline exactly as the developer would use it: save file →
  `/mb-wikilinks` → `/docs-manager` → `/mb-align-docs` →
  `/mb-submit-memory`. Confirm the skill's GBrain query step actually ran
  against real existing content (not skipped), confirm the
  `confidence`/`contradiction` values submitted are traceably derived from
  that query-and-read step rather than a fixed default, and confirm the
  reported outcome matches the candidate's actual, real decision path.

**Phase 14 exit gate:** a real document, submitted through the real
pipeline, produces a genuinely reasoned candidate and a correctly reported
outcome — not a synthetic test fixture with hand-typed values.

---

## Phase 15 — Full Integration & Acceptance

**Step 15.1 — End-to-end scenario test**
- Action: run one complete scenario touching every subsystem: submission →
  provenance check → scope check → contradiction check → both the
  auto-promote path and the needs-review path → GBrain write → register +
  payload mirror → provenance/audit retrieval. Include one pass through
  `mb-submit-memory` (Phase 14) and one real PDLF step through Phase 13's
  sequence as part of this scenario, not just direct API calls, so the
  full real-world path is exercised at least once here.

**Step 15.2 — Second disaster-recovery drill**
- Action: repeat Phase 7's drill, now with the full system (GBrain writes
  included) — confirm GBrain state and the register/payload store can both
  be used to cross-check each other after a simulated Postgres loss.

**Step 15.3 — Success-criteria sign-off**
- Action: check off Scope Doc §19's success criteria one by one, explicitly,
  against the running system — not assumed satisfied by passing unit tests
  alone.

**Phase 15 exit gate:** every item in Scope Doc §19 verified against the
live system before Phase 16 begins.

---

## Phase 16 — Cutover (Revised)

**Revised in full after a real design investigation** confirmed GBrain's
`dream` command has no interception point of any kind — no `--source`-style
redirect, nothing in its MCP tool schema, nothing in `gbrain config show`.
Dreaming writes directly to GBrain's own database through its own internal
engine; there is no configuration hook anywhere to route those writes
through this governor's API the way the other three writers do. This was
checked exhaustively, not assumed — the original Step 16.1/16.2/16.3
wording below described an outcome that is not achievable through
configuration, and forking GBrain's own source to intercept its internal
writes was considered and rejected on the same reasoning already applied
elsewhere in this project: a permanent obligation to re-merge against
GBrain's own ongoing releases, forever, for a problem solvable another way.

The real, working alternative, arrived at through direct investigation of
GBrain's actual behavior: `dream` runs in real, distinct, named phases —
confirmed via `--dry-run --json`, not assumed — and each phase reports its
own real result. GBrain also ships a real, separate, purpose-built tool,
`gbrain eval suspected-contradictions`, confirmed to NOT run automatically
as part of `dream`'s own cycle (its own tool description states plainly it
only reads a cached run row from the last deliberate invocation). Both
facts together produce a genuine, working discipline for this one writer —
not governance through the governor's own API, since that is structurally
impossible here, but a real, deliberate, always-applied review discipline
around a tool designed to be operated exactly this way. Third-party review
of GBrain confirms this matches its own stated design assumption directly:
GBrain is single-operator by design, and "does not fact-check the content
or confirm the knowledge is accurate or complete" — it assumes the operator
reviews it, not that GBrain guarantees correctness on its own.

**Step 16.1 — Establish the direct-operation discipline for GBrain
dreaming**
- Action: since dreaming cannot be routed through the governor's API,
  formally adopt the three-step sequence confirmed live this session as
  the accepted, documented governance mechanism for this one writer:
  1. Run `gbrain dream` for real (not `--dry-run` — a dry run writes
     nothing, confirmed directly, and cannot serve as a review step).
  2. Run `gbrain eval suspected-contradictions` immediately afterward —
     this does not run automatically and must be explicitly invoked
     every time.
  3. Review the findings; act on anything flagged, particularly high
     severity.
  This is the one deliberate, honestly-documented exception to "every
  writer's output is governed through the same API" — not a gap glossed
  over, a real structural limit of governing third-party software with no
  exposed extension point, named plainly as such.

**Step 16.2 — Observation period**
- Action: for an explicitly agreed number of real `dream` cycles, review
  the actual new concepts each cycle produces directly (`gbrain list
  --type concept --updated-after <date>`), not `needs_review` candidates
  in the governor's own queue — nothing from dreaming ever reaches that
  queue, since it never passes through the governor at all. Confirm the
  three-step discipline in Step 16.1 is being applied consistently before
  treating it as routine, unattended practice.

**Step 16.3 — Go-live**
- Action: formal confirmation that the three-step discipline (Step 16.1)
  is genuinely, consistently applied every time `dream` is run — not
  confirmation that dreaming's output "flows through the governor," which
  is not an achievable outcome for this specific writer, honestly stated
  rather than left as an unmet promise in this document.

**Steps 16.2 and 16.3 closed for now, 2026-08-25, by the same deliberate
developer decision as Step 13.4 above — not completed, not equivalent to
completion.** Both genuinely require real, elapsed, repeated `dream`
cycles under ordinary PDLF use to observe, which cannot exist before
PDLF's own real go-live. This is not a gap in the governor's own build —
its behavior has already been proven live and repeatedly throughout this
project. Reopen and actually run this observation once PDLF is in real,
ordinary use, not before.

---

**Memory Governor Agent — build status, 2026-08-25.** Every phase from 0
through 16 is either fully closed, or closed for now by an explicit,
recorded developer decision pending PDLF's own real go-live (Phase 13.4,
Phase 16.2, Phase 16.3) or a live chain test not yet run but not blocked
by anything (Phase 14.2, tracked on the master task list). There is no
remaining application code to write in the memory-governor repository
itself. The next real work is PDLF's own build.
