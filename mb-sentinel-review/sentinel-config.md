# Sentinel Configuration — dev-makepdlf

Canonical current-state configuration record. Agent-facing. Reflects the working
state of Sentinel as integrated into the `dev-makepdlf` project as of 2026-08-27.
This document states facts, not history — where a decision was made and the
reasoning matters, see `sentinel-security-system-plan.md`.

---

## Identity

| Item | Value |
|---|---|
| Skill 1 | `mb-sentinel-review` |
| Skill 2 | `mb-compile-rules` |
| Install status | Both installed. Cupcake is installed, live, and enforcing — `mb-compile-rules` is confirmed functional, used to build and deploy 17 real rules on 2026-08-29. |
| Skill files | `SKILL-mb-sentinel-review.md`, `SKILL-mb-compile-rules.md` |
| Plan document | `sentinel-security-system-plan.md` |
| Explainer | `sentinel-explainer.md` |
| Reasoning methodology (borrowed, not invented) | `secure-software-engineering` skill, from the `magnus919/agent-skills` repository — `github.com/magnus919/agent-skills/blob/main/secure-software-engineering/SKILL.md` |

## Related, non-duplicated tools (for cross-reference only — not part of Sentinel)

| Tool | What it is | Real command |
|---|---|---|
| GStack whole-codebase audit | Daily (low-noise) + monthly (comprehensive) security posture scan, read-only | `/cso` |
| PDLF Step 37 code-review security specialist | Authentication/authorization, cryptographic misuse, attack-surface, trust-boundary input validation checks | The security specialist inside `/review` |

Neither is built or maintained by Sentinel — see `sentinel-explainer.md`
for why they were deliberately not duplicated. Full invocation detail for
both lives in GStack's own reference documentation, not here.

## Library location

| Item | Value |
|---|---|
| Root | `C:\dev\project-library-global\security-global\` |
| Categories | 7 |
| Documents | 54 |
| File prefix | `sec-` (all files, all subfolders) |

| Category | Documents |
|---|---|
| `principles/` | 9 |
| `requirements/` | 6 |
| `threat-models/` | 11 |
| `infrastructure/` | 10 |
| `cloud/` | 7 |
| `secrets/` | 6 |
| `testing/` | 5 |

No document exists outside these seven folders. No duplicate content exists
between `security-global/` and the pre-existing `specifications-global/`/`adr-global/`
material it reads from (`spec-vault-system.md`, `spec-security.md`,
`spec-security-architecture.md`, `spec-api-specification.md`,
`spec-five-app-architecture-model.md`, and the onboarding/payment-gateway ADRs).

## Database — `triage_findings` (Sentinel-relevant columns)

| Column | Type | Notes |
|---|---|---|
| `source_step` | text | CHECK: `16,17,19,20,21,34,35,36,37,38,39,45,46` |
| `triage_label` | text | CHECK: `needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix, clear` |
| `concern`, `asset`, `threat`, `evidence` | text | Sentinel finding content |
| `severity` | text | CHECK: `Low, Medium, High, Critical` |
| `confidence` | text | CHECK: `Low, Medium, High` |
| `recommended_control`, `verification` | text | Sentinel finding content |

Full schema: `spec-postgres-ledger.md`. `triage_label` mapping:
`FLAG → needs-triage`, `ESCALATE → needs-info`, `CLEAR (reviewed) → clear`.
A step not in Section 9's table produces no row at all — not the same as `clear`.

## Step-intensity table (current, per `sentinel-security-system-plan.md` Section 9)

| Step | Scrutiny | Built as a real PDLF step file? |
|---|---|---|
| 16 — Domain model | Low/Medium | Yes — `step-16-domain-modeling.md` |
| 17 — Data tables | High | No |
| 19 — Tickets | Medium | No |
| 20 — Design | Medium/High | No |
| 21 — Concept lock | Medium | No |
| 34 — Architecture verification | Very High | No |
| 35 — Build | High | No |
| 37 — Code review | Very High | No |
| 38 — QA | High | No |
| 39 — Triage | — | No |
| 45 — Canary | Medium | No |
| 46 — LEARN | — | No |

Steps not in this table: no material security scrutiny by default.

## Retrofitted step files

| Step file | `mb-sentinel-review` invoked at | Gate-proof check at |
|---|---|---|
| `step-16-domain-modeling.md` | item 7 | item 9 |

No other step file currently invokes `mb-sentinel-review` — none of the other
eleven scoped steps exist as built files yet.

## Known scope limitations (accepted, not defects)

- **`mb-sentinel-review` has never been run live.** Built, installed, wired into
  Step 16. Not yet exercised against a real invocation.
- **Eleven of twelve scoped steps have nothing to retrofit into.** Steps 17, 19,
  20, 21, 34, 35, 37, 38, 39, 45, 46 don't exist as built PDLF step files. Section
  9's own numbers for them remain provisional until each is built and checked
  against its real file — not assumed correct in advance.
- **`finding_id` has no companion table.** Confirmed against the full seven-table
  schema. Free-standing text identifier only.

## Do not

- Do not treat Section 9's step numbers as final for any step not yet built —
  confirm against the real file when it exists, the same way Step 16 was.
- Do not write a new `security-global` document without first checking whether
  the category, or a specific fact, already exists elsewhere in
  `project-library-global` — most of the original fourteen proposed categories
  were already covered before any new file was written.
- Do not assume a `CLEAR` result from `mb-sentinel-review` needs no database row
  — this was true in the skill's first version and was a confirmed defect,
  corrected 2026-08-27.
- Do not let a PDLF gate pass on the assumption `mb-sentinel-review` was invoked
  — the real, current step file requires a verified `triage_findings` row before
  the gate procedure may begin; this check must be replicated in every future
  Sentinel-covered step file, not just Step 16.
