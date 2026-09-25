---
title: "sentinel-scope"
doc-id: "sentinel-scope"
---
# Sentinel — Scope

Agreed scope for the Sentinel system. Drafted 2026-09-09 from the scoping
side conversation; the credo applies: simple, secure, robust, fit for
purpose. This document is the spine the component suite hangs from.

---

## What Sentinel is

The step-triggered security review for PDLF. At defined steps, it reads the
real security-standard documents, reasons about the real feature being
built, and records the outcome in the PDLF ledger. It flags and proposes;
it never fixes. It exists so that the applications built through PDLF are
safe for clients and their users.

---

## What it is built from (the pre-makePDLF layer — exists now)

| Part | State |
|---|---|
| The security-global library — 54 documents, 7 categories; the authority on what "secure" means here | Built, verified live 2026-09-09 |
| The skill — `mb-sentinel-review` (the 8-step review cycle: check step → match documents → read fully → reason → CLEAR/FLAG/ESCALATE → write the row → stop) | Built, installed, never run live |
| The findings record — `triage_findings` (Windows PG15 `pdlf` DB, bridge-only access; verified live: table exists, 0 rows) | Built, verified live |
| The reasoning methodology — `secure-software-engineering` (upstream: github.com/magnus919/agent-skills/tree/main/secure-software-engineering) | **Installed 2026-09-09** — `~/.config/opencode/skills/secure-software-engineering/` (SKILL.md + 11 references + 3 templates + evals; supply-chain review passed) |
| The design genesis — [[sentinel-security-system|SSS - sentinel Security System]] (recovered 2026-09-09) | Recovered; serves as the plan document — suite citations re-point to it |

