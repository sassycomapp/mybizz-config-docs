---
document: "mb-doccycle — Log"
doc-id: doccycle-log
state: Live
date-created: 2026-09-22
---

# mb-doccycle — Log

Chronological record of notable events for this system: exam runs and
outcomes, crashes, failure incidents, upgrades, error reports, significant
guard denials. Events, not lessons — lessons live in
[[doccycle-learnings|Learnings]]. Seeded with development-period events so
the system has working data.

| date | event | outcome / disposition |
|---|---|---|
| 2026-09-21 | Source home created (`C:\mybizz\mb-doccycle\`, github.com/sassycomapp/mb-doccycle, initial commit 799c528); logs home + backup root scaffolded per the architecture proposal | Operational |
| 2026-09-22 | Shared run frame live (`doccycle-run-discipline.md`, suite home); old run frame retired in place (WP1) | Live |
| 2026-09-22 | WP2: canonical Phase-C detector authored with 19 defect-family fixtures and a 27-test suite (27/27 PASS); committed 7cd6dd6 | Tested, developer-reviewed |
| 2026-09-22 | WP3: commit-allowance channel (G1) + cross-project list amendments (G2) authored, compiled, offline fidelity 11/11; live-verified developer-terminal (commit-allow → allow; publish → deny; restricted write → deny; logs → allow); two real defects caught pre-live (git -C regex gap; granted-cwd masking) | Live-verified; 24985a3 |
| 2026-09-22 | WP4: workflow skill + three phase specs authored and approved (re-authoring absorbing the three retired skills); committed fd9b22e | Developer-approved |
| 2026-09-22 | WP6: learnings sweep — 45 files classified, 38 carried into 3 seed files, 4 superseded in place; archives untouched | Closed |
| 2026-09-22 | WP7: skill installed (SKILL.md + phases, hash pair `a8336c843c79c900cf98afe0c54c2f69`); the three superseded skills + their config-docs suites removed (39/39 backup at `C:\backup-mb-doccycle\wp7-retirement-20260922T183427`); registers updated; stale references healed; git-clean preflight added to the run frame | Retired + installed; 537cfce, 8c8bfa8 |
| 2026-09-22 | WP8 acceptance run 20260922T185208+0200 on data-mybizz-mgt: 2 Phase-A heals + 6/6 Phase-C conversions applied and diff-verified; commit 190dc59 (developer-terminal after the expired-allowance deny honored); per-source sync LAG 0s; dream cycle completed; both doctor counter checks ran | CLOSED — record in last-completed-run; index row appended |
| 2026-09-22 | Two detector defects found by the WP8 run (empty display on folder-shaped tokens; folder tokens entering suffix matching; universe build lacking scaffold-exception filtering) | Queued — rule-pipeline correction to the git-backed tool (carried-forward watch item CY3-2) |
| 2026-09-22 | **Config suite build-out + run #1 formal (2026-09-22):** 8-file suite completed per config-setup-prompt (learnings, log, exam-plan, exam-report, explainer/reference localization, exam-skill source); skill copy-installed to `~/.config/opencode/skills/mb-config-doccycle/` (hash pair `ca8546f10dd6859a`); register WIP → Installed. Run #1: HEALTHY — Tiers 0–2 all PASS, zero DOWN/UNHEALTHY/DRIFT | **Gate dispositions (developer, "apply all recommendations"):** F-1 approved — `.gitignore` added; CY3-2 executed and verified in-run — tool v0.1.1 (SKIP-FOLDER-REF class + display_default separator fix), 29/29 PASS; CY3-1 deferred to the next scheduled corpus cycle; LE-1 graduated into the reference (learning entry deleted) |