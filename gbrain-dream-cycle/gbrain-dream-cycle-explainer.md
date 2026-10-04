---
title: "gbrain-dream-cycle-explainer"
doc-id: "mb-957d54e7"
updated: "2026-10-04"
---
# GBrain Dream Cycle — Explainer

*Companion note: for current confirmed state (invocation model, provider
dependency, acceptance-test record, open items) see
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md). For commands and the mandatory post-run
verification procedure, see [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md). For how this
system is examined and kept healthy by the config-management apparatus, see
§8 below and the suite's exam set ([[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-exam-plan.md) /
`-exam-report.md` / `-log.md` / `-learnings.md`). For the full 23-phase
sequence and the cross-component framing, see [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md)
§4.*

---

## 1. What It Actually Is

The Dream Cycle is GBrain's own deepening mechanism: a long, fixed sequence of
23 phases that runs against everything already stored in the brain and tries
to build a deeper, more structured understanding of it — extracting facts,
attempting code-symbol relationships, scanning for contradictions, synthesizing
concepts across documents, proposing and grading its own interpretive
conclusions, and maintaining the brain's hygiene. Ordinary GBrain search
answers "find me something related to X"; the Dream Cycle does the different
kind of work that makes GBrain's memory more than a pile of separately-
searchable pages.

Two framings of its phase structure exist, both recorded with provenance: the
confirmed 23-phase sequence for this environment — now live-verified in exact
order by the 2026-09-06 acceptance run (master explainer §4: housekeeping,
extraction, synthesis, judgment/calibration, maintenance) — and upstream's
simplified harness-side framing (entity sweep → citation repair →
consolidation → sync). The 23-phase list is the operative one here.

Three structural facts define it. **It is advisory** — it operates only on
GBrain's stored content, has no authority over real files, and nothing it
produces overrides a repository, an ADR, or a spec. **It is ungovernable** —
Memory Governor structurally cannot intercept it (a permanent, exhaustively
verified limit), so its output reaches durable memory unreviewed; the
compensation is a manual, always-applied discipline: every dream run is
followed by a suspected-contradictions evaluation whose findings get reviewed.
And — the deliberate design choice confirmed 2026-09-06 — **it runs only when
invoked.** An autopilot schedule that would have run it every five minutes was
found completely inert (the cron daemon never ran; its target path predated
the current machine layout; its log file had never been created) and was
removed. On-demand invocation is the intended design, not a gap.

## 2. What It Can Actually Do

- **Fact extraction** (`extract_facts`, `extract_atoms`) — pull discrete, structured facts out of stored documents; `extract_atoms` makes its own Anthropic calls and is the phase most exposed to credential failure.
- **Code-symbol relationship resolution** (`resolve_symbol_edges`) — GBrain's own attempt at the call graph, permanently partial (see Limitations).
- **Contradiction surface** — the cycle's output feeds the suspected-contradictions evaluation that follows every run.
- **Concept synthesis and pattern-finding** (`patterns`, `synthesize_concepts`, `consolidate`) — higher-level concept pages summarizing many individual facts; near-duplicate consolidation. The verified acceptance run produced +89 synthesized concept pages.
- **Self-judgment and calibration** (`propose_takes`, `grade_takes`, `calibration_profile`, `drift`) — the system proposing interpretive conclusions, grading its own confidence, and tracking drift.
- **Maintenance and closure** (`enrich_thin`, `embed`, `orphans`, `schema-suggest`, `purge`) — filling thin pages, embedding new content, disconnecting orphans, suggesting schema improvements, removing what is genuinely no longer needed.

## 3. Suitability

**Best for:** periodic deepening of an already-synced brain — after ingestion
bursts, before design or review work that depends on synthesized understanding;
surfacing contradictions between stored documents; keeping concept pages and
fact coverage current without manual per-page effort.

**Good for:** source-scoped refreshes (`--source`) after heavy work in one
project; targeted single-phase re-runs during diagnosis; the emotional-weight
and calibration passes that keep GBrain's self-assessment honest.

**Not good for:** replacing `gbrain sync` — different operations, different
bookkeeping; a dream that "completed" does not mean sources are fresh, and
freshness counters do not prove a dream did work. Producing governed memory —
its output is structurally outside Memory Governor's reach, which is why the
post-run contradiction discipline exists. Running autonomously — deliberately
rejected here after its scheduled mechanism was found inert; unattended dream
runs would compound exactly the silent-failure risk its own incident history
documents. Resolving the code call graph — permanently partial; Graphify owns
that.

