---
title: "config-manager-explainer"
doc-id: "mb-c28cb8f9"
updated: "2026-10-14"
---
# mb-config-manager — Explainer

## What it is

mb-config-manager is the agent that keeps every MyBizz skill and system configured
to its standard. The estate this machine runs — skills, plugins, scripts,
applications, services — degrades quietly: a value drifts, a version falls behind,
a file disappears. The developer's attention is on building, not on watching
configs. This agent watches instead: invoked on demand, it examines one system's
live state against its recorded configuration, reports what differs, and changes
only what the developer approves. It is an OpenCode agent invoked through
`/mb-config-manager`, installed at `~/.config/opencode/agents/mb-config-manager.md`
with a command wrapper beside it.

## What it can do

- Examine one named system end to end: learnings, config, reference, register row,
  folder contents, installed version, live values, and a works-check.
- Report findings in six kinds — DOWN, UNHEALTHY, BEHIND, DRIFT, DEVIATION, GAP —
  each with evidence, proposed correction and justification.
- Propose register rows for systems that lack one, and refresh the examined
  system's row.
- Route work it must not do itself: issuer research and suite writing go to
  mb-sysdoc-creator; Cupcake rule changes go to mb-compile-rules.
- Maintain its own register, which includes every system — itself included.

## Suitability

Best for: gated, evidence-based correction of any system's configuration health;
the standing answer to "is X still configured to its standard?".

Good for: catching silent failure early, before it compounds.

Not good for: writing or refreshing documentation suites (mb-sysdoc-creator),
writing policy rules (mb-compile-rules), performing upgrades (the developer runs
every upgrade), or committing (the developer runs commit-all).

## Why it works this way

- **An agent, not a skill.** Every finding waits for the developer's decision, so
  the work is a conversation; a primary agent holds that conversation.
- **It holds nothing about its subjects.** Every value, source and check is read
  fresh from the system's folder each run. Memory of a system becomes stale
  authority; the folder is the truth.
- **Findings live in chat; the register is the only record.** Reports on disk
  would become a second, competing state. Chat carries the decision; the register
  row carries the outcome.
- **One change at a time, with the replaced value recorded.** A failed check must
  always leave a way back.
- **Blocks stop the run.** A guard denial is never retried, never reshaped, never
  worked around; the developer gets the exact grant line instead.
- **It counts itself.** The register includes mb-config-manager; exempting it
  would create an unwatched watcher.

## What has to happen

- The developer invokes it when a check is due and decides each finding.
- mb-sysdoc-creator keeps every suite's four documents current, so the config
  this agent reads stays the standard.
- mb-doc-check checks every document at every commit; the developer commits all
  repositories with commit-all.
- Learnings stay current: a rejected finding the developer wants kept, and every
  rebuild decision, becomes an entry.
