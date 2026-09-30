---
title: "mb-submit-memory-config"
doc-id: "mb-e76d96dd"
---
# mb-submit-memory — Configuration

Canonical current-state configuration record. Agent-facing. States facts,
not history — decisions and reasoning in [[mb-submit-memory-explainer|Explainer]];
the full cycle in [[mb-submit-memory-reference|Reference: Usage, Invocation, and the Full Cycle]]; the skill's own
`SKILL.md` is the authoritative procedure. All values verified live
2026-09-08 unless noted.

## Identity

| Item | Value |
|---|---|
| Skill name | `mb-submit-memory` — custom (mb-*) skill |
| Location | `~/.config/opencode/skills/mb-submit-memory/SKILL.md` (real file, 2026-08-25) — the sole copy; no repo-side mirror since 2026-09-15 (the folder's skill slot now holds the `mb-config-mb-submit-memory` exam-skill source per developer instruction; the 13,502 B fingerprint above is the repo-side anchor). The exam-skill source↔installed pair is hash-verified each cycle |
| Invocation | `/mb-submit-memory (path)` — path always given explicitly by the developer, never inferred; never auto-triggered |
| Structure | Single file (13,502 B). A 25-byte `Zone.Identifier` sidecar in the installed dir was removed 2026-09-08 |
| Modus operandi | learnings → backup (none needed) → detect → report → **pause for inline approval** → apply → verify → log → learnings — one continuous run, same as Docs Manager and mb-wikilinks |

## What it does — one line

Submits real, developer-authored file content into durable GBrain memory,
exclusively through the memory-governor's API — the single, correct governed
path. Never calls `gbrain remember` or `gbrain sync` directly.

## Downstream system — the memory governor (verified live 2026-09-08)

| Item | Value |
|---|---|
| App | `/home/dev-p/memory-governor` (WSL-native, deliberate — do not relocate); git remote `sassycomapp/memory-governor.git` |
| Version | pyproject declares `0.1.0`; a stray empty file `0.48.2.0` sits in the repo root (origin unconfirmed, likely a shell artifact of 2026-09-06) — deletion pending (developer; restricted folder) |
| API | `http://127.0.0.1:8321` — **ACTIVE as of 2026-09-08** (started detached, log-verified, survives shell exit); auth-gates unauthenticated calls correctly (HTTP 422 credential-required, observed live) |
| Start procedure (on demand) | `cd /home/dev-p/memory-governor && set -a && source .env && set +a && setsid nohup .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8321 >> /tmp/memory-governor.log 2>&1 < /dev/null &` — `.env` must be sourced first (no dotenv autoload) |
| Permanent auto-start | **Installed and verified 2026-09-15 (session 005):** systemd enabled in WSL; the governor runs as two auto-start, auto-restart user services (`memory-governor-api`, `memory-governor-worker`) |
| Database | `memory_governor` on WSL-native PostgreSQL 16 (server verified up today). DB-level state (5 tables, 5 real candidate rows, owner `memory_governor_svc`) verified 2026-09-05 by [[memory-governor-config|Memory Governor Configuration]]; re-check requires the service credential (not accessed) |
| Its own GBrain source | `memory-governor-code` — registered (53 pages); the 2026-09-05 recommendation was actioned |
| Past-run evidence | `/tmp/memory-governor.log` — clean startup + `POST /memory/projects` 201 + `POST /memory/candidate` 201; `registers/candidates/` holds the real candidate records |

## Governance chain state (all verified 2026-09-08)

| Item | State |
|---|---|
| Cupcake enforcement | **ACTIVE** |
| Outbound-network rule | **Amended 2026-09-08** — loopback destinations (`127.0.0.1`, `localhost`, `::1`) always allowed; the skill's API path is now permitted under active enforcement. Formal eval tests pending developer run; one real loopback call already passed live |
| MEMORY_VERBS | **Enabled** (`gbrain config get mcp_surface` → `verbs`) — the ungoverned quick path (`gbrain remember`) is a live tool surface; the discipline routing durable submissions through this skill is documented, not mechanical |
| mg-grant / mg-revoke | **Cupcake's** cross-project grant tools (`~/.config/cupcake/bin/`) — the "mg-" prefix has no connection to the memory governor; do not conflate |

## Naming drift — RESOLVED (source-side)

The old open item (`dev-makepdlf` vs `makepdlf-project-library`) is resolved
on the source side: `gbrain sources list` shows `makepdlf-project-library`
(128 pages, synced 2026-09-08). The governor-side `owning_project` rows are
pending a credentialed API check (needs the `manual_submission` credential).

## Logs

`/mnt/c/mybizz/logs/mb-submit-memory/` — two run logs (`2026-08-27T060743+0200.md`, `2026-09-14T222823+0200.md`) + `learnings.md` (8 durable entries). Verified live 2026-09-15 (exam run #1).

## Open items

- Governor-side `owning_project` verification — executed 2026-09-15 (exam run #1 Tier 3): credential accepted, review queue empty (nothing pending); every evidenced `owning_project` (`mybizz-config-docs`, `makepdlf-project-library`) matches a registered gbrain source exactly. Boundary: no documented API endpoint enumerates all project rows — full enumeration would require a new read endpoint (developer feature decision) or a credentialed DB query (developer-run).
- Permanent auto-start installation (systemd migration) — pending developer execution.
- Stray `0.48.2.0` file deletion — pending developer (restricted folder).
- Dual SKILL.md copies — dissolved 2026-09-15 (exam run #1 gate): the mirror slot was repurposed as the exam-skill source; the subject skill has a single installed copy.
