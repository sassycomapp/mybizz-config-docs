# Sentinel Reference — Usage, Invocation, and Worked Examples

Companion to `sentinel-config.md` (current installed state) and
`sentinel-security-system-plan.md` (design and history). This document covers
how to actually invoke and query Sentinel's components. Agent-facing.

---

## Invoking `mb-sentinel-review`

**From inside a retrofitted step file** (normal case): the step file's own
numbered instruction invokes it directly — see `step-16-domain-modeling.md`
item 7 for the real, working example. No manual invocation needed.

**Manual, ad-hoc invocation:**
```
/mb-sentinel-review (step-number) (feature-description)
```
Example:
```
/mb-sentinel-review 16 "New CONTEXT.md entries: Booking, Slot, Customer"
```
`step-number` must be one of the values in Section 9's table
(`sentinel-config.md`). A step number not in that table returns `CLEAR`
immediately, with no analysis performed and no database row written — this is
correct behavior, not a bug, per the skill's own Section 1.

## The real decision flow, step by step

1. Step number checked against the table.
   - Not listed → `CLEAR`, stop. No row written.
   - Listed → continue.
2. Matching `security-global` document(s) identified. See the mapping table
   below.
3. Document(s) read in full.
4. Reasoned against, using the `secure-software-engineering` methodology.
5. Outcome reached: `CLEAR`, `FLAG`, or `ESCALATE`.
6. Row written to `triage_findings` (see `sentinel-config.md` for the schema
   and the `triage_label` mapping).
7. `CLEAR` → row written already resolved. Done.
   `FLAG`/`ESCALATE` → STOP. Reported to developer. No further action by the
   skill itself.

## Step-to-document mapping (from `mb-sentinel-review` Section 2, Step 2)

| Step | Document(s) checked |
|---|---|
| 17 | `requirements/sec-requirements-data-table-creation.md` + matching `threat-models/` document |
| 34 | `requirements/sec-requirements-architecture-review.md` |
| 35 | `requirements/sec-requirements-server-function.md` + matching `threat-models/` document |
| 37 | Same document(s) as the step that introduced the code under review |
| 38 | `testing/sec-testing-coverage-minimum.md` + matching `threat-models/` document's own Verification Requirements |
| 45 | `requirements/sec-requirements-release-readiness.md` |

If no document clearly matches: this is itself an `ESCALATE`, not an
assumed `CLEAR`.

## Worked example — a real `FLAG` finding

Feature: a new server function `get_bookings(staff_id)` at Step 35.

```
/mb-sentinel-review 35 "get_bookings(staff_id) - returns bookings for given staff_id"
```

Matched document: `threat-models/sec-broken-access-control-within-instance.md`.
Comparison: the function's own signature matches that document's Prohibited
Pattern exactly — `staff_id` accepted from the caller, used directly to filter,
with no check against the authenticated user's own identity.

Result: `FLAG`. Row written:

```sql
INSERT INTO triage_findings (
  step_id, finding_id, source_step, triage_label,
  concern, asset, threat, evidence, severity, confidence,
  recommended_control, verification
) VALUES (
  42, 'sentinel-35-001', '35', 'needs-triage',
  'get_bookings(staff_id) accepts staff_id from the caller with no ownership check',
  'Other staff members'' booking records',
  'Any authenticated Staff-role user, by supplying a different staff_id',
  'Function signature reviewed directly against sec-broken-access-control-within-instance.md Prohibited Pattern',
  'High', 'High',
  'Derive staff identity from anvil.users.get_user() server-side; remove staff_id parameter',
  'Log in as Staff A, call with Staff B''s id, confirm rejection'
);
```

## Worked example — a real `CLEAR` finding

Feature: a new server function `get_my_bookings()` at Step 35, matching the
Approved Pattern exactly (scope from `anvil.users.get_user()`, no client
parameter).

```sql
INSERT INTO triage_findings (
  step_id, finding_id, source_step, triage_label, resolution_note, resolved_at
) VALUES (
  42, 'sentinel-35-002', '35', 'clear',
  'Sentinel: matches sec-broken-access-control-within-instance.md Approved Pattern; no client-supplied identifier used',
  now()
);
```

## Querying Sentinel's own findings

**All open Sentinel findings, any step:**
```sql
SELECT * FROM triage_findings
WHERE source_step IN ('16','17','19','20','21','34','35','37','38','39','45','46')
  AND triage_label IN ('needs-triage','needs-info')
  AND resolved_at IS NULL;
```

**Confirm Sentinel actually ran for a given step instance** (the real check
now built into `step-16-domain-modeling.md` item 9):
```sql
SELECT 1 FROM triage_findings
WHERE step_id = (real step_id)
  AND triage_label IN ('clear','needs-triage','needs-info')
LIMIT 1;
```
No row returned: Sentinel did not run, or ran and wrote nothing — either way,
per item 9, the gate does not proceed.

**Release-readiness check** (per `requirements/sec-requirements-release-readiness.md`):
```sql
SELECT * FROM triage_findings
WHERE severity IN ('High','Critical')
  AND resolved_at IS NULL
  AND triage_label != 'wontfix';
```
Any row returned: release should not proceed until resolved.

## Invoking `mb-compile-rules`

```
/mb-compile-rules (rule-name)
```
Requires a real Markdown file already present at
`C:\dev\project-library-global\rules-cupcake-global\cup-(rule-name).md`.

**Currently non-functional in this environment** — Step 1 of the skill's own
prerequisite check confirms `cupcake eval` is a real, runnable command before
proceeding. It is not, until Cupcake itself is installed. Do not attempt a
real invocation until `sentinel-config.md`'s Known Scope Limitations section
is updated to reflect Cupcake's installation.

## Do not

- Do not query `triage_findings` for a Sentinel finding without filtering
  `source_step` to Section 9's real list — other steps (36, for example) write
  to the same table for unrelated, non-Sentinel reasons.
- Do not treat a missing row as equivalent to a `CLEAR` result — a missing row
  means Sentinel never ran; `clear` means it ran and found nothing.
- Do not hand-write a `triage_label` value outside the six real allowed
  values — the CHECK constraint will reject it.
