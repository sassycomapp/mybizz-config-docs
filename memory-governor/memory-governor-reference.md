---
title: "memory-governor-reference"
doc-id: "mb-38660a2f"
updated: "2026-10-02"
---
# Memory Governor Reference — Usage, Invocation, and Incident Response

Companion to [[[mybizz-config-docs:memory-governor/memory-governor-config|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) (the spec — current state — ACTIVE, all
defects resolved 2026-09-08) and [[[mybizz-config-docs:memory-governor/memory-governor-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-explainer.md) (the
authoritative whole-system narrative — design, mechanics, and real incidents).
Exam companions: [[[mybizz-config-docs:memory-governor/memory-governor-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-exam-plan.md) (next run's job-spec),
[[[mybizz-config-docs:memory-governor/memory-governor-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-exam-report.md) (current verified state),
[[[mybizz-config-docs:memory-governor/memory-governor-log|Log]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-log.md) (notable events), [[[mybizz-config-docs:memory-governor/memory-governor-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-learnings.md)
(transient exam knowledge). The architecture standard:
[[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md). Agent-facing.

---

## Running the test suite — deterministically (use this, not bare pytest)

**Never run bare `pytest` while the worker is live** — the suite inserts events into the live outbox and the worker (NOTIFY wake + 60s poll) races the tests, producing timing-dependent failures (observed 2026-09-13: 2 failures, both traced to the worker consuming test events mid-assertion). Use the deterministic runner:

```bash
/home/dev-p/memory-governor/scripts/run-tests-deterministic.sh
```

It gracefully pauses the worker (kill by PID — the documented safe method), runs the full suite with the environment loaded, and **always** restarts the worker afterwards (trap, even on failure). Extra pytest arguments pass through (e.g. `... -k test_name`). Bare `pytest` is acceptable only when the worker is not running.

**Since the systemd units (2026-09-15) this runner is not systemd-aware — do not run it while `memory-governor-worker.service` is active.** It stops the worker with `kill`, and afterwards starts a plain unmanaged worker. The unit then stays stopped, and a later `systemctl --user start` would run a second worker beside the unmanaged one. Recommended procedure (read from the script on 2026-09-30, **not yet exercised**):

```bash
systemctl --user stop memory-governor-worker
cd /home/dev-p/memory-governor && set -a && source .env && set +a && .venv/bin/python -m pytest -q
systemctl --user start memory-governor-worker
gbrain config get sources.default
```

The suite writes test facts into the live brain and expires them itself. Afterwards `sources.default` must name a source that exists (see the incident of 2026-09-30 below).

## Starting and stopping the system (two processes, both required)

Start (from the app folder, `.env` sourced first — no dotenv autoload):

```bash
cd /home/dev-p/memory-governor && set -a && source .env && set +a
setsid .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321 >> /tmp/memory-governor.log 2>&1 < /dev/null &
PATH="$HOME/.bun/bin:$PATH" setsid .venv/bin/python -m app.worker >> /tmp/memory-governor-worker.log 2>&1 < /dev/null &
```

- **The worker's PATH prefix (`~/.bun/bin`) is mandatory** (proven 2026-09-14):
  without it the worker cannot invoke `gbrain` and every delivery fails
  permanently (`FileNotFoundError: 'gbrain'` after 5 attempts — event 4259).
  The API does not need the prefix (it never shells out to gbrain).
- `setsid` + full redirection is required: a plain `nohup &` child dies
  when the launching shell's process group is terminated (confirmed live).
- **Both processes are required.** The API decides; the worker delivers
  (GBrain writes + register/payload The use of registers has been discontinued. Please review writes). An API without a worker means
  promoted candidates silently never leave the outbox.
- Health checks: `ss -tlnp | grep 8321` (API listening); `ps aux | grep
  app.worker` (worker alive); unauthenticated `curl
  http://127.0.0.1:8321/memory/review-queue` must return HTTP 422
  (credential-required — proves the API is up AND auth-gating).

Stop: `pkill -f "uvicorn app.main:app"` and `pkill -f "app.worker"` —
**run from a command that does not itself contain those patterns in a
matching context, or the shell will kill itself** (confirmed live). Safest:
kill by PID from `ps aux` output.

Permanent auto-start (**installed and verified 2026-09-15, session 005**): WSL systemd
+ two user units (`memory-governor-api`, `memory-governor-worker`) —
enabled and active; the migration procedure below is retained as the record of how it was done.

### Stopping and starting around a GBrain upgrade (used 2026-09-30)

```bash
systemctl --user stop memory-governor-api
sleep 60          # the worker polls every 60 seconds and delivers what is already promoted
systemctl --user stop memory-governor-worker
# ... upgrade, then:
systemctl --user start memory-governor-api memory-governor-worker
ss -tlnp | grep 8321
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8321/memory/review-queue   # must print 422
```

Confirm that the worker unit still contains the `~/.bun/bin` PATH line. Prove the result afterwards with a per-source fact comparison and one real `/mb-submit-memory` run.

## Submitting a candidate — the real, correct paths

**Manual submission (the normal, real-world path):**
```
/mb-submit-memory <path>
```
Not a raw API call. Confirms the target is inside a registered GBrain
source, queries GBrain for related content and reads it, then submits with
a genuinely reasoned confidence/contradiction assessment — never a
placeholder.

**Direct API** (used by PDLF's step-completion writer, and available for
any future writer):
```
POST /memory/candidate
```
`writer_identity` is never supplied in the payload — it is derived from the
authenticating credential. A `writer_identity` value present in the body is
ignored or rejected, never trusted.

## The decision chain (source-verified, six review classifications)

Evaluated in order; `auto_promote` only if nothing triggers:

1. `provenance_failure` — writer identity fails server verification
   (recommended action: reject)
2. `scope_invalid` — visibility/`shared_with` inconsistent (recommended
   action: quarantine)
3. `unresolved_contradiction` — cross-project, unresolved, or
   `manual_review` (recommended action: none — never auto-decided)
4. `high_risk_type` — memory type is one of the five spec categories:
   `policy`, `credential`, `identity`, [[[mb-3-cs-project-library:docs-local/architecture|Architecture]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/architecture.md), [[[makepdlf-project-library:docs-local/pdlf-testing-seed-material/ci-based-checks-format/checks/security|Security Check]]](C:/dev/dev-makepdlf/makepdlf-project-library/docs-local/pdlf-testing-seed-material/ci-based-checks-format/checks/security.md)
5. `low_confidence` — confidence below the review threshold (default 0.65)
6. `medium_risk_moderate_confidence` — any sharing, or confidence < 0.5,
   with confidence below the auto-promote threshold (default 0.85)

Thresholds are read live from the active `policy_versions` row — policy
changes are data changes, not code changes. The five high-risk categories
became fully implementable on 2026-09-08 (MemoryType enum extended;
previously only `policy` was representable — the resolved spec
inconsistency).

## Checking and resolving the review queue

```
GET /memory/review-queue
```
Returns every candidate currently `under_review`, each with its
`ReviewPresentation` block (recommendation, validation, ramifications) and
any suggested `classification`/`recommended_action`. Empty list = nothing
blocking; non-empty = a decision is genuinely required before certain other
work may proceed (the PDLF step-continuation rule below).

```
POST /memory/{memory_id}/review
{"decision": "promote" | "quarantine" | "reject", "reason": "...", "reviewer": "..."}
```
The only path that resolves a `needs_review` candidate. The system's own
`recommended_action` is always a suggestion; the disposition is always the
developer's explicit decision.

## The PDLF step-continuation rule

**No PDLF step may begin while any review item is open anywhere in the
system** — not scoped to the immediately-preceding step. `GET
/memory/review-queue` is the real, sufficient primitive: empty means clear,
non-empty means block. Confirmed live across the full before/during/after
sequence for `pdlf_step_sync` submissions.

## Superseding a candidate

```
POST /memory/{memory_id}/supersede
```
Atomically sets `valid_until` and `valid_until_reason: superseded` on the
old record, in the same transaction as creating the new one. Use this,
never manual editing, whenever a fact has been deliberately and correctly
replaced.

## Cross-project sharing — real mechanics

A candidate's `scope.visibility` and `scope.shared_with` must be internally
consistent:

| `visibility` | Required `shared_with` |
|---|---|
| `project_local` | `[]` |
| `shared_all` | exactly `["all"]` |
| `shared_specific` | a real, non-empty, explicit project list (never `["all"]`) |

Read-time visibility is resolved against the requesting project (built
deliberately after the read-time gap was found — see the explainer §5).
The same scope drives the GBrain-write visibility mapping: `shared_all` →
world; everything else → private.

## Worked example — a real cross-project contradiction

A candidate submitted with `contradiction.detected: true` and
`contradiction.cross_project: true` always routes to `needs_review` — no
exception path, regardless of confidence or type. The review presentation
carries `classification: unresolved_contradiction` and no automatic
`recommended_action`: the governor never decides which of two conflicting
cross-project claims is correct.

## Permanent auto-start migration (M3-2) — executed + verified 2026-09-15 (procedure retained as the record)

**What it is:** migrating the two processes from the boot-script start to
native systemd user units. The current `[boot]` command already auto-starts
everything at WSL boot (proven), so this migration adds robustness (native
service management, restart=on-failure), not a missing capability.

**Impact warning:** enabling `systemd=true` changes the init model for the
entire WSL environment and **requires a full `wsl --shutdown`** (which
terminates any running agent session). Post-restart verification must
confirm PostgreSQL still auto-starts.

**Correction 2026-09-28 (memory-system-diagnostic §3):** the earlier belief
that "the start script is idempotent, so double-starts are prevented" was
DISPROVED at both 2026-09-28 boots — the script's API won the port-8321
bind race and `memory-governor-api.service` crash-looped on
"address already in use" until the duplicate was killed (twice,
journal-confirmed). **Boot-command retirement decided (full retirement):**
the `[boot]` command no longer invokes `start-memory-system.sh` — the units
own API + worker, `postgresql.service` owns the cluster; the script remains
on disk as a manual fallback for running the stack when the units are down.
`/etc/wsl.conf` is a system file — the developer applies that edit;
verification is a fresh `wsl --shutdown` boot with port 8321 held by the
unit's pid only, no crash-looping, auth-gate 422.

**Step 1 — author the two unit files (agent-runnable, already placed):**
`~/.config/systemd/user/memory-governor-api.service` and
`~/.config/systemd/user/memory-governor-worker.service` (definitions below).

**Step 2 — developer: enable systemd** (edit `/etc/wsl.conf`, add to the
`[boot]` section): `systemd=true` — then run `wsl --shutdown` from PowerShell
and reopen a terminal.

**Step 3 — developer: enable + start the units:**
```bash
systemctl --user daemon-reload
systemctl --user enable --now memory-governor-api.service memory-governor-worker.service
systemctl --user status memory-governor-api memory-governor-worker --no-pager
```

**Step 4 — verify (agent-runnable):** re-run this skill's Tier 0 — plus
confirm PostgreSQL auto-started, both processes healthy, auth-gate 422, and
the start script found both already running (idempotency proof).

### Unit file definitions

`~/.config/systemd/user/memory-governor-api.service`:
```ini
[Unit]
Description=Memory Governor API (FastAPI/uvicorn)
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/dev-p/memory-governor
EnvironmentFile=/home/dev-p/memory-governor/.env
ExecStart=/home/dev-p/memory-governor/.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

`~/.config/systemd/user/memory-governor-worker.service`:
```ini
[Unit]
Description=Memory Governor Worker (outbox LISTEN/NOTIFY)
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/dev-p/memory-governor
EnvironmentFile=/home/dev-p/memory-governor/.env
Environment="PATH=/home/dev-p/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/dev-p/memory-governor/.venv/bin/python -m app.worker
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

The worker unit **must** carry the `Environment="PATH=…"` line — the worker
shells out to `gbrain`, and without the `~/.bun/bin` prefix every delivery
fails (`FileNotFoundError: 'gbrain'`; proven live twice: the 2026-09-14
hand-started worker, and the 2026-09-15 systemd worker whose unit initially
lacked the line — fixed the same hour, four reset events delivered as facts
#60–63). The API unit needs no prefix (it never shells out to gbrain).

## Recovering from an accidental GBrain write — real, confirmed procedure

This procedure exists because it has already happened once. Follow it
exactly; do not improvise a shortcut.

**1. Stop immediately.** Do not run anything further until the real,
current state is understood.

**2. Find the real fact using `recall` — not `search`.** `search` operates
over pages/chunks and returns unrelated content by semantic similarity;
`recall` is the paired read-verb to `remember`:
```
gbrain call recall '{"grep": "<unique marker text from the mistaken fact>"}'
```
Confirm exactly one result matches and its provenance unambiguously
identifies it as the mistaken write. Governed facts live in the source
`memory-governor-code` (2026-09-30): put `GBRAIN_SOURCE=memory-governor-code`
in front of the command, and run it from a folder that does not select
another source (for example your home folder).

**3. Correct it with `forget`, never a guessed argument.** `forget` takes
the opaque `fact_id` from the recall result — never a page slug, never a
guessed number:
```
gbrain call forget '{"id": "<fact_id>", "reason": "<full, honest explanation>"}'
```
This expires the fact and keeps its full audit trail — it does not delete.

**4. Verify the correction took effect — do not trust the success response
alone:**
```
gbrain call recall '{"grep": "<same marker>", "include_expired": true}'
```
Confirm `expired_at` is a real, non-null timestamp.

**5. Fix the actual root cause before retrying.** The confirmed real cause:
a bash script chained commands without verifying each result. Build test
fixtures so a failed step genuinely halts (`subprocess.run(..., check=True)`),
with a `try`/`finally` that unconditionally restores the original state.

**6. Add a permanent standing test for the specific failure mode.**

## Recovering from a stale brain default (incident 2026-09-30)

**Symptom:** after the upgrade to 0.59.18.0, every `gbrain sync --source <id>` printed `Source "diag-mg-sec4" not found or is archived` and ended with an error, for all 15 sources. The same message had already appeared for `pdlf` before the upgrade.

**Cause:** the brain-level default source (`sources.default`) named a source that no longer existed. The worker changes that default before every governed write. The name `diag-mg-sec4` looks like a leftover of a diagnostic (not confirmed). The new version checks that the default exists; the old one was more forgiving.

**Check and fix:**
```
gbrain config get sources.default
gbrain sources list
gbrain sources default default
gbrain config get sources.default
```
The second command must show that the named source exists. If it does not, the third command sets the default to the source `default`. The next governed write sets it to its owning project again. Result on 2026-09-30: failures dropped from 15 to 3 (the remaining three had other causes) and then to none.

## `remember`, `recall`, `forget` — real MEMORY_VERBS mechanics

- **MCP-protocol verbs, not standalone CLI subcommands** — `gbrain recall
  --help` returns a generic usage line; expected, not an error.
- **The correct invocation is `gbrain call <verb> '<json>'`** — confirmed
  live (2026-09-08, protocol v1 JSON).
- **Real parameter schema via `--tools-json`**, saved to a file first:
  ```
  gbrain --tools-json > /tmp/gbrain-tools.json
  ```
  Read-only; safe at any time. `remember` accepts: `fact`, `provenance`
  (required), `ttl`, `entity`, `kind`, `visibility` (`world`|`private`).
- **GBrain 0.59.18.0 (2026-09-30) — inputs compared with 0.46.1.0:** nothing removed, nothing newly required. New optional inputs: `remember`: `source_id` (source to write to; defaults to the selected source), `expected_revision`, `force`, `request_id`; `recall`: `source_id` (narrows the read to one source), `budget_policy`; `forget`: `request_id`. The invocation `gbrain call <verb> '<json>'` is unchanged.
- **Which source a call uses:** `--source`, then the variable `GBRAIN_SOURCE`, then a `.gbrain-source` file, then the registered source whose folder contains the current folder, then the brain default set by `gbrain sources default`. `remember` writes into that source. Facts are stored per source.

## Isolation boundary — stated honestly (2026-09-08; corrected 2026-09-30)

**Facts are stored per source.** Every fact belongs to a source, and `recall` reads the facts of that one source (`source_id` names another single source).

Where governed facts land: the owning project's own documentation source. The worker names that source on every `gbrain remember` call (`GBRAIN_SOURCE`), so the fact lands there whatever folder the worker runs in. A fact written before 2026-10-01 may still sit in `memory-governor-code`.

Project isolation for governed memories is enforced by (a) the governor's own API (read-time visibility resolution against the requesting project) and (b) the write-path stamping added 2026-09-08 (entity = owning_project; visibility mapped from declared scope). It does not come from GBrain's sources.

## Do not

- Do not assume `gbrain sync` moves governed content into GBrain — only
  `remember` does; `sync` ingests raw content regardless of governor
  approval.
- Do not chain shell commands without verifying each result — the
  confirmed real cost is an accidental write into live memory.
- Do not guess at a `forget`/`recall` argument — confirm the schema via
  `--tools-json`, confirm the real `fact_id` via `recall` first.
- Do not treat GBrain dreaming's output as something that will ever appear
  in the review queue — it cannot, by design.
- Do not assume test fixtures are shared across test files.
- Do not run only the API without the worker — promoted candidates then
  silently never leave the outbox.
- Do not kill the processes with a `pkill -f` pattern that appears in your
  own command line — the shell kills itself (confirmed live).
- Do not run `scripts/run-tests-deterministic.sh` while `memory-governor-worker.service` is active — it leaves an unmanaged second worker (procedure above).
- Do not leave `sources.default` naming a source that does not exist — under 0.59.18.0 every sync then fails.
