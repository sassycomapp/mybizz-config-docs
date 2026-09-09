# Sentinel Configuration — dev-makepdlf

Canonical current-state configuration record. Agent-facing. Reflects the
verified live state as of 2026-09-09. States facts, not history — the
design genesis is `sentinel-security-system.md` (recovered), the agreed
scope is `sentinel-scope.md` (this folder), and the reasoning matters in
`sentinel-explainer.md`.

---

## Identity

| Item | Value |
|---|---|
| Skill 1 | `mb-sentinel-review` — installed (`~/.config/opencode/skills/mb-sentinel-review/`, byte-identical mirror in this folder) |
| Skill 2 | `mb-compile-rules` — installed; functional (built and amended 19 rules; latest amendments 2026-09-08) |
| Purpose | Step-triggered security review for PDLF steps, in service of shipped-application safety for clients and their users |
| Design genesis | `sentinel-security-system.md` (this folder, 2026-08-23, 2,204 lines — the original research conversation; recovered 2026-09-09 and serving as the plan document) |
| Scope | `sentinel-scope.md` (this folder) — the agreed three-layer scope |
| Reasoning methodology | `secure-software-engineering` — **installed 2026-09-09** at `~/.config/opencode/skills/secure-software-engineering/` (SKILL.md + 11 references + 3 templates + evals); upstream `github.com/magnus919/agent-skills/tree/main/secure-software-engineering` (MIT) |

## Environment position (per `mybizz-os-docs/environment-explainer.md`)

| Layer | Sentinel's presence |
|---|---|
| pre-makePDLF (where we are) | The skill, the security-global library, the findings database, the methodology — all built, verified, usable |
| makePDLF | The step-intensity wiring — built into each Sentinel-covered step file as it is developed (Step 16 done as the pattern; Steps 17–46 pending as built) |
| PDLF | The reviews fire during real step executions — testable against a real feature from PDLF's first run |
| shipped estate | **Out of Sentinel's scope** — no runtime safeguards built into the applications (a different scope of work, deferred) |

## Security-global library (verified live 2026-09-09)

| Item | Value |
|---|---|
| Root | `C:\dev\project-library-global\security-global\` |
| Categories | 7: principles (9), requirements (6), threat-models (11), infrastructure (10), cloud (7), secrets (6), testing (5) |
| Documents | 54, `sec-` prefix throughout |

## Governing architecture document

`adr-global/adr-dependency-based-not-multi-tenant.md` (Sealed) — cross-client
data isolation is **structural** (one Anvil app per client, one database per
client, `app_tables` resolves to the calling client's own tables —
live-tested 2026-06-13). Consequences for Sentinel: multi-tenancy patterns
(tenant discriminator columns, tenant-filtered queries, tenant context in
sessions) are **security findings**, not style issues — they would replace
structural isolation with a failure-prone filter. The review vocabulary is
within-instance: user-role access control, the Vault, server-side-only data
access. Related ADRs: `adr-client-instance-architecture.md`,
`adr-client-instance-readme-five-app-system.md`,
`adr-dependency-update-model.md`.

## Database — `triage_findings` (verified live 2026-09-09)

| Item | Value |
|---|---|
| Server | **Windows** PostgreSQL 15, `pdlf` database, role `pdlf_agent` — a DIFFERENT cluster from WSL's PostgreSQL 16 (GBrain + memory governor) despite the same port |
| Access route | The PowerShell bridge ONLY — direct WSL psql silently connects to the wrong server (`spec-postgres-ledger.md`, binding) |
| Verified state | Table exists; **0 rows** (Sentinel has never run live) |
| Sentinel-relevant columns | `source_step` (CHECK: 16,17,19,20,21,34,35,36,37,38,39,45,46), `triage_label` (CHECK: needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix, clear), `concern`, `asset`, `threat`, `evidence`, `severity` (Low/Medium/High/Critical), `confidence` (Low/Medium/High), `recommended_control`, `verification`, `finding_id` (free-standing text, no companion table) |
| Label mapping | FLAG → `needs-triage` · ESCALATE → `needs-info` · CLEAR (reviewed) → `clear` · a step not in the intensity table produces no row at all — not the same as `clear` |

## Step-intensity table (per `sentinel-security-system.md`; numbers provisional until each step file is built)

| Step | Scrutiny | Built as a real PDLF step file? |
|---|---|---|
| 16 — Domain model | Low/Medium | Yes — `stepwise/step-16-domain-modeling.md` (invocation at item 7, gate-proof at item 9 — verified live 2026-09-09) |
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
| `stepwise/step-16-domain-modeling.md` | item 7 | item 9 |

## Related, non-duplicated tools (cross-reference only — not part of Sentinel)

| Tool | What it is | Real command |
|---|---|---|
| GStack whole-codebase audit | Daily (low-noise) + monthly (comprehensive) security posture scan, read-only | `/cso` |
| PDLF Step 37 code-review security specialist | Authentication/authorization, cryptographic misuse, attack-surface, trust-boundary input validation | The security specialist inside `/review` |

## Known scope limitations (accepted, not defects)

- **`mb-sentinel-review` has never been run live against a real feature.**
  Built, installed, wired into Step 16, and its database path verified
  2026-09-09. The first real PDLF-run feature is the test that matters.
- **Eleven of twelve scoped steps have nothing to retrofit into.** Their
  intensity numbers remain provisional until each is built and checked.
- **`finding_id` has no companion table** — free-standing text identifier.
- **The methodology skill was installed 2026-09-09 without a restart** —
  OpenCode may need a session restart before the skill registers in its own
  catalog; the reference files are readable from disk regardless, which is
  what the review step uses.

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
