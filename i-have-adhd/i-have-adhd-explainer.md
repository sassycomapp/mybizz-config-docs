---
document: "i-have-adhd — Explainer"
doc-id: i-have-adhd-explainer
state: Live
date-created: 2026-09-19
---

# i-have-adhd — Explainer

*Companion note: for current confirmed state (paths, versions, integration,
open items) see [[i-have-adhd-config|Configuration]]. For invocation, operation, update,
and the do-not list, see [[i-have-adhd-reference|Reference: Invocation, Operation, Update]]. For the config-management
set: [[i-have-adhd-exam-plan|Exam Plan]] (transient job-spec — read second, every run),
[[i-have-adhd-exam-report|Exam Report]] (last verified state), [[i-have-adhd-log|Log]]
(chronological events), [[i-have-adhd-learnings|Learnings]] (transient knowledge), and
[[i-have-adhd-skill|I Have Adhd Skill]] (exam skill canonical source, installed as
`mb-config-i-have-adhd`). [[i-have-adhd-intro|I Have Adhd Intro]] is research provenance (not
state).*

---

## 1. What this actually is

The i-have-adhd skill is a third-party OpenCode skill — built by an
individual developer (Ayoub Ghriss, "ayghri"; verified live 2026-09-20),
installed through the `npx skills` CLI — that reshapes the agent's response
style for a reader with ADHD. Its entire runtime surface is prose: 142 lines
of instructions injected into the session prompt. No code executes, no CLI
runs, no background process exists, no project files are written. The
"installation" is a bundle mirrored in two places by the installer (the
`~/.agents/skills` universal registry primary and the CLI-derived OpenCode
copy), a global skills symlink, a slash-command file, and an empty marker
file; the "runtime" is prompt injection. That simplicity is the design, not a
limitation: it changes what responses look like, and nothing else.

It exists to fix a specific failure mode: models bury the actionable answer
under preamble, recap, and hedging. For a reader with ADHD — small working
memory, weak reward signal on buried wins, a high cost of re-reading — a
chatty response is not merely verbose, it is unusable: the action sits in
paragraph three, and by the time it is found the thread of what to do is
gone. The skill makes the action the first line.

Its role in this estate is cross-cutting. It is not a PDLF stage, it belongs
to no skill family, and it touches no pipeline — every session's output,
whatever the task, passes through it while active.

## 2. What it does (conceptual)

Ten rules in four groups:

- **Lead and land (rules 1, 3, 10).** The first line is something the reader
  can do now; the last line is the next step; nothing announces itself before
  the answer or apologises after it.
- **Structure (rules 2, 5).** Multi-step work becomes numbered bounded steps;
  state is restated every turn, so no reader has to hold "we are on step 3 of
  5" in their head between messages.
- **Focus and clarity (rules 4, 6, 7, 8).** Tangents are deferred to the end
  as separate questions; time is stated in concrete units; completed work is
  shown in concrete terms rather than buried in a recap; errors are stated
  cause-then-fix, without dramatic framing.
- **Economy (rule 9).** The visible working set is capped at five items per
  list, ranked by relevance — while completeness is retained internally. The
  cap shapes presentation only, never analysis or search.

Around the rules sit three governing mechanisms: a persistence clause (the
rules apply to every response for the rest of the session, across topic
changes, until the off phrase); six sanctioned overrides (explicit "explain"
requests, destructive-action confirmation, debug spirals, real ambiguity,
task-vs-rule conflicts, harness-vs-rule conflicts); and a five-item pre-send
check the agent runs on its own output before delivering it.

## 3. Suitability

**Best for:** implementation, debugging, and operations sessions — any
multi-step work whose output is commands, edits, and verification steps.

**Good for:** long multi-turn sessions generally, where per-turn state
restatement keeps the reader oriented; status-style outputs where the reader
must know what to do next.

