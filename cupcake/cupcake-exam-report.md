---
title: "cupcake-exam-report"
doc-id: "mb-19213c10"
---
# Cupcake — Exam Report

Run #1 — **first formal plan-driven run** (2026-09-13). Plan:
[[cupcake-exam-plan|Exam Plan]] (step-0 self-validation: PASS — 8 suite files, hash pair
MATCH ff34de94c7edd6df, spec present, no open run). Detection only — Tiers 0–2
executed; Tier 3 locked (inherently developer-run). Spec: [[cupcake-config|Cupcake Configuration]]
(refreshed pre-run per developer approval — backup inventory + jsonc naming).

## Verdict: ACTIVE & HEALTHY — enforcement proven live; zero compile failures; inventory exact

## Tier 0 — Liveness: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| C0-1 | Binaries resolve (fs listing) | real binary + symlinks per spec | exact match; opa 1.19.1 | PASS |
| C0-2 | Enforcement firing | deny on harmless known-blocked probe | **outbound-network deny received** (curl to non-allowlisted domain) | PASS |
| C0-3 | Plugin single live copy | one `cupcake.js` | one live copy + 2 correctly-suffixed backups | PASS |

## Tier 1 — Health: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| C1-1 | `opa check` all deployed + builtins + system | 0 failures | **24 files checked, 0 failures** | PASS |
| C1-2 | Scaffold absence | no `example.rego`/non-conforming files | none | PASS |
| C1-3 | Backup suffix discipline | all `.bak-*` non-`.rego`/non-`.js` | all 8 correct | PASS |
| C1-4 | Grants data file | generated-form | `GLOBAL-GRANTS-DATA` header | PASS |

## Tier 2 — State conformance: PASS

| ID | Expected | Actual | Result |
|---|---|---|---|
| C2-1 | 19 custom + 3 builtins + aggregator | exact match | PASS |
| C2-2 | `"task": "deny"` in `opencode.jsonc` | present | PASS |
| C2-3 | denylist: task, delegate, call_omo_agent, agent_session_create | exact | PASS |
| C2-4 | 20 sources ↔ 19 deployed; bash-governance folded into cross-project rule | correspondence verified; 4 bash-shape indicators present; sole NO-DEPLOY = expected fold-in | PASS |
| C2-5 | mg-grant, mg-revoke on PATH | present | PASS |
| C2-6 | Backup set vs refreshed spec | full set inventoried, matches (8 `.bak-*` files) | PASS |
| C2-7 | Grants file generated-form | confirmed | PASS |

## Findings

1. **CF-1/CF-2 verified APPLIED.** The spec refresh (backup inventory full set;
   `opencode.jsonc` naming) was approved pre-run and applied — this run re-checked
   against the corrected spec and matched. Prior flags closed.
2. **CF-3 verified:** the guard token-match class held — two build-phase commands
   containing the token `cupcake` were denied (honored, rerouted via approved glob
   form); one relative-path command containing the same token later passed,
   reconfirming the nondeterminism documented in [[config-manager-learnings|Learnings]].
   Denials recorded as liveness evidence per the standing doctrine.
3. **CF-5-class verification:** the ID'd check inventory (C0-1…C2-7, 17
   agent-runnable checks) executed correctly from this plan — the template format
   is proven. Eligible for graduation into the skill.

4. **SCOPED FINDING (new, real): bash-mediated writes do not decrement grant counts.** The plugin's decrement hook fires for file-tool writes (proven: 2→1→0) but not for Bash-tool writes (three bash redirects left count untouched while all were allowed). Consequence: a grant with count N permits **unlimited bash-mediated writes** to the granted path until grant expiry — the bash-governance amendment made bash writes *deniable* under the boundary, but the decrement mechanism was not extended to them. All checks otherwise pass, so no upgrade/unlock pressure — but this is a genuine present-≠-fully-working finding in the grant mechanism. → learning filed; **developer decision required** (see open question).
5. **Version corroboration (C3-4):** upstream latest **v0.5.1** vs installed **0.3.0** — gap recorded; per standing policy, upgrade only on check failure (none observed). Spec open item 3 updatable.

## Open question for the developer (C3-3 finding 4)

The decrement gap on bash writes: is **file-tool-only decrement the intended design** (bash shapes enforce the boundary via denial instead — which they do: ungranted bash writes ARE blocked), or should bash writes decrement too? **My recommendation:** accept file-tool-only decrement as intended design, and record it in [[cupcake-config|Cupcake Configuration]]'s grant mechanics section (one sentence: "count decrement fires for file-tool writes; Bash-mediated writes within a granted path are permitted without decrement until grant expiry"). Rationale: bash writes inside a *granted* folder are already inside a developer-approved slip; expiry bounds exposure; extending decrement to bash shapes would be a plugin code change for marginal gain — "never change what is working well without a sound justified reason."

## Guard layers

One outbound-network denial received this run (C0-2 probe) + two build-phase
token-match denials — all honored, all recorded. Enforcement is live, mechanical,
and now exam-verified.

## Tier 3 — deep pass (developer-verified 2026-09-13)

| ID | Check | Result |
|---|---|---|
| C3-1 | Authoritative live eval (allow case) | **PASS (D)** — clean `{"decision":"allow"}`; 23 policies matched, WASM compiled from all 24 files, project-local scan correctly empty (global-only deployment) |
| C3-2 | Block case | **PASS (D)** — `deny` with the exact outbound-network reason (rule `GLOBAL-POLICY-OUTBOUND-NETWORK-ACCESS-IS-ALLOWLIST-ONLY`), consistent across two runs |
| C3-3 | Grant lifecycle | **PASS for file tools — with a scoped finding (see 5).** Agent-executed: grant count=2 → Write-tool write allowed (2→1, decrement verified in the grants file) → Write-tool write allowed (1→0) → third Write-tool write **DENIED** (count exhausted). Bash-mediated writes: **no decrement fires** (three bash redirects left the count untouched; count=0 denial still applies to both tool types). Cleanup: grant revoked |

## C3-3 the corrected test — how it actually had to run

Two design errors were caught and corrected during this check, each instructive:

1. First attempt (`/tmp`): always-open path — grant never exercised. 
2. Second attempt (developer's bare terminal): writes bypass Cupcake entirely — the plugin's hooks fire only on *agent* tool calls, so no decrement can ever occur there.
3. Final design (agent-executed): grant as agent → file-tool writes from this session → decrements observed → exhaustion denial received. This is the only valid test path: **the enforcement point lives inside agent sessions.**
| C3-4 | Version corroboration | **CORROBORATED (D)** — upstream publishes releases: latest **v0.5.1**; installed **0.3.0**. Gap recorded; no upgrade action (all checks pass — upgrade only on check failure, per policy). Spec open item 3 updatable |

**Bonus evidence from the eval output (developer-verified):** all 24 policy files parsed successfully by name (19 custom + grants-data + 3 builtins + evaluate.rego — matches inventory exactly); unified WASM module compiled (466,125 bytes); project-local scan found 0 policies as expected (global-only deployment — the `WARN No valid policies found` line for the empty project skeleton is expected behavior, not a fault).

*End of report — Tier 3 partially open (C3-3 corrected test pending; C3-1/2/4 complete).*