**Relevant references from** `C:\dev\project-library-global\` (every file below verified on disk 2026-09-09):

| Folder | Relevant references |
|---|---|
| `adr-global` | **The five-app family:** [[adr-dependency-based-not-multi-tenant|Mybizz CS is a Dependency-Based Architecture, Not a Multi-Tenant Architecture]] (Sealed — the governing architecture ADR; tenant patterns are findings) · [[adr-client-instance-architecture|Client Instance Architecture]] · [[adr-client-instance-readme-five-app-system|Mandatory README in Every Client Instance Documenting the Five-App System]] · [[adr-dependency-update-model|Dependency Update Model]] · **The payment/webhook family:** [[adr-payment-security-boundary-vault|Payment Security Boundary: Secret Keys Deferred to the Vault]] (gateway secret keys deferred to the Vault — directly security-relevant) · [[adr-webhook-architecture|Webhook Architecture]] (three external services POST webhooks to client instances — the incoming untrusted-HTTP surface) · [[adr-payment-gateway-configuration-is-a-settings-function-and-is-rbac-governed|Payment Gateway Configuration Is a Settings Function and Is RBAC-Governed]] (RBAC governance of a critical function) · [[adr-payment-gateway-mutability|Payment Gateway Mutability]] (gateway assignment change policy) · the onboarding ADR family ([[adr-onboarding-data-schema-alignment|Onboarding Data Schema Alignment]], [[adr-onboarding-finality|Onboarding Finality]], [[adr-onboarding-resumability|Onboarding Resumability]], [[adr-onboarding-vs-settings-boundary|Onboarding vs Settings Boundary]]) |
| `security-global` | The full library — 54 documents across `principles/` (9), `requirements/` (6), `threat-models/` (11), `infrastructure/` (10), `cloud/` (7), `secrets/` (6), `testing/` (5) — the authority Sentinel reviews against |
| `specifications-global` | [[spec-security|Security Specification]] · [[spec-security-architecture|Security & Secrets Architecture]] · [[spec-vault-system|The Vault System]] · [[spec-five-app-architecture-model|Five-App Architecture Model (Specification)]] · [[spec-api-specification|API Specification (HTTP Endpoints)]] · [[spec-regulatory-compliance-baseline|Regulatory Compliance Baseline (Specification)]] (POPIA — mandatory every app; the regulatory driver behind the client-safety motive) · [[spec-observability|Observability Requirements]] (Anvil-native structured observability — the standard behind the Step 45 monitoring check) |

Reference assessment (developer uncertainty resolved): the **regulatory-compliance baseline** is included — POPIA registration and data-subject rights are mandatory for every app, which makes it a requirement-awareness reference for Steps 17 (personal data in tables) and 34 (architectural constraints), cited when personal data is involved. The **observability spec** is included as the Step 45 secondary reference — the release-readiness requirement's "monitoring confirmed active" is defined by this spec. Both are secondary-citation references: the review reads them when the step's feature touches their domain, not on every pass.

---

## What it becomes (the makePDLF layer — built as steps are built)

The wiring. Twelve steps carry security scrutiny; each Sentinel-covered
step file gets two things as it is built, following the Step 16 pattern:

1. **The invocation** — the step's own instruction calls
   `/mb-sentinel-review` at the right point in its sequence.
2. **The gate-proof check** — a verified `triage_findings` row is required
   before the step's gate proceeds. No row, no gate.

| Step | Scrutiny | Status |
|---|---|---|
| 16 — Domain model | Low/Medium | **WIRED** — [[step-16-domain-modeling|Step 16 Domain Modeling]] (invocation item 7, gate-proof item 9, verified live 2026-09-09) |
| 17 — Data tables | High | Pending — wired when the step file is built |
| 19 — Tickets | Medium | Pending |
| 20 — Design | Medium/High | Pending |
| 21 — Concept lock | Medium | Pending |
| 34 — Architecture verification | Very High | Pending |
| 35 — Build | High | Pending |
| 37 — Code review | Very High | Pending |
| 38 — QA | High | Pending |
| 39 — Triage | — | Pending |
| 45 — Canary | Medium | Pending |
| 46 — LEARN | — | Pending |

Section 9's scrutiny numbers for unbuilt steps are provisional until each
real step file exists — confirmed against it, the same way Step 16 was.

---

## What it does (the PDLF layer — when PDLF runs)

During real step executions, the reviews fire at their wired points. Every
outcome lands in `triage_findings` (including CLEAR, resolved immediately).
FLAGs and ESCALATEs stop for the developer's decision; PDLF's ordinary
build-review-test-triage cycle implements. The developer triages every flag
into one of three kinds:

| Kind | Meaning | Action |
|---|---|---|
| Legitimate, minimal consequence | Something real, not worth work | Set aside; move on |
| **Illegitimate** | Raised with no cause — the detector is wrong | **A system defect: correct the detection logic** |
| Legitimate, requires attention | Real and material | Decide; PDLF implements |

Over-warning is preferred to silence. An alarm with a real event of minimal
consequence is legitimate; an alarm with no cause is a detector defect.

---

## The doctrine (the review's own rules)

- Read the real document before reasoning — never a title or category.
- Three outcomes: CLEAR, FLAG, ESCALATE. "I don't know" is a valid, required
  answer.
- Every outcome writes a real row — no outcome leaves no trace.
- The content fields are real and specific — never a templated placeholder.
- Never implement a fix; never resolve a row; never resubmit to force an
  outcome.
- Multi-tenancy vocabulary in a reviewed feature is itself a finding — the
  ADR is binding.

---

## The boundaries (what Sentinel is not)

- **Not `/cso`** — the whole-codebase sweep, different rhythm, complement.
- **Not the `/review` security specialist** — independent general code
  review; Sentinel checks library conformance. Complement.
- **Not Cupcake** — Cupcake keeps honest agents honest (mechanical,
  always-on); Sentinel reasons at defined moments.
- **Not the memory governor's review queue** — a separate review discipline
  for a separate system; parallel, not connected.
- **Not continuously running; not auto-triggered; never implementing.**

---

## In scope — and out

**In scope:** security review of the twelve intensity-table steps, against
the security-global library, recorded in the PDLF ledger. The review of
what we build — before it ships.

**Out of scope:** the shipped estate itself (no runtime safeguards built
into the applications — that is a different scope of work, deferred until
the PDLF steps that scope shipping are developed); continuously-running
enforcement (Cupcake's job); general code quality (PDLF's own review and
QA); anything requiring GBrain or the memory system at runtime.

---

## How we know it works

- The gate-proof rows: every covered step's review is provable after the
  fact.
- The findings record: every outcome is a real, queryable row in the
  ledger.
- **The first real feature** through Steps 16 → 17 → 35 → 37 → 38 is the
  true test — expected naturally, at PDLF build time, with no special
  effort.

---

## Open items

- The first real review run — expected naturally at PDLF build time.
