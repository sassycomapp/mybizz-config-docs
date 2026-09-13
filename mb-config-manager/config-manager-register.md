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
runnable state) · `Registered` (examinable, module pending) · `Placeholder`
(folder reserved, no config doc yet) · `Retired` (no longer managed).

| system | exam skill | spec doc | state | sha256 (source) | install date | notes |
|---|---|---|---|---|---|---|
| postgresql | mb-config-postgresql | postgresql/postgresql-config.md | Installed | 9f61f34c9634b419 | 2026-09-12 | pilot — verified live 2026-09-12; source `postgresql/postgresql-skill.md`; installed `~/.config/opencode/skills/mb-config-postgresql/SKILL.md` |
| cupcake | mb-config-cupcake | cupcake/cupcake-config.md | Installed | f5e8489cf60a8abc | 2026-09-12 | verified live 2026-09-12; source `cupcake/cupcake-skill.md` (backfill developer-run 2026-09-12, hash-verified); installed `~/.config/opencode/skills/mb-config-cupcake/SKILL.md` (developer-run install) |
| gbrain | mb-config-gbrain | gbrain/gbrain-config.md | Installed | bb269e9944b03418 | 2026-09-12 | verified live 2026-09-12; source `gbrain/gbrain-skill.md`; installed `~/.config/opencode/skills/mb-config-gbrain/SKILL.md` |
| gstack | mb-config-gstack | gstack/gstack-config.md | Registered | module pending |
| opencode | mb-config-opencode | opencode/opencode-config.md | Registered | module pending |
| memory-governor | mb-config-memory-governor | memory-governor/memory-governor-config.md | Registered | module pending |
| archify | mb-config-archify | archify/archify-config.md | Registered | module pending |
| graphify | mb-config-graphify | graphify/graphify-config.md | Registered | module pending |
| magdoub-wireframe | mb-config-magdoub-wireframe | magdoub-wireframe/magdoub-wireframe-config.md | Registered | module pending |
| matt-pocock-skills | mb-config-matt-pocock-skills | matt-pocock-skills/matt-pocock-skills-config.md | Registered | module pending |
| gbrain-dream-cycle | mb-config-gbrain-dream-cycle | gbrain-dream-cycle/gbrain-dream-cycle-config.md | Registered | module pending |
| anvil-agent-references | mb-config-anvil-agent-references | anvil-agent-references/anvil-agent-references-config.md | Registered | module pending |
| mb-align-docs | mb-config-mb-align-docs | mb-align-docs/align-docs-config.md | Registered | module pending |
| mb-compile-rules | mb-config-mb-compile-rules | mb-compile-rules/mb-compile-rules-config.md | Registered | module pending |
| mb-docs-manager | mb-config-mb-docs-manager | mb-docs-manager/docs-manager-config.md | Registered | module pending |
| mb-sentinel-review | mb-config-mb-sentinel-review | mb-sentinel-review/sentinel-config.md | Registered | module pending |
| mb-submit-memory | mb-config-mb-submit-memory | mb-submit-memory/mb-submit-memory-config.md | Registered | module pending |
| mb-sysdoc-creator | mb-config-mb-sysdoc-creator | mb-sysdoc-creator/sysdoc-creator-config.md | Registered | module pending |
| mb-wikilinks | mb-config-mb-wikilinks | mb-wikilinks/wikilinks-config.md | Registered | module pending |
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