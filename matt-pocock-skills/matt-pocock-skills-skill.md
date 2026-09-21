---
name: mb-config-matt-pocock-skills
description: Matt Pocock Skills configuration exam — verifies the 35-skill installation's live configuration state (source clone pin, symlink topology, broken links, per-project setup gate, upgrade standing-rule, inventory conformance) against matt-pocock-skills-config.md and proves the set functionally resolves; detection and verification only — the installation is working well and this module changes nothing; catches silent failures and proposes gated repairs. Use when asked to "exam matt pocock skills", "check matt pocock skills health/install", or as part of a full mb-config-manager run.
---

# mb-config-matt-pocock-skills — Exam Skill

Exams the Matt Pocock skills installation's configuration state against its spec.
This skill holds the **procedure** only — expected values live in the spec doc and
are read fresh at the start of every run. The installation is working well; this
exam verifies that and repairs nothing.

- Spec: [[matt-pocock-skills-config|Matt Pocock Skills Configuration]] — read it first, every run
- **Exam plan: [[matt-pocock-skills-exam-plan|Exam Plan]] — read
  second, every run.** The plan-driven cycle: the config-manager synthesizes
  this plan fresh before each run (from spec + last report + log + learnings)
  and this skill executes it in hand. The plan carries run-specifics and
  deltas; the **standing check inventory lives in this skill** (below) —
  permanent occurrences graduate here, never into plans
- Reference: [[matt-pocock-skills-reference|Matt Pocock Skills Reference]] — invocation,
  standing rules, per-project setup gate, inline-execution table
- Report: [[matt-pocock-skills-exam-report|Exam Report]] — one file,
  overwritten each run (write-then-replace)
- Log: [[matt-pocock-skills-log|Log]] — one run row per exam;
  free rows for notable events witnessed between runs
- Learnings: [[matt-pocock-skills-learnings|Learnings]] — file new
  patterns/nuances; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the matt-pocock skill installation and lifecycle**: source
  clone pin, symlink topology in `~/.agents/skills/`, broken links, per-project
  setup gate, the no-upgrade standing rule, and inventory conformance.
- **The 5 Anvil skills sharing the `~/.agents/skills/` root** (`anvil-yaml`,
  `client-forms`, `client-modules`, `data-models`, `server-code`) belong to
  `anvil-agent-references` — this exam verifies coexistence **presence only**,
  never touches, never inventories them, never treats them as findings.
- **GStack's install locations and skill inventory** belong to `mb-config-gstack`
  — no shared entries with the matt set are expected; GStack's own state is
  never probed here.
- **`spawn-tools-denylist.json` and Cupcake guard policy** belong to the
  cupcake/opencode modules — referenced as standing rules, never re-verified.

## Credential discipline (hard rule)

This system has no distinct credential requirement. The generic rule still binds:
credentials are referenced by variable name only — never printed, logged, or
copied into reports, outputs, or learnings.

## Hard behavioral rules (from the suite's own Do-not list)

- **Never spawn sub-agents in any form** — the environment denies the
  Task/spawn tool family (denied natively, denied by Cupcake, denied in
  `spawn-tools-denylist.json`). Three skills are written for a spawning
  environment; execute them **inline** per the reference's table:
  `/code-review` (run both axes sequentially), `/wayfinder` (resolve research
  tickets in-session), `/ask-matt` (do the work in-session or hand the developer
  a precise checklist).
- **Never upgrade, pull, or reinstall the source clone** — updates/upgrades are
  deliberate-decision-only (standing rule, 2026-09-08). A pinned-head check is a
  state verification; a drift in HEAD is a finding, never a reason to pull.
- **Never use an engineering skill (`/to-tickets`, `/to-spec`, `/triage`,
  `/code-review` and their dependents) in a project that has not been through
  `/setup-matt-pocock-skills`** — they read a project contract; running them
  without it makes the skill guess.
- **Never treat GStack's skill inventory as part of this set** (separate
  discovery paths), and never confuse Matt's `/handoff` with a GStack command.
- **Never delete or alter the 5 Anvil shared-root entries** while managing this
  set — different owner, same root.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| MP0-1 | A | Source clone present + pinned: `git -C /mnt/c/mybizz/matt-pocock-skills-source rev-parse HEAD` | `84fdeff` (config §Identity — source clone). Clone missing or HEAD moved = DOWN (INVESTIGATE — never pull) |
