---
document: "Config Manager — Configuration"
doc-id: config-manager-config
state: Live
date-created: 2026-09-12
---

# Config Manager — Configuration

Canonical current-state configuration for the config-management system itself.
Concept: [[config-manager-explainer|Explainer]]; procedures: [[config-manager-reference|Reference: Commands, Procedures]].

## Identity

| Item | Value |
|---|---|
| System | `mb-config-manager` — configuration management for live systems |
| Orchestrator | an **agent**, not a skill — draft: [[config-manager-agent|Orchestrator Agent]] |
| Exam modules | per-system skills — draft: `{system}/{system}-skill.md` |
| Routing table | [[config-manager-register|Register: Managed Systems]] — authoritative for Enabled systems |
| Separation | config skills never touch docs registers; docs skills never probe live systems |

## Settings

| Setting | Value |
|---|---|
| Trigger | On demand only — developer-initiated |
| Detection autonomy | Full — a run asks no questions until the gate |
| Healing | Gated per item; nothing auto-approved, ever |
| Verdict classes | `DOWN` / `UNHEALTHY` / `DRIFT` / `GAP` |
| Exam cycle | Plan-driven — exam-plan synthesized fresh per run, skill executed with plan in hand |
| Report convention | `{system}-exam-report.md` per system folder — one file, overwritten each run, no history |
| Exam-plan convention | `{system}-exam-plan.md` per system — transient, rewritten at the start of each cycle |
| Log convention | `{system}-log.md` per system — one run row per exam + free rows for notable events (crashes, incidents, upgrades, errors, significant guard denials); appended at observation time; pruned once absorbed |
| Learnings convention | `{system}-learnings.md` per system; orchestrator's own: [[config-manager-learnings|Learnings]]. Transient — every entry eventually dropped or graduated into a permanent home |
| Graduation | Dual track: into the skill → agent-applied; into config/reference/explainer → flagged through docs governance |
| Tier 3 (deep/intrusive) | Explicit developer unlock per run; plan header carries the unlock state |
| Credentials | Referenced by variable name only — never printed |

## Install locations

| Component | Source (this repo) | Installed location |
|---|---|---|
| Orchestrator agent | [[config-manager-agent|Orchestrator Agent]] | resolved at agent install time (developer-set) |
| System exam skills | `{system}/{system}-skill.md` — canonical, git-versioned | `~/.config/opencode/skills/<skill-name>/SKILL.md` — installed **copy** (only executing copy) |

The skill file is **copied** at install, never moved — the suite folder keeps the
canonical source as backup and step-0 drift anchor. The register records each
Installed skill's sha256 (first 16 hex) and install date. Source files (agent +
skill files) are exempt from docs-management governance; everything else in every
suite is subject to it.

## Verification

Verified live through formal plan-driven exam runs: `mb-config-postgresql` (pilot), `mb-config-cupcake`, `mb-config-gbrain`, `mb-config-memory-governor`, and `mb-config-gbrain-dream-cycle` (2026-09-14 — including a developer-unlocked full DC3-1 dream cycle, all green). Each Installed and verified (see each system's exam report). The plan-driven cycle is proven across five systems; emulation continues across the WIP queue per the register.
