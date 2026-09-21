---
document: "docs-manager — Config"
doc-id: docs-manager-config
state: Live
date-created: 2026-09-10
---

# docs-manager — Config

State of the `mb-docs-manager` skill as of 2026-09-10. All facts verified
live this date unless noted. Skill version: **V11** (invocation grammar +
wide-sweep support, 2026-09-10; scope model V10, 2026-09-09).

## Identity

| Field | Value |
|---|---|
| Component | `mb-docs-manager` — first-party OpenCode skill (developer-built) |
| Role | System document inventory curator — keeps navigational documents synchronized with the filesystem |
| Invocation | `/mb-docs-manager (all)` — full scaffold sweep; `/mb-docs-manager (name)` — one target; `(division-maps)`, `(quick)`, `(references)` — named partial sweeps; trailing `no-push` modifier. Empty/omitted target → the skill ASKS, never assumes |
| Version | 11, frontmatter `version: 11`, `updated: 2026-09-10` |
| Language | Natural-language procedure + 5 sub-agent definition files; no executable code |

## File inventory

| Location | Files |
|---|---|
| This folder (canonical suite) | `docs-manager-config.md`, [[docs-manager-reference|Reference]], [[docs-manager-explainer|Explainer]] |
| Installed skill — `~/.config/opencode/skills/mb-docs-manager/` | `SKILL.md` (V11, 1,252 ln), `docs-manager-README.md`, `docs-manager-backup.md`, `docs-manager-scan.md`, `docs-manager-apply.md`, `docs-manager-filesystem.md`, `docs-manager-commit.md` |
| Artifacts documented, not deleted | `docs-manager-README.md:Zone.Identifier` |
| Repo mirror | none — removed 2026-09-09 (obsolete; this suite is the indexed artifact) |

## Scope model (V10, unchanged in V11)

| Element | Value |
|---|---|
| Scope source of truth | [[mybizz-scope-list|Mybizz Scope List]] — pinned managed document, read at Phase 0 of every run; wins over SKILL.md on scope |
| In-scope roots (everything walked) | `C:\_data-mybizz-mgt`, `C:\dev`, `C:\mybizz\mybizz-config-docs`, `C:\mybizz\mybizz-os-docs`, `C:\mybizz\memory-audit-reports` |
| Exceptions | `C:\mybizz\{gbrain, gstack, logs, matt-pocock-skills-source, anvil-agent-references, archify, archive, scripts}` |
| Out of scope (recorded) | `C:\dev\dev-mb5pdlf`, `C:\dev\dev-mb4ecom`, `C:\dev\project-template`, `C:\dev\obsolete`, `C:\pdlf`, `C:\_data-not mybizz`, `C:\_data-mybizz-exempt` (as listed in scaffold), `C:\backup-mb-*` folders, system paths |
| Hygiene carve-out | `.git`, `.opencode`, dependency dirs (`node_modules`, `.venv`, `venv`, `__pycache__`, `site-packages`, `vendor`, `.cache`) |
| Code repos | **Denied entirely (V11)** — never opened/read/edited in any mode, including `theme\assets\docs` inside them (Anvil app assets; Anvil owns their interpretation). Top-level paths existence-checked on reference; repo-checked in pre-flight. `dev-makepdlf\makepdlf` = declared placeholder, never flagged; no `anvil.yaml` will ever be proposed (standing rule) |
| Active Repositories (pre-flight) | the 12-repo GitHub list in `projects-config-register.md` (mirrors the scaffold) — checked even when folders are outside walk scope |

## Target grammar (V11)

| Invocation | Meaning |
|---|---|
| `(all)` | Every in-scope root walked in one run — the deliberate wide mode |
| `(name)` | One folder or document |
| `(division-maps)` / `(quick)` / `(references)` | Named partial sweeps |
| `(all) no-push` | Wide sweep, Phase 6 skipped (offer at Phase 9) |
| empty / omitted | **The skill asks for a target — never a default** (reverses the pre-V11 "no keyword = full run" rule) |
| code repo named | Denied — skill states it and asks for a planning-corpus target |

## Managed document types (backed up + scanned)