## 4. Why Manual-On-Demand, and Why the Incident Justifies It

Upstream designs the dream cycle as a nightly cron — "the most important cron
job," running while you sleep, part of a 20-job autonomous schedule. This
environment ran the opposite experiment without meaning to: an autopilot
schedule was installed in the old machine-layout era and never fired once —
the cron daemon was never running, its target path died in a layout move, and
its log file was never created. Three independent signals of total inertness,
discovered only when deliberately checked.

The incident history supplies the reason the on-demand choice is right here:
the one confirmed extended dream-cycle outage (every run, every source,
failing at `extract_atoms` with a bare "5 failed" count) was **silent** — the
real error existed in the code but was never surfaced, and finding it required
temporarily instrumenting GBrain's own source. A failure mode that hides its
own cause is precisely the kind of thing that must not run unattended: an
autonomous dream cycle failing silently would degrade the brain's quality for
weeks exactly as it did before, invisibly. On-demand invocation means a human
is present at every run, and the mandatory post-run verification procedure
means every run's real work is checked, not assumed — the 2026-09-06
acceptance run was the procedure's first live application, and it immediately
proved its worth by catching a broken diagnostic recipe and a stale
discipline command before they reached documentation.

The removal itself was the design decision made explicit: the inert autopilot
was removed on 2026-09-06 (crontab entry and script; the log never existed),
and on-demand invocation was confirmed as the intended design — not a gap
awaiting a fix.

## 5. A Real Incident Worth Understanding, Not Just Noting

For a real stretch of time, every Dream Cycle run, across every registered
source, failed completely at the `extract_atoms` phase — and the tool's own
summary output never explained why. It reported a bare count: "5 failed," with
no further detail, no matter how many times it was re-run.

The actual cause required direct investigation: `extract_atoms` uses its own
Anthropic API key, and that key had quietly expired. The real error — "API key
is invalid" — existed in the code but was silently swallowed and reduced to a
bare failure count. Finding it required temporarily adding one diagnostic line
directly into GBrain's own source, catching the real message on a single run,
then removing the diagnostic line immediately afterward.

Fixing the key wasn't the end of it. The replacement key, once pasted into its
configuration, had picked up a single stray line break inside its quoted
value — invisible on a plain read of the file, but enough to corrupt every
request using it, producing a completely different, misleading "invalid JSON"
error with no obvious connection to the real problem.

**Why this belongs here:** both failures share the same lesson, and it applies
every time a dream run reports a bare failure count — go find the actual
underlying error rather than accepting "it just doesn't work" as an answer. A
clean-looking config file is not proof the value inside it is actually clean.
It is also the reason the post-run verification procedure exists in its
current form: a completed run is not proof of real work.

## 6. Where It Sits — The Six-Component System

