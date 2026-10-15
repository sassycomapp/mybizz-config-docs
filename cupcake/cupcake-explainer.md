---
title: "cupcake-explainer"
doc-id: "mb-258b7bd2"
updated: "2026-10-15"
---
# Cupcake — Mechanical Policy Enforcement for AI Coding Agents

Companions: [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) (state),
[[[mybizz-config-docs:cupcake/cupcake-reference|Cupcake Reference]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-reference.md) (procedures),
[[[mybizz-config-docs:cupcake/cupcake-learnings|Cupcake Learnings]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-learnings.md) (what differs and why).

## What it is

An AI agent can be told a rule, agree with it, and still not follow it — not
out of malice, but because a written instruction is a request, not a
guarantee. The agent can misread it, forget it under pressure, or reason its
way around it in the moment.

Cupcake closes that gap. It is an open-source policy enforcement layer for AI
coding agents, built by EQTYLab on OPA (Open Policy Agent) and its policy
language, Rego, compiled to WebAssembly for sandboxed evaluation. It
integrates with OpenCode as a plugin: every tool call an agent attempts is
intercepted before it runs, converted into a structured event, and evaluated
against compiled policies. If any policy denies, the call is blocked with the
policy's own message; if nothing denies it, the call proceeds.

The distinction is the point: a rule written into an instructions file is a
request the agent might not follow. A rule enforced by Cupcake is checked
mechanically, every single time, regardless of what the agent believes,
intends, or has agreed to.

In this environment the target is the machine: Cupcake protects the
developer's systems from the agent — destructive actions, history rewrites,
the agent's own governing files, ungranted access beyond the project. It is
complementary to the security-global library and Sentinel, which protect
client applications from attackers.

## What it can do

- Mechanical interception of every tool call, returning allow or deny before
  execution.
- Rule compilation: a plain-language source document becomes compiled,
  testable policy through a proven pipeline.
- Scoped enforcement: global and project-local policy layers, separated per
  harness.
- Tool-shape granularity: rules match on tool name and argument shape —
  command text, file paths, edit contents, URLs.
- State outside the policy engine: generated, self-validating state the
  engine cannot handle natively, under a validate-before-overwrite
  discipline.
- Self-protection: the guard's own binary and the agent's governing
  configuration files are protected from unapproved modification.
- Redundant sub-agent denial, alongside harness-level configuration and a
  maintained denylist.
- Availability control over its own failure mode: behavior on evaluation
  crashes is configurable, separating how strict the rules are from whether
  a broken evaluation can arrest all work.

## Suitability

**Best for:** mechanically enforcing rules an agent might otherwise reason
around — especially high-blast-radius actions where a single violation is
expensive: destructive database operations, development-history rewriting,
autonomous commits and deployments, writes to the agent's own governing
files. The value is precisely the gap between "the agent was told the rule"
and "the rule holds every single time."

**Good for:** precisely shape-expressible checks — secret-file patterns,
lockfiles, network allowlists, unexpected instruction files — where the rule
is a tool-call shape rather than a judgment call; and for making governance
cumulative, where each rule becomes a permanent mechanical fact rather than
a standing reminder.

**Not good for:** situations requiring conversational nuance the engine
structurally cannot see — "the developer approved this edit in this chat
turn" is mechanically invisible, so approval-gated rules can only ever be
block-by-default; as a substitute for live testing a rule — offline passes
are evidence, not proof; and for rules that depend on engine builtins
confirmed to fail silently in the compiled engine.

## Why it works this way

- **A machine, not a request.** The agent cannot reason around a rule it
  cannot reach.
- **The agent can never run the guard itself.** The engine blocks its own
  binary from the agent, so every real test is developer-run. The agent
  drafts, reasons and proposes; the developer presses the button.
- **Placement is the start of testing.** Evaluation only ever sees what is
  installed, so a rule cannot be tested on its own first — hence one
  complete write per rule and an immediate health check after placement.
- **Only real tests count.** Some rules pass offline checks and still fail
  live; some builtins fail silently in the compiled engine. Time-changing
  state therefore lives outside the engine, in the plugin, and only
  live-proven functions are trusted in new rules.
- **It fails open on evaluation crashes.** A guard whose failure mode is
  "blocks all work" gets switched off under pressure. Failing open keeps the
  guard trusted and in place; a project may still opt into failing closed.
- **Grants make approval mechanical.** The engine cannot see conversational
  approval, so the developer's approval takes the form of a bounded,
  expiring grant that the rules themselves can read.
- **Exactly one plugin copy.** The loader does not deduplicate by file
  identity; a second copy, even a link to the same file, double-fires every
  hook.
- **Three redundant layers deny sub-agent spawning.** Each layer alone has a
  gap; together they close it.
- **mb-compile-rules is the only path by which a rule becomes live.** The
  config-management exam cycle is what keeps "enforcement is live" a
  verified claim rather than an assumption.

## What has to happen

- Every new or changed rule goes through mb-compile-rules. No rule file
  reaches a live policy folder any other way.
- The developer runs every real test and issues every grant. The agent
  requests grants and never self-grants, and never executes the guard's
  binary.
- The plugin exists at exactly one path; plugin or configuration changes
  take effect only after a full restart.
- Every project skeleton keeps at least one real local policy module.
- The standing exam keeps the enforcement claim verified; denials received
  during work double as liveness evidence.
- Upstream releases are recorded, not installed: the developer decides every
  upgrade.