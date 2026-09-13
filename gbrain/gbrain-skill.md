---
name: mb-config-gbrain
description: GBrain configuration exam — verifies the live GBrain system (CLI version, config, schema pack, 13 registered sources, MCP integration, sync state) against gbrain-config.md, catches silent failures, proposes gated repairs. Use when asked to "exam gbrain", "check gbrain health/config", or as part of a full mb-config-manager run.
---

# mb-config-gbrain — Exam Skill

Exams the live GBrain system against its spec. This skill holds the **procedure**
only — expected values live in the spec doc, read fresh at the start of every run.

- Spec: `gbrain/gbrain-config.md` — read it first, every run
- Reference: `gbrain/gbrain-reference.md`
- Report: `gbrain/gbrain-exam-report.md` — one file, overwritten each run
- Learnings: `gbrain/gbrain-learnings.md`

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

## Tier 0 — Liveness (run first; failure = report `DOWN`, stop)

- Binary resolves: `/home/dev-p/.bun/bin/gbrain` exists; `/home/dev-p/gbrain/VERSION`
  readable
- Engine responds: brain identity returns (CLI `gbrain status` / MCP identity call) —
  reports version + counters without error
- DB ping on `gbrain` database (same probe as postgres Tier 0)

## Tier 1 — Health

- `gbrain sources list` — all 13 spec sources present, each path exists on disk,
  page counts sane
- Sync freshness — spec records sync dates; the gap between then and now is
  **expected growth**, not drift — record only anomalies (a source whose page count
  shrank to zero, a path gone missing)
- Embedding pipeline alive — coverage check exists in the postgres module report;
  confirm its current result is 100% (read its report, do not re-probe)
- No scheduled jobs: crontab contains no gbrain entries (removed by design 2026-09-06;
  any reappearance = finding)
- Legacy artifact `~/.gbrain/brain.pglite` — record presence **or absence**: absence
  is a spec-drift flag (docs governance refresh), not a system fault — it was the
  documented stale artifact. It was found absent 2026-09-12 (first exam run).

## Tier 2 — State conformance (spec comparison)

- Version: live `0.46.1.0` vs upstream available — **not a failure by policy**
  (upgrade only on check failure); record the gap, never upgrade on newness
- Schema pack: `gbrain-everything@1.0.0`, sha8, 30 page types / 12 link types
- `~/.gbrain/config.json`: `self_upgrade_mode: notify`; **no API keys inside**
  (keys-in-env rule); database URL present
- MCP integration: `~/.config/opencode/opencode.jsonc` entry `mcp.gbrain` →
  `["/home/dev-p/.bun/bin/gbrain", "serve"]`, enabled true, env carries
  OPENAI_API_KEY / ZEROENTROPY_API_KEY by name
- Models: embedding `openai:text-embedding-3-large`, chat `openai:gpt-5.2`
- Skills bundle: 60 gbrain-pack skills + exactly one `skillify` at
  `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/`
- Open items (spec): source-clone staleness at `/mnt/c/mybizz/gbrain` — expected
  open, not a finding

## Tier 3 — Deep pass (developer-run; detection-only unless unlocked)

- Full sync verification run (`gbrain sync --source <id>` on a sample) — writes;
  needs go-ahead
- MCP server restart behavior (config changes need full process restart)
- Upgrade decision (policy question — developer's)

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

Write `gbrain-exam-report.md`: tier results, findings with class + evidence +
recommended repair, source table deltas vs spec. Overwritten every run.