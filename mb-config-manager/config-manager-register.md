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
| postgresql | mb-config-postgresql | postgresql/postgresql-config.md | Installed | b41a3e117dee1809 | 2026-09-12 | pilot — verified live 2026-09-12; source `postgresql/postgresql-skill.md`; installed `~/.config/opencode/skills/mb-config-postgresql/SKILL.md` |
| cupcake | mb-config-cupcake | cupcake/cupcake-config.md | Installed | f5e8489cf60a8abc | 2026-09-12 | verified live 2026-09-12; source `cupcake/cupcake-skill.md` (backfill developer-run 2026-09-12, hash-verified); installed `~/.config/opencode/skills/mb-config-cupcake/SKILL.md` (developer-run install) |
| gbrain | mb-config-gbrain | gbrain/gbrain-config.md | Installed | 58dc0b52cbc86d72 | 2026-09-12 | verified live 2026-09-12; source `gbrain/gbrain-skill.md`; installed `~/.config/opencode/skills/mb-config-gbrain/SKILL.md` |
| gstack | mb-config-gstack | gstack/gstack-config.md | Installed | 6a3afc08a93cee02 | 2026-09-16 | run #1 formal 2026-09-16: HEALTHY (Tiers 0–2 all PASS, zero live defects; Tier 3 GS3-1 executed developer-unlocked, GS3-2 policy stay-on-`1.58.1.0`); N-1 flagged to docs governance (spec wording nit); N-3 resolved by developer correction — GStack is NOT a memory-system component, related to the ecosystem only via GBrain (spec row corrected in-suite); output-location fact recorded 2026-09-16 (sole live location `~/.gstack/projects/$SLUG/`; `gstack-outputs/` copy lane = convention only, does not exist on this system — developer-confirmed); LE-1/LE-2/LE-3 filed (bin-tree mixed-interpreter; preamble host-path; output-location fact); skill re-installed twice after corrections (re-hash `6a3afc08a93cee02`); verified live 2026-09-16; source `gstack/gstack-skill.md`; installed `~/.config/opencode/skills/mb-config-gstack/SKILL.md` (copy-install, grant via mg-grant) |
| opencode | mb-config-opencode | opencode/opencode-config.md | Installed | 268bb702a038448b | 2026-09-15 | run #1 formal 2026-09-15: HEALTHY (all checks PASS, zero live defects); config-content field bundle closed developer-verified (all PASS); F-4/F-5 spec omissions approved at gate and applied to spec + permission-model doc; plugin load-once + single discoverable path + Active Project Standard verified live; Tier 3 locked, stay-on-1.15.12 (no check failed); learnings graduated into skill (config-content = runner D; token-in-argument guard class), re-installed (re-hash `268bb702a038448b`); verified live 2026-09-15; source `opencode/opencode-skill.md`; installed `~/.config/opencode/skills/mb-config-opencode/SKILL.md` |
| memory-governor | mb-config-memory-governor | memory-governor/memory-governor-config.md | Installed | c40df342d523aa59 | 2026-09-13 | run #1 formal: HEALTHY+FLAGS; verified live 2026-09-13; source `memory-governor/memory-governor-skill.md`; installed `~/.config/opencode/skills/mb-config-memory-governor/SKILL.md` |
| archify | mb-config-archify | archify/archify-config.md | Registered | module pending |
| graphify | mb-config-graphify | graphify/graphify-config.md | Installed | 1ca73897a2023741 | 2026-09-14 | run #1 formal, all tiers 0–3 in full: HEALTHY, every check PASS, zero open findings; Tier 3 realistic run = full documented rebuild (537/434/155, provenance == HEAD `59175d9e`) + GF3-2 stay-on-0.9.40; F-4 tool defect found+fixed in-run (extract stamps built_at_commit from cwd repo — rebuilds run from target root); run learnings graduated into skill+reference, skill re-installed (re-hash `1ca73897a2023741`); spec re-baselined 2026-09-14 (upstream 0.9.61); verified live 2026-09-14; source `graphify/graphify-skill.md`; installed `~/.config/opencode/skills/mb-config-graphify/SKILL.md` (copy-install; hash pair verified) |
| magdoub-wireframe | mb-config-magdoub-wireframe | magdoub-wireframe/magdoub-wireframe-config.md | WIP | emulation queued |
| matt-pocock-skills | mb-config-matt-pocock-skills | matt-pocock-skills/matt-pocock-skills-config.md | Installed | 86c78969ad0e8a80 | 2026-09-16 | run #1 formal 2026-09-16: HEALTHY (Tiers 0–2 all PASS, zero live defects); Tier 3 executed (MP3-1 full audit PASS — 0/35 byte mismatches; MP3-2 stay-pinned `84fdeff`; MP3-3 Zone.Identifier keep); one step-0 guard denial recorded class, honored; zero open findings; source `matt-pocock-skills/matt-pocock-skills-skill.md`; installed `~/.config/opencode/skills/mb-config-matt-pocock-skills/SKILL.md` (copy-install, grant via mg-grant); verified live 2026-09-16 |
| gbrain-dream-cycle | mb-config-gbrain-dream-cycle | gbrain-dream-cycle/gbrain-dream-cycle-config.md | Installed | a4872e9d61f1c32f | 2026-09-14 | run #1 formal + DC3-1 full cycle: HEALTHY, all PASS end-to-end (detection + functional probes + live deepening pass); verified live 2026-09-14; F-1 hardening graduated (re-hash a4872e9d61f1c32f); F-2 export lane approved (C:\backup-dream-cycle); DC3-2 policy: stay 0.46.1.0 (no check failed) |
| anvil-agent-references | mb-config-anvil-agent-references | anvil-agent-references/anvil-agent-references-config.md | WIP | emulation queued |
| mb-align-docs | mb-config-mb-align-docs | mb-align-docs/align-docs-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-compile-rules | mb-config-mb-compile-rules | mb-compile-rules/mb-compile-rules-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-docs-manager | mb-config-mb-docs-manager | mb-docs-manager/docs-manager-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-sentinel-review | mb-config-mb-sentinel-review | mb-sentinel-review/sentinel-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-submit-memory | mb-config-mb-submit-memory | mb-submit-memory/mb-submit-memory-config.md | Installed | 88a71641d03f1997 | 2026-09-15 | run #1 formal 2026-09-15: HEALTHY (Tiers 0–2 all PASS, zero live defects); Tier 3 executed (SM3-1 credential accepted/queue empty — evidenced owning_project ↔ gbrain sources all match; SM3-3 stray file verified absent; SM3-2 auto-start executed+verified, systemd units active, session 005); F-A/F-B/F-C spec corrections applied at gate; learnings graduated, re-hash `88a71641d03f1997`; verified live 2026-09-15; zero open items; source `mb-submit-memory/submit-memory-skill.md`; installed `~/.config/opencode/skills/mb-config-mb-submit-memory/SKILL.md` |
| mb-sysdoc-creator | mb-config-mb-sysdoc-creator | mb-sysdoc-creator/sysdoc-creator-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| mb-wikilinks | mb-config-mb-wikilinks | mb-wikilinks/wikilinks-config.md | Deferred | deliberately postponed (developer decision 2026-09-13) |
| cloudflare | — | — | Placeholder | no config doc yet |
| namecheap | — | — | Placeholder | no config doc yet |

Notes:

- **The config-manager does not list itself in this register** — a system that
  exams itself with its own machinery is circular redundancy; its health is
  maintained per `config-manager-explainer.md` §9 (docs governance + step-0
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
- Filename conventions differ per suite (e.g. `align-docs-config.md`,
  `docs-manager-config.md`) — the spec doc column is authoritative, never guessed.
- `mb-*` skills are themselves examinable systems: an installed skill can drift from
  its suite docs exactly like any tool.
- Every Installed system's folder carries the seven-file suite (config,
  exam-plan, exam-report, log, learnings, explainer, reference) per
  `config-manager-explainer.md`; suites built before that standard keep their
  existing files until their architecture emulation pass.
- Registration discipline: rows are added on demonstrated need, through the gate —
  not speculatively.