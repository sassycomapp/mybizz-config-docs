---
title: "mb-memory-system-diagnostic-exam-skill"
doc-id: "mb-memory-system-diagnostic-exam-skill"
---

# mb-config-mb-memory-system-diagnostic — Exam Skill

Exams the `mb-memory-system-diagnostic` system's configuration state against
its spec. This skill holds the **procedure** only — expected values live in the
spec doc and are read fresh at the start of every run. The diagnostic skill is
working well; this exam verifies that and repairs nothing.

- Spec: [[mb-memory-system-diagnostic-config|Configuration]] — read it first, every run
- **Exam plan: [[mb-memory-system-diagnostic-exam-plan|Exam Plan]] — read second, every run.** The plan-driven cycle: the config-manager synthesizes this plan fresh before each run (spec + last report + log + learnings) and this skill executes it in hand. Run-specifics and deltas live in the plan; the **standing check inventory lives in this skill** (below) — permanent occurrences graduate here, never into plans
- Reference: [[mb-memory-system-diagnostic-reference|Reference]] — invocation, section commands, gate semantics, report formats
- Explainer: [[mb-memory-system-diagnostic-explainer|Explainer]] — the whole-system narrative
- Report: [[mb-memory-system-diagnostic-exam-report|Exam Report]] — one file, overwritten each run (write-then-replace)
- Log: [[mb-memory-system-diagnostic-log|Log]] — one run row per exam; free rows for notable events witnessed between runs
- Learnings: [[mb-memory-system-diagnostic-learnings|Learnings]] — transient; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the diagnostic skill itself**: source artifact, installed copy, suite documents, register rows, recorded constants, invocation surface.
- **The six memory-ecosystem components** (GBrain, PostgreSQL Instance B, Memory Governor, mb-submit-memory, Graphify, GBrain Dream Cycle) are owned by their own exam modules (`mb-config-gbrain`, `mb-config-postgresql`, `mb-config-memory-governor`, `mb-config-mb-submit-memory`, `mb-config-graphify`, `mb-config-gbrain-dream-cycle`). This exam never live-tests a component; the deepest permitted probe is `--version`-class existence (Tier 2 MS2-2) and recorded-constant comparison against sibling suites' documents.
- **Running the diagnostic itself is out of exam scope** — it is heavyweight, developer-invoked, and carries real-write sections (§4/§5/§10). The exam verifies install and state; it never executes the subject.
- **Cupcake internals are out of scope entirely** — same rule that binds the subject skill binds this exam.
- **PostgreSQL Instance A / the `pdlf` ledger is out of scope entirely.**
- Spec-doc corrections are flagged to docs governance — never applied by the exam.

## Credential discipline (hard rule)

The subject skill's own hard rule binds this exam: never read, print, or copy
credential values — reference by variable name only. The exam reads no `.env`,
no `config.json` credential fields; any command text quoted from the skill is
quoted verbatim including its `***` / variable-name placeholders.

## Hard behavioral rules (from the suite's own Do-not list)

- Expected values are read fresh from the spec every run — never from memory.
- Never execute the diagnostic's heavyweight sections (§4, §5, §10) in any form — out of exam scope, permanently.
- Never touch PostgreSQL Instance A / `pdlf` in any check.
- Never execute the Cupcake binary or live-test a Cupcake rule.
- Never run `gbrain sync` or any G-brain write from the exam (content-changing; ingest-state checks are read-only).
- Never edit the subject `SKILL.md`, its source, any suite doc outside the exam set, or any sibling suite's documents — governance flags only.
- Never improvise probes outside the plan — capture output to files; never pipe live output to a truncating consumer.
- Never treat recorded constants as verified runtime state — the spec's own live-verified table distinguishes presence (verified) from runtime state (measured by runs).

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| MS0-1 | A | Installed subject skill present at `~/.config/opencode/skills/mb-memory-system-diagnostic/SKILL.md` with functional frontmatter (`name: mb-memory-system-diagnostic` + description) | Both present (config §Identity — installed skill). Absent = DOWN — the system cannot be invoked |
| MS0-2 | A | The skill name appears in the running session's discoverable skill surface (this session's own skill list carries it — observed convention per the doc-auditor F-1 lesson) | Listed (config §Identity — run surface). Absent = DOWN (undiscoverable install) |

