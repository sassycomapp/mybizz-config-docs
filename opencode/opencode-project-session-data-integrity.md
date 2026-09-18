---
doc-id: opencode-project-session-data-integrity
state: Live
date-created: 2026-09-05
document: OpenCode — Project & Session Data Integrity
status: Current — verified live 2026-09-17
---

# OpenCode — Project & Session Data Integrity

## What this covers

A confirmed, upstream limitation in OpenCode's own project/session
database (`opencode.db`), and the two maintenance scripts that exist to
manage it. This does not cover permission/access control — see
`opencode-permission-access-control-model.md` for that.

## The underlying problem

OpenCode has **no built-in cleanup mechanism** for its own
`~/.local/share/opencode/opencode.db`. This is a confirmed, reported gap
in the tool itself, not a misconfiguration on this machine:

- No `DELETE` endpoint/command exists for stale `project` rows
  (upstream feature request: anomalyco/opencode#25004).
- Renaming or moving a project folder orphans its sessions — they keep
  referencing the old path forever (upstream: #23248 — this is exactly
  what happened when `dev-pdlf` was renamed to `dev-makepdlf`, and when
  the machine's layout moved from `C:\projects\` to `C:\dev\`).
- Session storage (full reasoning/tool-output history) has no retention
  limit and grows unbounded — independently reported by other users
  reaching multi-gigabyte databases from normal use.

**Two distinct symptoms this produces, and how to tell them apart:**

| Symptom | Cause | Which script fixes it |
|---|---|---|
| OpenCode opens a project/path that no longer exists, or shows a folder from before a rename | Stale rows in the `project` and/or `session` tables, keyed to a directory that's gone | `opencode-db-cleanup.sh` (manual) |
| `opencode.db` growing large over time; general slowdown | Unbounded session history, no retention | `opencode-session-prune.sh` (scheduled) |

## Script 1 — `opencode-db-cleanup.sh` (manual, on demand)

**Purpose:** removes `project` and `session` rows whose folder no longer
exists on disk. **Deliberately not scheduled** — "stale" is judged by
folder existence, which could produce a false positive if a drive is
temporarily unmounted at the wrong moment. Always backs up the full
database first, always shows exactly what it found, and requires a typed
`YES` before deleting anything.

**Location:** `C:\mybizz\scripts\opencode-db-cleanup.sh`
**Backups written to:** `C:\backup-wsl\opencode-db-cleanup\<timestamp>\`

**When to run it:** after renaming or moving any project folder, or any
time OpenCode opens the wrong project on startup.

See `daily-ops.md` for the exact run command.

## Script 2 — `opencode-session-prune.sh` (scheduled, daily)

**Purpose:** deletes session history older than 60 days. Safe to run
unattended — the criterion is purely a timestamp, no false-positive risk.
Always backs up the full database first. Dynamically discovers which
tables reference `session` via `PRAGMA foreign_key_list` (rather than
hardcoding schema) and cleans dependent rows before deleting the session
rows themselves, then runs `VACUUM` to actually reclaim disk space.

**Location:** `C:\mybizz\scripts\opencode-session-prune.sh`
**Backups written to:** `C:\backup-wsl\opencode-session-prune\<timestamp>\`
**Retention:** 60 days
**Schedule:** Windows Task Scheduler task `OpenCodeSessionPrune`, daily
at 17:05 — **verified live 2026-09-09: the task exists, status Ready**.

See `daily-ops.md` for the exact run/verification commands.

## Critical operational note — WSL distro selection

**Verified live 2026-09-09** (the distro list): this machine has **two
WSL distributions installed** — `Ubuntu-22.04` (the DEFAULT, currently
stopped) and `Ubuntu` (running). `dev-p`'s home directory and all working
data live in `Ubuntu`, which is **not** the default distro. Any command
invoked from Windows (Task Scheduler, PowerShell) that calls a bare
`wsl.exe` will silently run against the wrong distro/user, producing
confusing failures (wrong `$HOME`, or an outright `WSL_E_USER_NOT_FOUND`
error).

**Always specify both distro and user explicitly:**
```
wsl.exe -d Ubuntu -u dev-p bash <full-script-path>
```

---

*End of document*
