---
title: "sentinel-reference"
doc-id: "mb-a075fac8"
updated: "2026-10-01"
---
# Sentinel Reference — Usage, Invocation, and Worked Examples

Companion to [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|dev-makepdlf]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) (current state) and
[[[mybizz-config-docs:mb-sentinel-review/sentinel-explainer|What It Is, What It Does, and Why It Matters]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-explainer.md) (design genesis and reasoning). The skill's own
`SKILL.md` is the authoritative procedure.

---

## Invoking `mb-sentinel-review`

**From inside a retrofitted step file** (normal case): the step file's own
numbered instruction invokes it directly — see `stepwise/
step-16-domain-modeling.md` item 7 for the real, working example. No manual
invocation needed.

**Manual, ad-hoc invocation:**
```
/mb-sentinel-review (step-number) (feature-description)
```
Example:
```
/mb-sentinel-review 16 "New CONTEXT.md entries: Booking, Slot, Customer"
```
`step-number` must be one of the values in the intensity table
([[[mybizz-config-docs:mb-sentinel-review/sentinel-config|dev-makepdlf]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md)). A step number not in that table returns `CLEAR`
immediately, with no analysis performed and no database row written — this
is correct behavior, not a bug, per the skill's own Section 1.

## The review cycle (8 steps — SKILL.md is authoritative)

1. Step number checked against the intensity table. Not listed → `CLEAR`,
   stop, no row. Listed → continue.
2. Matching security-global document(s) identified (mapping below). No
   clear match → ESCALATE, never an assumed CLEAR.
3. Document(s) read in full — never reasoned from a title or category.
4. Reasoned against, using the `secure-software-engineering` methodology
   (installed at `~/.config/opencode/skills/secure-software-engineering/`
   — its reference files are read at review time when the step's feature
   touches their domain).
5. Outcome reached: `CLEAR`, `FLAG`, or `ESCALATE`.
6. Row written to `triage_findings` (bridge procedure below).
7. `CLEAR` → row written already resolved. Done. `FLAG`/`ESCALATE` → STOP.
   Reported to the developer. No further action by the skill itself.
8. Learnings recorded.

## The governing ADR — checked at every data-touching review

[[[default:adr-global/adr-dependency-based-not-multi-tenant|Mybizz CS is a Dependency-Based Architecture, Not a Multi-Tenant Architecture]]](C:/dev/project-library-global/adr-global/adr-dependency-based-not-multi-tenant.md) (Sealed). Cross-client isolation
is structural — separate Anvil apps, separate databases. Consequences for
the review:

- Tenant discriminator columns (`client_id`, `tenant_id`,
  `organisation_id`, `account_id`), tenant-filtered queries, tenant session
  context, and cross-client access functions are **prohibited patterns** —
  a match is a FLAG-level finding (they weaken structural isolation).
- The only legitimate identity-based filtering is **user-role access
  control within one client instance** (`anvil.users.get_user()` → role →
  filter) — the [[[default:security-global/threat-models/sec-broken-access-control-within-instance|Broken Access Control Within a Client Instance]]](C:/dev/project-library-global/security-global/threat-models/sec-broken-access-control-within-instance.md) patterns
  apply.
- Direct, unfiltered `app_tables` queries are the approved pattern.

## Step-to-document mapping (SKILL.md Section 2)

| Step | Document(s) checked |
|---|---|
| 17 | [[[default:security-global/requirements/sec-requirements-data-table-creation\|New Data Table Creation]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-data-table-creation.md) + matching `threat-models/` document + the governing ADR |
| 34 | [[[default:security-global/requirements/sec-requirements-architecture-review\|Architecture Review]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-architecture-review.md) + the governing ADR |
| 35 | [[[default:security-global/requirements/sec-requirements-server-function\|New Server Function]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-server-function.md) + matching `threat-models/` document + the governing ADR |
| 37 | Same document(s) as the step that introduced the code under review |
| 38 | [[[default:security-global/testing/sec-testing-coverage-minimum\|Security Test Coverage Minimum]]](C:/dev/project-library-global/security-global/testing/sec-testing-coverage-minimum.md) + the threat-model document's own Verification Requirements |
| 45 | [[[default:security-global/requirements/sec-requirements-release-readiness\|Release Readiness]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-release-readiness.md) + [[[default:specifications-global/spec-observability\|Observability Requirements]]](C:/dev/project-library-global/specifications-global/spec-observability.md) (the monitoring standard behind the release check) |

If no document clearly matches: ESCALATE, not an assumed CLEAR.

## Writing the finding — the database route

The `pdlf` ledger runs on **Windows** PostgreSQL 15. A direct WSL psql
**silently connects to the wrong server** (WSL's own PostgreSQL 16 —
GBrain's cluster). The documented bridge is the only correct route:

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGPASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -U pdlf_agent -d pdlf -c '<the INSERT or SELECT>'"
```

Worked FLAG (the canonical example — a real broken-access-control catch):

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

Worked CLEAR:

```sql
INSERT INTO triage_findings (
  step_id, finding_id, source_step, triage_label, resolution_note, resolved_at
) VALUES (
  42, 'sentinel-35-002', '35', 'clear',
  'Sentinel: matches sec-broken-access-control-within-instance.md Approved Pattern; no client-supplied identifier used',
  now()
);
```

## Querying Sentinel's findings

**All open Sentinel findings, any step:**
```sql
SELECT * FROM triage_findings
WHERE source_step IN ('16','17','19','20','21','34','35','37','38','39','45','46')
  AND triage_label IN ('needs-triage','needs-info')
  AND resolved_at IS NULL;
```

**Gate-proof check** (built into [[[makepdlf-project-library:stepwise/step-16-domain-modeling|Step 16 Domain Modeling]]](C:/dev/dev-makepdlf/makepdlf-project-library/stepwise/step-16-domain-modeling.md) item 9):
```sql
SELECT 1 FROM triage_findings
WHERE step_id = (real step_id)
  AND triage_label IN ('clear','needs-triage','needs-info')
LIMIT 1;
```
No row returned: Sentinel did not run — per item 9, the gate does not
proceed.

**Release-readiness check** (per
[[[default:security-global/requirements/sec-requirements-release-readiness|Release Readiness]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-release-readiness.md)):
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
Requires a real Markdown source at
`C:\dev\project-library-global\rules-cupcake-global\cup-(rule-name).md`.
**Functional** — it has built and amended 19 rules (latest 2026-09-08),
all live-tested under active enforcement. Its own procedure:
`mb-compile-rules/SKILL.md`.

## Do not

- Do not query `triage_findings` for Sentinel findings without filtering
  `source_step` to the intensity table's list — other steps (36, for
  example) write to the same table for unrelated reasons.
- Do not treat a missing row as equivalent to a CLEAR — a missing row means
  the review never ran; `clear` means it ran and found nothing.
- Do not hand-write a `triage_label` outside the six real allowed values.
- Do not connect to the `pdlf` ledger with direct WSL psql — the bridge is
  the only route to the right server.
- Do not use multi-tenancy vocabulary in any finding — the ADR is binding;
  tenant patterns are findings, not idioms.
- Do not implement a fix — flag and propose; PDLF's cycle implements.
