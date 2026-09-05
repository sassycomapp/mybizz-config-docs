# Cupcake Reference — Usage, Invocation, and Worked Examples

Companion to `cupcake-config.md` (current installed state) and
`cupcake-explainer.md` (design, history, and real incidents). This document
covers how to actually invoke and verify Cupcake's components. Agent-facing.

---

## Invoking `mb-compile-rules`

```
/mb-compile-rules (rule-name)
```

Requires a real Markdown source file already present at
`C:\dev\project-library-global\rules-cupcake-global\(rule-name).md`, following
the fixed structure: Harness, What to block, Decision, Message shown to the
agent on block, Reason.

## The real, proven decision flow — every rule, every time

1. Read the source document in full.
2. Draft the `.rego` file as a **single, complete write** — never split
   across dependent parallel edits. A helper function must be defined in the
   same write as any rule that calls it.
3. Run `opa check` on the drafted file. Do not proceed on a non-zero exit.
4. Think through realistic false-positive and false-negative risks before
   finalizing test cases — a exact-basename match, not a substring match,
   for filenames; word-boundary edge cases for command patterns (a hyphen
   ends a word just as whitespace does); flag ordering in commands with
   multiple arguments.
5. Place the file directly at its real, live location —
   `~/.config/cupcake/policies/opencode/cup-(rule-name).rego` for a global
   rule. There is no separate "test in isolation, then deploy" step —
   `cupcake eval` only ever evaluates what is actually present in the real,
   scanned policy folder.
6. Immediately run a real health check — a harmless `read` on any file —
   to confirm the whole policy bundle still compiles. **If this returns
   anything other than a clean `allow`, this is a live incident**: the
   developer removes the file directly, in their own terminal, before
   anything else proceeds.
7. Run the real block-case and allow-case tests, via real `cupcake eval`
   output, run by the developer in their own terminal — never simulated,
   never predicted from the drafted logic alone.
8. Explicit keep/remove decision, stated plainly, only after real results
   are confirmed against expectations.

Any failure at any step: fix and re-verify from that step forward, or
remove and start over. Never proceed on an assumption that a fix "should"
work.

## Verified real invocation syntax

```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "(tool)", "args": {(fields)}}' | cupcake eval --harness opencode
```

Confirmed working `tool` values: `read`, `edit`, `write`, `bash`, `webfetch`.
Confirmed working `args` fields (camelCase): `filePath`, `oldString`,
`newString` (edit/write), `content` (write), `command` (bash), `url`
(webfetch).

**The agent cannot run this itself.** `cupcake_exec_protection` blocks
direct execution of the `cupcake` binary from the agent's own tool context,
including `cupcake eval`, `cupcake --help`, `cupcake --version`, and
`cupcake verify`. Every real test in this environment's entire rule-build
history was run by the developer, in their own terminal, and reported back.

## `mg-grant` / `mg-revoke` — cross-project access

```
mg-grant --path <folder> --count N
mg-revoke --path <folder>
```

`<folder>` accepts either Windows (`C:\…`) or WSL (`/mnt/c/…`) form —
converted internally to canonical WSL form (lowercase, forward slashes,
trailing slash stripped). Re-granting an already-granted path updates
that entry in place rather than duplicating it.

**Real worked example — full cycle:**
```
mg-grant --path /mnt/c/tmp/target --count 2
cat ~/.config/cupcake/policies/opencode/cup-grants-data.rego
# grants := { "/mnt/c/tmp/target": {"count": 2, "expires_at_ns": ...} }

# — a real Write tool call to a file inside /mnt/c/tmp/target/ —

cat ~/.config/cupcake/policies/opencode/cup-grants-data.rego
# count now 1 — decremented by the plugin's tool.execute.after hook

# — a second real write —
# count now 0

# — a third real write attempt —
# ❌ Policy Violation: This path is outside the current project...

mg-revoke --path /mnt/c/tmp/target
# entry removed entirely
```

**Important: a raw `cupcake eval` pipe does not exercise the decrement.**
It only asks the policy engine for a decision — it never executes a real
tool call, so the plugin's `tool.execute.after` hook never fires. Only a
genuine tool execution (a real `Write`/`Edit` performed by the agent)
moves the count. This distinction cost real debugging time once — see
`cupcake-explainer.md` Section 5E.

## Confirming the plugin is loaded exactly once

```bash
grep -ia 'loading plugin' ~/.local/share/opencode/log/*.log | tail -5
```

