---
title: "doc-maintainer-exam-plan"
doc-id: "mb-0dc13c83"
---
# mb-doc-maintainer — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager
before each run from: [[doc-maintainer-config|Configuration]] (spec), the last
[[doc-maintainer-exam-report|Exam Report]], [[doc-maintainer-log|Log]] (events
since last run), [[doc-maintainer-learnings|Learnings]]. Consumed by the skill
at run time; rewritten at the start of the following cycle. The file is live;
its contents are transient.

**This first plan is hand-written** (emulation of the proven cycle): it also
serves as the format template. The **standing check inventory lives in the
skill** ([[doc-maintainer-skill|Doc Maintainer Skill]], born-with-inventory);
this plan carries run-specifics and references. Once verified by a run, future
plans carry run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | 2026-09-25 |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution (config-manager-log.md) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request at the gate) | (a) Tier 3 unlock decision (DM3-1 live drain; DM3-2 exclusion fixture test incl. `anvil.yaml` — the agent cannot create an `anvil.yaml` fixture by policy); (b) any check whose command text a guard denies; (c) none else anticipated |
| Expected-value source of truth | [[doc-maintainer-config|Configuration]] — read fresh at run start; never rely on remembered values |
| Named state-change steps (Amendment: procedural conflicts stated, not asked) | **S-1 (2026-09-25):** the config-manager register carries no `doc-maintainer` row — a named step adds it in state `WIP` (spec doc `doc-maintainer/doc-maintainer-config.md` exists; examinable), citing developer instruction "Run mb-config-manager on mb-doc-maintainer" (2026-09-25); the row flips `WIP` → `Installed` at Phase 2 per the setup prompt. **S-2 (2026-09-25):** grant discipline — the 2026-09-15 amendment has the agent request grants from the developer; the developer's standing session instruction (2026-09-25) supersedes it for this session: the agent applies `mg-grant --path <folder> --count N` directly, batched, 1 slip per write |
| Scope boundary | Parent `mb-config-gbrain` owns GBrain binary/version/models/schema-pack/MCP/sync conformance — this exam reads only the source row's existence/federated/lag/coverage (DM1-6, permitted overlap). DB-level checks belong to `mb-config-postgresql`. Corpus documentation governance (register membership as content policy) belongs to the documentation-management side — this exam checks recorded rows only. The retired doccycle-adjacent skills are out of scope entirely |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states kept under watch
(observations, not findings):

| # | Watch item (spec open items) | This run's action |
|---|---|---|
| W-1 | Spec open item #1: register rows for the three suite docs absent from the config-docs register (stipulation excluded them) | DM1-9 executes the row check; expected GAP finding → gate |
| W-2 | Spec open item #2: code ingestion (`--strategy code`) not applied — markdown-only stands | Confirm via DM1-6 (1 page, no code chunks); no probe of strategy change (state change, developer-gated) |
| W-3 | Spec open item #3: live verification covers one modification event; creation/move/deletion proven on corpus copies only | Noted; DM3-1 is the designed closer when unlocked |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | Build-period tool defects (register separator/unpack, repair compliance, BOM, PS 5.1 ASCII) — all fixed and tested before live use | DM1-3 executes the regression (40/40); the ASCII rule is a hard behavioral rule in the skill |
| LG-2 | 2026-09-25 scheduled-task UserId registration error, fixed (userless AtLogOn) | DM0-1/DM1-4 verify the live task and its settings |
| LG-3 | 2026-09-25 first live run (repo-organization.md) — clean | DM1-5 verifies the run-log row landed; no new probe derived (one clean event) |
| LG-4 | Any queued events at run time | DM1-10 well-formedness + DM2-2 self-exclusion check |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | Point-in-time semantics: queue contents, lag, and page counts move with real activity — exact equality never asserted, explainability required | DM1-6 lag reading and DM1-10 interpreted as point-in-time, not exact-match |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[doc-maintainer-skill|Doc Maintainer Skill]] (Tiers 0–3).
Summary:

- **Tier 0 (A) — invocability:** DM0-1 task state Running · DM0-2 one watcher process live · DM0-3 queue dir + run-log exist
- **Tier 1 (A) — state conformance:** DM1-1 repo remote/HEAD/tree · DM1-2 installed-subject-skill hash pair · DM1-3 tools compile + 40/40 tests · DM1-4 task settings · DM1-5 run-log state + register row · DM1-6 gbrain source row · DM1-7 suite completeness (8 files) · DM1-8 contract artifact state · DM1-9 suite-doc register rows (anticipated GAP) · DM1-10 queue well-formedness
- **Tier 2 (A) — functional, present ≠ working:** DM2-1 frontmatter tool execution probe · DM2-2 watcher functional + self-exclusion proof · DM2-3 register tool read-only probe
- **Tier 3 (D, locked):** DM3-1a–g full live drain — pre-state capture per event, per-event walkthroughs with per-event tool evidence and §9 summaries, §20 checklist item-by-item, register four-event discipline under live load, run-log append-only byte-proof, queue drain verification, termination discipline · DM3-2a–e exclusion suite — every exclusion class with live fixtures (incl. the `anvil.yaml` class rule, developer-built fixture), coalescing under load, lifecycle churn, crash-restart resilience, scope-authority-read-live

## 7. Report requirements

The run writes [[doc-maintainer-exam-report|Exam Report]]: verdict line;
per-tier tables (check ID, expected, actual, result); findings with class +
evidence + recommended repair + risk; runner attribution for every deferred
item (guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[doc-maintainer-log|Log]] (run-row
format per [[config-manager-reference|Reference: Commands, Procedures]]); new
learnings filed.

## 8. Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- Agent-healable: suite-file repairs only (config-manager standard); everything
  else developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the subject `SKILL.md` + source ·
  `gbrain-doc-contract.md` · `anvil.yaml` · env credentials · any `gbrain sync`
  execution · the scheduled task's definition (mutation only via developer
  gate) · `~/.gbrain/config.json` and all credential values
- Tier 3 unlock decision asked at the gate, never assumed
- Credentials: variable names only, never printed