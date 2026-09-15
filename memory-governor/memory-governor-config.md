---
document: "Memory Governor Configuration"
doc-id: memory-governor-config
state: Live
date-created: 2026-09-05
---

# Memory Governor Configuration

Canonical current-state configuration record. Agent-facing. Reflects the
verified live state as of 2026-09-08 (system ACTIVE, all listed defects
resolved). States facts, not history — reasoning in
`memory-governor-explainer.md`; procedures in `memory-governor-reference.md`.

---

## Identity

| Item | Value |
|---|---|
| Repository | `github.com/sassycomapp/memory-governor` (local clone `/home/dev-p/memory-governor`, WSL-native — do not relocate) |
| Application | FastAPI (Python), `app/main.py`, version `0.1.0` (pyproject) |
| Decision engine | Two-outcome model (`auto_promote` / `needs_review`) — live since Phase 6.5, commit `c4df67d` |
| HIGH_RISK_TYPES | **RESOLVED 2026-09-08** (developer decision): `policy`, `credential`, `identity`, `architecture`, `security` — all five spec categories are now representable (`MemoryType` enum extended) and governed |
| Test suite | **304 passed, 0 failed** (2026-09-08, post-resolution run; build record was 296) |
| Operational status | **ACTIVE** — API + worker both running since 2026-09-08 (started on demand; permanent auto-start approved, pending developer execution — see Pending developer execution) |

## Processes (two, by design)

| Process | Command | State 2026-09-08 |
|---|---|---|
| API | `.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321` (from the app folder, with `.env` sourced) | Running (detached, log-verified; auth-gates unauthenticated calls — HTTP 422 observed live) |
| Worker | `.venv/bin/python -m app.worker` (persistent LISTEN loop; NOTIFY wake + 60s poll safety net) | Running — **first persistent run in the system's history** (an entry-point defect prevented this before 2026-09-08; fixed same day) |

Both must run for the system to function: the API decides, the worker
delivers (GBrain writes + register/payload writes). Start procedure in
`memory-governor-reference.md`. Permanent auto-start: two systemd user
units (`memory-governor-api`, `memory-governor-worker`) — command sequence
provided, pending developer execution.

## Database

| Item | Value |
|---|---|
| Engine | PostgreSQL — same WSL instance as GBrain's database (verified up 2026-09-08) |
| Database name | `memory_governor` — distinct from `gbrain` |
| Role | `memory_governor_svc` — scoped; cannot connect to the `gbrain` database |
| Tables | `projects`, `memory_candidates`, `policy_versions`, `memory_events`, `audit_log` (migrations 001–003). Row counts are **live and drift continuously** (worker/API write continuously) — point-in-time at verification: projects 3, candidates 5, events 7, audit 5, policy 0 (2026-09-13); exams compare growth explainability, never exact equality |
| `memory_type` column | Plain TEXT — no enum constraint (this is why the MemoryType enum extension needed **no migration**) |
| Concurrency mechanism | Transactional outbox (`memory_events`) + Postgres `LISTEN`/`NOTIFY`, one dedicated worker process. No external message broker. |

## Resolution record — 2026-09-08 (all verified by the full test suite)

