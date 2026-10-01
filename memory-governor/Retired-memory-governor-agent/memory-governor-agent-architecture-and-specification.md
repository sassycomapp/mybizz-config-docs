---
title: "memory-governor-agent-architecture-and-specification"
doc-id: "mb-6e1b2b63"
updated: "2026-10-01"
---
# Memory Governor Agent — Architecture & Specification

This is the technical foundation for implementation. Every design choice
below traces back to a decision recorded in the companion scope document.
Where a v1 sketch defect was found and corrected, the correction is stated
explicitly so it is never silently re-introduced.

---

## 1. Data Model

### 1.1 GovernedMemoryCandidate (Pydantic, authoritative)

```python
from pydantic import BaseModel, Field, constr, confloat
from typing import Optional, Literal, List, Union
from datetime import datetime

Visibility = Literal["project_local", "shared_all", "shared_specific"]
Retention = Literal["ephemeral", "session", "project", "long_term", "permanent"]
Authority = Literal["self_observed", "user_asserted", "tool_observed", "policy_derived", "human_reviewed"]
MemoryType = Literal[
    "fact", "preference", "policy", "episode", "trace",
    "task_state", "relationship", "summary", "procedural"
]
SourceType = Literal["user", "agent_trace", "tool_result", "file", "ticket", "document", "human_review", "external"]
RiskLevel = Literal["low", "medium", "high", "critical"]
DecisionPath = Literal["auto_promote", "quarantine", "reject", "needs_review", "supersede"]
Status = Literal["proposed", "promoted", "quarantined", "rejected", "superseded", "expired", "under_review"]
Resolution = Literal["none", "closed_by_new_fact", "manual_review", "merged", "deprecated"]
Method = Literal["rule_based", "model_based", "human_verified", "hybrid"]
Action = Literal["promote", "quarantine", "reject", "supersede", "expire", "reconcile"]
ValidUntilReason = Literal["superseded", "ttl_expired", "manual"]


class Scope(BaseModel):
    visibility: Visibility
    retention: Retention
    authority: Optional[Authority] = None
    owning_project: constr(max_length=64)          # aligned with GBrain source_id
    shared_with: List[constr(max_length=64)] = []   # [] | ["all"] | [project_id, ...]


class Subject(BaseModel):
    entity: str = Field(max_length=256)
    predicate: str = Field(max_length=256)
    object: Optional[Union[str, int, float, bool]] = None


class Content(BaseModel):
    text: str
    structured: Optional[Union[dict, list]] = None


class Provenance(BaseModel):
    source_type: SourceType
    source_ref: constr(max_length=1024)     # may be a filesystem path
    writer_identity: constr(max_length=128) # SERVER-DERIVED from auth credential; never accepted from payload
    derived_from: Optional[List[constr(max_length=128)]] = None
    policy_version: constr(max_length=64)
    lineage_hash: Optional[constr(max_length=128)] = None


class Timestamps(BaseModel):
    created_at: datetime
    updated_at: datetime
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    valid_until_reason: Optional[ValidUntilReason] = None


class Confidence(BaseModel):
    score: confloat(ge=0, le=1)
    method: Method


class Policy(BaseModel):
    risk_level: RiskLevel
    decision_path: DecisionPath
    requires_human_review: Optional[bool] = None
    allowed_actions: Optional[List[Action]] = None
    classification: Optional[str] = None       # e.g. "low_confidence", "unresolved_contradiction" -- machine-readable reason tag for a review item
    recommended_action: Optional[Action] = None  # a SUGGESTION shown on the review item, never a decision the system has made


class Contradiction(BaseModel):
    detected: bool = False
    conflicts_with: Optional[List[constr(max_length=128)]] = None
    resolution: Optional[Resolution] = None
    cross_project: bool = False   # True forces needs_review, no exceptions


class ReviewPresentation(BaseModel):
    """Populated whenever decision_path == needs_review. Rendered as the
    end-of-task Q&A sheet in OpenCode (see §6)."""
    recommendation: str
    validation: str
    ramifications: str


class Audit(BaseModel):
    decision_by: Optional[constr(max_length=128)] = None
    decision_at: Optional[datetime] = None
    decision_reason: Optional[str] = None
    reviewer: Optional[constr(max_length=128)] = None


class GovernedMemoryCandidate(BaseModel):
    memory_id: constr(max_length=128)
    owning_project: constr(max_length=64)
    agent_id: Optional[constr(max_length=64)] = None
    session_id: Optional[constr(max_length=128)] = None
    scope: Scope
    memory_type: MemoryType
    subject: Optional[Subject] = None
    content: Content
    provenance: Provenance
    timestamps: Timestamps
    confidence: Confidence
    policy: Policy
    status: Status
    supersedes_id: Optional[constr(max_length=128)] = None
    contradiction: Optional[Contradiction] = None
    review: Optional[ReviewPresentation] = None
    audit: Optional[Audit] = None


class MemoryDecision(BaseModel):
    memory_id: str
    previous_status: Status
    new_status: Status
    reason: Optional[str] = None
    reviewer: Optional[str] = None
```

