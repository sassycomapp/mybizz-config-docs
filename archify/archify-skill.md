---
title: "archify-skill"
doc-id: "archify-skill"
---
# mb-config-archify — Exam Skill

Exams the Archify skill installation's configuration state against its spec. This
skill holds the **procedure** only — expected values live in the spec doc and are
read fresh at the start of every run. The installation is working well; this exam
verifies that and repairs nothing.

- Spec: [[archify-config|Configuration]] — read it first, every run
- **Exam plan: [[archify-exam-plan|Exam Plan]] — read second, every run.** The
  plan-driven cycle: the config-manager synthesizes this plan fresh before each run
  (from spec + last report + log + learnings) and this skill executes it in hand.
  The plan carries run-specifics and deltas; the **standing check inventory lives in
  this skill** (below) — permanent occurrences graduate here, never into plans
- Reference: [[archify-reference|Reference]] — invocation, authoring procedure,
  authoring invariants, do-not list
- Explainer: [[archify-explainer|Explainer]] — what Archify is, why scoping comes
  first, config-maintenance model, S.W.O.T.
- Scoping component: [[archify-scope-skill|Scoping Skill Specification]] — the front-of-pipe spec
  whose installed copy this exam verifies (AR2-3)
- Report: [[archify-exam-report|Exam Report]] — one file, overwritten each run
  (write-then-replace)
- Log: [[archify-log|Log]] — one run row per exam; free rows for notable
  events witnessed between runs
- Learnings: [[archify-learnings|Learnings]] — file new patterns/nuances; delete
  entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the Archify tool installation and lifecycle**: the discovery
  symlink, the clone/package identity (version, license, authorship), the
  schemas/references/renderers inventory, the update-notice contract, the installed
  scoping-skill copy, and the runtime output convention.
- **The upstream repository's content** beyond the recorded version identity is not
  probed — the version pin is a recorded fact re-verified only at the gate
  (AR3-1, mechanical audit).
- **gbrain's sync state and the Memory Governor** belong to their own modules —
  Archify's *relationship* to them (no dedicated GBrain page; not a memory writer)
  is what this module verifies, never the memory systems themselves.
- **Graphify's structural graph and GStack's design-HTML** are complementary /
  different-domain skills — their health belongs to their own modules; this module
  only confirms the recorded "no dependency in either direction" relationship.
- **The quality of any past diagram subject** (e.g. the memory-ecosystem run) is
  out of scope — this exam performs its own bounded functional proof at Tier 3 and
  treats prior subjects as non-evidence per developer instruction.
- **`output/` artifact content** is convention-verified, never judged.

## Credential discipline (hard rule)

This system has no distinct credential requirement. The generic rule still binds:
credentials are referenced by variable name only — never printed, logged, or copied
into reports, outputs, or learnings.

## Hard behavioral rules (from the suite's own settled policy + do-not list)

- **Never update the source clone/package by any agent action.** Update is
  developer-run only; Archify's own update checker is notification-only and never
  downloads/installs/executes anything. A version drift is a finding to report,
  never a reason to mutate the clone.
- **Never modify `~/.config/opencode/skills/mb-archify-scope/SKILL.md`** — if it
  drifts from [[archify-scope-skill|Scoping Skill Specification]], report the gap; re-sync is a developer/gated
  action with the spec as source of truth. Never create a second discovery path for
  the scope skill or the tool (double-load).
