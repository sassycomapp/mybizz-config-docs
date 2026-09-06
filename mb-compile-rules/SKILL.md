---
name: mb-compile-rules
description: |
  Converts a Cupcake rule written in Markdown into a working, tested
  Rego policy file. Source: C:\dev\project-library-global\rules-cupcake-global\
  (Windows, human-readable Markdown). Destination: either
  ~/.config/cupcake/policies/opencode/ (global) or
  ./.cupcake/policies/opencode/ (project-local), chosen before drafting,
  since Cupcake's own routing requires the Rego package name to match the
  folder the file actually lives in. Corrected 2026-08-28, after live
  testing: Cupcake cannot evaluate a draft file in isolation — it only
  evaluates whatever is actually present in a real, scanned policy
  folder. Testing and placement are therefore the same action, not two
  separate steps. A file placed with the wrong package name for its
  location will load without error and silently never fire. Invoked as
  /mb-compile-rules (rule-name).
---

# mb-compile-rules

Turns a Markdown rule into a real, tested Cupcake policy. Nothing stays
in place without an explicit developer decision to keep it — a failed or
rejected placement is removed immediately, not left for cleanup later.

---

## Section 0 — Hard rules. Do not deviate.

1. **Never leave a placed file that failed its test or was rejected.**
   If either real test case produces the wrong result, or the developer
   declines to keep the rule, remove the file from disk immediately —
   see Section 2, Step 8.
2. **Never invent a test result.** Both test cases are run for real,
   against the real `cupcake eval` command, from inside a real project
   directory. A described or assumed result is not a substitute.
3. **Follow the naming convention exactly.** Every file, source and
   compiled, carries the `cup-` prefix, per the project's own naming
   standard.
4. **The Rego package name must match the real deployment location.**
   Confirmed live, 2026-08-28: a rule placed in the global folder
   (`~/.config/cupcake/policies/opencode/`) must use a package name
   starting `cupcake.global.policies.`, matching the real global
   builtins' own naming. A rule placed in a project-local folder
   (`./.cupcake/policies/opencode/`) must use `cupcake.policies.`,
   with no `global` in it, matching the real project builtins' own
   naming. A file with the wrong prefix for its location will be
   scanned and loaded by Cupcake without error, and will never actually
   fire — this was found and confirmed directly, not assumed: the same
   file, same content, produced zero denials in the project-local
   folder and a correct, real denial once moved to the global folder
   with no other change.
5. **Deployment target is decided before drafting, not after.** The
   target determines the required package name (Hard Rule 4), so it
   cannot be chosen as an afterthought once a draft already exists.

---

## User-invocable

Invoked as `/mb-compile-rules (rule-name)`, where `rule-name` identifies
a real Markdown file already present in
`C:\dev\project-library-global\rules-cupcake-global\`. The developer
supplies the rule name; this skill does not invent or guess which rule
to compile.

---

## Section 1 — Prerequisites

1. Confirm the source file exists:
   `C:\dev\project-library-global\rules-cupcake-global\cup-(rule-name).md`.
   If it does not exist, STOP and report — do not draft a rule from
   scratch on the skill's own initiative.
2. Confirm Cupcake is installed and `cupcake eval` is a real, runnable
   command in this environment. If not, STOP and report.
3. Confirm the command is actually reachable from inside a real tool
   call, not just from an interactive terminal — a PATH difference
   between the two contexts is a real, confirmed failure mode in this
   environment. If `cupcake` cannot be executed directly (for example,
   blocked by Cupcake's own `cupcake_exec_protection` builtin), do not
   attempt a workaround or ask for that protection to be weakened. STOP
   and ask the developer to run the real `cupcake eval` commands
   themselves, in their own terminal, and report the real output back.

---

## Section 2 — Cycle, per rule

### Step 1 — Read the source

Read `cup-(rule-name).md` in full. This is the real, authored intent —
work from the actual text, not a summary of it.

### Step 2 — Determine the real deployment target

Ask the developer, if not already stated: global
(`~/.config/cupcake/policies/opencode/`) or project-local
(`./.cupcake/policies/opencode/`, inside the current project). This
decision is required before Step 3, per Section 0, Hard Rule 5.

### Step 3 — Draft the `.rego` file, with the correct package name for the target

Convert the Markdown rule into a working Rego policy. The `package`
declaration must use `cupcake.global.policies.(name)` for a global
target, or `cupcake.policies.(name)` for a project-local target — per
Section 0, Hard Rule 4. Name the file `cup-(rule-name).rego`.

### Step 4 — Write two real test cases, using Cupcake's real, confirmed input schema

One action that the rule should block. One action that the rule should
allow. Both must be real, concrete, specific actions.

**Confirmed real schema, 2026-08-28 — do not use the field names from
Cupcake's own internal, post-normalization policy language
(`tool_name`, `tool_input`) as the raw test input; those are what a
policy sees internally, not what `cupcake eval` accepts on the command
line:**

```json
{
  "hook_event_name": "PreToolUse",
  "session_id": "test",
  "cwd": "(the real, current working directory)",
  "tool": "(lowercase tool name, e.g. task, read, bash)",
  "args": { "...": "tool-specific arguments" }
}
```

### Step 5 — Place the file at its real target location

This is not a preview or a draft placement — it is the file's real
location, and it is genuinely live the moment it's placed, since
Cupcake scans its policy folders directly. Tell the developer plainly
that the file now exists at its real, target path, pending the test
results in Step 6 and their own decision in Step 7.

### Step 6 — Run `cupcake eval` for real, from inside a real project directory

Run the real command against both test cases from Step 4. Capture the
real, actual output of each. Per Section 1, Prerequisite 3: if this
skill cannot execute the command directly in this environment, present
the exact commands to the developer and wait for their real output
rather than proceeding on an assumption.

- If the block-case genuinely produces a `deny` decision, and the
  allow-case genuinely produces an `allow` decision: proceed to Step 7.
- If either result is wrong: do not leave the file in place. Remove it
  (Step 8), return to Step 3, correct the draft, and repeat.

### Step 7 — Present for a real keep/remove decision

Show the developer all of it together: the original Markdown, the real,
deployed `.rego` content, its real path, and the real test results from
Step 6. Ask explicitly: keep this file at its current, real location, or
remove it.

### Step 8 — Apply the decision

On **keep**: nothing further to do — the file is already at its real,
correct, tested location from Step 5.
On **remove**, or on a failed test from Step 6: delete the file from
disk immediately. Do not leave a failed or rejected rule sitting in a
real, scanned policy folder.

---

## Section 3 — Completion status protocol

- **DONE** — the rule is tested, approved, and remains at its real,
  correct location.
- **BLOCKED** — the source file doesn't exist, `cupcake eval` isn't
  available, or it cannot be run directly by this skill and the
  developer has not yet supplied real output; state exactly which.
- **TEST_FAILED** — the deployed `.rego` did not produce the correct
  result on one or both test cases; the file has been removed per
  Section 2, Step 8; report the real output and stop for developer
  input before redrafting.
- **REJECTED** — the developer declined to keep the rule after a
  passing test; the file has been removed per Section 2, Step 8.

Never mark a rule DONE without Step 6's two real test results both
having passed, from the file's actual, real, final location, and
without Step 7's explicit keep decision having actually been given.
