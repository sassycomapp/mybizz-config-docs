---
title: "magdoub-wireframe-exam-report"
doc-id: "mb-057de579"
updated: "2026-10-05"
---
# Magdoub Wireframe — Exam Report

Run #1 — **first formal plan-driven exam** (2026-09-16). Plan:
[[[mybizz-config-docs:magdoub-wireframe/magdoub-wireframe-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/magdoub-wireframe/magdoub-wireframe-exam-plan.md) (bootstrap — no prior report). Step-0: **PASS**
— 12/12 hash pairs match via the approved glob form (postgresql `b41a3e117dee1809`
· cupcake `f5e8489cf60a8abc` · gbrain `58dc0b52cbc86d72` · memory-governor
`c40df342d523aa59` · gbrain-dream-cycle `a4872e9d61f1c32f` · graphify
`1ca73897a2023741` · mb-submit-memory `88a71641d03f1997` · opencode
`268bb702a038448b` · gstack `6a3afc08a93cee02` · matt-pocock-skills
`86c78969ad0e8a80` · anvil-agent-references `8f2f4ccd6dce29c0` · magdoub-wireframe
`703b7f340e4cf302`); suite completeness 12/12 at the 8-file standard; all register
spec-doc paths resolve; no open run blocks (bootstrap). One guard denial at
step-0 (brace-expansion glob across sibling suite folders — recorded class) —
honored, directory-read form used. Detection Tiers 0–2, then Tier 3 **unlocked at
the gate** (2026-09-16, all items approved) and executed.
Scope boundary honored (PDLF step 22/26 + [[[default:adr-global/adr-design-rules|Wireframe Design Rules]]](C:/dev/project-library-global/adr-global/adr-design-rules.md) ADR = docs domain;
`task`-tool guard layer = cupcake/opencode domain; gbrain sync = gbrain module —
none probed).

## Verdict: HEALTHY — all checks PASS (Tiers 0–2), zero live defects, zero open findings; Tier 3 executed (MW3-1 audit PASS, MW3-2 decisions recorded, MW3-3 re-confirmed)

The installation is working exactly as recorded in its spec: genuine real clone
pinned at the recorded HEAD with a clean tree, two-hop discovery symlink intact,
all bundled files present at their recorded line and byte counts, the
no-confirmed-run state standing, and the settled sync/update policy intact.

## Tier 0 — Invocability: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| MW0-1 | Real clone present + pinned | `44a5814d1583c4dc7cafa36611838669f0895af9` (config §Identity) | HEAD `44a5814d1583c4dc7cafa36611838669f0895af9`; working tree clean | PASS |
| MW0-2 | OpenCode discovery path resolves | `/home/dev-p/.claude/skills/wireframe/SKILL.md` | `readlink` → `/home/dev-p/.claude/skills/wireframe/SKILL.md` (symlink intact) | PASS |

## Tier 1 — State conformance: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| MW1-1 | SKILL.md frontmatter identity | `name: wireframe`, no version field | name `wireframe`, no version field; description matches | PASS |
| MW1-2 | Install architecture | remote `https://github.com/Magdoub/claude-wireframe-skill.git`, branch `main`, clean tree | remote exact; branch `main`; tree clean | PASS |
| MW1-3 | Bundled files live-counted | SKILL.md 404 l · base.css 244 l · template.html 274 l · self-reveal.css 9 l · design-taste.md 116 l; README + LICENSE; examples 3 PNGs | 404 / 244 / 274 / 9 / 116 all exact; README + LICENSE present; examples = 3 PNGs | PASS |
| MW1-4 | No-confirmed-run state | No `design-context.md`; no output dirs | absent; dirs absent under mb-3-cs, project-library, makepdlf | PASS |
| MW1-5 | Suite completeness | 8 files | 8 files | PASS |
| MW1-6 | Single discovery path | One `SKILL.md` symlink; no duplicate | Exactly one symlink; no duplicate entry | PASS |
| MW1-7 | Old single-file reference state | Present or absent (recorded; open item 5) | Present (3857 B, 2026-08-12) | PASS (recorded) |

## Tier 2 — Functional proof (present ≠ working): PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| MW2-1 | Reachability through two-hop path | Real frontmatter resolves through symlink | `head -5` → real `name: wireframe` | PASS |
| MW2-2 | Template-path integrity | base.css / template.html / self-reveal.css at bundled paths | All three present (5597 / 17250 / 699 B) | PASS |
| MW2-3 | Discipline — Phase-2 constraint intact | `task` tool absent; no parallel Task invocation | No task tool in environment set; Phase-2 paragraph not executed; open item 1 intact | PASS |

## Tier 3 — Deep pass: EXECUTED (developer unlocked at gate, 2026-09-16)

**MW3-1 — full mechanical integrity audit: PASS.**

| Check | Expected | Actual |
|---|---|---|
| SKILL.md | 27,731 B | 27,731 B (sha256 `9a29e197…`) |
| base.css | 5,597 B | 5,597 B (sha256 `5eaf1c7f…`) |
| template.html | 17,250 B | 17,250 B (sha256 `146b59b5…`) |
| self-reveal.css | 699 B | 699 B (sha256 `7aa42989…`) |
| design-taste.md | 6,611 B | 6,611 B (sha256 `9616244a…`) |
| Working tree | clean | clean |
| local vs origin | equal | equal (0 divergent commits) |

Labels/README/LICENSE/examples verified in Tier 1 (MW1-3). Every recorded value
confirmed exhaustively; the Tier 1/2 sampling is validated at full breadth.

**MW3-2 — open-item decisions (all gate-approved, recorded in the spec):**
- **W-3 supply-chain review — PERFORMED AND RECORDED** in
  [[[mybizz-config-docs:magdoub-wireframe/magdoub-wireframe-config|Configuration]]](C:/mybizz/mybizz-config-docs/magdoub-wireframe/magdoub-wireframe-config.md) (Security supply-chain review, 2026-09-16):
  benign on all four axes (publisher individual/acceptable · MIT clear ·
  maintenance dormant-but-stable acceptable · spawn-capability benign in this
  environment). Open item 3 **closed**.
- **W-4 [[[default:adr-global/adr-design-rules|Wireframe Design Rules]]](C:/dev/project-library-global/adr-global/adr-design-rules.md) ADR reconciliation — FLAGGED TO DOCS GOVERNANCE at the
  gate, then RESOLVED BY DIRECT DEVELOPER DECISION 2026-09-16** (ADR Section A
  added — Magdoub-skill exemption; open item 4 closed post-run; see suite log
  row).
- **W-5 old single-file reference — RETAINED FOR NOW** (retirement rides with
  future suite maintenance; open item 5 stays open).
- **W-1 Phase-2 mechanism — DEFERRED to a deliberate session** (candidates
  recorded: main-agent sequential fallback vs Phase-1-only; open item 1 stays
  open).

**MW3-3 — update-discipline re-confirmation: policy restated, no action.**
Update command stays developer-run only, never AI-invoked (`git fetch` +
`git reset --hard` inside the clone, from a terminal per the reference); content
reaches GBrain by ordinary `gbrain sync` only, never the Memory Governor's API
(permanent vendor-material bypass). Verified intact by the run's own behavior —
no fetch/reset attempted; no lifecycle change.

## Findings

None. All watch items (config §Open items) now carry dispositions: W-1 deferred,
W-2 recorded state, W-3 closed (reviewed), W-4 **closed post-run (resolved
2026-09-16 — ADR §A exemption applied by developer decision)**, W-5 retained. No
open findings remain from this run.

## Deferred (runner attribution)

None — Tier 3 executed in full at the gate; no guard-forbidden checks in Tiers
0–2.

## Guard layers

One denial this run, honored absolutely, recorded class: step-0 brace-expansion
glob across sibling suite folders (cross-project). No denial was retried through
an alternate path; the check re-ran in the directory-read form.
