---
title: "mb-memory-system-diagnostic-exam-plan"
doc-id: "mb-memory-system-diagnostic-exam-plan"
---
# mb-memory-system-diagnostic — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager
before each run from:
[[mb-memory-system-diagnostic-config|Configuration]] (spec), the last
[[mb-memory-system-diagnostic-exam-report|Exam Report]],
[[mb-memory-system-diagnostic-log|Log]] (events since last run),
[[mb-memory-system-diagnostic-learnings|Learnings]]. Consumed by the skill at
run time; rewritten at the start of the following cycle. The file is live; its
contents are transient.

**This first plan is hand-written** (emulation of the proven cycle): it also
serves as the format template. The **standing check inventory lives in the
skill** ([[mb-memory-system-diagnostic-skill|Exam Skill source]],
born-with-inventory); this plan carries run-specifics and references.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | 2026-09-28 |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution ([[config-manager-log|Config Manager Log]]) |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request at the gate) | (a) Tier 3 unlock decision (MS3-1 read-only deep audit of the installed copy + recorded constants vs live sibling-suite records; MS3-2 cross-suite constant verification against gbrain-config / memory-governor-config / postgresql-config / graphify-config / gbrain-dream-cycle-config current state); (b) any check whose command text a guard denies; (c) none else anticipated |
| Expected-value source of truth | [[mb-memory-system-diagnostic-config|Configuration]] — read fresh at run start; never rely on remembered values |
| Named state-change steps (Amendment: procedural conflicts stated, not asked) | **S-1 (2026-09-28):** the config-manager register carried no `mb-memory-system-diagnostic` row — added by named plan step in state `WIP` (spec doc `mb-memory-system-diagnostic/mb-memory-system-diagnostic-config.md` exists; examinable), citing the developer instruction "Run mb-config-manager on mb-memory-system-diagnostic" (2026-09-28) and the doc-maintainer S-1 precedent (2026-09-25) / doc-auditor S-1 precedent (2026-09-26); the row flips `WIP` → `Installed` at Phase 2 per the setup prompt. **S-2 (2026-09-28):** grant discipline — the 2026-09-15 amendment governs this session: when a guard denies, the agent requests the grant in chat and the developer executes it; denials are never worked around (first instance already recorded: mg-grant count 12 issued for suite writes). |
| Scope boundary | This module exams **the diagnostic skill itself**: its source artifact and installed copy (identity, hash pair, frontmatter formats), its suite documents and register rows, its recorded constants (62/62 RLS, high-risk category list, heavyweight-gate inventory, report path, GBrain-ingest state), and its invocation surface. **The six memory-ecosystem components** (GBrain, PostgreSQL Instance B, Memory Governor, mb-submit-memory, Graphify, Dream Cycle) belong to their own `mb-config-*` exam modules — this exam never re-tests them live; it verifies only that the diagnostic's recorded constants match those suites' current recorded state. **Running the diagnostic itself is out of exam scope** — it is a heavyweight, developer-invoked procedure (§4/§5/§10 real-write sections); the exam verifies its install and state, never executes it. Cupcake internals are out of scope entirely (the exam, like the subject skill, never touches them). PostgreSQL Instance A / `pdlf` is out of scope entirely. |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec open items kept under
watch (observations, not findings):

| # | Watch item (spec open items) | This run's action |
|---|---|---|
| W-1 | Spec open item #1: register rows for the suite's four documents — pending doc-maintainer; creation events absent from the queue | DA1-7 verifies the recorded absence (register-local + queue); registration itself is doc-maintainer's work, never the exam's |
| W-2 | Spec open item #3: report folder `C:\mybizz\memory-diagnostic-reports\` absent — created by the first run | DA1-8 verifies the recorded state; creation is the diagnostic run's job, not the exam's |
| W-3 | Spec open item #4: "First live run of the skill — not yet executed" vs git/log evidence of a live 2026-09-28 run (§2/§3/§4/§5) — **spec staleness suspected** | Flag to the developer at the gate (spec correction is a gated docs-governance action, never exam-applied); evidence: suite log row 2026-09-28, skill §3/§4 live-verified notes, memory-governor suite's same-day records |
| W-4 | Spec open item #5: no `mb-config-*` module for this suite | Closed by this very build — flip recorded at the gate after install |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-09-28 live diagnostic run (§2–§5) produced skill-embedded implementation notes (journald paths, /tmp/opencode script pattern, tracked-file rule) | DA1-4 confirms the source artifact carries them; no new probe derived (one clean build event) |
| LG-2 | 2026-09-28 rename + re-install + credential sweep + gbrain ingest at `c0570db` | DA1-2 (hash pair + body identity), DA1-9 (ingest state vs live `gbrain sources`) |
| LG-3 | 2026-09-28 S-1 register row + mg-grant issued | Phase 2 flips the row; hash pair recorded at install |

## 5. Learnings-driven items

None — bootstrap (the learnings table is empty at first plan synthesis).

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in the [[mb-memory-system-diagnostic-skill|exam skill source]]
(Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** MS0-1 installed subject skill present with functional frontmatter (`name: mb-memory-system-diagnostic` + description) · MS0-2 skill discoverable in the OpenCode skill surface (name listed)
- **Tier 1 (A) — state conformance:** MS1-1 source artifact format (two-field frontmatter, `-skill.md` stem naming) · MS1-2 hash pair + body identity from H1 (dual-format) · MS1-3 suite completeness (4-file current state; exam set joins at build — 9 files after) · MS1-4 scope table conformance (in-scope/out-of-scope rows match the spec) · MS1-5 section inventory conformance (11 sections, gate classes as recorded) · MS1-6 recorded constants present in the source artifact (62/62 RLS, HIGH_RISK_TYPES five-category list, HTTP 422, ≤7-day backup age) · MS1-7 register-local recorded absence (open item #1) · MS1-8 GBrain ingest state matches the spec (source `mybizz-config-docs`, ingest date, page counts)
- **Tier 2 (A) — functional proof (present ≠ working; read-only only):** MS2-1 installed copy readable and frontmatter-parsable by the discovery surface · MS2-2 the skill's section-command inventory is executable *in form* (command strings parse — binaries present: gbrain, psql, jq, sha256sum; nothing executed beyond `--version`-class probes) · MS2-3 report-path parent viability (`C:\mybizz\` exists; the reports folder itself correctly absent per open item #3) · MS2-4 cross-suite recorded-constant spot-check (RLS 62/62 row still current in postgresql-config; heavyweight inventory still matches the spec's Gates table)
- **Tier 3 (D, locked):** MS3-1 read-only deep audit — full source-vs-spec paragraph-level conformance walk · MS3-2 cross-suite constant verification against all five sibling suites' current recorded state

## 7. Report requirements

The run writes
[[mb-memory-system-diagnostic-exam-report|Exam Report]]: verdict line; per-tier
tables (check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to
[[mb-memory-system-diagnostic-log|Log]] (run-row format per
[[config-manager-reference|Reference: Commands, Procedures]]); new learnings
filed.

## 8. Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- Agent-healable: suite-file repairs only (config-manager standard); everything
  else developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the subject `SKILL.md` and its source ·
  the sibling suites' config documents (cross-checked, never edited) · env
  credentials (name only — the skill's own hard rule binds the exam) · any
  `gbrain sync` execution or G-brain write · the memory-ecosystem components
  themselves (no live component probing beyond `--version`-class form checks)
- Tier 3 unlock decision asked at the gate, never assumed
- Credentials: variable names only, never printed
