---
title: "doc-auditor-skill"
doc-id: "mb-02940a97"
---
# mb-config-doc-auditor — Exam Skill

Exams the `mb-doc-auditor` system's configuration state against its spec.
This skill holds the **procedure** only — expected values live in the spec doc
and are read fresh at the start of every run. The auditor is working well;
this exam verifies that and repairs nothing.

- Spec: [[doc-auditor-config|Configuration]] — read it first, every run
- **Exam plan: [[doc-auditor-exam-plan|Exam Plan]] — read second, every
  run.** The plan-driven cycle: the config-manager synthesizes this plan fresh
  before each run (spec + last report + log + learnings) and this skill
  executes it in hand. Run-specifics and deltas live in the plan; the
  **standing check inventory lives in this skill** (below) — permanent
  occurrences graduate here, never into plans
- Reference: [[doc-auditor-reference|Reference]] — invocation, tool syntax,
  scope and register rules, formats
- Explainer: [[doc-auditor-explainer|Explainer]] — the whole-system narrative
- Report: [[doc-auditor-exam-report|Exam Report]] — one file, overwritten
  each run (write-then-replace)
- Log: [[doc-auditor-log|Log]] — one run row per exam; free rows for notable
  events witnessed between runs
- Learnings: [[doc-auditor-learnings|Learnings]] — transient; delete entries
  once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the auditor system itself**: the installed subject
  skill's identity, the source repo and tooling, the audit-record artifact, the
  suite documents and their register rows, and the recorded external
  dependencies (contract, scope authority, maintainer run-log input, gbrain
  CLI).
- **The maintainer system** (watcher, queue, scheduled task, its tools, its
  run-log discipline) belongs to `mb-config-doc-maintainer` — this exam reads
  only the run-log artifact's recorded existence as the auditor's evidence
  input, never the maintainer's internals.
- **The contract's content** (`gbrain/gbrain-doc-contract.md`) is governance —
  the exam verifies its existence, frontmatter, and register row as artifacts;
  its requirements are never re-derived, re-interpreted, or edited here.
- **The scope authority** (`mybizz-scope-list.md`) is read live as a probe —
  its content is governance, never audited here.
- **The audit record's content** (what audits found) belongs to the auditor's
  own domain — this exam verifies the artifact's recorded state (exists,
  frontmatter, register row), never re-audits audit findings.
- **Corpus documentation governance** (register membership as a policy,
  corpus-wide register audits, wikilink content) belongs to the
  documentation-management side; this exam verifies registration **mechanics
  only** (does the recorded row exist) — never audits corpus content.
- **DocCycle is out of scope entirely** — no inspection, no interaction.

## Credential discipline (hard rule)

