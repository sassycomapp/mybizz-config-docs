---
title: "memory-governor-agent-scope"
doc-id: "mb-10605846"
updated: "2026-10-09"
---
# Memory Governor Agent — Scope Document

The thirteen v1 sketch files are illustrative indications of the kind of
documents a project like this normally needs. They are not binding. This
document, together with the companion Architecture & Specification draft
and the Implementation Workflow, is the actual scope for this project going
forward.

---

## 1. Problem Statement

Agents that write directly from raw output into durable long-term memory
propagate errors, unverified claims, and contradictions as permanent
"truth." This risk is documented in the literature (DeChant, Columbia,
SaTML 2025, arXiv:2501.11739): episodic memory in AI agents introduces
unwanted retention, unpredictability, and deception risk precisely because
memory formation is typically ungoverned.

Concretely, in this environment: GBrain's dream cycle synthesizes concepts
and candidate facts from raw project material. Nothing currently checks
those candidates for provenance, contradiction, or risk before they become
part of GBrain's durable, queryable memory. A dreaming process that goes
wrong — hallucinates a relationship, misreads a timestamp, draws a false
conclusion from ambiguous source material — currently has no gate between
"generated" and "permanently believed."

## 2. Proposed Solution

A control-plane service — provenance-checked, rule-based, audit-logged —
sitting between memory generation (GBrain dreaming, and any other future
generator, including manual developer submission) and durable storage
(GBrain). No candidate reaches durable, queryable memory without passing
through this governor first.

This is a gatekeeping layer, not a memory store in its own right. It does
not replace GBrain. It decides what GBrain is allowed to durably remember.

## 3. Governing Principles

These are non-negotiable design constraints, established directly by the
developer and carried through every subsequent decision in this document
and its companion specification.

1. **No ungated AI judgment.** The decision engine is fully deterministic
   and rule-based. Any generator (GBrain dreaming, a future LLM-based
   process, etc.) may *propose* candidates. Nothing but the governor's
   explicit, auditable rules may *decide* their fate. This rules out
   RL-trained or LLM-judged promotion decisions as the deciding mechanism,
   even though such approaches exist elsewhere in the field (e.g.
   Memory-R1, arXiv:2508.19828) — a deliberate tradeoff in favor of
   determinism and auditability over adaptive sophistication.
2. **Two automatic outcomes only — hard stop on everything else.**
   Revised from the original four-outcome design after direct developer
   review found that the original design let the system quietly close
   out a "rejected" or "quarantined" candidate on its own, without the
   developer ever being told. The governor's decision engine may now
   only ever assign one of two outcomes automatically: promote a
   candidate straight through, or route it to the developer's review
   list. There is no automatic reject and no automatic quarantine —
   those become dispositions the developer chooses when resolving a
   review item, never something the system decides and closes out by
   itself. Any candidate routed to review is genuinely blocking — it
   cannot reach a durable, retrievable state before an explicit developer
   decision is recorded against it. The candidate must present a
   recommendation, a validation summary, a ramifications statement, and
   may carry a suggested classification (e.g. "reject — credential
   failed authentication") — but the classification is always a
   suggestion attached to an open item, never a bare flag and never a
   decision the system has already made on its own.
3. **Not a copy of any other system.** Comparisons to Letta/MemGPT, Mem0,
   and Zep/Graphiti inform this design but do not govern it. Where this
   design diverges from the field's mainstream (e.g. external governance
   vs. agent self-editing), that divergence is intentional.
4. **Development credo: simple, secure, robust, fit for purpose.** Every
   infrastructure choice in the companion specification is justified
   against this credo explicitly. No component exists because it is
   possible or fashionable; each exists because a stated requirement
   demands it.
5. **Self-healing and iterative, but never autonomous.** The governor may
   learn about its own operation and propose changes to its own policy.
   It may never apply such a change without passing through its own
   governance pipeline like any other candidate.

## 4. Scope Boundary — What This Governs

This memory layer sits inside the developer's unique operating
system/development environment (referred to as "the unique OS"), and
governs memory arising from **PDLF (Project Development Life Cycle
Framework) work only**:

- Architecture decisions and their rationale
- Code patterns and corrections learned during development
- GBrain/Graphify operational learnings
- Project-management state and history
- Any material the developer explicitly submits for retention

## 5. Explicitly Out of Scope

- **The shipped SaaS applications themselves.** Every application built via
  PDLF is an independent Anvil.works application. Once shipped, it does not
  use this memory layer, the unique OS, or PDLF — it is a concluded,
  independent artifact. This governor never touches application runtime
  data.
- **Multi-tenant SaaS concerns.** This is a solo-developer, single-operator
  environment with AI assistance. There are no external tenants, no
  customer data isolation requirements, and no cross-tenant propagation
  concerns. Any schema field implying otherwise (`tenant_id`, `restricted`/
  `tenant_global` visibility tiers) is removed.