| Type | Ruleset |
|---|---|
| [[mybizz-scope-list|Mybizz Scope List]] (scope scaffold) | Section 1.3 — verified against disk every run; never edited by the skill |
| `docmap.md` (root, `C:\dev\dev-root\`) | Section 3.1 |
| `projects-config-register.md` | Section 3.1 — append-only register rules |
| `README.md` (discovered) | Section 3.5 |
| `AGENTS.md` (discovered) | Section 3.5 + per-file naming approval gate |
| `INDEX.md` (discovered) | Section 3.3 |

Retired: `scaffold-system.html`; `project-inventory.md` (replaced by the register); `workspace-docmap.md` (obsolete-moved to archive 2026-09-10).

## Register state

| Item | Value |
|---|---|
| Register rows | 11 (9 original + the two document repos registered 2026-09-09) |
| Config YAMLs | `mybizz-config-docs-config.yaml`, `mybizz-os-docs-config.yaml` |
| GitHub repositories section | 12 repos with visibility + local paths (verbatim from scaffold) |
| `mybizz-config.yaml` | rewritten 2026-09-10 — scaffold-driven scope documented |

## Procedure structure (SKILL.md V11)

| Section | Contents |
|---|---|
| Hard constraints | 3 — write-only-in-4a/4b (+4 create-only exemptions); Phase 0 mandatory pre-flight + count-verified backup; never runs GBrain state-changing commands |
| Phases | −2 resume → −1 learnings → 0 pre-flight/backup → 1 scan → 2 report → 2a two-tier presentation → 3 approval (push decision + AGENTS.md naming gate) → 3a grant handover → 4a text edits → 4b file ops (never deletes; second confirmation) → 5 verify → 6 commit/push (Step 0 batched commit plan) → 7 log → 8 learnings → 9 completion gate |
| Anomaly classes | 13 — REPOS_DIRTY, BACKUP_FAILED, BROKEN, MISMATCHED, AMBIGUOUS, CODE_REPO_AMBIGUOUS, GRANT_REQUIRED, STALE DATE, MISSING, UNDOCUMENTED, COUNT MISMATCH, NO_REPO, PUSH_FAILED |
| Run state | continuous checkpointing to `in-progress\` from Phase −2; resume always asked, never automatic |

## Log and backup infrastructure (live state 2026-09-10, post-rename)

| Path | State |
|---|---|
| `C:\mybizz\logs\mb-docs-manager\` | 4 permanent run logs (2026-07-23 ×2, 2026-07-30, 2026-09-10); Learnings: 17 files; in-progress/abandoned-runs: empty; last-completed-run: `2026-09-10T00-04-50.md` |
| `C:\backup-mb-docs-manager\` | 2 snapshots (2026-07-28; 2026-09-09 smoke — 45/45 verified) — renamed from `C:\backup-docs-manager` per the 2026-09-10 naming standard |
| `C:\mybizz\logs\github-logs\` | 3 commit-push + 3 git-status files |
| `C:\mybizz\logs\gbrain-logs\` | sync logs (written by the sync script, not this skill) |

## Approval and permission model (V11)

| Mechanism | Rule |
|---|---|
| Two-tier report | Standard tier: text edits grouped by folder×type, one yes/no per group, every item listed; rejectable per group. High-risk tier: own section, grouped + labelled by risk type (`HIGH RISK — renames/moves (N)`), approved individually, never batch |
| Grant handover | Approved edits outside the shared-library list → the ENTIRE request set tabled as ONE copy-pasteable block (`mg-grant --path <folder> --count N`, one line per folder); developer pastes once; skill never invokes `mg-grant` itself; verifies `cup-grants-data.rego`; slips ~30 min, decrement per use; any policy denial stops the run — never worked around |
| Commit plan | Phase 6 Step 0: one table (repo, folders touched, file count), one batch approval, one commit per repo |
| Push | Phase 3 push approval is a separate recorded decision; Phase 9 offers it again if skipped |

## Cross-cutting integration

| System | Finding |
|---|---|
| Cupcake | No component-specific rule. Three block classes designed-for: cross-project writes → Phase 3a grant handover; git commit/push → Phase 3/6 push-approval gates; AGENTS.md edits → per-file naming gate. Enforcement status of Cupcake itself is not fixed — live status: [[cupcake-config|Cupcake Configuration]] Current Operational Status |
| Memory Governor | None found — not a memory writer; GBrain read-only (Hard Constraint 3); sync is the external script at Phase 9 Step 3 |
| security-global | None found |
| Related skills | mb-align-docs (Phase 9 Step 3a reminder after 4b structural changes), mb-wikilinks, mb-sysdoc-creator (produced this suite). All three documentation skills now share: target grammar `(all)`/`(name)`/empty-asks, two-tier approval, grant-block handover, per-repo commits, Anvil code-repo denial |

## Open items

1. **docmap.md full redraw — deferred work order.** Executes in the dedicated wide-mode run after all three suites exist (planned: this suite's post-remodel run).
2. `docs-manager-scan.md` reference regex retains `projects-reference` deliberately (dead-path references classify BROKEN, not unclassified).
3. Two `:Zone.Identifier` artifacts documented, not deleted (standing pattern).
4. Trio documents (daily-ops.md, master-task-list.md, mybizz-todo.md) — refreshed by the 2026-09-17 wide-mode run: daily-ops and master-task-list Live at `C:\data-mybizz-mgt\desktop\`; mybizz-todo retired 2026-09-17 (not found on disk).
5. Big-run sequencing (final ruling 2026-09-10, product-then-packaging): **mb-docs-manager → mb-align-docs → mb-wikilinks** — align-docs validates and heals references in their existing form first; wikilinks then converts the healed corpus.
