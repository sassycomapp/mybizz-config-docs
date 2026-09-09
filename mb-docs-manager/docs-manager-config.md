# docs-manager — Config

State of the `mb-docs-manager` skill as of 2026-09-10. All facts verified
live this date unless noted. Skill version: **V10** (scaffold-driven scope
model, 2026-09-09).

## Identity

| Field | Value |
|---|---|
| Component | `mb-docs-manager` — first-party OpenCode skill (developer-built) |
| Role | System document inventory curator — keeps navigational documents synchronized with the filesystem |
| Invocation | `/mb-docs-manager` (full run), `/mb-docs-manager <scope>` — explicit invocation only, never auto-trigger |
| Version | 10, frontmatter `version: 10`, `updated: 2026-09-09` |
| Language | Natural-language procedure + 5 sub-agent definition files; no executable code |

## File inventory

| Location | Files |
|---|---|
| This folder (canonical suite) | `docs-manager-config.md`, `docs-manager-reference.md`, `docs-manager-explainer.md` |
| Installed skill — `~/.config/opencode/skills/mb-docs-manager/` | `SKILL.md` (V10), `docs-manager-README.md`, `docs-manager-backup.md`, `docs-manager-scan.md`, `docs-manager-apply.md`, `docs-manager-filesystem.md`, `docs-manager-commit.md` |
| Artifacts documented, not deleted | `docs-manager-README.md:Zone.Identifier`, (former) `mb-docs-manager-explainer.md:Zone.Identifier` — obsolete-moved with its file to `C:\mybizz\archive\` |
| Repo mirror | none — the former `mybizz-config-docs\mb-docs-manager\SKILL.md` reference copy was removed 2026-09-09 (obsolete; superseded by this suite) |

## Scope model (V10 — scaffold-driven)

| Element | Value |
|---|---|
| Scope source of truth | `C:\_data-mybizz-mgt\_desktop\mybizz-scope-list.md` — pinned managed document, read at Phase 0 of every run; wins over SKILL.md on scope |
| In-scope roots (everything walked) | `C:\_data-mybizz-mgt`, `C:\dev`, `C:\mybizz\mybizz-config-docs`, `C:\mybizz\mybizz-os-docs`, `C:\mybizz\memory-audit-reports` |
| Exceptions | `C:\mybizz\{gbrain, gstack, logs, matt-pocock-skills-source, anvil-agent-references, archify, archive, scripts}` |
| Out of scope (recorded) | `C:\dev\dev-mb5pdlf`, `C:\dev\dev-mb4ecom`, `C:\dev\project-template`, `C:\dev\obsolete`, `C:\pdlf`, `C:\_data-not mybizz`, `C:\_data-mybizz-exempt` (as listed in scaffold), `C:\backup-*` folders, system paths |
| Hygiene carve-out (never walked, inside roots) | `.git`, `.opencode`, `node_modules`, `.venv`, `venv`, `__pycache__`, `site-packages`, `vendor`, `.cache` |
| Code-repo content-exclusion | retained — code repo contents never opened; top-level paths existence-checked. In-scope code repo: `C:\dev\dev-mb-3-cs\mb-3-cs`. `C:\dev\dev-makepdlf\makepdlf` = declared placeholder, never flagged; no `anvil.yaml` will ever be proposed (standing rule) |
| Active Repositories (pre-flight) | the 12-repo GitHub list in `projects-config-register.md` (mirrors the scaffold) — checked even when folders are outside walk scope |

## Managed document types (backed up + scanned)

| Type | Ruleset |
|---|---|
| `mybizz-scope-list.md` (scope scaffold) | Section 1.3 — verified against disk every run; never edited by the skill |
| `docmap.md` (root, `C:\dev\dev-root\`) | Section 3.1 |
| `projects-config-register.md` | Section 3.1 — append-only register rules |
| `README.md` (discovered) | Section 3.5 |
| `AGENTS.md` (discovered) | Section 3.5 + per-file naming approval gate |
| `INDEX.md` (discovered) | Section 3.3 |

Retired: `scaffold-system.html` (historical only); `project-inventory.md` (deleted 2026-08-13, replaced by the register); `workspace-docmap.md` (obsolete-moved to archive 2026-09-10 — duplicate docmap).

## Register state (post-remediation)

| Item | Value |
|---|---|
| Register rows | 11 (9 original + `mybizz-config-docs-config`, `mybizz-os-docs-config` — document repos registered per developer decision 2026-09-09) |
| Config YAMLs created | `mybizz-config-docs-config.yaml`, `mybizz-os-docs-config.yaml` |
| GitHub repositories section | 12 repos with visibility + local paths (verbatim from scaffold) |
| `mybizz-config.yaml` | rewritten 2026-09-10 — six dead folders removed, scaffold-driven scope documented |

## Procedure structure (SKILL.md V10)

| Section | Contents |
|---|---|
| Hard constraints | 3 — write-only-in-4a/4b (+4 infrastructure exemptions); Phase 0 mandatory pre-flight+verified backup; never runs GBrain state-changing commands |
| Phases | −2 resume → −1 learnings → 0 pre-flight/backup → 1 scan → 2 report → 3 approval (+push decision, + AGENTS.md naming gate) → 3a grant handover → 4a text edits → 4b file ops (never deletes; second confirmation) → 5 verify → 6 commit/push → 7 log → 8 learnings → 9 completion gate |
| Anomaly classes | 13 — REPOS_DIRTY, BACKUP_FAILED, BROKEN, MISMATCHED, AMBIGUOUS, CODE_REPO_AMBIGUOUS, GRANT_REQUIRED, STALE DATE, MISSING, UNDOCUMENTED, COUNT MISMATCH, NO_REPO, PUSH_FAILED |
| Scope keywords | full (default), `<document-path>`, `division-maps`, `quick`, `references`, `no-push` |
| Run state | continuous checkpointing to `in-progress\` from Phase −2; resume always asked, never automatic |

## Log and backup infrastructure (live state 2026-09-10)

| Path | State |
|---|---|
| `C:\mybizz\logs\docs-manager\` | 4 permanent run logs (2026-07-23 ×2, 2026-07-30, 2026-09-10) |
| `...\Learnings\` | 17 files (14 historical + 3 from this remediation) |
| `...\in-progress\` / `...\abandoned-runs\` | empty |
| `...\last-completed-run\` | `2026-09-10T00-04-50.md` (the remediation/smoke run) |
| `C:\backup-docs-manager\` | 2 snapshots (2026-07-28T12-45-45; 2026-09-09 smoke — 45/45 verified) |
| `C:\mybizz\logs\github-logs\` | 3 commit-push + 3 git-status files |
| `C:\mybizz\logs\gbrain-logs\` | sync logs (written by the sync script, not this skill) |

## Cross-cutting integration

| System | Finding |
|---|---|
| Cupcake | No component-specific rule. Three block classes were analyzed and designed-for: cross-project writes → Phase 3a prefilled grant handover (the designed `mg-grant` mechanism, ~30-min ephemeral slips — no rule exceptions); git commit/push → Phase 3 push-approval gate (explicit, recorded, precedes execution); AGENTS.md edits → per-file naming approval gate. Enforcement status of Cupcake itself is not fixed — live status: `cupcake-config.md` Current Operational Status |
| Memory Governor | None found — not a memory writer; GBrain is read-only by Hard Constraint 3; sync is the external script at Phase 9 Step 3 |
| security-global | None found |
| Related skills | mb-align-docs (Phase 9 Step 3a reminder after 4b structural changes — complementary content-vs-structure division); mb-wikilinks (cross-reference form); mb-sysdoc-creator (produced this suite; declares the same modus operandi) |

## Open items

1. **docmap.md full redraw — deferred work order.** The smoke-run scan found it badly stale (dead `config\` tree pointers, 8 undocumented folders, wrong paths). Per developer sequencing: redraw happens in the dedicated run after the three doc suites exist and all three skills (mb-docs-manager, mb-align-docs, mb-wikilinks) have run.
2. `docs-manager-scan.md` reference-extraction regex retains `projects-reference` as a normalization pattern (deliberate — dead-path references classify BROKEN correctly); not a live scope reference.
3. The two `:Zone.Identifier` artifacts: documented, not deleted (standing pattern).
4. Trio documents (daily-ops.md, master-task-list.md, mybizz-todo.md) at `C:\_data-mybizz-mgt\_desktop\` are genuinely stale — updated later by the three-skills run (developer sequencing).
