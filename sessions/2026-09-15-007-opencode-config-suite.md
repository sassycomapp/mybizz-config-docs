---
title: "2026-09-15-007-opencode-config-suite"
doc-id: "mb-9c2693c3"
updated: "2026-10-01"
---
# Session 007 — mb-config-opencode config-management suite built, installed, run #1 HEALTHY

## What was done

1. **Suite build-out (Phase 1).** Built the OpenCode configuration-management
   suite to the 7-file standard + skill source in `mybizz-config-docs/opencode/`:
   [[[mybizz-config-docs:opencode/opencode-exam-plan|Exam Plan]]](C:/mybizz/mybizz-config-docs/opencode/opencode-exam-plan.md) (hand-written bootstrap plan, the format template),
   [[[mybizz-config-docs:opencode/opencode-exam-report|Exam Report]]](C:/mybizz/mybizz-config-docs/opencode/opencode-exam-report.md) (placeholder), [[[mybizz-config-docs:opencode/opencode-log|Log]]](C:/mybizz/mybizz-config-docs/opencode/opencode-log.md) (seeded from the
   suite's documented history: the 2026-09-01 config consolidation, the
   2026-09-06/08 plugin-restart incidents, the 2026-09-09 merge/deny/distro
   verifications, skill discovery taxonomy), [[[mybizz-config-docs:opencode/opencode-learnings|Learnings]]](C:/mybizz/mybizz-config-docs/opencode/opencode-learnings.md) (preamble +
   empty table), [[[mybizz-config-docs:opencode/opencode-skill|Opencode Skill]]](C:/mybizz/mybizz-config-docs/opencode/opencode-skill.md) (born-with-inventory, `mb-config-opencode`),
   and localized [[[mybizz-config-docs:opencode/opencode-explainer|OpenCode Explainer]]](C:/mybizz/mybizz-config-docs/opencode/opencode-explainer.md) (top companion note, §8 Config
   maintenance, §9 S.W.O.T., footer) and [[[mybizz-config-docs:opencode/opencode-reference|Commands, Verification, Troubleshooting]]](C:/mybizz/mybizz-config-docs/opencode/opencode-reference.md) (exam-set
   pointers in the header).
2. **Install (Phase 2).** Requested `mg-grant --path
   ~/.config/opencode/skills/mb-config-opencode --count 3` (developer-run,
   granted). Copy-installed the skill (copy, never move) to
   `~/.config/opencode/skills/mb-config-opencode/SKILL.md`; hash pair verified
   (`039b28e46b276834` initial). Register row flipped WIP → Installed. After
   run #1 learnings graduation, the skill was re-copied and re-hashed
   (final `268bb702a038448b`), register updated.
