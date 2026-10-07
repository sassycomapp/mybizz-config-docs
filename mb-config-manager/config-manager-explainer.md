---
title: "config-manager-explainer"
doc-id: "mb-c28cb8f9"
updated: "2026-10-07"
---
# mb-config-manager — Explainer

The authoritative narrative of the configuration-management system: what it is,
why it exists, how it works, everything about it. Multi-audience — written for the
human developer, a visiting technical consultant, and the agent. Companion files:
[[[mybizz-config-docs:mb-config-manager/config-manager-config|Configuration]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-config.md) (its own configurations), [[[mybizz-config-docs:mb-config-manager/config-manager-register|Register: Managed Systems]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-register.md)
(what it manages, current state), [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md) (agent-facing
procedures), [[[mybizz-config-docs:mb-config-manager/config-manager-agent|Orchestrator Agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md) (the orchestrator itself), [[[mybizz-config-docs:mb-config-manager/config-manager-log|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md) (notable events), [[[mybizz-config-docs:mb-config-manager/config-manager-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-learnings.md)
(transient knowledge).

---

## 1. Why this system exists

The developer's working life is dominated by building PDLF. When PDLF work is
underway, there is no capacity to stop and manage system configurations — check
whether a policy engine still enforces, whether a database matches its spec, whether
an installed skill still works. Yet every system on this machine quietly degrades in
exactly those ways. This was proven painfully: Cupcake — the mechanical policy
enforcement layer — once passed offline validation 17/17 while silently doing
nothing live; a scaffold file that "existed" broke the entire evaluation engine so
that every tool call failed. The class of failure is always the same: **present ≠
working**. Existence checks pass; the system is dead.

The config-management system exists so that configuration health is maintained by
a standing apparatus instead of by the developer's attention. The developer works
on PDLF; this system watches the estate and presents findings for gated repair.

## 2. What it is

Configuration management for the live systems this machine runs. It exams each
system's actual state against its config artifacts (`.yaml`, `.json`, `.gitignore`,
`.env`, service/boot configs), catches silent failures, and heals only through a
developer gate. It runs **on demand** — never scheduled, never background. It owns
live systems and their config artifacts, not documents: documents are maintained
by the agents doing the work, with the developer's approval, and checked at every
commit by `mb-doc-check`. The boundary in one line: the documentation process
keeps the *paperwork* truthful; this keeps the *systems* healthy.

## 3. What it consists of

- **The orchestrator agent** — `mb-config-manager`. An agent, not a skill (hence
  [[[mybizz-config-docs:mb-config-manager/config-manager-agent|Orchestrator Agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md), no skill file in its own suite). It routes exams,
  synthesizes each system's exam-plan, aggregates findings, runs the approval
  gate, owns the standards (verdict classes, heal classes, safety invariants).
  It owns no system. Its draft lives here; it moves to its install location when
  built.
- **System exam skills** — one per system, separate, sized to the system
  (`mb-config-postgresql`, `mb-config-cupcake`, ...). Each holds the standing exam
  procedure for that system (static, growing only by graduation), its heal
  allowlist, and its deny-list. Each lives as a canonical, git-versioned source
  at `{system}/{system}-skill.md` in its system folder; at install its text below
  the frontmatter is **copied** (never moved) to
  `~/.config/opencode/skills/<skill-name>/SKILL.md` — the installed copy is the
  only *executing* copy (the suite folder is not skill-scanned, so no
  double-load), while the source stays in the repo as backup and drift-detection
  anchor (step-0 check). The two differ only in frontmatter, by design: the source
  is a document and carries `title`, `doc-id` and `updated`; the installed copy is
  a skill and carries `name` and `description`, which OpenCode needs to load it.
- **System config docs** — each system's `{system}-config.md` is the spec its exam
  runs against. Examined, never maintained, by this system: drift is raised as a
  gate item with a proposed correction, and the correction is applied only after
  the developer approves it.

## 4. Invocation

- `/mb-config-manager (all)` — developer-initiated **system-wide health scan**:
  every Installed system is exam'd.
- `/mb-config-manager (system)` — **targeted single-system exam** (e.g.
  `/mb-config-manager (postgresql)`): used when the developer feels there is a
  problem with a particular system, or an agent has reported config problems on
  one.

Both forms trigger the same cycle (below); the invocation form determines scope
only.

## 5. The exam cycle (one run — plan-driven)

1. **Self-validation (step 0)** — verify its own functional consistency: register
   rows ↔ installed skills ↔ suite files agree. A self-check, never a self-exam
   (Section 9). Inconsistency = architecture defect → its own log/learnings →
   developer.
2. **Synthesize the exam-plan** for each target system — read that system's
   `{system}-config.md` (the spec), last `exam-report.md` (deferred **and erred** items),
   `log.md` (events since last run, including crashes and error reports), and
   `learnings.md` (lessons not yet graduated). Write the `exam-plan.md`: the
   synthesis that pulls all the loose ends together — a job-spec added to the
   skill for this run only. The file stays; its contents are transient.
3. **Run the skill with the plan in hand.** Detection is fully autonomous —
   no questions until the gate.
4. **Aggregate** — classify every finding: `DOWN` (unavailable) / `UNHEALTHY`
   (runs, wrong behavior) / `DRIFT` (live state vs spec mismatch) / `GAP`
   (examinable artifact missing or undocumented).
5. **Report** — per finding: evidence, class, recommended repair (allowlist
   only), rollback plan, risk. One structured report.
6. **GATE — hard stop.** Developer decides per item: approve / reject / defer.
   Nothing applies without approval; two decisions are never batched into one.
7. **Apply** — approved heals only, one at a time: capture pre-state → apply →
   verify → next. Failed verification = automatic rollback + halt the run.
8. **Re-exam** — touched systems re-run; green = healed.
9. **Record** — report rewritten (current state, no history); one run row
   appended to the system's log; new learnings filed; absorbed log/learning
   entries pruned.

## 6. The suite information model — what each file is for

Every managed system's folder carries seven information files (plus its skill
draft, which stays as canonical source — installed copy holds the runtime). Each has one distinct job:

- **`{system}-config.md`** — tells us the **ideal state for all configurations
  for that system**: the config specification. A table of configurations
  applicable to that system. Nothing else belongs in it.
- **`{system}-exam-plan.md`** — the guide for the **next exam run**: a synthesis
  constructed by looking at the exam-report (addressing what was deferred **and
  what erred** last run), the logged events, and the crash/error reports from
  the log, drawing guidance from the learnings file. It pulls all the loose ends
  together and constitutes a **job-spec for the next run** that is added to the
  system's skill for that run only — not permanently. The config-manager starts
  each exam by writing this plan and runs the skill with the plan in hand. The
  file is live; its **contents** are transient (rewritten each cycle).
- **`{system}-exam-report.md`** — tells us **exactly what the current state of
  the configs is as per the last exam** — no history.
- **`{system}-log.md`** — a **running record of all notable events for the
  system**: problems experienced by the system, problems caused by the system,
  system crashes, error reports, exam runs and their outcomes. It is **not** a
  duplication of the learnings file — it is the chronological record of
  meaningful events. The file is live; old, absorbed entries are pruned.
- **`{system}-learnings.md`** — the result of exam runs where new aspects were
  learned, decisions made, or nuances discovered that affect knowledge or
  understanding of the system (this has been very real — e.g. Cupcake's
  silent-failure behaviors). A **transient, temporary home**: learnings are
  always eventually dropped, or written into a permanent home (skill / config /
  reference / explainer) — then deleted from here.
- **`{system}-explainer.md`** — a **narrative form description of everything
  about the system**, including the config maintenance system but not limited to
  it: the whole system, all aspects, nuances included. The authoritative
  comprehensive reference — how the system works, its S.W.O.T., source links to
  authority documents. Multi-audience: the human developer, a visiting technical
  consultant, and the agent.
- **`{system}-reference.md`** — where **commands and technical guidance regarding
  the system are presented for the agent specifically**.

**Log vs learnings — the distinction.** Both are transient-in-contents, but their
origins differ: the log records what *happened* (an incident, an exam run, an
upgrade, a crash); learnings record what was *learned* (a pattern, a decision, a
nuance that changed understanding). One incident may legitimately produce one log
row **and** one learning entry — different files, different lifecycles. The log
never duplicates the learnings file, and vice versa.

**Graduation — the dual track.** When a learning or a recurring plan item becomes
a permanent occurrence, it is written into a permanent home and deleted from the
transient file. Into the **skill**: agent-applied directly, then re-installed.
Into **config / reference / explainer**: a proposal at the gate, applied only after
the developer approves it — never silently. **Graduation criteria (not
vibes):** the item must have appeared in ≥1 *executed* plan, its check must have
run at least once, and it must have survived unchanged. **The plan is never an
absorption destination** — it is transient; absorbing into a plan destroys the
knowledge at the next rewrite. Pruning requires the permanent home to exist
first, and happens at plan-synthesis time of the next run.

## 7. Governance

- **Every document under `mybizz-config-docs` follows the normal documentation
  process** — no exceptions for this suite. A document changes only with the
  developer's approval; the developer commits through close-out
  (close-out-process), which runs `commit-all.sh`
  ([[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md)); and `mb-doc-check` ([[[mybizz-config-docs:mb-doc-check/doc-check-explainer]]](C:/mybizz/mybizz-config-docs/mb-doc-check/doc-check-explainer.md))
  checks every document at every commit.
- **Cupcake rules and methods apply to the config-manager itself.** It is not
  above governance. If grants are required for cross-project operations (e.g.
  installing a skill into `~/.config/opencode/skills/`), the config-manager
  requests them in the normal way (`mg-grant --path <folder> --count N`).
  Exceptions are reserved for absolutely unavoidable situations (e.g. the
  exec-protection guard blocks any command text containing the token
  `cupcake` — such operations are handed to the developer verbatim; a denial is
  never worked around, never token-dodged).
- The agent file and all `-skill.md` files are documents like every other and
  follow the same process. Changes to a skill source reach the executing copy only
  through re-install, which keeps source and installed copy identical below the
  frontmatter.

## 8. Safety invariants (enforced in the orchestrator agent)

- Allowlist-only repairs; a failure outside every allowlist = diagnosis +
  proposal, never an improvised fix
- Deny-list never healed: auth-posture edits, role/database drops, service
  deletion, boot/`wsl.conf` edits, and any self-governing config
- Rollback captured before every live change; verify-gate after every heal
- No data mutations on any database; credentials by variable name only — never
  printed, logged, or copied into reports, outputs, or learnings
- Detection is fully autonomous; only healing is gated
- One heal at a time; halt on failed verification
- Guard denials are honored absolutely — never retried through alternate paths,
  never token-dodged; a blocked check becomes a developer-run request
- **Report discipline:** write-new-then-replace — a failed or incomplete run never
  touches the previous report; the report is written before any pruning
- **Install discipline:** skills install by **copy, never move** — the suite
  folder keeps the canonical, git-versioned source; the installed copy is the
  only executing copy; step 0 verifies every cycle that source and installed copy
  are identical below the frontmatter
- **One-run-at-a-time:** a new exam run is blocked while the target system's last
  log run-row lacks a disposition
- Diligence standard: no shortcuts, no partial solutions for speed, do exactly
  the right thing the right way every time, take exceptional care to do no harm

## 9. Self-coverage — anti-circular design

The config-manager is itself a configuration system, and it must remain updated
and healthy at all times. But a system that exams itself with its own exam
machinery enters **circular redundancy** — it would be grading its own paper.
The design:

- Its **documents** follow the same documentation process as every suite's
  (Section 7).
- Its **functional health** is validated at step 0 of every exam cycle, by
  concrete checks: every `Installed` row's skill exists at its recorded path and
  its text below the frontmatter is identical to its repo source's (compared by
  sha256, read via the approved glob form `mb-config-*/SKILL.md`); every Installed system's folder holds all seven suite
  files; every register spec-doc path exists; the target system's last log
  run-row has a disposition (an open run blocks a new one). This is a check,
  not an exam — no findings cycle, no self-directed heals. Result recorded in
  [[[mybizz-config-docs:mb-config-manager/config-manager-log|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md).
- Its register deliberately does **not** list the config-manager as a managed
  system — the exception is documented here, not silent.
- Defects it finds in itself route to its own [[[mybizz-config-docs:mb-config-manager/config-manager-log|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md) and
  [[[mybizz-config-docs:mb-config-manager/config-manager-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-learnings.md), and architecture-level fixes go to the
  developer.

## 10. Scaffold

```
mybizz-config-docs/mb-config-manager/       ← the orchestrator's own suite
├── config-manager-agent.md                 ← the agent (draft; installed when built)
├── config-manager-config.md                ← its own configurations
├── config-manager-explainer.md             ← this file
├── config-manager-log.md                   ← its own notable events
├── config-manager-learnings.md             ← its own transient learnings
├── config-manager-reference.md             ← its own procedures
└── config-manager-register.md              ← what it manages (current state)

mybizz-config-docs/{system}/                ← every managed system's suite
├── {system}-config.md                      ← the spec (ideal state)
├── {system}-exam-plan.md                   ← next run's job-spec (transient contents)
├── {system}-exam-report.md                 ← current verified state (no history)
├── {system}-log.md                         ← chronological notable events
├── {system}-learnings.md                   ← transient exam knowledge
├── {system}-explainer.md                   ← authoritative whole-system narrative
├── {system}-reference.md                   ← agent-facing commands
└── {system}-skill.md                       ← exam skill canonical source (copied to install location)

install location
├── agent: mb-config-manager                ← when built (location developer-set)
└── skills: ~/.config/opencode/skills/mb-config-{system}/SKILL.md
    (one per Installed row in the register)
```

Notes: the config-manager's own suite intentionally has no `-exam-plan` or
`-exam-report` of its own — it does not self-exam (Section 9). Placeholder
folders (cloudflare, namecheap) hold no config docs yet. Systems not yet built
out keep their existing files until their build-out pass.

## 11. Build status

The architecture was tuned on PostgreSQL and now runs for every system the
[[[mybizz-config-docs:mb-config-manager/config-manager-register|Register: Managed Systems]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-register.md) lists as `Installed`; each has completed a formal
plan-driven exam run. The register is the authority for what runs.

## 12. S.W.O.T.

**Strengths.** Plan-driven exams (each run gets a fresh job-spec — no stale
procedures); the present-≠-working discipline (liveness proven, not inferred);
gated healing with rollback-first; developer-run classes for everything the
guards rightly forbid agents; a self-consistent seven-file information model
with distinct file jobs.

**Weaknesses.** Full exam coverage needs developer participation (guard-forbidden
probes); the orchestrator agent is not yet installed (draft only).

**Opportunities.** One exam discipline across every system in the estate; the transient→permanent graduation flow keeps procedures improving
without archives; the log/learnings split gives both event memory and knowledge
without posterity.

**Threats.** Spec-doc drift between runs would silently weaken exams (mitigated:
exams flag spec drift); guard-rule changes could reclassify which checks are
agent-runnable (mitigated: denials are always honored and reclassify
developer-run items immediately); circular self-exam (designed out, Section 9).

## 13. Source links

- Governing philosophy and standing principles: [[[mybizz-os-docs:operating-procedures/standing-instruction|Engineering Principles]]](C:/mybizz/mybizz-os-docs/operating-procedures/standing-instruction.md)
- Global behavior rules: `~/.config/opencode/AGENTS.md`
- Cupcake (the guard layer that shapes developer-run classes): [[[mybizz-config-docs:cupcake/cupcake-config|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md), [[[mybizz-config-docs:cupcake/cupcake-explainer|Mechanical Policy Enforcement for AI Coding Agents]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-explainer.md)
- Grant mechanism: `mg-grant` / `mg-revoke` (cupcake-config.md §Cross-project access grants)
- Division docmap: `C:\dev\dev-root\docmap.md`
- The pilot suite where this architecture was tuned: `postgresql/` (all seven files)
