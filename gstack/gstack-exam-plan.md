---
title: "gstack-exam-plan"
doc-id: "mb-5870025e"
---
# GStack — Exam Plan

Transient job-spec for the next exam run. Synthesized by the config-manager before
each run from: [[gstack-config|GStack Configuration]] (spec), the last
[[gstack-exam-report|Exam Report]], [[gstack-log|Log]] (events since last
run), [[gstack-learnings|GStack Learnings]]. Consumed by the skill at run time;
rewritten at the start of the following cycle. The file is live; its contents are
transient.

**This first plan is hand-written** (emulation of the proven gbrain-dream-cycle
architecture): it also serves as the format template. The **standing check
inventory lives in the skill** ([[gstack-skill|Gstack Skill]], born-with-inventory); this
plan carries run-specifics and references. Once verified by a run, future plans
carry run-specifics + references only.

---

## 1. Run header

| Item | Value |
|---|---|
| Plan for run | #1 — first formal plan-driven run (no prior exam exists — bootstrap) |
| Run date | set at execution |
| Prior report | none — placeholder present; missing prior report = expected, not silence |
| Step-0 result | recorded at execution |
| Tier 3 unlock state | **Locked** — Tier 3 rows execute only if the developer unlocks this run |
| Developer-run requests this run (bundled into ONE request) | (a) `~/.gstack` file-content reads if any guard denies them (sensitive-data guards — proven classes); (b) any check whose command text the guards deny; (c) `.env.example` content verification (the one template line claim) |
| Expected-value source of truth | [[gstack-config|GStack Configuration]] — read fresh at run start; never rely on remembered values |
| Scope boundary | This module exams GStack itself: clone version/HEAD, discovery topology, config files, binary tree, integration facts. Sibling modules own: GBrain server/schema/conformance (`mb-config-gbrain`), dream-cycle pipeline (`mb-config-gbrain-dream-cycle`), OpenCode structure rows and Active Project Standard (`mb-config-opencode`), cross-tool skill enumeration ([[skills-register|Skill Register]], docs-managed). Skill-inventory re-audit is NOT performed here (docs governance owns [[skills-register|Skill Register]]). |
## 2. Carried-forward items

None — bootstrap (no prior exam exists). Recorded spec states kept under watch
(observations, not findings):

| # | Watch item (config open items) | This run's action |
|---|---|---|
| W-1 | Upgrade decision (major): upstream `v1.81.0.0` is Aside-browser-first; suite pins to installed `1.58.1.0` behavior | Verify installed version remains `1.58.1.0`/HEAD `c7ae632`; the upgrade is a developer re-decision, never a routine bump (GS0-1) |
| W-2 | Bare-name discovery links (2026-07-20) — earlier setup version unidentified | Observation only; provenance does not affect any rule (GS1-1) |
| W-3 | `last-update-check` artifact is stale (claims 1.61.0.0 latest; actual upstream is 1.81.0.0) | Verify artifact still reports the documented stale string (GS1-7); harmless |
| W-4 | 3 broken discovery entries (codex, connect-chrome, hackernews-frontpage → retired `/mnt/c/mybizz/skills/`) | Verify still inert/dead per spec; cleanup optional, no action taken (GS1-3) |

## 3. Erred last run

None — no prior exam exists (first formal run; bootstrap).

## 4. Log-driven items

| # | Event (log) | Check |
|---|---|---|
| LG-1 | 2026-07-20 bare-name links; 2026-09-02 prefixed links — two installer generations coexist | GS1-1 executes the discovery topology conformance check (both generations present, frontmatter decides command) |
| LG-2 | 2026-09-08 live verification recorded 54 invocable skills (superseding 52) | GS1-1 re-counts the per-host tree (54 expected) |
| LG-2 | No crashes/incidents logged since | If a new log row exists at synthesis time, derive a targeted probe from it |

## 5. Learnings-driven items

| # | Learning | Check |
|---|---|---|
| LE-1 | None yet — empty learnings file at bootstrap | Full suite build-out constitutes the initial learnings |

## 6. Standing checks — summary (the complete enumeration lives in the skill)

Every check: id, runner (A=agent, D=developer), probe, expected source, pass
rule — full tables in [[gstack-skill|Gstack Skill]] (Tiers 0–3). Summary:

- **Tier 0 (A) — invocability:** GS0-1 clone version `1.58.1.0` / HEAD `c7ae632` · GS0-2 discovery symlink tree exists at both link generations · GS0-3 aggregate `/gstack` entry + `GSTACK_BIN` resolve
- **Tier 1 (A/D) — state conformance:** GS1-1 per-host tree count 54 · GS1-2 74 binaries in `bin/` · GS1-3 3 broken entries dead/inert · GS1-4 `~/.gstack/config.yaml` live values · GS1-5 gbrain-detection.json + repo-policy.json agree with spec · GS1-6 GBrain worktree present, remote absent · GS1-7 `last-update-check` stale string · GS1-8 `.env` absent in clone (D on content) · GS1-9 slop-scan config + SKILL.md.tmpl generation source present · GS1-10 suite completeness (7 files + skill source)
- **Tier 2 (A) — functional, present ≠ working:** GS2-1 deterministic bin invocation: one `gstack-*.sh` script runs (read-only) · GS2-2 discipline probe: SKILL.md is generated (frontmatter `name` matches folder rule, not hand-edited) — verifies the regenerate-never-edit rule
- **Tier 3 (D, locked):** GS3-1 agent-visible invocation of a real GStack skill lifecycle (expensive/content-changing) · GS3-2 upgrade execution (developer decision; policy: only on check failure, never on newness)

## 7. Report requirements

The run writes [[gstack-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace; failed runs never
touch the prior report; written before any pruning). Then: one run row appended to
[[gstack-log|Log]] (run-row format per [[config-manager-reference|Reference: Commands, Procedures]]);
new learnings filed.

## 8. Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- Repairs are **allowlist-only**: anything outside the skill's allowlist = diagnosis + proposal, never an improvised fix
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the live clone's generated `SKILL.md` files (regenerate, never hand-edit) · `~/.gstack` credential-bearing content (sensitive-data guards; never read by the agent, never printed) · the dead duplicate Windows service / retired `/mnt/c/mybizz/skills/` folder (deletion, never touch) · the upgrade decision itself (developer-owned)
- Credentials: variable names only, never printed