- **Never submit skill content through the Memory Governor** — ordinary `gbrain
  sync` only (the ecosystem's standing bypass for skill content).
- **Never delete `output/` artifacts** of prior runs — retirement/removal is a
  developer decision, not an exam action.
- **Do not run `preview`** during the exam — it starts a live loopback watcher.
  Functional proof uses `doctor` + `validate` only (read-only).
- **Update-check `--ack` is never run** during an exam — acknowledging a reminder
  is a developer-owned action outside detection.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| AR0-1 | A | Discovery symlink resolves: `readlink ~/.config/opencode/skills/archify` | `archify` → `/mnt/c/mybizz/archify/archify` (config §Install on this machine — Discovery path). Missing/broken symlink = DOWN, stop |
| AR0-2 | A | CLI entry executable: `node bin/archify.mjs --help` (from `/mnt/c/mybizz/archify/archify`) | `bin/archify.mjs` exists and returns usage (config §Identity — CLI entry point). No such file or non-zero = DOWN, stop |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AR1-1 | A | Version identity: `node -p "require('./archify/package.json').version"` in `/mnt/c/mybizz/archify` + `head -5 archify/SKILL.md` | package.json `2.16.0`; SKILL.md frontmatter `version: "2.16"` (config §Identity — Version). Divergence = DRIFT |
| AR1-2 | A | Install architecture: symlink topology — `ls -la ~/.config/opencode/skills/archify` one entry (the tool package via symlink); discovery path resolves to the clone | Exactly one discovery entry; path `~/.config/opencode/skills/archify` → `/mnt/c/mybizz/archify/archify` (config §Install on this machine). Duplicate/broken = DRIFT/UNHEALTHY |
| AR1-3 | A | Package structure live-counted (config §Package structure): `schemas/` = 6 `.schema.json` (`common`, [[architecture|Architecture]], `workflow`, `sequence`, `dataflow`, `lifecycle`) + `README.md`; `references/` = 4 files (`authoring-contract`, `brand-marks`, `delivery-contract`, `viewer-runtime`); `renderers/` per-type + `shared/`; `bin/archify.mjs` present | Counts and paths match config §Package structure. Missing/moved/changed = DRIFT |
| AR1-4 | A | Suite completeness: the eight regular files in `archify/` (config, exam-plan, exam-report, log, learnings, explainer, reference, skill) + the scope-skill spec | All present (missing file = GAP) |
| AR1-5 | A | Update-notice contract: `grep -c "ARCHIFY_UPDATE_CHECK_DISABLED\|notification" archify/SKILL.md` + env check `echo "${ARCHIFY_UPDATE_CHECK_DISABLED:-unset}"` | Config §Install on this machine — update check is notification-only, never downloads/installs/executes; `ARCHIFY_UPDATE_CHECK_DISABLED=1` is the documented disable. Env present-or-unset recorded; contract text present = pass. Manifest URL NOT fetched (out of scope, W-3) |
| AR1-6 | A | Integration facts (config §Integration with other system parts): OpenCode `/archify` invocation recorded; GBrain "no dedicated page" finding still plausible (does not require a search — recorded fact); Memory Governor "no treatment — not a governed writer" recorded; Cupcake "no archify-specific rule" — provisional, re-qualified against [[cupcake-config|Cupcake Configuration]]'s Current Operational Status at run time | Recorded facts unchanged; Cupcake provisional wording honored (no assumption of current enforcement) |

## Tier 2 — Functional proof (present ≠ working; read-only — no changes to the installation from detection)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AR2-1 | A | Doctor probe: `node bin/archify.mjs doctor` (read-only; verifies runtime + all five renderer/schema/example triads) | 15/15 checks pass, final line "Archify is ready" (config §Identity — Doctor status). Any check fail = finding; capture output to a file, never pipe live output to a truncating consumer |
| AR2-2 | A | Skill invocability through discovery: `head -5 ~/.config/opencode/skills/archify/SKILL.md` | Real `name: archify` frontmatter + description resolve through the symlink; skill invocable as `/archify` (config §Identity — Invocation). Empty/None = finding |
| AR2-3 | A | Scoping-skill component integrity: `sha256sum archify/archify-scope-skill.md ~/.config/opencode/skills/mb-archify-scope/SKILL.md` | Two hashes identical (config §Scoping skill component — "kept byte-identical to the spec"). Divergence = DRIFT finding (spec edited without re-copy, or installed copy edited) |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AR3-1 | D | Full mechanical integrity audit: `sha256sum` of package.json, `bin/archify.mjs`, `SKILL.md`, and the 10 package-structure files (6 schemas + README, 4 references); byte counts exact; working tree clean (`git -C /mnt/c/mybizz/archify status --short`) | Every hash/count stable vs the package's recorded state; tree clean or only known untracked sidecar files (visual-check PNGs, examples). Cost: ~12 hashes, 0 writes |
| AR3-2 | D | Functional-ability acceptance: live bounded render proof — `doctor` (re-run) + `validate` of a representative example at showcase quality (e.g. `examples/web-app.architecture.json`) | doctor 15/15; validate returns the showcase receipt (9 artifact checks, 0 composition errors, 0 warnings) with `meta.quality_profile` honored. This is the acceptance record — the tool demonstrably renders; no deep re-authoring of a full subject is required |
| AR3-3 | D | Open-item dispositions (config §Open items): (a) symlink creation method (WSL-side vs Windows `mklink /D`) — recorded verdict or deliberate deferral; (b) Windows Explorer visibility through the symlink — unverifiable from WSL, deliberate disposition recorded; (c) update-check manifest URL — recorded as deliberately out of scope | Dispositions recorded; spec edits (if any follow) only via docs governance |
| AR3-4 | D | Supply-chain / adoption review (config §Identity — License MIT, Author tt-a1i, Based on Cocoon-AI/architecture-diagram-generator MIT v1.0): perform + record the adoption review on the established axes (publisher, license, maintenance, spawn-capability per [[sec-review-before-trust|Review Before Trust]] / [[sec-dependency-skill-supply-chain|Dependency and Skill Supply Chain]]), or record a deliberate deferral | Review performed and recorded (or deferral recorded with reason) |
| AR3-5 | D | Update-notice + integration discipline re-confirmation: the tool's only network surface is the notification-only checker; update decisions stay developer-owned; scope-skill copy stays in sync; ordinary `gbrain sync` only for content | Policy intact, restated. No action unless the developer deliberately decides otherwise |

## Report

Write [[archify-exam-report|Exam Report]]: verdict line; per-tier tables (check ID, expected,
actual, result); findings with class + evidence + recommended repair + risk; runner
attribution for every deferred item (guard-forbidden vs unlock-gated); overwritten
in full each run (write-then-replace: failed runs never touch the prior report;
written before any pruning). Then: one run row appended to [[archify-log|Log]]
(run-row format per [[config-manager-reference|Reference: Commands, Procedures]]); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — every repair/decision is developer-run
  (clone/update policy, scope-skill re-sync if drifted, open-item dispositions,
  adoption review) or proposal-first (spec corrections → docs governance)
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the Archify source clone/package
  (`/mnt/c/mybizz/archify/` — never fetched/pulled/reset by an agent) · the
  discovery symlink (never a second path, never a duplicate) · the installed
  scope-skill copy (re-sync is gated; spec is source of truth) · any
  Memory-Governor submission of skill content (permanent ordinary-`gbrain` bypass) ·
  `output/` artifacts of prior runs (never deleted by this exam) · `preview` /
  update-check `--ack` (never launched during an exam)
- Credentials: variable names only, never printed
