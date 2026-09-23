---
document: "mb-doccycle — Exam Skill"
doc-id: doccycle-skill
state: Live
date-created: 2026-09-22
---

# mb-config-doccycle — Exam Skill (source)

Exams the mb-doccycle documentation-management workflow system's live
configuration state against [[doccycle-config|doccycle Configuration]] and
proves the pipeline functionally executes. Detection and verification only
— the workflow is working well; this module changes nothing, catches
silent failures, and proposes gated repairs. Use when asked to "exam
doccycle", "check doccycle health", or as part of a full mb-config-manager
run.

- Spec (read first, every run): [[doccycle-config|Configuration]]
- **Exam plan (read second, every run):** [[doccycle-exam-plan|Exam Plan]]
  — the config-manager synthesizes it fresh each run; the **standing check
  inventory lives in this skill**, never in plans
- Reference: [[doccycle-reference|Reference: Usage and Invocation]]
- Report: [[doccycle-exam-report|Exam Report]] — overwritten each run
  (write-then-replace)
- Log: [[doccycle-log|Log]] · Learnings: [[doccycle-learnings|Learnings]]
- The workflow's own binding frame: [[doccycle-run-discipline|Shared Run
  Discipline]]

## Scope boundary (anti-duplication)

- Exams the **workflow system**: installed skill (hash pair vs the
  git-backed source), phase specs, the canonical detector `doccycle-detect.py`
  and its 27-test suite, the logs/records home, the backup root, the
  enforcement integration surfaces the workflow uses, the retirement
  residue, and the registers' doccycle rows.
- **Cupcake enforcement internals** belong to `mb-config-cupcake`; this
  module verifies the integration artifacts the workflow depends on
  (git-grant script presence, grants-data file shape) as states, never the
  enforcement layer's correctness.
- **GBrain** (sync machinery, dream cycle) belongs to `mb-config-gbrain`;
  **PostgreSQL** to `mb-config-postgresql`. The WP8 run record is verified
  as a state, never re-run here.

## Credential discipline (hard rule)

The system requires no credentials of its own (grant slips are
developer-issued). Reference grant tooling by name only; never print or
log grant contents beyond the counts/expiry lines the tools themselves
emit.

## Hard behavioral rules (from the suite's own Do-not list)

- The exam never invokes the workflow skills on a corpus — a full run is
  Tier 3, developer-gated and expensive.
- Never "fix" a detector finding by editing corpus documents — corpus work
  belongs to the workflow, not to its exam.
- Never bypass the hash-pair check; a hash divergence is a finding (DRIFT
  or stale GAP), not something to reconcile silently.
- The three retired skills are removed — their reappearance anywhere under
  `~/.config/opencode/skills/` or `mybizz-config-docs\` is a DRIFT
  finding, never "restored".
- The tool is read-only by contract — any write observed from a detection
  run is an UNHEALTHY finding, verified by fixture hashes before/after.

## Tier 0 — Invocability (run first; failure = report DOWN, stop)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| DCY0-1 | A | Installed skill present and hash-matches source: md5 `~/.config/opencode/skills/mb-doccycle/SKILL.md` vs `C:\mybizz\mb-doccycle\SKILL.md` | Identical (config §Component inventory — pair `a8336c843c79c900cf98afe0c54c2f69` recorded 2026-09-22; read the spec's current value). Divergence: installed-edited → DRIFT; source-edited-not-reinstalled → stale GAP |
| DCY0-2 | A | Installed phases: `~/.config/opencode/skills/mb-doccycle/phases\` holds A-structure.md, B-consistency.md, C-conversion.md | All three present (config §Component inventory) |
| DCY0-3 | A | Tool invocable: `python3 tool/doccycle-detect.py --version` from the source home | `0.1.0` (config §Component inventory; read fresh — the amendment queue may bump it) |

## Tier 1 — State conformance (each probe vs the spec's current expected value; mismatch = DRIFT)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DCY1-1 | A | Suite completeness: config, reference, explainer, run-discipline, exam-plan, exam-report, log, learnings + skill source in `C:\mybizz\mb-doccycle\` (SKILL.md, phases\, tool\, tests\) | All present (missing file = GAP). The doccycle suite carries an eighth file — the run frame — beyond the 7-file standard, by design |
| DCY1-2 | A | Source repo state: `git -C /mnt/c/mybizz/mb-doccycle status --porcelain` + `log --oneline -3` | Clean or known-pending only; HEAD pushed (origin/master exists) |
| DCY1-3 | A | Logs/records home: `C:\mybizz\logs\mb-doccycle\` — run-index.md, learnings\ (3 seed files), in-progress\ (empty between runs), last-completed-run\ (≥1 record), abandoned-runs\ | Structure present per config §Records |
| DCY1-4 | A | Backup evidence: `C:\backup-mb-doccycle\` holds the WP7 retirement backup and the WP8 run backup; WP8's folder count = 5 | Per config §Records |
| DCY1-5 | A | Enforcement integration: `git-grant` present at `~/.config/cupcake/bin/`; `cup-git-grants-data.rego` parses (package `git_grants_data`); the compiled commits policy references `git_grants_data` | Per config §Enforcement integration. Grant-file CONTENT is dynamic state — never treated as drift |
| DCY1-6 | A | Retirement residue: mb-docs-manager, mb-align-docs, mb-wikilinks absent from `~/.config/opencode/skills\` AND from `mybizz-config-docs\`; 39-file backup intact | All absent, backup present (config §Component inventory) |
| DCY1-7 | A | Registers: register-local.md carries 9 Retired rows + 4 doccycle rows Live; config-manager-register carries the doccycle row and the three retired rows | Per config §Open items / retirement record |

## Tier 2 — Functional proof (present ≠ working; read-only probes only)

| ID | Runner | Check | Expected |
|---|---|---|---|
| DCY2-1 | A | Tool functional probe: `doccycle-detect.py --universe tests/fixtures/universe.txt --format json` over a fixture file; fixture md5 before/after | JSON parses; counts derived; fixtures unchanged (read-only contract live) |
| DCY2-2 | A | Test suite: `python3 -m unittest discover -s tests` from the source home | 27/27 OK (config §Component inventory) |
| DCY2-3 | A | Run-record trail: run-index.md's WP8 row + the record in `last-completed-run\` | Present and dispositioned (the acceptance-test state) |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| CY3-1 | D | A full corpus cycle on a corpus other than the acceptance target, with slips and a granted commit | Developer decision — expensive (a full cycle) |
| CY3-2 | D | The detector amendment: display_default empty-display fix; folder-token skip; universe scaffold filtering — author with regression tests, commit, reinstall the workflow install if SKILL.md-adjacent files change | Queued from the WP8 run; this exam verifies the amendment state, never applies it unasked |

## Report

Write [[doccycle-exam-report|exam-report]] (write-then-replace): verdict
line; per-tier tables (check ID, expected, actual, result); findings with
class (DOWN / UNHEALTHY / DRIFT / GAP) + evidence + recommended repair +
risk; runner attribution for every deferred item. Then: one run row to
[[doccycle-log|log]]; new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- No agent-healable items expected: the tool and skill are git-backed
  developer artifacts — repairs are proposed and applied as approved
  commits; the installed copy re-hashes after any approved re-install
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never touch): anything under `~/.config/cupcake/` policies
  (examined by `mb-config-cupcake`); `~/.config/opencode/plugin/cupcake.js`
  (enforcement); the scope scaffold; the developer's own corpus files
- Credentials: none; grant tooling referenced by name only