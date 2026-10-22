---
title: "anvil-cli-learnings"
doc-id: "mb-f4847222"
updated: "2026-10-22"
---

# anvil-cli — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read
in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | The CLI is pinned at 0.7.7, the current stable latest; the 0.8.0 pre-releases are not installed. | Developer decision; the pre-releases' notable addition (`db apply-schema`) is hosted-agent-only and self-described destructive. | npm dist-tags, verified 2026-10-22 |
| L2 | `anvil watch` is not used anywhere in PDLF's pull-to-local procedure. | It is beta, its handling of conflicting edits is undocumented, and it would push an agent's local edits straight to App 1 without the developer's push. The decision is recorded in the step file. | c18-build-plan.md |
| L3 | `anvil db apply-schema --force` (anvil-yaml skill step 5) is never run in MyBizz. | Absent from 0.7.7; exists only in the 0.8.0 pre-releases under `ANVIL_AGENT_HOST=1` (Anvil's hosted agent) and can delete tables, columns or data. A schema change reaches the live app only when the developer applies it in Anvil's Data Tables view. | npm dist-tags, verified 2026-10-22; pol-anvil-platform.md; c17-build-plan.md |
| L4 | `anvil` is on the PATH of login shells only. | The installer appends its paths to the shell profiles; agent tool shells are non-login, so invoke through a login shell or the full binary path. | `~/.bashrc` line 147; `~/.profile` line 29 (live) |
| L5 | The issuer's CLI docs pages describe a surface ahead of the installed stable: `create` and `checkout --git-url` exist only in the docs, while 0.7.7 also has `config delete`, `deps`, `tables`, `convert-template` and `git-auth` that the pages do not document. | The pages are unversioned and track the newest surface; the installed binary defines behaviour. | docs pages versus `anvil --help` and installed source, both verified 2026-10-22 |
