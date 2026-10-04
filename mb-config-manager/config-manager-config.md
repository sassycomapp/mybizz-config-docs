---
title: "config-manager-config"
doc-id: "mb-48323f1a"
updated: "2026-10-04"
---
# Config Manager — Configuration

Canonical current-state configuration for the config-management system itself.
Concept: [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md); procedures: [[[mybizz-config-docs:mb-config-manager/config-manager-reference|Reference: Commands, Procedures]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-reference.md).

## Identity

| Item | Value |
|---|---|
| System | `mb-config-manager` — configuration management for live systems |
| Orchestrator | an **agent**, not a skill — draft: [[[mybizz-config-docs:mb-config-manager/config-manager-agent\|Orchestrator Agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md) |
| Exam modules | per-system skills — draft: `{system}/{system}-skill.md` |
| Routing table | [[[mybizz-config-docs:mb-config-manager/config-manager-register\|Register: Managed Systems]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-register.md) — authoritative for Enabled systems |
| Separation | config skills examine live systems and edit no document outside the config-management suites and the routing table; other documents are maintained by the agents doing the work, with the developer's approval, and checked at every commit by `mb-doc-check` |

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
| Learnings convention | `{system}-learnings.md` per system; orchestrator's own: [[[mybizz-config-docs:mb-config-manager/config-manager-learnings\|Learnings]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-learnings.md). Transient — every entry eventually dropped or graduated into a permanent home |
| Graduation | Dual track: into the skill → agent-applied, then re-installed; into config/reference/explainer → proposed at the gate, applied only after developer approval |
| Tier 3 (deep/intrusive) | Explicit developer unlock per run; plan header carries the unlock state |
| Credentials | Referenced by variable name only — never printed |

## Install locations

| Component | Source (this repo) | Installed location |
|---|---|---|
| Orchestrator agent | [[[mybizz-config-docs:mb-config-manager/config-manager-agent\|Orchestrator Agent]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-agent.md) | resolved at agent install time (developer-set) |
| System exam skills | `{system}/{system}-skill.md` — canonical, git-versioned | `~/.config/opencode/skills/<skill-name>/SKILL.md` — installed **copy** (only executing copy) |

Install copies the source's text below its frontmatter into the installed
`SKILL.md`, never moves it; the suite folder keeps the canonical source as backup
and step-0 drift anchor. The two files differ only in frontmatter, by design: the
source carries `title`, `doc-id` and `updated`, like every document; the installed
copy carries `name` and `description`, which the agent writes at first install and
keeps unchanged on every re-install. The register records each Installed skill's
install date and the first 16 hex of the sha256 of the text below the frontmatter,
which is identical for source and installed copy when they are in sync. Every file
in every suite, including the agent and the skill sources, is a document and is
checked by `mb-doc-check` at every commit.

## Verification

Every system in the [[[mybizz-config-docs:mb-config-manager/config-manager-register|Register: Managed Systems]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-register.md) with state `Installed` has completed a formal plan-driven exam run; each system's exam report holds its verified state.
