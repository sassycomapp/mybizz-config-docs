---
title: "mb-memory-system-diagnostic-explainer"
doc-id: "mb-dd98962e"
updated: "2026-10-03"
---
# mb-memory-system-diagnostic — What It Is, What It Does, and Why It Is Built This Way

Companion to [[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-config.md) (current
state) and [[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-reference.md) (commands and
report formats). The installed `SKILL.md` is the authoritative procedure; this
document owns the mental model: what the diagnostic is for, when to reach for
it, and why its sharpest rules exist.

---

## The Objective, Stated Plainly

The memory ecosystem — GBrain, the WSL PostgreSQL instance behind it, the
Memory Governor's durability gate, mb-submit-memory, Graphify, and the Dream
Cycle — is the substrate every other skill quietly trusts. When it degrades,
nothing fails loudly: a fact that never became durable still reads back as
saved, a stale graph still answers queries, a rotted backup still sits in its
folder looking like a backup. The failure modes of memory are silent by
nature, which is exactly why they need a loud, on-demand, honest check.

`mb-memory-system-diagnostic` is that check. It walks the ecosystem in one
ordered pass, section by section, running real commands and logging real
metrics — and where it finds something wrong, it stops and treats the defect
in place rather than accumulating it into an end-of-run report. It is
deliberately the opposite of an audit: a live pass that fixes where it can
(with approval), logs as it goes, and stops only where stopping is the safe
move.

## What It Actually Is

One procedure document, materialized in three layers:

1. **The source artifact** — `mb-memory-system-diagnostic-skill.md` in this
   suite folder; the canonical procedure, in the corpus's documentation-skill
   format (`title`/`doc-id` = filename stem).
2. **The installed skill** — a copy at
   `~/.config/opencode/skills/mb-memory-system-diagnostic/SKILL.md`, carrying the
   skill-discovery frontmatter (`name`/`description`) — the only copy that
   does — which is what makes `/mb-memory-system-diagnostic` invocable in
   OpenCode.
3. **Run reports** — one file per run at
   `C:\mybizz\memory-diagnostic-reports\`, appended section by section as
   each closes, ending in an aggregate roll-up.

The unit of work is the **section** — eleven of them: ten diagnostic sections
across the ecosystem (GBrain, PostgreSQL Instance B, Memory Governor,
governed-write positive and negative paths, Graphify, Cupcake interaction,
mb-submit-memory prerequisites, backups, Dream Cycle) plus a final roll-up.
Each section runs Diagnostic → Remediation → Reporting as its own loop, so a
healthy system passes through almost without interruption and a defective
section stops the run at exactly the point where the evidence is fresh.

Two gates govern the run: a **trouble gate** (a real defect, or a check that
cannot run, stops the run for a remediate/skip/abort decision) and a
**heavyweight-action gate** (any real-cost or state-changing write asks
first, healthy system or not).

## Feature Summary — conceptual

- **Whole-ecosystem coverage in one ordered pass**, ending in an aggregate
  verdict — the only tool in the estate that walks all six memory components
  in a single run.
- **Real-metric diagnostics** — every check runs for real and the report
  carries the real output or a faithful summary of it; a result that cannot
  be produced is a finding, never an invented pass.
- **In-place remediation under the trouble gate** — findings are treated at
  the moment of diagnosis, not banked for later.
- **Heavyweight-action gating** — governed writes, a real Dream Cycle run,
  and repo-creating remediations always ask first, regardless of health.
- **Trust-boundary checks with teeth** — role isolation proven via
  `has_database_privilege` (never `SET ROLE`, which a superuser session
  always passes vacuously); the governed spine proven in both directions
  (positive path: the gate says yes; negative path: the gate says no); backup
  pairs proven by hash, not by presence.
- **A live init-model check** — §2 refuses to assume either documented
  reality about WSL's service management and probes it first.
- **A Cupcake effect check** — verifies the enforcement layer did not
  interfere with the run without ever executing the enforcement layer.
- **Durable per-section reporting** — the report file holds everything that
  completed, even from an aborted run.

## Suitability

**Best for:** an on-demand, whole-ecosystem verification — before or after
memory-system changes, after a suspected incident, or whenever the developer
wants the substrate proven rather than assumed. Also the natural tool for
re-verifying after remediation, since each section's loop ends in a re-check.

**Good for:** narrowing an unknown memory failure to a section before deeper
per-component work; producing a durable, honest run record (the report file)
even from an aborted run; surfacing documented drift between component
suites and live reality (the init-model check is the built-in example).

**Not good for:** standing per-component conformance — that is the
`mb-config-*` exam modules' job (detection-only, per-component, part of the
config-management cycle); Cupcake policy or security posture — the cupcake
exam and the cso review own that, and this skill may never execute Cupcake
anyway; PostgreSQL Instance A / the `pdlf` ledger — outside the memory
ecosystem by definition; scheduled monitoring — the skill
is invocation-only by design.

## Why Diagnose–Remediate–Report Per Section, Not Audit-Then-Fix

A finding's context decays. At the moment §3 finds a stuck outbox, the
evidence for the right remediation is in the run's own hands — the API
response, the worker state, the register The use of registers has been discontinued. Please review diff. Banked into an end-of-run
report, the same finding becomes a backlog item that outlives its context and
invites a decision made from a summary instead of live evidence. The
per-section loop keeps diagnosis and decision adjacent, and it has a second,
quieter benefit: the report file is appended as each section closes, so an
aborted run still leaves a complete record of everything that was verified —
an audit-then-fix design loses its work product precisely when the run goes
wrong, which is when the record matters most.

## Why Two Distinct Gates

Conflating them fails in both directions. If a defect gate also gated
heavyweight actions, a healthy system would be waved straight through §4, §5,
and §10's real writes on the strength of §1–§3's cleanliness — exactly the
writes that must never run unattended. If heavyweight actions were treated as
findings, every declined action would be logged as a defect, polluting the
aggregate verdict with non-defects. The split keeps both halves honest: "skip"
on a finding is a real disposition about a real problem; "skipped by developer
choice" on a heavyweight action is not a defect and must never read as one.

## Why Cupcake Is Checked for Effect Only

The agent running this diagnostic is itself policed by Cupcake. Executing the
binary or live-testing a rule is permanently developer-only, and an
enforcement layer that could be probed by the process it polices would be an
enforcement layer with a hole. §7 inverts the question: did the police
interfere with this run? Denial/block lines in the run's own logs, the
loopback exemption's behavior during §4/§5, and the developer's direct answer
are the observable effects. A real finding here routes to a developer
decision about reconfiguring or disabling Cupcake before memory operations —
the skill cannot, and must not try to, remediate its own police.

## Why PostgreSQL Instance A Is Excluded

Instance A is the `pdlf` ledger — the application ledger, not part of the
memory ecosystem. Including it would widen every run's blast radius into a
production-data system that memory operations never touch, and blur the
meaning of the verdict: a PASS here must mean exactly "the memory system is
healthy" and nothing else. The exclusion is stated in the scope section, §2,
and §9 so that no section can drift into it.

## Why the Init-Model Check Runs First in §2

The recorded state is genuinely contradictory. `postgresql-reference.md`
(verified 2026-09-13) documents WSL here as systemd-less — `pg_ctlcluster` /
`service` only. Two days later, the Memory Governor's auto-start migration
flipped `systemd=true` in `/etc/wsl.conf`, a change its own documentation
states affects the entire WSL environment, not just the Governor's two
processes. Rather than silently picking the newer record, §2 probes PID 1 and
both management paths live, logs which actually work, and treats a mismatch
as a finding routed to a documentation correction (developer-approved before
editing) — never a live-system "fix" and never a contradiction papered over.
The same principle generalizes: a check that cannot run is a finding, not a
skip.

## Why Both Positive and Negative Governed-Write Tests

§4 alone proves the gate can say yes: a candidate flows submit → worker →
GBrain `private` fact → register The use of registers has been discontinued. Please review. But a gate that had silently lost its
ability to say no would pass §4 perfectly while every fact in the system
flowed straight to the durable layer unreviewed — the exact failure the gate
exists to prevent. §5 manufactures a must-review candidate (`policy` is one
of the five high-risk categories, classifying deterministically regardless of
confidence), proves the response is `under_review` and never `promoted`,
resolves it `rejected`, and cleans up. Both sections clean up unconditionally
in `try`/`finally` — a diagnostic must never leave state behind, including on
failure.

## Where It Sits in the System

The diagnostic is downstream of the six components' standing config suites —
it reads their recorded constants (the 62/62 RLS coverage, the high-risk
category list, the dream-cycle FAIL-expected reading, the ADR's remediation
sequence) instead of re-deriving them — and upstream of nothing: no build,
deploy, or enforcement consumes its output. It complements the `mb-config-*`
exams rather than duplicating them: those are per-component, detection-only,
and gate-resolving; this is cross-component, interactive, and treats defects
in place. It does not yet participate in the config-management exam cycle (no
`mb-config-*` module exists for it — an open item). It depends on the gbrain
CLI, the Governor's API and environment, the graphify CLI, the two backup
locations, and a developer present at the gates. Invocation is explicit-only;
nothing schedules it, and no skill chains into it without the developer
naming it.

## Honest Limits

- The skill has never run — every runtime claim (RLS counts, unit states,
  outbox counts, dump ages, graph freshness) is recorded procedure, not
  verified state, until a first live run executes.
- §7's developer question is subjective by design; a "felt slow" answer is
  logged verbatim as a metric, not adjudicated by the skill.
- The heavyweight sections cost real things — two disposable governed-write
  candidates, and LLM spend plus minutes for a real Dream Cycle run; a
  declined §10 leaves the Dream Cycle's live state unproven for that run.
- The skill trusts recorded constants from the sibling suites; if those
  suites drift, §2/§5 read them incorrectly — the exam modules, not this
  skill, are the standing guard on those records.
- §9 can only report backups — it never creates or refreshes dumps, so a
  failing backup habit surfaces as findings, not repairs.

## Deliberately Out of Scope

Cupcake internals and rule execution (developer-only, permanent); PostgreSQL
Instance A and its backups; everything outside the memory ecosystem;
scheduled or automatic triggering; silent documentation rewrites (a doc
correction is itself a gated remediation); compliance-style narrative
reporting (the report file is metrics and verdicts, not prose).

---

*Suite: [[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-config.md) (spec),
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-reference.md) (commands and report
formats), [[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-skill|Skill]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-skill.md) (the procedure — canonical
artifact in this folder, installed copy at
`~/.config/opencode/skills/mb-memory-system-diagnostic/SKILL.md`),
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-exam-plan.md) / 
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-exam-report.md) /
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-log|Log]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-log.md) /
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-learnings.md) /
[[[mybizz-config-docs:mb-memory-system-diagnostic/mb-memory-system-diagnostic-exam-skill|Exam Skill]]](C:/mybizz/mybizz-config-docs/mb-memory-system-diagnostic/mb-memory-system-diagnostic-exam-skill.md) (the config-management
exam set — the diagnostic's own standing check inventory; the diagnostic is
never executed by its exam). Ecosystem boundary:
`archify/output/memory-ecosystem-project/memory-ecosystem-scope.md`.*

*End of document*
