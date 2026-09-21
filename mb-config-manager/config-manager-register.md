---
document: "mb-config-manager — Register: Managed Systems"
doc-id: config-manager-register
state: Live
date-created: 2026-09-12
---

# mb-config-manager — Register: Managed Systems

The routing table. One row per system the config-manager manages. A row is added when
the system first becomes examinable (a config doc exists); `state` updates in place.
**A register is the current state, not a log** — no historical information is kept
here; superseded states simply change.

**States:** `Installed` (installed at the runtime location — the authoritative
runnable state) · `WIP` (emulation in progress — suite being built to the
7-file standard) · `Deferred` (registered, deliberately postponed — developer
decision) · `Registered` (examinable, module pending) · `Placeholder`
(folder reserved, no config doc yet) · `Retired` (no longer managed).

**Emulation queue (developer-set order, 2026-09-13):** gbrain-dream-cycle →
graphify → gstack → opencode → anvil-agent-references → matt-pocock-skills →
magdoub-wireframe. Completed pilots: postgresql, cupcake, gbrain.

| system | exam skill | spec doc | state | sha256 (source) | install date | notes |
|---|---|---|---|---|---|---|
| postgresql | mb-config-postgresql | postgresql/postgresql-config.md | Installed | b41a3e117dee1809 | 2026-09-12 | pilot — verified live 2026-09-12; source [[postgresql-skill|Postgresql Skill]]; installed `~/.config/opencode/skills/mb-config-postgresql/SKILL.md` |
| cupcake | mb-config-cupcake | cupcake/cupcake-config.md | Installed | f5e8489cf60a8abc | 2026-09-12 | verified live 2026-09-12; source [[cupcake-skill|Cupcake Skill]] (backfill developer-run 2026-09-12, hash-verified); installed `~/.config/opencode/skills/mb-config-cupcake/SKILL.md` (developer-run install) |
| gbrain | mb-config-gbrain | gbrain/gbrain-config.md | Installed | 58dc0b52cbc86d72 | 2026-09-12 | verified live 2026-09-12; source [[gbrain-skill|Gbrain Skill]]; installed `~/.config/opencode/skills/mb-config-gbrain/SKILL.md` |
| gstack | mb-config-gstack | gstack/gstack-config.md | Installed | 6a3afc08a93cee02 | 2026-09-16 | run #1 formal 2026-09-16: HEALTHY (Tiers 0–2 all PASS, zero live defects; Tier 3 GS3-1 executed developer-unlocked, GS3-2 policy stay-on-`1.58.1.0`); N-1 flagged to docs governance (spec wording nit); N-3 resolved by developer correction — GStack is NOT a memory-system component, related to the ecosystem only via GBrain (spec row corrected in-suite); output-location fact recorded 2026-09-16 (sole live location `~/.gstack/projects/$SLUG/`; `gstack-outputs/` copy lane = convention only, does not exist on this system — developer-confirmed); LE-1/LE-2/LE-3 filed (bin-tree mixed-interpreter; preamble host-path; output-location fact); skill re-installed twice after corrections (re-hash `6a3afc08a93cee02`); verified live 2026-09-16; source [[gstack-skill|Gstack Skill]]; installed `~/.config/opencode/skills/mb-config-gstack/SKILL.md` (copy-install, grant via mg-grant) |
| opencode | mb-config-opencode | opencode/opencode-config.md | Installed | 268bb702a038448b | 2026-09-15 | run #1 formal 2026-09-15: HEALTHY (all checks PASS, zero live defects); config-content field bundle closed developer-verified (all PASS); F-4/F-5 spec omissions approved at gate and applied to spec + permission-model doc; plugin load-once + single discoverable path + Active Project Standard verified live; Tier 3 locked, stay-on-1.15.12 (no check failed); learnings graduated into skill (config-content = runner D; token-in-argument guard class), re-installed (re-hash `268bb702a038448b`); verified live 2026-09-15; source [[opencode-skill|Opencode Skill]]; installed `~/.config/opencode/skills/mb-config-opencode/SKILL.md` |
| memory-governor | mb-config-memory-governor | memory-governor/memory-governor-config.md | Installed | c40df342d523aa59 | 2026-09-13 | run #1 formal: HEALTHY+FLAGS; verified live 2026-09-13; source [[memory-governor-skill|Memory Governor Skill]]; installed `~/.config/opencode/skills/mb-config-memory-governor/SKILL.md` |
| archify | mb-config-archify | archify/archify-config.md | Installed | 165897270158a38e | 2026-09-16 | run #1 formal 2026-09-16: HEALTHY (Tiers 0–3 all executed, zero open findings at close); scoping skill `mb-archify-scope` retained and documented as a permanent suite component (config §Scoping skill component); F-1 scope-skill re-sync applied at gate (installed copy had drifted — missing Phase 9; re-copy + hash pair `0e40e984ba82a5f6` verified); F-2 config Cupcake-status row refreshed (Cupcake ACTIVE per cupcake-config 2026-09-12, no archify rule re-confirmed); Tier 3 executed — AR3-1 mechanical audit PASS, AR3-2 functional-ability acceptance PASS (showcase validate 9/9, 0 errors, 0 warnings), AR3-3 open items recorded (W-1/W-2 retained — Windows-side readability unprovable from WSL; W-3 out of scope), AR3-4 adoption review benign all axes, AR3-5 policy re-confirmed; run-learnings facts graduated into explainer/reference (type-choice leverage, probe-before-connect, viewBox constraint, exact-port anchoring, corridor separation, visual-review-by-human); verified live 2026-09-16; source [[archify-skill|Archify Skill]]; installed `~/.config/opencode/skills/mb-config-archify/SKILL.md` (copy-install, hash pair `165897270158a38e` verified) |
| graphify | mb-config-graphify | graphify/graphify-config.md | Installed | 1ca73897a2023741 | 2026-09-14 | run #1 formal, all tiers 0–3 in full: HEALTHY, every check PASS, zero open findings; Tier 3 realistic run = full documented rebuild (537/434/155, provenance == HEAD `59175d9e`) + GF3-2 stay-on-0.9.40; F-4 tool defect found+fixed in-run (extract stamps built_at_commit from cwd repo — rebuilds run from target root); run learnings graduated into skill+reference, skill re-installed (re-hash `1ca73897a2023741`); spec re-baselined 2026-09-14 (upstream 0.9.61); verified live 2026-09-14; source [[graphify-skill|Graphify Skill]]; installed `~/.config/opencode/skills/mb-config-graphify/SKILL.md` (copy-install; hash pair verified) |
| magdoub-wireframe | mb-config-magdoub-wireframe | magdoub-wireframe/magdoub-wireframe-config.md | Installed | c570e38d0b490808 | 2026-09-16 | run #1 formal 2026-09-16: HEALTHY (Tiers 0–2 all PASS, zero live defects, zero open findings); Tier 3 executed developer-unlocked — MW3-1 full audit PASS (byte counts + sha256 all exact, tree clean, local==origin), MW3-2 W-3 supply-chain review performed+recorded (open item 3 closed, spec applied with gate approval), W-5 retained, W-1 deferred to deliberate session, MW3-3 update discipline re-confirmed; W-4 (design-rules ADR reconciliation) **closed 2026-09-16 by direct developer decision** — [[adr-design-rules|Wireframe Design Rules]] gained §A Magdoub-skill exemption (ADR binds only wireframes not created by the Magdoub skill; not an escape hatch — A3), suite reconciled, skill source re-edited (scope-boundary + open-item wording) and re-installed (re-hash `c570e38d0b490808`); verified live 2026-09-16; source [[magdoub-wireframe-skill|Magdoub Wireframe Skill]]; installed `~/.config/opencode/skills/mb-config-magdoub-wireframe/SKILL.md` (copy-install, grant via mg-grant, hash pair verified); open items 1/2/5 carry with dispositions |
| matt-pocock-skills | mb-config-matt-pocock-skills | matt-pocock-skills/matt-pocock-skills-config.md | Installed | 86c78969ad0e8a80 | 2026-09-16 | run #1 formal 2026-09-16: HEALTHY (Tiers 0–2 all PASS, zero live defects); Tier 3 executed (MP3-1 full audit PASS — 0/35 byte mismatches; MP3-2 stay-pinned `84fdeff`; MP3-3 Zone.Identifier keep); one step-0 guard denial recorded class, honored; zero open findings; source [[matt-pocock-skills-skill|Matt Pocock Skills Skill]]; installed `~/.config/opencode/skills/mb-config-matt-pocock-skills/SKILL.md` (copy-install, grant via mg-grant); verified live 2026-09-16 |
| gbrain-dream-cycle | mb-config-gbrain-dream-cycle | gbrain-dream-cycle/gbrain-dream-cycle-config.md | Installed | a4872e9d61f1c32f | 2026-09-14 | run #1 formal + DC3-1 full cycle: HEALTHY, all PASS end-to-end (detection + functional probes + live deepening pass); verified live 2026-09-14; F-1 hardening graduated (re-hash a4872e9d61f1c32f); F-2 export lane approved (C:\backup-dream-cycle); DC3-2 policy: stay 0.46.1.0 (no check failed) |
| anvil-agent-references | mb-config-anvil-agent-references | anvil-agent-references/anvil-agent-references-config.md | Installed | a66e0140a39a37e5 | 2026-09-16 | run #1 formal 2026-09-16: HEALTHY (Tiers 0–3 all PASS, zero live defects); Tier 3 executed (AR3-1 full audit PASS — 5/5 links + 5/5 SKILL.md byte-identity, structure conforms; AR3-2 stay-current-with-upstream, license no action; AR3-3 per-project setup remains developer-run pending, open item 3); **all five open items closed 2026-09-16** (direct spec corrections — HEAD `7c9b0a7`, stubs 63, refreshed inventory; adoption review recorded, license axis documented accepted risk; per-project setup = deliberate trigger-bound deferral per cupcake project-init status; Tier-2/3 verification record = confirmed skill verification; index-state corrected); two guard denials recorded class, honored; learnings graduated (content already in born-with skill); verified live 2026-09-16; source [[anvil-agent-skill|Anvil Agent Skill]]; installed `~/.config/opencode/skills/mb-config-anvil-agent-references/SKILL.md` (copy-install, hash pair `a66e0140a39a37e5` verified 2026-09-16 — re-synced by developer after source edited in `4aff290`) |
| i-have-adhd | mb-config-i-have-adhd | i-have-adhd/i-have-adhd-config.md | Installed | 1669db5ef2192a0d | 2026-09-20 | copy-install 2026-09-20 (developer authorized proceed-without-grant — Cupcake disabled); source [[i-have-adhd-skill|I Have Adhd Skill]]; installed `~/.config/opencode/skills/mb-config-i-have-adhd/SKILL.md`; born-with-inventory; run #1 formal 2026-09-20: HEALTHY — F-1 DRIFT (installer dual-write, registry primary `~/.agents/skills/` + CLI-derived OpenCode copy, dedup verified) resolved by gate-approved re-baseline + dual-path byte-identity check in skill (re-install, re-hash `1669db5ef2192a0d`); Tier 3 unlocked all PASS (IA3-1 upstream verified live 48.7k stars, HEAD pin `839872f9d1cd…`, bundle byte-identical to upstream main; IA3-2 update mechanism verified byte-idempotent; IA3-3 supply-chain review recorded benign — Gen Safe/Socket 0/Snyk Low); spec open items 1–5 closed, item 6 standing watch; verified live 2026-09-20 |
| mb-align-docs | mb-config-mb-align-docs | mb-align-docs/align-docs-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-compile-rules | mb-config-mb-compile-rules | mb-compile-rules/mb-compile-rules-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-docs-manager | mb-config-mb-docs-manager | mb-docs-manager/docs-manager-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-sentinel-review | mb-config-mb-sentinel-review | mb-sentinel-review/sentinel-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-submit-memory | mb-config-mb-submit-memory | mb-submit-memory/mb-submit-memory-config.md | Installed | 88a71641d03f1997 | 2026-09-15 | run #1 formal 2026-09-15: HEALTHY (Tiers 0–2 all PASS, zero live defects); Tier 3 executed (SM3-1 credential accepted/queue empty — evidenced owning_project ↔ gbrain sources all match; SM3-3 stray file verified absent; SM3-2 auto-start executed+verified, systemd units active, session 005); F-A/F-B/F-C spec corrections applied at gate; learnings graduated, re-hash `88a71641d03f1997`; verified live 2026-09-15; zero open items; source [[submit-memory-skill|Submit Memory Skill]]; installed `~/.config/opencode/skills/mb-config-mb-submit-memory/SKILL.md` |
| mb-sysdoc-creator | mb-config-mb-sysdoc-creator | mb-sysdoc-creator/sysdoc-creator-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-wikilinks | mb-config-mb-wikilinks | mb-wikilinks/wikilinks-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| cloudflare | — | — | Placeholder | no config doc yet |
| namecheap | — | — | Placeholder | no config doc yet |

