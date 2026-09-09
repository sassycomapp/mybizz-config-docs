# docs-manager — Explainer

## 1. What this actually is

`mb-docs-manager` is the skill that keeps a system's navigational documents honest against
the real filesystem. Every project ecosystem accumulates a layer of documents whose job is
not to describe the product but to map the territory — the division docmap, the projects
config register, the scope scaffold, and every README, AGENTS.md, and INDEX.md scattered
through the folders. Agents treat those documents as ground truth and navigate by them, so
when the real structure changes and the map doesn't, every agent that reads the map
afterwards confidently acts on a falsehood. Docs Manager walks the actual territory, compares
it street-by-street against what the maps claim, and proposes exact corrections — never
touching the territory itself. The city dictates the map; the map never dictates the city.

Its scope is not defined inside the skill at all. A separate document — the scope scaffold —
declares which roots are walked, which paths are excepted, and which GitHub repositories
exist. The skill reads that scaffold at the start of every run. When the system's shape
changes, the developer edits the scaffold; the skill follows. That design exists because the
skill's own internal scope copy went stale twice, and each time the staleness was invisible
until a run tripped over reality.

## 2. Feature summary

- Scaffold-driven scoping: five in-scope roots walked in full, exceptions and out-of-scope
  paths honored, all sourced from the scope scaffold each run — never from a copy.
- A mandatory, verified pre-flight: every listed repository must be git-clean and the backup
  of all managed documents must be count-verified before any scanning happens; either
  failing aborts the entire run.
- Structural drift detection: folders and files claimed by maps are checked for existence,
  real folders are checked for representation, counts and dates are verified, and internal
  cross-references between documents are resolved one level deep.
- Classified anomalies with a concrete recommendation attached to every finding — never a
  bare problem, never a guess.
- A two-stage, least-privilege application model: text corrections and file moves are
  applied by separate agents with separate permissions and separate approval gates; file
  moves get a second explicit confirmation and structurally cannot delete anything.
- Institutional memory: judgment calls the developer makes are captured as learnings that
  steer future runs, bounded so they can never authorize a write, skip a backup, or bypass
  approval.
- Interrupt-proof state: continuous checkpointing, an asked-always resume/discard decision,
  and a permanent structured log per run.

## 3. Suitability

**Best for:** closing the loop after structural changes — a folder created, renamed, moved,
or retired; a repo added or retired; scope reshaped in the scaffold. Running it is what
makes such a change "finished," and its `division-maps` scope is the right quick pass after
editing the docmap, register, or scaffold themselves.

**Good for:** periodic staleness sweeps (`quick`, `references`), verifying a document's
pointers after a manual edit (single-document scope), and post-run audits via its
`last-completed-run` record and backup snapshots.

**Not good for:** checking whether documents *agree with each other* on content — that is
mb-align-docs' job (structure vs content, deliberately separate skills); converting
cross-references into wikilink form — mb-wikilinks; creating canonical documentation —
mb-sysdoc-creator; submitting content into governed memory — mb-submit-memory. Also wrong
for creating documents: it will flag a missing docmap or README but will never write one —
document creation is deliberately outside what any automated write in this system is
trusted to do unsupervised.

## 4. Design reasoning

**Why the scaffold wins.** Scope is the highest-stakes input the skill has: walk the wrong
folders and the run generates noise or, worse, touches something it shouldn't. Encoding
scope in SKILL.md made every skill edit a scope edit — the exact drift class this
remediation fixed twice. Moving scope to a developer-owned scaffold that the skill reads
but never edits makes scope changes deliberate, versioned in the developer's hands, and
impossible for the skill to guess. The scaffold is itself a managed document, so the skill
verifies its paths against disk every run — a stale scaffold is caught, not silently obeyed.

**Why nothing is deleted.** The V7 incident: a run performed a real delete. The fix is
structural, not behavioral — the file-operations agent's own instructions define "delete"
as "move to `obsolete\`", so there is no delete action to perform regardless of how a
request is phrased. Anything removed by mistake is sitting in `obsolete`, not gone.

**Why text edits and file moves are separate agents.** A wrong one-line edit is visible in
a diff; a wrong move can lose a file. Different blast radius, different tool access (edit
without bash; bash without edit), different gates — Phase 3 approval covers both, and file
operations add a second explicit confirmation immediately before execution.

**Why the pre-flight is unconditional.** A dirty repository makes it impossible to reason
about what a run changed versus what was already pending; an unverified backup makes
recovery theoretical. Both are abort conditions, not warnings — the run either starts from
a known-clean, recoverable state or doesn't start.

**Why the grant handover instead of a rule exception.** The cross-project write rule
protects project boundaries; the skill legitimately needs to edit managed documents inside
other projects' folders. Rather than accumulating exceptions in policy (which become
unmanageable), the skill constructs the exact permission-slip commands the designed grant
mechanism expects and hands them to the developer — ephemeral, counted, ~30-minute slips
issued by a human at the moment of need. The same philosophy governs the push gate
(explicit approval precedes any commit/push) and the AGENTS.md naming gate (governance
files change only when the developer names the exact file).

**Where it sits.** It is the structural member of the documentation-skill family:
mb-docs-manager owns whether maps match the territory, mb-align-docs owns whether
documents agree with each other, mb-wikilinks owns cross-reference form, and
mb-sysdoc-creator owns whether content was true when written. The intended cycle after
this suite: create the remaining suites, run all three siblings, and the deferred work
order — the full docmap redraw to include everything in scope — executes then.

**Open items.** The docmap redraw is deferred by developer sequencing (this suite's config
document carries the work order). The scan sub-agent's reference-normalization regex
retains retired path names deliberately, so old dead references classify as BROKEN rather
than vanishing unclassified.
