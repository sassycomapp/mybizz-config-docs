---
title: "mb-compile-rules-explainer"
doc-id: "mb-3c93f17d"
updated: "2026-10-20"
---
# mb-compile-rules — Explainer

## What it is

This skill is the writing desk of the security system. Cupcake — the
mechanical checker that stands between the AI agent and its tools — can
only enforce rules that exist as compiled policy files. This skill is how
a rule gets there: a person writes what should be blocked in plain
language, and this skill turns that intent into a real, tested,
correctly-placed enforcement file. It exists because of a gap every
security system faces: a rule the agent is *told* is a request the agent
might not follow; a rule the checker *enforces* holds every single time.
Plain language is for people; only a compiled, tested file protects.

The skill's defining property is that it refuses to confuse "written" with
"working." Nothing stays in place unless it passed real tests, run by the
developer, against the real system — and anything that fails or is
rejected is removed immediately, not left for later cleanup.

## What it can do

- **The full authoring cycle.** Read the plain-language source in full;
  convert it to an enforcement file in one complete, atomic write; check
  its syntax with the standalone checker (`opa check`); place it at its
  real location; see it through real block-case and allow-case tests; and
  apply the developer's keep-or-remove decision.
- **Safe amendment of live rules.** The same cycle, applied minimally to
  an existing rule — small diffs on proven text, a rollback backup the
  scanner can never pick up, and a full re-test.
- **Guardrails against its own failure modes.** Testing and placement
  are one action (the checker only ever evaluates what is really
  installed), a rule's internal package name must match its real
  location or it loads silently and never fires, and the compiled file
  carries exactly one `cup-` prefix while the source keeps its own name.
- **A hard boundary on who presses the button.** The agent drafts,
  checks, places, and proposes tests — but every real test command is run
  by the developer in their own terminal, by design and by standing rule.

## Suitability

- **Best for:** turning an authored rule into a proven, live enforcement
  file; amending an existing rule with minimal, fully-retested changes;
  being the *only* door through which new enforcement files enter the
  live folder.
- **Good for:** auditing the rule estate (recorded in
  [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)); re-verifying a rule after a
  system change; onboarding a new rule from a plain-language proposal.
- **Not good for:** as proof on its own — an offline syntax pass is
  evidence, not verification, and a rule can pass offline and still fail
  live; for speed at the expense of the cycle — skipping the health
  check or the real tests is how an unvalidated file reaches the live
  folder and crashes evaluation; for anything requiring judgment
  about *what* should be blocked — that is the developer's authoring
  decision, made in the plain-language source; this skill never invents
  rules.

## Why it works this way

**Why placement and testing are one action.** The checker cannot evaluate
a draft file in isolation — it only ever sees
what is actually installed. A "test first, deploy later" workflow is
therefore impossible by construction; the pipeline treats placement as the
test's beginning, with an immediate health check so a bad file is caught
in seconds.

**Why the internal name must match the folder.** A rule with the wrong
internal namespace loads without error and silently never fires — the most dangerous failure mode in a security
system: protection that appears present but does nothing. The name rule
turns that silent gap into a checked property.

**Why the developer runs every real test.** Two reasons, one practical and
one principled. Practical: the checker's own self-protection blocks the
agent from executing it — by design, so the agent can never weaken or
misuse its own guard. Principled: the agent has an interest in its test
results; the developer does not. Real output from the developer's terminal
is the only honest verdict.

**Why one single, complete write per rule.** Dependent parallel edits
land out of order and leave the live file referencing a helper the
pipeline never wrote. One single, complete write per rule makes that
failure impossible.

**Why the source keeps its own name.** The rule sources are the
developer's plain-language documents, named for their subjects; the
`cup-` prefix belongs to the compiled, enforcement side of the pipeline.
Forcing the prefix onto sources — and doubling it where a compiled name
already carried one — would break the prerequisite step for most of the
estate. The convention keeps the two sides of the pipeline
distinct: sources as written, compiled files always prefixed exactly
once.

**Why this pipeline is a supply-chain control.** The security standards
require that nothing new is trusted by default
([[[default:security-global/principles/sec-review-before-trust|Review Before Trust]]](C:/dev/project-library-global/security-global/principles/sec-review-before-trust.md)) and name third-party
skill and dependency review
([[[default:security-global/infrastructure/sec-dependency-skill-supply-chain|Dependency and Skill Supply Chain]]](C:/dev/project-library-global/security-global/infrastructure/sec-dependency-skill-supply-chain.md));
the layered check-before-trust chain is
[[[default:security-global/principles/sec-defense-in-depth|Defense in Depth]]](C:/dev/project-library-global/security-global/principles/sec-defense-in-depth.md), and the boundary on what may
touch the machine's filesystem is
[[sec-local-filesystem-access-boundary|Local Filesystem Access
Boundary]]. An enforcement file is itself a security control — an
unvalidated one entering the live folder by any other path (a careless
"add everything" save) can crash evaluation entirely. This pipeline is
the sanctioned door, and its gates are the review.

## What has to happen

- The developer invokes the skill by name, with the rule to compile, and
  decides the deployment target before drafting.
- The developer runs every real test, does the health check's
  developer-side removals, and states every keep decision.
- After any change to the canonical source, the installed copy is updated
  to stay body-identical to it — a stale installed copy silently executes
  a superseded procedure.
- Rules belong to Cupcake: the estate lives in its configuration
  ([[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md)), and every new or amended
  rule reaches the live folder only through this pipeline.
- Cupcake stays active and enforcing — standing policy; its current state
  is recorded in its own configuration.
- The developer commits with commit-all, which also syncs these documents
  into the memory system.

*Companion documents: [[mb-compile-rules-config|mb-compile-rules
Configuration]] (state), [[mb-compile-rules-reference|mb-compile-rules
Reference]] (commands and rules),
[[[mybizz-config-docs:mb-compile-rules/mb-compile-rules-learnings|mb-compile-rules Learnings]]](C:/mybizz/mybizz-config-docs/mb-compile-rules/mb-compile-rules-learnings.md) (deviations),
canonical source `C:\mybizz\mb-compile-rules\mb-compile-rules.md` (the
authoritative procedure). System context:
[[cupcake-explainer|Mechanical Policy Enforcement for AI Coding
Agents]].*
