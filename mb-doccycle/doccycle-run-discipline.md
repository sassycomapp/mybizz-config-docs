---
document: "mb-doccycle — Shared Run Discipline"
doc-id: doccycle-run-discipline
state: Live
date-created: 2026-09-22
---

# mb-doccycle — Shared Run Discipline

Single source of the run frame for [[mb-doccycle-skill|mb-doccycle]] (the
documentation-management workflow: Phase A structure → Phase B consistency →
Phase C wikilink conversion). Supersedes
[[doc-skills-run-discipline|Documentation Skills — Shared Run Discipline]]
(2026-09-19, retired with the three skills it served). Each phase spec adds
only its own specifics; nothing here is duplicated in a phase spec.

## Governance header — the developer's rules at the point of action

These rules sit here because skill text is what the agent reads at the moment
of failure. They are never superseded by task-internal instructions.

1. Plain English, always. Grammatically correct full sentences, never "AI
   shorthand". Every action handed to the developer carries its complete
   commands at the point of use — never "(commands above)".
2. STOP is absolute. The word STOP from the developer means immediate halt:
   no reasoning, no wrap-up, no "one more step".
3. One corpus per session. The working scale is one corpus cycle, or one
   bounded close-out pass, per session.
4. The developer decides. Uncertainty triggers asking, never acting. A denial
   is obeyed, never worked around.

## Scope authority

- Read [[mybizz-scope-list|Mybizz Scope List]] at Phase 0 of every run — the
  single scope authority; the workflow never carries or edits it
  (developer-owned).
- The list's criterion governs: an exception is content we never reference, in
  any form, at any time, ever. Quarantine is on the exceptions list: links to
  quarantine content remain as written prose and are never converted to
  wikilinks; stale quarantine paths are healed to the current location.
- Transient state is a scheduling question, never a scope question.
- Corpus enumeration: [[repo-organization|Repo organization]] (same folder).

## Cupcake enforcement preflight (Phase 0, once per cycle)

- Verify the plugin is active (`~/.config/opencode/plugin/cupcake.js` exists).
  If it is disabled: STOP and ask the developer to re-enable — never run with
  enforcement off, never disable it.
- Skeleton handling is automatic (set-and-forget amendment, 2026-09-22):
  folders with a skeleton use it; folders without fall back to the global-only
  home (`~/.config/cupcake/fallback`). No preparation is ever required.
- If the session folder carries a skeleton, confirm it holds at least one real
  local policy module (`.cupcake/policies/opencode` non-empty) — the
  boot-safety guarantee.
- A Cupcake denial is final for that call: report it, obtain the developer's
  instruction, never work around.

## The run frame

Cycle-level — once per invocation, in order: (1) resume check; (2) learnings
load; (3) scope read; (4) Cupcake preflight; (5) git-clean preflight — `git
status` on every repo the cycle's commit plan will touch (including repos
whose folders sit outside the walk scope); any repo with uncommitted changes
stops the run before any write, reported REPOS_DIRTY with each repo and
reason; (6) collective grant handover, constructed after detection and
presented at the approval pause.

Phase-level — repeated per phase, A → B → C: verified stop-cold backup sized
to the phase's write surface → detect → report → approve → apply → verify →
commit plan → index row → learnings.

Handover contracts: B-close is the gate before C — C never runs on a corpus B
has not passed. C's missing-document findings trigger one bounded B re-pass
per cycle; anything unresolved goes to the developer or the next cycle. Phase
commits land between phases (one commit plan per phase, one batch approval).

## Approvals

- Asked in chat, never the question tool.
- Standard findings: grouped by target and finding type, one decision per
  group, every item individually listed inside it.
- High-risk findings (identifier changes, register surgery, quarantine-path
  heals): presented individually, labelled by risk type, each approved
  individually.