Check the most recent session's timestamp block specifically. Exactly
one `cupcake.js` line, from the global path only, is correct. Two lines
in the same session means a project-local copy still exists somewhere —
see `cupcake-config.md`'s Known scope limitations.

## Worked example — a real, live-verified rule build

Rule: `no_destructive_database_operations`.

**Source condition:** block `DROP` (table/database/schema/index/view/
function/role/user/trigger), unconditioned `DELETE`, `TRUNCATE`.

**Draft, tested offline, passed 26/26** — including deliberately-designed
false-positive checks: `cat truncate-notes.md` (must allow, not match
`\btruncate\b` as a substring of a hyphenated filename).

**Real, live test — a sample of the confirmed results:**

```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "bash", "args": {"command": "DROP TABLE users"}}' | cupcake eval --harness opencode
→ {"decision":"deny", "reason":"Destructive database operations are prohibited...", "rule_id":"GLOBAL-POLICY-NO-DESTRUCTIVE-DATABASE-OPERATIONS"}

echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "bash", "args": {"command": "cat truncate-notes.md"}}' | cupcake eval --harness opencode
→ {"decision":"allow"}
```

**Keep decision:** yes — real, live-verified in both directions.

## Worked example — a rule that failed live despite passing offline

Rule: `no_cross_project_filesystem_access_by_default`.

Passed 17/17 offline `opa eval`. Real, live test showed six of seven block
cases silently returning `allow`:

```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "edit", "args": {"filePath": "../other-project/file.py", "oldString": "a", "newString": "b"}}' | cupcake eval --harness opencode
→ {"decision":"allow"}   # WRONG — expected deny
```

Root cause: the draft used `regex.replace`, which fails silently in the real
compiled engine (`matched_policy_count=2`, `total_decisions=0` — the rule
matched but produced nothing). Rebuilt using only `split`/`concat`/iteration
— functions already proven live elsewhere — and re-verified against real
output before being trusted again.

## Worked example — a third confirmed offline-pass/live-fail case

Rule: the cross-project grant logic, first design (superseded).

An early draft used `time.now_ns()` inside Rego to compare a grant's
timestamp against the current moment. A dedicated, isolated probe —
placed live, tested, removed immediately — confirmed it fails exactly
like `regex.replace` and `opa.runtime().env` before it: the rule matched
(a control condition confirmed the event reached it) but the time-based
condition never fired, no error, no crash. The fix moved all time
computation out of Rego entirely — see `cupcake-config.md`'s Cross-
project access grants section for the current, working design.

## Confirming a rule is genuinely live and correctly scoped

**Health check** (run after placing or modifying any rule):
```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "read", "args": {"filePath": "README.md"}}' | cupcake eval --harness opencode
```
Anything other than a clean `{"decision":"allow"}` is a live incident.

**Recovering from a live incident** (developer's own terminal):
```
rm ~/.config/cupcake/policies/opencode/cup-(rule-name).rego
```
Then re-run the health check to confirm recovery before doing anything else.

**Real, live syntax check** for a Rego file, without touching the live
folder (safe, zero risk, works even when `cupcake eval` itself is blocked
for the agent, since it invokes `opa`, not `cupcake`):
```
opa check (path-to-file.rego)
```

## Do not

- Do not treat `opa check` or offline `opa eval` alone as sufficient —
  both are necessary, neither is sufficient. Only real, live `cupcake eval`
  output, run by the developer, closes a rule.
- Do not issue multiple dependent edits to the same drafted file in
  parallel — a rule referencing a helper function must have that helper
  defined in the same, single write.
- Do not assume a package name is correct without confirming it matches
  the deployment folder — `cupcake.global.policies.*` for
  `~/.config/cupcake/policies/opencode/`, `cupcake.policies.*` for a
  project-local `.cupcake/policies/opencode/` folder. A mismatch loads
  silently and never fires.
- Do not attempt any workaround when `cupcake_exec_protection` blocks a
  command — including via a wrapper script, a shell function, or any other
  indirect construction. Stop and hand the exact command to the developer.
- Do not run `cupcake init` in a project that has not actually started —
  see `cupcake-config.md` for the current, deliberate project-init scope.
- Do not use `time.*` or `opa.runtime().env` in any rule — both confirmed
  to fail silently live, despite working in the standalone `opa` CLI.
- Do not test the grant decrement mechanism with a raw `cupcake eval`
  pipe — it never executes a real tool call, so the decrement hook never
  fires. Use a genuine tool execution.
- Do not hand-edit `cup-grants-data.rego` — always use `mg-grant`/
  `mg-revoke`.
