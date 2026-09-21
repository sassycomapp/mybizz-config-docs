---
document: "Archify — Configuration"
doc-id: archify-config
state: Live
date-created: 2026-09-06
---

# Archify — Configuration

Canonical current-state configuration record for the Archify skill. Agent-facing.
States facts, not history or reasoning — see [[archify-explainer|Explainer]] for what it is
and why, [[archify-reference|Reference]] for commands and procedures.

---

## Identity

| Item | Value |
|---|---|
| Name | Archify |
| Version | 2.16.0 (`package.json`; SKILL.md frontmatter: "2.16") |
| License | MIT |
| Author | tt-a1i |
| Based on | Cocoon-AI/architecture-diagram-generator (MIT, v1.0) |
| Source repo | `github.com/tt-a1i/archify` |
| Local clone | `C:\mybizz\archify` (WSL: `/mnt/c/mybizz/archify`) |
| Skill package root | `C:\mybizz\archify\archify` (WSL: `/mnt/c/mybizz/archify/archify`) |
| CLI entry point | `archify/bin/archify.mjs` |
| Invocation | `/archify` |
| Node requirement | >=18 (active: v24.15.0, confirmed via doctor) |
| Runtime dependencies | None (devDependencies only: `ajv`, `parse5`, `saxes`, `simple-icons`) |
| Doctor status | 15/15 checks pass — "Archify is ready" (verified 2026-09-06) |

## Install on this machine

| Item | Value |
|---|---|
| Install method | WSL symlink from OpenCode's global skill discovery path to the real Windows-drive folder |
| Discovery path | `~/.config/opencode/skills/archify` → `/mnt/c/mybizz/archify/archify` |
| Skill status | Working (per [[skill-index|Skill Index]]; confirmed by successful doctor run) |
| Update check | Notification-only; never downloads, installs, or executes an update |
| Update-check disable | `ARCHIFY_UPDATE_CHECK_DISABLED=1` (disables networking and reminder-state writes) |

## Scoping skill component (`mb-archify-scope`)

A permanent front-of-pipe component of this suite — not transient tooling. It
turns a drawing request into an agreed Scope Card before any Archify authoring
begins; it scopes, it never draws.

| Item | Value |
|---|---|
| Spec (canonical) | [[archify-scope-skill|Scoping Skill Specification]] (this repo, git-versioned) |
| Installed copy | `~/.config/opencode/skills/mb-archify-scope/SKILL.md` (kept byte-identical to the spec — same install pattern as the exam skills) |
| Trigger | Model-invoked — a drawing request routes through scoping first; also fires on recovery after dense-route/corridor failures |
| Invocation order | `/mb-archify-scope` **before** `/archify`, never instead of it |
| Output convention | approved Scope Card → `output/{subject}-scope.md` + machine header `output/{subject}-header.json`; run outputs live under the project's `output/{slug}/` folder |
| Relationship to this exam | The scope-skill is examinable state: its installed copy must match the spec (AR2-3); it is documented in [[archify-explainer|Explainer]] and [[archify-reference|Reference]], and it produces the run learnings this suite absorbs |

## Package structure (`archify/archify/`)

| Path | Contents |
|---|---|
| `SKILL.md` | The skill instruction file OpenCode reads (frontmatter `name: archify`, version 2.16) |
| `bin/archify.mjs` | CLI entry point |
| `schemas/` | 6 files: `common`, [[architecture|Architecture]], `workflow`, `sequence`, `dataflow`, `lifecycle` (each `.schema.json`; `schemas/README.md` also present) |
| `references/` | 4 files: `authoring-contract.md`, `brand-marks.md`, `delivery-contract.md`, `viewer-runtime.md` |
| `renderers/` | Per-type renderers (one per diagram type, plus `shared/`) |
| `recipes/`, `examples/`, `test/`, `migrations/`, `delta/`, `assets/`, `brand-marks/`, `scripts/` | Supporting package content |

## Integration with other system parts

| System | Relationship |
|---|---|
| OpenCode | Skill discovered via symlink in the global skills folder; invoked as `/archify` |
| Scoping skill | `mb-archify-scope` is the documented front-of-pipe component — see the "Scoping skill component" section above; invoked before `/archify`, never instead of it |
| GBrain | No dedicated GBrain knowledge page exists for archify (all searches return unrelated content); install facts live in [[skill-index|Skill Index]] and [[opencode-config|OpenCode Configuration]] |
| Memory Governor | No treatment — archify produces HTML artifacts, not memory submissions; not a governed writer |
| Cupcake | No archify-specific rule in the global policy folder (re-verified 2026-09-16 — the only archify mention is the mg-grant access entry for `mb-config-archify`, an access grant, not an enforcement rule). Cupcake is **ACTIVE and enforcing** per [[cupcake-config|Cupcake Configuration]] §Current operational status (verified live 2026-09-12). Enforcement status is not fixed and should not be assumed current — re-check [[cupcake-config|Cupcake Configuration]] whenever enforcement state changes |
| security-global | No principle bears directly; the only network surface is the optional update check (IP + timestamp to one fixed manifest URL, nothing else transmitted, disableable) |
| Related skills | Graphify (knowledge graphs) and GStack `/design-html` (UI page HTML) are complementary / different-domain; no dependency in either direction |

## Open items

| Item | Status |
|---|---|
| Symlink creation method for this specific link (WSL-side vs Windows-side `mklink /D`) | Unverified. Known drvfs trap ([[opencode-explainer|OpenCode Explainer]] §4): WSL-side symlinks to Windows-drive targets are unreadable by Windows Explorer. Doctor passed, so OpenCode resolves it; Windows-side readability not checked |
| Windows Explorer visibility of the skill through the symlink | Unverified (same item as above) |
| Update-check manifest URL | Claimed by README as one fixed trusted URL; not fetched/verified (out of scope for local skill documentation) |