**Not good for:** deep design or architecture exploration without switching —
the style suppresses exactly the exploratory, trade-off-rich output those
sessions need, and override 1 covers explicit "explain" requests only. It
does not change analysis depth, tool behavior, gates, or PDLF steps — those
belong to other mechanisms. And it cannot substitute for the structured plans
produced in plan mode, where the harness's own output contract outranks the
skill (SKILL.md break-rule 6).

## 4. Design reasoning

### Why action-first

The skill's own foundation section names the five facts that drive every
rule: working memory is small (anything not on screen is gone); knowing the
answer is not doing it (the friction between "got it" and "done it" is where
work dies); starting is the hardest step; vague time estimates all register
the same; and visible progress is the scarce reward. Each rule is one of
those facts applied to text: the action leads because starting is hardest;
state is restated because working memory drops it; estimates are concrete
because "a bit of work" feels like "a few hours"; wins are unburied because
dopamine is scarce.

### Why always-on runs through a marker file

A skill about the cost of starting friction cannot demand per-session
re-invocation. Typing `/i-have-adhd` at the start of every session is the
same failure the skill exists to remove — the practice dies before it forms.
The marker file moves activation out of the user's hands into the session
start: zero actions per session. The cost is symmetrical — turning it off
requires a deliberate file operation — which is why the mid-session off
phrase (`stop adhd mode` / `normal mode`) exists: standing mode is cheap to
keep and cheap to suspend, both through one empty file.

### Why the harness-wins escape hatch is load-bearing here

This environment runs plan mode, hard approval gates, and a global ruleset.
Several ADHD rules collide with those surfaces head-on: "lead with the next
action" would have a planning response open with "run this command" — which
plan mode forbids; "end with one concrete next action" collides with a gate
that requires a question, not an action. SKILL.md's break-rule 6 resolves
every such collision in one direction: the system prompt outranks the skill;
the constraint wins, and the shape survives wherever it can. Without that
clause the skill would fight the environment's core discipline; with it, the
skill only shapes the prose that remains.

### Why the list cap does not limit analysis

Rule 9 carries an explicit carve-out: it shapes presentation only. Analysis,
search, tool results, candidate generation, and retained information are
unlimited; the cap governs what the reader sees at once. This preserves the
completeness the environment's work requires while keeping the visible
working set small.

### Why there is no AGENTS.md block

GBrain and Graphify earned managed blocks in AGENTS.md because they write
persistent guidance that agents must consult across sessions. This skill's
guidance lives in the session prompt itself, injected fresh at each session
start by the marker mechanism. A second copy in AGENTS.md would create a
second source of the same ruleset to drift — two copies of one ruleset is a
contradiction waiting to happen. The session-prompt injection is the single
canonical delivery path.

### Where this sits relative to the rest of the system

- **PDLF** does not register it: it is not one of the skill families and owns
  no pipeline stage. Its only PDLF interaction is deferential — gates and
  checkpoints override the skill's shape rules (break-rule 6).
- **Memory Governor** does not see it: the skill content is vendor-published
  material installed by a CLI, so it takes the same permanent ordinary-sync
  bypass as `anvil-agent-references` and `magdoub-wireframe` — no developer
  judgment to review.
- **AGENTS.md** keeps its single-writer discipline intact: the ruleset never
  touches any AGENTS.md file.
- **The config-management system** (mb-config-manager pattern) has a suite for
  it and an exam module — `mb-config-i-have-adhd`, created 2026-09-20 on the
  developer's explicit instruction (see §5).

### Open questions

