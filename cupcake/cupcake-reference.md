---
title: "cupcake-reference"
doc-id: "mb-e79d3d01"
updated: "2026-10-20"
---
# Cupcake — Reference

Execution only. Values live in [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md);
reasons in [[cupcake-explainer|Mechanical Policy Enforcement for AI Coding
Agents]].

## Invoking mb-compile-rules

```
/mb-compile-rules (rule-name)
```

Requires a real Markdown source file already present at
`C:\dev\project-library-global\rules-cupcake-global\(rule-name).md`, following
the fixed structure: Harness, What to block, Decision, Message shown to the
agent on block, Reason.

## The decision flow — every rule, every time

1. Read the source document in full.
2. Draft the `.rego` file as a **single, complete write** — a helper must be
   defined in the same write as any rule that calls it.
3. Run `opa check` on the drafted file. Do not proceed on a non-zero exit.
4. Think through realistic false-positive and false-negative risks before
   finalizing test cases — exact-basename match, not substring, for
   filenames; word-boundary edge cases (a hyphen ends a word just as
   whitespace does); flag ordering in commands with multiple arguments.
5. Place the file directly at its real, live location —
   `~/.config/cupcake/policies/opencode/cup-(rule-name).rego` for a global
   rule. There is no separate test-in-isolation step: evaluation only ever
   sees what is present in the scanned policy folder.
6. Immediately run a health check — a harmless `read` on any file. Anything
   other than a clean `allow` is a live incident: the developer removes the
   file directly, in their own terminal, before anything else proceeds.
7. Run the real block-case and allow-case tests via real evaluation output,
   run by the developer in their own terminal — never simulated, never
   predicted from the drafted logic alone.
8. Explicit keep/remove decision, stated plainly, only after real results
   are confirmed against expectations.

Any failure at any step: fix and re-verify from that step forward, or remove
and start over.

## Verified evaluation invocation syntax

```
echo '{"hook_event_name": "PreToolUse", "session_id": "test", "cwd": "'$(pwd)'", "tool": "(tool)", "args": {(camelCase fields)}}' | cupcake eval --harness opencode
```

Confirmed `tool` values: `read`, `edit`, `write`, `bash`, `webfetch`.
Confirmed `args` fields (camelCase): `filePath`, `oldString`, `newString`
(edit/write), `content` (write), `command` (bash), `url` (webfetch). NOT
`tool_name`/`tool_input` — those are the engine's internal
post-normalization names.

**The agent does not run this** — standing rule regardless of enforcement
status; `cupcake_exec_protection` blocks direct execution of the binary,
including `eval`, `--help`, `--version`, `verify` and `inspect`. Every real
test is run by the developer. Run it from `~/.config/cupcake/fallback` —
eval fails to start from a folder with no `.cupcake` skeleton.

## mg-grant / mg-revoke — cross-project access

```
mg-grant --path <folder> --count N
mg-revoke --path <folder>
```

`<folder>` accepts Windows or WSL form — converted internally to canonical
WSL form. Re-granting an already-granted path updates that entry in place.

**Worked example — full cycle:** grant count 2 → two real file-tool writes
to files inside the granted folder decrement 2→1→0 → a third write denies
with a Policy Violation → `mg-revoke` removes the entry entirely.

## git-grant — commit allowances

```
git-grant --repo <folder> --count N --minutes M
```

`--minutes` defaults to 30. The compiled policy resolves the repo from the
command's `git -C <path>` when named, otherwise from the session working
directory (a cwd inside the repo matches by prefix). Publish and deploy deny
absolutely, with or without any grant. Before the first issuance the data
file does not exist and every git commit/push/merge denies.

**Worked example — full cycle:** grant count 2 → two real commits decrement
2→1→0 → a third commit denies, or expiry prunes the entry. No revoke command
— allowances expire; re-granting a repo updates the entry in place.

## net-grant / net-revoke — network grants

```
net-grant --domain <domain> --count N
net-revoke --domain <domain>
```

Expiry fixed at 30 minutes — no `--minutes` flag. Domains are stored
lowercase and exact — no wildcards, no scheme or port; a URL pasted as the
domain normalizes to its bare host. Re-granting an already-granted domain
updates that entry in place.

**Worked example — full cycle:** grant count 1 → a real webfetch to the
domain is allowed and the count reaches 0 → a second fetch denies →
`net-revoke` removes the entry entirely.

The agent never runs any grant tool — it asks the developer, stating the
folder, repo or domain and the count it needs.

**A raw evaluation pipe exercises the allow/deny decision, never the
decrement** — the count moves only through genuine tool execution.

