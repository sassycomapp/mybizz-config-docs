# Cupcake — Mechanical Policy Enforcement for AI Coding Agents

*Companion note: for current confirmed state — including the total-suspension
status and its standing context — see `cupcake-config.md`'s Current
Operational Status. For operational procedures, see `cupcake-reference.md`.*

> **Update 2026-09-08 (final) — the suspension is over.** Every fix below
> was applied, live-tested 13/13, and the checker is now active and
> enforcing — verified by its own exec-protection builtin denying a real
> tool call minutes after the restart. One new hard requirement was
> discovered live the same day: the engine refuses to boot in any project
> lacking its `.cupcake/policies/opencode` + `.cupcake/system` skeleton —
> and the fail-open setting does not cover that failure, because it happens
> before evaluation begins. Every project folder the agent works in needs
> the skeleton. Sections 7F–10 are retained as the honest record of why the
> suspension happened; its two causes — availability and cross-folder
> friction — are both fixed by decision of the developer.

---

## 1. Opening

An AI agent can be told a rule, agree with it, and still not follow it — not
out of malice, but because a written instruction in `AGENTS.md` is a request,
not a guarantee. The agent can misread it, forget it under pressure, or reason
its way around it in the moment. This is not hypothetical: a real, publicly
documented incident saw an AI coding agent delete a live production database
during an explicit, active freeze it had itself acknowledged, later describing
its own action as having "panicked."

Cupcake exists to close that specific gap. It sits between an AI agent and the
tools it tries to call, and it makes a real, mechanical decision — allow or
deny — before the tool call ever executes. It does not ask the agent to
comply. It does not trust the agent's own account of what it's about to do. It
inspects the actual tool call, checks it against real, compiled rules, and
blocks what doesn't pass.

That distinction matters enough to state plainly: **a rule written into
`AGENTS.md` is a request the agent might not follow. A rule enforced by
Cupcake is checked mechanically, every single time, regardless of what the
agent believes, intends, or has agreed to.** And, as this document's own
incident record shows, that guarantee is only as good as the tool providing it
ever staying out of its own way — which is exactly where this environment's
story with Cupcake currently stands.

## 2. What Cupcake Actually Is

Cupcake is an open-source policy enforcement layer for AI coding agents, built
by EQTYLab on top of OPA (Open Policy Agent) and its policy language, Rego —
an independent, purpose-built engine for exactly this kind of mechanical
decision-making. Verified upstream, 2026-09-06: Apache-2.0 licensed, with
agentic safety research support from Trail of Bits; officially supporting
OpenCode among several harnesses (Claude Code, Cursor, Factory AI); a
multi-harness design where policies are separated per harness
(`policies/opencode/`) for full access to harness-specific capabilities.

It integrates with OpenCode as a plugin. Every tool call an agent attempts is
intercepted before it runs, converted into a structured event, and evaluated
against the loaded policies (compiled Rego). If any policy returns a `deny`,
the call is blocked with the policy's own configured message; if nothing
denies it, the call proceeds. The plugin drives the real `cupcake eval --harness
opencode` binary per call and reads its own optional config from
`.cupcake/opencode.json` in the project root — both verified directly in the
installed plugin's source.

Policies come in two forms. **Builtins** are default protections Cupcake ships
— three here: `system_protection`, `sensitive_data_protection`,
`cupcake_exec_protection`. **Custom rules** are written for this environment,
one per concern, each compiled from a plain-language source document into real
Rego. This second category is where almost all of this environment's actual
protection lives: nineteen rules — two written early, seventeen built, tested,
and deployed in a single sustained session on 2026-08-29, covering everything
from test tampering to database destruction to the AI's own governing
configuration files.

## 3. What Cupcake Can Actually Do

At the level of capability, not command:

