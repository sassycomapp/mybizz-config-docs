# Cupcake Reference — Usage, Invocation, and Worked Examples

Companion to `cupcake-config.md` (current installed state, operational status)
and `cupcake-explainer.md` (design, history, and real incidents). Agent-facing.

**Status note:** Cupcake is currently suspended — the procedures below are the
proven operational record and the path back, not a description of current live
behavior (see `cupcake-config.md`'s Current Operational Status).

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
2. Draft the `.rego` file as a **single, complete write** — never split across
   dependent parallel edits. A helper function must be defined in the same
   write as any rule that calls it.
3. Run `opa check` on the drafted file. Do not proceed on a non-zero exit.
4. Think through realistic false-positive and false-negative risks before
   finalizing test cases — exact-basename match, not substring, for filenames;
   word-boundary edge cases for command patterns (a hyphen ends a word just as
   whitespace does); flag ordering in commands with multiple arguments.
5. Place the file directly at its real, live location —
   `~/.config/cupcake/policies/opencode/cup-(rule-name).rego` for a global
   rule. There is no separate "test in isolation, then deploy" step —
   `cupcake eval` only ever evaluates what is actually present in the real,
   scanned policy folder.
6. Immediately run a real health check — a harmless `read` on any file — to
   confirm the whole policy bundle still compiles. Anything other than a clean
   `allow` is a live incident: the developer removes the file directly, in
   their own terminal, before anything else proceeds.
7. Run the real block-case and allow-case tests, via real `cupcake eval`
   output, run by the developer in their own terminal — never simulated,
   never predicted from the drafted logic alone.
8. Explicit keep/remove decision, stated plainly, only after real results are
   confirmed against expectations.

Any failure at any step: fix and re-verify from that step forward, or remove
and start over. Never proceed on an assumption that a fix "should" work.

## Verified real invocation syntax

```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "(tool)", "args": {(fields)}}' | cupcake eval --harness opencode
```

Confirmed working `tool` values: `read`, `edit`, `write`, `bash`, `webfetch`.
Confirmed working `args` fields (camelCase): `filePath`, `oldString`,
`newString` (edit/write), `content` (write), `command` (bash), `url` (webfetch).

**The agent does not run this itself — standing rule regardless of enforcement
status.** When active, `cupcake_exec_protection` blocks direct execution of
the `cupcake` binary from the agent's own tool context, including `cupcake
eval`, `--help`, `--version`, and `verify`. Cupcake is currently suspended, so
the block is inert today — the discipline stands anyway, and re-enabling
restores it mechanically. Every real test in this environment's entire
rule-build history was run by the developer, in their own terminal.

## `mg-grant` / `mg-revoke` — cross-project access

```
mg-grant --path <folder> --count N
mg-revoke --path <folder>
```

`<folder>` accepts Windows or WSL form — converted internally to canonical WSL
form. Re-granting an already-granted path updates that entry in place.

**Real worked example — full cycle:**
```
mg-grant --path /mnt/c/tmp/target --count 2
cat ~/.config/cupcake/policies/opencode/cup-grants-data.rego
# grants := { "/mnt/c/tmp/target": {"count": 2, "expires_at_ns": ...} }

# — a real Write tool call to a file inside /mnt/c/tmp/target/ —
# count now 1 — decremented by the plugin's tool.execute.after hook
# — a second real write — count now 0
# — a third real write attempt — ❌ Policy Violation

mg-revoke --path /mnt/c/tmp/target
# entry removed entirely
```

**Important: a raw `cupcake eval` pipe does not exercise the decrement.** It
only asks the policy engine for a decision — it never executes a real tool
call, so the plugin's `tool.execute.after` hook never fires. Only a genuine
tool execution moves the count (see `cupcake-explainer.md` §7E).

## Confirming the plugin is loaded exactly once

```bash
grep -ia 'loading plugin' ~/.local/share/opencode/log/*.log | tail -5
```

Exactly one `cupcake.js` line, from the global path only, in the most recent
session's timestamp block, is correct. (While suspended: zero lines.)

## Worked example — a real, live-verified rule build

Rule: `no_destructive_database_operations`. Source condition: block `DROP`
(9 object types), unconditioned `DELETE`, `TRUNCATE`. Draft passed 26/26
offline including false-positive checks (`cat truncate-notes.md` must allow).
Real live test: `DROP TABLE users` → deny with rule_id; `cat
truncate-notes.md` → allow. **Kept — live-verified in both directions.**

## Worked example — a rule that failed live despite passing offline

Rule: `no_cross_project_filesystem_access_by_default`, first draft. Passed
17/17 offline; live, six of seven block cases silently returned `allow`. Root
cause: `regex.replace` fails silently in the real compiled engine
(`matched_policy_count=2`, `total_decisions=0`). Rebuilt using only
`split`/`concat`/iteration and re-verified live before being trusted again.

## Worked example — a third confirmed offline-pass/live-fail case

The grant logic's first design used `time.now_ns()` inside Rego. An isolated
live probe confirmed the same silent-failure signature. The fix moved all time
computation out of Rego entirely — see `cupcake-config.md`'s grants mechanics.

## Confirming a rule is genuinely live and correctly scoped

**Health check** (after placing or modifying any rule):
```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "read", "args": {"filePath": "README.md"}}' | cupcake eval --harness opencode
```
Anything other than a clean `{"decision":"allow"}` is a live incident.

**Recovering from a live incident** (developer's own terminal):
```
rm ~/.config/cupcake/policies/opencode/cup-(rule-name).rego
```
Then re-run the health check to confirm recovery.

**Syntax check without touching the live folder** (safe — invokes `opa`, not
`cupcake`):
```
opa check (path-to-file.rego)
```

## Recovering from a total evaluation crash — every tool call blocked, "exited with code 1"

Distinct from a normal live incident: **every** tool call fails with a bare
`Cupcake exited with code 1` and no policy decision at all. Confirmed
real-world trigger, 2026-09-06: build-mode tool calls (Bash, Glob, Read) all
failed this way in the same session where identical read-only calls had
succeeded earlier in plan mode — evidence the crash is specific to whichever
enforcement path build mode invokes, never confirmed because the crash blocked
every tool needed to investigate it.

**Diagnostic sequence — developer's own terminal:**

1. **Isolate whether Cupcake crashes standalone:**
   ```bash
   cd <project-directory>
   echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "read", "args": {"filePath": "README.md"}}' | cupcake eval --harness opencode
   echo "Exit code: $?"
   ```
2. **Validate every policy file individually** (safe, no `cupcake` invocation):
   ```bash
   find ~/.config/cupcake/policies/opencode -name "*.rego" -exec sh -c 'echo "=== {} ==="; opa check "{}"' \;
   find .cupcake/policies/opencode -name "*.rego" -exec sh -c 'echo "=== {} ==="; opa check "{}"' \;
   ```
3. **Check for an unvalidated scaffold file** — `cupcake init` generates
   `example.rego` in a project-local policy folder; if it entered git history
   via a broad `git add -A` rather than the `mb-compile-rules` pipeline, it is
   a strong suspect for breaking the whole scanned folder (confirmed present
   as of 2026-09-06 — see `cupcake-config.md`):
   ```bash
   cat .cupcake/policies/opencode/example.rego
   opa check .cupcake/policies/opencode/example.rego
   ```
4. **If a bad file is confirmed, remove it directly**, then re-run the health
   check and confirm a clean `allow` before resuming.
5. **If steps 1–4 don't surface the cause:**
   ```bash
   grep -ia 'cupcake\|plugin' ~/.local/share/opencode/log/*.log | tail -50
   ```

## The candidate fix — fail-open mode + project-local scaffold cleanup

**Status: code-verified to exist in the installed plugin; NOT applied or
tested against the real crash.** Two facts, correctly distinguished: the
mechanism is real (verified in the installed plugin's own source —
`failMode` in its default config with real `"open"` handling branches, and
`loadConfig()` reading `.cupcake/opencode.json` from the project root); and
the problem it targets is real (the `.cupcake/policies/opencode/example.rego`
scaffold file is confirmed present in `makepdlf-project-library`). Applying
and testing it against the actual crash has not happened — that is the open
item.

**The mechanism** (from Cupcake's official docs, now confirmed in code):
`failMode` controls what happens when policy evaluation itself crashes or
times out — `"closed"` (default; what this environment ran) denies everything,
which is the exact total-block behavior of the incident; `"open"` allows the
action, logs it, and continues. It changes nothing about any rule's normal-
operation behavior.

**Full config file** — `.cupcake/opencode.json` in the project root
(`makepdlf-project-library`):
```json
{
  "enabled": true,
  "cupcakePath": "cupcake",
  "harness": "opencode",
  "logLevel": "info",
  "timeoutMs": 5000,
  "failMode": "open",
  "cacheDecisions": false
}
```
Minimal version (documented defaults for the rest):
```json
{
  "failMode": "open"
}
```

**Diagnosing the actual crash** (developer's own terminal):
```
cupcake inspect
```
Real, documented command — lists every policy currently loaded, without
needing `cupcake eval` to succeed first.

**The scaffold cleanup** (nothing real depends on the project-local folder —
all 19 rules are global):
```bash
opa check .cupcake/policies/opencode/*.rego
```
Remove any file that fails — most likely `example.rego`. Prevent recurrence:
add `.cupcake/policies/opencode/example.rego` to the project's `.gitignore`.

**Full proposed sequence:**
1. `cupcake inspect` (developer-run) — see what's actually loaded.
2. `opa check` every file in the project-local policy folder; remove anything invalid.
3. Create `.cupcake/opencode.json` with `failMode: "open"`.
4. Re-enable the plugin (below).
5. Re-run the health check — confirm a clean `allow`.
6. Add the `.gitignore` entry.

If step 5 doesn't produce a clean result, `failMode: "open"` means work isn't
blocked while diagnosis continues. **Until this sequence is actually run and
the crash reproduced-and-resolved, the fix remains a candidate, not a
solution** — see `cupcake-config.md`'s standing context.

## Disabling Cupcake — immediate, fully reversible

```bash
mv ~/.config/opencode/plugin/cupcake.js ~/.config/opencode/plugin/cupcake.js.disabled
```
Restart OpenCode. Nothing else on disk is touched. **To re-enable:**
```bash
mv ~/.config/opencode/plugin/cupcake.js.disabled ~/.config/opencode/plugin/cupcake.js
```

## Full uninstall — permanent, NOT reversible

**Prepared and held ready as of 2026-09-06, not executed.** Only run after an
explicit, deliberate decision to permanently remove Cupcake:

```bash
rm ~/.config/opencode/plugin/cupcake.js.disabled
rm -rf ~/.config/cupcake
rm /usr/local/bin/cupcake /usr/local/bin/opa
rm -rf ~/.cupcake
rm ~/.config/cupcake/bin/mg-grant ~/.config/cupcake/bin/mg-revoke 2>/dev/null
```

No backup is taken. The rule source documents at
`C:\dev\project-library-global\rules-cupcake-global\` are untouched and would
remain the only way to rebuild the rule set.

## Do not

- Do not treat an offline `opa eval` pass as sufficient — only real, live `cupcake eval` output, run by the developer, closes a rule.
- Do not issue multiple dependent edits to the same drafted file in parallel — a rule referencing a helper must have that helper in the same, single write.
- Do not assume a package name is correct without confirming it matches the deployment folder — `cupcake.global.policies.*` for global, `cupcake.policies.*` for project-local. A mismatch loads silently and never fires.
- Do not run `cupcake eval` (or any direct `cupcake` invocation) from the agent's own tool context — standing rule regardless of enforcement status; when active, `cupcake_exec_protection` blocks it mechanically. Hand the exact command to the developer.
- Do not construct an indirect path around an exec-protection block — wrapper script, shell function, or any other means, for any reason, including testing or diagnosis.
- Do not run `cupcake init` in a project that has not actually started — see config.md's project-init status.
- Do not create a project-local copy of `cupcake.js`, symlinked or otherwise — exactly one copy, at the global path.
- Do not use `time.*` or `opa.runtime().env` in any rule — both fail silently live.
- Do not test the grant decrement with a raw `cupcake eval` pipe — the decrement hook never fires without a real tool execution.
- Do not hand-edit `cup-grants-data.rego` — always `mg-grant`/`mg-revoke`.
- Do not treat the failMode candidate fix as applied or proven — it is code-verified to exist, not tested against the real crash.
