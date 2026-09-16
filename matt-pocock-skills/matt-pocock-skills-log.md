---
document: "Matt Pocock Skills — Log"
doc-id: matt-pocock-skills-log
state: Live
date-created: 2026-09-08
---

# Matt Pocock Skills — Log

Chronological record of notable events for this system: exam runs and outcomes,
crashes, failure incidents, upgrades, error reports, significant guard denials.
Events, not lessons — lessons live in `matt-pocock-skills-learnings.md`. Pruned
under the absorption rule. (Seeded with development-period events so the system
has working data; content beyond eventness is not the point.)

| date | event | outcome / disposition |
|---|---|---|
| 2026-08-12 | Initial install: 35 matt-pocock skill symlinks created in `~/.agents/skills/` → source clone's `skills/<category>/<name>/` (manual pinned clone — nothing copied, no vendor plugin/`npx` paths) | Installed; symlink topology in place |
| 2026-09-08 | Suite created: `config.md`, `reference.md`, `explainer.md`; values verified live. Supersession executed: prior `mybizz-os-docs/matt-pocock-skills-reference.md` **removed**, verified content merged into this suite (developer decision). Stale claims retired with it (`C:\mybizz\skills-collective\matt-pocock-skills` browsable-hub path does not exist); `~/.agents/skills/matt-pocock-skills-reference.md:Zone.Identifier` (25 B) inert artifact noted, cleanup optional — no action taken | Suite live; single canonical home established. Upgrade standing rule effective (2026-09-08): updates/upgrades by deliberate decision only |
| 2026-09-16 | Suite build-out: exam-plan, log (this file), learnings, exam-report placeholder created; explainer localized with config-maintenance + S.W.O.T.; reference gained the config-management set pointers; skill written born-with-inventory (`matt-pocock-skills-skill.md`) | Suite at the 7-file standard + skill source; formal run #1 pending |
| 2026-09-16 | **Run #1 formal — verdict: HEALTHY (all PASS, zero live defects).** Step-0 PASS (10/10 hash pairs, glob form); Tier 0: clone pinned `84fdeff`, root returns 35/40 links; Tier 1: 40 symlinks (35 matt + 5 anvil), 0 broken, 0 copied dirs, Zone.Identifier 25 B recorded, setup gate 1 Yes / 4 No, inventory 18/7/6/4 exact, no cross-target links, suite complete; Tier 2: frontmatter sweep **35/35**, three specialized skills resolve. One step-0 guard denial (token-literal sibling-name list — exec-protection class, recorded) honored. **Tier 3 executed (developer-unlocked):** MP3-1 full mechanical audit PASS — 40 links by origin (35 matt / 5 anvil / 0 other), 0 broken, 0/35 SKILL.md byte mismatches, counts exact; MP3-2 **stay pinned `84fdeff`** (no check failed — never on newness); MP3-3 Zone.Identifier **keep** (inert, optional, recorded) | Run closed; zero open findings; Tier 3 executed fully; all dispositions recorded |