---
title: "gbrain-dream-cycle-skill"
doc-id: "mb-f8859d84"
---
# mb-config-gbrain-dream-cycle — Exam Skill

Exams the Dream Cycle's configuration state against its spec. This skill holds
the **procedure** only — expected values live in the spec doc and are read fresh
at the start of every run. The Dream Cycle is working well; this exam verifies
that and repairs nothing.

- Spec: [[gbrain-dream-cycle-config|Configuration]] — read it first, every run
- **Exam plan: [[gbrain-dream-cycle-exam-plan|Exam Plan]] — read
  second, every run.** The plan-driven cycle: the config-manager synthesizes
  this plan fresh before each run (from spec + last report + log + learnings)
  and this skill executes it in hand. The plan carries run-specifics and
  deltas; the **standing check inventory lives in this skill** (below) —
  permanent occurrences graduate here, never into plans
- Reference: [[gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]] — invocation,
  post-run verification procedure, diagnostics
- Report: [[gbrain-dream-cycle-exam-report|Exam Report]] — one file,
  overwritten each run (write-then-replace)
- Log: [[gbrain-dream-cycle-log|Log]] — one run row per exam;
  free rows for notable events witnessed between runs
- Learnings: [[gbrain-dream-cycle-learnings|Learnings]] — file new
  patterns/nuances; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the Dream Cycle**: invocation model, scheduling absence,
  provider dependency, schema-pack coupling, trigger surfaces, the recorded
  known limitation, and functional liveness of the pipeline.
- **Parent GBrain conformance** (binary, version policy, config file, schema
  pack inventory, sources, models, MCP entry, sync machinery) belongs to
  `mb-config-gbrain` — cross-reference its current report; the version echo
  (DC0-1) is the one permitted overlap, never re-probe the rest.
- **Database-level checks** (tables, ownership, embedding coverage, backups)
  belong to `mb-config-postgresql` — dream output rides GBrain's Postgres;
  backup freshness is checked there.
- **Resolved code call-graph** belongs to Graphify — `resolve_symbol_edges`
  partiality is a known limitation, verified as a state, never "fixed" here.

## Credential discipline (hard rule)

`ANTHROPIC_API_KEY` is env-only and is the Dream Cycle's one distinct
credential requirement (`extract_atoms`). Reference it **by variable name
only** — never print, log, or copy the value into reports, outputs, or
learnings. The validity curl uses the variable, never a literal. If a guard
denies the curl, the check becomes a developer-run request — honored
absolutely, never retried through an alternate path.

## Hard behavioral rules (from the suite's own Do-not list)

- Never accept a bare "N failed" summary as a diagnosis — read the real
  per-phase JSON output first, and use **`.phase`** (not `.name` — the
  documented `.name` recipe silently matched nothing).
- Never treat a completed run as proof every phase did meaningful work —
  "completed" and "worked" are not the same claim.
- Never treat 0 resolved edges from `resolve_symbol_edges` as a failure — it
  is the permanent pack limitation; a phase *error* is the failure.
- Never use `sync_freshness` as evidence a dream ran — dream and sync are
  different bookkeeping operations; a no-op dream stamps nothing.
