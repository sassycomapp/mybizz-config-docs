---
document: "mb-doccycle Configuration"
doc-id: doccycle-config
state: Live
date-created: 2026-09-22
---

# mb-doccycle Configuration

Canonical current-state configuration record for the mb-doccycle
documentation-management workflow. Agent-facing. This document states
facts, not history — where a decision was made and the reasoning matters,
see [[doccycle-explainer|The mb-doccycle Documentation-Management Workflow]];
for operational commands and procedures, see
[[doccycle-reference|mb-doccycle Usage and Invocation]]; for the binding
shared run frame, see
[[doccycle-run-discipline|mb-doccycle — Shared Run Discipline]].

---

## Current operational status — INSTALLED, acceptance test pending

The workflow skill is authored, approved, installed, and hash-verified;
the canonical Phase-C tool is tested; the Cupcake coexistence amendments
are live-verified; the three superseded skills and their suite folders
are removed with registers updated (WP7). The acceptance test (WP8) —
one controlled corpus cycle with slips, a granted commit, per-source sync
evidence, and a dream-cycle run — remains before doccycle is judged
operational. The config-management build-out (doccycle-skill.md, exam
plan/report, log, learnings) runs as its own developer-driven engagement
after WP7, per config-manager-agent.md via config-setup-prompt.md.

## Identity

| Item | Value |
|---|---|
| Name | `mb-doccycle` (approved 2026-09-21) |
| Source home | `C:\mybizz\mb-doccycle\` — git-backed, github.com/sassycomapp/mb-doccycle |
| Source status | WP0–WP4 committed (initial 799c528; tool+tests 7cd6dd6; run frame doc + phases + SKILL.md pending commit at WP5) |
| Shared run frame | `C:\mybizz\mybizz-config-docs\mb-doccycle\doccycle-run-discipline.md` (live) |
| Suite home | `C:\mybizz\mybizz-config-docs\mb-doccycle\` (this file, reference, explainer, run frame) |
| Logs / records home | `C:\mybizz\logs\mb-doccycle\` — run-index.md, learnings\, in-progress\, last-completed-run\, abandoned-runs\ |
| Backup root | `C:\backup-mb-doccycle\` |
| Architecture decisions | G1–G7 resolved 2026-09-21 in the Docs-Skills Architecture Proposal (desktop, data-mybizz-mgt) |

## Component inventory

| Component | State |
|---|---|
| `SKILL.md` (workflow skill) | Authored WP4 2026-09-22, developer-approved. Governance header in its first lines; charter; invocation grammar `(all)` / `(corpus)` / `(phase corpus)` / `(closeout)` |
| `phases/A-structure.md` | Authored WP4, approved. Absorbs the retired mb-docs-manager (pinned/discovered document sets, structural code-repo rule, depth model, count-verified backup doctrine, never-delete, NTFS ls-files staging, PUSH_FAILED handling) |
| `phases/B-consistency.md` | Authored WP4, approved. Absorbs the retired mb-align-docs (two distinct operations, fixed option sets, front-matter identity rules, corrected directionality, quarantine purpose, missing-document investigation, PENDING-BUILD and treatment classes, F-MK3 nuance) |
| `phases/C-conversion.md` | Authored WP4, approved. Absorbs the retired mb-wikilinks (canonical-tool detection, corpus-wide universe, collision census, class-to-treatment mapping, pre-approval GBrain target verification) |
| `tool/doccycle-detect.py` v0.1.0 | Canonical Phase-C detector (WP2). Read-only; byte-preserving, line-precise, unique-context, backtick-first, check=True; refuses an empty universe. Developer-reviewed; committed 7cd6dd6 |
| `tests/` — 27 unittests | 27/27 PASS, including read-only contract and check=True contract tests; 19 defect-family fixtures + fixture universe |
| Installed copy | **Installed 2026-09-22 (WP7):** `~/.config/opencode/skills/mb-doccycle/` carries SKILL.md + `phases\`; source/install hash pair identical (md5 `a8336c843c79c900cf98afe0c54c2f69`); phases installed alongside SKILL.md as the skill's runtime dependency |
| Old skills (mb-docs-manager, mb-align-docs, mb-wikilinks) | **REMOVED 2026-09-22 (WP7, developer-confirmed):** installed folders deleted, config-docs suite folders deleted (9 register rows retired; 39-file verified backup at `C:\backup-mb-doccycle\wp7-retirement-20260922T183427`). Stale cross-references healed; the scope scaffold's skill-name list is a developer-owned flag, never edited by the workflow. Logs and records under `C:\mybizz\logs\` remain as historical archives |

## Enforcement integration (Cupcake, live as of 2026-09-22)

| Item | Value |
|---|---|
| Path slips | `mg-grant --path <folder> --count N` — developer-terminal only |
| Commit allowances | `git-grant --repo <folder> --count N --minutes M` (WP3, decision G1) — live-verified 2026-09-22; publishes/deploys carry no allowance channel |
| Governing rules | `no_autonomous_commits…` (allowance channel), `no_cross_project_filesystem_access_by_default` (shared-library list + slips), `no_bash_mediated_file_writes_without_grant` (same boundary, shell shapes) |
| Boot mode | Set-and-forget: skeleton-less folders evaluate global policies via `~/.config/cupcake/fallback`; `failMode: open` is the environment default. Raw `cupcake eval` launches from the fallback home |
| Suite docs for Cupcake | `C:\mybizz\mybizz-config-docs\cupcake\` (its own suite) |

## Records

| Item | Location |
|---|---|
| Run working record | `C:\mybizz\logs\mb-doccycle\in-progress\<run-timestamp>.md` — created at run start, appended at every decision point, minimum four appends per run |
| Completed records | `last-completed-run\` (moved at close; never deleted); declined-resume runs to `abandoned-runs\` |
| Permanent index | `C:\mybizz\logs\mb-doccycle\run-index.md` — one row per run: run-id, date, target, findings, decisions, commits |
| Learnings | `C:\mybizz\logs\mb-doccycle\learnings\` — seeded at WP6 with the still-valid items from the three retired skills' folders |
| Backups | `C:\backup-mb-doccycle\<run-timestamp>\`, sized to the phase's write surface, count-verified |
| Alignment log | Per-corpus, option B (G5): approved-and-applied entries only; the complete decision record lives in the run working record and index row |

## Open items

| # | Item | Status |
|---|---|---|
| 1 | WP5 gate — developer review of the three suite documents | CLOSED 2026-09-22 (approved) |
| 2 | WP6 learnings sweep | CLOSED 2026-09-22 — 45 files classified (38 carried into 3 seed files, 4 superseded in place with marks, 2 carried with superseded clauses struck); old run logs remain untouched as historical archives |
| 3 | WP7 install + retirement — **developer-extended scope 2026-09-22:** after install, the three old skills are completely removed INCLUDING their mybizz-config-docs suite folders, with all registers updated | Pending; developer confirms execution timing |
| 4 | WP8 acceptance test (controlled corpus cycle with slips, granted commit, per-source sync evidence, counter check or honest absence, dream-cycle run) | Pending |
| 5 | Config-management build-out (doccycle-skill.md, exam plan/report, log, learnings) | Own engagement after WP7, developer-driven |