---
title: "mb-archify-scope-exam-skill"
doc-id: "mb-06628fae"
updated: "2026-10-08"
---

# mb-config-mb-archify-scope — Exam Skill

Exams the `mb-archify-scope` scoping skill system's configuration state against
its spec. This skill holds the **procedure** only — expected values live in the
spec doc and are read fresh at the start of every run. The subject system is
working well; this exam verifies that and repairs nothing.

- Spec: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-config]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-config.md) — read it first, every run
- **Exam plan: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-plan]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-plan.md) — read second, every run.** The plan-driven cycle: the config-manager synthesizes this plan fresh before each run (spec + last report + log + learnings) and this skill executes it in hand. Run-specifics and deltas live in the plan; the **standing check inventory lives in this skill** (below) — permanent occurrences graduate here, never into plans
- Reference: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md) — invocation, the nine phases, sync procedure
- Explainer: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-explainer]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-explainer.md) — the whole-system narrative
- Report: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-report]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-report.md) — one file, overwritten each run (write-then-replace)
- Log: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-log]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-log.md) — one run row per exam; free rows for notable events witnessed between runs
- Learnings: [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md) — transient; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the `mb-archify-scope` skill system itself**: the subject
  repo (`/mnt/c/mybizz/mb-archify-scope/` — shape + git state), the installed
  copy (identity, integrity, frontmatter shape), the GBrain registration
  (row shape), this suite's documents, the archify suite's documented
  component facts, and the recorded run artifacts' state.
- **The Archify tool installation and lifecycle are out of scope** — owned by
  the `mb-config-archify` exam module. That module's AR2-3 (installed
  scope-skill copy byte-identity) is deliberately paralleled by this module's
  AS1-2 (the skill system's own deeper check: hash pair + frontmatter shape +
  recorded sizes); neither writes, and both may fire — overlapping detection
  is not duplicated healing.
- **GBrain's sync engine is out of scope** — owned by `mb-config-gbrain`.
  This module verifies the registration row's shape only; the last-sync
  timestamp is volatile (changes at every commit-all) and is never an
  expected-value check.
- **Cupcake internals are out of scope entirely.** The rule-inventory absence
  check (AS1-10) is a developer-run read confirming the spec's recorded
  claim — never a Cupcake probe.
- **Running the subject skill is out of exam scope** — an invocation starts an
  interactive scoping session; its first write (Phase 8) happens only on
  developer approval, and the exam never simulates a drawing request.
- **Run-artifact content quality is out of scope** — the diagrams' design
  quality is Archify's domain; the exam verifies the artifacts' recorded state
  (presence, schema), never their quality.
- The installed copy and the repo spec are **never edited by the exam** — sync
  is developer-run or gated (skills-directory writes are grant-required under
  standing Cupcake policy); spec-doc corrections are flagged, never applied.

## Credential discipline (hard rule)

No credential route exists in this system — no `.env`, no database, no keys,
no tokens. Nothing to reference by name; nothing to withhold. If a future
spec revision introduces a credential route, this section gains the
variable-name-only rule and the class is marked developer-run.

## Hard behavioral rules (from the spec's own Do-not list)

- Expected values are read fresh from the spec every run — never from memory.
- Never invoke the subject skill in any form — running it is out of exam scope.
- Never copy the repo spec over the installed `SKILL.md` — it replaces the
  skill frontmatter (`name`/`description`) with doc frontmatter; sync is
  body-to-body (confirmed-live 2026-10-07). Installed-copy writes are
  grant-required (developer-run) until the Cupcake ancestor-cwd case resolves.
- The exam never edits the installed copy, the repo spec, the archify suite's
  documents, or any run artifact.
- The subject skill is read-only until its Phase 8 — a rule the exam inherits
  by never invoking it; the exam's own writes are suite-file repairs only.
- Guard denials are honored absolutely — never retried through alternate
  paths, never token-dodged; a denied check bundles into the run's ONE
  developer-run request with the exact commands.
