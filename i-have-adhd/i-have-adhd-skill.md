---
title: "i-have-adhd-skill"
doc-id: "i-have-adhd-skill"
---
# mb-config-i-have-adhd — Exam Skill

Exams the i-have-adhd output-style skill's configuration state against its spec.
This skill holds the **procedure** only — expected values live in the spec doc and
are read fresh at the start of every run. The skill under exam is working well;
this exam verifies that and repairs nothing.

- Spec: [[i-have-adhd-config|Configuration]] — read it first, every run
- **Exam plan: [[i-have-adhd-exam-plan|Exam Plan]] — read second, every run.**
  The plan-driven cycle: the config-manager synthesizes this plan fresh before
  each run (from spec + last report + log + learnings) and this skill executes it
  in hand. The plan carries run-specifics and deltas; the **standing check
  inventory lives in this skill** (below) — permanent occurrences graduate here,
  never into plans
- Reference: [[i-have-adhd-reference|Reference: Invocation, Operation, Update]] — invocation, operation,
  update, uninstall, the do-not list
- Report: [[i-have-adhd-exam-report|Exam Report]] — one file, overwritten each
  run (write-then-replace)
- Log: [[i-have-adhd-log|Log]] — one run row per exam; free rows for
  notable events witnessed between runs
- Learnings: [[i-have-adhd-learnings|Learnings]] — file new patterns/nuances;
  delete entries once graduated into a permanent home
- Provenance: [[i-have-adhd-intro|I Have Adhd Intro]] — research notes from
  third-party sources; **never treated as verified state**

## Scope boundary (anti-duplication)

- This module exams **the i-have-adhd skill**: its bundle, activation surfaces
  (slash command, always-on marker), single-path discipline, run evidence, and
  the suite itself.
- **OpenCode machinery** (version, global-config consolidation, plugin
  load-once, MCP entry, permission posture, Active Project Standard) belongs to
  `mb-config-opencode` — this exam reads `opencode.json` only for the narrow
  install-surface fact that no i-have-adhd wiring exists, never re-probes the
  config's own conformance.
- **GStack skills** belong to `mb-config-gstack`. **Vendor-skill estates with
  their own modules** (magdoub-wireframe, matt-pocock-skills,
  anvil-agent-references) are examined by their own modules.
- The component has **no MCP entry, no database, no provider dependency, no
  scheduler, no credentials** — there is nothing else to boundary against.

## Credential discipline (hard rule)

This component has none. No credential is required or referenced by the skill
bundle, its activation surfaces, or any check in this inventory. If one is ever
discovered, the estate-wide rule applies: reference it **by variable name
only** — never print, log, or copy the value into reports, outputs, or
learnings.

## Hard behavioral rules (from the suite's own Do-not list)

- The component is a **prose output-style skill** — the exam never "fixes"
  output style by touching anything; DO NO DAMAGE, detection and verification
  only.
- **Never toggle the always-on marker** (`~/.config/opencode/.i-have-adhd-always`)
  — its presence is the developer's standing always-on decision (settled policy
  2026-09-19); toggling it silently changes every session's output style. Verify
  its state; never change it.
- **Never hand-patch the installed `SKILL.md` or `agents/` files** — vendor
  material; changes arrive via upstream and reinstall (developer-run).
- **Never remove or rewrite the `~/.config/skills` symlink** — shared
  infrastructure, not this skill's property.
- **Never create a second activation path** (duplicate skill dir, second
  slash-command file) — including as a "repair".
- **Never run any `npx skills` install/update command** as an exam action —
  content-changing to the bundle; developer-only (Tier 3).
- **Never probe the upstream repository over the network** without the
  developer bundle — outbound-network guard class, and the developer's standing
  decision records upstream as deliberately unverified.
- Never assume `stop adhd mode` survives a session — the marker re-applies the
  ruleset at every new session start; the phrase is mid-session only.
- Never treat [[i-have-adhd-intro|I Have Adhd Intro]] as verified state — research provenance.
- Never claim a standing version pin — the recorded drift-guards are the
  byte-identity checks (IA1-1/IA1-4) and the upstream verification of record
  (spec §Identity, 2026-09-20: bundle byte-identical to upstream main, HEAD
  pin recorded).
- Never treat the 5-item list cap as license to omit analysis — rule 9 shapes
  presentation only; the exam's own findings lists stay complete.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| IA0-1 | A | Skill bundle invocable: `/home/dev-p/.config/opencode/skills/i-have-adhd/SKILL.md` exists, frontmatter parses | Present; `name: i-have-adhd` exact (config §Identity). Failure = DOWN |
