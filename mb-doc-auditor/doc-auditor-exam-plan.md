---
title: "doc-auditor-exam-plan"
doc-id: "mb-a16fd4f1"
---
# mb-doc-auditor — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager
before each run from: [[doc-auditor-config|Configuration]] (spec), the last
[[doc-auditor-exam-report|Exam Report]], [[doc-auditor-log|Log]] (events since
last run), [[doc-auditor-learnings|Learnings]]. Consumed by the skill at run
time; rewritten at the start of the following cycle. The file is live; its
contents are transient.

**This first plan is hand-written** (emulation of the proven cycle): it also
serves as the format template. The **standing check inventory lives in the
skill** ([[doc-auditor-skill|Doc Auditor Skill]], born-with-inventory); this
plan carries run-specifics and references. Once verified by a run, future plans
carry run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | 2026-09-26 |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution ([[config-manager-log|Config Manager Log]]) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request at the gate) | (a) Tier 3 unlock decision (DA3-1 full live audit walkthrough; DA3-2 refusal-class live suite incl. the `anvil.yaml` class rule — the agent cannot create an `anvil.yaml` fixture by policy; DA3-3 repair apply-class on corpus copies); (b) any check whose command text a guard denies; (c) none else anticipated |
| Expected-value source of truth | [[doc-auditor-config|Configuration]] — read fresh at run start; never rely on remembered values |
| Named state-change steps (Amendment: procedural conflicts stated, not asked) | **S-1 (2026-09-26):** the config-manager register carried no `mb-doc-auditor` row — added by named plan step in state `WIP` (spec doc `mb-doc-auditor/doc-auditor-config.md` exists; examinable), citing the developer instruction "execute phase 8" (2026-09-26) and the doc-maintainer S-1 precedent (2026-09-25); the row flips `WIP` → `Installed` at Phase 2 per the setup prompt. **S-2 (2026-09-26):** grant discipline — the 2026-09-15 amendment governs this session (no superseding standing session instruction has been given): when a guard denies, the agent requests the grant in chat and the developer executes it; denials are never worked around. (The doc-maintainer run's agent-applies-directly S-2 applied to that session only.) |
| Scope boundary | `mb-config-doc-maintainer` owns the maintainer system (watcher, queue, scheduled task, its tools and run-log discipline) — this exam reads ONLY the run-log artifact as the auditor's evidence input (recorded state, never the maintainer's internals). The contract's content (`gbrain/gbrain-doc-contract.md`) is governance — artifact state only. The scope authority (`mybizz-scope-list.md`) is read live as a probe; its content is never audited here. The audit record's content belongs to the auditor's own domain — this exam checks the artifact's recorded state, never re-audits what audits found. DocCycle is out of scope entirely. Corpus documentation governance (register membership as content policy) belongs to the documentation-management side — this exam verifies recorded rows only. GBrain source registration for the auditor is spec open item #2 — the not-registered state is expected; no registration is performed by the exam (state change, developer-gated) |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec open items kept under
watch (observations, not findings):

| # | Watch item (spec open items) | This run's action |
|---|---|---|
| W-1 | Spec open item #1: nested-corpus registration convention (path-derived compound doc-ids vs bare stems) — detection heuristic works; the convention awaits a developer decision | Confirm the refusal behavior is live (DA2-3 on a real scope where multi-stems exist); no convention decided by the exam |
| W-2 | Spec open item #2: GBrain source registration for `mb-doc-auditor` not yet applied | DA1-10 verifies the not-registered state matches the spec (divergence either way = DRIFT) |
| W-3 | Spec open item #3: first-live-audit outstanding items carried in `doc-auditor-records.md` (README stem-collision ×5, 12 broken WikiLinks, 9 legacy-schema rows) | Confirm the record carries them (DA1-5); they remain the auditor's own domain, never exam work |
| W-4 | Spec open item #4: live-session confirmation of skill discovery (convention-verified 2026-09-25) | DA0-1 verifies the installed artifact; the running session's own skill list carries `mb-doc-auditor` (observed 2026-09-26) — closing evidence available for the developer's disposition |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-25 Phase 2 live smokes: real-corpus evidence (11 missing registrations, 105 obsolete rows, 27 collisions in project-library-global) | DA2-3 exercises `check` live on a small bounded root — the classification path runs on real data |
| LG-2 | 2026-09-25 developer commits + pushes (42b3391 / 5447954 / 5a55066); sync launched | DA1-1 verifies the source repo state matches the spec (origin, HEAD `aa91ff7`, clean) |
| LG-3 | 2026-09-25 Phase 5: audit record created + registered; 6 mechanical repairs applied and verified | DA1-5 verifies the record artifact (frontmatter + register row); no new probe derived (one clean build event) |
| LG-4 | 2026-09-26 S-1: register row added (WIP) | Phase 2 flips it; DA1-2 hash pair recorded at install |

## 5. Learnings-driven items

None — bootstrap (the learnings table is empty at first plan synthesis).

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[doc-auditor-skill|Doc Auditor Skill]] (Tiers 0–3).
Summary:

- **Tier 0 (A) — invocability:** DA0-1 installed subject skill present + functional frontmatter · DA0-2 tool modules compile
- **Tier 1 (A) — state conformance:** DA1-1 source repo remote/HEAD/tree · DA1-2 subject-skill hash pair + body identity (dual-format) · DA1-3 tools + 22/22 tests · DA1-4 suite completeness (8-file standard + spec-recorded record co-resident) · DA1-5 audit record state (frontmatter + register row) · DA1-6 suite-doc register rows · DA1-7 contract artifact state · DA1-8 scope authority present · DA1-9 run-log evidence input present (absent = normal state, noted) · DA1-10 gbrain source row = not registered (spec open item #2)
- **Tier 2 (A) — functional, present ≠ working (read-only only):** DA2-1 `scope.py paths` + `validate` live · DA2-2 `runlog.py summary` live + absent-path handling · DA2-3 `audit.py check` live on a bounded root · DA2-4 `audit.py repair` dry-run, byte-proof of zero change · DA2-5 `gbrain_reader.py sources` live read-only
- **Tier 3 (D, locked):** DA3-1 full live audit walkthrough on a real library root (end-to-end: scope parsed live, run-log evidence consumed, per-finding classification, safe repairs per automation boundary, record block append, terminal state) · DA3-2 refusal-class live suite (collision stems, multiply-occurring stems, obsolete-row-outside-library-root, structurally unrepairable frontmatter; `anvil.yaml` class rule at existence-check level only) · DA3-3 repair apply-class on corpus copies (frontmatter restore + register add/retire, byte-preservation proof)

## 7. Report requirements

The run writes [[doc-auditor-exam-report|Exam Report]]: verdict line; per-tier
tables (check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[doc-auditor-log|Log]] (run-row
format per [[config-manager-reference|Reference: Commands, Procedures]]); new
learnings filed.

## 8. Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- Agent-healable: suite-file repairs only (config-manager standard); everything
  else developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the subject `SKILL.md` + its source ·
  `gbrain-doc-contract.md` · the scope authority (governance — read live,
  never edited) · `anvil.yaml` (never created, read, or touched) · env
  credentials (name only) · any `gbrain sync` execution or G-brain write ·
  the audit record's existing blocks (append-only — never rewritten by the exam)
- Tier 3 unlock decision asked at the gate, never assumed
- Credentials: variable names only, never printed
