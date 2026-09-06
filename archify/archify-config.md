# Archify — Configuration

Canonical current-state configuration record for the Archify skill. Agent-facing.
States facts, not history or reasoning — see `archify-explainer.md` for what it is
and why, `archify-reference.md` for commands and procedures.

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
| Skill status | Working (per `skill-index.md`; confirmed by successful doctor run) |
| Update check | Notification-only; never downloads, installs, or executes an update |
| Update-check disable | `ARCHIFY_UPDATE_CHECK_DISABLED=1` (disables networking and reminder-state writes) |

## Package structure (`archify/archify/`)

| Path | Contents |
|---|---|
| `SKILL.md` | The skill instruction file OpenCode reads (frontmatter `name: archify`, version 2.16) |
| `bin/archify.mjs` | CLI entry point |
| `schemas/` | 6 files: `common`, `architecture`, `workflow`, `sequence`, `dataflow`, `lifecycle` (each `.schema.json`; `schemas/README.md` also present) |
| `references/` | 4 files: `authoring-contract.md`, `brand-marks.md`, `delivery-contract.md`, `viewer-runtime.md` |
| `renderers/` | Per-type renderers (one per diagram type, plus `shared/`) |
| `recipes/`, `examples/`, `test/`, `migrations/`, `delta/`, `assets/`, `brand-marks/`, `scripts/` | Supporting package content |

## Integration with other system parts

| System | Relationship |
|---|---|
| OpenCode | Skill discovered via symlink in the global skills folder; invoked as `/archify` |
| GBrain | No dedicated GBrain knowledge page exists for archify (all searches return unrelated content); install facts live in `skill-index.md` and `opencode-config.md` |
| Memory Governor | No treatment — archify produces HTML artifacts, not memory submissions; not a governed writer |
| Cupcake | No archify-specific rule in the global policy folder. Cupcake's enforcement status is not fixed and should not be assumed current — it was disabled environment-wide at research time (2026-09-06, plugin renamed `.disabled`); live status: `cupcake-config.md` Current Operational Status. This "no rule" finding needs re-verification whenever enforcement state changes |
| security-global | No principle bears directly; the only network surface is the optional update check (IP + timestamp to one fixed manifest URL, nothing else transmitted, disableable) |
| Related skills | Graphify (knowledge graphs) and GStack `/design-html` (UI page HTML) are complementary / different-domain; no dependency in either direction |

## Open items

| Item | Status |
|---|---|
| Symlink creation method for this specific link (WSL-side vs Windows-side `mklink /D`) | Unverified. Known drvfs trap (`opencode-explainer.md` §4): WSL-side symlinks to Windows-drive targets are unreadable by Windows Explorer. Doctor passed, so OpenCode resolves it; Windows-side readability not checked |
| Windows Explorer visibility of the skill through the symlink | Unverified (same item as above) |
| Update-check manifest URL | Claimed by README as one fixed trusted URL; not fetched/verified (out of scope for local skill documentation) |
