---
title: "mb-compile-rules-config"
doc-id: "mb-compile-rules-config"
---
# mb-compile-rules Configuration

Canonical current-state configuration record. Agent-facing. States facts,
not history or rules — the procedure itself lives in the skill's own
`SKILL.md` (same folder); commands in [[mb-compile-rules-reference|mb-compile-rules Reference]];
reasoning in [[mb-compile-rules-explainer|mb-compile-rules Explainer]]. All values verified live
2026-09-08 unless noted.

## Identity

| Item | Value |
|---|---|
| Name | `mb-compile-rules` — custom (mb-*) skill, not vendor software |
| Purpose | Converts a Cupcake rule written in Markdown into a working, tested policy file |
| Corrected | 2026-08-28, after live testing (two wrong assumptions fixed — see explainer) |
| Invoked as | `/mb-compile-rules (rule-name)` |
| Skill base directory | `~/.config/opencode/skills/mb-compile-rules/` |

## Skill file copies (two real copies exist)

| Copy | Path | State |
|---|---|---|
| Installed (what OpenCode loads) | `~/.config/opencode/skills/mb-compile-rules/SKILL.md` (real file, 2026-08-28) | Authoritative for execution |
| Mirror (in this folder) | `C:\mybizz\mybizz-config-docs\mb-compile-rules\SKILL.md` (2026-09-05) | Byte-identical at verification; **no sync mechanism between the two** |

## Pipeline state — the rule estate this skill manages

| Item | Value |
|---|---|
| Rule sources | `C:\dev\project-library-global\rules-cupcake-global\` — 19 `.md` files, `cup-` prefix |
| Live policy folder | `~/.config/cupcake/policies/opencode/` — 19 rules + grants data + `builtins/` (3) + `system/` aggregator |
| Deployment target | All rules global (`cupcake.global.policies.*` package namespace) |
| Rule-change method (developer-stated) | A similar rules file is created/edited in `rules-cupcake-global`; this skill compiles it; every change is thoroughly tested on implementation |
| Binaries | `cupcake` (18.4 MB) and `opa` (47.4 MB) at `~/.cupcake/bin/`; `/usr/local/bin/cupcake` symlink. **The agent never executes `cupcake` directly — standing rule** (see reference) |
| Downstream system | Cupcake — **ACTIVE** (reactivation completed and verified 2026-09-08, the same day this suite was written; status: [[cupcake-config|Cupcake Configuration]]) |

## Integration facts

| Item | State |
|---|---|
| Companion suite | [[cupcake-config|Cupcake Configuration]] + [[cupcake-reference|Usage, Invocation, and Worked Examples]] + [[cupcake-explainer|Mechanical Policy Enforcement for AI Coding Agents]] — the system this skill feeds |
| Sibling skills | `mb-sentinel-review`, `mb-submit-memory` — same custom-skill family; no structural coupling |
| Register | `register-global` lists `rules-cupcake-global` (19 documents) |
| Governance principles | [[sec-review-before-trust|Review Before Trust]], [[sec-dependency-skill-supply-chain|Dependency and Skill Supply Chain]], [[sec-defense-in-depth|Defense in Depth]] — this pipeline is their enforcement-authoring arm |

## Worked precedent (2026-09-08)

The cross-folder rule amendment went through the full pipeline end-to-end:
source updated in `rules-cupcake-global` (commit `fa02fbd`), compiled,
`opa check` pass, previous version backed up with a non-`.rego` suffix,
placed, and live-tested **13/13** by the developer
(`/mnt/c/mybizz/logs/cupcake-rule-test-record-2026-09-08.md`). This is the
standing pattern for any future rule change.

## Open items

- The two SKILL.md copies have no sync mechanism — they are byte-identical
  today (verified); a future edit to one can silently diverge from the other.
- Cupcake reactivation completed 2026-09-08 — the pipeline and live
  enforcement are both proven operational (the cross-folder amendment was
  compiled, tested 13/13, and is now enforced).
- New Cupcake requirement discovered the same day: every project folder the
  agent works in needs the `.cupcake/policies/opencode` + `.cupcake/system`
  skeleton, or the checker crashes on boot there (see [[cupcake-config|Cupcake Configuration]]).
