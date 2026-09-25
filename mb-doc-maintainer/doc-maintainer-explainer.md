---
title: "doc-maintainer-explainer"
doc-id: "doc-maintainer-explainer"
---
# mb-doc-maintainer — What It Is, What It Does, and Why It Is Built This Way

Companion to [[doc-maintainer-config|Configuration]] (current state) and
[[doc-maintainer-reference|Reference]] (commands and procedures). Exam set:
[[doc-maintainer-exam-plan|Exam Plan]] (next run's job-spec — transient),
[[doc-maintainer-exam-report|Exam Report]] (last run's verified state),
[[doc-maintainer-log|Log]] (notable events), [[doc-maintainer-learnings|Learnings]]
(transient exam knowledge), [[doc-maintainer-skill|Exam Skill]] (the standing
check inventory — canonical source lives in this suite folder). The exam cycle
architecture: [[config-manager-explainer|Explainer]]. This document owns the
mental model: what the maintainer is, what situation it is for, and why its
sharpest rules exist.

---

## The Objective, Stated Plainly

When a document is saved anywhere in the Mybizz documentation corpora, something
has to make sure that save did not leave the affected documentation broken —
unusable by G-brain, structurally incoherent, unregistered where registration
matters, or pointing at targets that no longer exist. `mb-doc-maintainer` is
that something. It maintains documentation integrity **at save time**, against
an explicit, developer-owned contract, doing the minimum work necessary —
repairing what is safely repairable, asking only when judgement is genuinely
required, and then stopping.

The problem it solves is specific: G-brain only stays useful if the documents
it ingests stay within its known requirements, and development constantly moves
those documents — creates them, edits them, renames them, deletes them. Left to
manual discipline, documentation drifts; left to an eager automated cleaner, it
sprawls. The maintainer's governing principle is deliberately narrow: **maintain
the saved change against the known requirements of G-brain, repair what can be
safely repaired, ask only when judgement is genuinely required, and then stop.**
Its purpose is to keep documentation maintenance almost invisible. The developer
is not the maintenance system; G-brain is the reason the maintainer exists.

## What It Actually Is — the Five Parts

The maintainer is not one program; it is a pipeline of small parts, each
replaceable:

1. **The watcher** — an always-on Windows scheduled task using
   `FileSystemWatcher`. It interprets raw filesystem change events (not
   semantic saves) into stable saved-document events, coalescing rapid saves of
   the same file so intermediate states are never processed. It writes a pending
   event and forgets about it.
2. **The queue** — one JSON file per stable event, under the logs area. Pure
   plumbing: regenerable, disposable, removed after processing.
3. **The skill** — the maintenance brain: an OpenCode skill invoked to drain
   the queue, running a fixed processing loop per event against the contract,
   and terminating. Empty queue means nothing to do.
4. **The tools** — three stdlib-only Python scripts (frontmatter, links,
   register) that make the mechanical checks deterministic and byte-preserving,
   so repairs are surgical and verifiable.
5. **The run log** — a durable, append-only record: one line per maintenance
   event. The queue is the working memory; the log is the history.

The requirements themselves are not in the skill. They live in the
**G-brain documentation contract** (`mybizz-config-docs/gbrain/`), a
developer-approved artifact with explicit change control: the skill enforces
the contract as written and may never extend, reinterpret, or quietly add
requirements. That separation is deliberate — what G-brain requires is an
architectural decision owned by the developer; the maintainer only ever answers
"does this saved document satisfy the known requirements," never "what should
G-brain require."

## Feature Summary — conceptual

- **Save-event maintenance** for four change kinds — creation, modification,
  move/rename, deletion — each with a bounded, defined work list.
- **Contract enforcement**, not taste: frontmatter is exactly `title` +
  `doc-id` = filename stem and nothing else; wikilinks use the required form
  and resolve; link targets exist; the applicable register is current on
  exactly four events.
- **Deterministic repair**: byte-preserving frontmatter repair and one-row
  register edits make every change surgical, verifiable, and safe.
- **Anti-work-generation**: an explicit not-required list (tags, numbering,
  density targets, perfect metadata) and a prohibition list keep the maintainer
  from generating work out of mere difference.
- **Classification of findings** into must fix / can wait / doesn't matter /
  requires human judgement — with "can wait" explicitly never becoming a new
  work queue.
- **Minimal reporting**: concise summary by default, full detail on request.
- **A durable audit trail** of every maintenance event, and an always-on
  watcher so saves are never missed between invocations.

## Suitability

**Best for:** keeping the documentation of an active development session
G-brain-usable — after saving a new document, after editing one, after renaming
or deleting one, the affected documentation is compliant again within one
invocation, with no effort from the developer.

**Good for:** first-import hygiene of newly created documents (frontmatter,
registration, wikilinkable references surfaced); surfacing genuine ambiguity
(ambiguous link targets, undeterminable registration) as concise decision
requests instead of guesses; maintaining the registers as a side effect of real
events rather than as a bureaucracy.

**Not good for:** whole-corpus health assessment — the maintainer examines only
what a saved change affected, by design; a periodic estate-wide examination is a
different job, not this one. Anything requiring mechanical guarantees — the
maintainer is advisory tooling; the files remain the only authority. Scheduled
or continuous cleaning — the maintainer runs when invoked on queued events and
never on a timer; nothing here puts maintenance on a schedule.

## Why Save-Time Rather Than Periodic

The maintainer's value comes from timing, not coverage. A save is the moment a
change is real but still fresh — the affected references are known, the intent
is recent, and the repair is small. The same checks run later, against an aged
corpus, lose the context that makes mechanical repair safe: which replacement
was "correct," which rename was intentional, which difference is deliberate.
The always-on watcher exists so that no save is ever missed between
invocations; the invocation-triggered drain exists so that no maintenance runs
unattended. Both halves of that split are deliberate: the watcher is
autonomous because observing is safe; the maintainer is invoked because acting
should have a human present.

## Why the Contract Is External — and Why Frontmatter Is Two Fields

A maintainer that "knows" what documentation should look like will inevitably
enforce taste: tidier tags, denser links, prettier metadata. Every one of those
is invented work the developer never asked for. The contract inverts that: the
maintainer may enforce only what the contract states, must record what is not
established rather than invent it, and carries an explicit not-required list.
Frontmatter exclusivity (`title` + `doc-id`, nothing else) is the clearest
example: legacy fields (`document:`, `state:`, `date-created:`, tags) are not
optional — they are prohibited, and repair deletes them. The reason is
integrity, not tidiness: `title:` is the only reliable title source for this
corpus (H1s are inconsistent), G-brain does not read the legacy fields, and a
repair that "preserved" them would preserve drift.

## Why Registers Move on Exactly Four Events

A register that changes on every content edit becomes an approval bureaucracy —
every save drags a table update behind it. The four-event model (creation,
supersession/retirement, rename, quarantine) encodes the only moments a
document's identity actually changes. Content edits need no register edit,
because the register registers documents, not their contents. And registers are
append-only: a deleted document's row becomes `Retired` rather than vanishing,
so history is never silently rewritten and a later reference to a retired
document can be explained rather than guessed at.

## Why the Tools Are Byte-Preserving

Maintenance edits documents the developer just wrote. A repair that reflows the
whole file would destroy work and make every change unverifiable. Both tools
replace only the affected byte range — the frontmatter block, or one register
row — leaving every other byte identical, and the test suite proves that
discipline (including CRLF bodies, missing trailing newlines, and unicode).
This is what makes automatic repair safe enough to not require approval: the
blast radius of a repair is exactly the defect.

## Where It Sits in the System

The maintainer consumes the **scope authority** (`mybizz-scope-list.md`) live
at every run — it carries no scope list of its own — and the **G-brain
documentation contract** as its requirement source. It is downstream of the
**watcher** and upstream of nothing: nothing builds, deploys, or enforces on
its output. It maintains **registers** as part of normal maintenance, never as
a separate bureaucracy. Its own artifacts live in three layers: source repo
(`C:\mybizz\mb-doc-maintainer`, GitHub-backed), installed skill (WSL
`~/.config/opencode/skills/`), and suite documentation (this folder). Its
GBrain source registration is for searching the skill spec itself — ingestion
of the corpus is G-brain sync's job, never the maintainer's.

The maintainer's own plumbing obeys its own rules: the run log carries exact
two-field frontmatter and a register row (it is a permanent corpus document);
the queue and watcher log live under the logs exception and are never
registered; the watcher never queues events for its own log, so the pipeline
cannot feed itself.

## Two Real Mistakes, Found While Building

**A script that PowerShell could not parse.** The watcher originally contained
em dashes — ordinary typographic punctuation in comments and one warning
string. PowerShell 5.1 reads BOM-less UTF-8 as ANSI, where one byte of the em
dash decodes as a curly quote, which PowerShell treats as a string delimiter.
The file parsed as Python but not as PowerShell. The fix — keep `.ps1` scripts
pure ASCII and re-run the parser check after every edit — is now a standing
rule in [[doc-maintainer-reference|Reference]].

**An event format with a hidden BOM.** The watcher's event writer used
`Set-Content -Encoding UTF8`, which in PowerShell 5.1 writes a UTF-8 BOM —
harmless to PowerShell, a real hazard for any strict JSON reader. The writer
now emits BOM-less UTF-8 explicitly. Both findings are examples of the same
lesson: this pipeline straddles WSL and Windows, and the boundary has its own
failure modes that only live execution surfaces.

## Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the suite files, and the exam cycle that runs them, are the
architecture described in [[config-manager-explainer|Explainer]]. The short
local version:

- [[doc-maintainer-config|Configuration]] is the **spec** — the ideal state
  every exam checks against.
- Before each run, the config-manager synthesizes
  [[doc-maintainer-exam-plan|Exam Plan]]: a fresh job-spec built from this
  spec, the last report, the log, and the learnings — carrying forward what was
  deferred, addressing what erred, deriving probes from new log events, and
  folding in lessons not yet graduated. The plan is transient.
- The exam runs the installed skill (`mb-config-doc-maintainer`) with the plan
  in hand — detection fully autonomous; healing gated. Suite-file repairs are
  the only agent-healable class; the watcher task, the subject skill, the
  contract, and any sync execution are developer-gated or deny-listed.
- **Scope boundary with the gbrain module:** GBrain binary/version/models/
  schema-pack/MCP/sync conformance belongs to `mb-config-gbrain`; this exam
  reads only the `mb-doc-maintainer` source row's existence/federated/lag/
  coverage reading and cross-references the parent's report instead of
  re-probing.
- The run rewrites [[doc-maintainer-exam-report|Exam Report]] (current state,
  no history), appends one row to [[doc-maintainer-log|Log]], files new
  learnings, and prunes absorbed entries.

## S.W.O.T.

**Strengths.** The pipeline is proven end-to-end on a live event (save →
watcher → coalesced event → tool-checked maintenance → verified → logged);
byte-preserving tools make every repair surgical and test-proven (40/40); the
contract separation means the system cannot invent requirements; the watcher is
always-on with single-instance and crash-restart guarantees.

**Weaknesses.** Live verification so far covers one modification event —
creation, move/rename, and deletion are proven on corpus copies and in the
suite's tests, not yet on live saves; the `anvil.yaml` class-rule exclusion is
code-inspection-verified only (a live test needs a fixture the environment
forbids the agent from building); the maintainer acts only on invocation — saves
accumulate in the queue until something drains it.

**Opportunities.** The exam cycle makes silent degradation of the pipeline — a
stopped watcher, a divergent installed skill, broken tools — detectable on
demand; the four-event register model keeps registration honest without
bureaucracy; the suite docs carry the open items (suite-doc register rows,
code ingestion) as explicit, gate-resolvable states rather than drift.

**Threats.** The pipeline straddles the WSL/Windows boundary, whose encoding
and quoting failure modes are real (two were found and fixed at build time);
an uninvoked maintainer could let events pile up harmlessly but indefinitely —
the designed answer is invocation discipline, not automation of the acting
half; upgrades or policy changes to G-brain itself would change the contract's
ground truth — the contract's change control is the mitigation.

## Deliberately Out of Scope

The maintainer is not a document-management system, not a corpus cleaner, and
not an auditor: it never perfects the estate, never searches for unrelated
problems, never processes historical inconsistencies, never creates work from
mere difference, and never becomes a smaller cleaning cycle. Where a finding is
real but outside the event, it is classified "can wait" and explicitly never
becomes a new work queue. Where judgement is genuinely required, the maintainer
asks — it never guesses to avoid asking. Those boundaries are not temporary
restraint; they are the component's contract with the developer, enforced by
the same prohibition list that every event run re-reads first.

## Honest Limits

- The `anvil.yaml` class-rule exclusion is verified by code inspection only — a
  live test would require creating an `anvil.yaml` fixture, which the
  environment forbids.
- The watcher's kind classification is heuristic (rename plus content change
  classifies as modification) — correct for editors' atomic-save patterns, not
  formally exhaustive.
- Events accumulate harmlessly if the maintainer is never invoked; nothing
  syncs, repairs, or logs by itself. Always-on applies to observing, not
  acting — that is the design split, not a defect.
- The first live verification covered one modification event; creation, rename,
  and deletion are proven on corpus copies and in the test suite, not yet on
  live saves.

---

*Suite: [[doc-maintainer-config|Configuration]] (spec), [[doc-maintainer-reference|Reference]]
(commands and procedures), [[doc-maintainer-exam-plan|Exam Plan]] /
[[doc-maintainer-exam-report|Exam Report]] / [[doc-maintainer-log|Log]] /
[[doc-maintainer-learnings|Learnings]] (config-management set),
[[doc-maintainer-skill|Exam Skill]] (standing check inventory). Requirements
source: `gbrain/gbrain-doc-contract.md`. Governing plan:
`mb-doc-maintainer — Complete Consolidated Plan.md` (doc-auditor-maintaner-planning).
Architecture: [[config-manager-explainer|Explainer]].*

*End of document*