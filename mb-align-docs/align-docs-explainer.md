---
document: "align-docs — Explainer"
doc-id: align-docs-explainer
state: Live
date-created: 2026-09-10
---

# align-docs — Explainer

Updated 2026-09-20 to reflect the refactored skill (`SKILL.md` V2.1,
2026-09-19): scope from the single authority list, shared run frame in
[[doc-skills-run-discipline|Shared Run Discipline]], roles as permission disciplines rather than
sub-agents, and es.exe-first file search.

## 1. What this actually is

`mb-align-docs` is the skill that keeps a project's *documents agreeing with each other*.
Where mb-docs-manager makes sure the map matches the territory (folders, files, indexes),
this skill makes sure everything written *on* the map agrees with everything else written on
it: the same concept is called the same name everywhere; requirements don't quietly
contradict each other; cross-references point where they claim to; and every document has a
stable, permanent identity — who it is, whether it's the current version, and what replaced
it if it isn't.

Its central idea is that documents have identity, kept in a small front-matter block set
once at creation and never edited. When meaning changes, you don't mutate the old document —
you create a new version with its own identity, and the old one retires. This one rule makes
everything else checkable: a reference pointing at a retired document is always a defect,
because the live corpus never cites history. The register — an append-only, permanent record
of every document ever registered — is the enforcement backbone: the live filesystem is
diffed against it on every run, and in any mismatch, **the register wins**.

## 2. Feature summary

- Content-agreement detection across an entire corpus: terminology mismatches, contradicting
  requirements, stale references, orphaned cross-references, and identifier drift.
- Register enforcement: the global register is not advisory — every run diffs reality
  against it, and divergence forces a binary decision (rename back to match, or retire).
- Document identity: four-field front matter (document, doc-id, state, date-created) with
  state — Live, Retired, Quarantine — authoritative for whether a reference is valid.
- Directionality validation: global documents may reference global and be referenced by
  local; global never depends on local; cross-project references never live — such content
  is copied into Quarantine with recorded provenance instead of linked.
- Two separated remediation paths: small reference repairs (frequent, local) and identifier
  changes (rare, but global in effect — triggering an immediate, visible, corpus-wide sweep)
  are executed by different permission classes, never mixed.
- A two-tier approval presentation that scales: everyday findings batched by target and type
  into single decisions; high-risk findings (identifier changes, register actions,
  quarantines) grouped by risk type, labelled, and decided individually with a second
  confirmation before anything structural executes.
- Scope from a single authority: the scoping list ([[mybizz-scope-list|Mybizz Scope List]]) governs every
  documentation skill — the skill never carries its own scope list, and transient state
  (a project under development) schedules the work, never removes scope.
