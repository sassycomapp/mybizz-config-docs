---
title: "mb-form-builder-config"
doc-id: "mb-364826fa"
updated: "2026-11-12"
---

# mb-form-builder — Configuration

Canonical current-state configuration record for the `mb-form-builder` form-building
skill. Agent-facing. States what exists and what it is set to — reasoning in
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-explainer.md);
procedure in
[[[mybizz-config-docs:mb-form-builder/mb-form-builder-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-form-builder/mb-form-builder-reference.md).

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | spec body — repository created 2026-11-12, no commit yet (spec uncommitted in the working tree) |
| Standard taken from | the repo spec — body byte-identical to the installed copy (verified, frontmatter excluded) |
| Last researched | 2026-11-12 |

## Skill

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Name | `mb-form-builder` | `mb-form-builder` | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md), row `mybizz / mb-form-builder` | |
| What it is | writes one feature's Anvil forms from its approved screen requirements, as HTML templates built from m3-custom-theme components, each with its empty Python class and its spec sheet; never wires handlers, never commits | identical to standard | repo spec (Reference §Authoritative sources) | |
| Invocation | the developer names the application and the feature; model-invoked — the description carries the trigger (mo-ui-production section 4, step 9) | identical to standard | repo spec (Reference §Authoritative sources) | |
| Catalog category | — | mybizz / mb-form-builder / Operational / Both hosts | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | |
| Structure | eight numbered sections: Rules It Follows, Input, Gate, Output per Form, Old Forms, Checks, Report, Never | identical to standard | repo spec (Reference §Authoritative sources) | |

## Canonical locations

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Canonical spec (repo) | — | `/mnt/c/mybizz/mb-form-builder/mb-form-builder.md` (6,163 B) | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Repo remote | — | `https://github.com/sassycomapp/mb-form-builder.git` — public, branch `main`, no commit yet | live `git remote -v` | |
| Repo contents | — | `.git/` + the spec file — nothing else | live listing | |
| Installed copy | — | `~/.config/opencode/skills/mb-form-builder/SKILL.md` (6,546 B) | live listing | |
| Body equality | — | bodies byte-identical, frontmatter only differs — the repo spec carries doc frontmatter (`title` only until the hook stamps `doc-id`/`updated` at first commit), the installed copy carries skill frontmatter (`name`/`description`) | `diff` of the two bodies, frontmatter excluded (Reference §Checks) | |
| Sync mechanism | — | none mechanical — the same body change is applied to both files by hand | Reference §Keeping spec and installed copy in sync | |
| Pre-commit hook | — | mb-doc-check installed in the repository (`.git/hooks/pre-commit`) | `install-hook --repo` output | |
| Commit-all | — | `/mnt/c/mybizz/mb-form-builder` in the REPOS array, beside `mb-archify-scope` | `commit-all.sh` | |
| mb-doc-check sources | — | `mb-form-builder = /mnt/c/mybizz/mb-form-builder`; `sources-check`: everything matches | `mb-doc-check.sources`; `sources-check` | |
| OpenCode project | — | project row in `opencode.db` (path `/mnt/c/mybizz/mb-form-builder`, vcs `git`); `projects/mb-form-builder` in daily-ops.md's project list | sqlite query; daily-ops.md | |

## GBrain registration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Source | — | `mb-form-builder` — federated, path `/mnt/c/mybizz/mb-form-builder`, 0 pages, never synced | `gbrain sources list` (command line) | |
| Sync | — | carried by commit all, through the standing GBrain sync | [[[mybizz-config-docs:gbrain/gbrain-config\|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) §Registered sources | |

## Integration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| mo-ui-production | section 5 defines the skill; section 4 step 9 runs it; section 1: the written form is the wireframe | identical — verified live | [[[default:specifications-global/mo-ui-production\|mo-ui-production]]](C:/dev/project-library-global/specifications-global/mo-ui-production.md) | |
| spec-ui-standards | section 14.1: only an approved screen requirement is built; section 14.2: the spec sheet's six contents; the skill is named as the writer | identical | [[[default:specifications-global/spec-ui-standards\|spec-ui-standards]]](C:/dev/project-library-global/specifications-global/spec-ui-standards.md) | |
| Check tooling | `ts_scan.py` under `project-library-global/test-suite/tools/`; the `anvil` CLI; Anvil's own `client-forms` skill | all installed | live listing | |

## Cross-cutting findings

| System | Finding |
|---|---|
| Cupcake | No component-specific rule for this skill. Standing policy: writes outside the working project require a grant — repo and installed-copy writes are grant-gated. Enforcement state per [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) §Operational status |
| Memory Governor | None found — not a memory writer; ordinary sync |
| security-global | No direct principle; two adjacencies carried in the Explainer (the HTMLTemplate ban alignment; the public `theme/assets/` spec-sheet posture) |
| Task/spawn capability | None — single-session skill; no sub-agent or spawn phrasing |

## Open items

1. The repository has no commit: the GBrain source shows 0 pages / never synced; the first commit-all assigns the spec's doc-id (frontmatter is title-only) and gives the source its first page.
2. The installed skill enters OpenCode's skill catalog at the next session start; this session's catalog predates the install.
3. Works (end to end): the first real run on a feature is developer-side (Reference §Checks).
