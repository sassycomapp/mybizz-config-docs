---
document: "The mb-doccycle Documentation-Management Workflow"
doc-id: doccycle-explainer
state: Live
date-created: 2026-09-22
---

# mb-doccycle — The Documentation-Management Workflow (Explainer)

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
paths B repoints and C converts), directionality validation needs the
target corpus and project-library-global in the same run, and one cycle
is already hours of work — sequential cycles give natural checkpoints and
limit session loss.

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
(directionality, quarantine, alignment-log semantics). The old skills'
learnings and run records remain as historical archives — nothing
deleted, nothing moved (WP6 handles the learnings supersession sweep).