---
title: "gstack-learnings"
doc-id: "mb-560c62ee"
updated: "2026-10-20"
---
# GStack — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The clone carries two MyBizz-local commits on top of the upstream `1.58.1.0` base — Brain Context Load sections in skill sources plus `.gitignore` additions — unpushed. Any upstream upgrade must rebase them; the installed state is version plus local modifications, not pure upstream. | A pristine-upstream assumption would mis-describe every future upgrade of this system. | live `git log` / `git branch -v` |
| L2 | `question_tuning: true` opts MyBizz into gstack's per-question preference tuning; the issuer default is `false`. | Deliberate opt-in: gstack skills adapt their questions to the recorded developer preferences. | `/mnt/c/mybizz/gstack/plan-tune/SKILL.md.tmpl` |
| L3 | `artifacts_sync_mode: full` syncs all allowlisted working state into the local git-backed brain worktree; the issuer default is `off`. | Deliberate opt-in: plans, designs, retros and learnings persist in the brain worktree for later skills to find. | `/mnt/c/mybizz/gstack/docs/gbrain-sync.md` |
