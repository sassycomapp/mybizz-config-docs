---
title: "magdoub-wireframe-skill"
doc-id: "mb-dd11c72e"
---
# mb-config-magdoub-wireframe — Exam Skill

Exams the Magdoub Claude Wireframe skill installation's configuration state
against its spec. This skill holds the **procedure** only — expected values live
in the spec doc and are read fresh at the start of every run. The installation
is working well; this exam verifies that and repairs nothing.

- Spec: [[magdoub-wireframe-config|Configuration]] — read it first, every run
- **Exam plan: [[magdoub-wireframe-exam-plan|Exam Plan]] — read
  second, every run.** The plan-driven cycle: the config-manager synthesizes
  this plan fresh before each run (from spec + last report + log + learnings)
  and this skill executes it in hand. The plan carries run-specifics and
  deltas; the **standing check inventory lives in this skill** (below) —
  permanent occurrences graduate here, never into plans
- Reference: [[magdoub-wireframe-reference|Reference: Invocation, Operation, Update]] — invocation,
  settled policy, do-not list
- Report: [[magdoub-wireframe-exam-report|Exam Report]] — one file,
  overwritten each run (write-then-replace)
- Log: [[magdoub-wireframe-log|Log]] — one run row per exam;
  free rows for notable events witnessed between runs
- Learnings: [[magdoub-wireframe-learnings|Learnings]] — file new
  patterns/nuances; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the magdoub-wireframe skill installation and lifecycle**:
  the real clone in `~/.claude/skills/wireframe/`, the OpenCode discovery
  symlink in `~/.config/opencode/skills/wireframe/`, the bundled file set, the
  runtime output structure, and the settled sync/update policy.
