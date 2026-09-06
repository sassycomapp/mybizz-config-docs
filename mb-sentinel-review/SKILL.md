---
name: mb-sentinel-review
description: |
  Runs Sentinel's step-triggered security review against a real PDLF step.
  Checks the step number against the step-intensity table
  (sentinel-security-system-plan.md Section 9). Not listed: CLEAR
  immediately, no analysis performed, no record written — the step was
  never in Sentinel's scope. Listed and reviewed: identifies the matching security-global
  document(s), reads them, reasons about the specific feature using the
  secure-software-engineering methodology, and produces CLEAR, FLAG, or
  ESCALATE. FLAG or ESCALATE writes a real row to triage_findings and
  stops for developer decision. Never implements a fix itself — flags
  and proposes only.
---

# mb-sentinel-review

Security-review layer for PDLF steps. Not a standalone security agent.
Not continuously running. Fires only when invoked, per the step-intensity
table below.

---

## Section 0 — Hard rules. Do not deviate.

1. **Never implement a fix.** This skill flags and proposes. It never
   edits application code, never resolves a `triage_findings` row itself.
   The developer decides; PDLF's own build/review/test/triage cycle
   implements.
2. **"I don't know" is a valid, required outcome.** If there is not
   enough evidence to decide CLEAR or FLAG with real confidence, the
   outcome is ESCALATE, not a guess in either direction.
3. **Never leave a CLEAR outcome unrecorded.** A CLEAR result gets a real
   row in `triage_findings`, the same as FLAG or ESCALATE — see Section
   3, Step 6. There is no outcome of this skill that leaves no trace.
4. **Read the real document before reasoning.** Never reason from a
   document's title or category alone — open and read the specific
   `security-global` file(s) that match, every time.

---

## User-invocable

Invoked as `/mb-sentinel-review (step-number) (feature-description)` for
a manual, ad-hoc review. Normally invoked automatically from inside a
PDLF step's own instructions, at the point that step's build calls for
it — the same way `mb-submit-memory` is invoked from step files, not
run as a background process.

---

## Section 1 — Step-intensity table (from `sentinel-security-system-plan.md` Section 9)

| Step | Scrutiny |
|---|---|
| 16 | Low/Medium |
| 17 | High |
| 19 | Medium |
| 20 | Medium/High |
| 21 | Medium |
| 34 | Very High |
| 35 | High |
| 36 | (existing PDLF triage source step) |
| 37 | Very High |
| 38 | High |
| 39 | — (findings enter as ordinary governed findings) |
| 45 | Medium |
| 46 | — (lessons enter GBrain) |

Any step number not in this table: CLEAR, immediately, no further action.
This is the same list already confirmed live against the real
`triage_findings.source_step` CHECK constraint.

---

## Section 2 — Cycle, per invocation

### Step 1 — Check step number

Compare the invoking step number against Section 1. Not listed: go
directly to Step 6 (CLEAR). Listed: continue.

### Step 2 — Identify matching document(s)

Based on the step number and the real feature/change being reviewed,
identify which document(s) in `security-global/` apply. Use the
step-to-question mapping already established:

- Step 17 → `requirements/sec-requirements-data-table-creation.md`, plus
  any specific `threat-models/` document matching the actual data
  involved (e.g. payment data → `sec-payment-manipulation.md`).
- Step 34 → `requirements/sec-requirements-architecture-review.md`.
- Step 35 → `requirements/sec-requirements-server-function.md`, plus any
  specific `threat-models/` document matching the feature.
- Step 37 → the same document(s) identified at the step that introduced
  the code being reviewed — code review re-checks against the same
  standard, it does not invent a new one.
- Step 38 → `testing/sec-testing-coverage-minimum.md`, plus the specific
  `threat-models/` document(s)' own Verification Requirements.
- Step 45 → `requirements/sec-requirements-release-readiness.md`.

If no existing document clearly matches, this is itself an ESCALATE —
do not proceed as if CLEAR because nothing matched.

### Step 3 — Read the matched document(s)

Read the real file content — Applicable Threat, Security Requirement,
Approved Pattern, Prohibited Pattern — in full. Do not proceed from a
filename or category alone.

### Step 4 — Reason

Compare the real feature/change against the document's Approved and
Prohibited patterns, using the `secure-software-engineering` skill's own
methodology for how to reason about this class of question. Form a real
judgment — not a template-filling exercise.

### Step 5 — Determine outcome

- **CLEAR** — the feature matches the Approved Pattern, or the
  document's concern genuinely does not apply here, with real confidence.
- **FLAG** — a real concern exists, matching or resembling the
  Prohibited Pattern, and there is enough evidence to describe it
  concretely.
- **ESCALATE** — not enough evidence, or not enough confidence, to
  decide CLEAR or FLAG. This includes Step 2's own "no document
  matched" case.

### Step 6 — On CLEAR

**Corrected — a CLEAR outcome is now recorded, not left unwritten.**
Write a real row to `triage_findings`:

```
INSERT INTO triage_findings (
  step_id, finding_id, source_step, triage_label,
  resolution_note, resolved_at
) VALUES (
  (step_id), (a real finding_id), (step number), 'clear',
  'Sentinel: no concern found', now()
)
```

`resolved_at` is set immediately — a CLEAR result has nothing left to
triage. Report `CLEAR` in the conversation, naming the step, the
document(s) checked, and a one-line reason, in addition to the row
written. Nothing further happens.

### Step 7 — On FLAG or ESCALATE

Construct the finding using the real, confirmed `triage_findings`
columns:

```
INSERT INTO triage_findings (
  step_id, finding_id, source_step, triage_label,
  concern, asset, threat, evidence, severity, confidence,
  recommended_control, verification
) VALUES (...)
```

- `triage_label`: `'needs-triage'` for FLAG, `'needs-info'` for
  ESCALATE. Confirmed, 2026-08-27 — `needs-triage` is the correct match
  for a fresh, unreviewed finding; `needs-info` is the correct match for
  insufficient evidence to decide, which is ESCALATE's own definition.
- `severity`, `confidence`: real values, per Section 7 of
  `sentinel-security-system-plan.md` — never a placeholder or default
  value.
- `recommended_control`: drawn directly from the matched document's own
  Approved Pattern, not invented independently of it.

STOP after writing the row. Do not proceed, do not implement, do not
mark it resolved. Present the finding to the developer in the same
plain format as `sentinel-security-system-plan.md` Section 7.

### Step 8 — Learnings

Record any real, durable pattern noticed — a document that needed
updating, a step-to-document mapping that was unclear — to this skill's
own log location, matching the convention already used by
`mb-submit-memory`.

---

## Section 3 — Completion status protocol

- **CLEAR (step not in Section 1's table)** — reported inline, nothing
  written to the database. The step was never in Sentinel's scope.
- **CLEAR (step reviewed, no concern found)** — a real row written to
  `triage_findings`, `triage_label = 'clear'`, `resolved_at` set
  immediately.
- **FLAG** / **ESCALATE** — a real row written to `triage_findings`,
  reported to the developer, stopped for their decision.
- **BLOCKED** — could not determine which document applies and Step 2's
  own "no match" ESCALATE path was not sufficient to proceed (e.g. the
  database itself is unreachable) — state exactly what stopped the run.

Never mark a run CLEAR without having actually read the matched
document(s) in Step 3. Never write a FLAG or ESCALATE row without real,
specific `concern`/`asset`/`threat`/`evidence` content — never a
templated placeholder.
