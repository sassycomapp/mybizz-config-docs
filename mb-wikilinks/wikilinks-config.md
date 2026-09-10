---
document: "wikilinks — Config"
doc-id: wikilinks-config
state: Live
date-created: 2026-09-10
---

# wikilinks — Config

State of the `mb-wikilinks` skill as of 2026-09-10. All facts verified live
this date unless noted.

## Identity

| Field | Value |
|---|---|
| Component | `mb-wikilinks` — first-party custom OpenCode skill (developer-built) |
| Role | Cross-reference conversion — turns backtick paths, inline prose references, and Related Documents tables into GBrain-resolvable `[[wikilink]]` syntax |
| Invocation | `/mb-wikilinks (all)` — wide sweep, sequential per-leaf-folder cycles; `/mb-wikilinks (leaf-folder-name)` — one leaf folder (quote names with spaces: `("Agent readiness")`); empty/omitted target → the skill ASKS, never assumes |
| Version | No version field in frontmatter; V2 content amendments applied 2026-09-10 (grammar, wide mode, Anvil denial, renamed paths) |
| Language | Natural-language procedure; no executable code, no sub-agents — one continuous run per leaf folder |

## File inventory

| Location | Files |
|---|---|
| This folder (canonical suite) | `wikilinks-config.md`, `wikilinks-reference.md`, `wikilinks-explainer.md` |
| Installed skill — `~/.config/opencode/skills/mb-wikilinks/` | `SKILL.md` (347 ln, post-V2-amendments) |
| Repo mirror | none — this suite is the indexed artifact |

## Scope

| Element | Value |
|---|---|
| Locked sources (in order) | 1. `project-library-global` (`/mnt/c/dev/project-library-global`) 2. `dev-root` (`/mnt/c/dev/dev-root`) 3. `dev-makepdlf` — content ONLY in `makepdlf-project-library`; the `makepdlf` sibling is a ceremonial placeholder, never scanned |
| Scope ∩ scaffold | Locked scope intersected with the scope scaffold (`mybizz-scope-list.md`) — out-of-scope paths stay out in every mode |
| Explicitly excluded sources | `mb-3-cs` (code + project-library), `mb4ecom` (placeholder), `mb5pdlf` (disposable test project), `project-template` (wikilinks belong to real projects at init), `C:\pdlf` (outside path boundary) |
| Anvil code repos | **Denied entirely** — never opened/read/backed-up/edited, including `theme\assets\docs` inside them (Anvil app assets; Anvil owns their interpretation) |
| Blanket folder exclusions | `obsolete`, `archive`, `*backup*`, `templates-global`, `quarantine`/`Quarantine`, `register-global`/`register-local` (align-docs territory), `pdlf-temp`, `workspace`, `.gstack`/`.opencode`/`.scratch`/`.out-of-scope`, `Frontmatter-prompts` |
| Scope-extension rule | Asked to extend scope to an excluded source → stop and confirm explicitly; "keep going" is never authorization |

## Technical requirements (Section 1 prerequisites)