- **PDLF's step 22/26 usage** of the skill and the [[adr-design-rules|Wireframe Design Rules]] ADR interplay
  belong to the PDLF / project-library-global docs domain (config open item 4 —
  **resolved 2026-09-16**: ADR §A exempts Magdoub-created wireframes; other
  wireframes fully governed — referenced, never verified here, never treated as
  this module's findings)
- **The `task`-tool guard layer and spawn-tools policy** belong to the
  cupcake/opencode modules — referenced as the standing constraint on Phase 2
  (open item 1), never re-enforced or re-verified here.
- **gbrain's sync state and the Memory Governor** belong to their own modules
  — `gbrain sync` behavior is out of scope; this module only verifies the
  settled-policy record is intact (MW3-3).
- **The upstream repository's content** (beyond the recorded HEAD match) is not
  probed — upstream match is a recorded fact re-verified only at the gate.

## Credential discipline (hard rule)

This system has no distinct credential requirement. The generic rule still binds:
credentials are referenced by variable name only — never printed, logged, or
copied into reports, outputs, or learnings.

## Hard behavioral rules (from the suite's own settled policy + do-not list)

- **Never update the real clone by any agent action.** The update command
  (`git -C ~/.claude/skills/wireframe fetch origin && git -C
  ~/.claude/skills/wireframe reset --hard origin/main`) is **developer-run
  only, from a terminal** — never AI-invoked (settled policy 2026-09-06;
  cross-project-write rule). A HEAD drift is a finding to report, never a
  reason to pull.
- **Never execute Phase 2's parallel foreground Task agents as SKILL.md
  instructs** — sub-agent creation is prohibited standing policy (three-layer
  denial when active; enforcement status not fixed — check
  [[cupcake-config|Cupcake Configuration]]'s Current Operational Status before relying on any
  enforcement claim). The replacement mechanism is open item 1 — never
  improvised.
- **Never submit skill content through the Memory Governor** — permanent
  bypass; ordinary `gbrain sync` only (settled policy 2026-09-06).
- **Never create a second discovery path** for this skill — a duplicate
  double-loads it (dedup is by discovery path).
- **Never treat [[skills-register|Skill Register]] "working" as run evidence** — no confirmed
  real run exists (config §Integration facts).

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| MW0-1 | A | Real clone present + pinned: `git -C ~/.claude/skills/wireframe rev-parse HEAD` | `44a5814d1583c4dc7cafa36611838669f0895af9` (config §Identity — Installed HEAD). Clone missing or HEAD moved = DOWN (INVESTIGATE — never pull) |
| MW0-2 | A | OpenCode discovery path resolves: `readlink ~/.config/opencode/skills/wireframe/SKILL.md` | `/home/dev-p/.claude/skills/wireframe/SKILL.md` (config §Install architecture — two-hop). Missing/broken symlink = DOWN, stop |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MW1-1 | A | SKILL.md frontmatter identity: `head -5 ~/.claude/skills/wireframe/SKILL.md` | `name: wireframe`, description line matches config §Identity (Skill name); no version field in frontmatter (version is the git HEAD — config §Identity, Version field). Divergence = DRIFT |
| MW1-2 | A | Install architecture: `git -C ~/.claude/skills/wireframe remote get-url origin` + `git branch --show-current` + `git status --short` | Remote `https://github.com/Magdoub/claude-wireframe-skill.git`, branch `main`, working tree clean, local `main` == `origin/main` (config §Install architecture). Divergence = DRIFT |
| MW1-3 | A | Bundled files live-counted (config §Bundled files — live-counted 2026-09-06): `wc -l` the five counted files + list `README.md`, `LICENSE`, `examples/` | SKILL.md 404 lines · `wireframe/templates/base.css` 244 · `template.html` 274 · `self-reveal.css` 9 · `wireframe/brain/design-taste.md` 116; README + LICENSE present; examples/ = 3 PNGs. Missing/moved/changed count = DRIFT |
| MW1-4 | A | Runtime output structure — no-confirmed-run state: `ls ~/.claude/skills/wireframe/wireframe/brain/design-context.md` absent; no `wireframe/DDMM-*/` output dirs under project roots | `design-context.md` absent, no output dirs (config §Runtime output structure — created on first run; §Integration facts — Confirmed real runs: none). Presence = recorded-state change to note (a real run happened), not a defect |
| MW1-5 | A | Suite completeness: the eight files in `magdoub-wireframe/` (config, exam-plan, exam-report, log, learnings, explainer, reference, skill) | All present (missing file = GAP) |
| MW1-6 | A | Single discovery path: `ls -la ~/.config/opencode/skills/wireframe/` | Exactly one entry, the `SKILL.md` symlink; no duplicate `wireframe` entry elsewhere in `~/.config/opencode/skills/` (config §Install architecture — two-hop; reference do-not: no second discovery path). Duplicate = UNHEALTHY |
| MW1-7 | A | Old single-file reference state: `ls ~/.config/opencode/skills/wireframe/magdoub-claude-wireframe-skill-reference.md` | Present or absent, both recorded (config §Integration facts — pre-existing reference 2026-08-12; open item 5). Either state is a recorded fact — absence means retirement happened, note it, flag spec for refresh |

## Tier 2 — Functional proof (present ≠ working; read-only — no changes to the installation from detection)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MW2-1 | A | Reachability through the two-hop path: `head -5 ~/.config/opencode/skills/wireframe/SKILL.md` | Real `name`/`description` frontmatter resolves through the discovery symlink; skill invocable as `/wireframe` (config §Identity — Invocation). Empty/None frontmatter = finding |
| MW2-2 | A | Template-path integrity (Phase-1 copy sources): each file the run flow copies exists at its bundled path per SKILL.md Phase 1 — `wireframe/templates/base.css`, `template.html`, `self-reveal.css` | All three present at the bundled `wireframe/templates/` location with the recorded line counts (MW1-3; config §Bundled files). Resolves = the Phase-1 copy step is executable as designed |
| MW2-3 | A | Discipline probe — Phase-2 spawn constraint intact (open item 1): confirm the `task` tool is absent from the visible tool set and no Phase-2 parallel Task invocation is attempted this run | `task` tool absent from the available set; Phase 2 executes Phase-1-only or as the developer directs — never as SKILL.md's 5-parallel-Task-agent paragraph (config §Open items 1; reference §Phase 2). Presence/attempt = flag, gate immediately |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MW3-1 | D | Full mechanical integrity audit: SKILL.md byte count exact (27,731 B), `wc -l` every counted bundled file, `sha256sum` of SKILL.md + the three templates + design-taste.md, working tree clean, local `main` == `origin/main` | Every file's byte/line count matches config §Bundled files; tree clean; no local/origin divergence. Cost: ~6 hashes + counts, 0 writes. Exhaustive sweep that Tier 1/2 sample |
| MW3-2 | D | Open-item decisions (config §Open items): (a) **W-3** supply-chain review — perform and record the review owed at adoption (publisher, license, maintenance, spawn-capability per [[sec-review-before-trust|Review Before Trust]] / [[sec-dependency-skill-supply-chain|Dependency and Skill Supply Chain]]), or record a deliberate deferral; (b) **W-5** old single-file reference — retired or retained, deliberate decision; (c) **W-1** Phase-2 mechanism — direction if the developer chooses to decide now (main-agent sequential fallback vs Phase-1-only) | Decisions recorded; spec edits (if any follow) only via docs governance |
| MW3-3 | D | Update discipline re-confirmation (settled policy 2026-09-06): update command stays developer-run only, never AI-invoked; content reaches GBrain by ordinary `gbrain sync` only | Policy intact, restated. No action unless the developer deliberately decides otherwise |

## Report

Write [[magdoub-wireframe-exam-report|Exam Report]]: verdict line; per-tier tables (check
ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[magdoub-wireframe-log|Log]] (run-row format per
[[config-manager-reference|Reference: Commands, Procedures]]); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — every repair/decision is developer-run
  (update, open-item resolutions) or proposal-first (spec corrections → docs
  governance)
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the real clone `~/.claude/skills/wireframe/`
  (never fetched/pulled/reset by an agent — developer-run only) · Phase-2
  sub-agent spawning in any form (three-layer standing denial; open item 1) ·
  any Memory-Governor submission of skill content (permanent bypass) · the
  OpenCode discovery symlink (never a second path, never a duplicate) · the
  old single-file reference (retirement is a developer decision, not a
  deletion by this exam)
- Credentials: variable names only, never printed
