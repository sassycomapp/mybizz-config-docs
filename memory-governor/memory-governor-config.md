---
title: "memory-governor-config"
doc-id: "mb-63bdf286"
updated: "2026-10-05"
---
# Memory Governor Configuration

Canonical current-state configuration record. Agent-facing. Reflects the
verified live state as of 2026-09-08 (system ACTIVE, all listed defects
resolved) and re-verified 2026-09-30 after the GBrain upgrade (see
§GBrain upgrade verification). States facts, not history — reasoning in
[[[mybizz-config-docs:memory-governor/memory-governor-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-explainer.md); procedures in [[[mybizz-config-docs:memory-governor/memory-governor-reference|Usage, Invocation, and Incident Response]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md).

---

## Identity

| Item | Value |
|---|---|
| Repository | `github.com/sassycomapp/memory-governor` (local clone `/home/dev-p/memory-governor`, WSL-native — do not relocate) |
| Application | FastAPI (Python), `app/main.py`, version `0.1.0` (pyproject) |
| Decision engine | Two-outcome model (`auto_promote` / `needs_review`) — live since Phase 6.5, commit `c4df67d` |
| HIGH_RISK_TYPES | **RESOLVED 2026-09-08** (developer decision): `policy`, `credential`, `identity`, `architecture`, `security` — all five spec categories are now representable (`MemoryType` enum extended) and governed |
| Test suite | **304 passed, 0 failed** (2026-09-08, post-resolution run; build record was 296); not re-run after the GBrain upgrade of 2026-09-30 or after the change to `app/gbrain.py` of 2026-10-01 — see Pending developer execution item 7 |
| Operational status | **ACTIVE** — API + worker both running under their systemd user units (permanent auto-start executed + verified 2026-09-15; boot-command retirement decided 2026-09-28 — see Pending developer execution item 4) |

## Processes (two, by design)

| Process | Command | State 2026-09-08 |
|---|---|---|
| API | `.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321` (from the app folder, with `.env` sourced) | Running (detached, log-verified; auth-gates unauthenticated calls — HTTP 422 observed live) |
| Worker | `.venv/bin/python -m app.worker` (persistent LISTEN loop; NOTIFY wake + 60s poll safety net) | Running — **first persistent run in the system's history** (an entry-point defect prevented this before 2026-09-08; fixed same day) |

Both must run for the system to function: the API decides, the worker
delivers (GBrain writes + register/payload writes). Start procedure in
[[[mybizz-config-docs:memory-governor/memory-governor-reference|Usage, Invocation, and Incident Response]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md). Permanent auto-start: two systemd user
units (`memory-governor-api`, `memory-governor-worker`) — enabled + verified
2026-09-15. Boot-command retirement (2026-09-28): the `[boot]` command no
longer invokes `start-memory-system.sh` — the units own both processes;
the script remains a manual fallback only.

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
| Source switching | `gbrain sources default <owning_project>` before every write — fails loudly on an unknown source (the coupling defect guard). The write itself names the owning project's source (`GBRAIN_SOURCE` on the `gbrain remember` call), so the fact lands in that source whatever folder the worker runs in |
| Where governed facts land | The owning project's own documentation source (federated). A fact written before 2026-10-01 may still sit in `memory-governor-code` |
| Code of the write | `app/gbrain.py`, `remember_candidate`: the `gbrain remember` call runs with the environment variable `GBRAIN_SOURCE` set to the candidate's owning project (changed 2026-10-01; the original is saved as `~/backups/gbrain.py.before-source-fix`) |
| Brain default after a write | `sources.default` = the last owning project (`mybizz-os-docs` on 2026-09-30). A default that names a deleted source stops `gbrain sync` under 0.59.18.0 — see the reference, incident 2026-09-30 |
| GBrain version | 0.59.18.0, schema 169 (upgraded 2026-09-30 from 0.46.1.0). `remember`, `recall`, `forget`: no input removed, none newly required. New optional inputs: `source_id`, `expected_revision`, `force`, `request_id` (`remember`); `source_id`, `budget_policy` (`recall`); `request_id` (`forget`) |
| MEMORY_VERBS surface | Enabled (`mcp_surface: verbs`, verified 2026-09-08; still `verbs` on 2026-09-30) |

## GBrain upgrade verification — 2026-09-30 (0.46.1.0 → 0.59.18.0, schema 128 → 169)

| Item | Value |
|---|---|
| Services after the upgrade | `memory-governor-api` and `memory-governor-worker` both active; port 8321 held by one listener; unauthenticated `GET /memory/review-queue` answers 422; the worker unit still carries the `~/.bun/bin` PATH line |
| Stop and start order used | API stopped first, 60 seconds wait so the worker delivers what is already promoted, then the worker; started together with `systemctl --user start` |
| Facts before and after | 85 facts in 5 sources, none missing: `memory-governor-code` 49, `mybizz-config-docs` 22, `default` 12, `makepdlf-project-library` 1, `mb-3-cs-code` 1. Every other source holds none |
| Governed write, end to end | `/mb-submit-memory` on `environment-explainer.md` (source `mybizz-os-docs`) → `promoted`, memory_id `2cb82774-957c-4772-be3e-8d421f030c4a`; that fact landed in `memory-governor-code` (49 → 50), before the change of 2026-10-01 |
| Worker's source step | `gbrain sources default mybizz-os-docs` succeeded under 0.59.18.0; `sources.default` printed `mybizz-os-docs` afterwards |
| Interface comparison | 114 agent tools present in both versions: no input removed, none newly required (names and inputs only — behavior was not compared) |
| Database dump before the upgrade | `~/backups/db-memory_governor-before-upgrade.dump` (readable, 2026-09-30) |
| Not verified | The full test suite was not re-run. The scripts/run-tests-deterministic.sh runner was not executed (see the reference) |

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
- **Governed facts land in the owning project's own documentation source** (since 2026-10-01; before that they landed in `memory-governor-code`). A search from a documentation session sees them. The isolation between projects is enforced by the governor (entity stamping, visibility mapping, read-time resolution), not by GBrain's sources.
- **The brain-level default source is changed by every governed write.** A default that names a source that no longer exists stops `gbrain sync` under 0.59.18.0 (incident 2026-09-30: `diag-mg-sec4`).
- **`scripts/run-tests-deterministic.sh` is not aware of the systemd units.** It stops the worker with `kill` and afterwards starts an unmanaged copy, which leaves the unit stopped.

## Do not

- Do not assume GBrain dreaming's output passes through the governor's review queue — it never does under the current design.
- Do not treat Phase 13.4/16.2/16.3 as failed builds — deliberately parked, real infrastructure.
- Do not call `gbrain sync` to move governed content into GBrain — only `remember` via the governor's async path counts as governed.
- Do not chain shell commands without verifying each result — the recorded real cost of this mistake is an accidental write into live memory.
- Do not assume test fixtures are shared across test files — `api_client`/`real_credential_headers` exist only in `test_api.py`.
- Do not hand-edit `registers/` or the database — the worker and API are the writers.
- Do not run `scripts/run-tests-deterministic.sh` while `memory-governor-worker.service` is active — it would leave an unmanaged second worker (procedure in the reference).
- Do not leave `sources.default` naming a source that does not exist.

## Pending developer execution (commands provided in the run record; not defects)

1. Outbound-network rule + cross-folder rule formal eval tests + keep decisions (both amendments already live and one real-call-verified each).
2. Credentialed registry/review-queue check (closes the governor-side `owning_project` verification).
3. Commit + push of the governor repository's resolution changes.
4. ~~Permanent auto-start: WSL systemd migration + the two service units~~ **EXECUTED + VERIFIED 2026-09-15 (session 005):** systemd enabled (`systemd=true` under `[boot]`, boot command preserved — PostgreSQL auto-started); both units enabled and active under the user manager (`memory-governor-api`, `memory-governor-worker`, Restart=on-failure); auth-gate 422; port 8321 held by the service. The system is restart-independent. (At the migration boot the boot script started the API but not the worker. The expected idempotent skip never materialized: at BOTH 2026-09-28 boots the boot script's API won the port-8321 bind race and the api unit crash-looped until the duplicate was killed — full boot-command retirement decided 2026-09-28, see [[[mybizz-config-docs:memory-governor/memory-governor-reference|Reference]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-reference.md) §Permanent auto-start migration.)
5. gbrain sync of the documentation commits.
6. Where governed facts live — decided 2026-10-01: in the owning project's own documentation source. The worker's `remember` call names it. Done.
7. Re-run the full test suite after the GBrain upgrade and the `app/gbrain.py` change of 2026-10-01 (stop the systemd worker first — procedure in the reference).
8. Commit the `app/gbrain.py` change in the governor's own repository: `cd /home/dev-p/memory-governor && git add app/gbrain.py && git commit -m "The governed write names the owning project's source"`. Developer-run: agents never use Git.
```
