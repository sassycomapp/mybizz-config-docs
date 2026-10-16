---
title: "sysdoc-creator-explainer"
doc-id: "mb-1b1e5218"
updated: "2026-10-16"
---
# sysdoc-creator — Explainer

Companion to [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-config.md) (the state) and
[[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-reference.md) (the execution form). This suite is
examined by mb-config-manager through the register cycle
([[[mybizz-config-docs:mb-config-manager/config-manager-agent|config-manager agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md)) — the examination verifies this
suite's state and never runs the subject skill itself.

## What it is

`mb-sysdoc-creator` is the skill that turns "document this system" into a
verified, four-document canonical suite: a config (what exists and what it is
set to), a reference (how to execute), an explainer (what it is, whether to use
it, why it works this way), and a learnings file (what differs from the standard
here, and why). The developer — or mb-config-manager — invokes it naming a
system and supplies whatever they have; the skill treats all of it as leads to
investigate, never as text to transcribe. It is a prose procedure with no
executable code and no runtime dependencies, in two modes: Create for a system
with no suite, Refresh for a system whose folder already holds documents —
refreshed row by row, an existing document rewritten whole only when it
must be restructured to the specification.

It exists because this environment repeatedly finds supplied source material
stale or flatly wrong — versions disagree across surfaces, claimed permissions
turn out expired, vendor READMEs contradict the skills actually installed. A
suite written by summarizing supplied material would canonize the errors. This
skill's core commitment is the reverse: research first, draft second, and
nothing enters a canonical document on a source's say-so when it could be
checked live.

## What it can do

- Enforced research-before-drafting: issuer and version identification,
  authoritative sources, live verification of every verifiable value, and
  multiple GBrain passes before any drafting is permitted.
- An unconditional cross-system check on every run — Cupcake rules, Memory
  Governor treatment, security-global principles, related skills and sources —
  with explicit "none found" reporting, so gaps are never silent.
- Two separate human approval gates: one on the findings, one on the drafts.
  Neither can absorb the other.
- Provenance tracking per fact (confirmed live, confirmed via GBrain,
  unverified from a source, developer-stated) — unverified items surface as
  open items, never guessed closed.
- Single-source-of-truth enforcement through per-document placement tests, so
  each fact lands in exactly one of the four documents.
- A learnings file that compounds the skill's own documentation craft across
  runs, read in full before any research.

## Suitability

**Best for:** creating the canonical four-document suite for any component of
this system — a tool, skill, service, or corpus — and for refreshing an
existing suite when the component's state has moved. Every suite in
`mybizz-config-docs` was produced this way.

**Good for:** targeted corrections to live suites ordered by the developer,
pre-write verification of procedures, and folding a live event into a suite as
its worked example.

**Not good for:** one-off documents outside the four-document pattern (right
tool: write it directly); converting cross-references into resolvable links
([[[mybizz-config-docs:mb-doc-check/doc-check-explainer|mb-doc-check]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-explainer.md) writes every link in the stored form at
every commit); submitting content into governed memory (right tool:
mb-submit-memory); examining whether a suite is still true (right tool:
mb-config-manager). Also wrong for casual use: it is expensive by design —
every run does real research and demands two human gates — so invoking it for a
quick note wastes its whole apparatus.

## Why it works this way

**Why research-first rather than intake-first.** The skill's value is entirely
in refusing to trust its inputs. Supplied material is a lead, never ground
truth; the phase order (research → report → gate → draft → gate → write) is
the mechanism that makes "verified, not transcribed" structural rather than
aspirational.

**Why two gates.** Findings and drafted prose fail in different ways: findings
can be wrong or incomplete; drafts can be well-researched but misfiled across
the four documents, or drifted from the specification's placement tests. A
single combined approval would let a bad draft ride in on good research or
force re-research over a wording fix. Two gates let the developer correct the
fact base and the prose independently.

**Why the cross-system check is unconditional.** Component-specific relevance
judgment is exactly what produces silent gaps: the category that "seems
irrelevant" is the one that goes stale. Requiring all four categories every
run, with explicit "none found", converts each into an auditable claim rather
than an omission.

**Why one fact, one home.** The four documents answer four different questions
— what is set, how to act, why it is so, what differs here. A fact restated in
a second document creates a second thing that can go stale; the specification's
placement tests give the drafter a mechanical way to catch the drift before
the developer ever sees it.

**Where it sits.** It is the producer of most of `mybizz-config-docs` and a
consumer of the rest: every suite it writes becomes GBrain-indexed corpus via
ordinary host-source sync, and its own learnings file shapes its next run. It
never installs, upgrades or updates any system — a newer issuer release is a
finding the developer decides. mb-config-manager examines its suites through
the register cycle and orders a Refresh when the source moves; the skill is
never run to examine itself.

## What has to happen

- The developer (or mb-config-manager, for a Refresh) invokes it explicitly
  and stands at both approval gates; nothing is drafted before the first,
  nothing written before the second.
- The developer runs commit-all; documents reach GBrain and the division only
  through commits.
- After any edit to the canonical source, the installed copy is re-synced
  body-to-body — only frontmatter may differ — and the sync is verified by
  the reference's body-hash check.
- mb-config-manager examines this suite through the register cycle and orders
  a Refresh when the source moves.
- Grants are requested when a destination becomes confirmable, before drafts —
  never self-issued, never worked around.
