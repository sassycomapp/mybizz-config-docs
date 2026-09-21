---
name: mb-config-gstack
description: GStack configuration exam — verifies the GStack workflow layer's live configuration state (clone version/HEAD, discovery link topology, config files, binary tree, integration facts) against gstack-config.md and proves the installation functionally executes; detection and verification only — GStack is working well and this module changes nothing; catches silent failures and proposes gated repairs. Use when asked to "exam gstack", "check gstack health", or as part of a full mb-config-manager run.
---

# mb-config-gstack — Exam Skill

Exams GStack's configuration state against its spec. This skill holds the
**procedure** only — expected values live in the spec doc and are read fresh at
the start of every run. GStack is working well; this exam verifies that and
repairs nothing.

- Spec: [[gstack-config|GStack Configuration]] — read it first, every run
- **Exam plan: [[gstack-exam-plan|Exam Plan]] — read second, every run.**
  The plan-driven cycle: the config-manager synthesizes this plan fresh before
  each run (from spec + last report + log + learnings) and this skill executes it
  in hand. The plan carries run-specifics and deltas; the **standing check
  inventory lives in this skill** (below) — permanent occurrences graduate here,
  never into plans
- Reference: [[gstack-reference|GStack Reference]] — workflows, commands, brain sync,
  restart/refresh
- Report: [[gstack-exam-report|Exam Report]] — one file, overwritten each run
  (write-then-replace)
- Log: [[gstack-log|Log]] — one run row per exam; free rows for notable
  events witnessed between runs
- Learnings: [[gstack-learnings|GStack Learnings]] — file new patterns/nuances; delete
  entries once graduated into a permanent home

## Scope boundary (anti-duplication)

- This module exams **GStack itself**: clone version/HEAD, discovery topology
  (both link generations + aggregate + legacy path), `GSTACK_BIN`, the
  `~/.gstack` config files, the binary tree, generation discipline, and the
  integration facts (skill-index cross-link, outputs convention — recorded
  convention only, the `gstack-outputs/` copy lane does not exist on this
  system, verified 2026-09-16 — and GBrain adjacency, not memory-family
  membership, per developer correction 2026-09-16).
- **GBrain server conformance** (binary, config, schema pack, sources, models,
  MCP entry, sync machinery) belongs to `mb-config-gbrain` — this exam reads
  `~/.gstack/gbrain-detection.json` and `gbrain-repo-policy.json` as GStack-side
  records only; it never re-probes the GBrain server itself.
- **Dream-cycle pipeline** belongs to `mb-config-gbrain-dream-cycle` — GStack
  ships `/sync-gbrain`; its source-overlap trap is a knowledge check here
  (reference §GBrain-facing skills), never a live probe.
- **OpenCode structure rows** (symlink + hybrid rows) belong to
  `mb-config-opencode` — this exam confirms the rows' targets exist, never
  re-audits OpenCode's config.
- **Cross-tool skill enumeration** belongs to [[skill-index|Skill Index]] (docs-managed) —
  this exam checks the discovery **mechanics** (that the documented link
  topology resolves), never re-audits the inventory.

## Credential discipline (hard rule)

The credential surfaces are `~/.gstack` config files that may embed
environment/token references and the `.env.example` template in the clone.
Reference anything credential-like **by variable name only** — never print, log,
or copy values into reports, outputs, or learnings. Sensitive-data guards block
agent reads of these files by class (proven for `.env` patterns and config.json
class files): a denied read becomes a developer-run request — honored
absolutely, never retried through an alternate path. `.env.example` content
verification (the "one template line" claim) is classified developer-run (D).

## Hard behavioral rules (from the suite's own Do-not list)

- Never hand-edit any generated `SKILL.md` — auto-generated from
  `SKILL.md.tmpl`; regenerate via `bun run gen:skill-docs`. A hand-edit would be
  silently overwritten on the next generation.
- Never delete `~/.config/opencode/skills/gstack/bin` — actively managed by
  setup, regenerated every run; not leftover.
