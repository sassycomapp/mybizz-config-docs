---
title: "i-have-adhd-config"
doc-id: "mb-ba0e811b"
---
# i-have-adhd — Configuration

Canonical current-state configuration record for the i-have-adhd skill as
installed on this machine. Agent-facing. Reflects the live-verified state as
of 2026-09-20 (on-disk facts verified directly; upstream verified live the
same day — run #1 Tier 3, gate-approved). This document states facts, not
history — where a decision was made and the reasoning matters, see
`i-have-adhd-explainer.md`; for operational commands and rules, see
`i-have-adhd-reference.md`.

---

## Identity

| Item                                      | Value                                                                                                                                                                                                                  |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Skill name (SKILL.md frontmatter)         | `i-have-adhd`                                                                                                                                                                                                          |
| Component                                 | Third-party OpenCode output-style skill — action-first response shaping for a reader with ADHD; prose only, no executable surface                                                                                      |
| Upstream repository                       | `github.com/ayghri/i-have-adhd` — "A skill to stop your coding agent from burying the answer. ADHD-friendly output." (verified live 2026-09-20)                                                                        |
| Publisher                                 | Ayoub Ghriss ("ayghri"), individual developer (GitHub API, PGP-verified HEAD commit)                                                                                                                                   |
| Upstream state (verified live 2026-09-20) | 48.7k stars · 2.8k forks · 154 watching · 245 commits · 24 open issues · 44 PRs — actively maintained; multi-agent repo (Claude/Codex/Cursor/OpenCode/Gemini/Qwen/Kimi/Zed/Copilot/Hermes adapters)                    |
| Upstream HEAD (pin of record)             | `839872f9d1cd634fed642b4589ce7226199cc15f` — 2026-09-19 16:44 UTC, docs-only translation merge (#211), PGP-verified; post-dates the install and touches no skill content — bundle byte-identity to upstream main holds |
| License                                   | MIT (SKILL.md frontmatter + repo LICENSE)                                                                                                                                                                              |
| Version field                             | None in SKILL.md frontmatter — the drift-guards of record are byte-identity (bundle hashes + dual-path check) and the 2026-09-20 upstream verification; bundle verified byte-identical to upstream main                |
| Model invocation                          | `disable-model-invocation: true` — user-invoked only (slash command or always-on injection); the model never auto-activates it                                                                                         |
| Category / tags                           | category `productivity`; tags "ADHD, Output Style, Productivity, Formatting" (frontmatter)                                                                                                                             |
| Invocation                                | `/i-have-adhd` (session); always-on via marker file; off: `stop adhd mode` / `normal mode`                                                                                                                             |

## Install surface — what each piece is (re-baselined 2026-09-20, run #1 gate)

| Piece                                 | Path                                                                        | Written by                                                                                                                                                                                                    |
| ------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Registry primary (CLI install target) | `/home/dev-p/.agents/skills/i-have-adhd/` — `SKILL.md` + `agents/`          | `npx skills add ayghri/i-have-adhd -a opencode -y -g` (2026-09-19 23:27; re-verified idempotent 2026-09-20). The multi-agent universal registry; upstream documents `.agents/skills` as a valid OpenCode path |
| OpenCode copy (CLI-derived)           | `/home/dev-p/.config/opencode/skills/i-have-adhd/` — `SKILL.md` + `agents/` | The CLI copies from the registry primary on every install/update ("copy → OpenCode, overwrites: OpenCode" — verified 2026-09-20)                                                                              |
| Global skills symlink                 | `/home/dev-p/.config/skills` → `/home/dev-p/.config/opencode/skills`        | Created 2026-09-19 23:31 alongside install                                                                                                                                                                    |
| Slash command                         | `/home/dev-p/.config/opencode/command/i-have-adhd.md`                       | Install (survives reinstall — verified 2026-09-20)                                                                                                                                                            |
| Always-on marker                      | `/home/dev-p/.config/opencode/.i-have-adhd-always` (empty, 0 bytes)         | Developer (2026-09-19 23:31)                                                                                                                                                                                  |
| `opencode.json`                       | Nothing — no plugin registration, no MCP entry for this skill               | —                                                                                                                                                                                                             |

Not a git clone — the bundle carries no `.git`; provenance is the npx skills
CLI download. Drift-guards of record: the bundle hashes (below), the
dual-path byte-identity check (IA1-4), and the 2026-09-20 upstream
verification (bundle byte-identical to upstream main; HEAD pin in §Identity).

## Bundle contents (live-counted 2026-09-19; hashes verified 2026-09-20)

| File                 | Size / lines            | sha256 (first 16)  | Role                                                                                       |
| -------------------- | ----------------------- | ------------------ | ------------------------------------------------------------------------------------------ |
| `SKILL.md`           | 7,207 bytes / 142 lines | `3170b16ace00aecb` | Full ruleset — persistence clause, 10 rules, 6 sanctioned overrides, 5-item pre-send check |
| `agents/gemini.toml` | 2,157 bytes / 24 lines  | `5108a6123beb9df2` | Gemini CLI custom-command variant of the same ruleset (unused on this machine)             |
| `agents/openai.yaml` | 238 bytes / 7 lines     | `2c51291283dcefdc` | OpenAI interface metadata (unused on this machine)                                         |

Both install locations carry byte-identical copies (verified 2026-09-20;
hashes apply to both).

## Runtime activation model

| Surface           | Mechanism                                                                                                               | Scope                                                  |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| On-demand         | `/i-have-adhd` — the slash command wrapper loads the skill and instructs the agent to apply its ruleset for the session | Rest of that session                                   |
| Always-on         | Marker file presence injects the ruleset at session start                                                               | Every session while the file exists                    |
| Off (mid-session) | `stop adhd mode` / `normal mode` — one-line confirmation, default style returns                                         | Rest of that session; skill returns via `/i-have-adhd` |
| Off (standing)    | Marker file deleted                                                                                                     | Always-on ends for good                                |

## Current state (verified live 2026-09-20)

| Item               | Value                                                                                                                                                                                                                                                                               |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Always-on marker   | Present, empty, since 2026-09-19 23:31 (re-verified 2026-09-20)                                                                                                                                                                                                                     |
| Run evidence       | Confirmed — session-start injection observed in the live system prompt ("ADHD MODE ACTIVE (always-on)" with the full ruleset); proven functionally on 2026-09-20 by the run #1 self-evidence probe (exam session's own system prompt carries the block while the marker is present) |
| Slash command      | Present, references the skill by name, session-scoped phrasing consistent with SKILL.md's persistence clause (survived the 2026-09-20 reinstall test untouched)                                                                                                                     |
| Confirmed behavior | Ruleset active in every session while the marker exists — functional proof 2026-09-20                                                                                                                                                                                               |

## Integration facts

| Item                     | State                                                                                                                                                                                                                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OpenCode skill discovery | Global skills dir `/home/dev-p/.config/opencode/skills/`; the `~/.config/skills` symlink aliases it for the npx skills CLI's conventional path                                                                                                                                |
| AGENTS.md                | No managed block, no second writer — the always-on ruleset lands in the session system prompt, not in any AGENTS.md file (see `i-have-adhd-explainer.md` §4)                                                                                                                  |
| GBrain                   | Skills dir is not a registered source; this suite's source is `mybizz-config-docs` (`/mnt/c/mybizz/mybizz-config-docs`, federated)                                                                                                                                            |
| PDLF                     | Not registered as a PDLF stage — cross-cutting output shaping, outside the skill families; PDLF gates and steps are unaffected (SKILL.md break-rule 6 defers to the harness)                                                                                                  |
| Cupcake                  | No interaction — the skill creates no sub-agents, runs no commands, writes no files                                                                                                                                                                                           |
| Memory Governor          | Bypass class: vendor-published material installed by a CLI, not developer-authored — same standing class as `anvil-agent-references` / `magdoub-wireframe`; ordinary `gbrain sync` only                                                                                       |
| Exam module              | `mb-config-i-have-adhd` — copy-installed 2026-09-20 at `~/.config/opencode/skills/mb-config-i-have-adhd/SKILL.md` (source `i-have-adhd-skill.md` in this folder; hash pair `1669db5ef2192a0d` after the run #1 IA1-4 amendment); born-with-inventory; no agent-healable items |

## Settled policy

| Rule                     | Detail                                                                                                                                                                              |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Always-on                | Developer decision 2026-09-19 — marker file present; every session starts in ADHD mode until the marker is removed (state file: `/home/dev-p/.config/opencode/.i-have-adhd-always`) |
| Content sync into GBrain | Ordinary `gbrain sync` — permanent bypass of Memory Governor's review pipeline (vendor material via CLI install; no developer-authored confidence/contradiction judgment to make)   |
| In-place skill edits     | Not permitted — the installed `SKILL.md` is vendor material; changes arrive via upstream and reinstall                                                                              |

## Known unverified or stale claims in `i-have-adhd-intro.md`

| Intro claim                                                                | Live reality on this machine                                                                                                              |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Marker at `$HOME\.opencode\.i-have-adhd-always`                            | Live marker: `/home/dev-p/.config/opencode/.i-have-adhd-always` (the OpenCode config dir here is `~/.config/opencode`, not `~/.opencode`) |
| ~29k stars / "28,000 developers" (third-party citations)                   | Verified live 2026-09-20: 48.7k stars — the intro's third-party figures were understated/stale                                            |
| Install pulls into `.opencode/skills/i-have-adhd/` (project-local framing) | Global variant used here: `~/.config/opencode/skills/i-have-adhd/` via the `-g` flag                                                      |
| `npx skills add` wires the slash command into sessions                     | Confirmed consistent — `/home/dev-p/.config/opencode/command/i-have-adhd.md` exists and matches                                           |

## Security supply-chain review (recorded 2026-09-20, gate-approved — run #1 Tier 3 IA3-3)

Axes per the estate's review-before-trust class (magdoub-wireframe precedent):

| Axis             | Finding                                                                                                                                                                                                                                                         | Verdict                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Publisher        | Ayoub Ghriss ("ayghri") — individual developer; repo credits "loosely based on *The Adult ADHD Tool Kit*" (Ramsay & Rostain)                                                                                                                                    | Acceptable (single-maintainer vendor, same class as other community skills in the estate) |
| License          | MIT — repo LICENSE file + SKILL.md frontmatter agree                                                                                                                                                                                                            | Clear                                                                                     |
| Maintenance      | 48.7k stars / 2.8k forks / 245 commits / 24 open issues / 44 PRs; HEAD 2026-09-19 (day before verification) — actively maintained                                                                                                                               | Clear                                                                                     |
| Spawn-capability | Pure prose skill — no executable code in the bundle; `disable-model-invocation: true`; the `agents/` files are metadata for other CLI agents, not code. CLI-run security assessments at install/update (2026-09-20): Gen Safe · Socket 0 alerts · Snyk Low Risk | Benign in this environment                                                                |

Overall: benign on every axis. Open item 4 closed with this record.

## Open items

| #   | Item                                                                                                                                                                                                                                                                  | Status          |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| 1   | ~~Upstream live state unverified~~ — **verified live 2026-09-20** (run #1 Tier 3 IA3-1, gate-unlocked): 48.7k stars, actively maintained, publisher Ayoub Ghriss; see §Identity                                                                                       | **Closed**      |
| 2   | ~~No version pin / drift unknown~~ — **closed 2026-09-20**: bundle verified byte-identical to upstream main (IA3-2 re-run hash proof); HEAD pin of record in §Identity; standing drift-guards = bundle hashes + dual-path identity check (IA1-4)                      | **Closed**      |
| 3   | ~~Update mechanism unverified~~ — **verified live 2026-09-20** (IA3-2, gate-unlocked): re-run refreshes the registry copy, overwrites the OpenCode copy from it, slash command survives, marker untouched, byte-idempotent on identical content; see §Install surface | **Closed**      |
| 4   | ~~Supply-chain review owed at adoption~~ — **reviewed and recorded 2026-09-20** (IA3-3, gate-approved; see Security supply-chain review above); benign on all axes                                                                                                    | **Closed**      |
| 5   | ~~Empty scaffold siblings / no exam module~~ — **closed 2026-09-20**: scaffold populated, exam module `mb-config-i-have-adhd` created and installed (see §Integration facts); first formal run #1 executed same day                                                   | **Closed**      |
| 6   | Design-mode discipline is informal: exploratory output for design sessions relies on the user remembering `normal mode` or session-level marker removal; no enforced mechanism exists.                                                                                | Open (standing) |
