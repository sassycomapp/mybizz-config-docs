---
title: "opencode-explainer"
doc-id: "opencode-explainer"
---
# OpenCode Explainer

*Companion note: for current confirmed state (identity, global-config content,
plugin state, skill discovery, Active Project Standard) see [[opencode-config|OpenCode Configuration]].
For commands and the restart/verification procedures, see [[opencode-reference|Commands, Verification, Troubleshooting]].
For the permission layers and the verified merge, see
[[opencode-permission-access-control-model|Permission & Access Control Model]]. For how this system is examined and
kept healthy by the config-management apparatus, see §8 below and the suite's exam
set ([[opencode-exam-plan|Exam Plan]] / `-exam-report.md` / `-log.md` / `-learnings.md`).*

---

## 1. Opening

OpenCode is the actual harness this entire environment runs inside — the
program that reads `AGENTS.md`, loads skills, enforces (or fails to
enforce) permissions, and decides which tool calls an agent can make.
Every other system documented in this project — Cupcake, GBrain, Memory
Governor, Sentinel, the PDLF application itself — is either a plugin
running inside OpenCode, or a tool OpenCode's agents call. Understanding
OpenCode's own real behavior, including its genuine rough edges, matters
more than any single tool built on top of it.

**OpenCode spans every layer of the environment** (see
[[pdlf-environment-explainer|the pre-makePDLF, makePDLF, PDLF, and shipped layers]] for the layer map): the
pre-makePDLF supporting systems run inside or beside it, the makePDLF
project builds the PDLF application in it, the PDLF layer builds the
shipped estate through it — and nothing in it travels to the shipped
estate. It is the harness for every layer except the one it produces.

This document exists because several real, costly incidents traced back
not to Cupcake, not to GBrain, but to OpenCode's own underlying mechanics
— behaving in ways that were reasonable, once understood, but genuinely
surprising the first time each one was hit.

---

## 2. Plugins Load Once, Not Per-Session

The single most consequential mechanical fact about OpenCode, discovered
the hard way, more than once: **a plugin is loaded exactly once, when the
OpenCode process itself starts — never per chat session, and never
automatically on a file change.**

Editing a plugin's own code on disk, while OpenCode is already running,
has zero visible effect. No error. No warning. The old, already-loaded
version keeps running silently, exactly as if nothing had changed, until
the whole process is fully quit and relaunched. This applies identically
to Cupcake's plugin, to MCP server entries like GBrain's, and to any other
plugin registered with OpenCode. Verified live twice: the Cupcake
suspension (2026-09-06) and its reactivation (2026-09-08) each required a
full process restart to take effect.

**A related, distinct trap: OpenCode does not deduplicate plugins by real
file identity — only by the path it was told to load.** If the same plugin
exists at two separate discovery paths — even a global copy and a symlink
pointing at that exact same file — OpenCode loads both as two independent
instances. Confirmed directly: this caused Cupcake's cross-project grant
system to decrement its write count by two for every single real write,
not one, because the plugin was genuinely running twice. A symlink did not
fix this — only removing the second discovery path entirely did. The
lesson generalizes beyond Cupcake specifically: **a plugin, skill, or MCP
entry must exist at exactly one discoverable path, never two, even if both
point at identical content.**

---

## 3. Skill Discovery — Several Real, Different Mechanisms, Not One

Skills reach OpenCode through more than one real pathway, and they are not
all installed the same way — confirmed directly by a full, real audit of
every skill on this machine (2026-09-08, the full inventory is
[[skill-index|Skill Index]]):

- **Plain, real folders** — no symlink at all. This project's own custom
  skills (`mb-align-docs`, `mb-docs-manager`, etc.) work this way.
