---
title: "sentinel-config"
doc-id: "mb-967f5148"
updated: "2026-10-09"
---
# Sentinel Configuration — dev-makepdlf

Canonical current-state configuration record. Agent-facing. Reflects the
verified live state as of 2026-09-09. States facts, not history — the
design genesis is [[[mybizz-config-docs:mb-sentinel-review/sentinel-security-system|SSS - sentinel Security System]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-security-system.md) (recovered), the agreed
scope is [[[mybizz-config-docs:mb-sentinel-review/sentinel-scope|Scope]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-scope.md) (this folder), and the reasoning matters in
[[[mybizz-config-docs:mb-sentinel-review/sentinel-explainer|What It Is, What It Does, and Why It Matters]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-explainer.md).

---

## Identity

| Item | Value |
|---|---|
| Skill 1 | `mb-sentinel-review` — installed (`~/.config/opencode/skills/mb-sentinel-review/`; authoritative copy — body hash `c4a2fe90283224cf` recorded 2026-10-07 after the gate-approved citation re-point; no mirror maintained in this folder — the suite's `sentinel-skill.md` holds the exam-skill source) |
| Skill 2 | `mb-compile-rules` — installed; functional — 20 compiled rules (`cup-*.rego` in `~/.config/cupcake/policies/opencode/`) plus 3 grants-data files; 6 `.bak` backups at root; 20 rule documents in `rules-cupcake-global/` (documentation only) [verified live 2026-10-07] |
| Purpose | Step-triggered security review for PDLF steps, in service of shipped-application safety for clients and their users |
| Design genesis | [[[mybizz-config-docs:mb-sentinel-review/sentinel-security-system\|SSS - sentinel Security System]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-security-system.md) (this folder, 2026-08-23, 2,204 lines — the original research conversation; recovered 2026-09-09 and serving as the plan document) |
| Scope | [[[mybizz-config-docs:mb-sentinel-review/sentinel-scope\|Scope]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-scope.md) (this folder) — the agreed three-layer scope |
| Reasoning methodology | `secure-software-engineering` — **installed 2026-09-09** at `~/.config/opencode/skills/secure-software-engineering/` (SKILL.md + README + 11 methodology references + source-index.md + 3 templates + evals.json — matches upstream tree shape; registered in the session skill catalog); upstream `github.com/magnus919/agent-skills/tree/main/secure-software-engineering` (MIT — re-verified live 2026-10-07: actively maintained) |

## Environment position (per the pre-makePDLF, makePDLF, PDLF, and shipped layers)

| Layer | Sentinel's presence |
|---|---|
| pre-makePDLF (where we are) | The skill, the security-global library, the findings database, the methodology — all built, verified, usable |
| makePDLF | The step-intensity wiring — built into each Sentinel-covered step file as it is developed (Step 16 wired as the pattern; all twelve step files built as of 2026-10-01/04 — Steps 17–46 exist but are not yet wired; retrofit approved as a PDLF-development work item 2026-10-07) |
| PDLF | The reviews fire during real step executions — testable against a real feature from PDLF's first run |
| shipped estate | **Out of Sentinel's scope** — no runtime safeguards built into the applications (a different scope of work, deferred) |

## Security-global library (verified live 2026-09-09; re-verified 2026-10-07 — counts exact)

| Item | Value |
|---|---|
| Root | `C:\dev\project-library-global\security-global\` |
| Categories | 7: principles (9), requirements (6), threat-models (11), infrastructure (10), cloud (7), secrets (6), testing (5) |
| Documents | 54, `sec-` prefix throughout |

## Governing architecture document

[[[default:adr-global/adr-dependency-based-not-multi-tenant|Mybizz CS is a Dependency-Based Architecture, Not a Multi-Tenant Architecture]]](C:/dev/project-library-global/adr-global/adr-dependency-based-not-multi-tenant.md) (Sealed) — cross-client
data isolation is **structural** (one Anvil app per client, one database per
client, `app_tables` resolves to the calling client's own tables —
live-tested 2026-06-13). Consequences for Sentinel: multi-tenancy patterns
(tenant discriminator columns, tenant-filtered queries, tenant context in
sessions) are **security findings**, not style issues — they would replace
structural isolation with a failure-prone filter. The review vocabulary is
within-instance: user-role access control, the Vault, server-side-only data
access. Related ADRs: [[[default:adr-global/adr-client-instance-architecture|Client Instance Architecture]]](C:/dev/project-library-global/adr-global/adr-client-instance-architecture.md),
[[[default:adr-global/adr-client-instance-readme-five-app-system|Mandatory README in Every Client Instance Documenting the Five-App System]]](C:/dev/project-library-global/adr-global/adr-client-instance-readme-five-app-system.md),
[[[default:adr-global/adr-dependency-update-model|Dependency Update Model]]](C:/dev/project-library-global/adr-global/adr-dependency-update-model.md).

## Database — `triage_findings` (verified live 2026-09-09)

| Item | Value |
|---|---|
| Server | **Windows** PostgreSQL 15, `pdlf` database, role `pdlf_agent` — a DIFFERENT cluster from WSL's PostgreSQL 16 (GBrain + memory governor) despite the same port |
| Access route | The PowerShell bridge ONLY, port **5433** (`-p 5433` — the ledger's port was changed after 2026-09-09; documented 2026-10-07 after the exam's failed 5432 attempt) — direct WSL psql silently connects to the wrong server ([[[pdlf:makepdlf-project-library/specifications-local/spec-postgres-ledger\|Spec Postgres Ledger]]](C:/pdlf/makepdlf-project-library/specifications-local/spec-postgres-ledger.md), binding) |
| Verified state | Table exists; **0 rows** (re-verified live 2026-10-07 via the bridge; `step_id` carries an FK to `steps(id)` — recorded 2026-10-07) |
| Sentinel-relevant columns | `source_step` (CHECK: 16,17,19,20,21,34,35,36,37,38,39,45,46), `triage_label` (CHECK: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix, clear), `concern`, `asset`, `threat`, `evidence`, `severity` (Low/Medium/High/Critical), `confidence` (Low/Medium/High), `recommended_control`, `verification`, `finding_id` (free-standing text, no companion table) |
| Label mapping | FLAG → `needs-triage` · ESCALATE → `needs-info` · CLEAR (reviewed) → `clear` · a step not in the intensity table produces no row at all — not the same as `clear` |

## Step-intensity table (per [[[mybizz-config-docs:mb-sentinel-review/sentinel-security-system|SSS - sentinel Security System]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-security-system.md); numbers confirmed against each real step file at wiring time — Step 16 done; retrofit pending for the rest)

| Step | Scrutiny | Built as a real PDLF step file? |
|---|---|---|
| 16 — Domain model | Low/Medium | Yes — [[[pdlf:makepdlf-project-library/stepwise/step-16-domain-modeling\|Step 16 Domain Modeling]]](C:/pdlf/makepdlf-project-library/stepwise/step-16-domain-modeling.md) (invocation at item 7, gate-proof at item 9 — verified live 2026-09-09) |
| 17 — Data tables | High | Yes — built 2026-10-01, not yet wired |
| 19 — Tickets | Medium | Yes — built 2026-10-01, not yet wired |
| 20 — Design | Medium/High | Yes — built 2026-10-04, not yet wired |
| 21 — Concept lock | Medium | Yes — built 2026-10-01, not yet wired |
| 34 — Architecture verification | Very High | Yes — built 2026-10-01, not yet wired |
| 35 — Build | High | Yes — built 2026-10-01, not yet wired |
| 37 — Code review | Very High | Yes — built 2026-10-01, not yet wired |
| 38 — QA | High | Yes — built 2026-10-01, not yet wired |
| 39 — Triage | — | Yes — built 2026-10-01, not wired (ordinary triage usage of the ledger) |
| 45 — Canary | Medium | Yes — built 2026-10-01, not yet wired |
| 46 — LEARN | — | Yes — built 2026-10-01, not yet wired |

Steps not in this table: no material security scrutiny by default.

## Retrofitted step files

| Step file | `mb-sentinel-review` invoked at | Gate-proof check at |
|---|---|---|
| [[[pdlf:makepdlf-project-library/stepwise/step-16-domain-modeling\|Step 16 Domain Modeling]]](C:/pdlf/makepdlf-project-library/stepwise/step-16-domain-modeling.md) | item 7 | item 9 |

## Related, non-duplicated tools (cross-reference only — not part of Sentinel)

| Tool | What it is | Real command |
|---|---|---|
| GStack whole-codebase audit | Daily (low-noise) + monthly (comprehensive) security posture scan, read-only | `/cso` |
| PDLF Step 37 code-review security specialist | Authentication/authorization, cryptographic misuse, attack-surface, trust-boundary input validation | The security specialist inside `/review` |

## Known scope limitations (accepted, not defects)

- **`mb-sentinel-review` has never been run live against a real feature.**
  Built, installed, wired into Step 16, and its database path verified
  2026-09-09. The first real PDLF-run feature is the test that matters.
- **All twelve scoped steps now exist as files; only Step 16 is wired.** The
  intensity numbers are confirmed at wiring time, file by file (Step 16's
  pattern); the retrofit is an approved PDLF-development work item
  (2026-10-07).
- **`finding_id` has no companion table** — free-standing text identifier
  (verified live against the table definition 2026-10-07).
- **The methodology skill is registered in the OpenCode skill catalog**
  (verified live in-session 2026-10-07 — no restart needed; the original
  install-day caveat is superseded).

## Do not

- Do not treat Section 9's step numbers as final for any step not yet
  built — confirm against the real file when it exists, the same way Step 16 was.
- Do not write a new security-global document without first checking whether
  the category, or a specific fact, already exists elsewhere in
  `project-library-global`.
- Do not assume a CLEAR result from `mb-sentinel-review` needs no database row
  — corrected 2026-08-27.
- Do not let a PDLF gate pass on the assumption `mb-sentinel-review` was invoked
  — the real, current step file requires a verified `triage_findings` row before
  the gate procedure may begin; replicated in every future Sentinel-covered step file.
- Do not use multi-tenancy vocabulary in any review finding — the ADR is
  binding; tenant patterns are findings, not idioms.
- Do not connect to the `pdlf` ledger with direct WSL psql — it silently
  reaches the wrong server; bridge only.