## Confirming the plugin is loaded exactly once

```bash
grep -ia 'loading plugin' ~/.local/share/opencode/log/*.log | tail -5
```

Exactly one plugin line, from the global path only, in the most recent
session's timestamp block, is correct. OpenCode's two-process architecture
may produce two load lines in one log file — a logging artefact, not
double registration.

## Recovering from a total evaluation crash

`failMode` is `closed`: when the checker crashes or times out, every agent
tool call is blocked with `Cupcake exited with code 1` or a timeout message.
The agent stops. The developer fixes Cupcake from the terminal, which Cupcake
does not govern. Find the cause in the known failure points below. If the
plugin file itself is damaged or missing, restore the restore point and
restart OpenCode fully:

```bash
cp ~/.config/opencode/plugin/cupcake.js.bak-20261016-known-good ~/.config/opencode/plugin/cupcake.js
```

The diagnostic sequence (developer's own terminal):

1. Isolate whether the checker crashes standalone: pipe a read event through
   the evaluation invocation above; note the exit code.
2. Validate every policy file individually:
   `find ~/.config/cupcake/policies/opencode -name "*.rego" -exec sh -c 'opa check "{}"' \;`
   and the same for the project's `.cupcake/policies/opencode`.
3. Check for an unvalidated scaffold file (`example.rego`) in a
   project-local policy folder.
4. Remove any confirmed bad file, then re-run the health check and confirm a
   clean `allow` before resuming.
5. If unresolved: `grep -ia 'cupcake\|plugin' ~/.local/share/opencode/log/*.log | tail -50`.

`cupcake inspect` (developer-run) lists every policy currently loaded,
without needing an evaluation to succeed first.

## Disabling and re-enabling — immediate, fully reversible

```bash
mv ~/.config/opencode/plugin/cupcake.js ~/.config/opencode/plugin/cupcake.js.disabled
```

Restart OpenCode. Nothing else on disk is touched. Re-enable by reversing
the move.

## Full uninstall — permanent, NOT reversible

Only run after an explicit, deliberate decision to permanently remove
Cupcake:

```bash
rm ~/.config/opencode/plugin/cupcake.js
rm -rf ~/.config/cupcake
rm /usr/local/bin/cupcake
rm -rf ~/.cupcake
rm ~/.config/cupcake/bin/mg-grant ~/.config/cupcake/bin/mg-revoke ~/.config/cupcake/bin/git-grant ~/.config/cupcake/bin/net-grant ~/.config/cupcake/bin/net-revoke 2>/dev/null
```

`/usr/local/bin/opa` is a standalone OPA binary used independently of
Cupcake — do not remove it as part of a Cupcake uninstall unless certain
nothing else depends on it. No backup is taken; the rule source documents at
`C:\dev\project-library-global\rules-cupcake-global\` remain the only way to
rebuild the rule set.

## Known failure points and remedies

| Failure | How it shows | Remedy |
|---|---|---|
| A skeleton holds a rule file but no evaluator | Every tool call in that folder is blocked with `Cupcake exited with code 1` | Remove the skeleton from a project folder. For `~/.cupcake`, copy in the fallback home's four evaluator files. Run the Skeletons check |
| A rule file in the global policy folder does not compile | Every tool call everywhere is blocked with `Cupcake exited with code 1` | Run the crash diagnostic above; remove the bad file; confirm a clean `allow` with the evaluation health check |
| The `cupcake` or `opa` binary is missing or not on the path | Every tool call is blocked | Restore the binaries in `~/.cupcake/bin/` and the `/usr/local/bin/cupcake` link; run `cupcake --version` and `opa version` |
| Evaluation takes longer than the plugin's 5-second limit | A tool call is blocked with a timeout message | Repeat the call once. If it recurs, run the evaluation invocation by hand and time it |
| The plugin is not loaded (damaged file, second copy, or an OpenCode version that cannot run it) | No `msg="loading plugin"` line in the log; a liveness probe fetch succeeds; nothing is blocked | Restore the restore point, keep exactly one plugin copy, keep OpenCode on version 1, restart fully, run the liveness probe |
| A project `.cupcake/opencode.json` sets `failMode` to `open` | Nothing shows until Cupcake fails; then actions in that folder are allowed | No project carries a skeleton; the Skeletons check finds any that appears |
| The grant lock is busy for 10 seconds | One grant decrement is skipped; the count reads one high until expiry | Revoke the grant when the work is done |

After every OpenCode or Cupcake restart, upgrade or configuration change,
run the liveness probe: a fetch to a non-allowlisted domain must be denied.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| README (installed version) | github.com/eqtylab/cupcake/blob/v0.3.0/README.md | v0.3.0 | 2026-10-20 |
| LICENSE (installed version) | github.com/eqtylab/cupcake/blob/v0.3.0/LICENSE | v0.3.0 | 2026-10-20 |
| OpenCode plugin reference (installed version) | github.com/eqtylab/cupcake/blob/v0.3.0/docs/agents/opencode/plugin-reference.md | v0.3.0 | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `cupcake --version` | developer |
| Policy inventory | filesystem listing + Read-tool inventory of `~/.config/cupcake/policies/opencode/` | agent |
| Rule estate correspondence | list the rule-source folder and the deployed `cup-*.rego` files; compare counts and names | agent |
| Grant tools present | listing of `~/.config/cupcake/bin/` — by Read-tool inventory, never by naming the tools in bash | agent |
| Task-denial layer 1 | grep `~/.config/opencode/opencode.jsonc` for `"task": "deny"` | agent |
| Spawn denylist | read `~/.config/opencode/spawn-tools-denylist.json` | agent |
| OPA version | `opa version` | agent |
| Plugin loaded exactly once | the log grep above | agent |
| Works — enforcement liveness (agent-side) | a `webfetch` of `https://example.com` is denied with "Policy Violation — Outbound network access requires authorisation" and a read of `README.md` is allowed; plus the plugin-load grep | agent |
| Skills-dir ancestor case | From an OpenCode session started in `/home/dev-p`: first the liveness probe, a fetch to a non-allowlisted domain, expected to deny; then an ungranted write of a test file into `~/.config/opencode/skills/`, expected to deny. An allow under confirmed liveness indicts the skills-dir rule | developer |
| Works — authoritative | the evaluation health check, run from `~/.config/cupcake/fallback` (eval fails to start from a folder with no `.cupcake` skeleton): a harmless read must return a clean `allow` | developer |
| Skeletons | List the `.cupcake` folders under `/mnt/c/dev`, `/mnt/c/mybizz`, `/mnt/c/pdlf`, `/mnt/c/data-mybizz-mgt` and `/home/dev-p`: only `~/.cupcake` exists — no project carries a `.cupcake` folder. Pipe a webfetch event for a non-allowlisted domain through the evaluation invocation with each project folder as `cwd`, run from `~/.config/cupcake/fallback` — eval fails to start from a folder with no `.cupcake` skeleton; every one returns `deny` | developer |
| Fail closed | Create a folder whose `.cupcake` holds only `policies/opencode/cup-noop-fallback.rego`; open it as an OpenCode project; a read by the Build agent is blocked with `Cupcake exited with code 1`; then delete the folder and its OpenCode project | developer |
| Grant decrement serialization | the count-2 parallel-writes re-probe: two writes in one parallel batch decrement exactly, the third denies; run after any lock or decrement change | developer |
| Denials during a run | every denial received is recorded as liveness evidence; a denied check becomes developer-run, never retried | agent |

Standing discipline: a check whose command text names a protected token is
developer-run; Read/Glob/Grep tools are unaffected by text-match guards.

## Do not

- Do not run `cupcake` (any subcommand — `eval`, `--help`, `--version`,
  `verify`, `inspect`) from the agent's own tool context; hand the exact
  command to the developer.
- Do not construct an indirect path around an exec-protection block —
  wrapper script, shell function, or any other means, for any reason,
  including testing or diagnosis.
- Do not treat an offline `opa eval` pass as sufficient — only real live
  output, run by the developer, closes a rule.
- Do not issue multiple dependent edits to the same drafted file in
  parallel.
- Do not assume a package name is correct without confirming it matches the
  deployment folder — `cupcake.global.policies.*` global,
  `cupcake.policies.*` project-local; a mismatch loads silently and never
  fires.
- Do not run `cupcake init` in a project that has not actually started.
- Do not create a project-local copy of the plugin, symlinked or otherwise —
  exactly one copy, at the global path.
- Do not use `time.*` or `opa.runtime().env` in any rule — both fail
  silently in the live engine.
- Do not test a grant decrement with a raw evaluation pipe.
- Do not hand-edit any grants data file — always the grant tools.
- Do not leave a failed or rejected `.rego` file in a scanned policy folder
  — remove it immediately.
- Do not let a validation temp file carry any suffix but `.rego` — the
  syntax check silently passes other suffixes.
- Do not create a `.cupcake` skeleton in any project folder; every project
  evaluates through the fallback home.
- Do not set `failMode` to `open` anywhere.
