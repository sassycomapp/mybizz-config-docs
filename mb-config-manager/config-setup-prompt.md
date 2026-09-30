---
title: "config-setup-prompt"
doc-id: "mb-68a57783"
---
# Config Manager — Setup Prompt

Generic task instruction / specification / prompt for a fresh session to build the
configuration-management suite for the next skill/system. Proven across five
systems (postgresql → cupcake → gbrain → memory-governor → gbrain-dream-cycle;
the last run 2026-09-14 is the freshest precedent). Use verbatim: replace
`{system}` with the target's name and follow in order. The architecture is
authoritative in `mb-config-manager/config-manager-explainer.md`; this file
adds nothing new — it packages the proven method.

---

## Prompt (paste at session start)

> Read `mybizz-config-docs/mb-config-manager/config-manager-explainer.md` (the
> authoritative architecture), `config-manager-reference.md` (procedures), and
> `config-manager-register.md` (current state). Then build and run the
> configuration-management suite for `{system}` against its spec
> `{system}/{system}-config.md`, exactly per
> `mb-config-manager/config-setup-prompt.md`. The system is
> working well — detection and verification only; nothing gets fixed without my
> explicit gate decision. First principle: DO NO DAMAGE.

## Phase 0 — Orientation (read, no writes)

- Read the target's three existing docs: `{system}-config.md` (the spec — the
  single source of expected values), `-reference.md`, `-explainer.md`.
- Read one completed suite as format template — prefer the most recent
  (`gbrain-dream-cycle/`).
