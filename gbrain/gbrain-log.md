---
document: "GBrain — Log"
doc-id: gbrain-log
state: Live
date-created: 2026-09-13
---

# GBrain — Log

Chronological record of notable events for this system: exam runs and outcomes,
crashes, failure incidents, upgrades, error reports, significant guard denials.
Events, not lessons — lessons live in [[gbrain-learnings|Learnings]]. Pruned under the
absorption rule. (Seeded with development-period events so the system has working
data.)

| date | event | outcome / disposition |
|---|---|---|
| 2026-07-28 → 2026-09-06 | Sync path established and exercised: 18 logged runs across all sources (`sync-gbrain.sh` + per-source syncs) | Dominant content path |
| 2026-09-05/06 | All 13 sources synced; the old "deferred sources" framing retired | Sources real and recent |
| 2026-09-06 | Doubly-inert cron entry (`gbrain autopilot`, every 5 min, dead target) found and **deliberately removed** | Design consequence: Dream Cycle on-demand only; nothing gbrain-related scheduled |
| 2026-09-06 | Suite verified comprehensively (stats, sources, MCP entry, credentials posture) | Spec written at that state |
| 2026-09-11 | New source registered: `pdlf` ("PDLF System", federated, 59 pages) — consistent with the pdlf project going live same day | Spec not yet refreshed (drift flag) |
| 2026-09-12 | Pilot exam run (detection-only, pre-architecture): engine green, schema pack exact, MCP entry exact, zero sync failures; 5 findings — 4 doc-drift flags (14th source, stale counts incl. a large drop needing explanation, `brain.pglite` gone, bundle evolved) + 1 execution boundary (config.json reads guard-blocked → developer-run class) | Verdict: HEALTHY; flags carried |
| 2026-09-12 | Skill installed by move to `~/.config/opencode/skills/mb-config-gbrain/` (no guard block) | Register flipped → Installed |
| 2026-09-13 | Copy-install model adopted repo-wide: skill source backfilled to suite folder, hash recorded; architecture upgraded (credential-discipline + artifact-recording amendments) | Hash bb269e9944b03418 in register |
| 2026-09-13 | Commits pushed + sync+embed runs: brain grew to 1,878 → 1,880 pages, 100% coverage maintained | Count drift at sync confirmed as design behavior |
| 2026-09-13 | Config-management architecture emulated onto this suite: exam-plan created (ID'd checks G0-1…G3-4), log created (this file), learnings filed | Suite at the 7-file standard; first formal plan-driven run pending |
| 2026-09-13 | Backup scope expanded estate-wide (developer decision): both gbrain + memory_governor DBs included in a 5-database weekly cycle covering both instances; gbrain-config.md Backups section now points to the authoritative estate convention in postgresql-config.md | Full DB estate backed up + hash-verified in both locations |
| 2026-09-13 | Run #1 — first formal plan-driven exam (step-0 PASS; Tiers 0–2 agent-runnable complete) | Verdict: HEALTHY — identity green (1,880/5,581, 100% coverage), schema pack exact, 14/14 source paths, zero sync failures, no cron; **273-page accounting question RESOLVED** (per-source attribution sums exactly — pilot gap was snapshot lag); guard reclassified opencode.jsonc reads → developer bundle; 4 spec-drift flags re-confirmed pending governance; check inventory graduated into skill |
| 2026-09-13 | Tier-3 partial + governance closed: G3-1 developer-verified (masked jq — `self_upgrade_mode` key ABSENT, `mcp_surface` absent re-confirmed, 10 keys); G2-3 MCP entry developer-verified exact; **gbrain-config.md refresh approved + applied** (14-source table w/ pdlf + current counts, stats 1,880/5,581 point-in-time, pglite removed, bundle row 65-entry, self-upgrade key-absent, verification date → 2026-09-13) | Spec now matches live reality; 2 learnings graduated (point-in-time note + bundle row); 1 remains (bundle-evolution standing rule, destination applied); skill graduated + synced (58dc0b52cbc86d72) |
| 2026-09-13 | Source-clone open item RESOLVED: `/mnt/c/mybizz/gbrain` (v0.25.0) deleted per developer decision — verified not implemented (live code is bun-global install; zero references) with only trivial local debris; upstream public, re-clonable. Deletion command developer-run (agent rm guard-blocked, honored). Upgrade advisory recorded: 0.50.0.0 requires coordinated cutover + DB backup first (none exists — gap noted) | Spec updated (install row, open items 1+3) |
| 2026-09-13 | **First full gbrain DB backup taken** (`pg_dump -Fc`): 51,429,231 bytes, 62 table-data entries verified via `pg_restore --list`; delivered to BOTH locations per developer instruction — default `/home/dev-p/backup-gbrain/` + security-net `/mnt/c/backup-gbrain/` (C:\backup-gbrain); copies hash-identical (6a6d60d57df162a4). Backup convention recorded in spec; the "no fresh backup" gap in open item 1 closed. Note: covers `gbrain` DB only — `memory_governor` DB not covered (add on developer decision) | The largest unmitigated risk in the system is now mitigated |