| IA0-2 | A | Slash command present: `~/.config/opencode/command/i-have-adhd.md` exists, references the skill by name | Present (config §Install surface) |
| IA0-3 | A | `disable-model-invocation: true` intact in SKILL.md frontmatter | `true` (config §Identity — Model invocation). Flip = DRIFT with behavioral consequence (the model could self-activate the skill) |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| IA1-1 | A | Bundle byte-level contents + sha256 first-16 (spec §Bundle contents): `SKILL.md` 7,207 B / 142 lines (`3170b16ace00aecb`); `agents/gemini.toml` 2,157 B (`5108a6123beb9df2`); `agents/openai.yaml` 238 B (`2c51291283dcefdc`) | Exact (config §Bundle contents, verified 2026-09-20). Mismatch = DRIFT (installed-edited, or upstream changed without a spec re-baseline) |
| IA1-2 | A | Always-on marker: `~/.config/opencode/.i-have-adhd-always` present and empty (0 bytes) | Present + empty (config §Current state; §Settled policy — always-on, developer decision 2026-09-19). Absence = DRIFT against settled policy; non-empty = UNHEALTHY (unknown semantics; never read-interpret it — flag) |
| IA1-3 | A | Global skills symlink: `~/.config/skills` resolves to `~/.config/opencode/skills` | Exact target (config §Install surface) |
| IA1-4 | A | Dual-path bundle identity: the npx CLI's primary install (`~/.agents/skills/i-have-adhd/`) and its CLI-derived OpenCode copy (`~/.config/opencode/skills/i-have-adhd/`) are byte-identical (sha256 first-16 per file, spec §Bundle contents); exactly one slash-command file; no manually created third copy | Both copies byte-identical (spec §Install surface — installer dual-write, registry primary). Divergence = DRIFT (dedup becomes path-dependent); a manually created additional copy = DRIFT (config Do-not: no second activation path) |
| IA1-5 | A | No i-have-adhd wiring in `~/.config/opencode/opencode.json` | No entry (config §Install surface — "Nothing"). Search for the skill's name only; opencode.json conformance itself is `mb-config-opencode`'s domain |
| IA1-6 | A | Suite completeness: 8 files in `mybizz-config-docs/i-have-adhd/` (config, exam-plan, exam-report, log, learnings, explainer, reference, skill source) + [[i-have-adhd-intro|I Have Adhd Intro]] (provenance) | All present (missing file = GAP) |
| IA1-7 | D | Upstream live state: GitHub repo check (activity, stars, publisher identity, HEAD vs installed bundle content) | Recorded into spec open items 1–2 (watch W-1/W-2). Developer-run — outbound network; feeds the run's developer bundle |

## Tier 2 — Functional proof (present ≠ working; read-only — no content changed by any probe)

| ID | Runner | Check | Expected |
|---|---|---|---|
| IA2-1 | A | **Self-evidence probe:** when the marker is present (IA1-2 PASS), the running exam session's own system prompt carries the always-on ruleset block ("ADHD MODE ACTIVE (always-on)" + the persistence note) — the exam session is itself a marker-governed OpenCode session. Marker present + block absent = the injection mechanism is broken → UNHEALTHY. Marker absent (already flagged at IA1-2) = N/A, not failing | Block present when marker present (config §Current state — the observed run-evidence mechanism) |
| IA2-2 | A | Ruleset structure conformance (read-only): the installed `SKILL.md` carries the persistence clause, all 10 rule headings, the 6 sanctioned overrides, and the 5-item pre-send check | All present (config §Bundle contents role; reference §What active mode does). Missing structure = DRIFT (truncated or corrupted copy — the injector would serve a broken ruleset) |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| IA3-1 | D | Upstream verification (closes W-1/W-2): fetch `github.com/ayghri/i-have-adhd` — stars, last commit, publisher; compare the upstream `SKILL.md` against the installed bundle (byte or content diff) | Outcome recorded into spec open items 1–2 + log; content drift → DRIFT finding + spec re-baseline proposal (docs governance) |
| IA3-2 | D | Update-mechanism verification (closes W-3): re-run `npx skills add ayghri/i-have-adhd -a opencode -y -g`; verify overwrite behavior, slash-command survival, byte-level delta vs IA1-1's baseline | Outcome recorded into spec open item 3; content-changing to the bundle — never agent-run |
| IA3-3 | D | Supply-chain review discharge (closes W-4): record publisher / license / maintenance / spawn-capability axes into the config (gated spec edit, magdoub precedent) | Review recorded with gate approval |

## Report

Write [[i-have-adhd-exam-report|Exam Report]]: verdict line; per-tier tables (check ID,
expected, actual, result); findings with class + evidence + recommended repair +
risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[i-have-adhd-log|Log]] (run-row format per
[[config-manager-reference|Reference: Commands, Procedures]]); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **No agent-healable items** — the skill bundle, the always-on marker, the
  slash command, and the symlink are vendor/policy surfaces; every repair is
  developer-run or proposed
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): the always-on marker (policy surface;
  toggling it silently changes every session's output style) · the installed
  `SKILL.md` + `agents/` (vendor material — never hand-patched) · the
  slash-command file · the `~/.config/skills` symlink · any `npx skills`
  install/update command · any upstream network probe without grant
- Credentials: this component has none — estate-wide name-only rule applies if
  one is ever discovered
