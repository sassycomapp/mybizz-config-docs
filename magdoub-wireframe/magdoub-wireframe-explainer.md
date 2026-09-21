---
document: "magdoub-wireframe — Explainer"
doc-id: magdoub-wireframe-explainer
state: Live
date-created: 2026-09-06
---

# magdoub-wireframe — Explainer

*Companion note: for current confirmed state (paths, versions, integration,
open items) see [[magdoub-wireframe-config|Configuration]]. For invocation, operation,
update, and the do-not list, see [[magdoub-wireframe-reference|Reference: Invocation, Operation, Update]]. For the
config-management set: [[magdoub-wireframe-exam-plan|Exam Plan]] (transient job-spec),
[[magdoub-wireframe-exam-report|Exam Report]] (last verified state),
[[magdoub-wireframe-log|Log]] (chronological events),
[[magdoub-wireframe-learnings|Learnings]] (transient knowledge), and
[[magdoub-wireframe-skill|Magdoub Wireframe Skill]] (exam skill canonical source).*

---

## 1. What this actually is

The Magdoub Wireframe Skill is a third-party agent skill — built for Claude Code
by an individual developer, installed here through a manual symlink because
OpenCode understands the same SKILL.md format — that turns a one-line feature
description into five alternative interactive wireframes of that feature,
delivered as a single self-contained HTML file. It exists to answer a question
that is expensive to answer by building: *what should this screen's structure
be?* — before any real UI work starts. The five proposals always include one
safe extension of the project's existing design and four deliberate departures,
so the comparison is between a baseline and genuine alternatives, not between
five flavors of the same idea.

Its role in this system is specific: PDLF's applications are built on Anvil,
and Anvil's designer cannot import from or export to conventional design tools
like Figma. This skill supplies the missing iteration loop — a fast, structured
way to explore and discard screen designs natively inside the agent workflow,
between the design-direction phase and actual form-building.

## 2. Feature summary — conceptual

- **Progressive exploration.** A structural black-and-white comparison arrives in about a minute; color treatment is a separate, later decision. Structure is decided before styling, on purpose.
- **Five philosophies per run.** Options draw from a wide repertoire (progressive disclosure, wizard, dashboard-first, search-first, and more), each named, scored against the run's stated goal, and reduced to a recommendation.
- **Parallel visual enrichment.** Each option can receive two color treatments — a flat "Clean" and a crafted "Polished" — generated independently, so one structural decision yields a full visual spectrum.
- **Persistent per-project memory.** First use scans the codebase and asks for screenshots, producing a design-context file that makes every later run's "safe option" a genuine extension of the existing product rather than a generic template.
- **Goal extraction.** A directional phrase in the request ("reduce clutter", "more conversions") becomes the lens that weights both the proposals and the scoring — no separate configuration step.
- **Zero-dependency output.** The comparison artifact is plain HTML/CSS with system fonts — no CDNs, no build step; openable anywhere, disposable by design.

## 3. Suitability

**Best for:** early structural exploration of a feature or screen in a
PDLF-governed Anvil project — choosing between genuinely different information
architectures before committing to Anvil forms; and for iterating visual
treatment over a locked layout once structure is agreed.

**Good for:** standalone throwaway prototypes for any web feature, as a
communication artifact between developer and stakeholder; bootstrapping a
persistent design-context file for an existing codebase, which has standalone
value beyond the wireframes themselves.

**Not good for:** production UI — the output is deliberately disposable HTML,
not Anvil components, and none of it is meant to ship. Producing
ADR-conforming construction-instruction wireframes directly — the [[adr-design-rules|Wireframe Design Rules]]
ADR (now scoped by its Section A) governs wireframes *not* created by this skill;
Magdoub output is a different genre and exempt as an artifact, but an
ADR-conforming deliverable still requires a conformance pass beyond what this
skill emits. Any flow requiring sub-agent delegation — standing policy prohibits
sub-agent creation in this environment, enforced when active at three
independent layers (enforcement status not fixed — see §8), and the skill's
Phase 2 was written assuming it exists. Visual design comps — the skill deliberately refuses to make styling
decisions in its structural phase.