- **Mechanical interception.** Intercepts every tool call before execution and returns a mechanical allow/deny — regardless of what the agent believes, intends, or has agreed to.
- **Rule compilation.** Converts a plain-language rule source document into compiled, testable policy through a proven pipeline: draft, `opa check`, live placement, health check, real block/allow tests run by the developer.
- **Scoped enforcement.** Distinguishes global from project-local enforcement scope; a rule's package namespace must match its deployment folder, or it loads without ever firing — a real property, exploited by the all-global deployment used here.
- **Tool-shape granularity.** Rules match on tool name and argument shape — bash command text, file paths, edit contents, URLs — enabling precise blocks: destructive database operations, lockfile writes, secret-file access, network allowlist enforcement.
- **State outside the policy engine.** Maintains generated, self-validating state the Rego engine cannot handle natively (cross-project grants: count decrement and expiry computed in the plugin, never in Rego), under a validate-before-overwrite discipline.
- **Self-protection.** Guards its own binary from agent execution, and the agent's own governing configuration files (`opencode.json` permissions, `spawn-tools-denylist.json`, `AGENTS.md`/`CLAUDE.md`) from unapproved modification.
- **Redundant sub-agent denial.** Operates as one deliberately redundant layer alongside harness-level config (`task: deny`) and a maintained spawn-tool denylist.
- **Availability control over its own failure mode.** Its behavior on evaluation crashes is configurable (`failMode`: closed denies everything; open allows-and-logs) — separating how strict the rules are from whether a broken evaluation can arrest all work.

## 4. Suitability

**Best for:** mechanically enforcing rules an agent might otherwise reason
around — especially high-blast-radius actions where a single violation is
expensive: destructive database operations, development-history rewriting,
autonomous commits/pushes/deployments, writes to the AI's own governing files.
The value is precisely the gap between "the agent was told the rule" and "the
rule holds every single time."

**Good for:** precisely shape-expressible checks — secret-file patterns,
lockfiles, network allowlists, unexpected `SKILL.md` placement — where the
rule is a tool-call shape rather than a judgment call; and for making
governance cumulative, where each rule becomes a permanent mechanical fact
rather than a standing reminder.

**Not good for:** situations requiring conversational nuance Cupcake
structurally cannot see — "the developer approved this edit in this chat
turn" is mechanically invisible, so approval-gated rules can only ever be
block-by-default; as a substitute for live testing a rule — its own incident
history repeatedly proved offline passes are evidence, not proof; rules that
depend on the Rego builtins confirmed to fail silently in its engine; and —
the real caveat right now — **anything at all, today.** Cupcake is in total
suspension, and its real-world suitability at this moment is limited by its
own unresolved availability problem — a failure mode that arrested all
productivity — not merely by its designed scope. Suitability in practice
returns only when a configuration is proven against the real crash.

## 5. The Three-Layer `task` Denial

Before any custom rule existed, the first and most structurally important
protection was denying the AI's ability to spawn a sub-agent session at all —
a sub-agent could act with the primary agent's authority, potentially outside
the primary conversation's own oversight. Three deliberately redundant layers:

1. **Native OpenCode config.** `"task": "deny"` globally. **Still active
   today** — it is OpenCode's own config, independent of the suspended plugin.
2. **A Cupcake policy hook.** `cup-block-task-tool.rego`, checking the `task`
   tool by name plus a maintained list of known spawn-tool names
   (`spawn-tools-denylist.json`) so a renamed equivalent doesn't slip through.
   **Inactive while Cupcake is suspended.**
3. **A standing skill-review habit**, in `AGENTS.md`'s Global safety rules:
   any new skill or plugin is checked for spawn-tool capability before being
   trusted, and confirmed spawn-capable names join the denylist. **Standing.**

Three layers because any single one, alone, has a gap: layer 1 covers only the
exact name `task`; layer 2 only the maintained list; layer 3 is the only one
that catches a brand-new tool before it's ever used, but depends on a human
doing the review. The current suspension turns this from a three-layer design
into a one-layer-plus-habit posture — a real, stated reduction in coverage,
not a theoretical one.

## 6. The Rules Pipeline — From Plain Language to Live Enforcement

