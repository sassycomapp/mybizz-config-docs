---
title: "sentinel-config"
doc-id: "mb-967f5148"
updated: "2026-10-20"
---
# Sentinel Configuration

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | Canonical commit `ee1877e` — the installed copy's body matches the canonical source |
| Standard taken from | The `mb-sentinel-review` repository at commit `ee1877e` — the installed version |
| Last researched | 2026-10-20 |

## Installed skill (`mb-sentinel-review`)

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Canonical source file | The repository's root file | `C:\mybizz\mb-sentinel-review\mb-sentinel-review.md` — GitHub-backed repository | repo-organization | |
| Installed copy | Body identical to the canonical source | `~/.config/opencode/skills/mb-sentinel-review/SKILL.md` — body identical; frontmatter packaging (`name`/`description` vs `title`/`doc-id`) differs by design | canonical repo file | |
| Body hash (sha256, body without frontmatter) | — | `673895ae8d51d3e0d9a73a74dc8e8f1f9af16cc4ebab32970d1cd0524923dd95` | verified live | |
| Runtime surface | — | registered in the OpenCode skill catalog | verified in-session | |

## Step-intensity table (canonical: SKILL.md Section 1 — `C:\mybizz\mb-sentinel-review\mb-sentinel-review.md`)

| Step | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| 11 — Init | High | Wired (Phase B): invocation and gate-proof in `b11-build-plan` and `b11-config`; also `b11-reference` item 26 | SKILL.md §1 | |
| 12 — Build notes: full task list | Medium | Wired (Phase B): invocation and gate-proof in `b12-build-plan` | SKILL.md §1 | |
| 14 — Build notes: plan-ceo-review | Medium | Wired (Phase B): invocation and gate-proof in `b14-build-plan` | SKILL.md §1 | |
| 15 — Build notes: plan-eng-review | High | Wired (Phase B): invocation and gate-proof in `b15-build-plan` | SKILL.md §1 | |
| 16 — Domain model | Low/Medium | Wired: invocation item 7 and gate-proof item 9 of `b16-reference` | SKILL.md §1 | |
| 17 — Data tables | High | Built (`c17`), not wired | SKILL.md §1 | |
| 19 — Tickets | Medium | Built (`c19`), not wired | SKILL.md §1 | |
| 20 — Design | Medium/High | Built (`c20`), not wired | SKILL.md §1 | |
| 21 — Concept lock | Medium | Built (`c21`), not wired | SKILL.md §1 | |
| 34 — Architecture verification | Very High | Built (`d34`), not wired | SKILL.md §1 | |
| 35 — Build | High | Built (`e35`), not wired | SKILL.md §1 | |
| 36 — PDLF triage source | Existing PDLF triage source step | Writes to the ledger as ordinary triage; not Sentinel-wired | SKILL.md §1 | |
| 37 — Code review | Very High | Built (`e37`), not wired | SKILL.md §1 | |
| 38 — QA | High | Built (`e38`), not wired | SKILL.md §1 | |
| 39 — Triage | — (findings enter as ordinary governed findings) | Built (`e39`), not wired | SKILL.md §1 | |
| 45 — Canary | Medium | Built (`f45`), not wired | SKILL.md §1 | |
| 46 — LEARN | — (lessons enter GBrain) | Built (`f46`), not wired | SKILL.md §1 | |

## Scope and environment

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Review scope | The intensity-table steps, against the security-global library, recorded in the ledger | The same scope | SKILL.md §1–§3 | |
| Step not in the table | CLEAR immediately — no analysis, no row | The same behavior | SKILL.md §1 | |
| Runtime mode | Not continuously running; fires only when invoked | The same | SKILL.md (header) | |
| Shipped estate | — | Out of scope: no runtime safeguards built into the applications; a separate scope of work | developer scope decision | |
| Memory system at runtime | — | No GBrain or memory-system dependency at review runtime | developer scope decision | |

