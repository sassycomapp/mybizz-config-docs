---
title: "sysdoc-creator-explainer"
doc-id: "mb-1b1e5218"
---
# sysdoc-creator — Explainer

## 1. What this actually is

`mb-sysdoc-creator` is the skill that turns "document this component"
into a verified, three-document canonical suite. The developer invokes it
naming a component and supplies whatever they have — a description,
files, links — and the skill treats all of it as leads to investigate,
never as text to transcribe. The output is always the same shape: a
config document (what exists and what it's set to), a reference document
(how to execute), and an explainer (what it is, when to use it, why it
works this way) — each constrained by a permanent specification that
defines what belongs in it and, just as firmly, what does not.

It exists because this environment repeatedly found supplied source
material stale or flatly wrong — versions disagreed across three
surfaces, claimed-whitelisted paths turned out empty, vendor READMEs
contradicted the skills actually installed. In that world, a document
suite written by summarizing the supplied material would canonize the
errors. This skill's core commitment is the reverse: research first,
draft second, and nothing enters a canonical document on a source's
say-so when it could be checked live.

## 2. Feature summary

- Enforced research-before-drafting: multiple GBrain passes, direct
  file reads, and live commands before any drafting is permitted.
- A mandatory cross-cutting system check on every run — Cupcake rules,
  Memory Governor treatment, security-global principles, related skills
  and sources — with explicit "none found" reporting, so gaps are
  never silent.
- Two separate human approval gates: one on the research findings,
  one on the drafted documents. Neither can absorb the other.
- Provenance tracking per fact (confirmed-live, confirmed-via-GBrain,
  unverified-from-source, developer-stated), carried honestly into the
  drafts — open items are stated as gaps, never guessed closed.
- Single-source-of-truth enforcement through per-document stray-line
  tests, so each fact lands in exactly one of the three documents.
- Interrupt-proof state: an in-progress run park, a permanent run
  history, and a component-owned learnings file that compounds the
  skill's own research craft across runs.

## 3. Suitability

**Best for:** creating the canonical config/reference/explainer suite
for any component of this system — a tool, skill, service, or corpus —
and for rewriting an existing suite when the component's state has
moved. Every suite in `mybizz-config-docs` was produced this way.

**Good for:** retroactive corrections to live suites (the Cupcake
phrasing standardization runs), targeted additions ordered by the
developer mid-run, and pre-write verification of procedures (the
dream-cycle acceptance test that caught two broken commands before
publication).

**Not good for:** one-off documents outside the three-doc pattern
(right tool: write it directly); navigational and structural documents
that index the filesystem (right tool: mb-docs-manager); checking
existing documents against each other for drift (right tool:
mb-align-docs); converting cross-references to wikilinks (right tool:
mb-wikilinks); submitting content into governed memory (right tool:
mb-submit-memory). Also wrong for casual use: it is expensive by
design — every run does real research and demands two human gates — so
invoking it for a quick note wastes its whole apparatus.

## 4. Design reasoning

**Why research-first rather than intake-first.** The skill's value is
entirely in refusing to trust its inputs. Every durable learning in its
learnings file is a story about a source that lied: frontmatter versions
disagreeing with live CLI output, grants files disproving historical
whitelist claims, vendor URLs that moved. The phase order (research →
report → gate → draft → gate → write) is the mechanism that makes
"verified, not transcribed" structural rather than aspirational.

**Why two gates.** Research findings and drafted prose fail in different
ways: findings can be wrong or incomplete; drafts can be well-researched
but misfiled across the three documents, or drift from the specification's
never-contains lists. A single combined approval would let a bad draft
ride in on good research or force re-research over a wording fix. The
two-gate design lets the developer correct the fact base and the prose
independently — and run history shows both directions happening.

**Why the cross-cutting check is unconditional.** Component-specific
relevance judgment is exactly what produced silent gaps before the check
became mandatory: the security-global arm was checking a nonexistent path
for three runs, and the skill-index register silently lacked this very
component. Requiring all four categories every run, with explicit
"none found," converts each category into an auditable claim rather
than an omission.

**Why one fact, one home.** The three documents answer three different
questions — what is set, how to act, why it is so. A fact restated in a
second document creates a second thing that can go stale; the spec's
stray-line tests give the drafter a mechanical way to catch the drift
before the developer ever sees it. This mirrors the whole
`mybizz-config-docs` repo's founding principle.

**Where it sits.** It is the producer of most of this repo's content and
a consumer of the rest: every suite it writes becomes GBrain-indexed
corpus via the ordinary host-source sync, and every run it closes feeds
its own learnings file, which shapes the next run's research pattern. It
is the doc-producing member of the mb-* family — mb-docs-manager owns
structure and navigation, mb-align-docs owns agreement between documents,
mb-wikilinks owns cross-reference form, and this skill owns whether the
content was true when it was written.

**Open questions.** The skill-index register's missing entry (open item
in the config doc) matters because that register is the environment's
authoritative skill status list — a gap there propagates as invisibility.
The prefix divergence in this suite (`sysdoc-creator-` vs the folder's
`mb-sysdoc-creator`) is harmless but breaks the repo's otherwise uniform
folder-name-as-prefix convention; worth a decision before the next suite
copies it.
