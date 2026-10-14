---
title: "sysdoc-creator-explainer"
doc-id: "mb-1b1e5218"
updated: "2026-10-14"
---
# sysdoc-creator — Explainer

Companion to [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-config.md) (the spec — current
state) and [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-reference.md) (the execution form). The
config-management exam set for this suite ([[sysdoc-creator-exam-plan|Exam
Plan]] · Exam Report · Log
· [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-learnings.md) ·
Exam Skill) is synthesized and consumed per the
[[[mybizz-config-docs:mb-config-manager/config-manager-agent|Config Manager]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md) plan-driven cycle — the exam verifies
this suite's state and never runs the subject skill itself.

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
(right tool: write it directly); converting cross-references into
resolvable links (mb-doc-check writes every link in the stored form at
every commit, [[[mybizz-config-docs:mb-doc-check/doc-check-explainer]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-explainer.md)); submitting content into governed memory (right tool:
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
its own learnings file, which shapes the next run's research pattern. This
skill owns whether the content was true when it was written.

**Decision — the skill-index register entry.** Closed as resolved: the skills catalogue lists `mb-sysdoc-creator`.

**Decision — the file prefix.** This suite keeps the prefix `sysdoc-creator-`, a deliberate exception to the convention that a suite's files use its folder name as prefix. Renaming the three files would disturb every link to them for no practical gain.

## 5. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[config-manager-explainer|the config-manager
explainer]] — emulated from the PostgreSQL pilot. The short local version:

- [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-config.md) is the **spec** — the ideal state
  every exam checks against.
- Before each exam run, the config-manager synthesizes
  Exam Plan: a fresh job-spec built from this
  spec, the last report, the log, and the learnings. The plan is transient
  (the file is live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-mb-sysdoc-creator`) with the
  plan in hand — detection fully autonomous; healing gated.
- **Agent-healable items are suite-file repairs only** (the exam set files).
  The subject `SKILL.md`, its source copy, `doc-suite-specification.md`, the
  run-log infrastructure, and every produced suite are deny-list: changes
  reach them only as gate proposals the developer approves item by item.
- The subject skill's own Hard Rule 7 binds the exam: a policy block stops
  and reports; grants are requested in chat, never self-issued.
- The run rewrites Exam Report (current state,
  no history), appends one row to Log, files new
  learnings, and prunes absorbed entries.

## 6. S.W.O.T.

**Strengths.** Research-first discipline that live-verifies instead of
transcribing; two independent human gates; the unconditional cross-cutting
check with explicit "none found" reporting; interrupt-proof run state with a
compounding learnings file; proven output — eighteen run logs across sixteen
systems plus correction runs, every suite in this repo produced this way.

**Weaknesses.** Expensive by design — every run demands real research and two
human gates, so casual use wastes the apparatus. The canonical source copy
lost its body from the working tree (2026-09-10) and the replacement stub
stayed empty, breaking the diff-based currency check until restored from git.
Phase 9a carries a retired institution's register policy into every live run.
No version field exists, so currency is provable only by the (currently
broken) diff.

**Opportunities.** The config-management exam adds standing verification this
system never had; learnings graduation can move settled patterns into the
skill itself.

**Threats.** Spec-doc drift between runs silently weakens exams (mitigated:
exams flag spec drift, never edit it). Retired-institution references
surviving in skill content produce spurious findings on live runs (observed
2026-10-07 — Phase 9a). Produced-suite drift (mitigated: each produced suite
is owned by its own `mb-config-*` exam module).

---

**Companion documents:** [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-config.md) (state) ·
[[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-reference|Reference]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-reference.md) (execution) ·
[[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) (the governing
specification this skill enforces) · Exam Plan ·
Exam Report · Log ·
[[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-learnings.md) ·
Exam Skill.
