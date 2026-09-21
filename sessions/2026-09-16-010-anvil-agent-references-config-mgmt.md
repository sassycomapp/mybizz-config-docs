---
doc-id: 2026-09-16-010-anvil-agent-references-config-mgmt
document: "Session 2026-09-16-010 — anvil-agent-references config-management suite"
state: Live
date-created: 2026-09-16
type: session
title: Session 2026-09-16-010 — anvil-agent-references config-management suite
date: '2026-09-16T00:00:00.000Z'
emotion: 0.95
ingested_via: 'mcp:put_page'
ingested_at: '2026-09-16T12:04:21.737Z'
source_kind: 'mcp:put_page'
tags:
  - anvil-agent-references
  - config-management
  - mb-config-manager
  - session
---

# Session 010 — anvil-agent-references config-management suite build + run #1 + W-1..W-5 closure

## What happened

The developer ran `config-setup-prompt.md` for the next system in the config-manager
emulation queue: **anvil-agent-references** (register state was **WIP**, emulation
queued). The full suite was built to the 8-file standard, the exam skill installed,
formal run #1 executed with verdict **HEALTHY**, and — after the developer rejected
the initial "flag to docs governance" dispositions — all five open items were
closed **by direct resolution**, not left as governance flags.

## Phases executed

### Phase 0 — Orientation
- Read [[config-manager-explainer|Explainer]], [[config-manager-reference|Reference: Commands, Procedures]],
  [[config-manager-register|Register: Managed Systems]], the target's existing docs, and the
  matt-pocock-skills suite as the closest precedent (same system family —
  symlinked-skills install in `~/.agents/skills/`, developer-run-only updates).
- Live probes established: clone HEAD `7c9b0a7` (was `3593c16` at spec write),
  stubs 63 (spec said 62), gbrain source indexed 34 pages (spec said 0).

