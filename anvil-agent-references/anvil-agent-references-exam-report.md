---
document: "anvil-agent-references — Exam Report"
doc-id: anvil-agent-references-exam-report
state: Live
date-created: 2026-09-16
---

# anvil-agent-references — Exam Report

Run #1 — **first formal plan-driven exam** (2026-09-16). Plan:
`anvil-agent-references-exam-plan.md` (bootstrap — no prior report). Step-0: **PASS**
— 11/11 hash pairs match via the approved glob form (postgresql `b41a3e117dee1809`
· cupcake `f5e8489cf60a8abc` · gbrain `58dc0b52cbc86d72` · memory-governor
`c40df342d523aa59` · gbrain-dream-cycle `a4872e9d61f1c32f` · graphify
`1ca73897a2023741` · mb-submit-memory `88a71641d03f1997` · opencode
`268bb702a038448b` · gstack `6a3afc08a93cee02` · matt-pocock-skills
`86c78969ad0e8a80` · anvil-agent-references `8f2f4ccd6dce29c0`); suite completeness
11/11 at the 8-file standard; register spec-doc paths 19/19 resolve; no open run
blocks (bootstrap). One guard denial at step-0 (literal sibling token in command
text — recorded exec-protection class) — honored, derived-glob form used.
Detection only — Tiers 0–2; Tier 3 **unlocked at gate** (developer decision
2026-09-16) and executed — AR3-1 full audit PASS, AR3-2 stay-current, AR3-3
developer-run pending. Gate dispositions recorded: W-1 and W-5 **flagged to docs
governance** (spec refresh + open items 1/5 closures; spec edits left to docs
governance — no live mismatch). Scope boundary honored (35 matt shared-root =
matt-pocock-skills domain, presence/count only; GStack and `anvil-docs/` never
probed; the 5 vendor Anvil skills are this module's subject, never conflated with
the matt set).

## Verdict: HEALTHY — all checks PASS (Tiers 0–3), zero live defects; two spec-staleness observations flagged to docs governance at the gate

The installation is working exactly as recorded in its spec: clone at upstream
HEAD `7c9b0a7` on `master`, 40-symlink shared root intact (5 vendor Anvil skills +
35 matt) with zero broken links, all five vendor Anvil skills reachable with real
frontmatter, discovery discipline clean (no second paths), per-project setup in
the recorded Done/Done/Not/Not/Not state, GBrain source registered non-federated,
and the three stale references confirmed absent.

## Tier 0 — Invocability: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| AR0-1 | Source clone present + HEAD reachable | Branch `master`, HEAD per config §Identity (recorded `3593c16`; read fresh) | HEAD `7c9b0a7a53a81f609fc6364cf70c0dc7fa1664b8` @ `master` — **moved to upstream HEAD since spec written** (log row 2026-09-16) | PASS (delta flagged, see W-1) |
| AR0-2 | Discovery root anvil set reachable | 5 symlinks `anvil-yaml` `client-forms` `client-modules` `data-models` `server-code` → clone `skills/` | All 5 present, all resolve via `readlink -f` into `/mnt/c/mybizz/anvil-agent-references/skills/<name>` | PASS |

## Tier 1 — State conformance: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| AR1-1 | Link graph | 40 symlinks (5 anvil + 35 matt); 0 broken; only non-symlink = matt Zone.Identifier | 40 links (5 anvil-targeted + 35 matt), 0 broken, exactly 1 regular file (matt `Zone.Identifier` — matt's domain, presence-only) | PASS |
| AR1-2 | Discovery discipline | No anvil entries in `~/.claude/skills/`; no project-local anvil copies | `~/.claude/skills/` holds gstack + wireframe only; 0 anvil entries; no project-local copies | PASS |
| AR1-3 | Repository structure | skills/ 5 named; stubs 62 = 31 client + 31 server (config §Repository structure); reference/types 3 `.d.ts`; docs/m3 layout; plugin name `anvil`/version `1.0.0` | skills/ 5 exact; **server stubs 32 (total 63)** — delta vs recorded 31 (flagged, W-1); client 31; reference/types 3; docs/m3 per spec; codex plugin `anvil`/`1.0.0` | PASS (stub-count delta noted) |
| AR1-4 | Per-project setup gate | makepdlf-project-library Done, mb-3-cs-project-library Done, mb-3-cs / mb4ecom / mb5pdlf Not done | makepdlf-project-library marker=1 · mb-3-cs-project-library marker=1 · mb-3-cs marker=0 · mb4ecom no AGENTS.md · mb5pdlf no AGENTS.md | PASS |
| AR1-5 | Suite completeness | 7 files in `anvil-agent-references/` | 8 files (7-file standard + skill source `anvil-agent-skill.md`) | PASS |
| AR1-6 | GBrain source registration | Source id `anvil-agent-references-code`, path `/mnt/c/mybizz/anvil-agent-references`, non-federated | Registered, id + path exact, federated `unset`; **34 pages, last sync 2026-09-06** — spec records "0 pages, never synced" (flagged, W-5) | PASS (index-state delta noted) |
| AR1-7 | Stale external references absent | `/mnt/c/mybizz/config`, `/mnt/c/mybizz/skills-collective`, `docs/material-3` all absent | All three absent | PASS |

