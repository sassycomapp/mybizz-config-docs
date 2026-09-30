---
title: "doc-maintainer-config"
doc-id: "mb-62b3add2"
---
# mb-doc-maintainer — Configuration

Canonical current-state configuration record for `mb-doc-maintainer` as a
division-wide system component. Agent-facing. Reflects the live-verified state
as of 2026-09-25. States facts, not history — reasoning in
[[doc-maintainer-explainer|Explainer]]; commands and procedures in
[[doc-maintainer-reference|Reference]].

---

## Identity

| Item | Value |
|---|---|
| Component | `mb-doc-maintainer` — save-time documentation-maintenance skill |
| Governing contract | `C:\mybizz\mybizz-config-docs\gbrain\gbrain-doc-contract.md` (Phase 1 artifact; developer-approved 2026-09-24; registered in the config-docs register) |
| Source repo | `C:\mybizz\mb-doc-maintainer` — git-initialized; GitHub `sassycomapp/mb-doc-maintainer` (private); first commit `9dae0db` (14 files, 1905 insertions) |
| Source artifact | `C:\mybizz\mb-doc-maintainer\mb-doc-maintainer-skill.md` — named per the reserved-filename rule (`SKILL.md` exists only at the managed install location) |
| Installed skill | `~/.config/opencode/skills/mb-doc-maintainer/SKILL.md` (installed by the developer 2026-09-25) |
| Skill frontmatter | corpus two-field format: `title`/`doc-id` = `SKILL`; no `description` field (developer-mandated format) |
| Governing plan | `C:\data-mybizz-mgt\desktop\doc-auditor-maintaner-planning\mb-doc-maintainer — Complete Consolidated Plan.md` (final; all decisions locked) |

## Component layout (source repo)

| Path | Role |
|---|---|
| `tool/frontmatter.py` | frontmatter validate/repair per contract (G1/G2/G5/O1; byte-preserving; UTF-8-BOM tolerant on read) |
| `tool/links.py` | wikilink grammar/resolution (G6/G7), target existence (O7), basename collisions, prose-reference candidates |
| `tool/register.py` | 5-column register check/diff/apply; four-event discipline enforced by surface area (append-only by construction) |
| `watch/save-watcher.ps1` | Windows FileSystemWatcher over runtime-derived scope; coalescing; writes pending events |
| `watch/run-watcher.cmd` | scheduled-task launcher (redirects console to the watcher log) |
| `tests/` | 40 stdlib-unittest tests (pytest-compatible if pytest is ever installed) — all passing 2026-09-25 |

## Watcher (always-on)

| Item | Verified state |
|---|---|
| Scheduled task | `mb-doc-maintainer-save-watcher` (registered 2026-09-25) |
| Trigger / durability | at logon; restart-on-failure 3 attempts / 1-min interval; no execution-time limit; battery-safe |
| Single instance | session mutex `mb-doc-maintainer-save-watcher`; abandoned-mutex tolerant (crash does not block restart) |
| Live state | Running at registration (PID 2320); console log `C:\mybizz\logs\mb-doc-maintainer\watcher.log` |
| Watched roots | derived at each start from `C:\mybizz\mybizz-os-docs\os-reference-docs\mybizz-scope-list.md`: `C:\data-mybizz-mgt`, `C:\dev`, `C:\mybizz`, `C:\pdlf` |
| Filter | `*.md` only |
| Defaults | debounce 60 s (tunable, never fixed), poll 5 s |
| Exclusions | scope-list exceptions; WIP/temp folder names and `temp-*` prefixes at any depth; dotfolders and `.git`; `tmp-` prefixed files (O3); any folder containing `anvil.yaml` (existence check only); the queue dir and run-log (never self-queues) |

## Storage

| Item | Path | Character |
|---|---|---|
| Pending-events queue | `C:\mybizz\logs\mb-doc-maintainer\pending-events\` | regenerable plumbing; one JSON file per stable saved-document event; removed after processing |
| Durable run log | `C:\mybizz\mybizz-config-docs\mb-doc-maintainer\doc-maintainer-run-log.md` | append-only; one line per maintenance event; registered in the config-docs register |
| Watcher console log | `C:\mybizz\logs\mb-doc-maintainer\watcher.log` | regenerable plumbing (logs exception area) |

## GBrain integration

| Item | Value |
|---|---|
| Source ID | `mb-doc-maintainer` (registered 2026-09-25) |
| Federated | no — searched only when explicitly named via `--source` |
| Ingestion | markdown-only (default strategy); 1 page (`mb-doc-maintainer-skill.md`), 7 chunks, 100% embedded; checkpoint at commit `9dae0db` |
| Code files | `.py`/`.ps1` not ingested — would require `--strategy code` (deliberate state change, not yet applied) |

## Register usage

| Register | Relevance |
|---|---|
| `C:\mybizz\mybizz-config-docs\register-local.md` | holds the run-log row (creation event 2026-09-25) and the contract row (`gbrain-doc-contract`, 2026-09-24) |
| Per-project-library `register-local.md` / `register-global.md` | the maintainer reads and maintains these by the four-event model; it never registers its own suite files (catalogue) |

## Recorded decisions (developer, 2026-09-25)

| Decision | Value |
|---|---|
| Watcher mode | always-on (scheduled task), not invoked per session |
| Skill artifact naming | source copy uses `-skill` suffix; `SKILL.md` only at the install location (Cupcake reserved-name rule) |
| Deletion handling | register rows are never removed; deletion sets `state: Retired` (four-event retirement) |

## Open items

| # | Item | Status |
|---|---|---|
| 1 | Register rows for `doc-maintainer-config`, `doc-maintainer-reference`, `doc-maintainer-explainer` — not appended (explicit task stipulation excluded register work); the config-docs register does not yet carry them. | Open |
| 2 | Code ingestion (`--strategy code`) for the source repo's `.py`/`.ps1` tooling — not applied; default markdown-only ingestion stands. | Open |
| 3 | First-run verification is on one live event (`repo-organization.md`, modification, no repairs). Creation/move/deletion are verified on corpus copies only, not yet on live saves. | Open |