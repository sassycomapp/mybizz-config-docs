# Memory Governor Configuration

Canonical current-state configuration record. Agent-facing. Reflects the working
state of Memory Governor as of the close of its own build sequence, 2026-08-25.
This document states facts, not history — where a decision was made and the
reasoning matters, see `memory-governor-explainer.md`.

---

## Identity

| Item | Value |
|---|---|
| Repository | `github.com/sassycomapp/memory-governor` |
| Application | FastAPI (Python), `app/main.py` |
| Decision engine version | Two-outcome model (Architecture §2.2) — live since Phase 6.5, commit `c4df67d` |
| Full test suite (final confirmed count) | 296 passed |
| Build status | Phases 0–15 fully closed. Phase 16 (Cutover) closed for the two writers that can be governed; Steps 16.2/16.3 explicitly parked pending PDLF go-live. No remaining application code to write in this repository. |

## Database

| Item | Value |
|---|---|
| Engine | PostgreSQL — same instance as GBrain's database |
| Database name | Dedicated, distinct from `gbrain` |
| Role | `memory_governor_svc` — scoped; cannot connect to the `gbrain` database |
| Tables | `projects`, `memory_candidates`, `policy_versions`, `memory_events` |
| Concurrency mechanism | Transactional outbox (`memory_events`) + Postgres `LISTEN`/`NOTIFY`, one dedicated worker process. No external message broker. |

## Real writers (confirmed)

| Writer | Routes through governor API? | Credential |
|---|---|---|
| Manual submission, via `mb-submit-memory` | Yes | Distinct, per-writer credential |
| PDLF step-completion | Yes | `pdlf_step_sync` — distinct from the other two |
| GBrain dream cycle | **No — structurally impossible.** See Known Scope Limitations below. | N/A for governor API purposes |

## Permanent exception — sources that bypass the governor entirely

**`anvil-agent-references`, and any future update to it, is synced into
GBrain the ordinary way (`gbrain sync`), never submitted through the
governor's API.** This is official, direct-from-Anvil reference
material — a dictionary does not need to be fact-checked against
itself; there is no genuine confidence or contradiction question to
ask about it. This is a permanent, standing rule for this source, not
a one-time exception for its initial install. Ordinary syncing keeping
this source current remains the developer's own responsibility.

## API surface (real endpoints)

| Method & Path | Purpose |
|---|---|
| `POST /memory/candidate` | Submit a candidate — inline content or a `provenance.source_ref` path |
| `GET /memory/{memory_id}` | Fetch a candidate |
| `GET /memory` | List candidates, filterable by project/status/type |
| `GET /memory/review-queue` | All candidates currently `under_review` |
| `POST /memory/{memory_id}/review` | Record a human decision: promote / quarantine / reject |
| `POST /memory/{memory_id}/supersede` | Supersede with a new record; atomically sets `valid_until` on the old one |
| `GET /memory/{memory_id}/provenance` | Full audit/decision history |
| `POST /memory/quarantine` | Manual quarantine of an existing candidate |
| `POST /memory/projects` | Register a new PDLF project |
| `PATCH /memory/projects/{project_id}` | Toggle a project's `dormant` flag |
| `POST /memory/policy` | Propose a new policy version — always routes through the standard `high_risk_types` pipeline |

Contract format: OpenAPI 3.1, generated live from the running application at `/openapi.json` — never a hand-maintained spec file.

## Decision engine — real, current logic

`decide_path()` returns exactly one of two automatic outcomes: `auto_promote` or `needs_review`. It never returns `reject` or `quarantine` as its own decision — confirmed both by source inspection and by live behavior across every trigger condition, and by permanent regression tests that assert no case returns either automatically.

**High-risk types** (force `needs_review` unconditionally): `policy`, `credential`, `identity`, `architecture`, `security`. A `shared_with` change adding or removing a project is also automatically high-risk.

**Contradiction handling** applies to every memory type, with no exceptions. A cross-project contradiction always forces `needs_review`, regardless of confidence score.

## GBrain integration

| Item | Value |
|---|---|
| Write mechanism | `remember` (MEMORY_VERBS), not `gbrain sync` — confirmed deliberate; sync would ingest raw content regardless of governor approval |
| Write timing | Asynchronous, via the `gbrain_write` outbox event — confirmed ~0.15s in practice, not a meaningful delay |
| `MEMORY_VERBS` MCP surface | Enabled (`mcp_surface: verbs`) — a real, resolved prerequisite (Step 0.2) |

## Backup / disaster recovery

| Item | Value |
|---|---|
| Register location | Inside this repository, `registers/` — not a separate external location |
| Register files | `register-memory-governor.md` (candidate index), `register-memory-governor-policy.md` (policy version index) |
| Payload files | `registers/candidates/<memory_id>.json` — full candidate, every field |
| Write mechanism | Asynchronous, via the same outbox/worker as GBrain writes; retries with backoff, surfaces failure after 5 consecutive attempts rather than retrying forever |
| Recovery proven | Twice — an isolated drill (Phase 7.5) and a full-system drill including GBrain writes (Phase 15.2), both confirming exact reconstruction from the register/payload store alone |