| Defect resolved | Fix |
|---|---|
| HIGH_RISK_TYPES spec inconsistency (only `policy` was representable; four spec categories were unimplementable) | `MemoryType` enum extended with `credential`, `identity`, `architecture`, `security`; `HIGH_RISK_TYPES` now covers all five spec categories; tests added — the architectural intent is now truly implemented |
| Project-isolation defect (every governed memory was written **world-visible** regardless of declared scope — caught by the system's own Step 12.2 isolation test) | Visibility mapping: `shared_all` → world; `project_local` / `shared_specific` → private. Project-local memories are no longer world-readable |
| Facts carried no project identity (project-scoped recall impossible) | Every governed fact is now stamped with `entity = owning_project` — entity-scoped recall is the project-scoped read |
| Worker had no production entry point (the documented "dedicated worker process" was unstartable outside tests) | `python -m app.worker` entry point added; worker running |
| Two world-visible test-marker facts polluting the live brain (today's + 2026-08-25's runs) | Both expired via `forget` with full audit-trail reasons; the test now expires its own facts in its cleanup |

## Real writers (confirmed)

| Writer | Routes through governor API? | Credential |
|---|---|---|
| Manual submission, via `mb-submit-memory` | Yes | Distinct, per-writer credential |
| PDLF step-completion | Yes | `pdlf_step_sync` — distinct from the other two |
| GBrain dream cycle | **No — structurally impossible** (permanent; governed by the documented manual discipline: run `dream` for real, then `gbrain eval suspected-contradictions`, review) | N/A |

## Permanent exception — sources that bypass the governor entirely

**`anvil-agent-references`, and any future update to it, is synced into
GBrain the ordinary way (`gbrain sync`), never submitted through the
governor's API.** Official, direct-from-Anvil reference material — a
dictionary does not need to be fact-checked against itself. Permanent,
standing rule. Ordinary syncing of this source remains the developer's
own responsibility.

## API surface (verified from source, **11 routes** — header corrected 2026-09-13: the previous "12" was a spec-internal error; the table and live source both count 11)

| Method & Path | Purpose |
|---|---|
| `POST /memory/candidate` | Submit a candidate — inline content or a `provenance.source_ref` path |
| `GET /memory/{memory_id}` | Fetch a candidate |
| `GET /memory` | List candidates, filterable by project/status/type |
| `GET /memory/review-queue` | All candidates currently `under_review`, each with its ReviewPresentation |
| `POST /memory/{memory_id}/review` | Record a human decision: promote / quarantine / reject |
| `POST /memory/{memory_id}/supersede` | Supersede with a new record; atomically sets `valid_until` on the old one |
| `GET /memory/{memory_id}/provenance` | Full audit/decision history |
| `POST /memory/quarantine` | Manual quarantine of an existing candidate |
| `POST /memory/projects` | Register a new project |
| `PATCH /memory/projects/{project_id}` | Toggle a project's `dormant` flag |
| `POST /memory/policy` | Propose a new policy version — routes through the standard high-risk pipeline |

A global guard rejects NUL bytes in any path or query parameter, on every
route. Contract format: OpenAPI 3.1, generated live at `/openapi.json`.

## Decision engine — real, current logic (source-verified)

`decide_path()` evaluates, in order, and returns `auto_promote` only if
nothing triggers:

| Order | Trigger | Classification | Recommended action |
|---|---|---|---|
| 1 | Provenance check fails (writer identity not server-verified) | `provenance_failure` | reject |
| 2 | Scope invalid (`visibility`/`shared_with` inconsistent) | `scope_invalid` | quarantine |
| 3 | Unresolved contradiction (cross-project, or no resolution, or `manual_review`) | `unresolved_contradiction` | none — never auto-decided |
| 4 | Memory type in the five high-risk categories | `high_risk_type` | none |
| 5 | Confidence below the review threshold (default 0.65) | `low_confidence` | none |
| 6 | Medium risk (any sharing, or confidence < 0.5) with confidence below the auto-promote threshold (default 0.85) | `medium_risk_moderate_confidence` | none |
| — | Nothing triggered | — | `auto_promote` |

Thresholds are read live from the active `policy_versions` row (bootstrap
defaults 0.65 / 0.85) — policy changes are data changes, not code changes.
Contradiction checking runs for every candidate, every type, no exceptions.
Risk levels: `high` = high-risk type; `medium` = any non-`project_local`
visibility or confidence < 0.5; else `low`.

## State machine (source-verified; code authoritative)

`proposed → {under_review, promoted, quarantined, rejected, superseded}` ·
`under_review → {promoted, quarantined, rejected, superseded}` ·
`promoted → {superseded, expired, quarantined}` ·
`quarantined → {promoted, rejected, expired}` ·
`rejected` terminal · `superseded → {expired}` · `expired` terminal.
Every write path goes through transition validation — creation included.

## GBrain integration

| Item | Value |
|---|---|
| Write mechanism | `remember` (MEMORY_VERBS) — never `gbrain sync`; each fact stamped `entity = owning_project` |
| Visibility mapping | `shared_all` → world; `project_local` / `shared_specific` → private |
| Write timing | Asynchronous, via the `gbrain_write` outbox event — ~0.15s in practice |
| Source switching | `gbrain sources default <owning_project>` before every write — fails loudly on an unknown source (the coupling defect guard) |
| MEMORY_VERBS surface | Enabled (`mcp_surface: verbs`, verified 2026-09-08) |

## Backup / disaster recovery

| Item | Value |
|---|---|
| Register location | Inside this repository, `registers/` — `register-memory-governor.md` (candidate index) + `registers/candidates/<memory_id>.json` (full payload per candidate) |
| Write mechanism | Asynchronous outbox/worker; retries with backoff; surfaces failure after 5 consecutive attempts. The worker git-commits AND pushes register changes |
| Register integrity | Index rows correspond to real payload files (verified 2026-09-08); real promoted candidates present, including a supersession pair |
| Recovery proven | Twice — Phase 7.5 isolated drill and Phase 15.2 full-system drill |

## Known scope limitations (honest, structural)

- **GBrain's dream cycle cannot be routed through the governor's API** — confirmed permanent structural limit (no interception point in GBrain's `dream`; forking GBrain was considered and rejected). Governed by the documented manual discipline. This is the one honestly-documented exception to "every writer routes through the same API" — an architectural boundary of the third-party tool, reported as such per the standing no-discrepancies requirement.
- **Phase 13.4 / 16.2 / 16.3 are explicitly parked** (a real PDLF step end-to-end; repeated real dream cycles under ordinary use) — they require real PDLF activity that cannot exist before PDLF's go-live. Deliberately parked working infrastructure, not incomplete builds. Reported separately, per the no-open-defects requirement, as scheduled-pending-external-dependency, not defects.
- **A `GBrain-dreaming` credential may exist from early provisioning but is functionally unused** — dreaming never presents a credential.

## Do not

- Do not assume GBrain dreaming's output passes through the governor's review queue — it never does under the current design.
- Do not treat Phase 13.4/16.2/16.3 as failed builds — deliberately parked, real infrastructure.
- Do not call `gbrain sync` to move governed content into GBrain — only `remember` via the governor's async path counts as governed.
- Do not chain shell commands without verifying each result — the recorded real cost of this mistake is an accidental write into live memory.
- Do not assume test fixtures are shared across test files — `api_client`/`real_credential_headers` exist only in `test_api.py`.
- Do not hand-edit `registers/` or the database — the worker and API are the writers.

## Pending developer execution (commands provided in the run record; not defects)

1. Outbound-network rule + cross-folder rule formal eval tests + keep decisions (both amendments already live and one real-call-verified each).
2. Credentialed registry/review-queue check (closes the governor-side `owning_project` verification).
3. Commit + push of the governor repository's resolution changes.
4. ~~Permanent auto-start: WSL systemd migration + the two service units~~ **EXECUTED + VERIFIED 2026-09-15 (session 005):** systemd enabled (`systemd=true` under `[boot]`, boot command preserved — PostgreSQL auto-started); both units enabled and active under the user manager (`memory-governor-api`, `memory-governor-worker`, Restart=on-failure); auth-gate 422; port 8321 held by the service. The system is restart-independent. (At the migration boot the boot script started the API but not the worker — the units now guarantee both; the script's idempotent skip is standing-check territory.)
5. gbrain sync of the documentation commits.
```