3. **Formal run #1 (Phase 3).** Step-0 self-validation PASS: 8/8 hash pairs via
   the approved glob form, suite completeness 7/7 on all eight Installed suites
   (mb-submit-memory naming variance register-documented), register spec-doc
   paths 8/8, no open run blocks. Tiers 0–2: version 1.15.12 exact; single
   global `.jsonc` (no sibling); global AGENTS.md present (~16.2 KB, moved from
   the spec's 14.4 KB figure — size drift, not a defect); resolved-config
   inspection runs (exit 0); instructions pointer resolves; plugin
   **discoverable exactly once** and **loaded exactly once in-session**; Active
   Project Standard holds (makepdlf present / mb-3-cs retained incl.
   mb-3-cs-project-library / mb4ecom+mb5pdlf absent / project-template literal);
   suite complete 7/7; known scope limitations honest. **Verdict: HEALTHY.**
4. **Guard denials honored (4).** (a) step-0 compound loop text carrying the
   `cupcake` token (exec-protection, token-in-command-text class) — re-issued as
   a directory-glob form; (b) resolved-config field extraction from a capture
   (sensitive-data — the resolved config carries `mcp.gbrain` env sections) —
   became a developer-run class; (c) a grep argument containing the `cupcake`
   token (exec-protection matches argument literals, not just paths) — re-issued
   path-free; (d) shell-mediated write outside the project on a compound
   orientation probe — honored, single-purpose glob form used. No denial was
   retried through an alternate path.
5. **Developer bundle (D-1) closed developer-verified.** The developer ran
   `opencode debug config` and `cat ~/.config/opencode/opencode.jsonc`; all
   field checks PASS: default_agent `plan`; permission.task deny; permission.edit
   ask + `**/anvil.yaml` deny; webfetch ask; permission.bash ask + all 13 deny
   patterns; agent.plan.permission.edit deny; mcp.gbrain local
   (`/home/dev-p/.bun/bin/gbrain serve`, `enabled: true`, `{env:...}`
   placeholders — no literals in config). Two new spec omissions surfaced:
   **F-4** `external_directory` carries a 4th allow root
   (`C:\data-mybizz-mgt\**`) and **F-5** `agent.docs-manager` subagent is
   undocumented.
6. **Gate approved all items (Phases 4–5).** F-4 and F-5 **approved and
   applied**: [[[mybizz-config-docs:opencode/opencode-config|OpenCode Configuration]]](C:/mybizz/mybizz-config-docs/opencode/opencode-config.md) §Global config updated (4th root, docs-manager
   row, 13-pattern note, 2026-09-15 re-verified banner, AGENTS.md ~16.2 KB) and
   [[[mybizz-config-docs:opencode/opencode-permission-access-control-model|Permission & Access Control Model]]](C:/mybizz/mybizz-config-docs/opencode/opencode-permission-access-control-model.md) per-agent bullet updated.
   **F-6** security confirmation recorded: `opencode debug config` stdout carries
   **literal API values** while the source `.jsonc` correctly holds `{env:...}`
   placeholders — confirms the sensitive-data guard class, the capture-delete
   discipline, and the rule that resolved-config stdout is secret-bearing.
   Tier 3 stays **locked**; stay on 1.15.12 (no check failed; policy: never on
   newness). Two run learnings **graduated into the skill** (config-content
   field extraction = permanently developer-run; exec-protection guard matches
   tokens in argument literals), learnings entries deleted.
7. **Register + logs updated.** Register row carries final hash/install/run
   facts; [[[mybizz-config-docs:mb-config-manager/config-manager-log|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md) records step-0 PASS + run closure;
   [[[mybizz-config-docs:opencode/opencode-log|Log]]](C:/mybizz/mybizz-config-docs/opencode/opencode-log.md) records the run row with the full gate disposition.

## Quirks and their dispositions

- **The exam runs inside the harness it exams** — restarts are Tier 3 and
  developer-run on the developer's schedule; the session database doc content is
  guard-denied (presence-only checks), and `opencode.jsonc` raw reads are
  standing-denied (resolved config via `opencode debug config` instead).
- **Config-content field extraction is guard-denied by class** — the executable
  config command runs, but extracting fields from a capture is blocked. All such
  checks are permanently developer-run (runner D).
- **A transcription slip caught and corrected:** the register initially recorded
  the re-installed hash as `268bb702a0384482`; the true first-16 is
  `268bb702a038448b` (b, not 2). Corrected in all three files.
- **A log-row editing slip caught and corrected:** an edit on
  [[[mybizz-config-docs:mb-config-manager/config-manager-log|Log]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-log.md) briefly replaced the mb-submit-memory row instead of
  appending; restored verbatim.

## Standards the developer set

- Grant discipline: the agent always requests grants; the developer executes
  `mg-grant` in WSL and returns the result (never self-grant).
- Never upgrade on newness — only on check failure (re-affirmed for OpenCode
  1.15.12).
- Spec-doc corrections are applied only with explicit developer approval at the
  gate (the F-4/F-5 precedent).

## Artifacts

- Suite: `opencode/opencode-{config,exam-plan,exam-report,log,learnings,explainer,reference,skill}.md` (10 files incl. the two sister scope docs).
- Installed skill: `~/.config/opencode/skills/mb-config-opencode/SKILL.md` (hash `268bb702a038448b`).
- Modified: `mb-config-manager/config-manager-{log,register}.md`.

## Open / next

- None open in this suite. Next regular exam run of `mb-config-opencode` will be
  plan-synthesized per the standard cycle. Tier 3 (restart + WSL distro +
  upgrade decision) remains available for a future unlock.
- The pre-existing [[[mybizz-config-docs:gbrain/gbrain-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-explainer.md) working-tree change predates
  this session — flagged, not touched.
