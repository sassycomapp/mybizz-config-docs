---
title: "matt-pocock-skills-exam-report"
doc-id: "matt-pocock-skills-exam-report"
---
# Matt Pocock Skills — Exam Report

Run #1 — **first formal plan-driven exam** (2026-09-16). Plan:
[[matt-pocock-skills-exam-plan|Exam Plan]] (bootstrap — no prior report). Step-0: **PASS**
— 10/10 hash pairs match via the approved glob form (postgresql `b41a3e117dee1809`
· cupcake `f5e8489cf60a8abc` · gbrain `58dc0b52cbc86d72` · memory-governor
`c40df342d523aa59` · gbrain-dream-cycle `a4872e9d61f1c32f` · graphify
`1ca73897a2023741` · mb-submit-memory `88a71641d03f1997` · opencode
`268bb702a038448b` · gstack `6a3afc08a93cee02` · matt-pocock-skills
`86c78969ad0e8a80`); suite completeness 10/10 at the 8-file standard; all register
spec-doc paths resolve; no open run blocks (bootstrap). One guard denial at
step-0 (token-literal sibling name in list text — recorded exec-protection class)
— honored, derived-glob form used. Detection only — Tiers 0–2; Tier 3 **unlocked at gate** and executed (MP3-1 full
audit, MP3-2 stay-pinned, MP3-3 keep).
Scope boundary honored (anvil 5 shared-root = anvil-agent-references domain;
GStack inventory/state never probed).

## Verdict: HEALTHY — all checks PASS, zero live defects, zero open findings; Tier 3 executed (MP3-1 full audit PASS, MP3-2 stay-pinned, MP3-3 keep)

The installation is working exactly as recorded in its spec: pinned clone at the
recorded HEAD, 40-symlink topology intact with zero broken links, inventory
conformance 18/7/6/4, per-project setup gate in the recorded 1 Yes / 4 No state,
and the standing no-upgrade rule intact.

## Tier 0 — Invocability: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| MP0-1 | Source clone present + pinned | `84fdeff` (config §Identity) | HEAD `84fdeffd12f2ee307994d1eb6feb48173b6e0502` @ `C:\mybizz\matt-pocock-skills-source` | PASS |
| MP0-2 | Discovery root matt set reachable | 35 matt symlinks → source clone `skills/{eng,prod,in-progress,misc}` | 35 matt-targeted symlinks resolve; 40 total links in root | PASS |

## Tier 1 — State conformance: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| MP1-1 | Link graph | 40 symlinks (35 matt + 5 anvil); 0 broken; only non-symlink = Zone.Identifier | 40 links (35 matt + 5 anvil), 0 broken, 0 real dirs, exactly 1 regular file (Zone.Identifier 25 B) | PASS |
| MP1-2 | Per-project setup gate | makepdlf Yes (4 files), other 4 No | makepdlf-project-library 4 files; mb-3-cs-project-library / mb-3-cs / mb4ecom / mb5pdlf-project-library 0 each | PASS |
| MP1-3 | Upgrade state | Pinned clone; symlinks only; no plugin/`npx` artifacts | HEAD pinned; 0 real dirs beneath root (nothing copied) | PASS |
| MP1-4 | Inventory conformance | 18/7/6/4, deprecated README-only | 18/7/6/4 all symlinked 1:1; deprecated non-README entries 0 | PASS |
| MP1-5 | Suite completeness | 7 files | 8 files (7-file standard + skill source) | PASS |
| MP1-6 | GStack relationship | No shared entries; all targets under source `skills/` | 0 cross-target links (none non-matt, non-anvil) | PASS |
| MP1-7 | Zone.Identifier artifact | Present, 25 B, inert | Present, 25 B (`matt-pocock-skills-reference.md:Zone.Identifier`) | PASS |

## Tier 2 — Functional proof (present ≠ working): PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| MP2-1 | Reachability + frontmatter sweep (35 skills) | Every SKILL.md exists at target, real `name:` frontmatter, resolves through symlink | **35 / 35** valid frontmatter; 0 failures | PASS |
| MP2-2 | Discipline probe — 3 sub-agent-referencing skills | code-review, wayfinder, ask-matt resolve + frontmatter (inline-execution policy) | All three RESOLVES + frontmatter | PASS |

## Findings

None. Watch items confirmed as recorded (observations, not findings):

- **W-1** — Zone.Identifier artifact present (25 B, inert) per config §Open items;
  cleanup optional, pending a deliberate decision.
- **W-2** — Upstream divergence recorded (`84fdeff` vs upstream ~1 month newer,
  incl. PR #1025 "stop linking misc/"); no-upgrade standing rule intact — MP1-3
  verified pin. Upgrade is a deliberate-decision item (MP3-2).

## Tier 3 — Deep pass: EXECUTED (developer unlocked at gate, 2026-09-16)

**MP3-1 — full mechanical integrity audit: PASS.**

| Check | Expected | Actual |
|---|---|---|
| Link origin counts | 35 matt + 5 anvil, 0 other | 35 matt / 5 anvil / 0 cross-target |
| Broken links | 0 | 0 |
| Category counts (source tree) | 18/7/6/4 | engineering 18 · productivity 7 · in-progress 6 · misc 4 |
| SKILL.md byte-identity (35 matt skills vs source) | 0 mismatches | **0 / 35** (sha256 first-16 on each resolved symlink target) |

Every link resolves to its intended target, every SKILL.md is byte-identical to
its source counterpart, catalog counts exact. Exhaustive sweep complete — Tier 2
sampling validated at full breadth.

**MP3-2 — deliberate upgrade decision:** **STAY PINNED at `84fdeff`** — no check
failed (policy: never on newness, only on check failure). Upstream divergence
(clone `84fdeff` vs upstream HEAD, ~1 month, incl. PR #1025 "stop linking
misc/") remains the recorded open item for any future deliberate decision.

**MP3-3 — Zone.Identifier cleanup decision:** **KEEP** — 25 B, inert, recorded in
config §Open items as optional; no action taken, no state change.

## Deferred (runner attribution)

None this run (no guard-forbidden checks; no unlock-gated items executed — Tier 3
awaiting the gate decision).

## Guard layers

One denial this run, honored absolutely, recorded class: step-0 token-literal
sibling name in an argument list (exec-protection). No denial was retried through
an alternate path; the check re-ran in the approved derived-glob form.
