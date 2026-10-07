---
title: "gstack-explainer"
doc-id: "mb-b80e9856"
updated: "2026-10-07"
---
# GStack Explainer

## 0. Config-management coverage

This suite is part of the config-management system (`mb-config-manager`): the
spec is [[[mybizz-config-docs:gstack/gstack-config|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md), the exam procedure is [[[mybizz-config-docs:gstack/gstack-skill|Gstack Skill]]](C:/mybizz/mybizz-config-docs/gstack/gstack-skill.md), and the
per-run job-spec is [[[mybizz-config-docs:gstack/gstack-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gstack/gstack-exam-plan.md) / [[[mybizz-config-docs:gstack/gstack-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gstack/gstack-exam-report.md) /
[[[mybizz-config-docs:gstack/gstack-log|Log]]](C:/mybizz/mybizz-config-docs/gstack/gstack-log.md) / [[[mybizz-config-docs:gstack/gstack-learnings|GStack Learnings]]](C:/mybizz/mybizz-config-docs/gstack/gstack-learnings.md). See §7 (Config maintenance) below.

## 1. What this actually is

GStack is a virtual engineering team implemented as markdown slash commands.
Each skill is a specialist with a job description — a CEO who challenges
scope before code exists, an eng manager who locks architecture, a designer
who catches AI slop, a reviewer who finds the bugs that pass CI, a QA lead
who opens a real browser, a security officer running OWASP and STRIDE, a
release engineer who ships the PR. The problem it solves is the one every
solo builder with an AI agent hits: a blank prompt produces plausible work,
but not *managed* work. GStack replaces the blank prompt with a process —
Think → Plan → Build → Review → Test → Ship → Reflect — where each skill
consumes the previous skill's output, so nothing falls through the cracks.

In this environment it is installed as one pinned clone (`1.58.1.0`) whose
files OpenCode reaches through symlinks, working alongside GBrain — the
division of labor is one line: **GBrain is memory (it stores and searches
decisions and rationale); GStack is workflow (it drives what gets done and
in what order).** Neither replaces reading the actual code.

## 2. What it can do (capability level)

- **Structured ideation and planning.** An interrogation skill that
  reframes product ideas against real pain; four independent plan reviews
  (CEO, design, developer-experience, engineering) that each amend the plan
  from a different professional angle; a pipeline that runs them
  automatically with the engineering review deliberately last.
- **Spec-to-issue authoring.** Vague intent becomes a precise, filed spec
  with scope boundaries.
- **Code review with teeth.** Finds production-bound bugs CI misses,
  auto-fixes the obvious ones, flags over-engineering without blocking.
- **Systematic debugging.** Root-cause-first investigation with an iron law:
  no fixes without a diagnosed cause.
- **Real-browser QA.** A bundled headless Chromium drives actual pages,
  clicks flows, screenshots evidence, fixes what it finds with atomic
  commits, and generates regression tests.
- **Design system work.** From consultation through variant exploration to
  production HTML and visual QA.
- **Security auditing.** Zero-noise OWASP + STRIDE passes in daily and
  monthly intensities.
- **Release engineering.** Test-gated shipping, version-slot management,
  merge-and-verify deployment, post-deploy canary monitoring, performance
  baselines.
- **Compounding memory.** Retrospectives with per-person breakdowns, and a
  learnings store that gets smarter about your codebase across sessions;
  session context save/restore.
- **Safety modes.** Destructive-command warnings, edit scoping, combined
  guard mode.
- **Documentation.** Diataxis-structured doc generation and post-ship doc
  syncing.
- **GBrain upkeep.** Per-repo brain sync and setup skills. Not used in this environment: GBrain is synced by commit all.

Roughly a third of the work is done by 74 standalone binaries under the
clone's `bin/` — deterministic scripts the skills call, not chat.

## 3. Suitability

- **Best for:** the full plan → review → ship loop on real code repos;
  enforcing review gates before anything lands; browser-based QA of web
  apps; post-ship verification (canary, benchmarks); retrospectives and
  learnings that compound across sessions.
- **Good for:** planning work in `-project-library` docs repos (the
  docs-plan workflow); security audits on any repo; PDF and diagram
  generation.
- **Not good for:** trivial one-line tasks — the ceremony costs more than
  it catches; `/land-and-deploy`
  before `/setup-deploy` has been configured; trusting `/setup-gbrain`'s
  own description of GBrain's backend (it describes PGLite/Supabase — this
  environment runs self-hosted PostgreSQL); replacing the authority model —
  no skill output outranks the current files, the user, or OpenCode rules.

## 4. Why it works the way it does

**Why skills are generated markdown, hand-edit forbidden.** Every SKILL.md
is rendered from one template (`SKILL.md.tmpl`), so behavioral rules exist
in exactly one place and every host tree stays in sync. Editing a rendered
file would be silently overwritten on the next generation — the doc rule
("regenerate, never edit") protects the editor, not the tool.

**Why the install is a symlink web instead of copies.** One real clone,
one real per-host skill tree, and discovery links pointing into it — so an
upgrade touches one place, and `GSTACK_BIN`-style paths stay stable across
it. OpenCode loads a skill only when the skill's frontmatter `name:` field
matches the folder that contains it, so each discovery shortcut carries
exactly the skill's declared name — the plain names plus `gstack-upgrade`,
the one skill whose frontmatter declares the prefixed name. `skill_prefix`
is false, and gstack's setup, upgrade and relink tools read that setting,
creating plain shortcuts only.

**Why the authority model is ordered that way.** A workflow layer's
greatest risk is quietly outranking reality: a skill's convention is
helpful exactly until it contradicts the user, the repo's own rules, or
OpenCode's configuration. The ordering makes workflow conventions
defeasible by everything that actually governs the machine, and demotes
GBrain's memory to advisory — memory informs, it never overrides.

**Why three workflow families.** The plan/build/handover split mirrors the
agent-role separation in this environment (plan reasons, build writes,
sessions end) — each family names its default agent and its exit condition,
so a workflow choice is an ownership decision, not a preference.

**Why the browser is bundled.** QA needs deterministic, repeatable page
driving without polluting or depending on a human's real logged-in browser.
The bundled Chromium provides that offline and reproducibly. Upstream's
move to an Aside-first model (driving the user's real browser) trades that
isolation for real-session fidelity — a genuine tradeoff, which is exactly
why the upgrade is an open decision here rather than a default.

**Why `/sync-gbrain` has a source-overlap trap.** The orchestrator derives
source IDs deterministically from repo path and cannot detect that a human
already registered the same path under a different ID — GBrain refuses the
overlap, and the skill stage errors rather than silently adopting the
existing source. The refusal is correct behavior; the bypass
(`gbrain dream --source <id>`) is the honest path.

**Open questions.** The `1.81.0.0` upgrade (Aside-first browser, team mode,
prune-on-setup) — a deliberate re-decision, not a routine bump, and the
reason this suite pins to installed behavior. Whether to configure a
brain-sync remote (artifact sync is currently local-only).

*Companion documents: [[[mybizz-config-docs:gstack/gstack-config|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md) (state), [[[mybizz-config-docs:gstack/gstack-reference|GStack Reference]]](C:/mybizz/mybizz-config-docs/gstack/gstack-reference.md)
(workflows and commands), [[[mybizz-config-docs:gstack/gstack-skills-reference|GStack Skills Reference]]](C:/mybizz/mybizz-config-docs/gstack/gstack-skills-reference.md) (catalog).
Cross-component reasoning: [[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md).*

## 7. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md) — emulated from the
PostgreSQL pilot and the gbrain-dream-cycle precedent. The short local version:

- [[[mybizz-config-docs:gstack/gstack-config|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md) is the **spec** — the ideal state every exam checks
  against. GStack is working well; the exam verifies that and changes nothing.
- Before each exam run, the config-manager synthesizes [[[mybizz-config-docs:gstack/gstack-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gstack/gstack-exam-plan.md):
  a fresh job-spec built from this spec, the last report, the log, and the
  learnings. The plan is transient (the file is live; contents rewritten each
  cycle).
- The exam runs the installed skill (`mb-config-gstack`) with the plan in hand —
  detection fully autonomous; healing gated. **This module has no standing
  agent-healable items**: GStack is working well, and every repair is
  developer-run or proposed through the gate.
- **Scope boundary:** GBrain server conformance belongs to `mb-config-gbrain`
  (this exam reads `~/.gstack/*.json` records only); the dream cycle belongs to
  `mb-config-gbrain-dream-cycle` (`/sync-gbrain` is a knowledge check only);
  OpenCode structure rows belong to `mb-config-opencode`; cross-tool skill
  enumeration belongs to [[[mybizz-os-docs:os-reference-docs/skills-catalog|Skills Catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md). This exam owns the
  discovery **mechanics** — that the documented clone, links, binaries, and
  config files resolve and are consistent.
- Several checks are permanently **developer-run**: `~/.gstack` credential-
  bearing content reads (sensitive-data guard — proven class), the `.env.example`
  content claim, and everything in Tier 3 (a real skill lifecycle is expensive
  and writes artifacts; the upgrade decision is the developer's).
- The run rewrites [[[mybizz-config-docs:gstack/gstack-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/gstack/gstack-exam-report.md) (current state, no history), appends
  one row to [[[mybizz-config-docs:gstack/gstack-log|Log]]](C:/mybizz/mybizz-config-docs/gstack/gstack-log.md), files new learnings, and prunes absorbed entries.

## 8. S.W.O.T.

**Strengths.** The installed-and-pinned model with every file links into one real
clone removes the multi-copy drift class entirely; each discovery shortcut
carries exactly the skill's declared frontmatter `name:` (OpenCode loads a
skill only on a name–folder match), so command resolution is unambiguous;
every known quirk — the stale update-check, the
source-overlap trap — is documented with its correct handling rather than left a
surprise.

**Weaknesses.** The environment sits 23 minor versions behind upstream
(`1.58.1.0` vs `1.81.0.0`), and the upgrade decision is a genuine re-design that
cannot be rushed; several checks are permanently developer-run (guard-denied file
content).

**Opportunities.** The config-management exam adds standing verification that
never existed: clone/version conformance, topology resolution (one shortcut
per installed skill, named by its declared name + aggregate + legacy path),
config-file conformance, a deterministic
bin invocation, and the generation-discipline probe — so the silent-failure class
(a symlink web that looks right but resolves dead) is caught before it compounds.

**Threats.** The symlink web can drift silently (a dead link, a double-load from a
manually-added path, an aggregate entry that stops resolving); an upstream change
minor-released into this pinned environment could quietly contradict the doc set;
a future setup run could re-generate the tree into a shape the doc no longer
describes (mitigated: GS0-GS2 topology checks every run).

---

*Companion documents: [[[mybizz-config-docs:gstack/gstack-config|GStack Configuration]]](C:/mybizz/mybizz-config-docs/gstack/gstack-config.md) (the spec),
[[[mybizz-config-docs:gstack/gstack-reference|GStack Reference]]](C:/mybizz/mybizz-config-docs/gstack/gstack-reference.md) (procedures and commands),
[[[mybizz-config-docs:gstack/gstack-skills-reference|GStack Skills Reference]]](C:/mybizz/mybizz-config-docs/gstack/gstack-skills-reference.md) (catalog), [[[mybizz-config-docs:gstack/gstack-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/gstack/gstack-exam-plan.md) /
`-exam-report.md` / `-log.md` / `-learnings.md` (config-management set),
[[[mybizz-config-docs:gstack/gstack-skill|Gstack Skill]]](C:/mybizz/mybizz-config-docs/gstack/gstack-skill.md) (exam skill canonical source). Architecture:
[[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md). Cross-component framing:
[[[mybizz-os-docs:os-reference-docs/memory-master-explainer|Master Explainer]]](C:/mybizz/mybizz-os-docs/os-reference-docs/memory-master-explainer.md).*
