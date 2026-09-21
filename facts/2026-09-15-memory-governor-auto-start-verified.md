---
document: "Fact — memory governor auto-start installed and verified"
doc-id: 2026-09-15-memory-governor-auto-start-verified
state: Live
date-created: 2026-09-15
---

# Fact — memory governor auto-start installed and verified

The memory governor's **permanent auto-start is installed and verified
(2026-09-15, session 005)** — the system is restart-independent:

- WSL systemd enabled (`systemd=true` under the existing `[boot]` section of
  `/etc/wsl.conf`; the prior boot command preserved — PostgreSQL auto-starts
  and the start script remains idempotent).
- Two systemd user units, placed 2026-09-13 and enabled 2026-09-15, both
  **active** with `Restart=on-failure`: `memory-governor-api` (uvicorn on
  127.0.0.1:8321) and `memory-governor-worker` (outbox LISTEN/NOTIFY).
- Verified live post-switchover: port 8321 held by the service's process,
  auth-gate 422, both processes under the user manager's CGroup.

Context: at the migration boot the boot script started the API but not the
worker (no worker log written) — the exact flakiness class the migration
eliminates; the worker now self-heals under its unit. The start script's
idempotent skip (finding both services already running) proves itself at the
next natural restart — standing-check territory, not an open item. Unit
definitions: [[memory-governor-reference|Usage, Invocation, and Incident Response]] §Permanent auto-start migration
(executed + verified 2026-09-15). Previously approved 2026-09-08; units
placed 2026-09-13.
