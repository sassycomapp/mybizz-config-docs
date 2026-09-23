---
document: "The mb-doccycle Documentation-Management Workflow"
doc-id: doccycle-explainer
state: Live
date-created: 2026-09-22
---

# mb-doccycle — The Documentation-Management Workflow (Explainer)

Companion note: this system is examinable — the standing check inventory
lives in [[doccycle-skill|the exam skill]], each run is driven by
[[doccycle-exam-plan|the exam plan]] synthesized fresh by the
config-manager, and outcomes are recorded in [[doccycle-log|the log]] and
[[doccycle-exam-report|the exam report]]. The exam is detection and
verification only — the workflow is working well and nothing gets fixed
without the developer's gate decision.

Why the workflow exists, why it has the shape it has, and what it
deliberately does not solve. For current state see
[[doccycle-config|mb-doccycle Configuration]]; for commands see
[[doccycle-reference|mb-doccycle Usage and Invocation]]; for the binding
run frame see [[doccycle-run-discipline|mb-doccycle — Shared Run
Discipline]].

---

## The problem it solves

Three separate skills once covered documentation management: a structural
manager, a content-consistency checker, and a wikilink converter. Each had
its own ceremony, its own corpus assumptions, its own governance header,
and its own learnings folder — and each drifted independently from the
developer's rulings. The 2026-09-21 architecture review found the
consequences: inconsistent state across three texts, duplicated ceremony,
independent and contradictory corpus rules, inconsistent governance at the
point of failure, and partial-corpus runs that broke the product-then-
packaging order. One merged workflow with one shared run frame ends all
of it — but only together with a canonical detection tool; the merge
without the tool would just re-create the same defects in one file.

## Why three sequential phases

The sequence is product-then-packaging. Phase A fixes where things are
(structure, docmaps, registers, INDEX files); Phase B fixes whether the
content agrees (references, front matter, identity/lifecycle); Phase C
converts what is already correct into GBrain-resolvable links. Conversion
last, because converting a wrong reference just makes a broken link
permanent and pretty. B-close is a hard gate before C; C's
missing-document findings trigger one bounded B re-pass and nothing more,
so the cycle cannot spiral.

One corpus per cycle is the layer-consistent working unit: the three
phases must see the same corpus state (A's structural fixes change the
paths B repoints and C converts). project-library-global joins every
cycle as the read-only resolution universe — its basename listing
resolves cross-corpus links and the directionality check — but takes no
writes from a local run; it receives full cycles only on its own
scheduled runs. Cross-corpus work never exists in both directions at
once: global docs never trackably reference local corpora (that is what
the healed-prose form is for), so a local change can never break global,
and vice versa.

## The canonical tool decision (Phase C)

The fifteen-cycle defect family that produced the retired skills (CRLF
corruption, spaces in paths, self-references, substring collisions,
double-occurrence tokens, malformed brackets, invisible bytes) came from
detection-and-apply being improvised per run. The remedy is tested code:
`doccycle-detect.py` enforces the proven invariants mechanically
(byte-preserving, line-precise, unique-context, backtick-first, check=True),
emits exact old-string → new-string pairs, and never writes — apply goes
through the governed file tools, verified by diff against the phase
backup. The tool's defect-family test suite (27 tests, 19 fixtures) is
the institutional memory of every defect that ever cost a re-run.

## Coexistence with enforcement (the grants design)

The workflow writes into restricted project folders and commits into git
repos — both governed by Cupcake. Rather than weakening enforcement, the
design clones the proven grant pattern: path slips (`mg-grant`) for
folder writes, commit allowances (`git-grant`, decision G1) for
commits — bounded, expiring, developer-issued, mechanically verified by
the compiled policies. Slips are requested COLLECTIVELY (one
copy-pasteable block per cycle, counts pre-determined), never one at a
time. A Cupcake denial is final for that call: report it, obtain the
developer's instruction, never work around. The
[[cupcake-config|Cupcake Configuration]] suite documents the enforcement
side.

## The false-alarm doctrine