- Never assume the folder name is the command — the frontmatter `name:` field
  decides the command; bare names except `/gstack-upgrade` and `/gstack`.
- Never run `/sync-gbrain --dream` against a manually-registered GBrain source —
  source-overlap trap; the honest bypass is `gbrain dream --source <id>`.
- Never trust `/setup-gbrain`'s own GBrain backend description — this
  environment runs self-hosted PostgreSQL; [[gbrain-config|Configuration]] is authoritative.
- Never remove the OpenClaw `gstack-openclaw-*` skill folders — updates recreate
  them; removal is churn, not a fix.
- Never treat upstream `1.81.0.0` documentation (Aside-first browser, team mode,
  prune-on-setup) as current behavior here — installed is `1.58.1.0`.
- Never probe content of `~/.gstack` credential-bearing files or the clone's
  `.env` — guards deny by class; a denied check becomes developer-run.

## Tier 0 — Invocability (run first; failure = report `DOWN`, stop; remaining tiers skipped)

| ID | Runner | Check | Expected (source: config §) |
|---|---|---|---|
| GS0-1 | A | Clone version/HEAD: `git -C /mnt/c/mybizz/gstack rev-parse --short HEAD` + `VERSION` + `package.json` version | HEAD `c7ae632`; `VERSION` = `1.58.1.0` = `package.json` version (config §Identity). The available upgrade is a recorded open decision — **never upgraded on newness**; upgrade only on check failure (GS3-2) |
| GS0-2 | A | Discovery topology resolves: per-host tree `/mnt/c/mybizz/gstack/.opencode/skills/` exists; `~/.config/opencode/skills/gstack-<name>` prefixed links and bare-name links present; aggregate `~/.config/opencode/skills/gstack/` hybrid entry exists | Both link generations + aggregate present (config §Install topology) |
| GS0-3 | A | `GSTACK_BIN` resolves: `~/.config/opencode/skills/gstack/bin` → `/mnt/c/mybizz/gstack/bin`; legacy `~/.claude/skills/gstack` → `/mnt/c/mybizz/gstack` | Symlinks point into the clone (config §Install topology) |

## Tier 1 — State conformance (each probe compared to the spec's current expected value; any mismatch = DRIFT finding)

| ID | Runner | Check | Expected |
|---|---|---|---|
| GS1-1 | A | Per-host skill tree count: `ls /mnt/c/mybizz/gstack/.opencode/skills/` | 54 entries (53 `gstack-<name>` + aggregate `gstack`) (config §Install topology). Count change = DRIFT (inventory change, not necessarily a defect — record the delta) |
| GS1-2 | A | Binary tree: `ls /mnt/c/mybizz/gstack/bin/` | 74 scripts (config §Install topology) |
| GS1-3 | A | Broken discovery entries: `codex`, `connect-chrome`, `hackernews-frontpage` resolve targets | Targets `/mnt/c/mybizz/skills/` (retired folder — absent) — **dead is the expected state**; inert, OpenCode skips them (config §Install topology). A *live* target here would be the finding |
| GS1-4 | A | `~/.gstack/config.yaml` live values (read — guard denial = D) | `artifacts_sync_mode: full` · `telemetry: community` · `question_tuning: true` · `user_slug_at_local: dev-p`; all other keys commented defaults (config §Config files) |
| GS1-5 | A | `~/.gstack/gbrain-detection.json` + `~/.gstack/gbrain-repo-policy.json` (read — guard denial = D) | Detection: engine `postgres`, doctor ok, `gbrain_mcp_mode: none`, sync `full`, remote `""`; policy: 8 repos, all `read-write`, all `github.com/sassycomapp/*` (config §Config files) |
| GS1-6 | A | GBrain worktree: `~/.gstack-brain-worktree/` exists, git-backed; `~/.gstack-brain-remote.txt` absent | Worktree present with `.brain-allowlist`/`.brain-privacy-map.json`/analytics/sessions; remote file **absent** — local-only sync is the design (config §Config files) |
| GS1-7 | A | `~/.gstack/last-update-check` content (read — guard denial = D) | `UPGRADE_AVAILABLE 1.58.1.0 1.61.0.0` — the stale string is the documented expected state (config §Identity); it being *current* (1.81.0.0) would not be a failure either — the artifact's staleness is a recorded open item (W-3), not a defect |
| GS1-8 | A/D | `.env` absence in the clone; `.env.example` single template line | `.env` absent in `/mnt/c/mybizz/gstack/` (directory listing — A); `.env.example` content claim = D (sensitive-data guard class) (config §Config files) |
| GS1-9 | A | Generation discipline: `SKILL.md.tmpl` exists; `gen:skill-docs` present in `package.json`; `slop-scan.config.json` = `{"ignores": ["**/vendor/**"]}` | All three present, values match (config §SKILL.md generation + §Config files) |
| GS1-10 | A | Suite completeness: the seven files in `gstack/` (config, exam-plan, exam-report, log, learnings, explainer, reference) + the skill source `gstack-skill.md` | All present (missing file = GAP) |