- **Graphify as a write target.** Graphify's content is entirely
  deterministic, AST-derived from real source code via Tree-sitter (see
  [[[mybizz-config-docs:graphify/graphify-reference|Graphify Reference]]](C:/mybizz/mybizz-config-docs/graphify/graphify-reference.md)). It is not a destination for arbitrary
  governor-approved facts. All governed, approved memory writes to
  **GBrain**, not Graphify.
- **Retrieval/search.** This governor controls what enters durable memory.
  It does not implement search or retrieval — that remains GBrain's
  existing job, exactly as already documented in [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-explainer.md).
- **`anvil-agent-references` and any other official, direct-from-vendor
  reference material.** Confirmed as a deliberate, permanent exception,
  not an oversight: this is Anvil's own documentation about how their own
  platform works, not a claim proposed by a process that could be wrong.
  There is no genuine confidence or contradiction question to ask about
  it. It is registered as its own GBrain source and kept current through
  GBrain's ordinary syncing, the same way `project-library-global`'s own
  specifications and ADRs already are — never through this governor,
  including for future updates Anvil releases to it. See master task list
  item 9.1 for the concrete action.

## 6. Scoping Unit — Project-Based, Not Tenant-Based

Every PDLF project is an Anvil.works application, developed via PDLF,
drawing on the same global project library. There is real value in sharing
memory across projects (shared architectural conventions, common ADRs),
so scoping is **per-project with explicit sharing**, not fully global and
not fully isolated:

- Every candidate carries an `owning_project` field, aligned with GBrain's
  existing `source_id` convention (`mb-3-cs-code`, `dev-root-hub`, etc.) —
  no new naming scheme invented.
- Every candidate carries a `shared_with` field: `[]` (project-local only,
  the default), `["all"]` (globally visible — for conventions used by every
  PDLF project), or an explicit list of named project IDs.
- This directly mirrors GBrain's own existing `default`-federated-source
  pattern (see [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)), applied one level below the source
  level.

## 7. New-Project Onboarding

Because scoping is data (a project-ID string), not schema or code,
onboarding a new PDLF project requires only registering a new project ID —
no schema migration, no redeploy. This mirrors `gbrain sources add` in
shape and cost. See the companion specification, §7, for the exact
mechanism.

## 8. Dormant-Project Handling

When a PDLF project becomes dormant, its governed memory is neither deleted
nor hidden — it is simply excluded from active processing until the
project is reactivated, exactly mirroring GBrain's existing
registered-but-deferred pattern for `mb4ecom-*`/`mb5pdlf-*` (documented in
`working-ledger.md`). Concretely: no new candidates accepted for that
project without explicit resubmission; excluded from scheduled sweeps;
fully queryable on request at any time; reactivation requires only
flipping a flag.

## 9. Memory Type Taxonomy

`fact`, `preference`, `policy`, `episode`, `trace`, `task_state`,
`relationship`, `summary`, **`procedural`** (added — learned skills,
patterns, and heuristics; absent from the v1 sketch, a documented gap in
CoALA-derived taxonomies generally per arXiv:2604.11364, now closed here).

## 10. Retention Model — Supersession vs. Expiry (Corrected)

Working inactivity on a topic is not staleness. An ADR from months ago that
hasn't been revisited remains exactly as valid as the day it was written,
until something explicitly contradicts or replaces it.

- **No blanket calendar-based TTL expiry.** `fact`, `policy`,
  `architecture`, `procedural`, `preference` memory never expires from age
  alone.
- **Supersession is the primary retirement mechanism.** A newer fact
  explicitly replaces an older one; the old record's `valid_until` is set
  to the moment the new one was accepted (`valid_until_reason:
  superseded`).
- **TTL remains available, opt-in only, for genuinely ephemeral types**
  (`trace`, `episode` — working scratch material), and even then never
  deletes — it moves the record to a quarantine-equivalent state for later
  review, consistent with the project's standing "never delete, only
  retire or quarantine" rule (see `mb-align-docs-README.md`).

## 11. Provenance Model

`provenance.writer_identity` is never self-reported in the request payload.
It is derived server-side from which per-writer API credential
authenticated the request. Each writer (GBrain dreaming, any future
generator, manual developer submission) holds a distinct credential. This
closes a documented real-world failure mode: Mem0's platform has been
observed writing a wrong date into memory by using the LLM's current date
instead of the source document's actual timestamp (mem0ai/mem0 GitHub
issue #3944) — an ungated provenance failure of exactly the kind this rule
prevents.

`provenance.source_ref` may be a filesystem path (or list of paths). When a
path is supplied, the governor reads the file(s) at submission time and
populates `content.text` from them — this is how manual developer
submission works (§13).