## Known scope limitations (accepted, not defects)

- **GBrain's dream cycle cannot be routed through the governor's API — a confirmed, permanent structural limit, not an oversight.** Exhaustive investigation found no interception point of any kind in GBrain's `dream` command. Governed instead by a manual, always-applied discipline: run `dream` for real, run `gbrain eval suspected-contradictions` immediately afterward (confirmed not automatic), review the findings. This is the one honestly-documented exception to "every writer routes through the same API."
- **Phase 13, Step 13.4 (a real PDLF step running end-to-end through the governor) is explicitly parked, not completed** — requires real PDLF activity that cannot exist before PDLF's own go-live. A synthetic substitute was considered and deliberately rejected as less honest.
- **Phase 16, Steps 16.2–16.3 (observation period and formal go-live confirmation for the dreaming discipline) are explicitly parked for the same reason** — require real, repeated dream cycles under ordinary PDLF use.
- **A `GBrain-dreaming` credential may exist from early provisioning (Step 0.3) but is functionally unused** — since dreaming cannot call the governor's API at all, no credential for it is ever actually presented in a real request.

## Do not

- Do not assume GBrain dreaming's output passes through the governor's review queue — it never does, and never will under the current design; see Known Scope Limitations.
- Do not treat `Phase 13.4`/`16.2`/`16.3` as failed or incomplete builds — they are deliberately parked, real, working infrastructure with nothing left to build, waiting only on real PDLF activity that doesn't yet exist.
- Do not call `gbrain sync` to move governed content into GBrain — only `remember`, via the governor's own async write path, actually counts as governed.
- Do not chain multiple shell commands together without verifying each one's real result before the next runs — see `memory-governor-reference.md`'s incident-response procedure for the real, confirmed cost of skipping this.
- Do not assume a fixture defined in one test file (e.g. `api_client`, `real_credential_headers` in `test_api.py`) is available in another — confirmed, repeated real mistake; build the client and credential inline in any new test file outside `test_api.py`.

## Local installation & infrastructure — verified 2026-09-05

Confirmed directly against the live system, not from memory or prior docs — recorded
here so this investigation never has to be repeated.

| Item | Value |
|---|---|
| Local clone | `/home/dev-p/memory-governor` — **WSL-native**, deliberately NOT under `C:\dev\`. This is the only project source in this shape; do not relocate it and do not "correct" it to match the `C:\dev\dev-{project}\` convention used elsewhere. |
| Git remote | Confirmed `origin` = `https://github.com/sassycomapp/memory-governor.git` — matches the Identity table above exactly. |
| Local folder contents | Real, active dev environment: `.venv`, `.env`, `app/`, `docs/`, `migrations/`, `registers/`, `scripts/`, `tests/`, plus `.pytest_cache`/`.hypothesis`/`.schemathesis` test-tool caches. Not a stub or abandoned clone. |
| Database, live-checked | `memory_governor` database confirmed present via `psql \l`, owned by `memory_governor_svc`. All 5 documented tables present (`projects`, `memory_candidates`, `policy_versions`, `memory_events`, `audit_log`). `memory_candidates` holds **5 real rows** as of this check — not an empty schema. |
| Process status at check time | No `uvicorn`/`memory-governor` process running (`ps aux` clean). Not currently live, but see log evidence below that it has run successfully. |
| `/tmp/memory-governor.log` | Shows a genuine successful run: clean Uvicorn startup on `127.0.0.1:8321`, followed by two real successful calls — `POST /memory/projects` → 201, `POST /memory/candidate` → 201. Confirms the governed-write path has actually executed end-to-end, not just been built. |
| `mb-submit-memory` skill usage | Confirmed genuinely invoked, not just installed: real log entries at `/mnt/c/mybizz/logs/mb-submit-memory/` — `2026-08-27T060743+0200.md` and `learnings.md`, both real files with content. |
| Canonical docs (this file + reference + explainer) | Now live at `C:\mybizz\mybizz-config-docs\memory-governor\` — part of the `mybizz-config-docs` GBrain source once that source is registered. The `Retired-memory-governor-agent/` subfolder alongside them (51 files: `Step 0` through `Step 16.1`, plus the three `memory-governor-agent-*` planning docs) is the genuinely retired step-by-step build log — historical record, correctly retired, not an open item. |

**GBrain source decision: add one.** Recommended — `memory-governor-code` → `/home/dev-p/memory-governor` (WSL-native path). Rationale: this is a real, actively-built application (296 tests, weeks of work, live DB with real rows) with no GBrain source at all right now. Every comparably real project (`mb-3-cs`, `mb4ecom`, `mb5pdlf`) has a matching `-code` source alongside its docs source — this should follow the same pattern. Not yet actioned as of this writing; register when ready.
