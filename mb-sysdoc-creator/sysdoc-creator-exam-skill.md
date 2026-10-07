---
title: "sysdoc-creator-exam-skill"
doc-id: "mb-1d8a2521"
updated: "2026-10-07"
---

# mb-config-mb-sysdoc-creator — Exam Skill

Exams the `mb-sysdoc-creator` system's configuration state against its spec.
This skill holds the **procedure** only — expected values live in the spec doc
and are read fresh at the start of every run. The subject skill is working
well; this exam verifies that and repairs nothing.

- Spec: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-config.md) — read it first, every run
- **Exam plan: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-exam-plan.md) — read second, every run.** The plan-driven cycle: the config-manager synthesizes this plan fresh before each run (spec + last report + log + learnings) and this skill executes it in hand. Run-specifics and deltas live in the plan; the **standing check inventory lives in this skill** (below) — permanent occurrences graduate here, never into plans
- Reference: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-reference.md) — invocation, phase procedure, gate semantics
- Explainer: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-explainer.md) — the whole-system narrative
- Report: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-exam-report.md) — one file, overwritten each run (write-then-replace)
- Log: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-log.md) — one run row per exam; free rows for notable events witnessed between runs
- Learnings: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-learnings.md) — transient; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the subject skill itself**: its installed copy, its
  authoritative source copy (`sysdoc-creator-skill.md`), the suite documents,
  the governing specification (`doc-suite-specification.md` — a system
  artifact of the subject, examined never edited), the run-log infrastructure
  at `C:\mybizz\logs\mb-sysdoc-creator\`, its GBrain integration state, and
  its invocation surface.
- **The three-document suites the skill produces** (`archify/`, `gbrain/`,
  `postgresql/`, ...) belong to their own `mb-config-*` exam modules. This
  exam never re-tests a produced suite's content; the deepest permitted probe
  is read-only output-discipline evidence (Tier 3 SC3-2, developer-run).
- **Running the subject skill is out of exam scope** — it is expensive by
  design (research phase, two human gates, real writes). The exam verifies
  install and state; it never executes any subject phase.
- **The run-log infrastructure is read-only for this exam** — the subject
  skill's Phase 0/9/10 own all writes there. The exam reads, counts, diffs;
  never appends, moves, or deletes.
- **Cupcake internals are out of scope entirely** — the subject's own Hard
  Rule 7 binds this exam the same way.
- Spec-doc corrections are flagged to docs governance — never applied by the
  exam.

## Credential discipline (hard rule)

No credential surfaces exist in this system. The general rule still binds:
credentials are referenced by variable name only — never printed, logged, or
copied into reports, outputs, or learnings. The exam reads no `.env`, no
credential-bearing config files.

## Hard behavioral rules (from the suite's own Do-not list)

- Expected values are read fresh from the spec every run — never from memory.
- Never execute the subject skill or any of its phases in any form.
- Never write to `C:\mybizz\logs\mb-sysdoc-creator\` or any subfolder.
- Never edit the subject `SKILL.md`, its source copy,
  `doc-suite-specification.md`, or any document the skill produced — these
  are deny-list; changes go through the gate as proposals (applied only on
  the developer's explicit per-item approval naming the file).
- Never invoke `mg-grant` or any permission-altering command (subject Hard
  Rule 7 discipline; grants are requested in chat, executed by the
  developer).
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
| SC0-1 | A | Installed subject skill present at `~/.config/opencode/skills/mb-sysdoc-creator/SKILL.md` with functional frontmatter (`name: mb-sysdoc-creator` + description) | Both present (config §Installed surface). Absent = DOWN — the system cannot be invoked |
| SC0-2 | A | The skill name appears in the running session's discoverable skill surface (this session's own skill list carries it) | Listed (config §Identity — invocation). Absent = DOWN (undiscoverable install) |
| SC0-3 | A | Governing specification present at its permanent location `C:\mybizz\mybizz-config-docs\mb-sysdoc-creator\doc-suite-specification.md`, non-empty | Present (config §Governing specification). Absent = DOWN — the subject's Phase 2 stops every run at the spec check; the system is lawful-operation unavailable |

## Tier 1 — State conformance (each probe vs the spec's current expected value; mismatch = DRIFT)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SC1-1 | A | Authoritative source copy format: `sysdoc-creator-skill.md` in the suite folder, document frontmatter (`title`/`doc-id`/`updated`; `title` = filename stem), body intact | Body intact (config §File inventory — 309 lines / 15,152 bytes as verified 2026-09-09). Empty body = DRIFT (lost canonical content) |
| SC1-2 | A | Hash pair: installed copy vs source copy (body-hash method, first 16 hex) + body identity below the frontmatter (frontmatter is the expected difference — installed keeps `name`/`description`, source carries `title`/`doc-id`/`updated`) | Body byte-identical below the frontmatter (config §Installed surface — sync state row). Installed-edited → DRIFT; source-edited-not-reinstalled → stale GAP |
| SC1-3 | A | Suite completeness — read the spec's tables, never a bare count: config, reference, explainer, learnings (4 pre-existing) + the exam set (exam-plan, exam-report, log, exam-skill source) + doc-suite-specification + the subject skill source | All present; missing file = GAP |
| SC1-4 | A | Structure inventory conformance: hard rules count, phase sequence (0–10 plus any lettered phases), hard constraints count, completion statuses (5), log folders (5) — live counts vs the spec's §Procedure structure rows | Live matches spec (config §Procedure structure). Mismatch = DRIFT — flag which side moved (spec staleness is a live possibility; flagged, never edited) |
| SC1-5 | A | Log infrastructure conformance: the 5 folders under `C:\mybizz\logs\mb-sysdoc-creator\` exist; `in-progress` empty; `abandoned-runs` empty or holding only declined-resume records; counts vs the spec's §Log infrastructure rows | Folders live; counts match spec (config §Log infrastructure). Count mismatch = DRIFT — flag which side moved |
| SC1-6 | A | GBrain integration state: pages live under `mb-sysdoc-creator/*` in GBrain (read-only search-class probes) vs the spec's §GBrain integration rows | Matches (config §GBrain integration). Page-set growth beyond recorded rows is reported factually, re-flagged only when a recorded page is missing |
| SC1-7 | A | Register row conformance: the config-manager register's `mb-sysdoc-creator` row carries state `Installed`, the recorded body hash, and an install date, after the Phase 2 flip | Row complete (config-manager register). Missing/Deferred after install = GAP |

## Tier 2 — Functional proof (present ≠ working; read-only probes only)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SC2-1 | A | Installed copy machine-parsable: frontmatter block parses as YAML with exactly `name` + `description` keys; body intact from H1 | Parses; two keys; body intact (config §Installed surface). Failure = the doc-auditor F-1 defect class |
| SC2-2 | A | Invocation contract live: the environment's skills catalog records `mb-sysdoc-creator` as installed (spec open item 1) | Catalog row present (config §Open items #1). Absent row = finding (invisibility in the authoritative skill status list) |
| SC2-3 | A | Resume machinery is real: `learnings/learnings.md` parses (run-section headers enumerable); `last-completed-run/` entries enumerable; `in-progress/` and `abandoned-runs/` state matches the spec | All parse and enumerate (config §Log infrastructure). Broken resume state = UNHEALTHY |
| SC2-4 | A | Drift-detection mechanism functions: the declared currency check (diff of the two copies — spec open item 2) executes read-only and reports the current hunk inventory between source and installed copies | Diff executes; hunks itemized (config §Installed surface — drift-detection row). Pre-restore the expected hunks are the F-2 set; post-restore: empty |
| SC2-5 | A | Run-log evidence vs the spec's §Suites produced table: dates and system names in `last-completed-run/` vs the recorded table (read-only enumeration) | Recorded systems substantiated by run logs (config §Suites produced). Newer runs beyond the table = DRIFT in the spec (flagged, never edited) |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier. Not skimped: every sub-check executes, evidence captured to files — a summary verdict without per-item evidence is a failed Tier 3)

| ID | Runner | Check | Expected |
|---|---|---|---|
| SC3-1 | D | **Full source-vs-spec conformance walk:** paragraph-level comparison of the installed skill against every spec table (Identity, File inventory, Installed surface, Governing specification, Procedure structure, Log infrastructure, GBrain integration, Cross-cutting integration, Suites produced, Open items) — every spec claim located in the skill, every skill rule traced to a spec row | Complete mapping recorded; every mismatch itemized with class + recommended resolution (spec-edit proposals go to docs governance) |
| SC3-2 | D | **Output-discipline evidence audit:** read the two 2026-10-07 run logs in full (`mb-archify-scope`, `mb-close-out`); spot-check one produced suite's documents against `doc-suite-specification.md`'s stray-line discipline (read-only) — evidence about the **producer's** discipline, never findings about the produced suite (those route to the owning module) | Run logs complete (phases, gates, outcome); produced documents conform to the governing spec |

## Report

Write [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-exam-report.md): verdict line; per-tier
tables (check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-log|Log]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-log.md); new
learnings filed in [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-learnings.md).

## Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk
- **Agent-healable items: suite-file repairs only** (config-manager standard:
  exam-suite file repairs in `mb-sysdoc-creator/` — exam-plan, exam-report,
  log, learnings, exam-skill source); everything else developer-run or
  proposed
- **Deny-list (never heal, never touch without the developer's explicit
  per-item gate approval naming the file): the subject `SKILL.md` · its
  source copy `sysdoc-creator-skill.md` · `doc-suite-specification.md` · the
  run-log infrastructure · any produced suite's documents · Cupcake internals
- Spec-doc corrections → flagged to docs governance, never applied here
- Tier 3 unlock decision asked at the gate, never assumed
- Grants: requested from the developer in chat — `mg-grant --path <folder>
  --count N` (developer-executed; never self-granted, never worked around)