---
title: "mb-archify-scope-config"
doc-id: "mb-694acd5e"
updated: "2026-10-08"
---

# mb-archify-scope — Configuration

Canonical current-state configuration record for the `mb-archify-scope` scoping
skill. Agent-facing. States facts, not history — reasoning in
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-explainer.md); procedure in
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md). All values verified live 2026-10-07
unless noted.

## Identity

| Item | Value |
|---|---|
| Name | `mb-archify-scope` — custom (mb-*) skill, mybizz-built |
| What it is | Front-of-pipe scoping for `/archify`: turns a drawing request into an approved Scope Card before any Archify authoring begins; scopes, never draws |
| Invocation | `/mb-archify-scope` — model-invoked (the description carries the trigger branches) |
| Category (skills-catalog) | mybizz / archify / Support / Both hosts / status OK |
| Built | 2026-09-15 (session 006), renamed from `mb-archify-scoping`; Phase 9 added during the first live run |

## Canonical locations

| Item | Value |
|---|---|
| Canonical spec (repo) | `C:\mybizz\mb-archify-scope\mb-archify-scope.md` (WSL: `/mnt/c/mybizz/mb-archify-scope/mb-archify-scope.md`), doc-id `mb-ab9e047b`, updated 2026-10-08 (run #1 gate-approved F-1 file-convention correction) |
| Repo contents | `.git/` + the spec file — nothing else |
| Installed copy | `~/.config/opencode/skills/mb-archify-scope/SKILL.md` (14,467 B; spec: 14,339 B) |
| Sync state | Bodies byte-identical (hash pair `c22bef6a8c635424` both sides, verified 2026-10-08 after the gate-approved body-to-body re-sync); frontmatter differs by design — repo spec carries doc frontmatter (`title`/`doc-id`/`updated`), installed copy carries skill frontmatter (`name`/`description`) |
| Sync mechanism | None mechanical — the same body change is applied to both files by hand; a plain copy of the spec over the installed copy destroys the skill frontmatter |

## GBrain registration

| Item | Value |
|---|---|
| Source | `mb-archify-scope` — federated |
| Path | `/mnt/c/mybizz/mb-archify-scope` |
| Pages | 1 (the spec) |
| Last sync | 2026-10-07 08:34 UTC |
| Pattern | One-page-per-skill-repo, shared with mb-close-out, mb-compile-rules, mb-project-docs, mb-sentinel-review, mb-sysdoc-creator, mb-submit-memory, mb-memory-system-diagnostic |

## Structure — the nine phases

| Phase | Output | Gate |
|---|---|---|
| 1 Intent | one-paragraph restatement (subject, audience, guarantee, load-bearing claim) | developer confirms |
| 2 ASK | bounded interview | interview complete |
| 3 Context | source material identified; load-bearing claim traced | claim traced |
| 4 Preliminary scope | single-word pipeline + type decision; `type + why` | developer approves type |
| 5 Scope the source | Node Inventory, one Main Path, Deferred List, Corridor Plan | inventory complete |
| 6 Feasibility probe | declaration only — the probe executes in the Archify run | declaration recorded |
| 7 Report and gate | Scope Card presented (+ reshaped alternatives when infeasible) | the single hard gate |
| 8 Handoff contract | Scope Card + machine header written verbatim — first write of the run | files byte-match approval |
| 9 Close-out | run learnings, written only on developer approval | ask, never assume |

The skill is read-only until Phase 8.

## Integration

| System | Relationship |
|---|---|
| /archify | consumes the approved machine header as its input contract; a failed probe returns work to Phase 5, never past it |
| Archify suite | documented as a component: [[[mybizz-config-docs:archify/archify-config\|Archify Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) (scoping-skill component section), [[[mybizz-config-docs:archify/archify-reference\|Archify Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md) (front-of-pipe invocation note), [[[mybizz-config-docs:archify/archify-explainer\|Archify Explainer]]](C:/mybizz/mybizz-config-docs/archify/archify-explainer.md) (why scoping comes first) |
| mb-config-archify exam | check AR2-3 verifies the installed copy matches the spec |
| Run artifacts | live under `C:\mybizz\mybizz-config-docs\archify\output\{slug}\` (one folder per project slug) |
| Provenance pages | [[[mybizz-config-docs:sessions/2026-09-15-006-archify-scope-skill\|Session 006]]](C:/mybizz/mybizz-config-docs/sessions/2026-09-15-006-archify-scope-skill.md), [[[mybizz-config-docs:facts/2026-09-15-archify-scope-pre-work\|durable fact]]](C:/mybizz/mybizz-config-docs/facts/2026-09-15-archify-scope-pre-work.md), [[[mybizz-config-docs:archify/output/memory-ecosystem-project/learnings/2026-09-15-memory-ecosystem\|first-run learnings]]](C:/mybizz/mybizz-config-docs/archify/output/memory-ecosystem-project/learnings/2026-09-15-memory-ecosystem.md) |

## Cross-cutting findings

| System | Finding |
|---|---|
| Cupcake | No component-specific rule (rule-source inventory checked 2026-10-07). Standing policy: writes to `~/.config/opencode/skills/` require a grant — installed-copy updates are developer-run. Enforcement ACTIVE everywhere, live-verified 2026-10-04 ([[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md), Current Operational Status) |
| Memory Governor | None found — not a memory writer; no bypass exemption; ordinary sync |
| security-global | No direct principle; one adjacent caution carried in the explainer (a diagram is communication, not trust-boundary evidence) |
| Task/spawn capability | None — single-session skill; no sub-agent or spawn phrasing |

## Run history

| Date | Run | Outcome |
|---|---|---|
| 2026-09-15 | memory-ecosystem architecture diagram | scope approved, 9 nodes; authoring converged 17→0 diagnostics; delivered 9/9 showcase |

## Open items

1. **RESOLVED 2026-10-08** — Spec drift closed at the run #1 gate (F-1 approved): the File-conventions drift (flat vs nested) was corrected at all three recorded locations (§File conventions table, Phase 8 inline paths, Phase 9 learnings path); the installed copy was re-synced body-to-body and the hash pair `c22bef6a8c635424` verified. The header contract carries one path shape.
2. Fact ownership: this suite now owns the skill's facts; archify-config's scoping-skill component section is to be reduced to a cross-reference pointer (developer-run edit, separate task).
3. mybizz-config-docs has no suite register (its README structure table lists only the 8 older reference-style folders) — flagged, not created.
4. Cupcake skills-dir ancestor-cwd case (carried in the cupcake exam report) is unresolved; installed-copy writes are treated as grant-required from every session until it is.