Within the six-component memory system (developer-stated framing; see
[[[mybizz-config-docs:gbrain/gbrain-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md)), the Dream Cycle is the autonomous-deepening layer of
GBrain itself — the third component in the grouping. Its relationships:
**GBrain** owns it (it deepens GBrain's own stored content); **Memory
Governor** cannot see it (the structural non-interception limit; the manual
contradiction discipline is the standing compensation); **PostgreSQL** carries
its output; **mb-submit-memory** is its governed opposite — the two paths
write different layers (facts vs pages) and neither substitutes for the other;
**gstack** supplies the `/sync-gbrain --dream` trigger, whose orchestrator
carries a real source-overlap trap with a confirmed incident. The
four-mechanism framing (master explainer) places it as the third mechanism,
with the same permanent limits. External recognition: another memory project's
feature request (claude-mem#1792) models its own consolidation directly on
this cycle — "the dream cycle is NOT optional; without it, signal leaks out of
every conversation" — evidence the design is the differentiator, and equally a
description of what an unattended, silently-failing dream cycle leaks.

## 7. Known Limitations, Honestly Stated

**`resolve_symbol_edges` does not close the call-graph gap.** GBrain's own
attempt, permanently partial — `code` is `extractable: false` in every bundled
pack. Graphify remains the tool of record for resolved cross-file
relationships.

**Failures can be silent.** A phase can fail and report only a bare count.
§5 is the standing reminder; the per-phase JSON procedure is the standing
answer.

**Provider dependency.** `extract_atoms` requires a valid, current Anthropic
key — the confirmed cause of the one extended outage. Check credentials first
when it fails (verified valid 2026-09-06).

**"Completed" is not "worked."** The cycle reaching its end says nothing about
whether each phase did meaningful work — on the verified acceptance run, 11 of
23 phases legitimately skipped and one warned (orphan backlog) while the run
still produced +89 pages. The verification procedure exists because of this,
and the autopilot finding adds the corollary: an unattended cycle cannot be
verified at all, which is why there are none.

**The orphan backlog is real.** 1,177 of 1,755 pages have no inbound links
(verified 2026-09-06; not re-measured since, the brain now holds about 2,450
pages) — the deepening passes create content faster than linking covers it.
Recorded as an open item, not a failure of the mechanism.

**Links between repositories are not its job.** The cycle's `extract` phase reads
one source at a time, so it cannot resolve a link that points into another
source. Those links are written by the full read at the end of the sync script
(`gbrain extract links --source db`). A dream run therefore neither creates nor
replaces them; if they are missing after a run, that command restores them.

## 8. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md) — emulated from the
PostgreSQL pilot. The short local version:

- [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md) is the **spec** — the ideal state every exam
  checks against. The dream cycle is working well; the exam verifies that and
  changes nothing.
- Before each exam run, the config-manager synthesizes
  [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-exam-plan.md): a fresh job-spec built from this spec,
  the last report, the log, and the learnings. The plan is transient (the file
  is live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-gbrain-dream-cycle`) with the
  plan in hand — detection fully autonomous; healing gated. **This module has
  no agent-healable items**: the Dream Cycle is part of GBrain (a memory
  system governed elsewhere), and every repair is developer-run or proposed.
- **Scope boundary with the parent gbrain module:** binary, version, config,
  schema-pack inventory, sources, models, MCP integration, and sync machinery
  belong to `mb-config-gbrain` (this exam cross-references; a version echo is
  the one permitted overlap). Database conformance and the estate backup
  convention belong to `mb-config-postgresql`. Resolved code call-graph work
  belongs to Graphify.
- Several checks are permanently **developer-run**: `config.json` content
  (sensitive-data guard — proven class), the Anthropic key-validity curl if a
  guard denies the agent attempt, and everything in Tier 3 (a full dream cycle
  is expensive and content-changing; the upgrade decision is the developer's).
- The run rewrites [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-exam-report.md) (current state, no
  history), appends one row to [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-log|Log]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-log.md), files new
  learnings, and prunes absorbed entries.

## 9. S.W.O.T.

**Strengths.** The mandatory post-run verification procedure (proven live —
"completed" is never accepted as "worked"); the deliberate on-demand design
with the inert-autopilot incident as its justification; every failure mode and
known limitation documented with its root cause, not just its symptom.

**Weaknesses.** Full verification of a real run is expensive (minutes, LLM
spend, +N pages) and stays developer-gated; several checks are permanently
developer-run (config content, credential validity); the orphan backlog grows
with every deepening pass (content-hygiene debt, by design unmanaged by the
cycle itself).

**Opportunities.** The config-management exam adds standing verification that
never existed between runs: the scheduling-absence check, the trigger-surface
inventory, the schema-pack coupling, and a cheap functional probe — catching
the silent-failure class (the historical `extract_atoms` outage ran
undetected for a long stretch) before it compounds.

**Threats.** Failures can be silent (a bare count hiding the real error); the
`extract_atoms` credential is a single point of failure with a confirmed
outage history; an unattended or scheduled dream run would compound exactly
the silent-failure risk the incident history documents — hence the deliberate
on-demand design, whose violation the exam watches for.

---

*Companion documents: [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-config|Configuration]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-config.md) (the spec),
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-reference|Reference: Invocation, Verification, Diagnostics]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-reference.md) (procedures and post-run verification),
[[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-exam-plan.md) / `-exam-report.md` / `-log.md` /
`-learnings.md` (config-management set), [[[mybizz-config-docs:gbrain-dream-cycle/gbrain-dream-cycle-skill|Gbrain Dream Cycle Skill]]](C:/mybizz/mybizz-config-docs/gbrain-dream-cycle/gbrain-dream-cycle-skill.md) (exam
skill canonical source). Architecture: [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md).
Cross-component framing: [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md) §4.*