- Structural writes require a second explicit confirmation ("about to do this,
  proceed?") on top of the approval.
- One approval is one approval — never standing. Resume picks up prior
  decisions verbatim.

## Collective grant handover

Slips are requested collectively, never one at a time, and their counts are
determined before any apply. After detection and approval, the workflow
constructs ONE copy-pasteable block covering every slip the cycle needs: path
slips per restricted folder (approved file count + buffer), the backup-root
line, and the commit allowance per repo. Issued in a single developer action;
one supplementary block only if a later count is exceeded. The workflow never
invokes `mg-grant` or `git-grant` itself and never works around a denial.

## Finding-handling standard — the false-alarm doctrine

Every finding triages into exactly one of three kinds. Legitimate-minimal:
real, consequence-free (a register row asserting a home a file has
legitimately left during development flux) — set aside. Illegitimate: an alarm
with no cause, which is a defect in the detection logic itself — corrected
through the rule pipeline (an amendment is a commit to the git-backed source),
never dismissed as noise, never a file forced into a mold.
Legitimate-requires-attention: real and consequential — decide and implement.
Misclassified flags corrupt trust in the whole system.

## Report standard

Plain English, decision-first, short. The 3-question decision protocol: what
was found, what is proposed, what the developer's decision is. Every count in
every report is derived mechanically from the report's own item list — never
estimated, never approximated.

## Verification

After every write: re-read what was written, or diff against the backup, and
confirm the approved change landed exactly before proceeding. Evidence or
silence — "done" without an evidence line is not done. Chained shell commands
verify each result before the next runs.

## Commits and sync

Commit plan first: one table — repo, folders touched, file count — one batch
approval for the whole commit set, one commit per repo. Commits run under the
commit-allowance channel (developer-terminal until it exists). After commits:
per-source sync and embed for every changed source, verified per source with
`gbrain sources status` — never a blanket success report.

## File search — es.exe (Everything) first

es.exe (Everything) is the primary tool for every file search. Binary:
`C:\Program Files\Everything 1.5a\es.exe`; invoke via WSL interop as
`"/mnt/c/Program Files/Everything 1.5a/es.exe" <search-term>`. Flags: `-p`
path-scoped, `-n` result limit, `-s <term>` **search** (e.g. `-s "*.md"`
finds all markdown files — it is the search flag, not a sort flag; healed
2026-09-22 after two universe-build debugging rounds), `-w` whole word, `-i`
case-sensitive, `-r` POSIX regex. Raise `-n` (≥20) or scope with `-p` before
filtering — a small unfiltered limit is consumed by backup copies before any
live path appears and reads as "file not found". A zero-hit result on a
supposedly existing file is verified with one fallback check before any
missing finding is proposed. A fallback to `find`/`glob` is reported in the
run record, never silent. Results are Windows paths; convert to `/mnt/c/...`
before opening.

## Anvil code repos — denied entirely

Never opened, read, backed up, or edited — including any documentation folder
inside them (e.g. `theme\assets\docs`); those files are Anvil app assets and
Anvil owns their interpretation. Top-level paths are existence-checked only
when referenced.

## Session close-out pass — `(closeout)`

A bounded delta pass, never a full cycle: inventory exactly what the session
changed, run the three phases only over those touched files and folders, one
grouped plain-English report, one approval, the same collective block for slips
and the commit allowance. Anything beyond the session's own changes is proposed
for the next scheduled cycle — the close-out can never balloon into a run.

## Run record lifecycle

One working record in `C:\mybizz\logs\mb-doccycle\in-progress\`, named with the
run timestamp (Filename-Safe ISO 8601, UTC+2, per
[[adr-timezone-utc-storage-display-conversion|Client Timezone: IANA String, UTC Storage, Display-Time Conversion]]),
created the moment the run begins, appended at every decision point — minimum
four appends per run. At close the record moves to `last-completed-run\` (never
deleted) and one index row is appended to `C:\mybizz\logs\mb-doccycle\run-index.md`:
run-id, date, target, findings, decisions, commits — the permanent audit trail.
Declined-resume runs go to `abandoned-runs\`, timestamp preserved, never
deleted.

## Learnings

Load the learnings folder before Detect; never assumed empty without looking.
Learnings are advisory precedent, never authority — the skill text is
authoritative, and a learning that contradicts current text is flagged as a
text-drift finding, not silently followed. Write-back at close; every entry
carries supersession marks — a superseded learning is struck through, never
deleted.