## 4. Design reasoning

### Why two phases with a hard B&W wall between them

Wireframe failures are usually visual decisions arriving too early: a hero
gradient polished onto a screen whose information architecture is wrong.
Forcing the structural pass to a gray-only palette makes styling literally
impossible and drives every debate onto layout, hierarchy, and flow — the
things that are expensive to change later and cheap to change now. The color
phases are separate because, once structure is locked, visual treatment is
genuinely parallelizable: nothing in one option's color variant affects
another's.

### Why the output is one shared HTML file with CSS-swapped variants

All three sub-tabs render the same DOM; switching tabs only swaps a class on
the wrapper, and each variant's CSS overrides treatment properties, never
layout. That architecture guarantees the thing the skill exists to guarantee:
a colored version cannot silently diverge from the structure that was approved.
The completion banner works through a CSS self-reveal mechanism — badges hide
themselves once variant CSS loads — so the page reports its own readiness
without polling or a page reload.

### Why the template-based workflow exists

Earlier versions had the agent regenerate the comparison page's boilerplate —
tabs, browser frame, annotations, footer — on every run: inconsistent, and a
recurring source of drift. Extracting that chrome into bundled templates, and
cutting the content-CSS budgets to a few hundred lines, confines the agent's
creativity to the only layer where it pays: the wireframe content itself. This
is also why an update can matter materially — template paths and budget rules
changed in recent upstream history.

### Where this sits relative to the rest of the system