- Never improvise probes outside the plan — capture output to files; never
  pipe live output to a truncating consumer.
- Spec-doc corrections → flagged at the gate, never applied here.
- The body-hash method (pinned 2026-10-04): strip the frontmatter (everything
  up to and including the second `---` line), sha256 the remainder, take the
  first 16 hex. Reference command:
  `awk 'NR==1&&$0=="---"{i=1;next} i&&$0=="---"{i=0;next} !i' FILE | sha256sum`
  Both subject files open with `---` — the installed copy's skill frontmatter
  is 4 lines (`---`/`name`/`description`/`---`, verified live 2026-10-08) — so
  the pinned command applies to both sides. Head-verify line 1 before hashing:
  a file NOT opening with `---` would need the variant
  `awk '$0=="---"&&!s{s=1;next} s' FILE | sha256sum`, and applying that variant
  to a leading-fence file includes the frontmatter and fabricates a DRIFT
  (both mistakes made and corrected in run #1).

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| AS0-1 | A | Installed subject skill present at `~/.config/opencode/skills/mb-archify-scope/SKILL.md` with functional frontmatter (`name: mb-archify-scope` + description) | Present (config §Canonical locations). Absent = DOWN — the skill cannot be invoked |
| AS0-2 | A | The skill name appears in the running session's discoverable skill surface | Listed (config §Identity — Invocation). Absent = DOWN (undiscoverable install) |
| AS0-3 | A | Suite spec doc present at `C:\mybizz\mybizz-config-docs\mb-archify-scope\mb-archify-scope-config.md`, non-empty | Present (the spec). Absent = DOWN — no expected values; the exam is unlawful |

## Tier 1 — State conformance (each probe vs the spec's current expected value; mismatch = DRIFT)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AS1-1 | A | Subject repo shape: `/mnt/c/mybizz/mb-archify-scope/` contains exactly `.git/` + `mb-archify-scope.md` | Match (config §Canonical locations — Repo contents). Extra or missing entries = DRIFT |
| AS1-2 | A | Body identity: installed copy vs repo spec — body-hash pair (pinned method — both subject files open with `---`) | Identical (config §Sync state — "Bodies byte-identical"). Divergence = DRIFT — flag which side moved (spec-side staleness is a live possibility: the 2026-09-16 AR2-3 event proved the spec-edited-after-install class) |
| AS1-3 | A | Recorded sizes: repo spec 14,228 B; installed copy 14,356 B | Match (config §Canonical locations). Divergence = flag — spec staleness possible (flagged, never edited) |
| AS1-4 | A | Frontmatter discipline: repo spec carries doc frontmatter (`title`/`doc-id`/`updated`); installed copy carries skill frontmatter (`name`/`description`) | As designed (config §Sync state). Doc frontmatter on the installed side, or skill frontmatter on the spec side = the forbidden plain-copy failure = DRIFT |
| AS1-5 | A | GBrain registration: source id `mb-archify-scope`, federated, path `/mnt/c/mybizz/mb-archify-scope`, 1 page | Match (config §GBrain registration). Missing source = GAP |
| AS1-6 | A | Suite completeness: config, exam-plan, exam-report, log, learnings, explainer, reference + exam-skill source | All present (8 files). Missing file = GAP |
| AS1-7 | A | Register row conformance: the config-manager register's `mb-archify-scope` row carries state `Installed`, the recorded body hash, and an install date, after the Phase 2 flip | Row complete (config-manager register). Missing or still `WIP` after install = GAP |
| AS1-8 | A | Integration mirror-facts: archify-config §Scoping skill component documents the component; archify-reference carries the front-of-pipe invocation note; archify-explainer "Why scoping comes first"; the archify exam carries AR2-3 | All present (config §Integration). Missing = GAP |
| AS1-9 | A | Run artifacts per Run history: `archify/output/memory-ecosystem-project/` carries the scope card, machine header, and learnings file (nested convention) | Present (config §Run history + §Open item 1). Mismatch = flag |
| AS1-10 | A | Cupcake component-rule absence: no `mb-archify-scope`-specific rule in the Cupcake rule inventory (compiled-policy lane + rule-documentation lane) | Match (config §Cross-cutting — Cupcake). Runner A via the approved read-only tool form (Grep/Glob tools — no shell command text, no denial; classification confirmed at the run #1 gate 2026-10-08; pre-classification was D on the command-text denial class). A future guard denial on any form is honored absolutely and bundles developer-run |

## Tier 2 — Functional proof (present ≠ working; read-only probes only; never content-changing)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AS2-1 | A | Installed skill machine-parsable: frontmatter parses as exactly `name` + `description`; body intact from H1 — the nine phases, abort conditions, machine-header JSON, and layout budgets present | Parses; two keys; body intact (config §Structure + §Canonical locations). Failure = lost canonical content |
| AS2-2 | A | Behavioral discipline intact in the body: read-only-until-Phase-8 statement; the single hard gate (Phase 7); abort-and-reshape, never end on a refusal; probe declared-not-executed (Phase 6); "Change this file and the installed copy together" sync rule | All present (repo spec §The nine phases + §Skill mechanics; config §Structure). Missing = UNHEALTHY |
| AS2-3 | A | Subject repo live: HEAD resolvable, working tree clean, origin GitHub-backed | Clean tree + GitHub origin (ADR source-repos-must-be-github-backed). Divergence = flag |
| AS2-4 | A | Sync discipline documented and correct: the suite reference documents the body-to-body sync procedure and the never-plain-copy rule (a plain copy of the spec over the installed copy destroys the skill frontmatter) | Both documented (suite reference §Keeping spec and installed copy in sync + §Do not; config §Canonical locations — Sync mechanism). Missing = UNHEALTHY |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier. Not skimped: every sub-check executes, evidence captured to files — a summary verdict without per-item evidence is a failed Tier 3)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AS3-1 | D | **Full spec-vs-live conformance walk:** paragraph-level comparison of every config table (Identity, Canonical locations, GBrain registration, Structure, Integration, Cross-cutting, Run history, Open items) against live state — every spec claim located; every live delta itemized with class + recommended resolution (spec-edit proposals flagged at the gate) | Complete mapping recorded; every mismatch itemized |
| AS3-2 | D | **Phase-8 contract mechanism deep proof:** the recorded run's `memory-ecosystem-header.json` re-validated field-by-field against the spec's machine-header schema; the approved scope-card content byte-checked against `memory-ecosystem-scope.md`; delivered render evidence (9/9 showcase per config §Run history) located | Header schema-valid; card content byte-match; render evidence present. Deltas = findings |

## Report

Write [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-exam-report]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-exam-report.md): verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated). Overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before
any pruning). Then: one run row appended to [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-log]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-log.md); new
learnings filed in [[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-learnings]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-learnings.md).

## Gate protocol

- Findings → classify (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`) → present with
  evidence + recommended repair + risk — per-item decisions, never batched
- **Agent-healable items: suite-file repairs only** (exam-plan, exam-report,
  log, learnings, exam-skill source in this folder); everything else
  developer-run or proposed
- **Deny-list (never heal, never touch without the developer's explicit
  per-item gate approval naming the file): the installed subject copy
  (`~/.config/opencode/skills/mb-archify-scope/SKILL.md`) · the repo spec
  (`/mnt/c/mybizz/mb-archify-scope/mb-archify-scope.md`) · the archify suite's
  documents · GBrain's engine · Cupcake internals · run artifacts**
- Spec-doc corrections → flagged at the gate, never applied here
- Tier 3 unlock decision asked at the gate, never assumed
- Grants: requested from the developer in chat — `mg-grant --path <folder>
  --count N` (developer-executed; never self-granted, never worked around)