1. **Upstream pin — RESOLVED 2026-09-20 (run #1 Tier 3, gate-unlocked).** The
   bundle is verified byte-identical to upstream main; the HEAD pin of record
   is `839872f9d1cd…` (2026-09-19, docs-only merge). Standing drift-guards:
   the bundle hashes + the dual-path identity check (skill IA1-4).
2. **Design mode is informal.** Switching to exploratory output for design
   sessions relies on remembered off-phrases rather than an enforced
   mechanism (config open item 6 — the suite's one standing watch).

## 5. Config maintenance

This suite participates in the config-management system (`mb-config-manager`).
The roles of the suite files, and the exam cycle that runs them, are the
architecture described in [[config-manager-explainer|Explainer]] — emulated across the
estate from the PostgreSQL pilot. The short local version:

- [[i-have-adhd-config|Configuration]] is the **spec** — the ideal state every exam checks
  against.
- Before each exam run, the config-manager synthesizes
  [[i-have-adhd-exam-plan|Exam Plan]]: a fresh job-spec built from this spec, the last
  report, the log, and the learnings. The plan is transient (the file is
  live; contents rewritten each cycle).
- The exam runs the installed skill (`mb-config-i-have-adhd`) with the plan in
  hand — detection fully autonomous; healing gated. The module has **no
  agent-healable items**: the bundle, the marker, the slash command, and the
  symlink are vendor/policy surfaces, and every repair is developer-run or
  proposed.
- The run rewrites [[i-have-adhd-exam-report|Exam Report]] (current state, no history),
  appends one row to [[i-have-adhd-log|Log]], files new learnings, and prunes
  absorbed entries.

The exam module was created 2026-09-20 on the developer's explicit setup
instruction (register row added the same day, state `WIP` → `Installed` on
copy-install); its first formal run executed the same day — **HEALTHY, all
open items closed except the standing watch** (config open item 6).
[[i-have-adhd-skill|I Have Adhd Skill]] in this folder is the canonical source;
the installed copy at
`~/.config/opencode/skills/mb-config-i-have-adhd/SKILL.md` is the only
executing one — copy, never move. The module was born-with-inventory: the
standing check inventory lives in the skill, never in plans. Exams run on
demand (via `/mb-config-manager`), never scheduled.

## 6. S.W.O.T.

**Strengths.** A tiny, inspectable surface — mirrored bundle copies, a
symlink, a slash command, and a marker, all verifiable in minutes; the
ruleset contains its own collision-resolution clause (harness-wins), so it
cannot fight the environment's gates or plan mode; confirmed working from day
one (session-start injection observed on the installation date, proven
functionally by run #1's self-evidence probe); byte-identity drift-guards on
record (bundle hashes + dual-path check) and a verified upstream pin; the
always-on mechanism is a single empty file whose state is trivially checkable.

**Weaknesses.** The always-on scope is global — every session, including
design sessions, starts in ADHD mode unless the user switches (open item 6,
the suite's standing watch); the intro document's third-party claims remain
stale or understated (48.7k stars verified vs its ~29k claims) and sit in the
same folder as state documents, mitigated only by their provenance label.

**Opportunities.** The `agents/` bundle metadata (Gemini, OpenAI variants) is
documented but unused — candidates for removal or for reuse if other agents
are ever brought into the workflow; upstream's multi-agent adapters
(.cursor/, .codex-plugin/, hooks/) are estate-relevant only if those agents
are ever adopted; `npx skills update` offers a lighter update path than the
full re-add (untested here — a future exam item).

**Threats.** A reinstall or `npx skills` update could change the ruleset —
mitigated by the recorded bundle hashes and the dual-path identity check
(IA1-4), which make any change a detectable, spec-re-baseline event rather
than a silent one; the marker file's presence is the entire always-on state —
an accidental deletion silently changes every session's output style; rule
text could drift between the injected prompt copy and the installed SKILL.md
across an update window (the injection is generated from the file, so the
risk is bounded to the moment of change).

---

*Companion documents: [[i-have-adhd-config|Configuration]] (state),
[[i-have-adhd-reference|Reference: Invocation, Operation, Update]] (commands and rules),
[[i-have-adhd-exam-plan|Exam Plan]] / [[i-have-adhd-exam-report|Exam Report]] /
[[i-have-adhd-log|Log]] / [[i-have-adhd-learnings|Learnings]]
(config-management set), [[i-have-adhd-skill|I Have Adhd Skill]] (exam skill canonical
source; the installed copy is the only executing one),
[[i-have-adhd-intro|I Have Adhd Intro]] (research provenance — not state). Architecture:
the mb-config-manager pattern per [[config-manager-explainer|Explainer]].*
