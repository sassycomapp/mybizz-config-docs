---
title: "mb-compile-rules-reference"
doc-id: "mb-c2e50820"
updated: "2026-10-15"
---
# mb-compile-rules — Reference

Execution reference for `/mb-compile-rules`. **The authoritative procedure is
the canonical source `C:\mybizz\mb-compile-rules\mb-compile-rules.md` — the
installed copy at `~/.config/opencode/skills/mb-compile-rules/SKILL.md` must
stay body-identical to it.** Values in
[[[mybizz-config-docs:mb-compile-rules/mb-compile-rules-config|mb-compile-rules Configuration]]](C:/mybizz/mybizz-config-docs/mb-compile-rules/mb-compile-rules-config.md); reasoning in
[[[mybizz-config-docs:mb-compile-rules/mb-compile-rules-explainer|mb-compile-rules Explainer]]](C:/mybizz/mybizz-config-docs/mb-compile-rules/mb-compile-rules-explainer.md).

## Invocation

```
/mb-compile-rules (rule-name)
```

`rule-name` is the name, without `.md`, of a real Markdown file already
present in `C:\dev\project-library-global\rules-cupcake-global\`. The source
keeps its own name — no forced `cup-` prefix. The developer supplies the
name; the skill never invents one.

## Rules that shape every run

- **Nothing stays without a real pass and an explicit keep.** Both test
  cases must genuinely pass against real `cupcake eval` output, from the
  file's real, final location, and the developer must state "keep" —
  otherwise the file is removed immediately.
- **Never invent a test result.** A described or assumed result is not a
  substitute for real output.
- **The agent never runs `cupcake` directly — standing rule regardless of
  enforcement status.** When Cupcake is active, its own exec-protection
  builtin blocks it mechanically; while suspended, the discipline stands.
  Draft the exact `cupcake eval` commands and hand them to the developer;
  wait for real output. Never construct an indirect path around the
  block, for any reason.
- **`opa check` is agent-safe** (invokes `opa`, never `cupcake`): run it
  on every draft before placement; do not proceed on a non-zero exit.
- **One rule, one single complete write.** A helper function must be in
  the same write as any rule that calls it — dependent parallel edits
  caused a real live crash.
- **The package name must match the deployment folder, decided before
  drafting.** Global target (`~/.config/cupcake/policies/opencode/`) →
  `cupcake.global.policies.(name)`. Project-local
  (`./.cupcake/policies/opencode/`) → `cupcake.policies.(name)`. A
  mismatch loads silently and never fires.
- **Placement and testing are the same action.** `cupcake eval` only ever
  evaluates what is actually present in a real, scanned policy folder —
  there is no test-in-isolation step.
- **Health check immediately after any placement or change**: a harmless
  `read` on any file must return a clean allow. Anything else is a live
  incident — the developer removes the file in their own terminal before
  anything else proceeds.
- **Naming.** Sources keep their own names; compiled files are
  `cup-(rule-name).rego`, and a rule-name already starting `cup-` is not
  prefixed a second time.

## Real evaluation

The verified invocation syntax, tool values and argument field names live
in [[[mybizz-config-docs:cupcake/cupcake-reference|Cupcake Reference]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-reference.md) — one fact, one home. Two facts
belong here:

- `cupcake eval` is inert: it never executes a real tool call — nothing
  is created or modified; the permission-slip decrement only happens in
  live use.
- The agent does not run it — standing rule; every real test in this
  environment's rule history was run by the developer.

## Amendment pattern

1. Update the plain-language source `.md` in `rules-cupcake-global`
   (keep its fixed structure).
2. Compile via the skill; apply **minimal diffs to live-proven rule text**
   rather than rewriting.
3. `opa check` the draft before touching the live folder.
4. Back up the current live rule with a **non-`.rego` suffix**
   (e.g. `.rego.bak-YYYYMMDD`) — never scanned, instant rollback.
5. Place; run the health check; run the full test sheet (developer-run);
   explicit keep decision.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Canonical source (issuer: MyBizz) | `C:\mybizz\mb-compile-rules\mb-compile-rules.md` | `2e2ac13` | 2026-10-15 |
| Cupcake reference — evaluation schema, invocation and grants | [[[mybizz-config-docs:cupcake/cupcake-reference\|Cupcake Reference]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-reference.md) | Cupcake `0.3.0` estate | 2026-10-15 |
| System integrity — division context, section 6 | [[[mybizz-os-docs:os-reference-docs/system-integrity-explainer\|System Integrity Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/system-integrity-explainer.md) | — | 2026-10-15 |
| Skills catalog — install record | [[[mybizz-os-docs:os-reference-docs/skills-catalog\|Skills Catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | — | 2026-10-15 |
| Repository organization — source-repo listing | [[[mybizz-os-docs:os-reference-docs/repo-organization\|Repository Organization]]](C:/mybizz/mybizz-os-docs/os-reference-docs/repo-organization.md) | — | 2026-10-15 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `git -C /mnt/c/mybizz/mb-compile-rules log -1 --format='%h %ad'`; then diff the installed copy against the recorded commit — `git -C /mnt/c/mybizz/mb-compile-rules show (commit):mb-compile-rules.md` against `~/.config/opencode/skills/mb-compile-rules/SKILL.md`: body must be identical, only the frontmatter transform (repo `title`/`doc-id` vs installed `name`/`description`) may differ | agent |
| Naming convention | Read the canonical source's Hard Rule 3; confirm the estate's source names keep their own names (`ls /mnt/c/dev/project-library-global/rules-cupcake-global/`) | agent |
| Deployment target | All rules global — read the estate rows in [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) | agent |
| Live policy folder | `ls ~/.config/cupcake/policies/opencode/builtins/` — deployed rules, grants-data files, backups never loaded | developer |
| Binaries | `ls ~/.cupcake/bin/` — `cupcake` and `opa` present | developer |
| Works | Source↔deployed correspondence current in [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md); the newest rule on record went through this pipeline end-to-end | agent |

## Do not

- Do not run `cupcake` (any subcommand) from the agent's own tool context.
- Do not construct an indirect path around exec-protection — wrapper
  script, shell function, or any other means, for any reason.
- Do not treat an offline `opa eval` pass as sufficient — only real live
  `cupcake eval` output, run by the developer, closes a rule.
- Do not split a rule across dependent parallel edits.
- Do not choose the deployment target after drafting.
- Do not let any `.rego` file enter a live policy folder by any path other
  than this pipeline — an unvalidated file there can crash evaluation
  entirely (the recorded incident).
- Do not use `time.*` or `opa.runtime().env` in any rule — both fail
  silently in the live engine.
- Do not leave a failed or rejected file in a scanned policy folder —
  remove it immediately.
