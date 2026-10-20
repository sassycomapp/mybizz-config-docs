---
title: "opencode-learnings"
doc-id: "mb-cecab1e4"
updated: "2026-10-20"
---
# OpenCode — Learnings

What differs from, or adds to, the standard in the MyBizz setup, and why. Read in full before any research, examination or proposal for this system.

| ID | Learning | Why it holds | Source |
|---|---|---|---|
| L1 | OpenCode runs the current major version line (1.19.0); the successor line does not run the Cupcake plugin, so version upgrades are gated on Cupcake compatibility. | The policy layer is load-bearing; a harness version that drops it is not adoptable. | Developer-approved finding; [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) |
| L2 | Skill discovery scans `~/.config/opencode/skills` and `~/.agents/skills`; `~/.config/skills` is a second name for the first, being a link to it. A skill discovered through more than one root logs a `duplicate skill name` warning; the `i-have-adhd` warning is harmless, because both of its entries resolve to one file. | Multi-root scanning makes exactly-one-path hygiene apply to skills as well as plugins; the warning is the tell, and it is not an error. | OpenCode log; live directory listings |
| L3 | The session database carries its `workspace` table in the 1.19.0 layout and keeps the version-2 layout under the name `workspace_v2_layout`; full-database backups are taken before any repair. | Version-2 leftovers break version 1; backup-first is the recovery pattern. | Developer-approved finding; `C:\backup-wsl\opencode-db-repair\` |
| L4 | Per-project configuration follows repo role: each app repo carries the full baseline; `mb-3-cs-project-library` carries a minimal config (`plan` default, no theme rows, no MCP entry); the newer project-libraries and `pdlf` carry none. | The deviations are deliberate, not drift; a new app repo receives the full baseline at creation. | Live reads of every project config; [[[mybizz-os-docs:os-reference-docs/repo-organization\|Repo Organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) |
| L5 | The web UI reopens the last active project regardless of start folder; its project box searches `/home/dev-p` only; "Recent projects" is remembered by the browser and can list folders that no longer exist — clearing the browser's site data for `localhost:4096` resets it. | Prevents misreading UI state as session-database corruption. | Developer-approved finding |
| L6 | `opencode debug config` opens the folder it runs from as a project and calls no AI model. | It is both the merged-config inspector and a project-registration act; run it from project roots only. | Developer-approved finding |
| L7 | The plugin folder loads only `.js` files; the `plugin` config list accepts folder paths, and a file path in it is rejected. The MyBizz setup carries no `plugin` list entry and relies on folder auto-loading. | Prevents re-introducing a rejected `plugin` entry or a file the loader ignores. | Developer-stated correction; live global config |
| L8 | This OpenCode version writes no plugin-load log lines; plugin checks are made inside OpenCode. | Prevents building verification on log lines that do not exist. | Developer-stated correction |
