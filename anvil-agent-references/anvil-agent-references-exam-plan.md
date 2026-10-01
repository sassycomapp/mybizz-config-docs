---
title: "anvil-agent-references-exam-plan"
doc-id: "mb-0aa9e73d"
updated: "2026-10-01"
---
# anvil-agent-references — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-config|Configuration]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-config.md) (spec), the last
[[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-exam-report.md), [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-log|Log]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-log.md) (events since
last run), [[[mybizz-config-docs:anvil-agent-references/anvil-agent-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-learnings.md). Consumed by the skill at run time; rewritten
at the start of the following cycle. The file is live; its contents are transient.

**This first plan is hand-written** (emulation of the established architecture):
it also serves as the format template. The **standing check inventory lives in the
skill** ([[[mybizz-config-docs:anvil-agent-references/anvil-agent-skill|Anvil Agent Skill]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-skill.md), born-with-inventory); this plan carries
run-specifics and references. Once verified by a run, future plans carry
run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) any check whose command text the guards deny (unexpected for this system — no sensitive-data config content in scope; the sensitive-file guard may deny the session-start-adjacent paths, but those are not exam targets; denied anyway → bundled, honored absolutely); (b) Tier 3 items if unlocked — AR3-1 (full mechanical audit) is the likely unlock candidate |
| Expected-value source of truth | [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-config\|Configuration]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-config.md) — read fresh at run start; never rely on remembered values |
| Scope boundary | This module exams **the anvil-agent-references install lifecycle**: the source clone (`/mnt/c/mybizz/anvil-agent-references`), the 5 symlinks in `~/.agents/skills/` (anvil-yaml, client-forms, client-modules, data-models, server-code), GBrain registration of source `anvil-agent-references-code`, and repository structure (stubs, type refs, docs/m3, plugin metadata). The 35 Matt Pocock symlinks sharing `~/.agents/skills/` belong to `mb-config-matt-pocock-skills` — coexistence **presence/count only**, never touched, never inventoried. GStack's install locations and skill inventory belong to `mb-config-gstack`. `anvil-docs/` (separate vendor-docs mirror) is adjacency only — out of exam scope. Cupcake guard policy and `spawn-tools-denylist.json` belong to the cupcake/opencode modules, not this exam |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). The spec's former **open items** were
**all closed 2026-09-16** (config.md open-items table + adoption review). They
remain as watch rows for this run (observations, not findings):

| # | Watch item (formerly config open items) | This run's action |
|---|---|---|
| W-1 | Clone was updated to `7c9b0a7`; a fresh one-commit upstream drift (`afe281d`, origin 2026-09-16) has since landed. Spec §Identity recaptured the delta and closed open item 1 | Re-probe HEAD live; if the clone has not been pulled again, state matches the recorded drift — record as observation, next update is developer-run |
| W-2 | License: none found; adoption review recorded 2026-09-16 (four axes, license axis = documented accepted risk). Open item 2 closed | Confirm LICENSE absence live; the record stands unless the developer pursues the upstream adoption route |
| W-3 | Per-project setup in `mb-3-cs`, `mb4ecom`, `mb5pdlf` app roots = deliberate trigger-bound deferral tied to project init (cupcake-config project-init status). Open item 3 closed | Verify the recorded Done/Not-done matrix live (AR1-4); a project initializing is progress — flag the spec for refresh, never self-update |
| W-4 | Tier-2/3 verification record stands as the confirmed on-record skill verification (open item 4 closed) | No live probe; an in-app first invocation is a future verification event, not a defect. Note in report |
| W-5 | gbrain source index-state corrected (34 pages, last sync 2026-09-06; open item 5 closed) | Confirm source registration + page count live (AR1-6); a re-sync after any future clone update is the developer's call |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-08-12 initial install (5 symlinks, symlink-only, nothing copied) | AR0-1/AR0-2 verify the topology still holds |
| LG-2 | 2026-09-06 suite created; gbrain source registered via host CLI; OpenCode discovery confirmed | AR1-1/AR1-5/AR1-6 re-verify the recorded facts are still true |
| LG-3 | 2026-09-16 upstream update observed (clone at `7c9b0a7`; stubs 63; gbrain 34 pages) | Re-probe HEAD, stub count, gbrain source state live; classify deltas at the gate (W-1/W-5) |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| — | none (learnings file empty at bootstrap) | — |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[[mybizz-config-docs:anvil-agent-references/anvil-agent-skill|Anvil Agent Skill]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-skill.md) (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** AR0-1 source clone present + HEAD reachable · AR0-2 discovery root `~/.agents/skills/` returns the anvil set (5 symlinks → clone's `skills/`). Failure = DOWN, stop.
- **Tier 1 (A) — state conformance:** AR1-1 link graph (5 anvil symlinks; 0 broken; total link count = 40 shared-root with the matt set, presence-only) · AR1-2 OpenCode discovery (no second discovery path, no `~/.claude/skills/` anvil entries) · AR1-3 repository structure (skills/ 5, stubs 63 = 31 client + 32 server per config §Repository structure — read fresh, reference/types 3, docs/m3 layout, plugin metadata) · AR1-4 per-project setup state (2 Done / 3 Not-done — Not-done = deliberate, project-init-tied; per the recorded matrix) · AR1-5 suite completeness (7 files) · AR1-6 GBrain source registration (`anvil-agent-references-code`, non-federated) · AR1-7 stale external references absent (`/mnt/c/mybizz/config`, `skills-collective`, `docs/material-3`)
- **Tier 2 (A) — functional, present ≠ working:** AR2-1 reachability/frontmatter sweep (5 skills via symlink, real `name:`/`description:` frontmatter) · AR2-2 discipline probe — the 5 roles in the clone's `AGENTS.md` Shared-Resources block present (the per-project copy source)
- **Tier 3 (D, locked):** AR3-1 full mechanical integrity audit (5 links + stub/type/doc counts + 5 SKILL.md byte-identity with vendor) · AR3-2 deliberate update + license decision (standing rule: stay current; upstream drift noted; license axis formally unmet) · AR3-3 per-project setup closure decision (the 3 Not-done roots)

## 7. Report requirements

The run writes [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-exam-report.md): verdict line; per-tier
tables (check ID, expected, actual, result); findings with class + evidence +
recommended repair + risk; runner attribution for every deferred item
(guard-forbidden vs unlock-gated); overwritten in full each run
(write-then-replace; failed runs never touch the prior report; written before any
pruning). Then: one run row appended to [[[mybizz-config-docs:anvil-agent-references/anvil-agent-references-log|Log]]](C:/mybizz/mybizz-config-docs/anvil-agent-references/anvil-agent-references-log.md)
(run-row format per [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md)); new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — the anvil set is a vendor-generated,
  symlink-installed, developer-maintained checkout; every repair/decision is
  developer-run or proposed
- Spec-doc corrections (the observed clone-update delta, stub count, gbrain page
  count) → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the 35 matt entries in `~/.agents/skills/`
  (different owner) · the source clone (AI-run `git pull` prohibited — the clone
  sits outside every project root; cross-project write; developer-run only) ·
  project `AGENTS.md`/`CLAUDE.md` writes (AI prohibited — the per-project setup is
  developer-run) · `anvil.yaml` writes in any app (standing policy, Cupcake
  enforced when active) · editing the generated checkout · Memory Governor
  submission of this source (permanent bypass — ordinary `gbrain sync` only)
- Credentials: variable names only, never printed
