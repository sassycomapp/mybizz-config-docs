---
title: "matt-pocock-skills-explainer"
doc-id: "mb-f1cf9f44"
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
- **A shared language.** Domain modeling that maintains [[CONTEXT|mb-3-cs (Mybizz Consulting Services)]] and
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

## 5. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[config-manager-explainer|Explainer]] — emulated from the
PostgreSQL pilot. The short local version:

- [[matt-pocock-skills-config|Matt Pocock Skills Configuration]] is the **spec** — the ideal state every exam
  checks against.
- Before each exam run, the config-manager synthesizes
  [[matt-pocock-skills-exam-plan|Exam Plan]]: a fresh job-spec built from this spec, the
  last report, the log, and the learnings. The plan is transient (the file is
  live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-matt-pocock-skills`) with the
  plan in hand — detection fully autonomous; healing gated. **This module has
  no agent-healable items**: the installation is deliberate-manual by standing
  rule; every repair/decision (upgrade, artifact cleanup, link repair) is
  developer-run or proposed.
- **Scope boundary:** the 5 Anvil skills sharing `~/.agents/skills/` belong to
  `anvil-agent-references` (coexistence presence only); GStack's install
  locations and inventory belong to `mb-config-gstack`; `spawn-tools-denylist`
  and Cupcake policy belong to the cupcake/opencode modules.
- The run rewrites [[matt-pocock-skills-exam-report|Exam Report]] (current state, no
  history), appends one row to [[matt-pocock-skills-log|Log]], files new
  learnings, and prunes absorbed entries.

## 6. S.W.O.T.

**Strengths.** Install-by-symlink from one pinned clone: 35 live skills, zero
copies, zero drift between them, and zero automatic updates (the deliberate-only
rule is mechanical); symlink topology is cheap to verify exhaustively (0 broken
links is a real, checkable claim); per-project setup gate gives a hard, visible
contract for the planning skills.

**Weaknesses.** Deliberate only-update means the set steadily falls behind
upstream (already ~1 month at last record) by design; several skills are written
for a sub-agent environment this one denies (inline-execution table is the cost
of the denial); the set's health depends on the source clone staying put — a
relocated or rewritten clone would sever all 35 symlinks at once.

**Opportunities.** The config-management exam adds standing liveness (frontmatter
sweep) and topology verification that never existed for the install; an inventory
re-count each run keeps the 35-member catalog honest against the source clone.

**Threats.** A silent `git pull` (someone else's automation) would re-pin the set
without the deliberate decision — the exam's HEAD check catches it; a shared-root
accident could delete or rename an Anvil entry while managing this set —
designated different-owner, coexistence-presence only; guard-rule changes could
reclassify which checks are agent-runnable (denials honored, reclassified
developer-run immediately).

---

*Companion documents: [[matt-pocock-skills-config|Matt Pocock Skills Configuration]] (state),
[[matt-pocock-skills-reference|Matt Pocock Skills Reference]] (commands and rules),
[[matt-pocock-skills-exam-plan|Exam Plan]] / [[matt-pocock-skills-exam-report|Exam Report]] /
[[matt-pocock-skills-log|Log]] / [[matt-pocock-skills-learnings|Learnings]]
(config-management set), [[matt-pocock-skills-skill|Matt Pocock Skills Skill]] (exam skill canonical
source). Architecture: [[config-manager-explainer|Explainer]].*
