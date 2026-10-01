---
title: "gbrain-skill"
doc-id: "mb-0bfb2a59"
updated: "2026-10-01"
---
# mb-config-gbrain — Exam Skill

Exams the live GBrain system against its spec. This skill holds the **procedure**
only — expected values live in the spec doc, read fresh at the start of every run.

- Spec: [[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) — read it first, every run
- **Exam plan: [[[mybizz-config-docs:gbrain/gbrain-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-plan.md) — read second, every run.** The
  plan-driven cycle: the config-manager synthesizes this plan fresh before each run
  (from spec + last report + log + learnings) and this skill executes it in hand.
  The plan carries run-specifics and deltas; the **standing check inventory lives
  in this skill** (below) — permanent occurrences graduate here, never into plans
- Reference: [[[mybizz-config-docs:gbrain/gbrain-reference|Reference: Commands, Mechanics, Incidents, Troubleshooting]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-reference.md)
- Report: [[[mybizz-config-docs:gbrain/gbrain-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md) — one file, overwritten each run
- Log: [[[mybizz-config-docs:gbrain/gbrain-log|Log]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-log.md) — append one run row (date, verdict, findings,
  disposition) after every run; free rows for notable events witnessed between runs
- Learnings: [[[mybizz-config-docs:gbrain/gbrain-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-learnings.md) — file new patterns/nuances; delete
  entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **GBrain the system**: binary, config, schema pack, sources,
  models, MCP integration, sync machinery, stale artifacts.
- **Database-level checks (tables, RLS, roles, embedding coverage, extensions)
  belong to `mb-config-postgresql`** — never duplicate them here; cross-reference
  its current exam report when a DB fact is needed.

## Credential discipline (hard rule)

`~/.gbrain/config.json` carries the database URL **with the real password**. Never
print it, never cat the file. The sensitive-data guard blocks agent reads of this
file entirely (proven live 2026-09-12) — so **config-content probes
(`self_upgrade_mode`, models, keys-absent) are developer-run**: the agent verifies
file existence/permissions only and hands the developer the exact jq checks. API
keys appear in the environment only; verify **presence**, never value.

## Tier 0 — Liveness (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| G0-1 | A | Binary resolves: `/home/dev-p/.bun/bin/gbrain` exists; `/home/dev-p/gbrain/VERSION` readable | Both present; VERSION matches spec |
| G0-2 | A | Engine responds: brain identity call (MCP) returns version + counters without error | 0.46.1.0, engine postgres, counters sane |
| G0-3 | A | DB ping on `gbrain` database | `SELECT 1` returns 1 |

## Tier 1 — Health

| ID | Runner | Check | Expected |
|---|---|---|---|
| G1-1 | A | `sources list` — every registered source's path exists on disk; page counts sane (growth-at-sync expected; only zero-count or missing-path = anomaly) | 14 live (spec 13 + `pdlf` until spec refreshed) |
| G1-2 | A | Sync machinery: `~/.gbrain/sync-failures.jsonl` empty; crontab holds no gbrain entries | Both clean (any cron reappearance = finding) |
| G1-3 | A | Embedding coverage — cross-reference the postgres module's current exam report (never re-probe); quick count permitted | 100% |
| G1-4 | A | Legacy artifact `~/.gbrain/brain.pglite` — record presence or absence | Absence expected (documented stale artifact; spec-drift flag until refreshed) |
| G1-5 | A | `~/.gbrain/` directory integrity — listing only (names/metadata; **never read `config.json`**) | Structure matches spec; `config.json` present with restrictive permissions |

## Tier 2 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| G2-1 | A | Version | live 0.46.1.0; upstream gap recorded, **never upgraded on newness** (upgrade only on check failure) |
| G2-2 | A | Schema pack (MCP) | `gbrain-everything@1.0.0+7021205a`, 30 page types / 12 link types |
| G2-3 | A | MCP integration entry | `opencode.jsonc` → `mcp.gbrain`: local, `["/home/dev-p/.bun/bin/gbrain", "serve"]`, enabled true, env names OPENAI_API_KEY + ZEROENTROPY_API_KEY |
| G2-4 | A | Models (via DB [[[makepdlf-project-library:docs-local/config\|Config]]](C:/dev/dev-makepdlf/makepdlf-project-library/docs-local/config.md) table — agent-safe, unlike `config.json`) | embedding `openai:text-embedding-3-large`, dims 1536 |
| G2-5 | A | Skills bundle at `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` | re-inventory vs last recorded state (bundle evolves with CLI — flag divergence from last recorded, not older snapshots) |
| G2-6 | A | Page accounting — **per-source DB query** (`GROUP BY source_id`), not cross-snapshot sums: the MCP sources list reports per-source counts as-of last sync and can lag the identity total | sums reconcile exactly; unattributed pages = real finding |
| G2-7 | A | Registered source paths all exist | all present on disk |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| G3-1 | D | `config.json` content (masked output — never print the DB URL): `self_upgrade_mode: notify`; no API keys inside; DB URL present | as spec |
| G3-2 | D | Full sync verification on a sample source (writes — content-changing) | clean sync, no failures |
| G3-3 | D | MCP server restart behavior (config changes need full process restart) | documented behavior holds |
| G3-4 | D | Upgrade decision | policy question — developer's, never agent-initiated |

## Heal allowlist (gate-gated)

- Doc corrections → flagged to docs governance, never applied here
- **No live-system heals defined** — gbrain repairs (sync, schema, upgrade) are
  all state changes to a memory system governed elsewhere; diagnosis + proposal
  only

## Deny-list (never heal, never touch)

`~/.gbrain/config.json` (never hand-edited; never printed) · the live install at
`/home/dev-p/gbrain` · the source clone's open item (never resolve unilaterally) ·
env-managed API keys · MCP entry in `opencode.jsonc` (self-governing config) ·
any `gbrain sync`/`embed` execution without explicit developer go — sync is a
content-changing operation, not part of detection.

## Report

Write [[[mybizz-config-docs:gbrain/gbrain-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-exam-report.md): tier results, findings with class + evidence +
recommended repair, source table deltas vs spec. Overwritten every run.