- Check live state of the target (read-only probes matching the spec's tables).
- `git status` — tree should be clean or carry only known pending edits; report.
- Confirm the register row exists (state `WIP`). If no register row or no spec
  doc exists → stop, report: the system is not yet examinable.

## Phase 1 — Suite build-out (8 files total: 7-file standard + skill source)

- `learnings.md` — if empty, add the standard preamble + empty table (transient
  way-station; delete-on-graduation; cross-cutting learnings stay in
  `config-manager-learnings.md`).
- `log.md` — create; standard preamble ("events, not lessons… seeded with
  development-period events"); seed from documented history in the suite's own
  docs (incidents, removals, first runs, guard denials — each with date +
  outcome/disposition).
- `exam-plan.md` — bootstrap, hand-written (it is the format template):
  §1 run header (run #1; bootstrap = no prior report/log, expected not silence;
  Tier 3 **Locked**; developer-run bundle for guard-forbidden classes; expected
  values read fresh from the spec at run start; scope boundary — name which
  sibling modules own which checks, anti-duplication), §2 carried-forward (none;
  spec open items as watch rows), §3 erred (none), §4 log-driven items, §5
  learnings-driven items, §6 standing-checks summary (full tables live in the
  skill), §7 report requirements (write-then-replace), §8 gate protocol.
- `exam-report.md` — placeholder only: "No formal exam run yet."
- `explainer.md` — localize: extend the top companion note with the exam set;
  add "Config maintenance" section (memory-governor §14 pattern); add S.W.O.T.;
  add companion-documents footer.
- `reference.md` — add exam-plan/report/log/learnings pointers to the header.
- `skill.md` — born-with-inventory (the standing check inventory lives HERE,
  never in plans): frontmatter (name `mb-config-{system}`, description with
  triggers); file-pointer list (spec first, exam-plan second); scope boundary
  (anti-duplication); credential discipline (variable names only); hard
  behavioral rules (from the spec's own Do-not list); then the tiers:
  - **Tier 0 — liveness/invocability** (agent-runnable; failure = DOWN, stop)
  - **Tier 1 — state conformance** (each probe vs the spec's expected value;
    mismatch = DRIFT; guard-forbidden checks marked D with the proven class)
  - **Tier 2 — functional proof** (present ≠ working: one safe read-only
    execution probe + one discipline check; never content-changing)
  - **Tier 3 — deep pass** (developer-run, Locked by default: expensive /
    content-changing / policy items)
  - Report + gate-protocol sections (allowlist; deny-list; credentials by name
    only). Most modules have **no agent-healable items** — repairs are
    developer-run or proposed.

## Phase 2 — Install

- Request grant: `mg-grant --path ~/.config/opencode/skills/mb-config-{system} --count 3`
  (any guard denial honored → hand the developer exact commands, never work around).
- `mkdir -p` + `cp` source → `SKILL.md` (**copy, never move**; one skill per
  completion, never batch).
- `sha256sum` both files — record first 16 hex in the register + install date;
  flip register row WIP → Installed.

## Phase 3 — Formal run #1

- **Step 0 self-validation** (record in `config-manager-log.md`): hash pairs for
  every Installed skill via the approved glob form (`mb-config-*/SKILL.md` —
  **never a token-literal command naming a sibling guard's name**; proven denial
  class); suite completeness; register spec-doc paths exist; target's last log
  run-row has a disposition.
- Execute the plan: Tiers 0–2, fully autonomous — no questions until the gate.
- Guard denials: honored absolutely; blocked checks bundle into ONE developer
  request; results recorded verbatim, tagged developer-verified, with the exact
  commands.
- Never improvise probes outside the plan (run #1 lesson: an unplanned bare
  `--phase` probe started a live cycle — capture output to files, never pipe
  live output to a truncating consumer).
- Write the report (compose fully, then replace; before any pruning); append
  one run row to the log; file new learnings.

## Phase 4 — GATE (hard stop; per-item decisions, never batched)

- Present findings: evidence, class (`DOWN`/`UNHEALTHY`/`DRIFT`/`GAP`),
  recommended repair, risk.
- Developer decides per item: approve / reject / defer. Dispositions recorded in
  the run row.
- F-2 pattern (quirks are common): where a check reveals a design gap, present
  options with a plain-English explanation and a recommendation — never apply
  anything unasked.
- Tier 3 unlock decision asked at the gate, never assumed.

## Phase 5 — Close-out

- Graduated refinements → into the skill (agent-applied), re-copy, re-hash,
  update register hash.
- Learnings graduated → delete entries (permanent home exists first).
- Spec-doc corrections → flagged to docs governance; applied only with explicit
  developer approval (the gbrain precedent).
- If the system belongs to the memory family: update
  `mybizz-os-docs/memory-master-explainer.md` to current verified state (standing
  rule — its own commit).
- Register notes updated (verified-live date). Completion report; then the two
  standard asks: developer commit+push; agent runs
  `setsid bash /mnt/c/mybizz/scripts/sync-gbrain.sh > /tmp/sync-output.txt 2>&1 &`.

## Standing rules (violation = escalation)

- DO NO DAMAGE — detection and verification only; the system is working well.
- Guards' denials never worked around (sensitive-data: `.env`, `config.json`,
  `opencode.jsonc` reads; `/proc`; critical paths; token-literal command text).
- Copy-install, never move; hash pair verified each cycle.
- Spec docs are flagged, never edited, by the exam.
- Learnings transient; the plan is never an absorption destination.
- The agent never commits — the developer runs commit+push; then the agent runs
  sync+embed.
- Expected values are read fresh from the spec every run — never from memory.

## Amendment 2026-09-15 — clarity discipline (developer instruction, session 003)

Appended verbatim per developer instruction; nothing above is altered. A
violation of any rule in this section = escalation, same as the standing rules.

**Purpose.** This prompt defines the task completely: replace `{system}`, follow
the phases in order. The subject system is the developer's working system,
assumed working well; the run exists to keep it correctly configured and
functioning at optimum. The failure mode this amendment prevents: an agent
talking itself into confusion — re-deriving a settled task, re-asking what the
prompt already answers, manufacturing ambiguity — and wrecking the run.

- **The prompt is the task definition.** Scope is never re-confirmed, re-derived,
  or re-asked. If scope seems unclear, re-read this prompt, the register row, and
  the developer's instruction first — the answer is in those files in all but the
  rarest cases.
- **Procedural conflicts are stated, not asked.** Where a register state, file,
  or fact does not match what a phase expects (e.g. a register row in state
  `Deferred` where `WIP` is required), the resolution is an explicit named step
  in the plan — dated, with the developer's instruction cited — not a question.
  The developer's explicit instruction to run this prompt IS the authority to
  perform the documented state change.
- **Questions are mandatory where they are genuine, forbidden where they are
  not.** A question is genuine when the agent cannot lawfully or knowledgeably
  proceed: a guard denial, a missing credential, a per-item gate decision, or an
  issue discovered in the subject system that needs the developer's clarity or
  decision. Discovered subject-matter issues — drift, stale spec claims, files
  contradicting their documentation, pending items, disrepair — ARE asked about
  for clarity, plainly and once, with a recommendation. Questions that re-tread
  settled ground, re-define the task, or introduce doubt where none exists are
  the same failure as wrong answers.
- **Open issues are never left open.** Nothing discovered in the subject system
  may be worked around, silently accepted, or left unattended: every issue is
  carried to closure — as a carried-forward watch row, a governance flag, or a
  gate item with the developer's disposition recorded. A run ends only when the
  subject system holds no workaround, no unresolved open issue, and no element
  in a state of disrepair.
- **Grant discipline — request, never self-grant.** When Cupcake blocks an
  operation, the agent requests the grant from the developer in the chat
  interface and does nothing else: an agent never issues a grant request and
  then grants the authority itself; that situation may not occur. The developer
  executes the grant in WSL and returns the result to the agent in chat.
  Prescribed commands (developer-run):
  `mg-grant --path <folder> --count N` · `mg-revoke --path <folder>` ·
  `net-grant --domain <domain> --count NN` · `net-revoke --domain <domain>`
- **Report what is, both ways.** A judgment formed is reported as formed; a
  thing unknown is reported as unknown. Fabricated certainty and manufactured
  doubt are the same violation from opposite directions.