Notes:

- **The config-manager does not list itself in this register** — a system that
  exams itself with its own machinery is circular redundancy; its health is
  maintained per [[config-manager-explainer|Explainer]] §9 (docs governance + step-0
  self-validation).
- **Install discipline:** install = **copy, never move** — the suite folder keeps
  the canonical source (`{system}-skill.md`, versioned in this repo); the
  installed copy at `~/.config/opencode/skills/<name>/SKILL.md` is the only
  *executing* copy (the suite folder is not skill-scanned — no double-load).
  The sha256 column records the source's first 16 hex chars; step-0 verification
  compares source ↔ installed every cycle (hash check via the approved glob form
  `mb-config-*/SKILL.md`, never token-literal commands). Divergence = finding:
  installed-edited → DRIFT; source-edited-not-reinstalled → stale GAP.
- `spec doc` is the single file the exam runs against; the exam also verifies the
  suite's other documents as part of the GAP class.
- Filename conventions differ per suite (e.g. [[align-docs-config|Config]],
  [[docs-manager-config|Config]]) — the spec doc column is authoritative, never guessed.
- `mb-*` skills are themselves examinable systems: an installed skill can drift from
  its suite docs exactly like any tool.
- Every Installed system's folder carries the seven-file suite (config,
  exam-plan, exam-report, log, learnings, explainer, reference) per
  [[config-manager-explainer|Explainer]]; suites built before that standard keep their
  existing files until their architecture emulation pass.
- Registration discipline: rows are added on demonstrated need, through the gate —
  not speculatively.
