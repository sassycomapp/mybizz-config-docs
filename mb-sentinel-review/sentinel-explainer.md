---
title: "sentinel-explainer"
doc-id: "mb-d54f779d"
updated: "2026-10-20"
---
# Sentinel — What It Is and Why It Works This Way

Companion to [[[mybizz-config-docs:mb-sentinel-review/sentinel-config|Sentinel Configuration]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-config.md) (values) and
[[[mybizz-config-docs:mb-sentinel-review/sentinel-reference|the reference]]](C:/mybizz/mybizz-config-docs/mb-sentinel-review/sentinel-reference.md) (procedures and worked examples).

## What it is

The applications built through PDLF hold real client money, real client
data, and real personal information belonging to their clients' own
customers — and every line of their code is written by an AI agent.
Regulatory duties (POPIA) make protecting that data mandatory for every
application, not optional. Sentinel is MyBizz's answer: the step-triggered
security review for PDLF. At defined steps it reads the real
security-standard documents, reasons about the real feature being built,
records the outcome in the PDLF ledger, and stops. It flags and proposes;
it never fixes. It is build-time safeguarding in service of
shipped-application safety, and it is part of PDLF itself — pre-built into
specific steps, at the specific moments where security weight sits. It is
not a standalone security agent, and it does not run continuously.

## What it can do

- Check any step number against the intensity table, and decline instantly
  when a step carries no security scrutiny.
- Identify the specific security-global documents that apply to a step and
  a feature — and read them in full before judging.
- Reason about the real feature against those documents' approved and
  prohibited patterns, using the `secure-software-engineering` methodology.
- Reach one of three outcomes — CLEAR, FLAG, ESCALATE — and write a real,
  structured ledger row for every reviewed outcome, CLEAR included.
- Prove, at a step's own gate, that a review actually ran.
- Present a finding in plain words: what the review found, how severe, how
  confident, and what control is recommended.

## Suitability

**Best for:** narrow, build-moment security questions tied to a PDLF step,
where the answer requires reading a real standard and judging a real
feature — and for making security review provable rather than assumed.

**Good for:** catching the platform's own characteristic mistakes —
multi-tenancy patterns, within-instance access-control flaws, secrets
entering public repositories.

**Not good for:** whole-codebase sweeps (GStack's `/cso`); general code
review (the `/review` security specialist); mechanical, always-on
enforcement (Cupcake); the memory governor's review queue; continuously
running enforcement; the shipped estate's runtime safeguards; general code
quality (PDLF's own review and QA).

## Why it works this way

**Four layers, one job each.** The security-global library is the
authority — a real, written body of documents defining, in checkable
terms, what "secure" means for this project. GBrain is retrieval only,
never authority: it locates where knowledge lives, and the review always
reads the real, current document — never a GBrain summary of a security
rule. Sentinel itself is the reasoning layer: it decides when a security
question needs asking, based on which PDLF step just occurred, and applies
the library's standards to the real, specific thing being built. PDLF owns
enforcement: every finding becomes a row in PDLF's own findings table and
its ordinary triage discipline.

**Noise control by table.** Sentinel does not review everything at maximum
intensity — that would produce so much noise that nothing real would stand
out. Domain modeling gets a light check; creating a data table gets high
scrutiny; locking the architecture gets the highest; building real code and
reviewing that code get sustained, serious attention; QA asks whether the
security requirements can actually be demonstrated. A step not on the table
gets no review — a deliberate, stated choice.

**"I don't know" is a required answer.** A system built to only ever
answer "clear" or "flag" will, sooner or later, be forced into guessing
when it genuinely does not know — and a confident wrong guess is strictly
worse than an honest admission of uncertainty. ESCALATE exists so the
system never has to guess.

**Every flag is triaged into three kinds.** Legitimate with minimal
consequence: real, not worth work — set aside. Illegitimate: raised with no
real problem — that is a defect in the detection itself, corrected through
the rule pipeline, not merely dismissed. Legitimate requiring attention:
the normal case — decided by the developer, implemented by PDLF. Over-warning
is preferred to silence; the misclassification, not the flag, is what
corrupts the system's trustworthiness.

**The boundary it reviews within.** Cross-client data isolation on this
platform is structural — one Anvil application per client, one database per
client, `app_tables` resolving to the calling client's own tables — sealed
by the governing ADR. Multi-tenancy patterns are therefore security
findings, not idioms: they would replace structural isolation with a
failure-prone filter. The genuine threats live within an instance —
user-role access control, the Vault, input validation, server-side-only
data access — and the review concentrates on what the architecture cannot
solve: the quality of the code inside one client instance.

**Non-duplication, deliberately checked.** `/cso` sweeps the whole codebase
on a different rhythm; the `/review` security specialist reviews code
independently; Cupcake keeps honest agents honest — the same forbidden
action blocked identically every time, with no reasoning; the memory
governor's review queue is a separate review discipline for a separate
system. Sentinel is the reasoning layer for the questions that cannot be
reduced to a fixed pattern. Neither replaces the other.

**The security knowledge is MyBizz's own, confirmed rather than invented.**
Most of it already exists in MyBizz's specifications and ADRs — the Vault
system design, the RBAC role table, the five-app data-isolation model, the
payment-gateway decisions. Only the six categories without existing
coverage hold purpose-written `sec-` documents, each grounded in established
project fact.

**The methodology is borrowed.** The `secure-software-engineering` skill
supplies the reasoning process — a prevention-oriented workflow. Two
honesty notes: its multi-tenant isolation reference does not apply on this
platform (the governing ADR establishes structural isolation, so the review
vocabulary is within-instance), and a methodology is not enforcement —
nothing in it blocks a vulnerable function from shipping. Its value is a
better-informed reviewing agent at the moment of judgment.

**Every outcome leaves a trace, and invocation is proved.** A CLEAR writes
its own row, resolved immediately; a FLAG or ESCALATE writes a row and
stops for the developer. The gate-proof pattern means a step cannot pass
its own gate on the assumption that Sentinel ran — a verified ledger row
must exist first.

## What has to happen

- PDLF wires each intensity-table step as its step file develops: the
  invocation in the step's own procedure, and the gate-proof check before
  the gate.
- The intensity table and the ledger's `source_step` CHECK change in the
  same change.
- The developer triages every flag into its three kinds; PDLF's cycle
  implements; Sentinel never fixes and never resolves.
- The security-global library stays the one authority; new security
  knowledge lands there, not in the skill.
- GBrain stays retrieval-only for security truth.
- The suite's four documents stay current with the live system.
- The reasoning is self-review by the writing agent; checkable patterns,
  evidence-required rows and independent tools reduce the risk, and the
  developer's triage of every flag is the standing control.
- Sentinel is untested against a real feature; the first real PDLF-run
  feature is the test that matters — expected naturally at PDLF build time,
  with no special effort.