- **Symlinks to a real folder elsewhere on the same drive** — most
  third-party skills (Anvil, GStack's individual skills, Archify).
- **A hybrid pattern** — GStack's own top-level entry is a real folder,
  but individual skills *inside* that folder are themselves further
  symlinks to yet another location.
- **A two-hop pattern** — Magdoub's wireframe skill points to an empty
  intermediate folder, which in turn points to the real content sitting in
  a completely separate directory tree (`~/.claude/skills/`).

No single "correct" install method exists across every skill-set; what
matters is that whichever method is used, it resolves correctly from
OpenCode's own real discovery path.

---

## 4. The `drvfs` Symlink Trap — Windows and WSL Disagree About What a Link Is

A real, structural incompatibility, confirmed directly through forensic
inspection of the actual filesystem reparse-point tags: **a symlink
created from inside WSL, pointing at a folder on the Windows drive,
produces a special "LX symlink" type that Windows Explorer cannot read at
all** — it shows as an empty, 0-byte file, not a broken link, not an
error, just apparently nothing.

The reverse direction has the opposite problem: a symlink created from the
*Windows* side, pointing back *into* WSL's own internal filesystem,
displays correctly in Explorer but cannot be resolved from WSL's own side.

**The only combination that works reliably both ways: create the symlink
from the Windows side, using `mklink /D`, pointing at a target that itself
lives on the Windows drive** — never a WSL-internal path. This requires
Windows Developer Mode to be enabled for an unprivileged account to create
this specific kind of link at all; without it, only a junction (a
different, slightly less capable link type) is available without elevated
permissions.

---

## 5. Global vs. Per-Project Configuration — and the Verified Merge

Two separate, distinct config layers exist:

- **Global** — `~/.config/opencode/opencode.jsonc`, applies everywhere,
  every project, unless overridden.
- **Per-project** — an `opencode.json` sitting inside a specific project's
  own folder, overriding the global config for that project only.

**The merge semantics are now verified, not assumed (2026-09-09):**
configuration files are **merged together, not replaced** — project config
overrides global config only for conflicting keys; non-conflicting
settings from both survive; and nested permission maps **merge deeply**
(verified empirically with `opencode debug config`: a project-level bash
allow override and all thirteen global deny patterns were both present in
the resolved map). The upstream documentation is authoritative:
opencode.ai/docs/config, "Precedence order."

**A separate, now-resolved incident: the global folder itself briefly held
two files at once** — `opencode.json` and `opencode.jsonc`, both real,
both loaded, with genuinely different content in each, and no clear,
verified answer for which one would win if they ever conflicted. Confirmed
and fixed 2026-09-01: consolidated into a single `opencode.jsonc`, the
other deleted. One file, one source of truth, going forward — see
[[opencode-config|OpenCode Configuration]] for the real, current content.

---

## 6. Stale Database Rows, and the Two-WSL-Distro Risk

OpenCode tracks known projects and sessions in its own local database,
with no built-in cleanup when a project folder is renamed or moved — the
old row simply lingers, sometimes causing OpenCode to open the wrong,
stale project on startup. A real, dedicated script
(`opencode-db-cleanup.sh`) exists specifically for this, run manually,
right after any project rename or move — never scheduled automatically,
since a false positive (like a temporarily unmounted drive) could
otherwise delete real history unattended.

**A separate, more subtle risk, confirmed real on this specific machine
(distros verified live 2026-09-09): two WSL distributions are installed,
and the actual working environment lives in the non-default one.** Any
command triggered from the Windows side — a scheduled task, a shortcut —
that invokes `wsl.exe` without explicitly naming the correct distro and
user risks silently running against the wrong environment entirely, with
no visible error. Every real, Windows-triggered command touching this
environment must explicitly specify `-d <distro> -u <user>`.

---

## 7. Known Limitations, Honestly Stated

**No native session-start hook exists.** There is no OpenCode mechanism
that automatically runs a checklist or prompt at the start of every
session — the session-start checklist is a human-run practice, pasted
manually, not a technical control.

**No skill-identity field reaches any plugin.** Confirmed directly, from
OpenCode's own real source: the event a plugin receives for any tool call
carries the tool name, arguments, and session ID — never which skill, if
any, triggered the call. Per-skill permission rules are not currently
possible for this reason, confirmed structurally, not assumed.

**Plugin deduplication is by path, not identity** — covered fully in
Section 2. Anything relying on a plugin's state (like a count or a cache)
must ensure that plugin is discoverable from exactly one path.

---

## 8. Config maintenance — how this system is examined and kept healthy

This suite participates in the config-management system (`mb-config-manager`).
The roles of the seven suite files, and the exam cycle that runs them, are the
architecture described in [[config-manager-explainer|Explainer]] — emulated from the
PostgreSQL pilot. The short local version:

- [[opencode-config|OpenCode Configuration]] is the **spec** — the ideal state every exam checks
  against. OpenCode is working well; the exam verifies that and changes nothing.
- Before each exam run, the config-manager synthesizes [[opencode-exam-plan|Exam Plan]]:
  a fresh job-spec built from this spec, the last report, the log, and the
  learnings. The plan is transient (the file is live; contents rewritten each
  cycle).
- The exam runs the installed skill (`mb-config-opencode`) with the plan in hand —
  detection fully autonomous; healing gated. **This module has no agent-healable
  items**: the harness's own config, plugin tree, and process are beyond agent
  repair by design — every repair is developer-run or proposed.
- **The self-referential trap, named:** the config-manager itself lives **inside**
  this harness (`~/.config/opencode/skills/`, plugin, skills). The exam therefore
  never touches the plugin tree, never restarts the running process (it would
  interrupt the very session running the exam), and never edits its own
  config file. Self-health of the config-manager is step-0 of every exam cycle
  (register ↔ installed skill ↔ source hash), never a finding of this module.
- **Scope boundary with sibling modules:** cupcake **enforcement** (rules compile +
  firing) belongs to `mb-config-cupcake` — this exam owns the plugin's
  **discoverability/dedup mechanics** (exactly one discoverable path). GBrain
  **server** liveness belongs to `mb-config-gbrain` — this exam owns the
  `mcp.gbrain` **config entry**. The **session database** and its cleanup belong
  to [[opencode-project-session-data-integrity|Project & Session Data Integrity]] (agent content reads
  guard-denied — the exam checks presence only, via directory listing). Full skill
  **inventory** belongs to [[skill-index|Skill Index]] (docs-managed) — this exam checks
  discovery **mechanics**, never re-audits the inventory.
- Several checks are permanently **developer-run**: `opencode.jsonc` content
  (sensitive-data guard class), the session-data doc content (proven denial), and
  everything in Tier 3 (full restart; WSL default-distro check via `wsl.exe`;
  the upgrade decision).
- The run rewrites [[opencode-exam-report|Exam Report]] (current state, no history), appends
  one row to [[opencode-log|Log]], files new learnings, and prunes absorbed entries.

## 9. S.W.O.T.

**Strengths.** Three independently-verified hard facts underpin every other
system's exam: configs **merge** (project overrides global only on conflict;
nested maps merge deeply — verified 2026-09-09); plugins load **once** at process
start (verified twice); deny patterns match command **text** (verified live). The
suite's probe set is deliberately small because the mechanics are proven.