| MP0-2 | A | Discovery root reachable: `ls ~/.agents/skills/` returns the matt set — symlinks resolving into `skills/{engineering,productivity,in-progress,misc}` of the source clone | 35 matt symlinks (config §Install topology; §Skill inventory 35 = 18+7+6+4). Root missing / set missing = DOWN, stop |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MP1-1 | A | Link graph: `find ~/.agents/skills/ -maxdepth 1 -type l` = 40 total, of which 35 target the matt source clone + 5 target `anvil-agent-references/skills/`; broken = 0 (`find -L ... -type l`); the only non-symlink entry is the `matt-pocock-skills-reference.md:Zone.Identifier` artifact | 40 symlinks = 35 matt + 5 anvil; 0 broken (config §Install topology — Broken links 0). Divergence in count or target = DRIFT |
| MP1-2 | A | Per-project setup gate (reference §Mandatory per-project setup gate): for each of the 5 named projects, `ls <project>/agents/` — the four files `domain.md` `instructions.md` `issue-tracker.md` `triage-labels.md` present or absent; project paths per config §Per-project setup state | `makepdlf` = Yes (4 files), the other four = No (config §Per-project setup state table). Any flip = DRIFT (note: a project newly configured is progress, flag the spec for refresh — never auto-update) |
| MP1-3 | A | Upgrade state: HEAD unchanged (already MP0-1) **and** no new install artifacts — `~/.agents/skills/` holds nothing but the recorded symlinks + the Zone.Identifier file; no `npx skills`/plugin-path install present anywhere under the root | Manual pinned clone + symlinks only (config §Identity — Install method; §Installed topology — nothing copied). A copied skill dir or plugin artifact = UNHEALTHY |
| MP1-4 | A | Inventory conformance: the 35 matt symlink names split exactly 18 / 7 / 6 / 4 across category folders in the source clone (`engineering` 18, `productivity` 7, `in-progress` 6, `misc` 4); `deprecated/` holds a README only | 18+7+6+4 = 35, names match the catalog rows (config §Skill inventory). Member added/removed/moved between categories = DRIFT |
| MP1-5 | A | Suite completeness: the seven files in `matt-pocock-skills/` (config, exam-plan, exam-report, log, learnings, explainer, reference) | All present (missing file = GAP) |
| MP1-6 | A | GStack relationship: no shared entries — no GStack skill name appears in `~/.agents/skills/`, and all 35 matt symlink targets stay under the source clone's `skills/` tree | No shared entries (config §Install topology — GStack relationship). A cross-target symlink = DRIFT |
| MP1-7 | A | Zone.Identifier artifact: `~/.agents/skills/matt-pocock-skills-reference.md:Zone.Identifier` present, size 25 B | Present, inert (config §Install topology — Stale artifact + §Open items). Absence = recorded-state change to note (cleanup happened), not a defect |

## Tier 2 — Functional proof (present ≠ working; read-only — no changes to the installation from detection)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MP2-1 | A | Reachability + frontmatter sweep (reference §Invocation): for each of the 35 matt symlinks (glob off the resolved matt targets), `head -5 <name>/SKILL.md` | SKILL.md exists at every target and shows real `name:`/`description:` frontmatter; resolve through the symlink; no empty/missing file = all PASS. Any skill whose command would fail this check → the finding (per reference: file exists but command fails → check the symlink) |
| MP2-2 | A | Discipline probe — the three sub-agent-referencing skills resolve and carry the inline-execution expectation: `head -5 ~/.agents/skills/{code-review,wayfinder,ask-matt}/SKILL.md` | Real frontmatter on all three (they are the environment's key adaptations — inline execution); their SKILL.md resolves through the symlink. This is the present-≠-working guard on the set's most specialized members |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| MP3-1 | D | Full mechanical integrity audit: every one of the 40 symlinks resolves to its intended target (35 → source clone `skills/<category>/<name>/`, 5 → anvil-agent-references); all 35 SKILL.md files present and byte-identical to their source counterpart; full inventory re-count 18/7/6/4 | Every link correct, every SKILL.md matches source bytes, every category count exact. Cost: ~40 reads incl. hash of 35 files; 0 writes. This is the exhaustive sweep that Tier 2 samples |
| MP3-2 | D | Deliberate upgrade decision (standing rule, 2026-09-08): now that the exam is live, re-confirm no-upgrade posture; note upstream divergence (clone `84fdeff` vs upstream HEAD ~1 month newer) as the recorded open item | Decision recorded, no action unless the developer deliberately decides otherwise (config §Identity — Upgrade policy). Stay-pinned is the expected default; never on newness |
| MP3-3 | D | Zone.Identifier artifact cleanup decision: `~/.agents/skills/matt-pocock-skills-reference.md:Zone.Identifier` (25 B, inert) | Developer decides keep/remove (config §Open items — cleanup optional). If removed, spec's open item closes via governance |

## Report

Write [[matt-pocock-skills-exam-report|Exam Report]]: verdict line; per-tier tables (check
ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[matt-pocock-skills-log|Log]] (run-row format per
[[config-manager-reference|Reference: Commands, Procedures]]); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — the matt set is a deliberate-manual
  install; every repair/decision is developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the 5 Anvil entries in the shared root
  (different owner) · the source clone (never pulled/upgraded/reinstalled —
  standing rule) · any sub-agent spawn attempt (execute inline) · any
  `npx skills` / plugin-path install, ever
- Credentials: variable names only, never printed