## 11A. Origin of Confidence and Contradiction Values (Resolved)

A real gap, left open through the early build phases and closed here: the
governor enforces rules against `confidence.score` and `contradiction`
once they exist on a candidate, but nothing in the governor's own design
ever specified where a genuine value comes from. Every candidate submitted
during early testing had these fields typed in by hand, standing in for a
judgment nobody was actually making.

**The governor itself must never compute these values.** Doing so would
require exactly the kind of AI judgment Principle 1 (§3) rules out of the
deterministic engine. The governor's job stays what it has always been:
enforce policy against whatever is honestly submitted.

**Responsibility is placed on the submitting agent, not on the developer
and not on the governor.** The developer is not positioned to assess a
document's confidence or judge whether it contradicts existing material on
demand — expecting that of him is asking for a technical judgment he has
been clear he cannot reliably make. A hardcoded default is equally wrong,
for the opposite reason: it cannot understand what a real document
actually says.

The only remaining candidate is genuine reasoning over genuine content,
performed by whichever agent is proposing the write — this mirrors PDLF's
own established discipline exactly (query first, then fetch and read the
real content, then form a judgment, then act). Applied here: before
submitting a candidate, the proposing agent must query GBrain for related
existing material, read what comes back, and arrive at a genuine
confidence assessment and contradiction determination — not invent a
plausible-looking number.

This is a **process requirement placed on every writer**, not a governor
capability. GBrain dreaming's own reasoning is the source of these values
when it submits. Manual submission, via `mb-submit-memory` (§13), and
PDLF's own step-completion writer (§13A) must include this same
query-then-read-then-assess step as a mandatory part of their own
procedure — not an optional nicety a future version might add.

No schema or governor-side change follows from this — `confidence` and
`contradiction` were already real fields on every request. What changes is
that these fields are now understood to carry a genuine, load-bearing
meaning, and every writer built for this system must be held to that
standard from its first version, not retrofitted later.

## 12. Contradiction Handling

Applies uniformly across **all** memory types — not gated to a high-risk
subset (a defect identified and corrected from the v1 sketch). A detected,
unresolved contradiction always blocks auto-promotion regardless of
confidence score.

**A contradiction is not, by itself, a judgment that something is wrong.**
It is only ever a flag that two things disagree. If a decision was
genuinely and deliberately changed later — for example, something decided
one way at one point, and intentionally changed to something else at a
later point in the same project's own work — that is not an error. It is
one true fact correctly replacing an earlier one, and the mechanism for
this is supersession (§10): the proposing agent, which has direct,
contemporaneous knowledge that the change was deliberate, marks the
contradiction resolved (`resolution: closed_by_new_fact`), and a resolved
contradiction does not block auto-promotion. Only a genuinely unexplained
disagreement — where nothing available tells the proposing agent which of
two conflicting claims is current — is a case for the developer's review
list, consistent with the two-outcome model in §3, Principle 2. The
governor never judges, on its own, whether a later decision was the
*right* decision; it only judges whether the disagreement has been
accounted for.

**Cross-project contradictions are always treated as an anomaly requiring
human decision** — never auto-resolved, regardless of risk level or
confidence, with no exception path.

## 13. Manual Submission

The developer may submit material directly for governance by pointing the
governor at a path — a file or folder — rather than composing structured
JSON by hand. `provenance.source_type = "user"`. This is the same
submission pipeline as any other writer, distinguished only by credential
and source type.

**The real-world front end for this is `mb-submit-memory`, an OpenCode
skill**, invoked as `/mb-submit-memory <path>` — not raw API calls. It is
deliberately its own skill, not folded into `docs-manager`, `mb-align-docs`,
or `mb-wikilinks`: those three each own exactly one job and interoperate
with nothing else by design, and adding memory-submission to any of them
would break that boundary. `mb-submit-memory` carries the §11A obligation
directly — it must query GBrain for related content and read it before
submitting, supplying a genuinely reasoned `confidence`/`contradiction`
assessment, never a placeholder value.

## 13A. PDLF Step-Completion Writer (New)