- Check the credential FIRST for any `extract_atoms` failure — the confirmed
  cause of the one extended outage (and check for stray whitespace inside a
  recently rotated key's quoted value).
- Never run a full dream cycle to diagnose a single failing phase — isolate
  with `--phase`.
- Never re-enable the autopilot schedule or put the cycle on any scheduler —
  on-demand invocation is the deliberate design; a schedule's reappearance is
  a finding, not a convenience.
- **Never probe `--phase` bare** (run #1 incident, 2026-09-14): a bare
  `gbrain dream --phase <flagless>` does NOT parse-fail — it starts a full
  cycle. Only `--source` parse-fails safely ("missing value" before any
  execution). Never pipe live dream output to a truncating consumer
  (`head`/`tail` SIGPIPE kills the cycle mid-flight, leaving an unknown-state
  run) — capture to a file, then read the file.

## Run #1 lessons graduated (2026-09-14)

- F-1 method hardening (above): bare `--phase` starts a live cycle; safe probe
  pattern is `--phase orphans --json > /tmp/file` then read the file.
- F-2 backup second lane: DB-only dream-synthesized concept pages (122 at run
  #1) gain a real second line of defense via `gbrain export --dir <path>` in
  the weekly backup routine — destination per developer decision:
  `C:\backup-dream-cycle` (`/mnt/c/backup-dream-cycle`), alongside the weekly
  PostgreSQL dump. Estate convention update flagged to
  [[postgresql-config|Configuration]] §Backups via governance (approved at run #1 gate).

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| DC0-1 | A | `gbrain --version` | `0.46.1.0` (config §Identity — parent system). The available upgrade is a recorded open item — **never upgraded on newness**; upgrade only on check failure (DC3-2). Permitted overlap with the parent module's version check |
| DC0-2 | A | Autopilot absence: `crontab -l` carries no dream/autopilot entry; `~/.gbrain/autopilot-run.sh` absent; `~/.gbrain/autopilot.log` absent | All three absent (config §Autopilot — removed 2026-09-06, on-demand is the deliberate design). Any reappearance = DRIFT |
| DC0-3 | A | Schema pack identity (MCP) | `gbrain-everything@1.0.0`, sha8 `7021205a`, the only installed pack (config §Identity — Schema pack coupling). Mismatch = DRIFT |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DC1-1 | A→D | Anthropic credential presence: `echo ${ANTHROPIC_API_KEY:+present}` | `present` (config §Provider dependency — required, env-only). **Never print the value.** Validity: the reference's documented curl with `x-api-key: $ANTHROPIC_API_KEY` — agent-attempted; guard denial → developer bundle. A `401 authentication_error` = the confirmed outage cause → UNHEALTHY |
| DC1-2 | A | Trigger surfaces: `gbrain dream --help` | Exposes `--phase`, `--source`, `--json`, `--dry-run` (config §Identity — Trigger surfaces). A missing flag = DRIFT |
| DC1-3 | D | `mcp_surface` key absence in `~/.gbrain/config.json` (config content — sensitive-data guard class → developer bundle; agent-side soft corroboration: the memory verbs are callable on the MCP surface) | Key absent — the default surface includes the verbs (config §MEMORY_VERBS surface, reconciled 2026-09-06) |
| DC1-4 | A | `code` page type extractability in the active pack (schema explain-type) | `extractable: false` (config §Known limitation — permanent; resolve_symbol_edges returns symbol names only). If it flips to true, the limitation state changed → flag for spec refresh (progress, not a defect) |
| DC1-5 | A | Suite completeness: the seven files in `gbrain-dream-cycle/` (config, exam-plan, exam-report, log, learnings, explainer, reference) | All present (missing file = GAP) |

## Tier 2 — Functional proof (present ≠ working; read-only reporting surfaces — no brain mutation from detection)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DC2-1 | A | Single-phase functional probe: `gbrain dream --phase orphans --json`, per-phase status via `.phase` | Phase reports `ok` or `warn`; a warn **with a count is the expected healthy output** — orphans reports, it does not fix (reference §expectations; count is point-in-time, LE-1). Proves the pipeline executes for real |
| DC2-2 | A | Discipline probe: `gbrain eval suspected-contradictions --query "<a real topic from recently deepened content>"` | Runs to completion (the bare form fails exit 2 — a query is required, reference §4). Small LLM cost ($1 default budget, per-query top-5, n<30 caveat). Confirms the mandatory ungovernable-writer compensation tool works |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DC3-1 | D | Full dream cycle (`gbrain dream --json`) + the complete post-run verification procedure: per-phase capture (`.phase`), before/after `gbrain stats` delta, `gbrain doctor` freshness reading, suspected-contradictions eval with every finding reviewed | Every phase `ok`/legitimately `skipped`; real-work delta recorded (pages/chunks may move — +89 on the verified run); freshness read per the documented stamping mechanism; findings reviewed. Expensive: minutes, LLM spend, +N pages |
| DC3-2 | D | Upgrade execution (0.46.1.0 → available newer version) | Developer decision, pending; policy: **never on newness — only on check failure**. Requires coordinated cutover + DB backup first (gbrain log: upgrade advisory, no DB backup existed until 2026-09-13 — now mitigated) |

## Report

Write [[gbrain-dream-cycle-exam-report|Exam Report]]: verdict line; per-tier tables (check
ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[gbrain-dream-cycle-log|Log]] (run-row format per
[[config-manager-reference|Reference: Commands, Procedures]]); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — the Dream Cycle is part of GBrain (a memory
  system governed elsewhere); every repair is developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): `~/.gbrain/config.json` (never read by
  the agent, never printed) · env-managed API keys (name only) · the autopilot
  schedule (never re-enabled; no scheduler of any kind) · any `gbrain sync`
  execution · any full dream cycle without explicit developer go · the live
  install at `/home/dev-p/gbrain`
- Credentials: variable names only, never printed
