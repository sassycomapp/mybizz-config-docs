---
title: "memory-governor-config"
doc-id: "mb-63bdf286"
updated: "2026-10-20"
---
# Memory Governor Configuration

State of the memory governor: what exists, what each part is set to, and the
standard for it. Reasoning in [[[mybizz-config-docs:memory-governor/memory-governor-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-explainer.md);
procedures in [[[mybizz-config-docs:memory-governor/memory-governor-reference|Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md); standing differences in
[[[mybizz-config-docs:memory-governor/memory-governor-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-learnings.md).

---

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | 0.1.0 |
| Standard taken from | 0.1.0 |
| Last researched | 2026-10-20 |

## Repository and deployment

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Repository | — | `github.com/sassycomapp/memory-governor`; local clone `/home/dev-p/memory-governor` (WSL-native — do not relocate) | `repo-organization.md` | |
| Repository commits | — | Committed by hand; `commit-all` does not cover this repository | Developer decision | L6 |
| Application | Python ≥ 3.11, FastAPI | `app/main.py`; serves `app.main:app` | `pyproject.toml` | |
| `.cupcake` folder | — | Absent — no project carries one | repository tree | |

## Processes

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| API process | `.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321`, `.env` sourced, from the app folder | Running under the `memory-governor-api` unit | `~/.config/systemd/user/memory-governor-api.service` | |
| Worker process | `.venv/bin/python -m app.worker` | Running under the `memory-governor-worker` unit | `~/.config/systemd/user/memory-governor-worker.service` | |
| Auto-start | — | Two systemd user units, enabled, `Restart=on-failure`, `RestartSec=5` | `~/.config/systemd/user/` unit files | |
| Worker unit PATH | — | Carries the `/home/dev-p/.bun/bin` prefix — the worker shells out to `gbrain`; the API unit needs no prefix | `~/.config/systemd/user/memory-governor-worker.service` | |
| Boot behavior | — | The units own both processes at boot; `scripts/start-memory-system.sh` is a manual fallback | unit files; `scripts/start-memory-system.sh` | |
| Operational status | — | ACTIVE — both units active and enabled; port 8321 held by one listener; unauthenticated requests answer HTTP 422 | live check (reference, Checks) | |

## Database

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Engine | PostgreSQL | Same WSL instance as GBrain's database | `migrations/001_initial_schema.sql` | |
| Database name | `memory_governor` | Distinct from the `gbrain` database | `migrations/001_initial_schema.sql` | |
| Role | — | `memory_governor_svc` — scoped; cannot connect to the `gbrain` database | Developer setup | |
| Tables | `projects`, `memory_candidates`, `policy_versions`, `memory_events`, `audit_log` | Migrations 001–003 applied | `migrations/` | |
| `policy_versions` | Read for active thresholds; an empty table falls back to the built-in limits | Holds no rows — the built-in limits 0.65 and 0.85 apply | `app/policy.py` | |
| `memory_type` column | Plain TEXT, no enum constraint | As standard | `migrations/001_initial_schema.sql` | |
| Registered projects | — | `makepdlf-project-library` and `mb-3-cs-code` are dormant | Developer decision | |
| Concurrency | — | Transactional outbox (`memory_events`) + Postgres `LISTEN`/`NOTIFY`, one dedicated worker; no external message broker | `app/worker.py`; `app/outbox.py` | |

## API surface

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Routes | 11 | 11 — inventory in the reference | `app/api.py` | |
| Contract format | OpenAPI 3.1, generated at `/openapi.json` | As standard | `app/main.py` | |
| NUL-byte guard | Rejects NUL bytes in any path, query or body field | Active on every route | `app/models.py` | |
| Auth gate | Credential required on every route; `writer_identity` derived from the credential, never from the payload | Unauthenticated requests answer HTTP 422 | `app/provenance.py`; `app/api.py` | |
| Network exposure | Localhost bind only | `127.0.0.1:8321` | `~/.config/systemd/user/memory-governor-api.service` | |
| Cupcake allowlist | — | The outbound-network allowlist policy names the governor endpoint `127.0.0.1:8321` | `~/.config/cupcake/policies/opencode/cup-outbound_network_access_is_allowlist_only.rego` — standing policy; see [[[mybizz-config-docs:cupcake/cupcake-config\|cupcake-config]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md), Operational status | |

## Decision engine

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Outcomes | `auto_promote` or `needs_review` only — the engine never closes a candidate out on its own | As standard | `app/policy.py` | |
| Trigger chain | Six triggers, evaluated in order | As standard — the chain is in the reference | `app/policy.py` | |
| High-risk types | `policy`, `credential`, `identity`, `architecture`, `security` | As standard — all five governed | `app/policy.py` | |
| Review threshold | `0.65`, built in — used when `policy_versions` holds no active row | `0.65` — `policy_versions` holds no rows | `app/policy.py` | |
| Auto-promote threshold | `0.85`, built in — same fallback | `0.85` — as above | `app/policy.py` | |
| Contradiction checking | Every candidate, every memory type, no exceptions | As standard | `app/policy.py` | |
| Risk levels | `high` = high-risk type; `medium` = any non-`project_local` visibility or confidence < 0.5; else `low` | As standard | `app/policy.py` | |

## State machine

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Allowed transitions | `proposed → {under_review, promoted, quarantined, rejected, superseded}` · `under_review → {promoted, quarantined, rejected, superseded}` · `promoted → {superseded, expired, quarantined}` · `quarantined → {promoted, rejected, expired}` · `superseded → {expired}` · `rejected`, `expired` terminal | As standard | `app/state_machine.py` | |
| Status writes | `apply_decision()` is the only mutator after creation; `initialize_candidate()` is the only creation entry | As standard | `app/state_machine.py` | |

## GBrain integration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| GBrain version | The installed version governs | 0.59.18.0 | `gbrain` CLI | |
| Write mechanism | `remember` (MEMORY_VERBS) — never `gbrain sync` | As standard | `app/gbrain.py` | |
| Entity stamping | `entity = owning_project` on every fact | As standard | `app/gbrain.py` | |
| Visibility mapping | `shared_all` → world; `project_local` / `shared_specific` → private | As standard | `app/gbrain.py` | |
| Write timing | Asynchronous, via the `gbrain_write` outbox event (~0.15 s) | As standard | `app/worker.py` | |
| Source naming | `GBRAIN_SOURCE` set to the candidate's owning project on every `gbrain remember` call | As standard | `app/gbrain.py` | L1 |
| Where governed facts land | The owning project's own documentation source (federated) | As standard | Developer decision | L1 |
| Brain default after a write | `sources.default` = the write's owning project | As standard | `app/gbrain.py` | L2 |
| MEMORY_VERBS surface | `mcp_surface: verbs` | `verbs` | `gbrain` config | |

## Backup and disaster recovery

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Register location | Inside the repository: `registers/register-memory-governor.md` (index) + `registers/candidates/<memory_id>.json` (full payload per candidate) | As standard | repository tree | |
| Register write | Asynchronous outbox/worker; retries with backoff; surfaces failure after 5 consecutive attempts; the worker git-commits and pushes register changes | As standard | `app/worker.py`; `app/registers.py` | |
| Register contents | Every promoted candidate produces one index row and one full payload file | Index present; 75 payload files | repository tree | |

## Writers

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Manual submission | Through the governor API, via the `mb-submit-memory` suite | Active — distinct per-writer credential | `mb-submit-memory` suite | |
| PDLF step-completion | Through the governor API | Built; PDLF does not call it — credential `pdlf_step_sync` | `app/pdlf_writer.py` | |
| GBrain dream cycle | Not routable through the API | Governed by the manual discipline — real `dream`, then `gbrain eval suspected-contradictions`, then review | [[[mybizz-config-docs:memory-governor/memory-governor-learnings\|Learnings]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-learnings.md) L4 | |

## Open items

None.
