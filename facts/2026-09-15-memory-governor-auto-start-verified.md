---
title: "2026-09-15-memory-governor-auto-start-verified"
doc-id: "mb-a782c00a"
---
# Fact — memory governor auto-start installed and verified

The memory governor's **permanent auto-start is installed and verified
(2026-09-15, session 005)** — the system is restart-independent:

- WSL systemd enabled (`systemd=true` under the existing `[boot]` section of
  `/etc/wsl.conf`). Two systemd user units, placed 2026-09-13 and enabled
  2026-09-15, both **active** with `Restart=on-failure`:
  `memory-governor-api` (uvicorn on 127.0.0.1:8321) and
  `memory-governor-worker` (outbox LISTEN/NOTIFY).
- Verified live post-switchover: port 8321 held by the service's process,
  auth-gate 422, both processes under the user manager's CGroup.

**Correction 2026-09-28 (memory-system-diagnostic §3):** two claims in the
original record were disproved by live evidence. (1) "The prior boot
command preserved … the start script remains idempotent" — at BOTH
2026-09-28 boots the boot script's API instance won the port-8321 bind race
and `memory-governor-api.service` crash-looped ("address already in use")
until the duplicate was killed; the expected idempotent skip never fired.
(2) The "idempotent skip proves itself at the next natural restart"
standing-check — it ran at two restarts and failed both. **Decision — full
boot-command retirement (developer-approved 2026-09-28):** the `[boot]`
command no longer invokes `start-memory-system.sh`; the units own both
processes and `postgresql.service` owns the cluster. Unit definitions:
[[memory-governor-reference|Usage, Invocation, and Incident Response]]
§Permanent auto-start migration. Previously approved 2026-09-08; units
placed 2026-09-13.
