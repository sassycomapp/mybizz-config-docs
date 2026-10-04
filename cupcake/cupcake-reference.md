---
title: "cupcake-reference"
doc-id: "mb-e79d3d01"
updated: "2026-10-04"
---
# Cupcake Reference — Usage, Invocation, and Worked Examples

Companion to [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) (the spec — current installed state, operational
status) and [[[mybizz-config-docs:cupcake/cupcake-explainer|Mechanical Policy Enforcement for AI Coding Agents]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-explainer.md) (design, history, and real incidents — the
authoritative whole-system narrative). Exam companions: [[[mybizz-config-docs:cupcake/cupcake-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-exam-plan.md)
(next run's job-spec), [[[mybizz-config-docs:cupcake/cupcake-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-exam-report.md) (current verified state),
[[[mybizz-config-docs:cupcake/cupcake-log|Log]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-log.md) (notable events), [[[mybizz-config-docs:cupcake/cupcake-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-learnings.md) (transient exam
knowledge). Agent-facing.

**Status note:** Cupcake is **ACTIVE** as of 2026-09-12 — enforcement verified
end-to-end (plugin → engine → rules) after the plugin `cwd` fix, the
Bash-governance amendment live-tested 35/35, and the system-protection bash
matcher corrected (its `/dev/` substring had halted every `/mnt/c/dev/` path
and `/dev/null` redirect). Full record:
`/mnt/c/mybizz/logs/cupcake-rule-test-record-2026-09-12.md`. The procedures
below are the proven operational record. **Amended 2026-09-22 (set-and-forget):
`failMode: open` is the environment default, and sessions in folders without a
`.cupcake` skeleton evaluate global policies only via the fallback home
`~/.config/cupcake/fallback` (WARN-logged per call) — launching from any folder
is safe, with no per-folder preparation ever required.** One load-bearing
requirement remains: any folder that DOES carry a `.cupcake` skeleton must keep
at least one real local policy module in `.cupcake/policies/opencode` (the
input-gated `cup-noop-fallback.rego` placeholder satisfies this) — OPA v1.19.1's
wasm compiler panics on an aggregator-only bundle.

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
status.** `cupcake_exec_protection` blocks direct execution of the `cupcake`
binary from the agent's own tool context, including `cupcake eval`, `--help`,
`--version`, and `verify`. This block is mechanically active and confirmed live.
Every real test in this environment's entire rule-build history was run by the
developer, in their own terminal.

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
tool execution moves the count (see [[[mybizz-config-docs:cupcake/cupcake-explainer|Mechanical Policy Enforcement for AI Coding Agents]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-explainer.md) §7E).

## `git-grant` — commit allowances (WP3, 2026-09-22)

```
git-grant --repo <folder> --count N --minutes M
```

Issues a bounded commit allowance for one repository: `git commit`,
`git push`, and `git merge` in that repo are allowed while the entry is
live, and each allowed action consumes one unit. `--minutes` is
configurable (default 30, matching `mg-grant`'s fixed expiry). Writes the
same generated-file discipline as `mg-grant`:
`~/.config/cupcake/policies/opencode/cup-git-grants-data.rego`, package
`cupcake.global.policies.git_grants_data` — never hand-edited.

The compiled commits policy resolves the target repo from the command's
`git -C <path>` when the command names one, otherwise from the session
working directory (a cwd inside the repo matches by prefix). Publish
(`npm/yarn/pnpm publish`) and the named deploy CLI invocations are
outside the channel entirely — they deny absolutely regardless of any
grant. Before the first `git-grant` call the file does not exist and
every git commit/push/merge denies (fail-closed).

**Worked example — full cycle:**
```
git-grant --repo /mnt/c/mybizz/mybizz-config-docs --count 2 --minutes 30
cat ~/.config/cupcake/policies/opencode/cup-git-grants-data.rego
# grants := { "/mnt/c/mybizz/mybizz-config-docs": {"count": 2, "expires_at_ns": ...} }

# — a real `git commit -m "..."` in that repo (through the plugin) —
# count now 1 — decremented by the plugin's tool.execute.after hook
# — a second real commit — count now 0
# — a third commit attempt — ❌ Policy Violation (or expiry prunes the entry)

git-revoke: none — allowances expire; re-granting a repo updates the entry in place
```

**Important: a raw `cupcake eval` pipe exercises the allow/deny decision
but not the decrement**, exactly as for path grants — the count moves
only through genuine plugin-governed tool calls.

## `net-grant` / `net-revoke` — network grants (2026-09-13)

```
net-grant --domain <domain> --count N
net-revoke --domain <domain>
```

Issues a bounded fetch allowance for one domain: webfetches to that host are
allowed while the entry is live, and the count decreases by one per allowed
fetch — decremented by the plugin's `tool.execute.after` hook. Expiry is
fixed at 30 minutes — hardcoded, no `--minutes` flag (matching `mg-grant`'s
fixed expiry), pruned by the plugin's `tool.execute.before` hook. Domains
are stored lowercase and exact — no wildcards, no scheme or port (a URL
pasted as the domain is normalized to its bare host). Re-granting an
already-granted domain updates that entry in place. Writes the same
generated-file discipline as `mg-grant`:
`~/.config/cupcake/policies/opencode/cup-network-grants-data.rego`, package
`cupcake.global.policies.network_grants_data` — never hand-edited.

**Real worked example — full cycle (live-verified 2026-10-04):**
```
net-grant --domain example.com --count 1
cat ~/.config/cupcake/policies/opencode/cup-network-grants-data.rego
# grants := { "example.com": {"count": 1, "expires_at_ns": ...} }

# — a real webfetch to https://example.com — allowed, count now 0
# — a second fetch attempt — ❌ Policy Violation (count exhausted, or expiry prunes the entry)

net-revoke --domain example.com
# entry removed entirely
```

**The agent does not run these tools itself.** The grant tools are
developer-terminal only — the agent asks the developer to run `net-grant`,
stating the domain and the count it needs; the control-plane rule denies
agent invocation of the grant tools by name in bash, and the outbound-network
deny message itself instructs the agent to ask.

**Important: a raw `cupcake eval` pipe exercises the allow/deny decision
but not the decrement**, exactly as for path grants — the count moves only
through genuine plugin-governed tool calls.

## Confirming the plugin is loaded exactly once

```bash
grep -ia 'loading plugin' ~/.local/share/opencode/log/*.log | tail -5
```

Exactly one `cupcake.js` line, from the global path only, in the most recent
session's timestamp block, is correct. Note: OpenCode's two-process architecture
(server + TUI) may produce two load lines in the same log file — this is a
logging artefact, not a double-registration. Confirmed 2026-09-12: one plugin
initialization per session, hooks fire once per tool call.

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
computation out of Rego entirely — see [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)'s grants mechanics.

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
real-world triggers, 2026-09-06 and 2026-09-22 (full accounts in the
[[[mybizz-config-docs:cupcake/cupcake-explainer|Mechanical Policy Enforcement for AI Coding Agents]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-explainer.md)).

**Since the 2026-09-22 set-and-forget amendment, this failure class cannot
block the environment anymore:** `failMode: open` is the environment default
(evaluation failures degrade to log-and-allow), and skeleton-less folders fall
back to `~/.config/cupcake/fallback` instead of failing checker init. A crash
of this shape after 2026-09-22 means the plugin file itself is damaged or
missing — recover by restoring a backup
(`cp ~/.config/opencode/plugin/cupcake.js.bak-20260922-pre-amendment ~/.config/opencode/plugin/cupcake.js`)
and restarting.

The historical diagnostic sequence remains valid for understanding either
incident, and for any future pre-amendment plugin version:

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
   as of 2026-09-06 — see [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)):
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

**Status: APPLIED 2026-09-08.** The config was written and the scaffold file
removed and gitignored (commit `3abf084`). The original crash was never
reproduced, so the fix's effect on that specific crash is untested — but by
construction, any future evaluation crash now degrades to "log and allow"
instead of blocking all work.

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
solution** — see [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)'s standing context.

## Disabling Cupcake — immediate, fully reversible

```bash
mv ~/.config/opencode/plugin/cupcake.js ~/.config/opencode/plugin/cupcake.js.disabled
```
Restart OpenCode. Nothing else on disk is touched. **To re-enable:**
```bash
mv ~/.config/opencode/plugin/cupcake.js.disabled ~/.config/opencode/plugin/cupcake.js
```

## Full uninstall — permanent, NOT reversible

Only run after an explicit, deliberate decision to permanently remove Cupcake:

```bash
rm ~/.config/opencode/plugin/cupcake.js
rm -rf ~/.config/cupcake
rm /usr/local/bin/cupcake
rm -rf ~/.cupcake
rm ~/.config/cupcake/bin/mg-grant ~/.config/cupcake/bin/mg-revoke 2>/dev/null
```

Note: `/usr/local/bin/opa` is a standalone OPA binary used independently of
Cupcake — do not remove it as part of a Cupcake uninstall unless you are
certain nothing else depends on it.

No backup is taken. The rule source documents at
`C:\dev\project-library-global\rules-cupcake-global\` are untouched and would
remain the only way to rebuild the rule set.

## Do not

- Do not treat an offline `opa eval` pass as sufficient — only real, live `cupcake eval` output, run by the developer, closes a rule.
- Do not issue multiple dependent edits to the same drafted file in parallel — a rule referencing a helper must have that helper in the same, single write.
- Do not assume a package name is correct without confirming it matches the deployment folder — `cupcake.global.policies.*` for global, `cupcake.policies.*` for project-local. A mismatch loads silently and never fires.
- Do not run `cupcake eval` (or any direct `cupcake` invocation) from the agent's own tool context — standing rule regardless of enforcement status; when active, `cupcake_exec_protection` blocks it mechanically. Hand the exact command to the developer.
- Do not construct an indirect path around an exec-protection block — wrapper script, shell function, or any other means, for any reason, including testing or diagnosis.
- Do not run `cupcake init` in a project that has not actually started — see config.md's project-init status. (Note: `cupcake init` stalled interactively without output when run in `~/.config/cupcake/fallback` on 2026-09-22; the fallback skeleton was built by selective copy from the proven makepdlf scaffold instead. Init is now optional everywhere — the fallback covers skeleton-less folders.)
- Do not create a project-local copy of `cupcake.js`, symlinked or otherwise — exactly one copy, at the global path.
- Do not use `time.*` or `opa.runtime().env` in any rule — both fail silently live.
- Do not test the grant decrement with a raw `cupcake eval` pipe — the decrement hook never fires without a real tool execution.
- Do not hand-edit `cup-grants-data.rego` — always `mg-grant`/`mg-revoke`.
- Every `.cupcake` skeleton must keep at least one real local policy module — never empty `policies/opencode` (the OPA wasm compiler panics on an aggregator-only bundle); the input-gated `cup-noop-fallback.rego` placeholder satisfies this and never fires.
