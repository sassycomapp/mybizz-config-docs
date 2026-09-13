---
document: "Memory Governor — Exam Report"
doc-id: memory-governor-exam-report
state: Live
date-created: 2026-09-13
---

# Memory Governor — Exam Report

Run #1 — **first formal plan-driven exam** (2026-09-13). Plan:
`memory-governor-exam-plan.md` (bootstrap run — no prior report; step-0: 7 suite
files present, skill installed+hash-matched `4f5df4779a6d4597`, spec present).
Detection only — Tiers 0–2; Tier 3 locked. Scope boundary honored (DB
conformance cross-referenced from postgres run #2).

## Verdict: HEALTHY + FLAGS — system live and conformant; worker write-pipeline carries unresolved historical failures (finding 3)

## Tier 0 — Liveness: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| M0-1 | API process | uvicorn 8321, documented command | PID 312, exact command match | PASS |
| M0-2 | Worker process | `python -m app.worker` | PID 315, exact | PASS |
| M0-3 | Port 8321 | LISTEN 127.0.0.1 | LISTEN | PASS |
| M0-4 | HTTP auth-gate | **422** unauthenticated | **422 observed** — gate closed + API alive in one probe | PASS |

## Tier 1 — Health: PASS with finding 3

| ID | Check | Result |
|---|---|---|
| M1-1 | Repo integrity: working tree **clean** (worker auto-commits registers as designed); HEAD `d31642f` | PASS |
| M1-2 | Venv present + executable | PASS |
| M1-3 | DB quick sanity: projects 3, candidates 5, events 7, audit 5, policy 0 — **exact match to last recorded** | PASS |
| M1-4 | Register correspondence: 18 payload files ↔ 18 index data rows (1:1) | PASS |
| M1-5 | Log/error scan — **finding 3**: API log 0 errors; worker log carries 5 unresolved first-attempt failures (git ops exit 128 via stale lock + `FileNotFoundError: 'gbrain'`), **zero retry attempts logged beyond 1/5**, and **the worker log has no timestamps** | FLAG |

## Tier 2 — State conformance: PASS with finding 2

| ID | Expected | Actual | Result |
|---|---|---|---|
| M2-1 | 0.1.0 | 0.1.0 (pyproject) | PASS |
| M2-2 | Two-outcome model | `auto_promote`/`needs_review` in source (api.py) | PASS |
| M2-3 | 5 high-risk types | frozenset verified in `app/policy.py`: policy, credential, identity, architecture, security | PASS |
| M2-4 | Thresholds 0.65 / 0.85 | `REVIEW_THRESHOLD = 0.65`, `AUTO_PROMOTE_THRESHOLD = 0.85` (policy.py) | PASS |
| M2-5 | 12 routes + NUL guard | **11 routes in source** (matches the spec's own 11-row table — the spec's section header says 12: internal inconsistency); NUL guard **present** (`reject_nul_bytes_in_path_and_query`, api.py:95, raises 400) | DRIFT (spec-internal) |
| M2-6 | systemd units absent (pending) | absent | PASS |
| M2-7 | Credentialed registry check | developer-run (request issued) | DEFERRED |

## Findings

1. **Spec-internal inconsistency (M2-5).** The spec's API-surface header claims
   "12 routes"; its own table lists **11**; live source shows **11**. The table
   and reality agree; the header count is wrong. → docs governance (one-word fix).
2. **Worker observability gap (new learning).** The worker log has **no
   timestamps**, and retry warnings show only "attempt 1/5" with no resolution
   lines — the fate of failed events cannot be determined from the log alone.
   → learning filed; destination: skill Tier 1 note + a developer-decision item
   (add timestamps to worker logging — a code change, gated).
3. **Unresolved worker write failures — RESOLVED during the run (2026-09-13).**
   Events 3802–3806 failed attempt 1/5 (git ops exit 128 via a stale lock, since
   cleared; `FileNotFoundError: 'gbrain'` — worker PATH). Investigation: the
   outbox now holds **zero unprocessed events** and **no rows with IDs ≥ 3802**
   — the outbox deletes on delivery, so those events were ultimately
   **delivered and purged**, not lost. The stale-lock condition is gone (clean
   tree). Remaining uncertainty: whether the boot-spawned worker's PATH includes
   `~/.bun/bin` for **future** gbrain writes — `/proc` environ read is
   guard-blocked for agents → developer PATH check (bundle item 1).
   Class downgraded: UNHEALTHY-leaning → resolved-with-follow-up.
4. **M0-4 doctrine validated:** the 422 probe (auth-gate closed + API alive)
   worked exactly as designed — one request, two facts.

## Guard layers

One guard denial this run (`/proc/<pid>/environ` read — critical system path) —
honored, rerouted to the developer bundle.

## Developer-run request (bundled)

1. **Worker PATH check:** `cat /proc/<worker-pid>/environ | tr '\0' '\n' | grep PATH` — does it include `/home/dev-p/.bun/bin`?
2. **M3-1 + M2-7 full test suite** (requires the env the 2026-09-08 run had):
   `cd /home/dev-p/memory-governor && set -a && source .env && set +a && .venv/bin/python -m pytest -q` — expect 304 passed, 0 failed; also covers the credentialed registry check
3. **Timestamps decision:** should worker logging gain timestamps? (code change, gated)

## Not run this cycle

Tier 3 (locked): M3-1 suite (→ developer, above), M3-2 auto-start execution,
M3-3 recovery drill. M3-4 repo push state: **already satisfied** — `main` in
sync with `origin/main` (HEAD d31642f).