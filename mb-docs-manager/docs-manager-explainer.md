---
document: "docs-manager — Explainer"
doc-id: docs-manager-explainer
state: Live
date-created: 2026-09-10
---

# docs-manager — Explainer

## 1. What this actually is

`mb-docs-manager` is the skill that keeps a system's navigational documents honest against
the real filesystem. Every project ecosystem accumulates documents whose job is not to
describe the product but to map the territory — the division docmap, the projects config
register, the scope scaffold, and every README, AGENTS.md, and INDEX.md scattered through
the folders. Agents treat those documents as ground truth and navigate by them, so when the
real structure changes and the map doesn't, every agent that reads the map afterwards
confidently acts on a falsehood. Docs Manager walks the actual territory, compares it
street-by-street against what the maps claim, and proposes exact corrections — never
touching the territory itself. The city dictates the map; the map never dictates the city.

Two design decisions define its character. First, its scope is not defined inside the skill
at all: a separate developer-owned document — the scope scaffold — declares which roots are
walked, which paths are excepted, and which repositories exist, and the skill reads it at
the start of every run. When the system's shape changes, the developer edits the scaffold;
the skill follows, and never guesses. Second, it now speaks a target grammar shared by all
three documentation skills — you name a single target, or say `(all)` to sweep everything in
scope, or leave it empty and the skill simply asks. After a vast refactoring, `(all)` is the
right answer; the skill was built to make that sweep survivable rather than a flood.

## 2. Feature summary

- Scaffold-driven scoping, read fresh every run — five in-scope roots walked in full,
  exceptions honored, code repos denied outright, nothing assumed.
- A mandatory, verified pre-flight: every listed repository must be git-clean and the backup
  of all managed documents must be count-verified before any scanning; either failing aborts
  the entire run.
- Structural drift detection: claimed folders checked for existence, real folders checked
  for representation, counts and dates verified, internal cross-references resolved one
  level deep.
- A two-tier findings report that scales with sweep size: everyday corrections batched by
  folder and type into single approve/reject decisions; anything dangerous isolated in a
  labelled high-risk section where each item is decided individually.
- Permission-aware applying: when a correction must write into another project's folder, the
  skill hands the developer one complete, copy-pasteable block of permission commands
  instead of negotiating access per file.
- A least-privilege application model: text corrections and file moves are applied by
  separate agents with separate permissions and separate gates; file moves cannot delete —
  structurally, not by promise.
- Institutional memory: judgment calls become learnings that steer future runs, bounded so
  they can never authorize a write or skip a gate.
- Interrupt-proof state: continuous checkpointing, an asked-always resume/discard decision,
  a permanent structured log, and a batched commit plan (one approval, one commit per
  repository).

## 3. Suitability

**Best for:** closing the loop after structural changes — a folder created, renamed, moved,
or retired; a repo added or retired; scope reshaped in the scaffold. `(division-maps)` is
the right quick pass after editing the docmap, register, or scaffold; `(all)` is the right
tool after a big refactoring has left the maps badly stale — the deliberate wide sweep.

**Good for:** periodic staleness sweeps (`(quick)`, `(references)`), verifying pointers
after a manual edit (`(single document)`), and post-run audits via the
`last-completed-run` record and backup snapshots.

**Not good for:** checking whether documents *agree with each other* on content — that is
mb-align-docs' job; converting cross-references into wikilink form — mb-wikilinks; creating
canonical documentation — mb-sysdoc-creator; submitting content into governed memory —
mb-submit-memory. Also categorically wrong for: anything inside an Anvil code repo —
including documentation files stored under `theme\assets\docs`. Those are app assets in
Anvil's territory; these skills never open them. And it will never create a document: a
missing docmap or README is flagged, not written.

## 4. Design reasoning

**Why the scaffold wins.** Scope is the highest-stakes input the skill has; encoding it in
SKILL.md made every skill edit a scope edit, and the drift was invisible until a run tripped
over reality — twice. Moving scope to a developer-owned scaffold the skill reads but never
edits makes scope changes deliberate and impossible to guess. The scaffold is itself a
managed document, so its paths are verified against disk every run — a stale scaffold is
caught, not silently obeyed.

**Why the empty target now asks.** The original rule — no target means full run — made the
widest, most consequential mode the *accidental* one. The grammar now makes wide mode the
explicit choice (`(all)`) and silence a question. A rule whose default is "do the big thing"
inverts under fatigue; a rule whose default is "ask" cannot.

**Why nothing is deleted.** The V7 incident: a run performed a real delete. The fix is
structural — the file-operations agent's own instructions define "delete" as "move to
`obsolete\`", so there is no delete action to perform regardless of phrasing.

**Why text edits and file moves are separate agents.** A wrong one-line edit is visible in a
diff; a wrong move can lose a file. Different blast radius, different tool access, different
gates — approval covers both, and file operations add a second explicit confirmation
immediately before execution.

**Why the two-tier report.** A post-refactoring sweep can surface hundreds of findings;
one-decision-per-item approval would exhaust the very person it protects. Batching the
everyday corrections by folder and type turns the flood into a dozen decisions, while the
high-risk tier keeps every dangerous action — renames, register actions, anything
structural — visible, labelled, and individually approved. Grouping is a convenience for
review, never a shortcut for consent.

**Why the grant handover instead of rule exceptions.** The cross-project write rule protects
project boundaries, and the skill legitimately needs to edit managed documents across them.
Rather than accumulating standing exceptions in policy, the skill constructs the exact
permission commands the designed grant mechanism expects and hands them over as one block —
ephemeral, counted, ~30-minute slips issued by a human at the moment of need. The same
philosophy governs the push gate and the AGENTS.md naming gate: consequential actions stay
under explicit developer control.

**Why Anvil code repos are denied outright.** Anvil owns everything inside its code repos,
including how files under `assets` are interpreted. A documentation skill "helpfully"
reformatting something there would detonate at the worst possible moment — when the app is
next opened in the Anvil editor. The denial is absolute and covers the documentation files
inside code repos too; if those files ever need to be searchable in GBrain or linked
differently, that is a separate, researched decision — not a side effect of document
maintenance.

**Where it sits.** It is the structural member of the documentation-skill family, and the
first run in the fixed sequence: mb-docs-manager makes the structure truthful, mb-wikilinks
then fixes reference form against a stable structure, and mb-align-docs last validates
content agreement against the final `[[wikilink]]` convention. Each sweeps a corpus the
previous one just cleaned.

**Open items.** The docmap full redraw is the wide-mode run's standing work order; the trio
of desktop reference documents gets refreshed by that same run; the scan sub-agent's
reference-normalization regex deliberately retains retired path names so old dead references
classify as BROKEN rather than vanishing unclassified.
