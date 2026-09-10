---
document: "Matt Pocock Skills Explainer"
doc-id: matt-pocock-skills-explainer
state: Live
date-created: 2026-09-08
---

# Matt Pocock Skills Explainer

## 1. What this actually is

Matt Pocock's personal engineering discipline, shipped as 35 small
markdown skills for AI coding agents — the practices he uses daily for
"real engineering, not vibe coding." The set's philosophy is deliberately
the opposite of process frameworks like GSD, BMAD, or Spec-Kit: those own
the whole workflow, which makes their bugs hard to find and your control
over the work smaller. These skills are small, composable, and hackable —
each one is a discipline you can read in minutes and adapt.

In this environment the set is installed as one pinned clone whose files
OpenCode reaches through symlinks, alongside (and independent of) GStack's
workflow layer and GBrain's memory. It answers a different question than
either: not "what is the current structure" (Graphify), not "why was this
decided" (GBrain), not "what ships next" (GStack) — but "how does good
engineering judgment get applied, step by step, inside this session."

## 2. What it can do (capability level)

- **Alignment before building.** A reusable interview primitive
  ("grilling") plus four packaged forms of it, on the evidence that the
  most common failure mode is the agent building the wrong thing well.
- **A shared language.** Domain modeling that maintains `CONTEXT.md` and
  ADRs, so project jargon becomes concise, consistent, and cheap for an
  agent to use — naming, navigation, and fewer thinking tokens.
- **Feedback loops.** A red-green-refactor TDD skill and a gated
  diagnosis loop for hard bugs, both built on the principle that the rate
  of feedback is the speed limit.
- **Design care.** A shared vocabulary for deep modules and a survey skill
  that finds untangling candidates in an aging codebase — investing in
  design daily to counter AI-accelerated entropy.
- **Planning artifacts.** Conversation-to-spec, spec-to-tickets with
  blocking edges, and a wayfinder for work larger than one session —
  expressed as decision tickets on the project's issue tracker.
- **Verification and recovery.** Two-axis code review (standards + spec
  fidelity) and intent-traced merge-conflict resolution.
- **Human-only steps.** A wizard generator that turns agent-unreachable
  steps (credentials, dashboards, migrations) into interactive scripts for
  the human.
- **Productivity periphery.** Teaching, conversation handoff,
  questionnaires, re-pitching, and writing for agents.

## 3. Suitability

- **Best for:** aligning on intent before any code is written (grilling in
  all its forms); test-driven slices during implementation; architecture
  surveys and domain-model upkeep in any repo with the setup gate done;
  code review that checks both standards and spec fidelity.
- **Good for:** `-project-library` planning repos (domain docs, triage
  vocabularies); merge-conflict recovery; bootstrapping repo engineering
  hygiene (pre-commit, git guardrails); TS deep-module enforcement.
- **Not good for:** spawning sub-agents — several skills are written for a
  spawning environment, and this one denies it (execute inline per the
  reference's table); keeping the set current — upgrades are
  deliberate-decision-only by standing rule, so it will drift until you
  decide; projects without the setup gate — engineering skills will
  misfire without their tracker/labels/domain layout; replacing GStack —
  GStack owns release workflow, QA-with-browser, and deploy here; this set
  has no browser, no ship pipeline, and no deployment story.

## 4. Why it works the way it does

**Why small and composable instead of a framework.** A framework that owns
the process hides its assumptions; when it fails, you debug the framework
instead of the work. Skills that each encode one discipline stay
inspectable, adaptable, and composable — and they transfer across models,
which monolithic workflows do not.

**Why the per-project setup gate is mandatory.** The planning skills
(spec, tickets, triage, review) all read a project-specific contract —
where issues live, what triage labels mean, where domain docs go. Running
them without that contract makes the skill guess, and a guessing skill
reproduces exactly the misalignment the set exists to prevent.

**Why user-invoked vs model-invoked matters.** Orchestration skills that
fire automatically would have the agent reorganizing your work unprompted;
discipline skills that never fire automatically would never be there when
needed. The split keeps agency with you at the seams and gives the model
reusable judgment in the middle.

**Why the sub-agent denial reshapes three skills without breaking them.**
This environment keeps every agent action attributable and steerable in
one session — sub-agent spawning is denied at multiple layers, permanently
by policy. The affected skills' value (two-axis review, wayfinder research,
AFK delegation) survives the denial because their *method* — separated
concerns, recorded findings, precise handoffs — is executable inline;
only their *parallelism* is lost. The reference documents the inline
execution per skill.

**Why a pinned clone with symlink installs.** One real copy, 35 live
skills, zero drift between them — and, crucially, zero automatic updates:
the set changes only when a human decides it changes, which is the same
deliberate-decision philosophy the vendor's own "tinkerer" path espouses
and this environment extends into a standing rule.

**Why this suite supersedes the old reference.** The prior
`mybizz-os-docs` reference carried claims that failed live verification
(a browsable Windows hub path that does not exist) and predated the
current upstream drift; its verified content — install architecture,
setup gate, catalog — is merged here, and the old file is retired so the
canonical state lives in exactly one place.

*Companion documents: `matt-pocock-skills-config.md` (state),
`matt-pocock-skills-reference.md` (commands and rules).*