Every finding triages into exactly one of three kinds. Legitimate-minimal:
real, consequence-free (a register row asserting a home a file has
legitimately left during development flux) — set aside. Illegitimate: an
alarm with no cause — a defect in the detection logic itself, corrected
through the rule pipeline (an amendment is a commit to the git-backed
source), never dismissed as noise, never a file forced into a mold.
Legitimate-requires-attention: real and consequential — decide and
implement. Misclassified flags corrupt trust in the whole system; this
doctrine is the structural counter to remediation-as-error on a corpus in
deliberate flux.

## Why the run frame lives outside the skill text

Skill text is what the agent reads at the moment of failure — so the
developer's rules sit in the skill's first lines (the governance header).
But the shared cycle (backups, approvals, grants, verification, commits,
sync) is one discipline shared by every phase: it lives once in
[[doccycle-run-discipline|the run frame]], and each phase spec adds only
its own specifics. Duplication across files was the drift machine of the
three-skill era; single-sourcing is the structural answer.

## What it deliberately does not solve

- **Residual run duration** — inherent detection time stays; the ceremony
  overhead was the architectural target.
- **Developer rulings on vendor corpora, directionality of new kinds,
  alignment-log semantics** — the workflow is agnostic to outcomes;
  rulings change phase-spec content, not shape.
- **Dream-cycle staleness** — an operational GBrain item the close
  protocol reports, not an architecture concern.
- **No new infrastructure** — no scheduler, no orchestration platform, no
  database. The one new machinery is the detection tool, and it replaced
  improvisation, not a platform.

## Supersession

This workflow supersedes the three retired skills (mb-docs-manager,
mb-align-docs, mb-wikilinks) and their shared run frame
(`doc-skills-run-discipline.md`, retired in place 2026-09-22). Their
proven rules were absorbed into the phase specs and the run frame; their
sub-agent architecture was retired (no sub-agents, no exceptions — G4);
their pre-ruling texts were corrected where the rulings changed them
(directionality, quarantine, alignment-log semantics). The old skills and
their suite folders were removed 2026-09-22 (WP7, developer-confirmed;
39-file verified backup); their logs and run records remain as historical
archives.

## Config maintenance

The configuration suite for this system is maintained by the
configuration-management cycle: [[doccycle-skill|the exam skill]] exams
live state against [[doccycle-config|the spec]] under
[[doccycle-exam-plan|a fresh exam plan]], catches silent failures, and
heals only through the developer gate. Learnings are transient
([[doccycle-learnings|way-station]]); the log records events
([[doccycle-log|log]]).

## S.W.O.T. (2026-09-22, suite build-out state)

- **Strengths:** one git-backed text ends the drift machine; the canonical
  detector is tested code (27 tests, defect-family fixtures); grants
  coexistence proven live (G1); the retirement residue is verified and
  archived; the acceptance run exercised the full cycle end to end.
- **Weaknesses:** two detector defects queued (folder-token suffix
  matching; empty display; universe scaffold filtering); the suffix-variant
  matcher remains semantically loose (wrong-target pairs relied on the
  triage layer — by design, but noisy).
- **Opportunities:** universe construction gains scaffold filtering as a
  run-frame step; the amendment ride makes the detector's false-alarm
  classes fail mechanically rather than by triage.
- **Threats:** muscle memory to the retired skills (all references healed
  or retired); grant expiry mid-cycle (the observed re-grant-replaces-
  count behavior); the scope scaffold's skill-name list pending a
  developer-owned update.

## Companion documents

| File | Orientation |
|---|---|
| [[doccycle-config|Configuration]] | Ideal — the spec |
| [[doccycle-reference|Reference]] | Agent-facing commands |
| [[doccycle-run-discipline|Run Discipline]] | The binding shared frame |
| [[doccycle-skill|Exam Skill]] | Standing check inventory |
| [[doccycle-exam-plan|Exam Plan]] | Next run's job-spec |
| [[doccycle-exam-report|Exam Report]] | Last run's verified state |
| [[doccycle-log|Log]] | Events, not lessons |
| [[doccycle-learnings|Learnings]] | Transient way-station |