**Corrections from v1, applied here:**
- `tenant_id`/`user_id`/multi-tenant visibility tiers removed (Scope Doc §5).
- `owning_project`/`shared_with` replace tenant-based scoping (Scope Doc §6).
- `procedural` added to `MemoryType` (Scope Doc §9).
- `valid_until_reason` added — disambiguates supersession from TTL expiry
  (Scope Doc §10).
- `provenance.writer_identity` is documented here as server-derived, not
  payload-supplied — enforced at the API layer, not just by convention
  (§3.2 below).
- `Contradiction.cross_project` added — forces `needs_review` unconditionally
  (Scope Doc §12).
- `ReviewPresentation` added — the recommendation/validation/ramifications
  block required for every hard-stop review (Scope Doc §3, principle 2).

### 1.2 Postgres schema (authoritative store)

```sql
CREATE TABLE projects (
    project_id      TEXT PRIMARY KEY,       -- aligned with GBrain source_id
    display_name    TEXT NOT NULL,
    dormant         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE memory_candidates (
    memory_id           TEXT PRIMARY KEY,
    owning_project       TEXT NOT NULL REFERENCES projects(project_id),
    agent_id            TEXT,
    session_id          TEXT,
    scope                JSONB NOT NULL,
    memory_type          TEXT NOT NULL,
    subject              JSONB,
    content              JSONB NOT NULL,
    provenance            JSONB NOT NULL,
    created_at           TIMESTAMPTZ NOT NULL,
    updated_at           TIMESTAMPTZ NOT NULL,
    valid_from           TIMESTAMPTZ,
    valid_until          TIMESTAMPTZ,
    valid_until_reason   TEXT,
    confidence           JSONB NOT NULL,
    policy               JSONB NOT NULL,
    status               TEXT NOT NULL,
    supersedes_id        TEXT REFERENCES memory_candidates(memory_id),
    contradiction         JSONB,
    review                JSONB,
    audit                 JSONB
);
CREATE INDEX idx_mc_project ON memory_candidates(owning_project);
CREATE INDEX idx_mc_status  ON memory_candidates(status);

CREATE TABLE policy_versions (
    policy_version   TEXT PRIMARY KEY,
    thresholds        JSONB NOT NULL,     -- auto_promote_threshold, review_threshold, etc.
    active            BOOLEAN NOT NULL DEFAULT FALSE,
    effective_from    TIMESTAMPTZ NOT NULL DEFAULT now(),
    approved_by       TEXT NOT NULL       -- human reviewer identity, always required
);

-- Transactional outbox — doubles as the immutable event log (§4) and the
-- retry ledger for asynchronous downstream writes (register mirror, GBrain
-- write, self-healing pass).
CREATE TABLE memory_events (
    event_id       BIGSERIAL PRIMARY KEY,
    event_type     TEXT NOT NULL,   -- candidate_created | contradiction_detected |
                                      -- review_requested | expiry_due |
                                      -- scheduled_consolidation | register_write |
                                      -- gbrain_write
    memory_id      TEXT REFERENCES memory_candidates(memory_id),
    payload        JSONB NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at   TIMESTAMPTZ,
    processed_by   TEXT,
    attempt_count  INT NOT NULL DEFAULT 0,
    last_error     TEXT
);
CREATE INDEX idx_events_unprocessed ON memory_events(created_at) WHERE processed_at IS NULL;
```

