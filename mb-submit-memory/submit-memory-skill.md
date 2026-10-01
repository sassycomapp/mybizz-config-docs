---
title: "submit-memory-skill"
doc-id: "mb-1e60b7fc"
updated: "2026-10-01"
---
# mb-config-mb-submit-memory — Exam Skill

Exams the mb-submit-memory system's configuration state against its spec. This
skill holds the **procedure** only — expected values live in the spec doc and
are read fresh at the start of every run. The submission skill is working
well; this exam verifies that and repairs nothing.

- Spec: [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-config.md) — read it first, every run
- **Exam plan: [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-exam-plan.md) — read second,
  every run.** The plan-driven cycle: the config-manager synthesizes this plan
  fresh before each run (from spec + last report + log + learnings) and this
  skill executes it in hand. The plan carries run-specifics and deltas; the
  **standing check inventory lives in this skill** (below) — permanent
  occurrences graduate here, never into plans
- Reference: [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-reference|Reference: Usage, Invocation, and the Full Cycle]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-reference.md) — invocation,
  the full submission cycle, prerequisites
- Report: [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-exam-report.md) — one file,
  overwritten each run (write-then-replace)
- Log: [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-log|Log]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-log.md) — one run row per exam;
  free rows for notable events witnessed between runs
- Learnings: [[[mybizz-config-docs:mb-submit-memory/submit-memory-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/submit-memory-learnings.md) — file new
  patterns/nuances; delete entries once graduated into a permanent home
- The system's own operational learnings:
  `/mnt/c/mybizz/logs/mb-submit-memory/learnings.md` — read for context; the
  exam never writes there (that lane belongs to submission runs)

## Scope boundary (anti-duplication)

- This module exams **the submission skill**: the installed skill file, the
  governance-chain expectations recorded in its spec (Cupcake enforcement
  posture, MEMORY_VERBS surface, mg-grant naming), its logs lane, and the
  submission-discipline doctrine.
- **Governor internals** (binary/version, database, worker, project
  registration, start/stop) belong to `mb-config-memory-governor` —
  cross-reference its current report, never re-probe.
- **Cupcake conformance** (binary, policy inventory, rule liveness) belongs to
  `mb-config-cupcake` — cross-reference, never re-probe. The loopback
  exemption is watched HERE only as the load-bearing dependency this spec
  records, never as a Cupcake health check.
- **GBrain surface mechanics** (binary, sources, sync) belong to
  `mb-config-gbrain` — cross-reference, never re-probe. The recall probe
  (SM2-2) is the one permitted overlap: it proves the detect surface this
  skill depends on, not gbrain's health.

## Credential discipline (hard rule)

Two credentials exist for governed submissions — `manual_submission` and
`pdlf_step_sync` — and they are referenced **by name only**: never printed,
logged, or copied into reports, outputs, or learnings. The governor's `.env`
is never read, never printed. Agent-side `.env` sourcing for a credentialed
call is a **proven permanent guard-denial class** (2026-09-14): the pattern is
bundle-handoff — the agent composes the exact command bundle (credential by
variable name), the developer executes it in WSL, and results return verbatim
as developer-verified. If a guard denies any check, the denial is honored
absolutely — never retried through an alternate path; the check becomes a
developer-run request bundled into ONE request at the gate.

## Hard behavioral rules (from the suite's own Do-not lists)

- Never call `gbrain remember` or `gbrain sync` for anything meant to be
  governed — that is the ungoverned quick path this skill exists to replace;
  the exam never uses it, not even "just to test".
- Never resolve or resubmit an `under_review` item; the review queue is
  developer-owned. `under_review` is a healthy reported outcome, not an error.
- Never assign a placeholder or default confidence score — in any exam
  artifact or anywhere else.
- Never submit a folder in one call or share one judgment across files —
  the per-file judgment doctrine is watched here, never violated by the exam.
- Never edit the installed subject skill
  (`~/.config/opencode/skills/mb-submit-memory/SKILL.md`) — the exam reads it.
- Never remove the Cupcake loopback exemption — it is the load-bearing rule
  that permits the API path under active enforcement.
- Never start or stop the governor agent-side — developer-run; the documented
  startup procedure lives in the reference.
- Never conflate `mg-grant` / `mg-revoke` (Cupcake's cross-project grant
  tools) with anything in the memory-governor system.
- Grant discipline (prompt amendment 2026-09-15): a Cupcake block → request
  the grant from the developer in chat; the agent never issues a grant
  request and then grants the authority itself.
- Project-local facts are NOT recallable via `gbrain call recall` in
  0.46.1.0 (`include_private` is not honored through the call path) — a zero
  total on a private-fact phrase is expected behavior, not a failure; probe
  with phrases known to exist in world-visible content.

## Run #1 lessons graduated (2026-09-15)

- L-1: the gbrain CLI prints an `UPGRADE_AVAILABLE 0.46.1.0 0.50.0.0` banner
  on stdout ahead of real output on several commands (`config get`,
  `call recall` — observed run #1). Probe consumers expect and skip the
  banner; it is never a probe failure.
- L-2: `gbrain call recall`'s grep arm returning `total: 0` on a world-fact
  phrase can reflect an all-private fact inventory (operational learning #7
  corollary) — the surface is proven by the clean envelope (protocol_version,
  exit 0), never by a nonzero count. Never improvise a stronger probe outside
  the plan to "get a nonzero".

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| SM0-1 | A | Installed skill present: `~/.config/opencode/skills/mb-submit-memory/SKILL.md` exists, frontmatter `name: mb-submit-memory` | Present, name matches (config §Identity). Absent = DOWN |
| SM0-2 | A | File size vs the spec's recorded fingerprint | 13,502 B (config §Identity, single file). Mismatch = DRIFT vs spec → spec flagged (the skill may have legitimately changed; the spec fingerprint is the only repo-side anchor — see W-5) |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SM1-1 | A | Suite completeness: the eight files in `mb-submit-memory/` (config, exam-plan, exam-report, log, learnings, explainer, reference, skill source) | All present (missing file = GAP) |
| SM1-2 | A | MEMORY_VERBS surface: `gbrain config get mcp_surface` | `verbs` (config §Governance chain, verified 2026-09-08). Cross-watch W-6: the dream-cycle spec records key-absent default (2026-09-06) — a live result disagreeing with either spec is flagged to docs governance at the gate; the exam edits neither |
| SM1-3 | A | Governor API listening: `ss -tlnp \| grep 8321` | Listening on `127.0.0.1:8321` (config §Downstream — ACTIVE). Not listening = DOWN; hand the documented startup procedure to the developer, never start agent-side |
| SM1-4 | A | Run-logs lane per config §Logs: `/mnt/c/mybizz/logs/mb-submit-memory/` holds run log(s) + `learnings.md` | Present. Count vs the spec's recorded "one run log + 6 entries" — live growth (two + eight as of 2026-09-15) is normal operation = spec-progress DRIFT → flag W-4 to docs governance at the gate |
| SM1-5 | A | Spec §Identity mirror claim vs reality: does a repo-side byte-identical copy of the installed skill exist as the spec records? | Reality 2026-09-15: no — `submit-memory-skill.md` is the exam-skill source (developer instruction); the subject skill has no repo-side mirror. Finding = GAP (spec claim superseded) → spec correction flagged at the gate; hash anchor reverts to the spec fingerprint (SM0-2) until the developer decides otherwise |

## Tier 2 — Functional proof (present ≠ working; read-only surfaces — no governed content is created or changed by detection)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SM2-1 | A | Auth-gate probe: `curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8321/memory/candidate` (unauthenticated, loopback — permitted by the amended outbound-network rule) | `422` (auth-gates unauthenticated calls correctly — config §Downstream, observed live). `200`/`201` without a credential = UNHEALTHY (auth posture broken — escalate immediately, never probe with a credential); connection refused = DOWN |
| SM2-2 | A | Detect-surface probe: `gbrain call recall '{"grep": "<a real phrase from world-visible content>"}'` | Command succeeds and returns real results (the detect step's proven command form). Zero total on a private-fact phrase is expected (hard rule above), not a failure |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SM3-1 | D | Credentialed `owning_project` verification: enumerate the governor's project/candidate rows with the `manual_submission` credential (name only) and compare against `gbrain sources list` (config §Naming drift open item) | Every `owning_project` carrying submissions has an exactly-matching gbrain source. Agent composes the exact bundle; developer executes in WSL; results return verbatim (developer-verified) |
| SM3-2 | D | Permanent auto-start installation: systemd enabled in WSL + the governor installed as an auto-start, auto-restart service (config §Downstream — recommended and approved 2026-09-08, pending execution) | Service present, enabled, restarted clean. Boot-config change → permanently developer-run |
| SM3-3 | D | Stray `0.48.2.0` file deletion in the governor repo root (origin unconfirmed, likely shell artifact of 2026-09-06; restricted folder) | File gone; repo clean. Developer-run |

## Report

Write [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-exam-report.md): verdict line; per-tier tables (check
ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-log|Log]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-log.md) (run-row format per
[[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings filed to
[[[mybizz-config-docs:mb-submit-memory/submit-memory-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/submit-memory-learnings.md).

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **Agent-healable items:** suite-folder file repairs only (the skill source
  and the suite's transient files sit outside docs governance). Everything
  else is developer-run or proposed — the submission skill is working well
- Spec-doc corrections → flagged to docs governance, never applied here
  (expected flags this cycle: W-4 logs staleness, W-5 mirror claim superseded,
  W-6 cross-spec `mcp_surface` contradiction)
- Deny-list (never heal, never touch): the governor's `.env` (never read,
  never printed) · credential values (`manual_submission`, `pdlf_step_sync` —
  names only) · the developer review queue (never resolved, never resubmitted
  agent-side) · the installed subject skill file (read, never edited) · the
  governor's database (no data mutations) · the ungoverned quick path
  (`gbrain remember` / `gbrain sync` for governed content) · governor
  start/stop (developer-run) · any real governed submission without explicit
  developer go (content-changing)
- Credentials: variable names only, never printed