A second, distinct writer, identified during review as a real gap rather
than a planned feature: PDLF's own step-completion process. Every one of
PDLF's steps — all 46 of them, not only the 7 formal gates — ends in a
full stop, per PDLF's own execution discipline, before the next step's
work begins. That full stop is where the second of PDLF's two standing
housekeeping questions is answered, and as of this revision, that answer
is no longer "run GBrain's ordinary sync command." It is "route this
step's real artifacts through the memory governor," using a dedicated
credential (`pdlf_step_sync`, distinct from both GBrain-dreaming's and
manual submission's) so the governor can always tell which writer a
candidate came from.

This writer holds the same §11A obligation as every other: the OpenCode
agent that just executed the step, having direct, contemporaneous
knowledge of what it did, is responsible for assessing each artifact's
confidence and checking it against existing memory before submission — not
the developer, not the governor. A single step can produce more than one
artifact worth remembering; each is submitted and decided individually,
not batched as one candidate.

The concrete mechanics of this writer — its place in the five-point due
diligence sequence, and the two questions still open about how it
interacts with an in-progress PDLF step — are recorded in the companion
[[[pdlf:makepdlf-project-library/docs-local/system-description|System Description]]](C:/pdlf/makepdlf-project-library/docs-local/system-description.md) and Implementation Workflow, not duplicated here.

## 14. Self-Healing / Iterative Learning

The governor may observe patterns in its own decision history (e.g. "this
source's candidates are routed to developer review at an unusually high
rate, and are typically rejected once reviewed") and generate a
`procedural`-type memory candidate
describing that observation. This candidate is submitted through the
governor's own pipeline like any other candidate. Because policy/threshold
changes fall under `high_risk_types`, this guarantees mandatory human
review before any actual behavior change — the governor proposes, it never
autonomously applies.

## 15. Security and Disaster Recovery

- Dedicated Postgres database, same instance as GBrain's existing database,
  distinct name, distinct scoped role (`memory_governor_svc`) — isolated
  credential and blast radius from the existing `gbrain` database.
- Per-writer API credentials (§11) — no shared/ambient write access.
- **Git-tracked backup, living inside the memory-governor application's own
  repository** (resolved: not a separate external location — see
  Architecture §8 for the reasoning). Every promoted memory produces two
  things, committed together: a row in Register Memory Governor
  (the same append-only, never-delete register schema already used
  throughout this environment — see `register-global.md`,
  `register-local.md`) acting as a human-readable index, and a full JSON
  payload of the candidate at `registers/candidates/<memory_id>.json`
  capturing every field, not just the register's own columns. The register
  alone was found insufficient for real recovery (it cannot represent
  `content.text`); the register-plus-payload pair together can fully
  reconstruct a lost record.
- **Register/payload writes are asynchronous, not part of the promotion
  request.** Postgres and git cannot commit atomically across two separate
  systems (the "dual-write problem"); rather than couple the two systems
  together in the request path, the write is driven by the same
  transactional-outbox worker that already exists for other downstream
  effects (Architecture §4), with retry-with-backoff and a failure surfaced
  to the developer after repeated attempts rather than silently dropped or
  silently retried forever.
- `policy_version` is managed the same way: a dedicated register
  (`register-memory-governor-policy.md`), one row per policy version,
  previous version retired with `superseded-by` pointing at the new one on
  every change.

## 16. Dependencies and Prerequisites

- **GBrain's `MEMORY_VERBS` MCP surface** (`recall`/`remember`/`entity`/
  `synthesize`/`forget`) must be enabled (`gbrain config set mcp_surface
  verbs`) before the governor can write approved memory into GBrain. Per
  [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md), this is currently **disabled** in this environment.
  This is a concrete, outstanding prerequisite, not yet resolved.
- A dedicated Postgres database and role must be provisioned (§15).
- The memory-governor application's own git repository must have a remote
  configured before Phase 7 of the implementation workflow — this is now a
  trivial requirement, since the register lives inside that repo rather
  than a separately managed location.

## 17. Operational Footprint

Stated explicitly because it was raised as a direct concern: this design
adds no new class of infrastructure to the existing environment.

- Postgres: one additional database on the already-running instance used by
  GBrain — not a new server, not measurably more RAM.
- The governor's own process (API + worker): comparable in footprint to a
  browser tab, idle almost all the time, waking only on event or a 60-second
  poll.
- No LLM inference anywhere in the governor itself — the only model cost in
  the whole pipeline is upstream in GBrain dreaming, which already exists
  and is already paid for.
- No message broker, no vector database, no GPU, no second server.
- The git-backed register/payload store is small text (JSON + markdown
  tables) — realistically low hundreds of MB even after years of sustained
  use at solo-developer volumes.

## 18. Non-Goals for This Version

- No cross-tenant propagation (not applicable — see §5).
- No autonomous policy self-modification (see §14).
- No retrieval/query interface (see §5).
- No message-broker infrastructure (Kafka/Redis) — see companion
  specification §4 for the simpler mechanism chosen instead.

## 19. Success Criteria

The governor is fit for purpose when:
- No candidate reaches durable GBrain memory without passing provenance,
  scope, and contradiction checks.
- Every high-risk or contradicted candidate produces a genuine blocking
  review with recommendation/validation/ramifications, never a silent
  auto-promotion.
- Postgres state can be fully reconstructed from the git-tracked register
  and payload store alone, with no data loss beyond the most recent
  not-yet-committed batch.
- A new PDLF project can be onboarded without any code change.
- A dormant project's memory survives indefinitely, untouched, until
  reactivated.