## Governing architecture

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Governing ADR | [[[default:adr-global/adr-dependency-based-not-multi-tenant\|Mybizz CS is a Dependency-Based Architecture, Not a Multi-Tenant Architecture]]](C:/dev/project-library-global/adr-global/adr-dependency-based-not-multi-tenant.md) (Sealed) — binding on every review | Adopted | the ADR | |
| Related ADRs | — | [[[default:adr-global/adr-client-instance-architecture\|Client Instance Architecture]]](C:/dev/project-library-global/adr-global/adr-client-instance-architecture.md) · [[[default:adr-global/adr-client-instance-readme-five-app-system\|Mandatory README in Every Client Instance Documenting the Five-App System]]](C:/dev/project-library-global/adr-global/adr-client-instance-readme-five-app-system.md) · [[[default:adr-global/adr-dependency-update-model\|Dependency Update Model]]](C:/dev/project-library-global/adr-global/adr-dependency-update-model.md) | the ADRs | |

## security-global library

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Root | — | `C:\dev\project-library-global\security-global\` | the library | |
| Categories | 7 | principles (9), requirements (6), threat-models (11), infrastructure (10), cloud (7), secrets (6), testing (5) | verified live | |
| Documents | 54 | 54, `sec-` prefix throughout | verified live | |

## Ledger database (`triage_findings`)

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Server | [[[pdlf:pdlf-library/specifications-local/spec-postgres-ledger\|Spec Postgres Ledger]]](C:/pdlf/pdlf-library/specifications-local/spec-postgres-ledger.md) (binding) | Windows PostgreSQL 15, database `pdlf`, role `pdlf_agent` — a separate cluster from WSL's PostgreSQL 16 | the binding spec | |
| Port | 5433 | 5433 — through the PowerShell bridge only; direct WSL psql reaches the wrong server | the binding spec | |
| `source_step` CHECK | `11, 12, 14, 15, 16, 17, 19, 20, 21, 34, 35, 36, 37, 38, 39, 45, 46` — must equal the intensity table | The same 17 values | the binding spec | |
| `triage_label` CHECK | `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, `clear` | The same six values | the binding spec | |
| `severity` | `Low`, `Medium`, `High`, `Critical` | The same values | the binding spec | |
| `confidence` | `Low`, `Medium`, `High` | The same values | the binding spec | |
| `finding_id` | Free-standing text, no companion table | The same | the binding spec | |
| Label mapping | FLAG → `needs-triage` · ESCALATE → `needs-info` · CLEAR (reviewed) → `clear` · step outside the intensity table → no row | The same | SKILL.md §2 Step 7, §3 | |
| Build-verified gate | Every row for the feature's `step_id` must have `triage_label = 'wontfix'` or `resolved_at IS NOT NULL` | The same | the binding spec | |

## Reasoning methodology

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Skill | — | `secure-software-engineering` | | |
| Installed at | — | `~/.config/opencode/skills/secure-software-engineering/` | verified live | |
| Tree | Upstream shape | SKILL.md + README + `references/` (11 files + `source-index.md`) + `templates/` (3) + `evals/evals.json` | verified live | |
| Upstream | — | `github.com/magnus919/agent-skills/tree/main/secure-software-engineering` | | |
| Licence | MIT | MIT | | |

## Operational status

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Compiled rules | — | 20 `cup-*.rego` live in `~/.config/cupcake/policies/opencode/` | verified live | |
| Grants data | — | 3 grants-data files alongside the rules | verified live | |
| Backups | — | 6 `.bak` files at the policy root | verified live | |
| Source documents | — | 21 in `C:\dev\project-library-global\rules-cupcake-global\`; `no_bash_mediated_file_writes_without_grant.md` has no compiled counterpart | verified live | |
| Sentinel coverage | — | No compiled rule content mentions Sentinel or `triage_findings` | verified live | |

## Related tools (cross-reference; not part of Sentinel)

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Whole-codebase audit | — | GStack `/cso`: daily low-noise and monthly comprehensive modes; read-only | | |
| Step 37 security specialist | — | The security specialist inside GStack `/review` | | |

## Open items

None.
