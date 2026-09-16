---
document: "Matt Pocock Skills — Exam Plan"
doc-id: matt-pocock-skills-exam-plan
state: Live
date-created: 2026-09-16
---

# Matt Pocock Skills — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: `matt-pocock-skills-config.md` (spec), the last
`matt-pocock-skills-exam-report.md`, `matt-pocock-skills-log.md` (events since last
run), `matt-pocock-skills-learnings.md`. Consumed by the skill at run time;
rewritten at the start of the following cycle. The file is live; its contents are
transient.

**This first plan is hand-written** (emulation of the established architecture):
it also serves as the format template. The **standing check inventory lives in the
skill** (`matt-pocock-skills-skill.md`, born-with-inventory); this plan carries
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
| Developer-run requests this run (bundled into ONE request) | (a) any check whose command text the guards deny (unexpected for this system — no sensitive-data config content in scope; denied anyway → bundled, honored absolutely); (b) Tier 3 items if unlocked |
| Expected-value source of truth | `matt-pocock-skills-config.md` — read fresh at run start; never rely on remembered values |
| Scope boundary | This module exams **the matt-pocock skill installation and lifecycle** in `~/.agents/skills/`. The 5 Anvil skills sharing the same root (`anvil-yaml`, `client-forms`, `client-modules`, `data-models`, `server-code`) belong to `anvil-agent-references` — coexistence presence only, never touched, never inventoried. GStack's install locations and inventory belong to `mb-config-gstack` — no shared entries expected, GStack's own state never probed. `spawn-tools-denylist.json` and Cupcake guard policy belong to the cupcake/opencode modules, not this exam |

## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states kept under watch
(observations, not findings):

| # | Watch item (config open items) | This run's action |
|---|---|---|
| W-1 | `~/.agents/skills/matt-pocock-skills-reference.md:Zone.Identifier` (25 B) inert Windows-Zone artifact — cleanup optional, no action taken | Confirm presence (recorded state; cleanup pending a deliberate decision only); absence = state change to note, not a defect |
| W-2 | Upstream's newest change (stop linking `misc/` into local skill directories, PR #1025) — noted for any future deliberate upgrade decision | No live probe; upgrade is deliberate-decision-only under the standing rule (MP3-2) |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-08-12 initial install topology (35 symlinks, clone-pinned) | MP0-1/MP0-2 verify the topology still holds |
| LG-2 | 2026-09-08 supersession (suite created; old `mybizz-os-docs` reference removed) | Single canonical home intact: suite completeness check (MP1-5); no revived stale claims observed (MP1-3) |
| LG-3 | 2026-09-16 suite build-out | MP1-5 suite completeness (7 files); run #1 is the closure |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| — | none (learnings file empty at bootstrap) | — |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in `matt-pocock-skills-skill.md` (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** MP0-1 source clone present + pinned at HEAD `84fdeff` · MP0-2 discovery root `~/.agents/skills/` returns the matt set (35 symlinks → source clone). Failure = DOWN, stop.
- **Tier 1 (A) — state conformance:** MP1-1 link graph (40 symlinks = 35 matt + 5 anvil; 0 broken) · MP1-2 per-project setup-gate state (1 Yes / 4 No) · MP1-3 upgrade state (pinned clone, manual-install only, no plugin/`npx` artifacts) · MP1-4 inventory conformance (18/7/6/4, deprecated README-only) · MP1-5 suite completeness (7 files) · MP1-6 GStack relationship (no shared entries) · MP1-7 Zone.Identifier artifact state
- **Tier 2 (A) — functional, present ≠ working:** MP2-1 full reachability/frontmatter sweep (35 skills, `head -5` → real `name:`/`description:` frontmatter through the symlinks) · MP2-2 category-live samples (one skill per category resolves and frontmatter matches source)
- **Tier 3 (D, locked):** MP3-1 full mechanical integrity audit (40 links + 35 bytes-identical to source) · MP3-2 deliberate upgrade decision (standing rule — never on newness) · MP3-3 Zone.Identifier artifact cleanup decision

## 7. Report requirements

The run writes `matt-pocock-skills-exam-report.md`: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs never
touch the prior report; written before any pruning). Then: one run row appended to
`matt-pocock-skills-log.md` (run-row format per `config-manager-reference.md`);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items expected** — the matt set is a deliberate-manual
  install; every repair/decision is developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the 5 Anvil skills in `~/.agents/skills/`
  (different owner) · the source clone (never pull/upgrade/reinstall — standing
  rule; only the developer's deliberate decision can change it) · sub-agent
  spawning in any form (execute inline per the reference's table) · any
  `npx skills` / plugin-path install, ever
- Credentials: variable names only, never printed