## Tier 2 — Functional proof (present ≠ working): PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| AR2-1 | Reachability + frontmatter sweep (5 vendor Anvil skills) | Every SKILL.md exists at target, real `name:`/`description:` frontmatter, resolves through symlink | **5 / 5** valid frontmatter (`anvil-yaml`, `client-forms`, `client-modules`, `data-models`, `server-code`); 0 failures | PASS |
| AR2-2 | Discipline probe — shared-resource block source | Clone `AGENTS.md` carries "Shared Anvil Resources" with **5 roles** (client stubs, server stubs, type references, docs, skills) | Block present with all 5 roles + Skills list naming all 5 vendor Anvil skills | PASS |

## Findings

None (no DOWN / UNHEALTHY / DRIFT live-state mismatch, no GAP). Two
**spec-staleness observations** — flagged to docs governance at the gate
(approved 2026-09-16), spec edits left to docs governance, no live mismatch:

- **W-1 — clone updated since spec written.** Spec §Identity records installed
  HEAD `3593c16` with update pending (open item 1); live HEAD is `7c9b0a7` — the
  previously-recorded *upstream* HEAD — so the developer-run `git pull` has
  evidently executed. Consistent with this, the server stub count is now 32 (total
  63) vs recorded 31/62. **Class: DRIFT (spec vs live).** Disposition: **flagged
  to docs governance** — refresh spec §Identity + §Repository-structure, close
  open item 1. Evidence: `git rev-parse HEAD`; stub `find`.
- **W-5 — GBrain index state advanced.** Spec §GBrain registration + open item 5
  record "0 pages, never synced"; live shows 34 pages, last sync 2026-09-06 — the
  first sync has evidently run. **Class: DRIFT (spec vs live).** Disposition:
  **flagged to docs governance** — refresh spec's index-state claim, close open
  item 5. Note: last sync predates the clone update — the re-sync after the update
  is a developer-run decision (regular `gbrain sync` path, Memory Governor
  bypassed).
- **W-2 / W-3 / W-4** (open items 2/3/4) confirmed unchanged: no LICENSE (license
  axis still formally unmet); 3 app roots still Not-done; no confirmed run record
  of any vendor Anvil skill yet — each remains a recorded open item, no action.

## Tier 3 — Deep pass: EXECUTED (developer unlocked at gate, 2026-09-16)

**AR3-1 — full mechanical integrity audit: PASS.**

| Check | Expected | Actual |
|---|---|---|
| Symlink origins | 5 links → `anvil-agent-references/skills/<name>` | 5/5 resolve exact (anvil-yaml · client-forms · client-modules · data-models · server-code) |
| SKILL.md byte-identity | 5/5 match vendor source bytes | **5 / 5** (sha256 first-16 each: `85d76f9363c0d029` · `85b9cbc57ff3d7a9` · `c384c9d74d2efc9b` · `f3d08f42392ff4c6` · `06a92faab532497d`) |
| skills/ folder count | 5 | 5 |
| Stub counts | 31 client + 31 server (config §Repository structure) | 31 client + **32 server** (total 63 — delta, flag W-1) |
| reference/types | 3 `.d.ts` | 3 |
| docs/m3 | per config | 49 files, layout per spec |
| Plugin metadata | codex + claude: name `anvil`, version `1.0.0`, recorded descriptions | Both verified from disk — name `anvil`, version `1.0.0`, descriptions match config §Plugin metadata |

Exhaustive sweep complete — every link resolves to its intended vendor target,
every SKILL.md byte-identical, structure conforms (server stub delta carried as
W-1).

**AR3-2 — update + license decision:** **STAY CURRENT WITH UPSTREAM** — the clone
is already at upstream HEAD `7c9b0a7` (a generated checkout; update cadence is an
operational habit, not a pin — the recorded default). Spec refresh flagged via
docs governance (W-1, approved at gate). License: **no action** — open item 2
remains (no LICENSE found; supply-chain license axis formally unmet); the
vendor-publisher + generated-read-only context keeps practical risk low.

**AR3-3 — per-project setup closure decision:** the 3 Not-done app roots
(`mb-3-cs`, `mb4ecom`, `mb5pdlf`) remain **developer-run pending** — AI writes to
project `AGENTS.md` are prohibited either way (standing policy). Open item 3
carries until the developer acts.

## Deferred (runner attribution)

None this run (no guard-forbidden checks; Tier 3 was unlock-gated and executed
after the developer's gate unlock; AR3-3's per-project setup remains
developer-run pending — a recorded decision, not a deferral).

## Guard layers

Two denials this run, honored absolutely, recorded classes: (1) step-0
token-literal sibling token in command text — exec-protection; (2) a shell probe
on the clone's AGENTS.md misread as a write boundary — command-scope
protection. Neither was retried through an alternate path; the checks re-ran in
approved forms (derived glob; direct Read tool).
