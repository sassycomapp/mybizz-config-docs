---
document: "mb-compile-rules Reference"
doc-id: mb-compile-rules-reference
state: Live
date-created: 2026-09-08
---

# mb-compile-rules Reference

Execution reference for `/mb-compile-rules`. **The authoritative procedure
is the skill's own `SKILL.md` in this folder — it loads automatically on
invocation and is never summarized away.** This document carries the
environment-verified facts and the rules that shape execution. Current
state: [[mb-compile-rules-config|mb-compile-rules Configuration]]. Why the design is what it is:
[[mb-compile-rules-explainer|mb-compile-rules Explainer]].

## Invocation

```
/mb-compile-rules (rule-name)
```

`rule-name` identifies a real Markdown file already present at
`C:\dev\project-library-global\rules-cupcake-global\cup-(rule-name).md`.
The developer supplies the name; the skill never invents one.

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
- **`cup-` prefix on every file, source and compiled.**

## Verified real eval schema (do not use other field names)

```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "(tool)", "args": {(camelCase fields)}}' | cupcake eval --harness opencode
```

Confirmed `tool` values: `read`, `edit`, `write`, `bash`, `webfetch`.
Confirmed `args` fields: `filePath`, `oldString`, `newString` (edit/write),
`content` (write), `command` (bash), `url` (webfetch). NOT `tool_name`/
`tool_input` — those are the engine's internal post-normalization names,
invalid as raw input. `cupcake eval` never executes a real tool call —
nothing is created or modified; the permission-slip decrement only happens
in live use.

## Amendment pattern (proven 2026-09-08)

1. Update the plain-language source `.md` in `rules-cupcake-global`
   (keep its fixed structure).
2. Compile via the skill; apply **minimal diffs to live-proven rule text**
   rather than rewriting.
3. `opa check` the draft before touching the live folder.
4. Back up the current live rule with a **non-`.rego` suffix**
   (e.g. `.rego.bak-YYYYMMDD`) — never scanned, instant rollback.
5. Place; run the health check; run the full test sheet (developer-run);
   explicit keep decision.
Worked precedent: the cross-folder rule's three-tier amendment, 13/13
live (`/mnt/c/mybizz/logs/cupcake-rule-test-record-2026-09-08.md`).

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
  entirely (the recorded 2026-09-06 incident).
- Do not use `time.*` or `opa.runtime().env` in any rule — both fail
  silently in the live engine.
- Do not leave a failed or rejected file in a scanned policy folder —
  remove it immediately.