## Tier 2 — Functional proof (present ≠ working; read-only execution probes — no clone mutation, no skill invocation)

| ID | Runner | Check | Expected |
|---|---|---|---|
| GS2-1 | A | Deterministic bin invocation: run one read-only bin script to completion (e.g. `bash /mnt/c/mybizz/gstack/bin/gstack-gbrain-detect` or `gstack-brain-sync --status`) | Script executes and exits 0 with sane JSON/status output. Proves the documented binary tree is live, not just present. Guard denial → D |
| GS2-2 | A | Discipline probe — generation rule holds: read one generated `SKILL.md` from `/mnt/c/mybizz/gstack/.opencode/skills/<name>/` and verify its frontmatter `name:` matches the command convention (bare name, or `gstack-upgrade`/`gstack` for the two exceptions) | Frontmatter `name:` present and matches the command rule (config §SKILL.md generation + skills-reference §Invocation rules). Confirms no drift toward folder-name-command assumptions |

## Tier 3 — Deep pass (developer-run; executes only if the developer unlocks this tier)

| ID | Runner | Check | Expected |
|---|---|---|---|
| GS3-1 | D | Full functional lifecycle: agent-visible invocation of a real GStack skill in a live session (plan→review flow or one browser/QA skill) | Skill runs to completion per its documented exit condition. Expensive: minutes, real session work, artifact writes |
| GS3-2 | D | Upgrade execution (`1.58.1.0` → available newer version) | Developer decision, pending; policy: **never on newness — only on check failure**. Requires coordinated re-run of `./setup --host opencode`, GSTACK_BIN regeneration, topology re-verification, and acceptance of the Aside-first browser change (config §Open items — W-1) |

## Report

Write [[gstack-exam-report|Exam Report]]: verdict line; per-tier tables
(check ID, expected, actual, result); findings with class + evidence + recommended
repair + risk; runner attribution for every deferred item (guard-forbidden vs
unlock-gated); overwritten in full each run (write-then-replace: failed runs
never touch the prior report; written before any pruning). Then: one run row
appended to [[gstack-log|Log]] (run-row format per
[[config-manager-reference|Reference: Commands, Procedures]]); new learnings filed.

## Gate protocol

- Findings → classify → present with evidence + recommended repair + risk
- **Allowlist of agent-healable repairs:** none standing — GStack is working
  well; every repair is developer-run or proposed. (A proposed allowlist item
  would graduate here only after a run proves it safe and the developer
  approves it.)
- Spec-doc corrections → flagged to docs governance, never applied here
- Deny-list (never heal, never touch): generated `SKILL.md` files in the clone
  (regenerate, never hand-edit) · `~/.gstack` credential-bearing file content
  (never read by the agent, never printed) · the retired `/mnt/c/mybizz/skills/`
  folder and its dead links (deletion is cleanup decision, developer-owned) ·
  the upgrade decision itself (GS3-2, developer-owned) · any `./setup` re-run
  (GS3-2 — changes the discovery tree; gated)
- Credentials: variable names only, never printed