- A shared run frame defined once ([[doc-skills-run-discipline|Shared Run Discipline]]): resume check, learnings
  load, git-clean precondition, verified stop-cold backup, decision-point checkpointing,
  run-record lifecycle (working record → `last-completed-run\` + one row in
  `run-index.md`), approvals in chat, es.exe-first file search, per-source GBrain sync at
  close. The write classes are permission disciplines enacted by the orchestrating agent —
  never spawned as sub-agents.

## 3. Suitability

**Best for:** the content-hygiene pass of the documentation cycle — after structure is true
(mb-docs-manager) and BEFORE mb-wikilinks, this skill makes a corpus internally consistent:
one terminology, one identity system, no dead or contradictory references. align-docs runs
first by the product-then-packaging principle: it heals every reference in its existing
written form, and only then does wikilinks package the validated product into
`[[wikilink]]` links. Running it per project (`(slug)`) is the routine form; `(all)` is the
post-refactoring wide sweep.

**Good for:** onboarding a newly imported or heavily reworked project library (the register
enforcement and front-matter checks bring order fast); auditing a corpus before a major
hand-off or migration; preserving valuable content from another project safely via the
Quarantine mechanism.

**Not good for:** folder/file structure and current-state indexing — mb-docs-manager's
territory, deliberately separate (the two skills do not interoperate or lean on each other's
outputs); converting cross-reference *style* — mb-wikilinks runs after this skill, packaging
what align-docs healed; anything inside an Anvil code repo — categorically denied, including
documentation under `theme\assets\docs`; creating documents — it validates and repairs,
never authors; managing UI build artefacts — HTML/PNG outputs under `ui\` are permanently
out of front-matter scope by nature.

## 4. Design reasoning

**Why identity is front matter, and never edited.** Reference-checking needs a single source
of truth about what a document *is*. Keeping references out of front matter (they live only
in body text) and identity immutable means "is this reference valid?" has exactly one
answer — the target's state — and history is never silently rewritten. Supersession creates;
it doesn't mutate.

**Why the register wins, absolutely.** An advisory register would drift the moment a rename
felt convenient. Making it enforcement — with exactly two exits (rename back, or retire)
— is what turns "a list of documents" into an identity system. The severity is deliberate:
a global document's name, once given, is permanent, and changing a concept's name is a
corpus-wide event, not a folder-level convenience.

**Why two operations never share a remediation path.** "This pointer is wrong" and "this
thing is being renamed" look similar in a report but have completely different blast
radii — the second silently re-breaks every other reference in the corpus if treated
locally. Separate permission classes, and a mandatory immediate corpus-wide sweep
for identifier changes exist because that distinction must be structural, not judgment
exercised under time pressure.

**Why Quarantine instead of just deleting cross-project references.** Content from another
project is sometimes genuinely valuable, but linking it live couples two projects'
lifecycles. The copy-with-provenance pattern preserves the content without the coupling —
and preserves it *from eventual purge*, which is the one thing Quarantine does that Obsolete
does not.

**Why the two-tier approval.** The skill was designed for a moment exactly like the present
one: a corpus left badly stale by a big refactoring, where per-item approval would flood the
developer. Batching the routine by target and type turns hundreds of findings into a review
of a dozen groups; the high-risk tier keeps the dangerous work — the changes that ripple —
impossible to approve casually. The grouping is presentation; consent stays per item where
it matters.

**Why a shared run frame.** Before the 2026-09-19 refactor, each documentation skill
carried its own copy of the safety procedure, and the copies drifted — different backup
schemes, different search tools, different record lifecycles. The frame now lives once
([[doc-skills-run-discipline|Shared Run Discipline]]) and each skill adds only its own specifics, so a lesson
learned in one skill (es.exe's swallowed result limits, backup verification, the resume
contract) applies identically in all of them and cannot be fixed in one copy while staying
broken in another.

**Where it sits.** It runs BEFORE mb-wikilinks, by the product-then-packaging principle:
align-docs creates the correct product (every reference pointing where it should), and
wikilinks then packages that validated product in the link format. It is also
mb-docs-manager's deliberate mirror: that skill owns the map's accuracy, this one
owns the map's internal consistency — they share the safety framework (verified backup,
checkpointing, resume, least-privilege write classes, append-only logging) but never share
inputs, outputs, or responsibilities.

**Open items.** The skill has completed real runs: the 2026-09-18 passes healed front
matter and cross-references (including one approved identifier change with its corpus-wide
sweep), and the 2026-09-19 V2.1 run returned relocated explainers, applied front matter to
eight documents, and updated the register — all committed. The two-tier approval has faced
volume; the next scale test is the pending post-refactor `mb-wikilinks` wide sweep, which
consumes align-docs' healed output. Front matter stays identity-only and small; if PDLF
ever needs more (step-linkage, for instance), the growth path is a deliberate broad-sweep
addition, not silent accretion. And the Anvil-hosted documentation question (what
formatting Anvil accepts, whether wikilinks can ever resolve there) is standing research
feeding a future decision — safely moot for now, since code repos are denied outright.
