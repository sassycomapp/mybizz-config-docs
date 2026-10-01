---
title: "matt-pocock-skills-reference"
doc-id: "mb-f0c79098"
updated: "2026-10-01"
---
# Matt Pocock Skills Reference

Execution reference for the 35 installed Matt Pocock skills. Current state
values: [[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-config|Matt Pocock Skills Configuration]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-config.md). Why the set is built this way:
[[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-explainer|Matt Pocock Skills Explainer]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-explainer.md). Config-management set:
[[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-exam-plan.md) (transient job-spec — read second, every
run), [[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-exam-report.md) (last verified state),
[[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-log|Log]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-log.md) (chronological events),
[[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-learnings.md) (transient knowledge). Agent-facing.

## Standing rules

- **No sub-agent spawning, ever.** The environment denies the Task/spawn
  tool family (`task`, `delegate`, `call_omo_agent`,
  `agent_session_create`) — denied natively in OpenCode config, denied by
  the Cupcake rule `cup-block-task-tool.rego` whenever enforcement is
  active (live status: [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md), Current Operational Status),
  and listed in `spawn-tools-denylist.json`. Do not retry under another
  name.
- **No upgrades.** Updates/upgrades of this skill set happen by deliberate
  developer decision only (standing rule, 2026-09-08). Do not pull, update,
  or reinstall the source clone unprompted.

## Mandatory per-project setup gate

`/setup-matt-pocock-skills` must have been run in a project before any other
engineering skill from this set is used there — [[[makepdlf-project-library:stepwise/step-19-to-tickets|Step 19 to Tickets]]](C:/dev/dev-makepdlf/makepdlf-project-library/stepwise/step-19-to-tickets.md), `to-spec`,
`triage`, and `code-review` depend on its output. Check:

```bash
ls <project-path>/agents/
```

All four files present (`agents/domain.md`, `agents/instructions.md`,
`agents/issue-tracker.md`, `agents/triage-labels.md`) = configured. Missing
or incomplete = run `/setup-matt-pocock-skills` in that project first.
Current per-project state: [[[mybizz-config-docs:matt-pocock-skills/matt-pocock-skills-config|Matt Pocock Skills Configuration]]](C:/mybizz/mybizz-config-docs/matt-pocock-skills/matt-pocock-skills-config.md).

## Invocation

- Skills are bare-name slash commands (`/grill-me`, `/tdd`, `/triage`) —
  OpenCode reads `~/.agents/skills/` directly; no registration step.
- Verify reachability: `head -5 ~/.agents/skills/<skill-name>/SKILL.md`
  (must show real `name:`/`description:` frontmatter). If the file exists
  but the command fails, check the symlink: `ls -la ~/.agents/skills/<skill-name>`.

## User-invoked vs model-invoked

Per upstream's own split: **user-invoked** skills run only when typed —
they orchestrate. **Model-invoked** skills may also be reached for
automatically when the task fits — they hold reusable discipline. A
user-invoked skill may invoke model-invoked ones, never another
user-invoked one.

## Engineering (18)

| Command | Type | What it does |
|---|---|---|
| `/ask-matt` | user | Router over this set — asks which skill or flow fits your situation. |
| `/grill-with-docs` | user | Grilling session that also builds the project's domain model, updating [[[mb-3-cs-project-library:docs-local/context\|mb-3-cs (Mybizz Consulting Services)]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/CONTEXT.md) and ADRs inline. |
| `/triage` | user | Move issues through a state machine of triage roles. |
| `/improve-codebase-architecture` | user | Scan a codebase for deepening opportunities, present an HTML report, grill through the pick. |
| `/setup-matt-pocock-skills` | user | One-time per-repo config (issue tracker, triage labels, domain doc layout). |
| `/to-spec` | user | Turn the current conversation into a spec and publish to the issue tracker. |
| `/to-tickets` | user | Break a plan/spec/conversation into tracer-bullet tickets with blocking edges. |
| `/implement` | user | Build the work a spec or tickets describe, driving `/tdd` at pre-agreed seams, closing with `/code-review`. |
| `/wayfinder` | user | Plan work larger than one session as a shared map of decision tickets; resolve one at a time. |
| `/prototype` | model | Throwaway prototype to answer a design question. |
| `/diagnosing-bugs` | model | Disciplined diagnosis loop: red feedback loop → minimise → hypothesise → instrument → fix → regression-test. |
| `/research` | model | Investigate against high-trust primary sources; capture findings as a cited Markdown file. |
| `/tdd` | model | Red-green-refactor TDD, one vertical slice at a time. |
| `/domain-modeling` | model | Build/sharpen the domain model: glossary challenges, edge-case stress tests, [[[mb-3-cs-project-library:docs-local/context\|mb-3-cs (Mybizz Consulting Services)]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/CONTEXT.md)/ADR updates. |
| `/codebase-design` | model | Deep-module design vocabulary: behaviour behind small interfaces at clean seams. |
| `/code-review` | model | Two-axis review since a fixed point: Standards + Spec. |
| `/resolving-merge-conflicts` | model | Resolve merge/rebase conflicts hunk by hunk, by intent; never `--abort`. |
| `/wizard` | model | Generate an interactive bash wizard for human-only steps (credentials, dashboards, migrations). |

## Productivity (7)

| Command | Type | What it does |
|---|---|---|
| `/grill-me` | user | Relentless interview about a plan or design until every branch is resolved. |
| `/handoff` | user | Compact the conversation into a handoff document for another agent. |
| `/teach` | user | Teach a concept over multiple sessions, using the directory as stateful workspace. |
| `/to-questionnaire` | user | Turn an unanswerable decision into a Markdown questionnaire for the one person who can answer. |
| `/wait-what` | user | Re-pitch a message that didn't land, with missing context, in [[[mb-3-cs-project-library:docs-local/context\|mb-3-cs (Mybizz Consulting Services)]]](C:/dev/dev-mb-3-cs/mb-3-cs-project-library/docs-local/CONTEXT.md) vocabulary. |
| `/grilling` | model | The reusable interview primitive behind grill-me / grill-with-docs / triage / wayfinder. |
| `/writing-for-agents` | model | Writing documents for agents: skills, AGENTS.md/CLAUDE.md, pointer-reachable docs. |

## In-progress (6)

| Command | What it does |
|---|---|
| `/claude-handoff` | Hand the conversation to a fresh background agent that picks up immediately. |
| `/loop-me` | Grill about specs for workflows to build, within the workspace. |
| `/setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo for deep-module enforcement. |
| `/writing-beats` | Assemble raw material into a journey of beats. |
| `/writing-fragments` | Mine raw fragments; no structure yet. |
| `/writing-shape` | Shape raw material into an article, paragraph by paragraph. |

## Misc (4)

| Command | What it does |
|---|---|
| `/git-guardrails-claude-code` | Set up hooks blocking dangerous git operations in Claude Code. |
| `/migrate-to-shoehorn` | Migrate `as` type assertions to @total-typescript/shoehorn. |
| `/scaffold-exercises` | Create exercise directory structures that pass linting. |
| `/setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged, type checking, tests. |

## Executing sub-agent-referencing skills in this environment

Three skills write sub-agent instructions that cannot run as written here
(the standing rule above). Execute them inline instead:

| Skill | Written as | Execute instead |
|---|---|---|
| `/code-review` | Standards + Spec reviews as parallel sub-agents | Run both axes sequentially in one context, keeping the two findings sets clearly separated, then aggregate |
| `/wayfinder` | Research tickets resolved by `/research` subagents | Resolve research tickets inline, in-session, one at a time; record findings on the ticket |
| `/ask-matt` | AFK work "sent to a subagent" | Do the work in-session, or hand the developer a precise checklist for genuine AFK work |

## Do not

- Do not spawn sub-agents — denied at multiple layers; execute inline per
  the table above.
- Do not upgrade, pull, or reinstall the source clone without a deliberate
  developer decision (standing rule).
- Do not use any engineering skill in a project that has not been through
  `/setup-matt-pocock-skills`.
- Do not use GStack's skill inventory for this set (separate discovery
  paths) — and do not confuse Matt's `/handoff` with a GStack command
  (GStack has none).
- Do not delete the shared `~/.agents/skills/` entries for Anvil's five
  skills while managing this set — different owner, same root.