This system holds no credentials of its own. Any credential encountered
incidentally (env vars, other systems' configs) is referenced **by variable
name only** — never printed, logged, or copied into reports, outputs, or
learnings.

## Hard behavioral rules (from the suite's own Do-not list)

- Expected values are read fresh from the spec every run — never from memory.
- Never write to G-brain: `gbrain_reader.py` is read-only by construction; any
  `gbrain sync` execution is forbidden from the exam (content-changing).
- Never read, write, or touch `anvil.yaml`, and never create an `anvil.yaml`
  fixture — policy-forbidden; the class-rule live test is developer-run by
  design (existence-check level only).
- Never trigger on saves and never involve DocCycle — the auditor is never a
  save-time handler, and DocCycle is out of scope entirely.
- Never edit the subject `SKILL.md`, its source, the contract, the scope
  authority, or any spec doc — governance flags only.
- Never remove register rows — retirement is the auditor's repair class, not
  the exam's; the exam never mutates a register.
- Links are never tool-repaired — semantics are agent-level; the exam performs
  no link repairs.
- The audit record is append-only — existing blocks are never rewritten by the
  exam (a record append happens only inside an unlocked Tier 3 walkthrough).
- Never improvise probes outside the plan — the run #1 Dream Cycle lesson
  generalizes: only parse-safe forms, capture output to files, never pipe live
  output to a truncating consumer.
- Point-in-time semantics: gbrain page counts and coverage move with real
  activity — exact equality is never asserted; explainability is required.
- Never expand a check into a corpus-wide investigation — the auditor's own
  minimum-sufficient principle applies to its exam.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| DA0-1 | A | Installed subject skill present at `~/.config/opencode/skills/mb-doc-auditor/SKILL.md` with functional frontmatter (`name: mb-doc-auditor` + description) | Both present (config §Identity — installed skill). Absent = DOWN — the system cannot be invoked |
| DA0-2 | A | Tool modules present and compile (`python3 -m py_compile` on `scope.py`, `runlog.py`, `gbrain_reader.py`, `record.py`, `audit.py`) | All five compile (config §Component layout). Missing/uncompilable = DOWN — the system cannot audit without its tools |

## Tier 1 — State conformance (each probe vs the spec's current expected value; mismatch = DRIFT)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DA1-1 | A | Source repo: `git -C C:\mybizz\mb-doc-auditor remote -v` + `log --oneline -1` + `status --short` | Origin `https://github.com/sassycomapp/mb-doc-auditor.git`; HEAD `aa91ff7`; tree clean (config §Identity). Untracked debris = finding |
| DA1-2 | A | Hash pair: installed subject skill vs source `mb-doc-auditor-skill.md` (sha256 first 16 hex) + body-identity from H1 (dual-format: frontmatter block = expected difference per the register's install-discipline note) | Source `8e0def60659e0854`, installed `42790f675a784bdd`, body byte-identical from H1 (config §Identity). Installed-edited → DRIFT; source-edited-not-reinstalled → stale GAP |
| DA1-3 | A | Tools compile (covered by DA0-2) and the test suite passes (`python3 -m unittest discover -s tests`) | 22/22 pass (config §Component layout) |
| DA1-4 | A | Suite completeness — read the spec's tables, never a bare count: config, exam-plan, exam-report, log, learnings, explainer, reference, skill source (8-file standard) + `doc-auditor-records.md` co-resident per the spec's Storage table | All present; missing file = GAP |
| DA1-5 | A | Audit-record state: exists at the recorded path; frontmatter two-field compliant; register row present (`doc-auditor-records`, Live) | All three (config §Storage + §Register usage) |
| DA1-6 | A | Register rows for the suite docs in the config-docs register (config/reference/explainer + records + the exam set added at build) | Rows present; missing row = GAP |
| DA1-7 | A | Contract artifact: exists at `C:\mybizz\mybizz-config-docs\gbrain\gbrain-doc-contract.md`; frontmatter two-field compliant (tool check); register row in config-docs register | All three (config §Identity — governing contract) |
| DA1-8 | A | Scope authority: exists and is readable at `C:\mybizz\mybizz-os-docs\os-reference-docs\mybizz-scope-list.md` (locked path, plan §16); parses live (functional proof at DA2-1) | Present and readable (config §Identity — governing plan) |
| DA1-9 | A | Run-log evidence input: `doc-maintainer-run-log.md` exists at the hard-wired path (`C:\mybizz\mybizz-config-docs\mb-doc-maintainer\doc-maintainer-run-log.md` — not the unrelated `doc-maintainer-log.md` in the same directory) | Present (config §Component layout — runlog.py). Absent/empty = the auditor's designed normal state ("no maintenance history available") — recorded as an awareness note, not a defect |
| DA1-10 | A | GBrain source row: `gbrain sources list` must carry an `mb-doc-auditor` row matching the spec's recorded state (config §GBrain integration — registered 2026-09-27, non-federated; open item #2 closed) | Row present and matching spec. Absent = DRIFT; registration state changes are developer-gated state changes the exam never performs |

## Tier 2 — Functional proof (present ≠ working; read-only probes only — no record append, no register mutation)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DA2-1 | A | Scope reader live: `scope.py paths <root>` + `scope.py validate --root <dir>` on a known in-scope root | Exit 0; the authority parses live; paths enumerate with exclusions applied (config §Component layout — scope.py) |
| DA2-2 | A | Run-log reader live: `runlog.py summary` on the real run-log, plus the absent-path handling (nonexistent path → "no maintenance history available", exit clean) | Evidence rows returned for the real log; graceful message for the absent case (config §Component layout — runlog.py) |
| DA2-3 | A | Audit check live: `audit.py check --root <bounded root>` (read-only, always exit 0; findings ride in JSON) — bounded root = the auditor's own suite folder | Exit 0; JSON findings for the real files; no byte changed (hash-proof before/after) (config §Component layout — audit.py) |
| DA2-4 | A | Repair dry-run: `audit.py repair --root <same bounded root>` without `--apply` | Zero bytes changed (hash-proof before/after); exit 0 when nothing was refused, exit 1 with refusal-class residuals when the audit root is not the register's library root (reference §Tool commands — refusals are the human-judgement path, never silent) (config §Component layout + reference repair table) |
| DA2-5 | A | GBrain reader live: `gbrain_reader.py sources` (read-only CLI) | Source list returned; failure → classified Can wait per the spec, exam continues (config §GBrain integration) |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier. Not skimped: every sub-check executes, evidence captured to files — a summary verdict without per-item evidence is a failed Tier 3)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DA3-1 | D | **Full live audit walkthrough, end-to-end** on a real library root (the Phase 5 pattern): scope parsed live from the authority · maintainer run-log evidence consumed · tool checks run live · per-finding classification recorded · safe mechanical repairs applied per the automation boundary (with per-repair pre-state hash capture) · one audit-record block appended · terminal state reached | Every stage evidenced in files; repairs verified by re-check; the record block lands append-only; the invocation terminates cleanly (no follow-up work queues) |
| DA3-2 | D | **Refusal-class live suite** (developer builds fixtures where policy forbids the agent): collision stems (never auto-registered) · multiply-occurring stems (never auto-registered) · obsolete-row retirement outside a library-root audit (refused) · structurally unrepairable frontmatter (reported, never touched) · `anvil.yaml` class rule (existence-check level only — the file itself is never read) | Every refusal surfaces as a finding, never a guess; the anvil folder produces no findings |
| DA3-3 | D | **Repair apply-class on corpus copies:** frontmatter restore (exact two-field block, body byte-preserved) · register add-creation (unique stem) · retire-in-place under a library-root audit | Hash comparison proves only the affected byte range differs; register changes are append-only or in-place state edits per the four-event model; verification rides in the same result |

## Report

Write [[doc-auditor-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[doc-auditor-log|Log]]; new
learnings filed in [[doc-auditor-learnings|Learnings]].

## Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk
- **Agent-healable items: none by default** — this system's artifacts are
  governed documents and a runtime install; repairs are developer-run or
  proposed, except suite-file repairs (the one agent-healable class per the
  config-manager standard: exam-suite file repairs in `mb-doc-auditor/`)
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the subject `SKILL.md` and its source ·
  `gbrain-doc-contract.md` · the scope authority (read live, never edited) ·
  `anvil.yaml` (never created, read, or touched) · env credentials (name only)
  · any `gbrain sync` execution or G-brain write · the audit record's existing
  blocks (append-only)
- Grants: requested from the developer per the 2026-09-15 amendment —
  `mg-grant --path <folder> --count N` (developer-executed; never self-granted,
  never worked around)
