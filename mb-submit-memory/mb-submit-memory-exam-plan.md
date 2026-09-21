---
document: "mb-submit-memory — Exam Plan"
doc-id: mb-submit-memory-exam-plan
state: Live
date-created: 2026-09-15
---

# mb-submit-memory — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[mb-submit-memory-config|Configuration]] (spec), the last
[[mb-submit-memory-exam-report|Exam Report]], [[mb-submit-memory-log|Log]] (events since last
run), [[submit-memory-learnings|Learnings]]. Consumed by the skill at run time; rewritten
at the start of the following cycle. The file is live; its contents are transient.

**This first plan is hand-written** (emulation of the PostgreSQL architecture): it
also serves as the format template. The **standing check inventory lives in the
skill** ([[submit-memory-skill|Submit Memory Skill]], born-with-inventory); this plan carries
run-specifics and references. Once verified by a run, future plans carry
run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) any check whose command text the guards deny — proven permanent classes for this system: agent-side `.env` sourcing for the submission credential; credentialed API calls; (b) if Tier 3 unlocked: SM3-1 / SM3-2 / SM3-3 |
| Expected-value source of truth | [[mb-submit-memory-config|Configuration]] — read fresh at run start; never rely on remembered values |
| Scope boundary | Parent `mb-config-memory-governor` owns the governor's internals (binary/version, database, worker, project registration) — cross-reference its current report, never re-probe; `mb-config-cupcake` owns Cupcake conformance — cross-reference, never re-probe; `mb-config-gbrain` owns gbrain surface mechanics — cross-reference. **This module owns:** the subject skill's configuration state, the governance-chain expectations recorded in its spec, the suite's own files, and the submission-discipline doctrine |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states and Phase 0
observations kept under watch (observations, not findings):

| # | Watch item (spec open items / Phase 0) | This run's action |
|---|---|---|
| W-1 | Governor-side `owning_project` verification — pending credentialed API call (spec §Naming drift) | SM3-1 when Tier 3 unlocked; else stays open with runner D recorded |
| W-2 | Permanent auto-start (systemd migration) — approved, pending developer execution (spec §Downstream) | SM3-2 when unlocked; else stays open, developer-run |
| W-3 | Stray `0.48.2.0` file in the governor repo — pending developer deletion (restricted folder) | SM3-3 when unlocked; else stays open, developer-run |
| W-4 | Spec §Logs staleness: spec records one run log + 6 learnings entries (verified 2026-09-08); live shows two run logs + 8 entries | Count live (SM1-4); mismatch = spec progress → flag to docs governance at the gate, never edited here |
| W-5 | Spec §Identity mirror claim (byte-identical mirror, 2026-09-05, 13,502 B) vs an empty file — superseded 2026-09-15 by developer instruction: the slot is now the exam-skill source | Verify reality (SM1-5); spec correction flagged at the gate; the subject skill's repo-side hash anchor is lost until the developer decides otherwise (recorded gap, not silently accepted) |
| W-6 | Inter-spec contradiction (candidate): this spec §Governance chain records `mcp_surface` → `verbs` (verified 2026-09-08); the dream-cycle spec (reconciled 2026-09-06) records **no** `mcp_surface` key with the verbs in the default surface | Probe live (SM1-2); whichever state holds, the disagreeing spec is flagged to docs governance at the gate — never edited here |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| SM-L1 | 2026-09-08 governor found down — startup coupling (`.env` sourced first, no dotenv autoload; without it every submission 401s) | Knowledge check: reference carries the exact start procedure and the never-read-`.env` rule; no live probe (governor process state belongs to the parent module) |
| SM-L2 | 2026-09-08 outbound-network rule amended — loopback always allowed; the skill's API path permitted | Check: reference §Prerequisites carries the do-not-remove note; Cupcake live conformance cross-referenced to `mb-config-cupcake`'s current report, never re-probed here |
| SM-L3 | 2026-09-14 agent-side `.env` sourcing for the submission credential proven a permanent guard-denial class | Embedded doctrine: every credentialed row is runner D; bundle-handoff pattern (developer executes, results return verbatim as developer-verified) |
| SM-L4 | 2026-09-14 world-visibility submissions route to `needs_review`; `under_review` outcomes left to the developer's review queue | Check: skill and reference carry the under_review doctrine intact (report plainly, never resolve, never resubmit to force promotion) |

## 5. Learnings-driven items

None yet — bootstrap (suite learnings empty at build time; the system's eight
operational learnings are distilled into the skill's hard behavioral rules, not
re-listed here). Cross-cutting learnings (guard classes, graduation rules) live in
the orchestrator's own [[config-manager-learnings|Learnings]], not here.

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[submit-memory-skill|Submit Memory Skill]] (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** SM0-1 installed skill present, frontmatter name `mb-submit-memory` · SM0-2 file size vs spec §Identity recorded fingerprint (13,502 B at spec date)
- **Tier 1 (A/D) — state conformance:** SM1-1 suite completeness (8 files) · SM1-2 MEMORY_VERBS surface (spec: `verbs`; W-6 cross-spec watch) · SM1-3 governor API listening on `127.0.0.1:8321` · SM1-4 run-logs directory per spec §Logs (W-4) · SM1-5 mirror claim vs reality (W-5)
- **Tier 2 (A) — functional, present ≠ working:** SM2-1 unauthenticated auth-gate probe → **422** (safe, read-only; proven live 2026-09-15) · SM2-2 detect-surface probe: `gbrain call recall` grep with a real phrase from real content (read-only)
- **Tier 3 (D, locked):** SM3-1 credentialed `owning_project` check (credential `manual_submission`, name only) · SM3-2 systemd auto-start installation · SM3-3 stray `0.48.2.0` deletion (restricted folder)

## 7. Report requirements

The run writes [[mb-submit-memory-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs never
touch the prior report; written before any pruning). Then: one run row appended to
[[mb-submit-memory-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **Agent-healable items:** suite-folder file repairs only (the `-skill.md` source
  and the suite's transient files sit outside docs governance). Everything else is
  developer-run or proposed — the skill itself is working well
- Spec-doc corrections → flagged to docs governance, never applied here (W-4, W-5,
  W-6 are the expected flags)
- Deny-list (never heal, never touch): the governor's `.env` (never read, never
  printed) · credential values (names only: `manual_submission`, `pdlf_step_sync`)
  · the developer review queue (never resolved, never resubmitted agent-side) ·
  the installed subject skill file `~/.config/opencode/skills/mb-submit-memory/SKILL.md`
  (the exam reads it, never edits it) · the governor's database (no data
  mutations) · the ungoverned quick path (`gbrain remember` / `gbrain sync` for
  governed content — the exam never uses it) · governor start/stop (developer-run;
  the startup procedure lives in the reference) · any real governed submission
  without explicit developer go (content-changing)
- Credentials: variable names only, never printed