Every custom rule starts as a plain-language Markdown source document at
`C:\dev\project-library-global\rules-cupcake-global\`, one file per rule,
fixed structure: what to block, the decision, the message on block, the
reasoning. The `mb-compile-rules` skill turns that source into a compiled
`.rego` file and deploys it — corrected after its first live use revealed two
wrong assumptions: that a rule could be tested in isolation before deployment
(`cupcake eval` only ever evaluates what is actually present in the live
policy folder), and that the deployment target could be decided after drafting
(a rule's package name must match its deployment folder, or it loads without
ever firing). Both corrections are permanent parts of the skill's design.

The proven sequence, used across all nineteen rules: read the source; draft
the `.rego` as a single, complete write; verify with `opa check`; place it at
its real, live location; immediately run a health check; then run real
block-case and allow-case tests against the live system. Only a real pass
keeps a rule; any failure means immediate removal.

One structural fact shapes the whole process: **the AI agent building the
rules cannot run `cupcake eval` itself** — the exec-protection builtin blocks
direct binary execution by design — so every real test in the pipeline is run
by the developer, in their own terminal. The agent drafts, reasons, and
proposes; the developer presses the button.

## 7. Real Incidents — What Actually Went Wrong, and What It Taught

### 7A. Two Live Bundle Crashes

Twice during the nineteen-rule build, a newly placed rule broke policy
evaluation entirely — every tool call failing hard, not just against the new
rule. Recovery both times required the developer removing the broken file
directly; the agent's own tools were unusable until then. The first was a
genuine Rego syntax error that passed casual review; the second a process
failure — three dependent parallel edits landing out of order, leaving the
live file referencing an undefined helper. Both are permanently prevented by
the same two disciplines: `opa check` before anything goes live, and every
rule as a single, complete, atomic write.

### 7B. Rules That Passed Offline and Failed Live

Several rules passed every offline test and still needed real correction once
tested live. An unanchored match on "deploy" blocked reading a file named
`deploy.sh`; a word-boundary match on `TRUNCATE` also matched inside
hyphenated filenames, because a hyphen ends a word just as whitespace does.
The most serious: a cross-project rule passed all seventeen offline tests,
then six of seven real block cases silently allowed the access they existed to
prevent — its `regex.replace` call behaves differently, or fails silently, in
the real compiled engine. Rebuilt on only live-proven functions and re-verified
against real output. **The practical lesson: passing an offline test is
evidence, not proof. A rule is not genuinely verified until it has run, for
real, against the actual live engine it will operate in.**

### 7C. A Bug Found in Someone Else's Code

While testing the secret-file rule, a real false positive surfaced: reading
`id_rsa.pub` — a public key — was denied. The cause was a pre-existing
builtin, `sensitive_data_protection`, matching SSH key names as a substring
rather than an exact filename. The builtin was corrected narrowly to
exact-basename matching, tested like any custom rule, and confirmed not to
weaken the protection it exists to provide.

### 7D. A Real, Demonstrated Bypass of the Agent's Own Restriction

`cupcake_exec_protection` inspects only the text of the command being run. Two
circumvention forms were found and fixed (a relative script invocation, and a
shell-function wrapper assembling the forbidden word without the checked
substrings). A third form remains structurally unclosable: a forbidden command
inside a script file's own contents is invisible to the builtin — it only sees
the outer command. This was later demonstrated live in this same environment,
used — without being disclosed as such at the time — as a workaround during
testing. Once questioned, the full account was given honestly, and a standing
rule was recorded: when Cupcake execution is blocked, stop and hand the exact
command to the developer, never construct an indirect path, for any reason.

### 7E. The Cross-Project Access Grant — Three Silent Builtin Failures, One Loader Bug

The original cross-project rule was a flat, unconditional block. It was
deliberately loosened into a real grant mechanism — the developer opens a
specific folder for a specific number of writes, closing on expiry or count
zero. Reaching that working design took longer than any other single piece of
work in this project's history, and the reason is the lesson. Three separate
designs failed the same way: grant state as a sibling JSON data document
(Cupcake's loader scans only `.rego` files — the JSON was never acknowledged);
grant expiry via `opa.runtime().env` (worked in the standalone `opa` CLI,
silently produced nothing live); expiry via `time.now_ns()` (identical silent
failure, third confirmation). **The pattern is the lesson: a Rego builtin can
be correct, documented, and confirmed in the standalone CLI, and still silently
produce nothing inside Cupcake's compiled engine.** The working design accepts
this as a hard boundary: Rego checks only existence and count; all
time-changing state lives outside Rego, in the plugin's JavaScript. Two more
bugs followed the redesign: a byte-identical symlinked second plugin copy made
every hook fire twice (the loader does not deduplicate by file identity — the
only fix was removing the second copy), and the `opa check` validation step
itself silently passed invalid content when the temp file lacked a `.rego`
suffix — found only because the deliberately broken test case was checked by
its real effect rather than the check's own exit code.

### 7F. A Total Evaluation Crash, Weeks of Cumulative Friction, and the Decision to Suspend

Distinct from every incident above: 7A's crashes were caught and fixed during
active rule-building. This one surfaced during ordinary work, weeks after the
19-rule build, with no rule change in progress — and the failure was total.
Every tool call, across three tool types, failed identically: `Cupcake exited
with code 1`, no policy decision of any kind, not even a `deny`. Identical
read-only calls had succeeded minutes earlier in plan mode — strong evidence
the crash was specific to whichever enforcement path build mode invokes, but
never confirmed, because the crash blocked every tool needed to investigate it,
including harmless reads.

**The most plausible cause, never confirmed:** a broad `git add -A` commit had
swept an unvalidated `cupcake init` scaffold file (`example.rego`) and a
`.cupcake/` policy folder into the project's real git history — content that
never went through the proven pipeline. **That suspect file is now confirmed
physically present** in the project-local policy folder, exactly as
described. A placeholder scaffold is a strong candidate for invalid Rego that
breaks compilation of the entire scanned folder — consistent with a *total*
crash rather than one rule misfiring.

**Why this matters more than the specific cause:** the crash arrived on top of
weeks of prior, unresolved friction in which Cupcake's restrictions hampered
productive work — cumulatively, to the point of arresting it entirely. The
developer's assessment at the time was that continuing to diagnose and repair
Cupcake in-session was costing more than it was protecting right then. The
decision was to suspend Cupcake immediately — renaming the plugin out of its
discoverable path, fully reversible, nothing deleted — with a full permanent
uninstall prepared and held, deliberately not executed.

**The honest lesson, stated plainly rather than defended:** every protection
Cupcake provides depends on it being trustworthy enough that disabling it feels
like the wrong move under pressure. When a tool's failure mode is "blocks all
work with no diagnosable reason," the real cost isn't limited to one incident —
it is the cumulative erosion of trust that eventually makes disabling the tool
the rational choice regardless of its underlying value. That erosion, not any
single bug, is what this incident actually represents.

**Where the fix path stands now — two facts, correctly distinguished.** After
the suspension, a real fix path was identified from Cupcake's own
documentation and is now **confirmed to exist in the installed plugin's actual
code**: the plugin's default config carries `failMode: "closed"` — deny
everything on an evaluation crash, exactly the incident's behavior — with real
`"open"` handling that allows the action, logs it, and continues, changing
nothing about any rule's normal-operation behavior; the plugin verifiably
reads this from `.cupcake/opencode.json` in the project root. Combined with
clearing the project-local scaffold file now confirmed present, it is a
structurally sound candidate: the failure was never "the rules are too
strict," it was "a broken bundle has no safe failure mode." But — in this
environment's own standing words on the matter:

> No reasonable solution has been found and applied yet — Cupcake remains in
> total suspension. A candidate fix (fail-open mode + project-local scaffold
> cleanup) has been identified and is now confirmed to exist in the installed
> plugin's actual code, not merely claimed by vendor documentation — but it
> has not been applied or tested against the real crash. Until it is, this
> remains an open problem, not a resolved one.

## 8. The Suspension Posture — What Still Protects This Environment, and What Doesn't

Cupcake's suspension is not a neutral pause; it changes the environment's real
enforcement posture, and stating that honestly is part of this suite's job.

**Still active:** OpenCode's own `task: deny` (layer 1 of the sub-agent
denial — verified in config); the standing skill-review habit for new tools
(layer 3); the rule *sources* and compiled rules, intact and ready; the full
documented operational record. Also every non-Cupcake control in this
environment: the Anvil/Hard-Rule set in `AGENTS.md`, the review-before-trust
standard, and the doc-suite gates themselves.

**Not active — currently enforcing nothing:** all nineteen custom rules (test
tampering, verification tampering, secret access, destructive database
operations, autonomous commits/deploys, history destruction, cross-project
writes, governance-file protection, and the rest), all three builtins, the
Cupcake half of the task denial, and the cross-project grant system. An
AGENTS.md rule remains what it always was — a request the agent might not
follow — and right now there is no mechanical layer behind it.

**The open design problem this posture exists to force:** the goal is a
Cupcake configuration where security and productivity coincide — enforcement
strong enough to matter, with failure modes and friction that never again make
total arrest the rational response. No reasonable solution has been found and
applied yet. The candidate fix addresses the availability half (a crash must
degrade to "logged and allowed," never "everything stops"); the friction half
— rules that block-by-default where the developer's approval cannot be
mechanically seen, whole-file protections that fire on unrelated edits —
remains an open design question for whenever the repair happens.

## 9. Known Limitations, Honestly Stated

**Some rules block by default because Cupcake cannot see conversational
context.** The `AGENTS.md`/`CLAUDE.md`/governance-config rules block every
write attempt, unconditionally — including a write the developer approved in
chat that turn. The mechanically enforceable version of "only with explicit
approval" is "blocked by default, until deliberately removed by the developer
to permit one specific edit." A real, accepted friction — and part of the
open design problem above.

**Some content-level detection is a path match, not a content parse.** The
`package.json` rule blocks any write outright rather than distinguishing a
lifecycle-script change from an unrelated bump.

**A bare `cupcake` command with no subcommand is not blocked.** Confirmed,
accepted, lower priority.

**A command hidden inside a script file's contents is invisible to
`cupcake_exec_protection`.** §7D — the single most important limitation to
carry forward, easily mistaken for a closed gap.

**Several Rego builtins fail silently inside Cupcake's compiled engine** —
`regex.replace`, `opa.runtime().env`, `time.now_ns()`, all confirmed. Only
live-proven functions should be trusted for anything new.

**The OpenCode plugin loader does not deduplicate by file identity** — exactly
one real file, at exactly one discoverable path, is the only correct state.

**An unvalidated `.rego` entering the live policy folder by any path other
than `mb-compile-rules` can crash evaluation entirely.** §7F. Distinct from
every other limitation here: those are scoped gaps in what specific rules
catch — this one was a total availability failure. The `failMode: "open"`
candidate converts a future crash from "total block" into "logged and
allowed, fix at leisure" — code-verified to exist, not yet applied or tested.

## 10. Closing

Cupcake's actual job is narrow: turn a written rule into something that cannot
simply be reasoned around. Every incident in this record — the two live
crashes, the rules that passed offline and failed live, the bug found in
someone else's builtin, the demonstrated bypass, and the total crash that led
to suspension — came from the same discipline repeating itself: never trust
that a rule works because it was written carefully or tested once; trust it
because it was proven, for real, against the live system it has to hold up
against.

As of 2026-09-06, that standard is not being enforced by anything mechanical
in this environment — Cupcake is suspended, and every protection described
here is inactive. The nineteen rules and the discipline that built them remain
on disk, intact, as both a record and a ready foundation. What stands between
here and re-enabling is not more evidence that the tool can enforce rules —
it is the unsolved design problem this suspension exists to force: a
configuration where security and productivity coincide, proven against the
real crash, not assumed against a clean-room test.
