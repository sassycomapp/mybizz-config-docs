---
title: "sentinel-reference"
doc-id: "mb-a075fac8"
updated: "2026-10-20"
---
# Sentinel Reference — Usage, Invocation, and Worked Examples

Values live in [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Sentinel Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md); reasoning in [[[mybizz-config-docs:mb-sentinel-review/sentinel-explainer|the explainer]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-explainer.md). The skill's own `SKILL.md` is the authoritative procedure.

---

## Invoking `mb-sentinel-review`

**From a wired step file** (normal case): the step's own build-plan carries the invocation and the gate-proof check. Steps 11, 12, 14 and 15 carry them in their `b1x-build-plan` files (Step 11 also at `b11-reference` item 26); Step 16 carries them at `b16-reference` items 7 and 9. The `b12`, `b14` and `b15` reference files carry no Sentinel instruction. No manual invocation needed.

**Manual, ad-hoc invocation:**
```
/mb-sentinel-review (step-number) (feature-description)
```
Example:
```
/mb-sentinel-review 16 "New CONTEXT.md entries: Booking, Slot, Customer"
```
`step-number` must be one of the values in the intensity table ([[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Sentinel Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md)). A step number not in that table returns `CLEAR` immediately, with no analysis performed and no database row written — correct behavior, per the skill's own Section 1.

## The review cycle (8 steps — SKILL.md is authoritative)

1. Step number checked against the intensity table. Not listed → `CLEAR`, stop, no row. Listed → continue.
2. Matching security-global document(s) identified (mapping below). No clear match → ESCALATE, never an assumed CLEAR.
3. Document(s) read in full — never reasoned from a title or category.
4. Reasoned against, using the `secure-software-engineering` methodology (installed at `~/.config/opencode/skills/secure-software-engineering/` — its reference files are read at review time when the step's feature touches their domain).
5. Outcome reached: `CLEAR`, `FLAG`, or `ESCALATE`.
6. Row written to `triage_findings` (bridge procedure below) — CLEAR included, resolved immediately.
7. `FLAG`/`ESCALATE` → STOP. Reported to the developer. No further action by the skill itself.
8. Learnings recorded.

## Presenting a finding

On FLAG or ESCALATE, present the finding in plain words, one line per item: step, matched document, what the review found, severity, confidence, recommended control, and the decision needed. Severity is `Low`, `Medium`, `High` or `Critical`; confidence is `Low`, `Medium` or `High` — the values the ledger accepts.

## Step-to-document mapping (SKILL.md Section 2)

| Step | Document(s) checked |
|---|---|
| 11 | `cloud/sec-github-repository-access-control.md` + `infrastructure/sec-development-environment-credential-hygiene.md` + `secrets/sec-ai-agent-secret-visibility.md` — the app repositories are public, so nothing secret may enter them, and every repository's access must be what it should be |
| 12 | `threat-models/sec-multi-tenant-assumption-leakage.md` + `principles/sec-server-side-authority.md`, plus any `threat-models/` document matching the data the concept holds (payments → `sec-payment-manipulation.md`; sign-in → `sec-authentication-session.md`) |
| 14 | Any `threat-models/` document matching the data and capabilities the chosen scope adds, plus `requirements/sec-requirements-third-party-integration.md` when the scope includes an outside service |
| 15 | `requirements/sec-requirements-architecture-review.md` + `principles/sec-explicit-responsibility-assignment.md` + `principles/sec-least-privilege.md` — where are the trust boundaries, and is each one governed and assigned |
| 16 | Any `threat-models/` document matching the entities named in `CONTEXT.md`, plus `requirements/sec-requirements-data-table-creation.md` (Step 17 builds the tables from this vocabulary) |
| 17 | [[[default:security-global/requirements/sec-requirements-data-table-creation\|New Data Table Creation]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-data-table-creation.md) + matching `threat-models/` document + the governing ADR |
| 34 | [[[default:security-global/requirements/sec-requirements-architecture-review\|Architecture Review]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-architecture-review.md) + the governing ADR |
| 35 | [[[default:security-global/requirements/sec-requirements-server-function\|New Server Function]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-server-function.md) + matching `threat-models/` document + the governing ADR |
| 37 | The same document(s) identified at the step that introduced the code under review — code review re-checks against the same standard, it does not invent a new one |
| 38 | [[[default:security-global/testing/sec-testing-coverage-minimum\|Security Test Coverage Minimum]]](C:/dev/project-library-global/security-global/testing/sec-testing-coverage-minimum.md) + the matched threat-model document's own Verification Requirements |
| 45 | [[[default:security-global/requirements/sec-requirements-release-readiness\|Release Readiness]]](C:/dev/project-library-global/security-global/requirements/sec-requirements-release-readiness.md) + [[[default:specifications-global/spec-observability\|Observability Requirements]]](C:/dev/project-library-global/specifications-global/spec-observability.md) (the monitoring standard behind the release check) |

Secondary references are read when the feature touches their domain, not on every pass — for example the regulatory-compliance baseline (POPIA) when personal data is involved, and the observability spec behind the Step 45 release check. If no document clearly matches: ESCALATE, not an assumed CLEAR.

## The governing ADR — checked at every data-touching review

[[[default:adr-global/adr-dependency-based-not-multi-tenant|Mybizz CS is a Dependency-Based Architecture, Not a Multi-Tenant Architecture]]](C:/dev/project-library-global/adr-global/adr-dependency-based-not-multi-tenant.md) (Sealed). Consequences for the review, as imperatives:

- Treat tenant discriminator columns (`client_id`, `tenant_id`, `organisation_id`, `account_id`), tenant-filtered queries, tenant session context, and cross-client access functions as prohibited patterns — a match is a FLAG-level finding.
- Treat user-role access control within one client instance as the only legitimate identity-based filtering (`anvil.users.get_user()` → role → filter) — the [[[default:security-global/threat-models/sec-broken-access-control-within-instance|Broken Access Control Within a Client Instance]]](C:/dev/project-library-global/security-global/threat-models/sec-broken-access-control-within-instance.md) patterns apply.
- Treat direct, unfiltered `app_tables` queries as the approved pattern.

## Writing the finding — the bridge procedure

The ledger is reachable only through the PowerShell bridge (server and port: [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Sentinel Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md)):

```bash
cd <the PDLF project folder> && set -a && source .env && set +a
powershell.exe -NoProfile -Command "\$env:PGPASSWORD='$PGPASSWORD'; & 'C:\Program Files\PostgreSQL\15\bin\psql.exe' -h localhost -p 5433 -U pdlf_agent -d pdlf -c '<the INSERT or SELECT>'"
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
WHERE source_step IN ('11','12','14','15','16','17','19','20','21','34','35','37','38','39','45','46')
  AND triage_label IN ('needs-triage','needs-info')
  AND resolved_at IS NULL;
```
Step 36 is excluded: it writes to the same table as ordinary triage.

**Gate-proof check** (built into the wired step files — Step 16 at `b16-reference` item 9):
```sql
SELECT 1 FROM triage_findings
WHERE step_id = (real step_id)
  AND triage_label IN ('clear','needs-triage','needs-info')
LIMIT 1;
```
No row returned: Sentinel did not run — the gate does not proceed.

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
Live counts and state: the config's Operational status section.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Canonical skill source (`mb-sentinel-review`) | `C:\mybizz\mb-sentinel-review\mb-sentinel-review.md` | `ee1877e` | 2026-10-20 |
| Binding ledger specification | [[[pdlf:pdlf-library/specifications-local/spec-postgres-ledger\|Spec Postgres Ledger]]](C:/pdlf/pdlf-library/specifications-local/spec-postgres-ledger.md) | — | 2026-10-20 |
| security-global library | `C:\dev\project-library-global\security-global\` | — | 2026-10-20 |
| Governing ADR | [[[default:adr-global/adr-dependency-based-not-multi-tenant\|Mybizz CS is a Dependency-Based Architecture, Not a Multi-Tenant Architecture]]](C:/dev/project-library-global/adr-global/adr-dependency-based-not-multi-tenant.md) | — | 2026-10-20 |
| `secure-software-engineering` (installed) | `~/.config/opencode/skills/secure-software-engineering/` | — | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Intensity table | Read the canonical SKILL.md Section 1; compare row-for-row against the config's table | agent |
| Installed version | Diff the installed SKILL.md body against the canonical repository file; `git -C /mnt/c/mybizz/mb-sentinel-review log -1` | agent |
| Step wiring | Search the step's build-plan (and its reference file) for the `mb-sentinel-review` invocation and the gate-proof query | agent |
| security-global counts | Per-category file count, compared against the config's numbers | agent |
| Ledger reachable | The bridge procedure above with `SELECT count(*) FROM triage_findings;` | developer |
| Works | Run `/mb-sentinel-review` on a real feature at a wired step; confirm the `triage_findings` row through the bridge | developer |

## Do not

- Do not query `triage_findings` for Sentinel findings without filtering `source_step` to the intensity table's list — step 36 writes to the same table for unrelated reasons.
- Do not treat a missing row as equivalent to a CLEAR — a missing row means the review never ran; `clear` means it ran and found nothing.
- Do not assume a CLEAR outcome needs no database row — every reviewed outcome writes one.
- Do not let a gate pass on the assumption that `mb-sentinel-review` ran — require the verified gate-proof row before the gate procedure begins.
- Do not hand-write a `triage_label` outside the six real allowed values.
- Do not connect to the `pdlf` ledger with direct WSL psql — the bridge is the only route to the right server.
- Do not use multi-tenancy vocabulary in any finding — the ADR is binding; tenant patterns are findings, not idioms.
- Do not implement a fix, resolve a row, or resubmit to force an outcome — flag and propose; PDLF's cycle implements.
- Do not reason from a document's title or category — read the matched document in full before judging, and never mark a run CLEAR otherwise.
- Do not write a new security-global document without first checking whether the category, or the specific fact, already exists elsewhere in `project-library-global`.
