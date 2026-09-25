---
title: "i-have-adhd-exam-report"
doc-id: "i-have-adhd-exam-report"
---
# i-have-adhd — Exam Report

Run #1 — **first formal plan-driven exam, gate closed** (2026-09-20). Plan:
[[i-have-adhd-exam-plan|Exam Plan]] (bootstrap — no prior report). Install: copy-install
executed 2026-09-20 without `mg-grant` (Cupcake disabled; developer authorized
proceed-without-grant in chat) — hash pair identical `b27623b6faf7ebe8`;
register flipped `WIP` → `Installed`; re-installed once after the gate-approved
IA1-4 amendment (re-hash `1669db5ef2192a0d`). Step-0: **PASS** — 14/14 installed
hash pairs match the register via the approved glob form (`postgresql`
b41a3e117dee1809 · `cupcake` f5e8489cf60a8abc · `gbrain` 58dc0b52cbc86d72 ·
`memory-governor` c40df342d523aa59 · `gbrain-dream-cycle` a4872e9d61f1c32f ·
`graphify` 1ca73897a2023741 · `gstack` 6a3afc08a93cee02 · `opencode`
268bb702a038448b · `matt-pocock-skills` 86c78969ad0e8a80 ·
`anvil-agent-references` a66e0140a39a37e5 · `magdoub-wireframe`
c570e38d0b490808 · `archify` 165897270158a38e · `mb-submit-memory`
88a71641d03f1997 · `i-have-adhd` b27623b6faf7ebe8); suite completeness 14/14 at
the 8-file standard; register spec-doc paths 20/20 exist; i-have-adhd carries no
prior run row (bootstrap — one-run-at-a-time not triggered). No guard denials
(Cupcake disabled) — the sensitive-data/outbound-network classes stay
developer-bundled by spec design regardless. Tier 3 **unlocked at the gate** —
all three rows executed and passed.

## Verdict: HEALTHY — every check PASS, F-1 resolved in-run by gate-approved re-baseline, Tier 3 all PASS, all open items closed except open item 6 (standing watch)

The component works, byte-exact against its spec and byte-identical to upstream
main. The one finding (F-1, second activation path) was resolved the day it was
found: the installer's dual-write is now documented state, the divergence blind
spot is closed by a standing dual-path identity check, and removal was
deliberately not pursued (the CLI recreates the copy; the registry hosts ~40
other skills the same way).

## Tier 0 — Invocability: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| IA0-1 | Bundle present + frontmatter name | Present; `name: i-have-adhd` | Present; name exact | PASS |
| IA0-2 | Slash command present | Present, references the skill | `/home/dev-p/.config/opencode/command/i-have-adhd.md` (409 B), references skill | PASS |
| IA0-3 | `disable-model-invocation` | `true` | `true` | PASS |

## Tier 1 — State conformance: PASS (F-1 found and resolved in-run)

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| IA1-1 | Bundle byte-level + sha256 | 7,207 B/142 lines · 2,157 B · 238 B | Exact (`3170b16ace00aecb` · `5108a6123beb9df2` · `2c51291283dcefdc` — now recorded in the spec) | PASS |
| IA1-2 | Always-on marker | Present + empty (0 bytes) | Present, 0 bytes, 2026-09-19 23:31:28 | PASS |
| IA1-3 | Global skills symlink | `~/.config/skills` → `~/.config/opencode/skills` | Exact | PASS |
| IA1-4 | Dual-path bundle identity | Byte-identical registry + OpenCode copies; one slash-command file; no manual third copy | **DRIFT found**: a second, byte-identical bundle copy at `~/.agents/skills/i-have-adhd/` (installer dual-write; dedup verified working — one surfaced entry). **Resolved in-run by gate decision**: spec §Install surface re-baselined (registry primary + CLI-derived copy); skill IA1-4 amended into the standing dual-path byte-identity check; reference Do-not clarified; re-install + re-hash `1669db5ef2192a0d` | PASS (post-amendment) |
| IA1-5 | No opencode.json wiring | No entry | 0 entries | PASS |
| IA1-6 | Suite completeness | 8 files + intro = 9 | 9/9 | PASS |
| IA1-7 | Upstream live state | Developer bundle (W-1/W-2) | **Executed at gate** (IA3-1 unlocked) — see Tier 3 | CLOSED |

