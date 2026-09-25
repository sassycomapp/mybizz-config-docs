---
title: "doc-auditor-explainer"
doc-id: "doc-auditor-explainer"
---
# mb-doc-auditor — What It Is, What It Does, and Why It Is Built This Way

Companion to [[doc-auditor-config|Configuration]] (current state) and
[[doc-auditor-reference|Reference]] (commands and procedures). This document
owns the mental model: what the auditor is, what situation it is for, and why
its sharpest rules exist.

---

## The Objective, Stated Plainly

Documentation drifts in ways no single save event can cause or reveal: files
get renamed far from their references, registers fall behind reality, link
targets rot, legacy schema rows survive modernization, whole folders go
unregistered. `mb-doc-maintainer` handles each save the moment it happens, but
it deliberately never looks wider than the change — so something else has to,
periodically and on demand, establish whether the wider estate still satisfies
what G-brain depends on. `mb-doc-auditor` is that something. It examines a
selected scope against the explicit, developer-owned contract, repairs what is
safely repairable, surfaces genuine ambiguity as concise decision requests,
records what it did, and terminates.

Its governing principle is deliberately narrow: **measure the documentation
estate against the known requirements of G-brain, repair what can be safely
repaired, use maintenance history as evidence rather than as a work queue, ask
for human judgement only when genuinely necessary, and then finish.** The
developer is not the maintenance system; G-brain is the reason the auditor
exists.

## What It Actually Is — the Five Parts

The auditor is not one program; it is a pipeline of small parts, each
replaceable:

1. **The skill** — the audit brain: an OpenCode skill invoked explicitly or on
   a stated audit condition, with the scope and purpose named at invocation. It
   runs a fixed processing loop against the contract and terminates.
2. **The scope reader + estate scanner** — one stdlib-only Python module that
   parses the scope authority live at every run (nothing carried), applies the
   authority's exceptions, the Anvil class rule, and the treatment exclusions,
   and discovers registers by walking up from the audit root.
3. **The evidence tools** — the orchestrator plus the maintainer's own
   frontmatter, links, and register primitives (shared infrastructure, reused
   without merging responsibilities): read-only evidence over the selected
   scope, then mechanical repairs that are byte-surgical and verified in the
   same result.
4. **The run-log reader** — the maintainer's durable log consumed strictly as
   investigative evidence; absent or empty is a normal state, and repetition
   never becomes work without a reasoned connection to a requirement.
5. **The audit record** — an append-only block per run (scope, purpose,
   checked, findings by classification, actions, outstanding, terminal state),
   so the developer can interrogate any completed audit on demand.

The requirements themselves are not in the skill. They live in the **G-brain
documentation contract**, consumed read-only with explicit change control: the
auditor enforces the contract as written, records what is not established
rather than inventing it, and never decides what G-brain should require.

## Feature Summary — conceptual

- **Scope-bounded audits**: one purpose, one scope, one terminal state — deep
  examination, never maximum scanning; the minimum sufficient scope.
- **Contract enforcement, not taste**: the same requirements the maintainer
  enforces (frontmatter exclusivity, wikilink grammar and resolution, target
  existence, register schema and four-event discipline), measured across the
  wider estate.
- **Read-only live G-brain checks**: registered-source boundary (G9) and
  orphan health (G10) verified through `gbrain sources list` / `gbrain
  orphans` — read-only by construction; a failed call is Can wait, never a
  blocker.
- **Deterministic repair with refusals**: byte-preserving frontmatter restore,
  append-only register creations, and retire-in-place — with explicit refusal
  classes (collision stems, multi-occurrence stems, out-of-scope obsolete rows)
  surfaced for human judgement instead of guessed.
- **Anti-work-generation**: retired rows are history, not repeat findings;
  prose candidates are candidates, not conversions; "can wait" never becomes a
  work queue.
- **Minimal reporting with durable evidence**: a concise summary by default,
  full detail on demand from the audit record.

## Suitability

**Best for:** establishing, on demand, that a whole library or corpus satisfies
the documented G-brain requirements — after substantial restructuring, after a
migration, after an ingestion or indexing change, or whenever accumulated
maintenance history suggests a wider look.

