---
title: "memory-governor-reference"
doc-id: "mb-38660a2f"
updated: "2026-10-20"
---
# Memory Governor Reference — Usage, Invocation, and Incident Response

State: [[[mybizz-config-docs:memory-governor/memory-governor-config|Config]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md). Reasoning:
[[[mybizz-config-docs:memory-governor/memory-governor-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-explainer.md). Standing differences:
[[[mybizz-config-docs:memory-governor/memory-governor-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-learnings.md). The full memory-system map:
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Memory Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md). Skills named here are
listed in the skills catalog:
`/mnt/c/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md`.

---

## Running the test suite

The suite writes into the live database and the live queue. It is never run
against live memory. Use the deterministic runner, never bare `pytest` while
the worker runs:

```bash
/home/dev-p/memory-governor/scripts/run-tests-deterministic.sh
```

It pauses the worker (kill by PID — the safe method), runs the full suite
with the environment loaded, and always restarts the worker afterwards
(trap, even on failure). Extra pytest arguments pass through (for example
`... -k test_name`). Bare `pytest` is acceptable only when the worker is not
running.

The runner is not systemd-aware — never run it while
`memory-governor-worker.service` is active. It stops the worker with `kill`
and afterwards starts a plain unmanaged worker; the unit then stays stopped,
and a later `systemctl --user start` would run a second worker beside the
unmanaged one. The correct sequence:

```bash
systemctl --user stop memory-governor-worker
cd /home/dev-p/memory-governor && set -a && source .env && set +a && .venv/bin/python -m pytest -q
systemctl --user start memory-governor-worker
gbrain config get sources.default
```

Afterwards `sources.default` must name a source that exists (see the
stale-brain-default procedure below).

A code change is proven by one real governed submission, end to end — never
by the test suite alone.

## Starting and stopping the system

Both processes are required. The API decides; the worker delivers (GBrain
writes and register/payload writes). An API without a worker leaves promoted
candidates stranded in the outbox.

Stop in this order: API first; wait 60 seconds (the worker polls every 60
seconds and delivers what is already promoted); then the worker. Start both
together:

```bash
systemctl --user stop memory-governor-api
sleep 60
systemctl --user stop memory-governor-worker
systemctl --user start memory-governor-api memory-governor-worker
ss -tlnp \| grep 8321
```

Manual start (when the units are down), from the app folder with `.env`
sourced first — there is no dotenv autoload:

```bash
cd /home/dev-p/memory-governor && set -a && source .env && set +a
setsid .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321 >> /tmp/memory-governor.log 2>&1 < /dev/null &
PATH="$HOME/.bun/bin:$PATH" setsid .venv/bin/python -m app.worker >> /tmp/memory-governor-worker.log 2>&1 < /dev/null &
```

- The worker's PATH prefix (`~/.bun/bin`) is mandatory: without it the
  worker cannot invoke `gbrain` and every delivery fails. The API does not
  need the prefix (it never shells out to gbrain).
- `setsid` + full redirection is required: a plain `nohup &` child dies when
  the launching shell's process group is terminated.

Stop by PID from `ps aux` output. Never kill with a `pkill -f` pattern that
appears in your own command line — the shell kills itself.

## Submitting a candidate

Manual submission — the normal path:

```
/mb-submit-memory <path>
```

Not a raw API call. The suite confirms the target is inside a registered
GBrain source, queries GBrain for related content and reads it, then submits
with a genuinely reasoned confidence/contradiction assessment — never a
placeholder.

Direct API — the PDLF step-completion writer's path, available to any
writer:

```
POST /memory/candidate
```

`writer_identity` is never supplied in the payload — it is derived from the
authenticating credential. A `writer_identity` value present in the body is
ignored or rejected, never trusted.

## Route inventory (11 routes)

| Method & Path | Purpose |
|---|---|
| `POST /memory/candidate` | Submit a candidate — inline content or a `provenance.source_ref` path |
| `GET /memory/{memory_id}` | Fetch a candidate |
| `GET /memory` | List candidates, filterable by project/status/type |
| `GET /memory/review-queue` | All candidates currently `under_review`, each with its ReviewPresentation |
| `POST /memory/{memory_id}/review` | Record a human decision: promote / quarantine / reject |
| `POST /memory/{memory_id}/supersede` | Supersede with a new record; atomically sets `valid_until` on the old one |
| `GET /memory/{memory_id}/provenance` | Full audit and decision trail |
| `POST /memory/quarantine` | Manual quarantine of an existing candidate |
| `POST /memory/projects` | Register a project |
| `PATCH /memory/projects/{project_id}` | Toggle a project's `dormant` flag |
| `POST /memory/policy` | Propose a new policy version — routes through the standard high-risk pipeline |

## The decision chain

Evaluated in order; `auto_promote` only if nothing triggers:

1. `provenance_failure` — writer identity fails server verification
   (recommended action: reject)
2. `scope_invalid` — visibility/`shared_with` inconsistent (recommended
   action: quarantine)
3. `unresolved_contradiction` — cross-project, unresolved, or
   `manual_review` (no recommended action — never auto-decided)
4. `high_risk_type` — memory type is one of the five high-risk types:
   `policy`, `credential`, `identity`, `architecture`, `security`
5. `low_confidence` — confidence below the review threshold
6. `medium_risk_moderate_confidence` — any sharing, or confidence < 0.5,
   with confidence below the auto-promote threshold

Threshold values live in the config. A candidate submitted with
`contradiction.cross_project: true` always routes to `needs_review` — no
exception path, regardless of confidence or type — and carries no automatic
recommended action: the governor never decides which of two conflicting
cross-project claims is correct.

## Resolving the review queue

```
GET /memory/review-queue
```

Returns every candidate currently `under_review`, each with its
`ReviewPresentation` block (recommendation, validation, ramifications) and
any suggested `classification`/`recommended_action`. Empty list = nothing
blocking; non-empty = a decision is required. The system's own
`recommended_action` is always a suggestion; the disposition is always the
developer's explicit decision.

```
POST /memory/{memory_id}/review
{"decision": "promote", "reason": "...", "reviewer": "dev-p"}
```

`decision` is `promote`, `quarantine` or `reject`; `reviewer` is `dev-p`.
This is the only path that resolves a `needs_review` candidate.

## Superseding a fact

Superseding changes only the governor's record. It atomically sets
`valid_until` (reason `superseded`) on the old record, in the same
transaction as creating the new one:

```
POST /memory/{memory_id}/supersede
```

The old fact in GBrain is retired with `forget`, using the fact's real id
from `recall`:

```bash
gbrain call forget '{"id": "<fact_id>"}'
```

Both steps, every time — the governor's record and the brain must agree.
Never hand-edit either side.

## The PDLF step-continuation rule

No PDLF step may begin while any review item is open anywhere in the system
— not scoped to the immediately-preceding step. `GET /memory/review-queue`
is the sufficient primitive: empty means clear, non-empty means block.

## Cross-project sharing

A candidate's `scope.visibility` and `scope.shared_with` must be internally
consistent:

| `visibility` | Required `shared_with` |
|---|---|
| `project_local` | `[]` |
| `shared_all` | exactly `["all"]` |
| `shared_specific` | a real, non-empty, explicit project list (never `["all"]`) |

Read-time visibility resolves against the requesting project: a candidate is
visible when it is the requester's own, `shared_all`, or `shared_specific`
with the requester explicitly listed. The same scope drives the GBrain-write
visibility mapping (config, GBrain integration).

## Recovering from an accidental GBrain write

1. Stop immediately. Do not run anything further until the real state is
   understood.
2. Find the real fact with `recall`, not `search` — `search` operates over
   pages/chunks and returns unrelated content by similarity; `recall` is the
   paired read-verb to `remember`:
   ```bash
   gbrain call recall '{"grep": "<unique marker text from the mistaken fact>"}'
   ```
   Governed facts live in their owning project's source: put
   `GBRAIN_SOURCE=<owning project>` in front of the command, and run it from
   a folder that does not select another source. Confirm exactly one result
   matches and its provenance unambiguously identifies the mistaken write.
3. Correct it with `forget`, using the opaque `fact_id` from the recall
   result — never a page slug, never a guessed number:
   ```bash
   gbrain call forget '{"id": "<fact_id>", "reason": "<full, honest explanation>"}'
   ```
   This expires the fact and keeps its audit trail — it does not delete.
4. Verify the correction took effect — do not trust the success response
   alone:
   ```bash
   gbrain call recall '{"grep": "<same marker>", "include_expired": true}'
   ```
   Confirm `expired_at` is a real, non-null timestamp.
5. Fix the actual root cause before retrying. Build scripts so a failed step
   genuinely halts (`subprocess.run(..., check=True)`), with a
   `try`/`finally` that unconditionally restores the original state.
6. Add a standing test for the specific failure mode.

## Recovering from a stale brain default

Symptom: every `gbrain sync --source <id>` ends with
`Source "<name>" not found or is archived`.

Cause: the brain-level default source (`sources.default`) names a source
that does not exist. Every governed write sets that default to its owning
project; removing a source leaves the default dangling, and `gbrain sync`
then fails for every source.

Check and fix:

```bash
gbrain config get sources.default
gbrain sources list
gbrain sources default default
gbrain config get sources.default
```

The second command must show that the named source exists; if it does not,
the third command sets the default to the source `default`. The next
governed write sets it to its owning project again.

## MEMORY_VERBS mechanics

- The verbs are MCP-protocol verbs, not standalone CLI subcommands —
  `gbrain recall --help` returning a generic usage line is expected, not an
  error.
- The invocation is `gbrain call <verb> '<json>'`.
- Confirm the real parameter schema before any call:
  ```bash
  gbrain --tools-json > /tmp/gbrain-tools.json
  ```
  Read-only; safe at any time.
- Which source a call uses, in order: `--source`, then the variable
  `GBRAIN_SOURCE`, then a `.gbrain-source` file, then the registered source
  whose folder contains the current folder, then the brain default set by
  `gbrain sources default`. `remember` writes into that source; facts are
  stored per source.

## Committing the repository

The repository is committed by hand; `commit-all` does not cover it. The
developer runs:

```bash
cd /home/dev-p/memory-governor && git add <files> && git commit -m "<message>"
```

Agents never use Git. The worker itself commits and pushes register changes.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Repository (canonical source) | `/home/dev-p/memory-governor` — `github.com/sassycomapp/memory-governor` | 0.1.0 | 2026-10-20 |
| `pyproject.toml` | `/home/dev-p/memory-governor/pyproject.toml` | 0.1.0 | 2026-10-20 |
| `app/policy.py` | `/home/dev-p/memory-governor/app/policy.py` | 0.1.0 | 2026-10-20 |
| `app/api.py` | `/home/dev-p/memory-governor/app/api.py` | 0.1.0 | 2026-10-20 |
| `app/models.py` | `/home/dev-p/memory-governor/app/models.py` | 0.1.0 | 2026-10-20 |
| `app/state_machine.py` | `/home/dev-p/memory-governor/app/state_machine.py` | 0.1.0 | 2026-10-20 |
| `app/gbrain.py` | `/home/dev-p/memory-governor/app/gbrain.py` | 0.1.0 | 2026-10-20 |
| `app/worker.py` | `/home/dev-p/memory-governor/app/worker.py` | 0.1.0 | 2026-10-20 |
| `scripts/run-tests-deterministic.sh` | `/home/dev-p/memory-governor/scripts/run-tests-deterministic.sh` | — | 2026-10-20 |
| systemd user units | `~/.config/systemd/user/memory-governor-api.service`; `~/.config/systemd/user/memory-governor-worker.service` | — | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Operational status | `systemctl --user is-active memory-governor-api memory-governor-worker`; `systemctl --user is-enabled memory-governor-api memory-governor-worker` | agent |
| Installed version | Read `version` in `/home/dev-p/memory-governor/pyproject.toml` | agent |
| Works | One real governed submission via `/mb-submit-memory`; confirm `promoted` and the fact present in the owning project's source | agent |
| API up and auth-gating | `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8321/memory/review-queue` — must print 422 | agent |
| Port listener | `ss -tlnp \| grep 8321` — one listener | agent |
| Worker process | `ps aux \| grep app.worker` | agent |
| Worker unit PATH line | `systemctl --user cat memory-governor-worker` — the `Environment="PATH=…"` line carries the `/home/dev-p/.bun/bin` prefix | agent |
| Brain default source | `gbrain config get sources.default`, cross-checked against `gbrain sources list` — names a source that exists | agent |
| Register integrity | Count `registers/candidates/*.json` against the index rows in `registers/register-memory-governor.md` | agent |
| Review queue | `GET /memory/review-queue` with the credential from `.env` — agents never read `.env` | developer |
| Database state | `sudo -u postgres psql -d memory_governor` — row counts and the `policy_versions` state | developer |
| Test suite | Stop unit → pytest → start unit (writes the live database and queue) | developer |

## Do not

- Do not submit material through any path other than the governed ones —
  `gbrain sync` ingests raw content regardless of governor approval.
- Do not submit `anvil-agent-references`, or any update to it, through the
  governor API — sync it into GBrain the ordinary way (`gbrain sync`).
- Do not assume GBrain dreaming's output reaches the review queue — it
  cannot, by design.
- Do not write `writer_identity` into a candidate payload — it is derived
  from the credential.
- Do not chain shell commands without verifying each result.
- Do not guess a `forget`/`recall` argument — confirm the schema via
  `--tools-json` and the real `fact_id` via `recall` first.
- Do not assume test fixtures are shared across test files —
  `api_client`/`real_credential_headers` exist only in `test_api.py`.
- Do not hand-edit `registers/` or the database — the worker and the API are
  the writers.
- Do not run `scripts/run-tests-deterministic.sh` while
  `memory-governor-worker.service` is active.
- Do not run the API without the worker — promoted candidates then silently
  never leave the outbox.
- Do not kill with a `pkill -f` pattern that appears in your own command
  line — kill by PID.
- Do not leave `sources.default` naming a source that does not exist.