| Requirement | Value |
|---|---|
| Wikilink resolver | `link_resolution.global_basename` must be `true` (checked/set via `gbrain config`) |
| Target format | `[[basename\|Display Text]]` — bare filename stem, NO folder prefix, NO extension (directory-qualified wikilinks never resolve in this corpus — folder names are not in GBrain's `DIR_PATTERN`) |
| Basename collisions | Checked per source (`find … basename \| sort \| uniq -c`); any basename with count > 1 is NEVER wikilinked in that source — recorded as a permanent exception. Known: `INDEX.md` collides 3 ways in `project-library-global` |
| Leaf-folder rule | Leaf folders (files only, or only excluded subfolders) are the unit of work; non-leaf folders are decomposed into child leaf folders, never batched as one unit |

## Per-leaf-folder cycle (one continuous run)

| Step | Action |
|---|---|
| 1 Learnings | Load `C:\mybizz\logs\mb-wikilinks\learnings\` — prior NO_MATCH patterns and settled naming conventions steer this folder |
| 2 Backup | Every file in the leaf folder, unedited, to `C:\backup-mb-wikilinks\backup-mb-wikilinks_<source>_<folder-path-flattened>_<filename>_<YYYYMMDDTHHMMSS>.md` — `.md` is always the final suffix; ≥1 s between file backups (timestamp collision prevention) |
| 3 Detect | Identify every candidate cross-reference (3 patterns: backtick-wrapped bare refs, Related Documents table rows, inline prose refs); classify each `MATCH` / `NO_MATCH` / `AMBIGUOUS` against the real file listing; nothing converted, nothing written |
| 4 Report | Fixed structure: one heading per file (path as heading); per candidate exactly four parts — line number, the anomaly quoted exactly, the proposed exact `[[slug\|Display Text]]` (or "flagged for your decision"), a short justification. Then STOP — same-run pause |
| 5 Approve | Full approval / partial-corrected approval (user edits are authoritative, applied exactly) / clarification request / rejection. No apply without an explicit on-record approval for this exact report, this same run |
| 6 Apply | Only what was approved, exactly as returned; no re-deriving, no extending, no touching frontmatter or anything unapproved |
| 7 Verify | Per edited file: `diff <backup> <edited>` — every changed line must match an approved conversion exactly; any unexpected change → STOP, report |
| 8 Commit/push | Only edited files; message identifies leaf folder + task (`mb-wikilinks: adr-global — N references converted`); skipped if not a git repo or workflow says no — confirm, don't assume |
| 9 Log | Append to `C:\mybizz\logs\mb-wikilinks\run-log.md` (or the per-run in-progress record moved to `last-completed-run\` at close-out): filename, backup path, count converted, diff-clean yes/no, commit hash |
| 10 Learnings | Durable patterns for the next leaf folder (recurring NO_MATCH resolutions, confirmed naming conventions) — same learnings file as Step 1 |
| End of run | `gbrain sync --source <source-id>`; `gbrain extract --stale`; `gbrain doctor` — confirm `link_resolution_opportunity`/`graph_signals_coverage` *moved*, not just "no errors". Next leaf folder = its own invocation |

## Wide mode (`(all)`)

| Rule | Content |
|---|---|
| Meaning | Every locked source, in Section 0 order; every leaf folder within each source |
| Never merged | Each leaf folder still gets its own complete cycle — own backup, own report, own approval pause, own commit — a wide run is a sequence of full cycles |
| Progress | Per-folder completion tracked in the run log; resume at the current folder |
| Commits | Per-folder (as today); batched commit plan (one table — repo, folders, file count; one approval) applies when a folder's cycle commits |

## Operational state (live, 2026-09-10)

| Item | Value |
|---|---|
| Runs completed | None on record — no run logs, no learnings files yet (retrofit work predates the logging discipline; SKILL.md notes in-scope sources were worked in the earlier manual retrofit) |
| `C:\mybizz\logs\mb-wikilinks\` | + 4 subfolders (learnings / in-progress / last-completed-run / abandoned-runs) — created 2026-09-10, empty |
| `C:\backup-mb-wikilinks\` | Renamed from `C:\backup-wikilinks` 2026-09-10 per the naming standard |
| skill-index status | "mb-wikilinks — working" |
| V2 remediations | Target grammar `(all)`/`(folder)`/empty-asks; wide mode; Anvil code-repo denial; path renames (backup + logs + 4 subfolders); scope note (locked scope ∩ scaffold) |

## Cross-cutting integration

| System | Finding |
|---|---|
| Cupcake | No component-specific rule. Cross-project writes → the shared grant-handover pattern (one copy-pasteable `mg-grant` block, developer-issued). Enforcement status of Cupcake is not fixed — live status: `cupcake-config.md` Current Operational Status |
| Memory Governor | None found |
| security-global | None found |
| Related skills | mb-align-docs (**runs FIRST** — it validates and heals every reference in its existing written form; this skill then converts the healed, correct references — product-then-packaging, final ruling 2026-09-10); mb-docs-manager (structure first); mb-sysdoc-creator (produced this suite) |

## Resolution universe (corrected 2026-09-10)

The skill's collision check and target lookup run against the **whole corpus** — every
registered source — matching the global basename resolver the skill itself enables. A name
matching exactly one document anywhere converts; a name matching several anywhere is
ambiguous (never auto-converted); a name matching nowhere is a **missing-document finding**
for align-docs (the hard-won rule: every corpus document was researched and built
deliberately — investigate, never dismiss), reported as such and never buried as noise.
| GBrain | The skill's entire purpose — converts prose conventions into GBrain-parseable links; end-of-run verification reads GBrain's own counters (`link_resolution_opportunity`, `graph_signals_coverage`), not just error-free status |

## Open items

1. **Run order (final ruling 2026-09-10):** mb-docs-manager → mb-align-docs (validate and heal first) → **mb-wikilinks** (convert the healed corpus).
2. `templates-global` frontmatter status (5 files without any block) — excluded from retrofit regardless; the underlying status question is align-docs/frontmatter territory, not this skill's.
3. Retroactive run logs: the earlier manual retrofit work has no run-log records; history is reconstructable only from git commits (`mb-wikilinks:`-prefixed messages).
4. `INDEX.md` collision exception: 3-way in project-library-global — permanent, recorded in the skill text.
5. Anvil-hosted documentation: standing research task (as with the other two skills) — moot while code repos are denied.