**Weaknesses.** The deepest checks are developer-run by natural law (full restart
kills the session that asks; `wsl.exe` is Windows-side; config content is
sensitive-guarded). Version/behavior drift between spec and reality is only as
visible as the exams' spot-probes make it — a deep merge re-verification is not
performed each run.

**Opportunities.** Every other config-manager module inherits OpenCode's verified
truths (merge, load-once, text-matching) — the harness is the foundation layer
the whole estate builds on; one healthy exam here pays forward across all
modules. The plugin/skill inventory stays a docs-side concern, so the exam stays
small and fast.

**Threats.** A future OpenCode upgrade could silently change merge, load, or
deny-matching behavior (mitigated: OC1/OC2 re-verify, never assume); a second
discoverable plugin path could revive the double-load class of bug (mitigated:
OC1-5 watches exactly-one-path); a "Paused" project's config could be mistaken
for stale and removed (mitigated: the Active-Project Standard is checked, and the
spec explicitly forbids treating Paused configs as stale).

---

*Companion documents: [[opencode-config|OpenCode Configuration]] (current configuration, real skill
inventory, active-project standard),
[[opencode-permission-access-control-model|Permission & Access Control Model]] (the permission layers),
[[opencode-project-session-data-integrity|Project & Session Data Integrity]] (the session database),
[[opencode-reference|Commands, Verification, Troubleshooting]] (procedures). Config-management set:
[[opencode-exam-plan|Exam Plan]] / `-exam-report.md` / `-log.md` / `-learnings.md`.
Exam skill canonical source: [[opencode-skill|Opencode Skill]]. Architecture:
[[config-manager-explainer|Explainer]]. The environment layer map:
[[pdlf-environment-explainer|the pre-makePDLF, makePDLF, PDLF, and shipped layers]].*

*End of document*
