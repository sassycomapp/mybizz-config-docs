# mb-compile-rules Explainer

## 1. What this actually is

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

## 2. What it can do (capability level)

- **The full authoring cycle.** Read the plain-language source in full;
  convert it to an enforcement file in one complete, atomic write; check
  its syntax with the standalone checker (`opa check`); place it at its
  real location; see it through real block-case and allow-case tests; and
  apply the developer's keep-or-remove decision.
- **Safe amendment of live rules.** The same cycle, applied minimally to
  an existing rule — small diffs on proven text, a rollback backup that
  the scanner can never pick up, and a full re-test. Proven end-to-end on
  2026-09-08 with the cross-folder rule's redesign (13/13 live tests).
- **Guardrails against its own failure modes.** The pipeline encodes two
  corrections learned the hard way: testing and placement are one action
  (the checker only ever evaluates what is really installed), and a
  rule's internal name must match its real location or it loads silently
  and never fires.
- **A hard boundary on who presses the button.** The agent drafts,
  checks, places, and proposes tests — but every real test command is run
  by the developer in their own terminal, by design and by standing rule.

## 3. Suitability

- **Best for:** turning an authored rule into a proven, live enforcement
  file; amending an existing rule with minimal, fully-retested changes;
  being the *only* door through which new enforcement files enter the
  live folder.
- **Good for:** auditing the rule estate (19 source documents, all
  deployed globally); re-verifying a rule after a system change; onboarding
  a new rule from a plain-language proposal.
- **Not good for:** as proof on its own — an offline syntax pass is
  evidence, not verification; several real rules passed offline and failed
  live; for speed at the expense of the cycle — skipping the health check
  or the real tests is exactly how the two live crashes and the total
  2026-09-06 outage happened; for anything requiring judgment about *what*
  should be blocked — that is the developer's authoring decision, made in
  the plain-language source; this skill never invents rules.

## 4. Why it works the way it does

**Why placement and testing are one action.** The first live use proved
the checker cannot evaluate a draft file in isolation — it only ever sees
what is actually installed. A "test first, deploy later" workflow is
therefore impossible by construction; the pipeline treats placement as the
test's beginning, with an immediate health check so a bad file is caught
in seconds.

**Why the internal name must match the folder.** The same live testing
proved a rule with the wrong internal namespace loads without error and
silently never fires — the most dangerous failure mode in a security
system: protection that appears present but does nothing. The name rule
turns that silent gap into a checked property.

**Why the developer runs every real test.** Two reasons, one practical and
one principled. Practical: the checker's own self-protection blocks the
agent from executing it — by design, so the agent can never weaken or
misuse its own guard. Principled: the agent has an interest in its test
results; the developer does not. Real output from the developer's terminal
is the only honest verdict.

**Why one single, complete write per rule.** A real crash once came from
three dependent edits landing out of order, leaving the live file
referencing a helper that was never written. Atomic writes make that
failure impossible.

**Why this pipeline is a supply-chain control.** The security standards
require that nothing new is trusted by default (`sec-review-before-trust`)
and name third-party skill and dependency review
(`sec-dependency-skill-supply-chain`). An enforcement file is itself a
security control — an unvalidated one entering the live folder by any
other path (a careless "add everything" save) was the recorded cause of
the total 2026-09-06 outage. This pipeline is the sanctioned door, and
its gates are the review.

**Open questions.** The two copies of the skill file (the installed one
and the mirror in this folder) are identical today but nothing keeps them
synced — a divergence would mean the documentation and the behavior drift
apart. Cupcake's reactivation completed the same day this suite was
written: the cross-folder rule went through this very pipeline, passed
13/13 live tests, and is now enforced — the strongest possible validation
of both the pipeline and these documents.

*Companion documents: `mb-compile-rules-config.md` (state),
`mb-compile-rules-reference.md` (commands and rules), `SKILL.md` (the
authoritative procedure). System context: `cupcake/cupcake-explainer.md`.*
