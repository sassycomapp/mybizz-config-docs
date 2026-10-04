---
title: "anvil-agent-skill"
doc-id: "mb-c6a3ff36"
updated: "2026-10-04"
---
# mb-config-anvil-agent-references — Exam Skill

Exams the anvil-agent-references installation's configuration state against its
spec. This skill holds the **procedure** only — expected values live in the spec
doc and are read fresh at the start of every run. The installation is working
well; this exam verifies that and repairs nothing.

- Spec: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-config|Configuration]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-config.md) — read it first, every run
- **Exam plan: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-exam-plan.md) —
  read second, every run.** The plan-driven cycle: the config-manager synthesizes
  this plan fresh before each run (from spec + last report + log + learnings)
  and this skill executes it in hand. The plan carries run-specifics and
  deltas; the **standing check inventory lives in this skill** (below) —
  permanent occurrences graduate here, never into plans
- Reference: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-reference|Reference: Install, Skills, and Technical Detail]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-reference.md) —
  installation, per-skill rules, update procedure, GBrain sync path
- Explainer: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-explainer.md) — what
  this is, suitability, runtime constraints, open items
- Report: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-exam-report.md) — one
  file, overwritten each run (write-then-replace)
- Log: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-log|Log]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-log.md) — one run row per
  exam; free rows for notable events witnessed between runs
- Learnings: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-learnings.md) — file new
  patterns/nuances; delete entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **the anvil-agent-references install and lifecycle**: source
  clone at `/mnt/c/mybizz/anvil-agent-references`, the 5 symlinks in
  `~/.agents/skills/` (`anvil-yaml`, `client-forms`, `client-modules`,
  `data-models`, `server-code`), OpenCode discovery discipline, repository
  structure (stubs, type refs, `docs/m3/`, plugin metadata), per-project setup
  state, GBrain source registration, and stale-reference absences.
- **The 35 Matt Pocock symlinks sharing the `~/.agents/skills/` root** belong to
  `mb-config-matt-pocock-skills` — this exam verifies coexistence **presence/
  count only**, never touches, never inventories them, never treats them as
  findings (link-count checks include them only as the recorded shared-root
  total).
- **GStack's install locations and skill inventory** belong to `mb-config-gstack`
  — no shared entries with the anvil set are expected; GStack's own state is
  never probed here.
