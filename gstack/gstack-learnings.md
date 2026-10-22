---
title: "gstack-learnings"
doc-id: "mb-560c62ee"
updated: "2026-10-22"
---
# GStack — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why.
Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The clone carries one MyBizz-local commit (`d8775cc20`: two `.gitignore` entries — `docs/gbrain-credentials.md`, `test-results/`) on upstream `c580561` (`1.91.164.0`), branch `mybizz-c580561`; earlier MyBizz-local commits are not carried — the installed version generates the Brain Context Load sections itself. Any upgrade must rebase the local commit. | A pristine-upstream assumption would mis-describe every future upgrade of this system; the `.gitignore` entries keep local credential notes and test results out of the repo. | live `git log`, verified 2026-10-22 |
| L2 | `question_tuning: true` opts MyBizz into gstack's per-question preference tuning; the issuer default is `false`. | Deliberate opt-in: gstack skills adapt their questions to the recorded developer preferences. | `/mnt/c/mybizz/gstack/plan-tune/SKILL.md.tmpl` |
| L3 | `artifacts_sync_mode: full` syncs all allowlisted working state into the local git-backed brain worktree; the issuer default is `off`. | Deliberate opt-in: plans, designs, retros and learnings persist in the brain worktree for later skills to find. | `/mnt/c/mybizz/gstack/docs/gbrain-sync.md` |
| L4 | Bun is 1.3.14; GStack is tested on 1.4.2 (setup warning). Not upgraded, by developer decision; setup and build completed on 1.3.14. | The developer keeps the runtime unchanged on a low-resource PC; the warning is informational and the install is functional. | setup output, developer-verified 2026-10-22 |
| L5 | Docker is not installed, by developer decision (low PC resources); `/cso` runs its static audit; the qualified CSO reproduction images are unavailable. Podman is the preferred container tool if one is ever added. | The static audit covers daily use; the developer chose the trade-off knowingly. | developer-verified 2026-10-22 |
| L6 | GStack is pinned for PDLF at upstream `c580561` (`1.91.164.0`); never upgraded without the developer's decision. | PDLF scoped its phases against this source; an upgrade would change skill behaviour mid-pipeline. | developer decision, 2026-10-22 |