Deliberately **one database, no external broker.** `memory_events` is both
the durable event log and the queue — see §4. `attempt_count`/`last_error`
support the retry-with-backoff behavior in §8.

---

## 2. State Machine

```python
ALLOWED_TRANSITIONS = {
    "proposed":     {"under_review", "promoted", "quarantined", "rejected", "superseded"},
    "under_review": {"promoted", "quarantined", "rejected", "superseded"},
    "promoted":     {"superseded", "expired"},
    "quarantined":  {"promoted", "rejected", "expired"},
    "rejected":     set(),
    "superseded":   {"expired"},
    "expired":      set(),
}
```

**Hard requirement, corrected from v1:** every write path — including the
**initial submission**, not only `/review` — must go through this state
machine's transition validation. The v1 sketch's `submit_candidate()` wrote
directly to storage, bypassing `ALLOWED_TRANSITIONS` entirely on first
write and on any resubmission with a reused ID; this allowed a `promoted`
record to be silently overwritten. In this specification, `apply_decision()`
is the **only** function permitted to change `status`, called on every
path without exception, including creation (treated as a transition from a
virtual "none" state into `proposed`).

**Hard requirement, corrected from v1:** contradiction checking is not
conditional on `memory_type`. It runs for every candidate, every time.

```python
def decide_path(candidate: GovernedMemoryCandidate) -> Policy:
    """
    TWO-OUTCOME MODEL (Scope Doc §3, Principle 2, revised). This function's
    own automatic output is now limited to exactly two decision_path
    values: "auto_promote" or "needs_review". It never returns "reject" or
    "quarantine" as its own decision -- those remain legal DecisionPath
    values elsewhere (e.g. a developer's own resolution of a review item),
    but the engine itself no longer closes a candidate out unilaterally.
    Where the prior design auto-quarantined or auto-rejected, this version
    returns needs_review, carrying a `classification` tag and a
    `recommended_action` -- a suggestion attached to an open item, not a
    decision already made.
    """
    risk = compute_risk_level(candidate)

    if not check_provenance(candidate):          # server-verified writer identity
        return Policy(risk_level=risk, decision_path="needs_review", requires_human_review=True,
                       classification="provenance_failure", recommended_action="reject",
                       allowed_actions=["promote", "quarantine", "reject"])

    if not check_scope(candidate):
        return Policy(risk_level=risk, decision_path="needs_review", requires_human_review=True,
                       classification="scope_invalid", recommended_action="quarantine",
                       allowed_actions=["promote", "quarantine", "reject"])

    contradiction = candidate.contradiction
    if contradiction and contradiction.detected:
        if contradiction.cross_project or not contradiction.resolution or contradiction.resolution == "manual_review":
            return Policy(risk_level=risk, decision_path="needs_review", requires_human_review=True,
                           classification="unresolved_contradiction", recommended_action=None,
                           allowed_actions=["promote", "quarantine", "reject"])
        # a genuinely RESOLVED contradiction (e.g. resolution == "closed_by_new_fact",
        # a deliberate supersession -- Scope Doc §12) does NOT block here.
        # applies regardless of memory_type — no high_risk_types gate here (v1 defect, fixed)

    if risk == "high":
        return Policy(risk_level=risk, decision_path="needs_review", requires_human_review=True,
                       classification="high_risk_type", recommended_action=None,
                       allowed_actions=["promote", "quarantine", "reject"])

    if candidate.confidence.score < REVIEW_THRESHOLD:      # from active policy_versions row
        return Policy(risk_level=risk, decision_path="needs_review", requires_human_review=True,
                       classification="low_confidence", recommended_action=None,
                       allowed_actions=["promote", "quarantine", "reject"])

    if risk == "medium" and candidate.confidence.score < AUTO_PROMOTE_THRESHOLD:
        return Policy(risk_level=risk, decision_path="needs_review", requires_human_review=True,
                       classification="medium_risk_moderate_confidence", recommended_action=None,
                       allowed_actions=["promote", "quarantine", "reject"])

    return Policy(risk_level=risk, decision_path="auto_promote", requires_human_review=False, allowed_actions=["promote"])
```