**Good for:** honest accounting of the estate's real state (broken links,
collisions, legacy register rows surfaced as classified findings, not silent
neglect); mechanical hygiene at scale (frontmatter and registration repairs
applied and verified in one run); producing a durable, queryable audit trail.

**Not good for:** save-time maintenance — a saved document's needs are the
maintainer's job, by design; continuous cleaning — the auditor runs when
invoked, never on a timer (v1 has no scheduler); deciding what the
documentation requirements should be — that is the developer's architectural
authority, and the auditor surfaces, never invents.

## Why Periodic-and-On-Demand Rather Than Save-Time

The maintainer's strength is timing: a save is fresh, its context known, its
repair small. The auditor's strength is coverage: it sees what no single save
event can — accumulated drift, systemic patterns, dead registrations. Running
the auditor at save time would recreate the second DocCycle the plan forbids;
running the maintainer corpus-wide after every save would destroy its value.
The split is the architecture: the maintainer protects what is currently being
built; the auditor checks the wider estate; neither reaches into the other's
scope.

## Why the Contract Is External — and Why Repairs Refuse

The same inversion the maintainer uses applies at estate scale: an auditor
that "knew" what documentation should look like would generate work from every
difference it could detect. The contract inverts that — enforce as written,
record the not-established, keep an explicit not-required list. The refusal
classes are the sharp edge of the same principle: where the correct action is
underdetermined (which file a collision-stem row represents; what doc-id
convention nested corpora should use), the tool reports instead of guessing,
because a wrong mechanical "repair" of identity is worse than an honest
question.

## Why Retire-in-Place

Registers are append-only — rows are never deleted — so history is never
silently rewritten and a later question about a retired document has an answer
instead of a gap. Obsolescence is a state change (`Retired`, `superseded-by`
where known), never an excision. The same discipline applies to the auditor's
own artifacts: the audit record is append-only, and a retired register row is
register history — re-flagging it would manufacture repeat work, so the
tooling filters it.

## Where It Sits in the System

The auditor consumes the **scope authority** live at every run (no carried
scope list) and the **G-brain documentation contract** as its requirement
source. It is independent of the **watcher** and of the maintainer's save-time
loop — though it reads the maintainer's durable run log as evidence. Its own
artifacts live in three layers: source repo (`C:\mybizz\mb-doc-auditor`,
GitHub-backed), installed skill (WSL `~/.config/opencode/skills/`), and suite
documentation (this folder). Its own plumbing obeys its own rules: the audit
record carries exact two-field frontmatter and a register row; it is never its
own trigger; it never writes to G-brain.

## Honest Limits

- The nested-corpus registration convention is matched by a candidate
  heuristic (detection only); confirming the convention is a developer
  decision surfaced by the first live audit.
- The doc-id candidate set is evidence-derived from this corpus's registers;
  a future corpus using a different derivation would need the candidate set
  revisited — the refusals make that visible rather than dangerous.
- Live verification so far covers one full audit of `project-library-global`
  (frontmatter clean, 6 register repairs verified); walkthroughs on corpus
  copies cover the repair and refusal paths.
- Discovery of the installed skill is convention-verified (path, frontmatter,
  body rule identical to 100+ working skills); the live session listing
  confirms at the next session start.
- No scheduler exists in v1; nothing runs by itself. That is the design split,
  not a defect.

## Deliberately Out of Scope

The auditor is not a save-time handler, not a corpus cleaner, not a
document-management system, and never another DocCycle. It does not modify,
migrate, refactor, dismantle, retire, extract from, or incorporate DocCycle.
It does not duplicate the maintainer's save-time work, does not demand approval
for safe mechanical repairs, does not create metadata churn, does not rescan
without reason, and does not turn the maintainer run-log into a work queue.
Where a finding is real but not for this run, it is classified "can wait" and
explicitly never becomes a new work queue. Where judgement is genuinely
required, it asks — it never guesses to avoid asking. Those boundaries are the
component's contract with the developer, enforced by the prohibition list every
run re-reads first.

---

*Suite: [[doc-auditor-config|Configuration]] (spec), [[doc-auditor-reference|Reference]]
(commands and procedures). Requirements source: `gbrain/gbrain-doc-contract.md`.
Governing plan: `mb-doc-auditor — Complete Consolidated Plan.md`
(doc-auditor-maintaner-planning, amendments A–H applied 2026-09-25).*

*End of document*