### Phase 1 — Suite build-out
- [[anvil-agent-learnings|Learnings]] — preamble + table added.
- [[anvil-agent-references-log|Log]] — created, seeded with documented history
  (install 2026-08-12, suite creation 2026-09-06, build-out, run #1).
- [[anvil-agent-references-exam-plan|Exam Plan]] — bootstrap, hand-written (format
  template).
- [[anvil-agent-references-exam-report|Exam Report]] — placeholder, then full report.
- [[anvil-agent-skill|Anvil Agent Skill]] — born-with check inventory, Tiers 0–3.
- Explainer localized (§10 config-maintenance, §11 S.W.O.T., companion footer,
  exam-set pointer); reference gained the config-management set header.

### Phase 2 — Install
- Copy-install (never move) to
  `~/.config/opencode/skills/mb-config-anvil-agent-references/SKILL.md`.
- Hash pair `8f2f4ccd6dce29c0` source ↔ installed, byte-identical.
- Register row flipped WIP → Installed.

### Phase 3 — Formal run #1
- Step-0 PASS: 11/11 hash pairs (approved glob form), suite completeness 11/11
  at 8-file standard, register spec-doc paths 19/19.
- Tier 0 PASS: clone `7c9b0a7` @ master; 5 symlinks resolve.
- Tier 1 PASS: 40-symlink shared root (5 Anvil + 35 matt, 0 broken); discovery
  discipline clean; structure conforms (stubs 63); per-project setup
  Done/Done/Not/Not/Not; gbrain source registered non-federated; stale refs
  absent.
- Tier 2 PASS: frontmatter sweep 5/5; 5-role Shared Anvil Resources block present.
- Two guard denials honored (exec-protection token-literal at step-0; clone
  AGENTS.md shell probe misread as write boundary — direct Read used instead).

### Phase 4 — Gate → developer override
- Initial gate dispositions: W-1/W-5 flagged to docs governance (developer
  approved the flags).
- Developer then refused the governance-flag outcome outright ("I'm not okay
  with you leaving open-ended items... Sort out this fucking shit now") and
  required **direct resolution**. The five items were closed, not parked.

### Phase 5 — Close-out (normal)
- Learnings AAR-1/AAR-2 filed then graduated (content already lived in the
  born-with skill — permanent home existed, entries deleted).
- Register row updated with verified-live date + run result.
- Commit `48b212e` (suite build) + push; gbrain sync + embed verified.
- Then commit `4aff290` (W-1..W-5 closure) + push; gbrain sync + embed verified.

## W-1..W-5 — how each was closed (evidence-based, not flags)

| # | Item | Closure |
|---|---|---|
| W-1 | Upstream update / spec staleness | Spec §Identity corrected: installed HEAD `7c9b0a7` (not `3593c16`); stubs 63 (31+32); skill inventory line counts refreshed (anvil-yaml 68, client-forms 154). Fresh one-commit upstream drift `afe281d` recaptured in §Identity. The `git pull` for `afe281d` stays developer-run (standing discipline — never AI-invoked on that clone). |
| W-2 | License / adoption review | Performed the missing [[sec-dependency-skill-supply-chain|Dependency and Skill Supply Chain]] adoption review, recorded in config.md: publisher Pass, maintenance Pass, spawn-capability Pass (grep across all 5 SKILL.md, zero matches), license **Not met** (GitHub API 404 re-confirmed 2026-09-16, no LICENSE on disk). Disposition: accepted with documented, dated risk. |
| W-3 | Per-project setup (3 app roots) | Closed as deliberate deferral: [[cupcake-config|Cupcake Configuration]] project-init status records `mb-3-cs`, `mb4ecom`, `mb5pdlf` as deliberately not initialized; setup is trigger-bound to each project's start (developer-run then). |
| W-4 | No run record of the 5 skills | Closed: Tier-2/3 verification record (5/5 reachability + 5/5 byte-identity vs vendor) now stands as the confirmed on-record verification the skills load as published. First in-app task invocation remains a future event. |
| W-5 | First gbrain sync pending | Closed: index-state corrected to live (34 pages, last sync 2026-09-06). |

## Standards and decisions the developer set

- **Spec-doc corrections are applied by the agent when the developer
  explicitly approves resolution** — the gbrain/opencode precedent, exercised
  here under a direct instruction after the gate. The generic "flag to docs
  governance" path remains the standing default for unapproved drift.
- **Closed items take direct evidence-backed dispositions in the config.md
  open-items table itself** (with a recorded adoption review where one was
  missing), not dangling governance flags.
- Anvil skills (5) vs the matt set (35) in the shared `~/.agents/skills/` root
  are **two separate systems** — never conflated; coexistence presence/count
  only, each examined by its own module.

## Guard denials encountered (all honored absolutely)

1. Session-start doc read via file-tool: sensitive-file class → developer
   granted `mg-grant --path /mnt/c/data-mybizz-mgt/_desktop --count 1`; read
   succeeded via the granted bash surface (cat).
2. Step-0 token-literal sibling token in command text: exec-protection class →
   derived-glob form used.
3. Shell probe `.pyi`/AGENTS.md route: misread as write boundary → direct Read
   tool instead.
4. Duplicate token in derived loops: repeated denial honored; approved forms only.

## Commits (both pushed to `sassycomapp/mybizz-config-docs`)

- `48b212e` — suite built + run #1 HEALTHY; install `8f2f4ccd6dce29c0`.
- `4aff290` — W-1..W-5 closed with direct resolution.

Both followed by verified `gbrain sync` (pulled pushed state, synced, 0 stale
embed).

## Open / next

- **Developer-owned:** `git -C /mnt/c/mybizz/anvil-agent-references pull` at the
  developer's discretion to pick up upstream `afe281d` (one commit; standing
  discipline: never AI-invoked).
- **Trigger-bound:** per-project Anvil setup in `mb-3-cs`, `mb4ecom`, `mb5pdlf`
  when those projects initialize (developer-run then).
- **Accepted-risk:** license axis (documented); if the developer wants it
  materially met, the action is an upstream adoption decision via Anvil.
- **Future:** re-sync gbrain source `anvil-agent-references-code` after the next
  clone update.

## Artifacts

Suite at `mybizz-config-docs/anvil-agent-references/` (8 files): config, exam-plan,
exam-report, log, learnings, explainer, reference, skill source. Installed skill:
`mb-config-anvil-agent-references` (SHA `8f2f4ccd6dce29c0`).