`REVIEW_THRESHOLD`/`AUTO_PROMOTE_THRESHOLD` are read from the currently
`active` row in `policy_versions` (§1.2), never hardcoded — this is what
makes policy changes (§7) a data change, not a code change.

**This is a genuine behavior change from the version already built in
Phases 1–6.** The real, already-implemented `decide_path()` in the actual
repository still returns `"quarantine"` and `"reject"` as automatic
decisions — it was built correctly against the design as it stood at the
time. Bringing the real code in line with this revision is real,
outstanding rework, not yet done, and is called out explicitly in the
Implementation Workflow rather than left to be discovered by surprise when
the build resumes.

**High-risk types**, unchanged in substance from v1: `policy`, `credential`,
`identity`, [[[mb-3-cs-project-library:docs-local/architecture|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md), [[[makepdlf-project-library:docs-local/pdlf-testing-seed-material/ci-based-checks-format/checks/security|Security Check]]](C:/dev/dev-makepdlf/makepdlf-project-library/docs-local/pdlf-testing-seed-material/ci-based-checks-format/checks/security.md). Scope changes that add or remove a
`shared_with` project are also treated as high risk automatically —
cross-project visibility changes are a blast-radius action.

---

## 3. API Surface

### 3.1 Contract format

**OpenAPI 3.1, generated live from the FastAPI implementation** — not a
hand-maintained YAML file. This resolves a concrete v1 defect: the sketch's
static `openapi.yaml` described `POST /memory/review/{memory_id}` while the
actual code implemented `POST /memory/{memory_id}/review` — a real,
undetected spec/implementation divergence. Generating the spec from the
running application at `/openapi.json` makes that class of drift
structurally impossible. A static export may still be committed to
`docs/openapi-export.json` periodically for external reference, but it is
never the source of truth.

### 3.2 Endpoints

| Method & Path | Purpose |
|---|---|
| `POST /memory/candidate` | Submit a candidate. Accepts either inline `content.text` or a `provenance.source_ref` filesystem path (or list of paths) — see §5. `writer_identity` is derived from the authenticating credential, **rejected if present and mismatched in the payload**. |
| `GET /memory/{memory_id}` | Fetch a candidate, scoped by caller's project access. |
| `GET /memory` | List candidates, filterable by `owning_project`, `status`, `memory_type`. |
| `GET /memory/review-queue` | All candidates currently `under_review`, rendered with their `ReviewPresentation` block — the source for the OpenCode Q&A sheet (§6). |
| `POST /memory/{memory_id}/review` | Record a human decision: `promote` / `quarantine` / `reject`, with `reason` and `reviewer`. Only path that may resolve a `needs_review` candidate. |
| `POST /memory/{memory_id}/supersede` | Supersede with a new record. **Must atomically set `valid_until`/`valid_until_reason=superseded` on the old record** — a v1 defect (the field existed but was never actually set by this operation) is fixed here explicitly. |
| `GET /memory/{memory_id}/provenance` | Full audit/decision history for a candidate. |
| `POST /memory/quarantine` | Manual quarantine of an existing candidate. |
| `POST /memory/projects` | Register The use of registers has been discontinued. Please review a new PDLF project (`project_id`, `display_name`) — the onboarding mechanism (Scope Doc §7). |
| `PATCH /memory/projects/{project_id}` | Toggle `dormant` true/false (Scope Doc §8). |
| `POST /memory/policy` | Propose a new policy version. **Always routes through the standard candidate pipeline as a `policy`-type, `high_risk_types` candidate** — never applies directly (§7). |

### 3.3 Authentication

Per-writer API credential, one per known writer (GBrain dreaming process,
manual-developer-submission client, any future generator). The API layer
resolves `writer_identity` from the credential itself; any `writer_identity`
value present in the request body is ignored or rejected, never trusted.

---

## 4. Concurrency & Event Model

**No external message broker.** Given single-operator, single-machine
deployment, a separate Kafka/Redis/RabbitMQ instance is unjustified
infrastructure — it would violate the "simple" credo for no corresponding
benefit at this scale.

**Chosen pattern: transactional outbox + `LISTEN`/`NOTIFY`, one dedicated
worker process.**

1. Any state change that should trigger downstream processing (a new
   candidate, a detected contradiction, an expiry becoming due, a scheduled
   consolidation window, a promotion needing a register The use of registers has been discontinued. Please review write or a GBrain
   write) inserts a row into `memory_events` in the same transaction as the
   state change itself — this is what makes it a true outbox, not a
   best-effort side-channel.
2. The same transaction issues `NOTIFY memory_governor_events`.
3. A single lightweight worker process holds a persistent `LISTEN
   memory_governor_events` connection and wakes immediately on notify.
4. The worker also polls `memory_events WHERE processed_at IS NULL` on a
   fixed interval (e.g. every 60s) as a safety net — covers the case where a
   notify is missed (e.g. worker was mid-restart).
5. This single mechanism satisfies both the "immutable event log" and the
   "queue" pieces of the original concept — one piece of infrastructure,
   not two. It is also what resolves the Postgres/git dual-write problem in
   §8: the register The use of registers has been discontinued. Please review write is just another queued, retryable consumer of
   this same event stream, never a synchronous call inside a request.

**Triggers the worker acts on** (unchanged in substance from the original
concept, now concretely wired):
- `candidate_created` — run `decide_path`.
- `contradiction_detected` — re-evaluate against current unresolved
  contradictions.
- `review_requested` — populate/refresh the review queue.
- `expiry_due` — only fires for opt-in TTL types (`trace`/`episode`); moves
  the record to quarantine, never deletes.
- `scheduled_consolidation_window` — periodic self-observation pass (§7).
- `register_write` — write the register The use of registers has been discontinued. Please review row + JSON payload for a promoted
  candidate (§8).
- `gbrain_write` — write a promoted candidate into GBrain via
  `MEMORY_VERBS` (Scope Doc §16).

All API request handlers stay synchronous and fast (write + outbox insert
+ notify, then return). All actual policy evaluation and downstream effects
happen in the worker, off the request path — this is what makes the service
"perpetual" without being blocking, matching the original concept's intent
without the sketch's gap (where everything ran inline in the HTTP handler).

---

## 5. Manual Submission (Path-Based)

```
POST /memory/candidate
{
  "provenance": {
    "source_type": "user",
    "source_ref": "/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library/adr-local/some-adr.md"
  },
  "owning_project": "mb-3-cs-code",
  "memory_type": "fact"
  ... (writer_identity is NOT supplied — derived from credential)
}
```

On receipt, if `content.text` is absent and `provenance.source_ref` resolves
to a readable path, the governor reads the file (or, for a folder, each file
within it, producing one candidate per file) and populates `content.text`
from it before proceeding through the normal pipeline. No separate ingestion
endpoint — this is the same `/memory/candidate` path, distinguished only by
what's present in the payload.

---

## 5A. Confidence/Contradiction Responsibility, and GBrain Write Mechanics
(Resolved)

**Confidence and contradiction values are never computed inside this
service.** Scope Doc §11A places that responsibility on the submitting
agent — `mb-submit-memory` for manual submission, PDLF's own
step-completion writer (§13A, companion Scope Doc), and GBrain dreaming's
own reasoning for that path. No code in this specification computes either
value; `decide_path()` (§2) only ever consumes them. This section records
the two mechanism decisions that follow from that.

**Mechanism: `remember` (MEMORY_VERBS), uniformly, for every writer.**
Considered and rejected: routing a promoted candidate through GBrain's
ordinary sync/dream ingestion path instead. Rejected because sync ingests
any raw file already sitting in a registered source's folder regardless of
whether the governor ever approved it — since both `mb-submit-memory`'s
and PDLF's own workflows save content inside folders already part of a
registered GBrain source, that raw content would reach GBrain via ordinary
sync whether or not this service exists at all. Routing the governor's
*output* through the same path would not add governance, it would just
duplicate content already arriving ungoverned, and could silently
overwrite a candidate the governor had specifically routed to review.
`remember` writes a distinct, provenance-carrying memory entry — including
`memory_id`, `policy_version`, `decision_path`, `confidence`, and who or
what approved it — which is what actually earns the write the label
"governed." The one deliberate exception is `anvil-agent-references`
(Scope Doc §5), which bypasses the governor entirely and continues to use
ordinary sync, by design.

**Timing: asynchronous, via the `gbrain_write` event already defined in
§4 — no new mechanism.** A synchronous call inside the promotion request
was considered and rejected on the same grounds `register_write` already
settled: it would couple the API response to a second system's
availability and violate the non-blocking design stated in §4. In
practice this is not a meaningful delay — the `NOTIFY`-driven worker wake
was proven at roughly 0.15 seconds during Phase 4 verification, not a
batched or scheduled delay.

No schema or endpoint change follows from either decision — Phase 12
(Workflow) was already specified this way; this section records the
reasoning that confirms it rather than changing it.

---

## 6. Review Presentation — OpenCode Q&A Sheet

Every `needs_review` candidate is rendered by OpenCode using the exact
convention already used throughout this project's work-package reports
(the "Next steps"/"Housekeeping" section format):

```
## Memory Review Required
- Candidate: <memory_id>, type: <memory_type>, project: <owning_project>, risk: <risk_level>
- Anomaly / classification: <Policy.classification>
- Recommendation: <ReviewPresentation.recommendation> (suggested action: <Policy.recommended_action, if any>)
- Validation: <ReviewPresentation.validation>
- Ramifications: <ReviewPresentation.ramifications>
- Decision needed: promote / quarantine / reject
```

The `classification` and suggested `recommended_action` fields, added in
this revision, mirror the same anomaly / recommendation / justification
shape `docs-manager` already uses when presenting findings to the
developer — a deliberately familiar format, not a new one. Sourced from
`GET /memory/review-queue` (§3.2). No new UI pattern — reuses a convention
already in daily use. Regardless of what `recommended_action` suggests,
the actual disposition — promote, quarantine, or reject — is always the
developer's own decision, recorded via `POST /memory/{memory_id}/review`;
the system's suggestion is never applied automatically.

---

## 7. Self-Healing / Iterative Learning Mechanism

1. On each `scheduled_consolidation_window` event, the worker runs a
   read-only pass over recent decision history (e.g. "candidates of type X
   from project Y quarantined at rate Z over the last N days").
2. If a pattern crosses a (separately, conservatively set) noteworthiness
   threshold, the worker submits a `procedural`-type candidate describing
   the observation and a suggested policy adjustment — through
   `POST /memory/candidate`, the same endpoint any other writer uses.
3. Because `policy` and [[[mb-3-cs-project-library:docs-local/architecture|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md)-adjacent candidates are
   `high_risk_types`, this candidate is guaranteed `needs_review` — it
   cannot skip review by virtue of being self-generated.
4. Only on explicit developer approval via `POST /memory/{memory_id}/review`
   does a corresponding new row get written to `policy_versions`
   (§1.2), with the previous version's `active` flag cleared and the change
   mirrored into `register-memory-governor-policy.md` The use of registers has been discontinued. Please review (§8).

The governor is permitted to notice things about itself. It is never
permitted to act on that noticing without the same human gate every other
high-risk candidate goes through.

---

## 8. Backup / Disaster Recovery — Register The use of registers has been discontinued. Please review + Payload Mirroring (Resolved)

Three design questions were open in the prior revision of this document.
All three are resolved here.

### 8.1 Where the register The use of registers has been discontinued. Please review lives

**Inside the memory-governor application's own git repository**, at
`registers/` The use of registers has been discontinued. Please review, not a separately managed external location. This follows the
existing pattern in this environment exactly: a register The use of registers has been discontinued. Please review lives inside the
repo of the thing it describes (`register-global` The use of registers has been discontinued. Please review inside
`project-library-global`, `register-local` The use of registers has been discontinued. Please review inside each project-library).
The memory-governor already has its own repository as a normal consequence
of being a real codebase (§9); putting the register The use of registers has been discontinued. Please review there costs nothing
additional and avoids a second remote, a second credential, and
cross-repo coordination. It also means code changes and governed-memory
changes share one commit history.

### 8.2 The register The use of registers has been discontinued. Please review alone is not sufficient for recovery — fixed

The register The use of registers has been discontinued. Please review's nine columns (`doc-id`/`filename`/`folder`/`type`/`state`/
`date-registered`/`date-state-changed`/`superseded-by`/`notes`) were
designed for tracking documents that live elsewhere on disk. A
`GovernedMemoryCandidate` is not a file living elsewhere — it *is* the
content, and critically `content.text` has no column to occupy in that
schema. Recovery from the register The use of registers has been discontinued. Please review alone would tell you a memory existed
and what happened to it, but not what it said.

**Fix:** keep the register The use of registers has been discontinued. Please review exactly as-is — it remains genuinely useful as a
human-readable index — and add a full JSON payload alongside it:

```
registers/
├── register-memory-governor.md         # index: one row per candidate
├── register-memory-governor-policy.md  # index: one row per policy version
└── candidates/
    └── <memory_id>.json                # full GovernedMemoryCandidate, every field
```

Both the register The use of registers has been discontinued. Please review row and the corresponding JSON payload are written and
committed together, in the same commit. Together they fully reconstruct a
lost Postgres record; the register The use of registers has been discontinued. Please review alone does not.

### 8.3 Postgres and git cannot commit atomically — resolved via the outbox

Rather than write the register/payload The use of registers has been discontinued. Please review synchronously inside the promotion
request (coupling Postgres availability to git remote availability, and
making the request path slower and less robust), the write is a queued,
retryable consumer of the `register_write` event already defined in §4 —
the same transactional-outbox mechanism used for every other downstream
effect in this system, not a new mechanism invented for this case.

- On a `promoted` transition, `apply_decision()` inserts a `register_write`
  event in the same transaction as the status change.
- The worker processes it: writes the register The use of registers has been discontinued. Please review row + JSON payload, commits,
  pushes.
- On failure (disk full, remote unreachable, etc.), `attempt_count`
  increments and `last_error` is recorded (§1.2); the worker retries with
  exponential backoff.
- After 5 consecutive failures, the worker stops retrying automatically and
  instead surfaces the failure the same way any other developer-facing item
  surfaces in this project — as a line in the next task report — rather
  than retrying silently forever or blocking the promotion itself.

This keeps Postgres and the register The use of registers has been discontinued. Please review mirror eventually consistent without
making one system's availability depend on the other's, and without adding
any new infrastructure beyond the outbox table already required for other
reasons.

### 8.4 Policy version register The use of registers has been discontinued. Please review

Unchanged in substance: `register-memory-governor-policy.md` The use of registers has been discontinued. Please review, one row per
policy version, previous version's row set to `Retired` with
`superseded-by` pointing at the new version, written via the same
`register_write` event mechanism.

---

## 9. Repository Layout

```
memory-governor/
├── pyproject.toml
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app; OpenAPI generated live, not hand-written
│   ├── models.py         # §1.1, authoritative Pydantic models
│   ├── policy.py         # §2 decide_path — reads active policy_versions row
│   ├── state_machine.py  # §2 ALLOWED_TRANSITIONS + apply_decision (sole writer of status)
│   ├── storage.py        # Postgres-backed (NOT in-memory dict — v1 defect fixed)
│   ├── provenance.py     # credential -> writer_identity resolution; lineage utilities
│   ├── audit.py          # immutable decision records, consistent field set on every entry
│   ├── outbox.py         # memory_events writes + NOTIFY (§4)
│   ├── worker.py         # LISTEN loop + polling fallback + register/GBrain writers + self-healing pass (§4, §7, §8)
│   ├── registers.py      # register row + JSON payload writer, called by worker.py (§8)
│   ├── projects.py       # project registration + dormant toggle (Scope Doc §7, §8)
│   └── api.py            # §3.2 endpoints
├── registers/             # git-tracked backup store — see §8. Lives in THIS repo.
│   ├── register-memory-governor.md
│   ├── register-memory-governor-policy.md
│   └── candidates/
│       └── <memory_id>.json
├── migrations/           # Postgres schema migrations (§1.2)
├── tests/
│   ├── test_models.py
│   ├── test_policy.py         # explicit test: contradiction check fires for every memory_type
│   ├── test_state_machine.py  # explicit test: no path bypasses ALLOWED_TRANSITIONS
│   ├── test_provenance.py     # explicit test: payload-supplied writer_identity is rejected
│   ├── test_supersede.py      # explicit test: valid_until is set atomically
│   ├── test_registers.py      # explicit test: register + JSON payload together reconstruct a candidate
│   └── test_api.py            # contract test against live /openapi.json (e.g. Schemathesis)
└── docs/
    └── openapi-export.json    # periodic static snapshot, reference only
```

**Build order** (dependency-driven, deterministic-core-first):
1. `models.py`
2. `state_machine.py` (depends only on models)
3. `policy.py` (depends on models + a stub `policy_versions` read)
4. `storage.py` (Postgres wiring)
5. `provenance.py` + `audit.py`
6. `outbox.py` + `worker.py`
7. `registers.py` The use of registers has been discontinued. Please review
8. `api.py` + `main.py`
9. Tests throughout, not deferred to the end — each module above gets its
   corresponding test file before the next module starts.

---

## 10. Explicit Test Requirements (traceable to corrected v1 defects)

These are not optional/nice-to-have — each corresponds directly to a defect
found either in the v1 sketch or in the v2.0 revision of this document, and
must have a regression test from day one:

1. Resubmitting an existing `memory_id` never bypasses `ALLOWED_TRANSITIONS`.
2. A contradiction on a `fact`/`preference` (non-high-risk type) still
   blocks auto-promotion.
3. A `writer_identity` value supplied in the request body is ignored;
   the credential-derived value is what's stored.
4. `POST /memory/{id}/supersede` sets `valid_until` and `valid_until_reason`
   on the old record in the same transaction as the status change.
5. A `trace`/`episode` past its TTL is quarantined, never deleted.
6. A `fact`/`policy`/[[[mb-3-cs-project-library:docs-local/architecture|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md) candidate is never auto-expired by age
   alone, regardless of how long it sits untouched.
7. A cross-project contradiction always produces `needs_review`, regardless
   of confidence score.
8. A self-generated policy-change candidate cannot reach `promoted` without
   a recorded human `reviewer`.
9. A `register_write` event that fails is retried with backoff, and the
   original promotion is unaffected by the failure (the candidate remains
   `promoted` in Postgres regardless of register-write The use of registers has been discontinued. Please review status).
10. Reconstructing a candidate from `registers/candidates/ The use of registers has been discontinued. Please review<memory_id>.json`
    alone (no Postgres) reproduces every field of the original.
