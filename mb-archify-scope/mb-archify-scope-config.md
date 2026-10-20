---
title: "mb-archify-scope-config"
doc-id: "mb-694acd5e"
updated: "2026-10-20"
---

# mb-archify-scope — Configuration

Canonical current-state configuration record for the `mb-archify-scope` scoping
skill. Agent-facing. States what exists and what it is set to — reasoning in
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-explainer.md);
procedure in
[[[mybizz-config-docs:mb-archify-scope/mb-archify-scope-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-archify-scope/mb-archify-scope-reference.md).

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | spec body at repo commit `cfcf0fa` (branch `main`, working tree clean) |
| Standard taken from | the repo spec, doc-id `mb-ab9e047b` — the same body as the installed copy |
| Last researched | 2026-10-20 |

## Skill

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Name | `mb-archify-scope` | `mb-archify-scope` | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md), row `mybizz / archify` | |
| What it is | front-of-pipe scoping for `/archify`: turns a drawing request into an approved Scope Card before any Archify authoring begins; scopes, never draws | identical to standard | repo spec (Reference §Authoritative sources) | |
| Invocation | `/mb-archify-scope` | `/mb-archify-scope`, model-invoked (the description carries the trigger branches) | repo spec (Reference §Authoritative sources) | |
| Catalog category | — | mybizz / archify / Support / Both hosts / status OK | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | |
| Structure | nine phases, each with a completion gate | identical to standard: Intent → ASK → Context → Preliminary scope → Scope the source → Feasibility probe declaration → Report and gate → Handoff contract → Close-out | repo spec (Reference §Authoritative sources) | |

## Canonical locations

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Canonical spec (repo) | — | `/mnt/c/mybizz/mb-archify-scope/mb-archify-scope.md` (doc-id `mb-ab9e047b`) | [[[mybizz-os-docs:os-reference-docs/repo-organization\|repo-organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | |
| Repo contents | — | `.git/` + the spec file — nothing else | live listing | |
| Installed copy | — | `~/.config/opencode/skills/mb-archify-scope/SKILL.md` (14,467 B; spec: 14,339 B) | live listing | |
| Body equality | — | bodies byte-identical, frontmatter only differs — the repo spec carries doc frontmatter (`title`/`doc-id`/`updated`), the installed copy carries skill frontmatter (`name`/`description`) | `diff` of the two bodies, frontmatter excluded (Reference §Checks) | |
| Sync mechanism | — | none mechanical — the same body change is applied to both files by hand | Reference §Keeping spec and installed copy in sync | |

## GBrain registration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Source | — | `mb-archify-scope` — federated, path `/mnt/c/mybizz/mb-archify-scope`, 1 page (the spec) | `gbrain sources list` (command line) | |
| Sync | — | carried by commit all, through the standing GBrain sync | [[[mybizz-config-docs:gbrain/gbrain-config\|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) §Registered sources | |

## Layout budget (dataflow)

Read fresh from the Archify package at Phase 5, never from memory. Values
verified against the installed archify package:

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Stages (2–5) | centers `x = 100 + stage×215`; band 168 wide; header `y=46` | identical to standard | `renderers/dataflow/README.md` (archify package) | |
| Row tops (row 0–4) | `y = 128, 242, 356, 470, 584` (+ `yOffset`) | identical to standard | `renderers/dataflow/README.md` (archify package) | |
| Default node | 112×58 | identical to standard | `renderers/dataflow/README.md` (archify package) | |
| Node spacing | ≥10px between any two nodes | identical to standard | `renderers/dataflow/README.md` (archify package) | |
| Flow length | ≥34px between endpoints | identical to standard | `renderers/dataflow/README.md` (archify package) | |
| Showcase rhythm | every nonzero segment ≥8px; interior turns ≥16px | identical to standard | `renderers/dataflow/README.md` (archify package) | |
| Automatic Port Spread | default; skipped for explicit `via`/`channelX`/`channelY`/`labelAt`/non-auto routes | identical to standard | `renderers/dataflow/README.md` (archify package) | |
| Repair order | quality_profile → node overlap → edge-through-node/endpoint-direction → crossings/corridors/rhythm → label clearance | identical to standard | `renderers/dataflow/README.md` (archify package) | |

## Integration

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| /archify | consumes the approved machine header as its input contract | identical — a failed probe returns work to Phase 5, never past it | repo spec (Reference §Authoritative sources) | |
| Archify suite | — | documented as a component: [[[mybizz-config-docs:archify/archify-config\|Archify Configuration]]](C:/mybizz/mybizz-config-docs/archify/archify-config.md) (scoping-skill component section), [[[mybizz-config-docs:archify/archify-reference\|Archify Reference]]](C:/mybizz/mybizz-config-docs/archify/archify-reference.md) (front-of-pipe invocation note), [[[mybizz-config-docs:archify/archify-explainer\|Archify Explainer]]](C:/mybizz/mybizz-config-docs/archify/archify-explainer.md) (why scoping comes first) | archify suite | |
| Run artifacts | — | live under `C:\mybizz\mybizz-config-docs\archify\output\{slug}\` (one folder per project slug) | repo spec (Reference §Authoritative sources) | |
| Provenance pages | — | [[[mybizz-config-docs:sessions/2026-09-15-006-archify-scope-skill\|Session 006]]](C:/mybizz/mybizz-config-docs/sessions/2026-09-15-006-archify-scope-skill.md), [[[mybizz-config-docs:facts/2026-09-15-archify-scope-pre-work\|durable fact]]](C:/mybizz/mybizz-config-docs/facts/2026-09-15-archify-scope-pre-work.md), [[[mybizz-config-docs:archify/output/memory-ecosystem-project/learnings/2026-09-15-memory-ecosystem\|first-run learnings]]](C:/mybizz/mybizz-config-docs/archify/output/memory-ecosystem-project/learnings/2026-09-15-memory-ecosystem.md) | live pages | |

## Cross-cutting findings

| System | Finding |
|---|---|
| Cupcake | No component-specific rule for this skill. Standing policy: writes to `~/.config/opencode/skills/` require a grant — installed-copy updates are developer-run. Enforcement state per [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) §Operational status |
| Memory Governor | None found — not a memory writer; no bypass exemption; ordinary sync |
| security-global | No direct principle; one adjacent caution carried in the Explainer (a diagram is communication, not trust-boundary evidence) |
| Task/spawn capability | None — single-session skill; no sub-agent or spawn phrasing |

## Open items

None.
