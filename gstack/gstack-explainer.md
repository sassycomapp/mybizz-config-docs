# GStack Explainer

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
- **Platform-specific loops.** Live-device iOS QA through a real iPhone.
- **Documentation.** Diataxis-structured doc generation and post-ship doc
  syncing.
- **Second opinions.** Cross-model review through Codex and Claude wrappers.
- **GBrain upkeep.** Per-repo brain sync and setup skills (with known
  caveats — see suitability).

Roughly a third of the work is done by 74 standalone binaries under the
clone's `bin/` — deterministic scripts the skills call, not chat.

## 3. Suitability

- **Best for:** the full plan → review → ship loop on real code repos;
  enforcing review gates before anything lands; browser-based QA of web
  apps; post-ship verification (canary, benchmarks); retrospectives and
  learnings that compound across sessions.
- **Good for:** planning work in `-project-library` docs repos (the
  docs-plan workflow); security audits on any repo; PDF and diagram
  generation; keeping GBrain synced per repo.
- **Not good for:** trivial one-line tasks — the ceremony costs more than
  it catches; iOS work without a connected iPhone; `/land-and-deploy`
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
it. The bare-named and `gstack-` prefixed discovery links are two
generations of the same installer pointing at the same files; the
frontmatter `name:` field, not either folder naming, decides the command —
which is why both link generations can coexist without ambiguity.

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
reason this suite pins to installed behavior. Whether to clean up the three
broken discovery symlinks (inert; cosmetic only). Whether to configure a
brain-sync remote (artifact sync is currently local-only). Which setup
version produced the July bare-name links (provenance only, no rule
depends on it).

*Companion documents: `gstack-config.md` (state), `gstack-reference.md`
(workflows and commands), `gstack-skills-reference.md` (catalog).
Cross-component reasoning: `mybizz-os-docs/memory-master-explainer.md`.*