## Tier 1 — State conformance (each probe vs the spec's current expected value; mismatch = DRIFT)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MS1-1 | A | Source artifact format: two-field corpus frontmatter (`title`/`doc-id` = `mb-memory-system-diagnostic-skill`), lowercase `-skill.md` suffix, filename stem = doc-id | All three (config §Identity — skill frontmatter row + §Recorded decisions) |
| MS1-2 | A | Hash pair: installed copy vs source `mb-memory-system-diagnostic-skill.md` (sha256 first 16 hex) + body-identity from H1 (dual-format: frontmatter block = expected difference per the register's install-discipline note) | Hashes recorded at Phase 2 install; body byte-identical from H1. Installed-edited → DRIFT; source-edited-not-reinstalled → stale GAP |
| MS1-3 | A | Suite completeness — read the spec's tables, never a bare count: config, reference, explainer, skill source (4 pre-existing) + the exam set (exam-plan, exam-report, log, learnings, exam-skill source) joined at this build | All present; missing file = GAP |
| MS1-4 | A | Scope conformance: the source artifact's §Scope matches the spec's §Scope table (in-scope six components; out-of-scope Instance A, Cupcake internals, everything outside the memory ecosystem) | Tables agree (config §Scope) |
| MS1-5 | A | Section inventory conformance: the source artifact carries the 11 sections with the gate classes recorded in the spec's §Section inventory (§4/§5/§10 heavyweight-always; §1/§6 trouble+heavyweight remediation; §2/§3/§7/§8/§9 trouble) | All 11 present, classes match (config §Section inventory) |
| MS1-6 | A | Recorded constants present in the source artifact verbatim: RLS coverage 62/62 · HIGH_RISK_TYPES includes the five categories with `policy` in them · §3 curl pass value HTTP 422 · §9 backup age ≤ 7 days · role-isolation via `has_database_privilege` (never `SET ROLE`) · §10 cycle_freshness + `.phase` (never `.name`) | All present (config §Scope + sibling-suite recorded constants as cited in the skill text) |
| MS1-7 | A | Register-local recorded absence: no rows for the suite's documents in `register-local.md`; pending-events queue holds no events for these files (open item #1 state) | Both absences confirmed (config §Register usage). Registration is doc-maintainer's work, never the exam's |
| MS1-8 | A | GBrain ingest state: the spec's §GBrain integration row (source `mybizz-config-docs`, ingest 2026-09-28 at commit `c0570db`, 4 pages) matches the live gbrain pages for the suite (read-only `gbrain search`/`get_page`-class probes) | Matches (config §GBrain integration). Post-commit sync already ran — a higher page/chunk count than recorded is expected drift, reported factually not re-flagged |

## Tier 2 — Functional proof (present ≠ working; read-only probes only)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MS2-1 | A | Installed copy machine-parsable: frontmatter block parses as YAML with exactly `name` + `description` keys; body intact from H1 | Parses; two keys; body intact (config §Identity). Failure here is the doc-auditor F-1 defect class |
| MS2-2 | A | Command inventory executability *in form*: for each binary the skill's sections invoke (gbrain, psql, jq, sha256sum, ss, curl, git, journalctl, graphify), confirm presence on PATH — `command -v` only; no skill command executed beyond this | All present (config §Live-verified component presence + reference §Run flow). Absent binary = finding (the section that needs it cannot run) |
| MS2-3 | A | Report-path parent viability: `C:\mybizz\` (= `/mnt/c/mybizz/`) exists and is writable-by-developer convention; the reports folder `memory-diagnostic-reports/` is absent per open item #3 | Parent present; folder absent (config §Report storage + §Open items #3). Folder present before a first run = spec-staleness flag, not a defect |
| MS2-4 | A | Cross-suite recorded-constant spot-check (read-only document comparison): postgresql-config's RLS row still records 62/62; memory-governor-config still records the high-risk classification the skill cites; the spec's Gates table matches the skill's heavyweight-action list (§4/§5/§10 + §1's `gh repo create` + §6's `graphify update`) | Constants agree (config §Section inventory + §Gates). Divergence = DRIFT in whichever document moved — flagged, never edited here |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier. Not skimped: every sub-check executes, evidence captured to files — a summary verdict without per-item evidence is a failed Tier 3)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MS3-1 | D | **Full source-vs-spec conformance walk:** paragraph-level comparison of the skill source against every spec table (Identity, Scope, Section inventory, Gates, Report storage, GBrain integration, Register usage, Open items) — every claim in the spec located in the artifact, every artifact command traced to a spec row | Complete mapping recorded; every mismatch itemized with class + recommended resolution (spec-edit proposals go to docs governance) |
| MS3-2 | D | **Cross-suite constant verification:** each recorded constant the skill cites (RLS 62/62; HIGH_RISK_TYPES; HTTP 422; cycle_freshness semantics; backup locations/age; ADR remediation sequence) verified against the *current* recorded state of all five sibling suites (gbrain, postgresql, memory-governor, graphify, gbrain-dream-cycle) — the trust relationship the explainer documents, proven rather than assumed | Every constant current; stale constants itemized for the owning suite's docs governance |

## Report

Write [[mb-memory-system-diagnostic-exam-report|Exam Report]]: verdict line;
per-tier tables (check ID, expected, actual, result); findings with class +
evidence + recommended repair + risk; runner attribution for every deferred
item (guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to
[[mb-memory-system-diagnostic-log|Log]]; new learnings filed in
[[mb-memory-system-diagnostic-learnings|Learnings]].

## Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk
- **Agent-healable items: suite-file repairs only** (config-manager standard:
  exam-suite file repairs in `mb-memory-system-diagnostic/`); everything else
  developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the subject `SKILL.md` and its source ·
  sibling suites' documents (read for comparison, never edited) · env
  credentials (name only) · any `gbrain sync` execution or G-brain write · the
  memory-ecosystem components (no live probing beyond form checks) ·
  PostgreSQL Instance A / `pdlf` · Cupcake internals
- Grants: requested from the developer per the 2026-09-15 amendment —
  `mg-grant --path <folder> --count N` (developer-executed; never self-granted,
  never worked around)