- **PDLF** registers the skill as its visual-iteration stage: a structural pass between the design reviews, then a second pass with an approval gate before screen work. It is one of five deliberately narrow skill families; it owns visual iteration and nothing else.
- **Cupcake** constrains it more than any other component — with one standing caveat: enforcement status is not fixed and should not be assumed current at any given time (check [[cupcake-config|Cupcake Configuration]]'s Current Operational Status). Standing policy denies sub-agent creation, enforced when active at three independent layers, and the skill's Phase 2 was written assuming sub-agents exist. The structural phase is unaffected; the color phase's mechanism on this machine is the suite's principal open question.
- **Memory Governor** does not see it: skill content is vendor-published reference material arriving via a real git clone, so it takes the same permanent ordinary-sync bypass as Anvil's agent references. The update command, unlike the content, is confined to the developer's own terminal because it rewrites files outside every project root — a deliberate split between how the skill's content flows and who may touch the clone.
- **security-global's review-before-trust principle** is the standard this skill was supposed to be admitted under: publisher, license, maintenance, spawn-capability. Its profile is benign on every axis, but no record of that review exists — which is itself the finding.
- **The [[adr-design-rules|Wireframe Design Rules]] ADR** governs what a wireframe *document* must be in project-library-global — instructive, three-section, scaffold-read-first. Reconciliation **resolved 2026-09-16** by Section A: the ADR applies only to wireframes not created by this skill; this skill's comparison artifact is a different genre, exempt; but the exemption is not an escape hatch for ADR-conforming deliverables (A3).

### Open architectural questions

1. **What executes Phase 2 here?** The honest candidates are a main-agent fallback (sequential CSS authorship — losing the parallelism, keeping the output contract) or treating the skill as Phase-1-only in this environment. The answer determines whether PDLF's gated second stage can run as designed or needs its own adaptation.
2. **The first real run is a verification event, not a routine use.** Everything in the config doc except run behavior is verified; the skill's actual behavior here — first-run flows against Anvil projects, interplay with the ADR's mandatory reading — is untested. Treating the first run as routine would let unverified assumptions harden into practice.
3. **ADR reconciliation — RESOLVED 2026-09-16 (developer decision).** If PDLF projects need ADR-conforming wireframes, either the skill's output needs a conformance pass after generation, or the ADR needs a documented carve-out for exploratory comparison artifacts. **Decision:** the carve-out was taken — [[adr-design-rules|Wireframe Design Rules]] gained Section A (Magdoub-skill exemption): the ADR applies only to wireframes not created by this skill; Magdoub output is a different genre, exempt as an artifact; but the exemption is not an escape hatch — an ADR-conforming deliverable still requires a conformance pass (ADR §A3). Avoiding non-compliant deliverables at scale is now handled by A3's explicit clause.
4. **Retiring the old in-folder reference doc.** It predates this suite, carries two stale claims, and lives where a clone reset won't touch it but a reinstall would. Keeping two reference documents for one component recreates the drift problem the doc-suite pattern exists to prevent.

## 5. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[config-manager-explainer|Explainer]] — emulated from the
PostgreSQL pilot. The short local version:

- [[magdoub-wireframe-config|Configuration]] is the **spec** — the ideal state every exam
  checks against.
- Before each exam run, the config-manager synthesizes
  [[magdoub-wireframe-exam-plan|Exam Plan]]: a fresh job-spec built from this spec, the
  last report, the log, and the learnings. The plan is transient (the file is
  live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-magdoub-wireframe`) with the
  plan in hand — detection fully autonomous; healing gated. **This module has
  no agent-healable items**: the clone is developer-owned (update command
  developer-run only, settled policy), and every open item resolves by developer
  decision or docs governance.
- **Scope boundary:** PDLF's step 22/26 usage and [[adr-design-rules|Wireframe Design Rules]] ADR interplay
  belong to the PDLF / project-library-global docs domain; the `task`-tool guard
  layer and spawn-tools policy belong to the cupcake/opencode modules; gbrain's
  sync state belongs to the gbrain module. This exam touches none of them.
- The run rewrites [[magdoub-wireframe-exam-report|Exam Report]] (current state, no
  history), appends one row to [[magdoub-wireframe-log|Log]], files new learnings,
  and prunes absorbed entries.

## 6. S.W.O.T.

**Strengths.** A genuinely clean install topology — one real git clone, one
discovery symlink, no copies, no second paths, easily verified exhaustively (a
HEAD pin and a symlink resolution are hard, cheap checks); the template-based
output design confines drift to the one layer that pays; a settled, recorded
policy on the two touchpoints that could hurt (updates and memory syncing)
makes the exam's job mostly verification.

**Weaknesses.** No confirmed real run anywhere — everything except run behavior
is verified, so the first governed use is itself a verification event; Phase 2
(the color pass) is written for a sub-agent environment this one denies, and its
replacement mechanism is undecided; the skill is unmaintained upstream (last
commit 2026-03-01), so no drift pressure exists but no improvement pressure
either.

**Opportunities.** A standing liveness exam gives the first health record the
install has ever had; the supply-chain review owed at adoption (open item 3) can
be discharged properly once the exam surfaces it; retiring the old single-file
reference (open item 5) would restore the one-canonical-home principle.

**Threats.** A silent `git pull` or `reset --hard` by any automation would
move the pinned HEAD without a decision — the exam's HEAD check catches it; an
accidental second discovery path would double-load the skill — the single-path
check catches it; the `task`-tool guard layer changing state could reclassify
which Phase-2 checks are even reachable — denials are honored and reclassified
developer-run immediately.

---

*Companion documents: [[magdoub-wireframe-config|Configuration]] (state),
[[magdoub-wireframe-reference|Reference: Invocation, Operation, Update]] (commands and rules),
[[magdoub-wireframe-exam-plan|Exam Plan]] / [[magdoub-wireframe-exam-report|Exam Report]] /
[[magdoub-wireframe-log|Log]] / [[magdoub-wireframe-learnings|Learnings]]
(config-management set), [[magdoub-wireframe-skill|Magdoub Wireframe Skill]] (exam skill canonical
source). Architecture: [[config-manager-explainer|Explainer]].*
