---
document: "anvil-agent-references — Log"
doc-id: anvil-agent-references-log
state: Live
date-created: 2026-09-06
---

# anvil-agent-references — Log

Chronological record of notable events for this system: exam runs and outcomes,
crashes, failure incidents, upgrades, error reports, significant guard denials.
Events, not lessons — lessons live in `anvil-agent-learnings.md`. Pruned under
the absorption rule. (Seeded with development-period events so the system has
working data; content beyond eventness is not the point.)

| date | event | outcome / disposition |
|---|---|---|
| 2026-08-12 | Initial install: five symlinks created in `~/.agents/skills/` (`anvil-yaml`, `client-forms`, `client-modules`, `data-models`, `server-code`) → the clone's `skills/` folders. Nothing copied — symlink-only install (config §Install architecture) | Installed; symlink topology in place |
| 2026-09-06 | Suite created: `config.md`, `reference.md`, `explainer.md`; values verified live. GBrain source `anvil-agent-references-code` registered via host CLI `gbrain sources add` (MCP path registration security-confined and refused); non-federated. OpenCode discovery confirmed working (all five skills in the catalog); duplicate discovery paths none | Suite live; gbrain source registered (0 pages at that time); drift recorded: installed HEAD `3593c16`, upstream `7c9b0a7` (update pending, open item 1) |
| 2026-09-16 | Suite build-out: exam-plan, log (this file), learnings, exam-report placeholder created; explainer localized with config-maintenance + S.W.O.T.; reference gained the config-management set pointers; skill written born-with-inventory (`anvil-agent-skill.md`) | Suite at the 7-file standard + skill source; formal run #1 pending |
| 2026-09-16 | Upstream update observed at build-out orientation: clone HEAD now `7c9b0a7` — the previously-recorded *upstream* HEAD (spec open item 1). Stub count 63 (31 client + 32 server) vs spec-recorded 62. GBrain source shows 34 pages, last sync 2026-09-06 — spec records "0 pages, never synced" (open item 5). Developer-run `git pull` evidently executed since 2026-09-06 | State change vs spec recorded; disposition to be classified in run #1 (DIRFT/GAP classes) and carried to the gate |
| 2026-09-16 | **Run #1 formal — verdict: HEALTHY (Tiers 0–2 all PASS, zero live defects).** Step-0 PASS (11/11 hash pairs, glob form); Tier 0: clone at upstream HEAD `7c9b0a7` @ master, discovery root returns all 5 vendor Anvil skills; Tier 1: 40 symlinks (5 anvil + 35 matt), 0 broken, discovery discipline clean, structure conforms (server stubs 32 vs recorded 31 — delta), per-project setup Done/Done/Not/Not/Not, suite complete, gbrain source registered (34 pages vs recorded 0 — delta), stale refs absent; Tier 2: frontmatter sweep **5/5**, shared-resource block 5 roles present. Two guard denials honored (exec-protection token-literal; command-scope write-boundary misread). **Two spec-staleness observations flagged: W-1** (clone moved to upstream `7c9b0a7`; stub count 63) **and W-5** (gbrain source indexed 34 pages) — both DRIFT-class spec-refresh flags carried to the gate. **Tier 3 Locked** — unlock asked at gate (AR3-1/AR3-2/AR3-3) | Run closed; verdict HEALTHY; W-1/W-5 await gate disposition; zero open findings in live state |
| 2026-09-16 | **Gate dispositions (run #1) — all approved:** W-1 **flagged to docs governance** (spec §Identity + §Repository-structure refresh; open item 1 closure) — spec edit left to docs governance, no live mismatch; W-5 **flagged to docs governance** (spec §GBrain registration index-state refresh; open item 5 closure) — spec edit left to docs governance; **Tier 3 unlocked** and executed. **Tier 3 results:** AR3-1 full mechanical audit **PASS** — 5/5 links resolve exact, 5/5 SKILL.md byte-identity vs vendor, structure counts conform (server stubs 32, delta as W-1), plugin metadata exact; AR3-2 **stay-current with upstream** (clone already at `7c9b0a7`), license **no action** (open item 2 unchanged); AR3-3 per-project setup for the 3 Not-done roots remains **developer-run pending** (open item 3 carries) | Run #1 fully closed 2026-09-16: verdict HEALTHY, zero open findings in live state; W-1/W-5 governance flags filed for docs-governance pickup; open items 2/3/4 unchanged |

(Events beyond build-out seed: appended at observation time / run rows per run.)