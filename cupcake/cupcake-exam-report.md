---
title: "cupcake-exam-report"
doc-id: "mb-19213c10"
updated: "2026-10-04"
---
# Cupcake — Exam Report

Run #2 — second formal plan-driven run (2026-10-04). Plan:
[[[mybizz-config-docs:cupcake/cupcake-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-exam-plan.md) (step-0: PASS with estate finding F-S0-1 —
register body-hash columns stale ×15, re-recorded this run under F-8 with the
method pinned in the register notes). Spec: [[cupcake-config|Cupcake
Configuration]] (re-baselined this run under F-3/F-5). Detection only for the
live system; approved doc-side repairs applied in-run; deny-listed code repairs
staged for developer application.

## Verdict: HEALTHY+FLAGS — enforcement proven live; 27/27 files compile; two grant-machinery defects found, staged fixes approved; post-fix verification PASS 2026-10-04 (F-1/F-2 closed; F-7 live in-project, ancestor case carried forward)

## Tier 0 — Liveness: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| C0-1 | Binaries resolve (fs listing) | real binary + symlinks per spec | exact match; opa real file via symlink chain | PASS |
| C0-2 | Enforcement firing | deny on harmless known-blocked probe | **outbound-network deny received** (curl to a non-allowlisted `.invalid` host) | PASS |
| C0-3 | Plugin single live copy | one live plugin | one live copy + 4 correctly-suffixed backups | PASS |

## Tier 1 — Health: PASS

| ID | Check | Expected | Actual | Result |
|---|---|---|---|---|
| C1-1 | `opa check` all deployed + builtins + system + fallback skeleton | 0 failures | **27 files checked, 0 failures** | PASS |
| C1-2 | Scaffold absence; repo skeleton intact | none; placeholder present | no scaffold files; repo `.cupcake/` carries the input-gated placeholder (`failMode: open` in its opencode.json) | PASS |
| C1-3 | Backup suffix discipline | nothing loadable among backups/cruft | all `.bak`/`.bak2`/`:Zone.Identifier` artifacts non-loadable (cruft recorded → F-4) | PASS |
| C1-4 | Grants data files generated-form | generated markers present | all three files carry METADATA + `custom.id` (`GLOBAL-GRANTS-DATA`, `GLOBAL-GIT-GRANTS-DATA`, `GLOBAL-NETWORK-GRANTS-DATA`) | PASS |

## Tier 2 — State conformance: PASS with F-3/F-4 drift (spec corrected this run)

| ID | Expected | Actual | Result |
|---|---|---|---|
| C2-1 | Inventory vs spec | live: 20 custom + 3 builtins + 3 grants-data + aggregator (spec said 19 + 2 data files) | DRIFT → F-3; spec re-baselined |
| C2-2 | `"task": "deny"` in opencode.jsonc | present (line 11) | PASS |
| C2-3 | spawn-tools-denylist exact | exactly task, delegate, call_omo_agent, agent_session_create | PASS |
| C2-4 | 20 sources ↔ 19 deployed; fold-in; bash-shape indicators | correspondence verified both legs (source read approved mid-run); allowance clauses present in both amended sources; 4+ bash-shape indicator groups live; `skills-collective` absent from the deployed rule (a historical mention in the source doc's amendment note is prose, not an entry); **new finding F-11**: deployed exempt list is `/tmp/`-only while the source doc documents an 8-entry always-open list | PASS with F-11 |
| C2-5 | Grant tooling present on PATH | all five tools present (`mg-grant`, `mg-revoke`, `git-grant`, `net-grant`, `net-revoke` — the latter two undocumented → F-3); PATH carries both homes; verified via Read-tool inventory after the name-matcher denial (F-10) | PASS |
| C2-6 | Backup set vs spec | spec stale (dated cross-project backups gone; undated `.bak`/`.bak2` + Zone.Identifier cruft live) | DRIFT → F-4; spec refreshed to post-cleanup state |
| C2-7 | Grants files present, generated-form | all three, generated-form | PASS |

## LG items — both 2026-09-22 amendments verified live

- **LG-1 set-and-forget:** `failMode: open` default + fallback-home logic in the
  live plugin; fallback skeleton = exactly the five expected files, all compile;
  `.bak-20260922-pre-amendment` present.
- **LG-2 WP3 commit-allowance:** allowance clause live (commit/push/merge
  grantable; publish/deploy absolute); exclusive `-C` resolution; empty
  git-grants file fails closed; `.bak-20260922-pre-wp3` present; `git-grant` on
  PATH.

## Grant-enforcement investigation (developer-requested item)

| # | Question | Answer |
|---|---|---|
| GR-1 | How grants are recorded | `mg-grant` reads the live file via `opa eval`, merges via jq, regenerates the whole file through a `.rego` temp + `opa check` before mv. No separate state store — **decrements persist across re-grants**. Paths canonicalized to lowercase WSL form. Path/network grants: hardcoded +30 min expiry; `git-grant`: `--minutes` (default 30) |
| GR-2 | Counts decrease / enforced? | Yes, sequentially — decrement per successful write-type tool call (write/edit/patch/multiedit/notebookedit), longest-prefix match, count>0 gate. Proven live twice this run (developer's count-1 grant 1→0; the two mb-config-manager writes 2→0). Bash-mediated writes never decrement (accepted design, 2026-09-13). **Defect F-2: the read-modify-write is unserialized — parallel tool calls race and lose decrements** |
| GR-3 | Expiry? | Enforced by the plugin's before-hook prune for path + git files (BigInt ns, fail-safe). **Not for network grants — the plugin never touches that file (F-1)** |
| GR-4 | `mg-revoke`? | Exact canonical entry `del()`, same opa-check safety; silent no-op on absent entry |
| GR-5 | Ungranted skills-dir writes? | The cross-project rule blocks only writes outside the session cwd tree; the control-plane rule covers the plugin but not the skills dir. A session launched from an ancestor of `~/.config/opencode/skills/` sees those writes as in-project (→ F-7) |
| GR-6 | Live probes | **Pre-fix probe executed with developer-issued grant:** two parallel Write calls against a count-2 grant → count fell only 2→1 (one decrement lost); a third write was then ALLOWED at count 1 and decremented to 0. **Three successful writes against a two-write grant — the race and the over-allowance proven live.** Post-fix re-probe executed 2026-10-04: **PASS** — two parallel writes both allowed and decremented (count 0 exactly), third write denied |

## Findings

| # | Class | Finding | Disposition (gate 2026-10-04) |
|---|---|---|---|
| F-1 | UNHEALTHY | Network-grant channel has no enforcement legs: no prune, no decrement for `cup-network-grants-data.rego`; the rule allows on existence+count with no time check. Live proof: `opencode.ai count=3` issued 2026-09-13, expired ~3 weeks, still granting | **Approved:** extend the plugin's prune + decrement to the network file — staged in `/tmp/cupcake-staging/cupcake.js`; **applied by the developer 2026-10-04 and verified PASS** (count-1 `example.com` grant: first fetch allowed, second denied) |
| F-2 | UNHEALTHY | Grant decrement/prune is a non-atomic read-modify-write; parallel tool calls lose decrements (proven live in GR-6; consistent with the developer's 2026-10-04 numbers: ~27 writes vs count 22; 4 vs 3) | **Approved:** serialize every grants-file RMW with a mkdir-lock in the plugin and all five grant tools — **applied 2026-10-04 and verified PASS** per the GR-6 re-probe protocol |
| F-3 | DRIFT | Spec inventory stale: 20th custom rule (`cup-protect-cupcake-control-plane.rego`, no source document), third grants file + `net-grant`/`net-revoke`, allowlist 11 not 10 | **Approved + applied:** spec re-baselined this run |
| F-4 | DRIFT | Backup inventory stale + cruft: five `:Zone.Identifier` artifacts, `system_protection.rego (2).bak`, undated `.bak`/`.bak2` where the spec listed dated ones | **Approved:** removal commands handed to the developer; spec refreshed to post-cleanup state |
| F-5 | DRIFT | Spec promised an always-open shared-library tier; live exempt list is `/tmp/` only; 2026-09-24 broadening→revert episode unrecorded in the spec | **Approved + applied:** spec states current exempt list; episode recorded in the log (F-6), not the spec |
| F-6 | GAP | Log silence 2026-09-22 → 2026-10-04 despite real events (net-grant creation 2026-09-13; control-plane rule creation + broadening/revert 2026-09-24) | **Approved + applied:** backfill row appended to the log this run |
| F-7 | GAP | `~/.config/opencode/skills/` protected only cwd-relatively | **Approved:** grant-required from every session — staged rule amendment (`needs_grant_check`); not absolute; skill installs use grants. **Applied 2026-10-04; verified from a session in the cupcake folder** (ungranted skills-dir write denied); the ancestor-cwd case carried to the next exam (see Post-fix verification) |
| F-8 | DRIFT | Register body-hash columns stale ×15; method undocumented (step-0 F-S0-1) | **Approved + applied:** all 15 rows re-recorded; method + reference command pinned in the register notes |
| F-9 | GAP | config-manager-log carried a duplicated S-4 row | **Approved + applied:** duplicate removed this run |
| F-10 | GAP | New guard-denial class: the control-plane rule denies bash command text that merely NAMES the grant tools (caught a `command -v` probe); plus 4 exec-protection token/path false-positives this run — including a `sed -n` READ of a control-plane path treated as a sed write | Recorded; learning filed; C2-5 verifies via Read-tool inventory + PATH |
| F-11 | DRIFT | Deployed cross-project exempt list (`/tmp/` only) diverges from its source doc's 8-entry always-open list (incl. `mybizz-config-docs`, `logs`, both config homes) — live consequence: writes to those folders currently require grants (this session's own grant corroborates). **Raised after the gate (emerged from the approved C2-4 source read)** | **Dispositioned 2026-10-04:** keep the deployed `/tmp/`-only state; the rule is NOT changed; the source doc is corrected to present state (staged in `/tmp/cupcake-staging/no_cross_project_filesystem_access_by_default.md`, developer applies); spec already states current state — **source-doc correction applied 2026-10-04; source and deployed rule now match** |

## Liveness evidence

Outbound-network deny received on the C0-2 probe (rule
`GLOBAL-POLICY-OUTBOUND-NETWORK-ACCESS-IS-ALLOWLIST-ONLY`); five guard denials
honored during the run (four exec-protection token/path matches, one
control-plane grant-tool name match) — all recorded, none worked around; two
clean decrement sequences observed in the grants file.

## Post-fix verification (2026-10-04) — F-1/F-2 PASS; F-7 live in-project; run #2 closed

The developer applied all staged files on 2026-10-04 — the five grant tools
(the F-2 lock), the cross-project rule (the F-7 amendment and the corrected
block message), the plugin (F-1 + F-2), and the F-11 source-document
correction — restarted OpenCode, and re-ran the probes from a fresh web-UI
session.

| Check | Result |
|---|---|
| Cupcake active post-restart | an ungranted write to `/mnt/c/mybizz/scripts` was denied |
| F-1 — network-channel prune + decrement | **PASS:** with an `example.com` grant of count 1, the first fetch was allowed and the second denied |
| F-2 — serialized RMW (the GR-6 re-probe, per the recorded protocol) | **PASS:** with a grant of count 2, two parallel writes were both allowed (and both decremented — count 0 exactly), and the third write was denied |
| F-7 — skills-dir grant requirement | confirmed from a session opened in the cupcake folder: an ungranted write to `~/.config/opencode/skills` was denied. The target is outside that project regardless, so this confirms the rule but not the ancestor-cwd case |

Note: the recorded protocol's expired-entry-prune confirmation was not part of
the reported results — the F-1 PASS rests on the allow→deny sequence.

### Carried forward to the next exam — the skills-dir ancestor-cwd case

Observation as reported: a session of the terminal version of OpenCode,
started in `/home/dev-p`, was allowed to write to `~/.config/opencode/skills/`
without a grant. Unknown: whether (a) Cupcake loads in the terminal interface
at all, or (b) the F-7 rule fails when the session starts in an ancestor
folder of the target. Exact check to run — two steps, in order, because the
write probe only means something if step 1 first proves enforcement:

1. **Terminal liveness probe (cwd-independent).** From a terminal-OpenCode
   session opened in `/home/dev-p`, fetch a non-allowlisted host (the C0-2
   probe shape). Expected under enforcement: the outbound-network deny (rule
   `GLOBAL-POLICY-OUTBOUND-NETWORK-ACCESS-IS-ALLOWLIST-ONLY`). An allow here
   means Cupcake is not enforcing in the terminal interface — record that as a
   new finding and stop; do not run step 2.
2. **Ancestor-cwd F-7 probe (only if step 1 denied).** From the same session,
   attempt an ungranted Write to a probe file under `~/.config/opencode/skills/`
   (for example `zz-grant-probe/probe.txt`, content `probe`). Expected under
   the amended rule: deny — the grant requirement holds from every session,
   whatever the working directory. An allow indicts the F-7 rule from an
   ancestor cwd: record the deployed
   `cup-no_cross_project_filesystem_access_by_default.rego` behavior as a new
   finding.

Neither step requests or uses a grant — both expect denial.

## Runner attribution / deferred

- Tier 3 (C3-1…C3-4): **locked** per developer instruction — remains
  developer-run if unlocked later.
- Deny-listed code repairs (F-1/F-2/F-7): applied by the developer 2026-10-04;
  post-fix verification PASS (see above) — F-1/F-2 closed, F-7 live in-project
  with the ancestor case carried forward.
- F-4 cleanup + network revoke: developer-run commands handed over.
- F-11: decision received and the source-doc correction applied 2026-10-04.
- Carried to the next exam: the skills-dir ancestor-cwd check (exact steps in
  the Post-fix verification section).

*End of report — run #2 closed 2026-10-04 on the post-fix verification: F-1
and F-2 closed, F-7 live in-project with the ancestor case carried to the next
exam.*
