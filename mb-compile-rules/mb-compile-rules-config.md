---
title: "mb-compile-rules-config"
doc-id: "mb-9fcb2ee6"
updated: "2026-10-20"
---
# mb-compile-rules — Configuration

State of the mb-compile-rules skill. The procedure lives in the canonical
source (`C:\mybizz\mb-compile-rules\mb-compile-rules.md`); commands in
[[[mybizz-config-docs:mb-compile-rules/mb-compile-rules-reference|mb-compile-rules Reference]]](C:/mybizz/mybizz-config-docs/mb-compile-rules/mb-compile-rules-reference.md); reasoning in
[[[mybizz-config-docs:mb-compile-rules/mb-compile-rules-explainer|mb-compile-rules Explainer]]](C:/mybizz/mybizz-config-docs/mb-compile-rules/mb-compile-rules-explainer.md). All values verified
live unless noted. The rule estate is not recorded here (see
[[[mybizz-config-docs:mb-compile-rules/mb-compile-rules-learnings|mb-compile-rules Learnings]]](C:/mybizz/mybizz-config-docs/mb-compile-rules/mb-compile-rules-learnings.md), L1).

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | `2e2ac13` — "mb-compile-rules: correct rule-file naming" |
| Standard taken from | Canonical source `C:\mybizz\mb-compile-rules\mb-compile-rules.md` at commit `2e2ac13` |
| Last researched | 2026-10-20 |

## Naming convention

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Source file name | The source keeps its own name: `(rule-name).md` — no forced `cup-` prefix | Same, verified against the 21 files in the estate | Canonical source, Hard Rule 3 (`2e2ac13`); live estate listing | |
| Compiled file name | `cup-(rule-name).rego`; a rule-name already starting `cup-` is not prefixed a second time | Same | Canonical source, Hard Rule 3 | |
| Package name | Global target `~/.config/cupcake/policies/opencode/` → `cupcake.global.policies.(name)`; project-local `./.cupcake/policies/opencode/` → `cupcake.policies.(name)`; must match the real deployment folder — a mismatch loads without error and never fires | Same | Canonical source, Hard Rule 4 | |
| Deployment target | `cupcake.policies.*` for project-local | All rules global — `cupcake.global.policies.*` | [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md); canonical source | |

## Installed copy

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Skill copy | One canonical source file | Single installed copy at `~/.config/opencode/skills/mb-compile-rules/SKILL.md`; body identical to canonical `2e2ac13` (frontmatter transformed to `name`/`description` by design) | Live diff against `2e2ac13` | |
| Invocation | — | `/mb-compile-rules (rule-name)` — `rule-name` is the source file's name without `.md` | Canonical source, User-invocable section | |

## Operational status

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Rule estate | — | Recorded in [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) — sources in `C:\dev\project-library-global\rules-cupcake-global\`, deployed files in the global policy folder; this suite carries no estate rows | [[[mybizz-os-docs:os-reference-docs/system-integrity-explainer\|System Integrity Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/system-integrity-explainer.md), section 6 | L1 |
| Cupcake enforcement | — | Standing policy — status and current enforcement state in [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | |

## Open items

None.
