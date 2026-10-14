---
title: "memory-governor-explainer"
doc-id: "mb-47216ab9"
updated: "2026-10-14"
---
# Memory Governor — Explainer

*Companion note: for current confirmed state — the system is ACTIVE as of
2026-09-08, with every listed defect resolved, and re-verified on 2026-09-30
after the GBrain upgrade — see
[[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md). For procedures, see
[[[mybizz-config-docs:memory-governor/memory-governor-reference|Usage, Invocation, and Incident Response]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md).*

## 1. Opening

An AI agent that writes directly from its own raw output into durable,
permanent memory has no check on whether what it just wrote is actually
true. This isn't hypothetical — it's a documented failure mode in the
field: episodic memory in AI agents introduces unwanted retention,
unpredictability, and real deception risk, precisely because memory
formation is typically ungoverned. Concretely: GBrain's own dream cycle
synthesizes concepts and facts from raw project material, and nothing
checked those candidates for provenance, contradiction, or risk before
they became part of GBrain's durable, queryable memory.

Memory Governor exists to close that gap. It is a control-plane service —
provenance-checked, rule-based, audit-logged — sitting between memory
generation and durable GBrain storage. No candidate reaches durable,
queryable memory through the governed path without passing through it
first. It is a gatekeeping layer, not a memory store in its own right. It
does not replace GBrain; it decides what GBrain is allowed to durably
remember.

**Operational reality since 2026-09-08: the gate is not only built — it is
running.** Two processes (the deciding API and the delivering worker) are
live and verified; a permanent auto-start installation is approved so
"the gate was closed" stops being a possible state. The same day's work
resolved the system's one documented spec inconsistency, fixed a real
isolation defect caught by its own test, and brought the worker into
persistent operation for the first time.

## 2. The Decision Engine — Exactly Two Automatic Outcomes

The governor's decision function, `decide_path()`, is fully deterministic
and rule-based by design — no AI judgment, no model call, decides a
candidate's fate. This is a deliberate tradeoff: adaptive, LLM-judged
promotion exists elsewhere in the field, and was rejected here in favor of
determinism and auditability.

**The automatic engine may only ever produce one of two outcomes: promote
a candidate straight through, or route it to the developer's review list.**
This is a real, live design correction, not the original plan — the
system's first version allowed the engine to automatically reject or
quarantine a candidate on its own, closing it out without the developer
ever being told. Direct review caught this, and the design was rewritten.
A candidate routed to review is genuinely blocking — it cannot reach a
durable state before an explicit developer decision is recorded. It
carries a recommendation, a validation summary, and a ramifications
statement, and may carry a suggested `classification` and
`recommended_action` — but that suggestion is always attached to an open
item, never a decision already made.

The engine evaluates, in order: provenance (server-verified writer
identity), scope consistency, contradictions (unresolved ones only block),
the five high-risk types, low confidence, and medium-risk-moderate-
confidence. Each failing trigger produces one of six named review
classifications (the full table is in the reference); nothing triggered
means `auto_promote`.

## 3. Where Confidence and Contradiction Judgments Actually Come From

The governor enforces rules against a candidate's confidence and
contradiction status — but it never computes either value itself. Doing so
would require exactly the kind of AI judgment the deterministic-engine
principle rules out.

**Responsibility sits with whichever agent is actually proposing the
candidate** — the one with direct, contemporaneous knowledge of what it
just did. Before submitting, that agent must query GBrain for related
material, read what comes back, and arrive at a genuine confidence
assessment and contradiction determination — never a hardcoded default.
This is a process requirement on every writer, carried as a mandatory part
of their procedures (`mb-submit-memory`, PDLF's writer).

## 4. Contradiction Handling — A Flag, Not a Verdict

Contradiction checking runs for every candidate, every memory type, no
exceptions — an earlier version gated it to high-risk types only, and that
gap was corrected.

**A detected contradiction is not, by itself, a judgment that something is
wrong.** It only means two things disagree. If a decision was genuinely
and deliberately changed later, that's one true fact correctly replacing
an earlier one — handled through supersession (`resolution:
closed_by_new_fact`), and a resolved contradiction doesn't block automatic
promotion. Only a genuinely unexplained disagreement routes to review.
**Cross-project contradictions are a hard exception** — they always route
to review, regardless of confidence.

## 5. Cross-Project Sharing — A Real Gap That Had to Be Found and Built

Every candidate carries `owning_project` and `shared_with`. The write-time
check (does the sharing declaration make internal sense) was built and
tested early. The read-time question had gone unbuilt: does a request
scoped to project B actually see a candidate shared with project B?
Checking directly confirmed the mechanism was missing entirely; it was
found by checking rather than assuming, then built properly, with
permanent regression coverage.

**The 2026-09-8 extension of the same lesson — isolation below the API.**
The system's own end-to-end test then caught a deeper layer: governed
memories were written into GBrain **world-visible regardless of declared
scope**, and carried no project identity, so no project-scoped read was
even possible. (The 2026-09-08 wording called GBrain's facts layer
brain-global; that was corrected on 2026-09-30, see below.) The real
guarantees now enforced: every
governed fact is stamped with its owning project (`entity`), and
visibility is mapped from declared scope (`shared_all` → world; everything
else → private). Project-scoped recall is entity-scoped recall.

**Facts are stored per source.** Every fact belongs to a source, and `recall` reads the facts of one source. The worker names the owning project's own documentation source on every write, so a governed fact lands with the documents it belongs to, in a federated source, and an ordinary search finds its fact file. Isolation between projects is enforced by the governor itself (entity stamping, visibility mapping, read-time resolution); it does not come from GBrain's sources. A fact written before 2026-10-01 may still sit in `memory-governor-code`.

## 6. Backup and Disaster Recovery — Why Two Writes, Not One

Every promoted memory produces two things, committed together: a
human-readable index row, and a full JSON payload of the complete
candidate. The index alone cannot reconstruct a lost Postgres record — it
has no column for the content text. Postgres and git cannot be committed
atomically together, so the register-and-payload write is asynchronous —
a queued, retryable consumer of the same outbox mechanism as every other
downstream effect. On failure it retries with backoff; after five
consecutive failures it surfaces the failure rather than blocking the
promotion or retrying silently forever. The worker git-commits AND pushes
the register changes. Proven twice by real disaster-recovery drills,
including once with GBrain writes in the picture.

## 7. The Event Backbone, and Why There's No Message Broker

For a single-operator, single-machine deployment, a separate Kafka/Redis/
RabbitMQ instance was judged unjustified infrastructure. Instead: a
transactional outbox plus Postgres's native `LISTEN`/`NOTIFY`, with one
dedicated worker process. Any state change that should trigger downstream
processing inserts an event row in the same transaction as the change and
issues a `NOTIFY`; the worker holds a persistent `LISTEN` connection and
wakes immediately, polling on a fixed interval as a safety net. One
mechanism is both the durable event log and the queue. Confirmed live:
notify-driven wake measured at ~0.15 seconds.

## 8. The Two Processes — Why Both Must Run

The deciding and the delivering are deliberately separate: the API makes
the governed decision; the worker performs every downstream effect (the
GBrain write, the register/payload write). Both consume the same
`MEMORY_GOVERNOR_DATABASE_URL` and both read their configuration from the
environment at start — the startup coupling documented in
`mb-submit-memory`'s explainer. Until 2026-09-08 the worker had no
production entry point at all (the documented "dedicated worker process"
was unstartable outside tests) — an entry-point defect, resolved the same
day, and the worker's first persistent run began then. Both start the one
correct way (reference); a permanent auto-start installation makes their
running state independent of anyone remembering to start them.

## 9. `mb-submit-memory` — The Real Front End for Manual Submission

The developer's actual way of submitting material for governance is
`mb-submit-memory`, an OpenCode skill — deliberately its own skill. It follows
a single-continuous-run rhythm and carries the full
judgment obligation directly: query GBrain for related content, read it,
supply genuinely reasoned confidence and contradiction values — never a
placeholder. It was proven end-to-end with a real document.

## 10. The Writer GBrain's Dream Cycle Cannot Actually Be, and Why

This is the single most important structural nuance in the whole system.

**GBrain's dream cycle cannot be routed through the governor at all** —
investigated exhaustively: `dream` has no interception point of any kind.
Forking GBrain's own source to intercept those writes was considered and
rejected — a permanent re-merge obligation against GBrain's releases,
forever, for a problem solvable another way.

**The real, working alternative:** `dream` runs in real, named phases, and
GBrain separately ships `gbrain eval suspected-contradictions` — confirmed
not to run automatically as part of the dream cycle. The accepted,
documented discipline: run `dream` for real (never `--dry-run`), run the
contradiction evaluation immediately afterward, review the findings. This
is the one honestly-documented exception to "every writer's output is
governed through the same API" — a genuine structural limit of governing
third-party software with no exposed extension point, named plainly per
the standing no-discrepancies requirement.

Only two writers submit through the governor's real API: manual submission
via `mb-submit-memory`, and PDLF's step-completion writer under its own
credential (`pdlf_step_sync`).

## 11. A Real Incident — An Accidental Write Into Live Memory, and How It Was Recovered

During testing of the GBrain-write logic, a chained script ran several
commands without verifying each result. The command meant to create a
disposable test source failed cleanly; the script continued; the next
`remember` executed against whatever source was actually active — the real
`mb-3-cs-code`. A real, permanent, factually-false fact entered live
memory.

**Recovery was deliberate and fully verified:** `recall` (not `search`,
which returns unrelated content by similarity) found the real `fact_id`;
`forget` expired it keeping its full audit trail; a second recall verified
the expiry. **The lasting fix was structural** — a redesigned test fixture
(check=True halting, unconditional try/finally restoration) and a standing
regression test. The same discipline caught the 2026-09-08 isolation
defect: the test asserted what the system should guarantee, the assertion
failed against reality, and reality was corrected.

## 12. Suitability

- **Best for:** gating developer- and PDLF-authored facts and decisions
  into durable memory with real provenance, contradiction, and risk
  checks; any submission where being *believed later* is the point.
- **Good for:** deliberate corrections via atomic supersession; cross-
  project sharing with read-time visibility; self-observation (the
  governor may notice patterns in its own decision history and *propose*
  a policy change — which routes through the same human gate, since policy
  changes are themselves high-risk).
- **Not good for:** bulk raw content (the mirror layer — sync's job);
  dream-cycle output (structurally ungovernable — the manual discipline);
  forcing past review (the engine has no such path by design); running
  without both processes (an API without a worker silently strands
  promotions in the outbox).

## 13. Known Limitations, Honestly Stated

**GBrain's dream cycle is structurally ungovernable through this system's
API** — covered in §10. Its content reaches GBrain through a real,
deliberate, always-applied manual discipline. A permanent property of the
third-party tool, reported per the no-discrepancies requirement.

**Governed facts are stored in the owning project's own source** — covered in §5. Governed-memory isolation is enforced
by the governor (API-level visibility resolution + write-path stamping), not
by GBrain's sources. Reported.

**The GBrain upgrade of 2026-09-30 (0.46.1.0 → 0.59.18.0).** The governor
reaches GBrain only through the `gbrain` command line (`sources default`,
`remember`), so the upgrade touched it only there. Across 114 agent tools
present in both versions, no input was removed and none became required;
the verbs gained optional inputs (`source_id` and others). After the upgrade
both processes ran, all 85 facts were still present, and a real governed
submission was promoted end to end. One incident surfaced: the brain default
source named a source that no longer existed, which stops `gbrain sync`
under 0.59.18.0 (reference, incident 2026-09-30). The governor's own test
runner is not aware of the systemd units and was not run. No change to the
governor's code was made or needed.

**Several phases are closed by explicit developer decision, not
completion**, pending PDLF's own go-live (a real PDLF step end-to-end;
repeated real dream cycles under ordinary use). Deliberately parked, real,
working infrastructure — reported separately from defects, per the
no-open-defects requirement.

**The governor may observe patterns in its own decision history and
propose a policy change, but may never apply one to itself** — policy
changes are high-risk content, so any self-generated candidate is
guaranteed to require human review.

## 14. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md) — emulated from the
PostgreSQL pilot. The short local version:

- [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) is the **spec** — the ideal state every exam
  checks against.
- Before each exam run, the config-manager synthesizes Exam Plan:
  a fresh job-spec built from this spec, the last report, the log, and the
  learnings. The plan is transient (the file is live; contents rewritten each
  cycle).
- The exam runs the installed skill (`mb-config-memory-governor`) with the plan
  in hand — detection fully autonomous; healing gated. **This module has no
  agent-healable items**: the worker and API are the only writers to
  `registers/` and the database; every repair is developer-run or proposed.
- **Scope boundary with the postgres module:** database conformance (tables,
  ownership) and the estate backup convention belong to `mb-config-postgresql`
  (this exam cross-references; quick row counts permitted).
- Several checks are permanently **developer-run**: credentialed registry
  checks, the full test suite, the auto-start execution, recovery drills.
- The run rewrites Exam Report (current state, no
  history), appends one row to Log, files new learnings,
  and prunes absorbed entries.

## 15. S.W.O.T.

**Strengths.** Mechanical two-outcome gating of everything entering permanent
memory; the decision engine is source-verified with all five high-risk types
governed; the register is a git-committed second write (disaster recovery
proven twice); the event backbone needs no message broker; 304-test suite
green at last full run.

**Weaknesses.** The deterministic test runner is not aware of the systemd
units (it stops the worker with `kill` and starts an unmanaged copy afterwards);
the brain default source is changed by
every write and can go stale; several checks are
permanently developer-run (credentialed checks, full test suite); row counts
are live and drift continuously (point-in-time assertions only).

**Opportunities.** The config-management exam adds standing liveness + auth-gate
verification that never existed for the governor; the register/DB dual-write
gives the exam a second consistency surface to check (index ↔ payload).

**Threats.** An accidental write into live memory is the recorded real incident
class (recovery procedure exists and is proven); the auth-gate silently opening
would be a silent failure (exam M0-4 asserts the 422 exactly); FK/dupe-key
errors from dev-testing have appeared in logs before (rate-watch, not alarm).

## 16. Closing

The governor's entire job is narrow: decide what's allowed to become
permanent, trusted memory, using rules a human can audit, never a judgment
call it makes for itself. Every real correction described here — the
two-outcome rewrite, the read-time sharing gap, the accidental write and
its verified recovery, the honest acknowledgment of the one ungovernable
writer, and the 2026-09-08 resolution set (the spec inconsistency, the
isolation defect its own test caught, the worker's missing entry point) —
came from the same discipline: check directly, verify at each step, and
never let "should work" stand in for "confirmed working." The system now
runs, both processes live, with every known defect resolved and every
remaining dependency named.

---

*Companion documents: [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) (the spec),
[[[mybizz-config-docs:memory-governor/memory-governor-reference|Usage, Invocation, and Incident Response]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md) (procedures and incident response),
Exam Plan / Exam Report /
Log / [[[mybizz-config-docs:memory-governor/memory-governor-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-learnings.md) (config-management
set), Memory Governor Skill (exam skill canonical source). Architecture:
[[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md). The full memory-system map:
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md). The front end: `mb-submit-memory` (its own
suite). System health procedure: `memory-functionality-audit.md` (memory functionality audit)
(mybizz-os-docs).*

*End of document*
