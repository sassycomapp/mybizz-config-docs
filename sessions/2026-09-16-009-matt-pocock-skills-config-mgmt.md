---
title: "2026-09-16-009-matt-pocock-skills-config-mgmt"
doc-id: "2026-09-16-009-matt-pocock-skills-config-mgmt"
---
# Session 009 — matt-pocock-skills configuration-management suite: built, installed, run #1 HEALTHY

## What was done (with evidence)

1. **Suite build-out (Phase 1).** Built the matt-pocock-skills configuration-management suite to the 7-file standard + skill source in `mybizz-config-docs/matt-pocock-skills/`: [[matt-pocock-skills-exam-plan|Exam Plan]] (hand-written bootstrap 1-8 format template), [[matt-pocock-skills-exam-report|Exam Report]] (placeholder then write-then-replace run #1), [[matt-pocock-skills-log|Log]] (seeded: 2026-08-12 install, 2026-09-08 supersession, 2026-09-16 build-out), [[matt-pocock-skills-learnings|Learnings]] (preamble + empty table), [[matt-pocock-skills-skill|Matt Pocock Skills Skill]] (born-with-inventory, `mb-config-matt-pocock-skills`, Tiers 0-3, scope boundary vs anvil-agent-references / gstack / cupcake), localized [[matt-pocock-skills-explainer|Matt Pocock Skills Explainer]] (config maintenance + SWOT + companion footer) and [[matt-pocock-skills-reference|Matt Pocock Skills Reference]] (config-management set pointers in header).

2. **Install (Phase 2).** `mg-grant --path ~/.config/opencode/skills/mb-config-matt-pocock-skills --count 3` (developer-executed, granted). Copy-installed (copy, never move) to `~/.config/opencode/skills/mb-config-matt-pocock-skills/SKILL.md`; hash pair verified (`86c78969ad0e8a80`, source = installed identical). Register row flipped WIP to Installed.

3. **Formal run #1 (Phase 3).** Step-0 self-validation PASS: 10/10 hash pairs via the approved glob form; suite completeness 10/10 at the 8-file standard; register spec-doc paths all resolve; bootstrap (no open run block). Tiers 0-2 all PASS: clone pinned `84fdeff`; discovery root 35/40 links; 40 symlinks (35 matt + 5 anvil targets), 0 broken; 0 copied dirs; setup gate 1 Yes / 4 No; inventory 18/7/6/4 exact; no cross-target links; Zone.Identifier 25 B recorded; suite complete; frontmatter sweep 35/35; code-review / wayfinder / ask-matt resolve. Verdict: HEALTHY - zero live defects, zero open findings.

4. **Tier 3 executed (gate-unlocked).** MP3-1 full mechanical integrity audit PASS - 40 links by origin (35 matt / 5 anvil / 0 other), 0 broken, category counts 18/7/6/4, 0/35 SKILL.md byte mismatches vs source. MP3-2 deliberate upgrade decision: stay pinned `84fdeff` (no check failed - never on newness). MP3-3 Zone.Identifier artifact decision: keep (25 B, inert, recorded open item).

5. **Guard denials honored (1).** Step-0 token-literal sibling-name list text (exec-protection, token-in-argument class) - re-issued in the approved derived-glob form. No denial retried through an alternate path.

6. **Commit + push + sync.** Developer committed and pushed `fd8cb38` (suite + register + config-manager log). Agent ran `setsid bash /mnt/c/mybizz/scripts/sync-gbrain.sh` - completed: synced `2aa9a9d0..fd8cb389`, 33 chunks created, 10 pages embedded, 0 stale.

7. **Close-out (this session).** Session page written; candidate durable facts checked against GBrain (genuine contradiction check, multiple queries) and presented once for the single approval gate.

## Standards set this session

- matt-pocock-skills is **not** a memory-family member - it is a skills installation; no master-explainer involvement (mirrors the GStack exclusion precedent, session 008).
- Stay-pinned philosophy reaffirmed for this set: never on newness, only on check failure. The set drifts behind upstream (~1 month) by deliberate design.
- Zone.Identifier inert artifacts across suites are a known environmental remnant, not defects.

## Quirks and dispositions

- The 5 Anvil skills sharing `~/.agents/skills/` are a different owner (anvil-agent-references) - coexistence presence only, never touched, never inventoried (scope boundary in the skill).
- Upstream divergence (`84fdeff` vs upstream ~1 month newer, incl. PR #1025 "stop linking misc/") is a recorded open item for any future deliberate upgrade decision - none planned.

## Artifacts

- Register: matt-pocock-skills Installed, hash `86c78969ad0e8a80`, verified live 2026-09-16.
- Suite: `mybizz-config-docs/matt-pocock-skills/` - 8 standard files + skill source; skill installed at `~/.config/opencode/skills/mb-config-matt-pocock-skills/SKILL.md`.
- Commit: `fd8cb38` (10 files, +435/-11), pushed to GitHub.

## Open / next

- Zero open items for matt-pocock-skills.
- Emulation queue's remaining WIP targets: `anvil-agent-references`, `magdoub-wireframe` (`config-setup-prompt.md` is the entry point).
