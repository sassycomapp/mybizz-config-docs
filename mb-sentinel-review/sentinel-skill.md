---
title: "sentinel-skill"
doc-id: "mb-92f85bd1"
updated: "2026-10-07"
---

# mb-config-mb-sentinel-review — Exam Skill

Exams the Sentinel security-review system's configuration state against its
spec. This skill holds the **procedure** only — expected values live in the
spec doc and are read fresh at the start of every run. The subject system is
working well; this exam verifies that and repairs nothing.

- Spec: [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) — read it first, every run
- **Exam plan: [[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-plan.md) — read second, every run.** The plan-driven cycle: the config-manager synthesizes this plan fresh before each run (spec + last report + log + learnings) and this skill executes it in hand. Run-specifics and deltas live in the plan; the **standing check inventory lives in this skill** (below) — permanent occurrences graduate here, never into plans
- Reference: [[[mybizz-config-docs:mb-sentinel-review/sentinel-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-reference.md) — invocation, review cycle, worked examples
- Explainer: [[[mybizz-config-docs:mb-sentinel-review/sentinel-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-explainer.md) — the whole-system narrative
- Scope: [[[mybizz-config-docs:mb-sentinel-review/sentinel-scope|Scope]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-scope.md) — the agreed scope (the exam stays inside it)
- Design genesis: [[[mybizz-config-docs:mb-sentinel-review/sentinel-security-system|SSS - sentinel Security System]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-security-system.md) — the recovered plan document (cited, never edited)
- Report: [[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-report.md) — one file, overwritten each run (write-then-replace)
- Log: [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md) — one run row per exam; free rows for notable events witnessed between runs
- Learnings: [[[mybizz-config-docs:mb-sentinel-review/sentinel-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-learnings.md) — transient; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the Sentinel system itself**: its two subject skills
  (installed copies), the reasoning-methodology install, the security-global
  library's recorded shape, the `triage_findings` database state, the
  step-intensity wiring in PDLF step files, and this suite's documents.
- **The security-global documents' CONTENT is out of scope** — the library is
  the authority Sentinel reviews against; this exam verifies its recorded
  shape (root, categories, counts, prefix), never its content (owned by docs
  governance).
- **PDLF step files are read-only evidence** — the wiring checks read them
  and never edit them. Step-file wiring work belongs to PDLF development
  (the makePDLF layer); the exam surfaces wiring gaps as findings only.
- **`triage_findings` is read-only for this exam** — no INSERT/UPDATE/DELETE
  ever, by any route; the database and its ledger are deny-list.
- **Running the subject skill is out of exam scope** — a real review writes
  database rows (content-changing). The exam verifies install, state, and
  wiring; it never executes a review.
- **Cupcake internals are out of scope entirely.** `mb-compile-rules` is
  verified at install/state level only — its Rego outputs and policy
  behavior are Cupcake's own exam module's domain.
- The governing ADR (dependency-based, not multi-tenant) is **Sealed** —
  cited, never touched.
- Spec-doc corrections are flagged — never applied by the exam.

## Credential discipline (hard rule)

The database route carries a credential (`PGPASSWORD`, sourced from the PDLF
project's `.env` by the bridge procedure): referenced by variable name only —
never printed, logged, or copied into reports, outputs, or learnings. The
exam never reads `.env` contents; the bridge probes are developer-run (class
below). Direct WSL psql is never used — it silently reaches the wrong server.

## Hard behavioral rules (from the spec's own Do-not list)

- Expected values are read fresh from the spec every run — never from memory.
- Do not treat the step-intensity numbers as final for any step not yet
  built — confirm against the real file when it exists; the exam verifies the
  built-status column live and flags staleness on either side.
- Do not treat a missing `triage_findings` row as equivalent to a CLEAR — a
  missing row means the review never ran; `clear` means it ran and found
  nothing.
- Do not use multi-tenancy vocabulary in any finding — the ADR is binding;
  tenant patterns are findings, not idioms.
- Do not connect to the `pdlf` ledger with direct WSL psql — the bridge is
  the only route to the right server.
- Never execute the subject skill or any review in any form.
- Never write to PDLF step files, the security-global library, the governing
  ADR, the installed subject skills, or the database.
- Guard denials are honored absolutely — never retried through alternate
  paths, never token-dodged; a denied check bundles into the run's ONE
  developer-run request with the exact commands.
- Never improvise probes outside the plan — capture output to files; never
  pipe live output to a truncating consumer.
- The body-hash method (pinned 2026-10-04): strip the frontmatter (everything
  up to and including the second `---` line), sha256 the remainder, take the
  first 16 hex. Reference command:
  `awk 'NR==1&&$0=="---"{i=1;next} i&&$0=="---"{i=0;next} !i' FILE | sha256sum`

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| SN0-1 | A | Installed subject skill present at `~/.config/opencode/skills/mb-sentinel-review/SKILL.md` with functional frontmatter (`name: mb-sentinel-review` + description) | Present (config §Identity — Skill 1). Absent = DOWN — the system cannot be invoked |
| SN0-2 | A | The skill name appears in the running session's discoverable skill surface | Listed (config §Identity — installed). Absent = DOWN (undiscoverable install) |
| SN0-3 | A | Spec doc present at `C:\mybizz\mybizz-config-docs\mb-sentinel-review\sentinel-config.md`, non-empty | Present (the spec). Absent = DOWN — no expected values; the exam is unlawful |

## Tier 1 — State conformance (each probe vs the spec's current expected value; mismatch = DRIFT)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SN1-1 | A | Skill 2 `mb-compile-rules` installed at `~/.config/opencode/skills/mb-compile-rules/SKILL.md` with functional frontmatter (`name` + `description`) | Present (config §Identity — Skill 2). Absent = DRIFT |
| SN1-2 | A | Methodology `secure-software-engineering` installed at `~/.config/opencode/skills/secure-software-engineering/` — SKILL.md, references/, templates/, evals/ present | Present (config §Identity). Tree-shape deltas recorded factually; spec staleness flagged, never edited |
| SN1-3 | A | Companion artifacts present: design genesis `sentinel-security-system.md` and scope `sentinel-scope.md` in this folder; governing ADR at `C:\dev\project-library-global\adr-global\adr-dependency-based-not-multi-tenant.md` | All present (config §Identity + §Governing architecture document). Missing = GAP |
| SN1-4 | A | Step-16 wiring live in the real step file (`stepwise/step-16-domain-modeling.md`): the `mb-sentinel-review` invocation at item 7; the gate-proof check (verified `triage_findings` row before the gate proceeds) at item 9 | Both present (config §Retrofitted + §Step-intensity row 16). Missing = DRIFT |
| SN1-5 | A | Step-intensity built-status vs live: which of the twelve intensity-table steps exist as real step files under `stepwise/` | Per the spec's built-status column, read fresh. Mismatch = DRIFT — flag which side moved (spec staleness is a live possibility; flagged, never edited) |
| SN1-6 | A | Unwired-built-steps evidence: intensity steps other than 16 that exist as files carry no Sentinel wiring (step 39's ordinary triage usage of the ledger is not wiring) | Recorded factually; a wiring coverage gap is surfaced as a finding — the wiring work itself belongs to PDLF development |
| SN1-7 | A | Installed skill §1 step-intensity table vs spec §Step-intensity table: step membership and scrutiny values | Match on shared steps; any delta (e.g. an extra marker row) itemized and flagged — never edited |
| SN1-8 | A | Suite completeness: config, exam-plan, exam-report, log, learnings, explainer, reference + exam-skill source, plus scope and design genesis | All present; missing file = GAP |
| SN1-9 | A | Register row conformance: the config-manager register's `mb-sentinel-review` row carries state `Installed`, the recorded body hash, and an install date, after the Phase 2 flip | Row complete (config-manager register). Missing/Deferred after install = GAP |
| SN1-10 | D | Security-global library shape: root `C:\dev\project-library-global\security-global\` exists; 7 categories; 54 `sec-*.md` documents; per-category counts (principles 9, requirements 6, threat-models 11, infrastructure 10, cloud 7, secrets 6, testing 5) | Match (config §Security-global). **Guard-forbidden (D):** the count command text carries the `secrets` category name — sensitive-token class, denial proven live 2026-10-07; bundled developer-run |
| SN1-11 | D | Database state: `triage_findings` exists on the Windows PG15 `pdlf` database (role `pdlf_agent`, bridge-only); 0 rows; columns per spec incl. `source_step` CHECK and `triage_label` CHECK; `finding_id` free-standing | Match (config §Database). **Guard-forbidden (D):** the bridge procedure requires `source .env` — secrets class, proven; bundled developer-run; direct WSL psql never used |
| SN1-12 | D | Skill 2 functional evidence: the built/amended rule inventory in `C:\dev\project-library-global\rules-cupcake-global\` (19 rules; latest amendments 2026-09-08) | Match (config §Identity — Skill 2). **Guard-forbidden (D):** the rules path carries the sibling guard's token — exec-protection class, proven; bundled developer-run |
| SN1-13 | A | Spec §Identity mirror claim vs live: is a byte-identical mirror of Skill 1 present in this suite folder? | Mirror present per the spec's claim, read fresh. Mismatch = DRIFT — flag which side moved (spec staleness is a live possibility; flagged, never edited) |

## Tier 2 — Functional proof (present ≠ working; read-only probes only; never content-changing)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SN2-1 | A | Installed skill machine-parsable: frontmatter parses as YAML with exactly `name` + `description` keys; body intact from H1 (hard rules, intensity table, review cycle present) | Parses; two keys; body intact (config §Identity). Failure = lost canonical content |
| SN2-2 | A | CLEAR-fast-path real: the skill's "any step number not in this table: CLEAR, immediately" rule present; the corrected CLEAR-row doctrine present (a reviewed CLEAR writes a real, immediately-resolved `triage_findings` row) | Both present (skill §1 + §2 Step 6; config §Do-not). Missing = UNHEALTHY — the safety valve is gone |
| SN2-3 | A | Gate-proof semantics real in the wired step file: "No row: STOP, present a..." text at item 9 | Present (config §Retrofitted). Missing = UNHEALTHY — the gate-proof is the invocation guarantee |
| SN2-4 | A | Three-outcome discipline: CLEAR/FLAG/ESCALATE defined in the installed skill; ESCALATE fires on no-document-match (never an assumed CLEAR); ESCALATE's row mapping `needs-info` correct | Present (skill §2 Steps 5/7; reference cycle). Missing = UNHEALTHY |
| SN2-5 | A | Database route discipline: the reference documents the bridge as the only route; no direct-WSL-psql instruction anywhere in the suite | Bridge-only documented (config §Database + reference). A direct-route instruction = DRIFT |
| SN2-6 | A | Methodology discoverable: `secure-software-engineering` listed in the running session's skill surface (the spec's restart caveat resolved by observation) | Listed (config §Identity). Absent = finding (reasoning layer unreachable) |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier. Not skimped: every sub-check executes, evidence captured to files — a summary verdict without per-item evidence is a failed Tier 3)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SN3-1 | D | **Full spec-vs-live conformance walk:** paragraph-level comparison of every spec table (Identity, Environment position, Security-global, Governing architecture document, Database, Step-intensity, Retrofitted, Related tools, Known limitations) against live state — every spec claim located; every live delta itemized with class + recommended resolution (spec-edit proposals to docs governance) | Complete mapping recorded; every mismatch itemized |
| SN3-2 | D | **Database deep probe (bridge):** `source_step` CHECK values (13 incl. 36), `triage_label` CHECK (6 values), column list, row count — live via the PowerShell bridge, evidence to files | Match (config §Database). Deviations = DRIFT |
| SN3-3 | D | **Methodology currency:** upstream `github.com/magnus919/agent-skills/tree/main/secure-software-engineering` — license (MIT), maintenance status, installed tree vs upstream | Recorded (config §Identity). Supply-chain posture re-confirmed or deltas flagged |

## Report

Write [[[mybizz-config-docs:mb-sentinel-review/sentinel-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-exam-report.md): verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[[mybizz-config-docs:mb-sentinel-review/sentinel-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-log.md); new
learnings filed in [[[mybizz-config-docs:mb-sentinel-review/sentinel-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-learnings.md).

## Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- **Agent-healable items: suite-file repairs only** (exam-plan, exam-report,
  log, learnings, exam-skill source in this folder); everything else
  developer-run or proposed
- **Deny-list (never heal, never touch without the developer's explicit
  per-item gate approval naming the file): the installed subject skills
  (`mb-sentinel-review`, `mb-compile-rules`, `secure-software-engineering`) ·
  PDLF step files · the security-global library · the governing ADR (Sealed)
  · `triage_findings` and its database · Cupcake internals
- Spec-doc corrections → flagged to docs governance, never applied here
- Tier 3 unlock decision asked at the gate, never assumed
- Grants: requested from the developer in chat — `mg-grant --path <folder>
  --count N` (developer-executed; never self-granted, never worked around)