## Tier 2 — Functional proof (present ≠ working): PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| IA2-1 | Self-evidence probe: marker present → session system prompt carries the always-on ruleset block | Block present when marker present | **Observed live in the exam session's own system prompt**: "ADHD MODE ACTIVE (always-on)" with the full ruleset, persistence note, and marker-file deletion note, while IA1-2 confirms the marker present — the injection mechanism functionally works | PASS |
| IA2-2 | Ruleset structure conformance (read-only) | Persistence clause, 10 rule headings, 6 overrides, 5-item pre-send check | All present (`## Persistence`; 10 `###` rule headings; `## When to break the rules`; `## Pre-send check`; off-phrases present) | PASS |

## Tier 3 — Deep pass (developer-unlocked at the gate): all PASS

| ID | Check | Actual | Result |
|---|---|---|---|
| IA3-1 | Upstream verification | `github.com/ayghri/i-have-adhd` live: **48.7k stars · 2.8k forks · 154 watching · 245 commits · 24 issues · 44 PRs — actively maintained**; publisher **Ayoub Ghriss** ("ayghri", GitHub API + PGP-verified HEAD); HEAD pin of record `839872f9d1cd634fed642b4589ce7226199cc15f` (2026-09-19, docs-only translation merge — post-dates the install, touches no skill content); upstream `SKILL.md` content read and structurally identical to the installed bundle | PASS — spec open items 1–2 closed (§Identity + §Install surface re-baselined) |
| IA3-2 | Update-mechanism verification | `npx skills add ayghri/i-have-adhd -a opencode -y -g` re-run live: CLI refreshes the **registry primary** (`~/.agents/skills/i-have-adhd/`), then overwrites the OpenCode copy from it ("copy → OpenCode, overwrites: OpenCode"); **byte-idempotent** on identical content (all four file hashes unchanged pre/post: SKILL.md `3170b16ace00aecb`, gemini.toml `5108a6123beb9df2`, openai.yaml `2c51291283dcefdc`); slash command survived untouched (409 B); marker untouched. Bundle byte-identity to upstream main thereby proven | PASS — spec open item 3 closed (§Install surface verified behavior recorded) |
| IA3-3 | Supply-chain review discharge | Four axes recorded in the spec (new §Security supply-chain review): publisher individual/acceptable · MIT clear · actively-maintained clear · spawn-capability benign (pure prose, `disable-model-invocation: true`; installer-run assessments **Gen Safe · Socket 0 alerts · Snyk Low Risk**) | PASS — spec open item 4 closed |

## Findings — all with recorded dispositions

1. **F-1 — DRIFT (second activation path): RESOLVED in-run, gate-approved
   re-baseline.** Found at IA1-4: the installer dual-writes (registry primary +
   OpenCode-derived copy), the spec modeled a single path. Gate decision:
   **re-baseline + identity check** (removal rejected — the CLI recreates the
   copy; the registry hosts ~40 other skills the same way). Applied: spec
   §Install surface re-baselined; skill IA1-4 amended to the dual-path
   byte-identity check; reference §Install/§Update/Do-not updated; re-install +
   re-hash `1669db5ef2192a0d`; learning #1 graduated into the skill + spec.
2. **F-2 — GAP (spec staleness): RESOLVED in-run, gate-approved spec
   application.** Open item 5 closed (scaffold populated, module created);
   §Integration facts gained the exam-module row; §Current state re-verified
   2026-09-20.
3. **IA1-7 deferred bundle: DISCHARGED** — upstream verification executed at
   the gate (IA3-1), open items 1–2 closed.
4. **Standing watch:** spec open item 6 (design-mode discipline informal)
   remains open — no approved mechanism change; carries into run #2's plan.

## Gate record (per-item, 2026-09-20)

| Item | Decision |
|---|---|
| F-1 disposition | Re-baseline + dual-path identity check (developer-selected; removal and defer rejected) |
| F-2 spec corrections | Apply now (developer-selected; magdoub/anvil precedent) |
| Tier 3 IA3-1 (upstream) | Unlocked — executed, PASS |
| Tier 3 IA3-2 (update test) | Unlocked — executed, PASS |
| Tier 3 IA3-3 (supply-chain) | Unlocked — executed, PASS |