- **`anvil-docs/`** (`C:\dev\project-library-global\anvil-docs\`) is a separate
  vendor-docs mirror — adjacency only, out of exam scope.
- **`spawn-tools-denylist.json` and Cupcake guard policy** belong to the
  cupcake/opencode modules — referenced as standing rules, never re-verified.

## Credential discipline (hard rule)

This system has no distinct credential requirement. The generic rule still binds:
credentials are referenced by variable name only — never printed, logged, or
copied into reports, outputs, or learnings. This source is vendor-published
reference material with **no Memory Governor involvement** (permanent bypass —
ordinary `gbrain sync` only).

## Hard behavioral rules (from the suite's own Do-not list)

- **Never AI-run the update `git pull`** in the source clone — developer-run
  only, from a terminal. The clone sits outside every project root; an AI-run
  write there is a cross-project write (Cupcake's cross-project-write rule
  blocks when active). A HEAD check is a state verification; a HEAD delta is a
  finding to classify at the gate — the clone is **never pulled, upgraded, or
  mutated by this exam under any circumstance**.
- **Never AI-write `anvil.yaml`, ever, in any project** — standing policy
  regardless of enforcement status (`cup-block-anvil-yaml-writes.rego` enforces
  mechanically when active); route the change to the developer.
- **Never AI-write any project's `AGENTS.md`/`CLAUDE.md`** — including the
  per-project setup step (`cup-protected_ai_governance_files_may_not_be_modified
  .rego` enforces when active); developer-run either way.
- **Never submit this source's content through Memory Governor** — permanent
  bypass; ordinary `gbrain sync` only.
- **Never edit the generated checkout** or `.anvil/` dependency material in an
  app — read-only reference.
- **Never create a second discovery path** for any of these skills (no
  `~/.claude/skills/` anvil links, no project-local copies) — dedup is by
  discovery path; duplicates double-load.
- **Never treat the 35 matt entries in `~/.agents/skills/` as exam material** —
  different owner, same root (coexistence presence only).
- **Never guess unfamiliar `anvil.*` symbols, dependency properties, roles, or
  CSS hooks** — confirm from stubs/docs/examples; never treat a passing
  `anvil --json validate` as proof a runtime API or dependency property exists.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| AR0-1 | A | Source clone present + HEAD reachable: `git -C /mnt/c/mybizz/anvil-agent-references rev-parse HEAD` and `--abbrev-ref HEAD` | Returns a HEAD on branch `master` (config §Identity — Installed HEAD; read fresh from spec). Clone missing / not a git repo / HEAD unreadable = DOWN (INVESTIGATE — never pull) |
| AR0-2 | A | Discovery root reachable: `ls ~/.agents/skills/` returns the anvil set — symlinks `anvil-yaml`, `client-forms`, `client-modules`, `data-models`, `server-code` resolving into the clone's `skills/`. Verify with `ls -la ~/.agents/skills/ | grep anvil-` and `readlink -f` on each | 5 anvil symlinks → `.../anvil-agent-references/skills/<name>` (config §Install architecture — Symlinks). Root missing / anvil set missing = DOWN, stop |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AR1-1 | A | Link graph: `find ~/.agents/skills/ -maxdepth 1 -type l` = 40 total, of which 5 target the anvil clone's `skills/` + 35 target the matt source clone; broken = 0 (`find -L ~/.agents/skills/ -maxdepth 1 -type l`); the only non-symlink entry is the matt `Zone.Identifier` artifact | 40 symlinks = 5 anvil + 35 matt; 0 broken; the 5 anvil targets exactly `anvil-agent-references/skills/{anvil-yaml,client-forms,client-modules,data-models,server-code}` (config §Install architecture; §Repository structure — skills/). Divergence in count or target = DRIFT |
| AR1-2 | A | Discovery discipline: no second discovery path for any anvil skill — `ls ~/.claude/skills/` shows no anvil entries; no `<project>/.agents/skills/anvil-*` project-local copies in the 5 named projects (`dev-makepdlf/makepdlf-project-library`, `dev-mb-3-cs/mb-3-cs-project-library`, `dev-mb-3-cs/mb-3-cs`, `dev-mb4ecom/mb4ecom`, `dev-mb5pdlf/mb5pdlf`) | No duplicate paths (config §Install architecture — Duplicate discovery paths: none). An entry = UNHEALTHY (double-load risk) |
| AR1-3 | A | Repository structure: `ls skills/` (5 folders) · stub counts `find stubs -name "*.pyi" | wc -l` per client/server · `ls reference/types/` (3 `.d.ts`) · `ls docs/` + `docs/m3/` layout · plugin metadata `cat .codex-plugin/plugin.json` + `cat .claude-plugin/plugin.json` (name `anvil`, version `1.0.0`) | skills/ 5 named per inventory; stub counts per config §Repository structure — **read fresh from the spec every run, never remembered** (last verified 2026-09-16: 63 = 31 client + 32 server); reference/types 3 files; docs/m3 structure per config; plugin name/version per config §Plugin metadata (verified from disk). A drift between spec and live = classify at the gate; the spec was corrected to live on 2026-09-16 |
| AR1-4 | A | Per-project setup gate (config §Per-project setup status): for each of the 5 recorded projects, check `AGENTS.md` for the "Anvil Agent References (skills available via ~/.agents/skills/)" section marker (`grep -c "Shared Anvil Resources" <project>/AGENTS.md` or the recorded marker) | makepdlf-project-library = Done, mb-3-cs-project-library = Done, mb-3-cs / mb4ecom / mb5pdlf = Not done (config §Per-project setup status table). Any flip = DRIFT (note: a project newly configured is progress, flag the spec for refresh — never auto-update) |
| AR1-5 | A | Suite completeness: the seven files in `anvil-agent-references/` (config, exam-plan, exam-report, log, learnings, explainer, reference) | All present (missing file = GAP) |
| AR1-6 | A | GBrain source registration: `gbrain sources list` shows source id `anvil-agent-references-code`, path `/mnt/c/mybizz/anvil-agent-references`, non-federated (registered 2026-09-06 via host CLI) | Source registered with that id + path (config §GBrain registration). Missing id / wrong path = DRIFT. Page count / last-sync deltas observed (34 pages at orientation) → recorded as state-change observations, classified at the gate — registration itself is the conformance fact |
| AR1-7 | A | Stale external references absent: `ls -d /mnt/c/mybizz/config`, `/mnt/c/mybizz/skills-collective`, `.../anvil-agent-references/docs/material-3` | All three absent — those paths do not exist (config §Known stale external references: verified reality). Any resurrected path = DRIFT |

## Tier 2 — Functional proof (present ≠ working; read-only — no changes to the installation from detection)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AR2-1 | A | Reachability + frontmatter sweep (reference §Installing — OpenCode): for each of the 5 anvil symlinks, `head -5 ~/.agents/skills/<name>/SKILL.md` | SKILL.md exists at every target with real `name:`/`description:` frontmatter, resolves through the symlink; no empty/missing file = all PASS. Any skill whose command would fail this check → the finding (per reference: file exists but command fails → check the symlink) |
| AR2-2 | A | Discipline probe — the shared-resource block source (reference §The required follow-up step; config §Repository structure — AGENTS.md): the clone's `AGENTS.md` carries the "Shared Anvil Resources" block defining the **5 resource roles** (client stubs, server stubs, type references, docs, skills) | Block present with 5 roles (config §Repository structure — AGENTS.md: 5 resource roles — the current count). This block is what every app project copies at setup; its integrity is the present-≠-working guard on the per-project setup mechanism |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| AR3-1 | D | Full mechanical integrity audit: all 5 symlinks resolve to their intended clone targets; every SKILL.md present + byte-identical to its vendor source; exhaustive stub/type/doc/plugin counts vs the spec's recorded structure; plugin JSON contents verified against recorded values (name `anvil`, version `1.0.0`, documented descriptions) | Every link correct, all SKILL.md match vendor bytes, structure counts exact. Cost: ~15 reads incl. 5 SKILL.md hashes; 0 writes. This is the exhaustive sweep that Tier 2 samples |
| AR3-2 | D | Deliberate update + license decision: record the observed clone-update delta (installed HEAD moved to upstream `7c9b0a7`; stub count 63 at orientation) — decide whether the spec's Identity/Repository-structure rows get refreshed via docs governance, and re-confirm the no-license open item posture | Decision recorded; any spec refresh routed through docs governance, never self-applied. Stay-current-with-upstream is the expected default (generated checkout — update cadence is an operational habit, not a no-upgrade pin) |
| AR3-3 | D | Per-project setup closure decision: for the 3 Not-done app roots (`mb-3-cs`, `mb4ecom`, `mb5pdlf`), confirm whether the developer will run the setup step (AI writes to project `AGENTS.md` are prohibited either way) | Decision recorded (done-later / declined / scheduled); open item carried until the developer acts |

## Report

Write [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-exam-report.md): verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-log|Log]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-log.md) (run-row format per
[[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — the anvil set is a vendor-generated,
  symlink-installed, developer-maintained checkout; every repair/decision is
  developer-run or proposed
- Spec-doc corrections (clone-update delta, stub-count drift, gbrain page-count
  state) → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the 35 matt entries in the shared root
  (different owner) · the source clone (never pulled/upgraded/mutated by the
  exam; update = developer-run, standing discipline) · project
  `AGENTS.md`/`CLAUDE.md` writes (AI prohibited — per-project setup is
  developer-run) · `anvil.yaml` writes in any app · editing the generated
  checkout or `.anvil/` · Memory Governor submission of this source · any
  second discovery path for these skills
- Credentials: variable names only, never printed
