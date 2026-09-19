---
document: "i-have-adhd — Reference: Invocation, Operation, Update"
doc-id: i-have-adhd-reference
state: Live
date-created: 2026-09-19
---

# i-have-adhd — Reference: Invocation, Operation, Update

Companion to `i-have-adhd-config.md` (current installed state, open items) and
`i-have-adhd-explainer.md` (design reasoning). Agent-facing. The full ruleset
lives in the skill's own `SKILL.md` (loaded into the session prompt on
invocation); this doc carries what is needed to invoke, run, constrain,
update, and remove the skill on this machine.

Config-management set: `i-have-adhd-exam-plan.md` (transient job-spec — read
second, every exam run), `i-have-adhd-exam-report.md` (last verified state),
`i-have-adhd-log.md` (chronological events), `i-have-adhd-learnings.md`
(transient knowledge). The exam skill's canonical source is
`i-have-adhd-skill.md` (installed as `mb-config-i-have-adhd`; the installed
copy is the only executing one — copy, never move). Research provenance:
`i-have-adhd-intro.md` (third-party sources — not verified state).

---

## Activation

| Surface | How | Scope |
|---|---|---|
| On-demand | `/i-have-adhd` (slash command, backed by `~/.config/opencode/command/i-have-adhd.md`) | Rest of that session |
| Always-on | Presence of the marker file `~/.config/opencode/.i-have-adhd-always` (empty, presence = on) | Every session while the file exists — ruleset injected at session start |
| Off (mid-session) | Say `stop adhd mode` or `normal mode` | Rest of that session; skill returns via `/i-have-adhd` |
| Off (standing) | Delete the marker file | Always-on ends for good |

`disable-model-invocation: true` in SKILL.md frontmatter — the model never
activates this skill on its own; only the slash command or the always-on
injection turns it on.

## What active mode does (SKILL.md is authoritative)

Ten rules, applied to every response until the off phrase:

| # | Rule |
|---|---|
| 1 | Lead with the next action — first line is something the reader can do, not context |
| 2 | Number multi-step tasks — one bounded action per step, fewest steps that work |
| 3 | End with one concrete next action doable in under two minutes |
| 4 | Suppress tangents — finish the first issue; offer the second as a separate question |
| 5 | Restate state every turn (step position, what is done, what is next) |
| 6 | Give specific time estimates in concrete units — never "a bit of work" |
| 7 | Make completed work visible in concrete terms ("Login now works. Try: …") |
| 8 | Matter-of-fact tone for errors — state cause, then fix; no "uh oh" |
| 9 | Cap visible lists to 5 items — presentation only; never omit relevant items when completeness matters |
| 10 | No preamble, no recap, no closing pleasantries |

Persistence clause: the rules apply to every response for the rest of the
session, across topic changes; they lapse only on `stop adhd mode` /
`normal mode`.

## Sanctioned overrides (break the rules when)

1. Reader asks to "explain" or "walk me through" — full explanation; still no preamble or closer.
2. Destructive action ahead (`rm -rf`, force push, schema migration, table drop) — confirm first; safety wins over brevity.
3. Debug spiral (three consecutive "still broken" turns) — stop iterating; name the assumption that might be wrong; ask one diagnostic question.
4. Real ambiguity — one short clarifying question beats guessing.
5. A rule fights the task — the task wins; the shape stays (e.g. "what are my options" gets ranked options, not one path).
6. A rule fights the harness — the harness/system prompt outranks the skill; the constraint wins, the shape stays. This is the clause that keeps plan mode, approval gates, and PDLF checkpoints unaffected.

## Pre-send check

Before sending, delete: (1) the first sentence if it announces what is about
to happen; (2) the last sentence if it asks "anything else?" or recaps;
(3) any "by the way" sidebar; (4) hedging adverbs adding no information;
(5) idioms — replace with the literal action. Then verify: reading only the
first and last line, the reader knows what to do next and what just
happened.

## Install / reinstall

```bash
npx skills add ayghri/i-have-adhd -a opencode -y -g
```

What the install wrote on this machine (2026-09-19):

| Piece | Path |
|---|---|
| Registry primary (npx CLI's install target) | `~/.agents/skills/i-have-adhd/` — `SKILL.md` + `agents/` (the multi-agent universal registry; upstream documents `.agents/skills` as a valid OpenCode path) |
| OpenCode copy (CLI-derived) | `~/.config/opencode/skills/i-have-adhd/` — `SKILL.md` + `agents/` (written by the CLI from the registry copy: "copy → OpenCode, overwrites: OpenCode") |
| Global skills symlink | `~/.config/skills` → `~/.config/opencode/skills` (aliases the whole dir for the npx skills CLI's conventional path) |
| Slash command | `~/.config/opencode/command/i-have-adhd.md` |
| `opencode.json` | Nothing — no plugin registration, no MCP entry |

Manual fallback (no npx skills CLI): fetch the upstream `SKILL.md` raw file
and write it into the skill directory (per `i-have-adhd-intro.md` Option B;
the exact upstream raw URL is not verified here — open item).

## Always-on toggle

```bash
# on (stays on for every session until removed)
touch /home/dev-p/.config/opencode/.i-have-adhd-always

# off (turn always-on off for good)
rm /home/dev-p/.config/opencode/.i-have-adhd-always
```

Per-session off while the marker is present: either temporarily rename the
marker before starting the session and restore it afterwards, or say
`normal mode` mid-session.

## Update

Re-running the install command is the expected update path (behavior verified
live 2026-09-20, run #1 Tier 3):

```bash
npx skills add ayghri/i-have-adhd -a opencode -y -g
```

Verified behavior: the CLI refreshes the registry copy first
(`~/.agents/skills/i-have-adhd/`), then overwrites the OpenCode copy from it
("copy → OpenCode, overwrites: OpenCode"); the slash-command file survives; the
always-on marker is untouched; on identical content the run is byte-idempotent.
After any update, compare both copies byte-for-byte (spec §Bundle contents
hashes) and re-read the installed `SKILL.md` against the spec — a content
change is a spec re-baseline, never an in-place patch. In-place edits to either
copy never survive a reinstall.

## Uninstall

```bash
rm -rf /home/dev-p/.config/opencode/skills/i-have-adhd
rm /home/dev-p/.config/opencode/command/i-have-adhd.md
rm -f /home/dev-p/.config/opencode/.i-have-adhd-always
```

Do not remove the `~/.config/skills` symlink as part of uninstalling this
skill — it aliases the entire global skills directory (shared infrastructure
for the npx skills CLI's conventional path).

## Do not

- Do not treat the 5-item list cap (rule 9) as license to omit analysis — it shapes presentation only; never omit relevant items when completeness matters.
- Do not assume `stop adhd mode` survives a session — the marker re-applies the ruleset at every new session start; the phrase is mid-session only.
- Do not hand-patch the installed `SKILL.md` expecting changes to survive a reinstall — it is vendor material; changes arrive via upstream and reinstall.
- Do not remove the `~/.config/skills` symlink as part of uninstalling this skill.
- Do not treat `i-have-adhd-intro.md` as verified state — it is research notes assembled from third-party reviews; several of its specifics (star counts, marker path, install layout) are unverified or stale for this machine.
- Do not run deep design or architecture sessions expecting exploratory output while the marker is present, without either saying `normal mode` or starting the session with the marker removed.
- Do not create a second activation path for the same ruleset (a duplicate skill folder or a second slash-command file) — it would load the same instructions twice into the session prompt. The installer's own registry copy at `~/.agents/skills/i-have-adhd/` is documented state (config §Install surface), not a violation; manually created duplicates remain prohibited.
- Do not describe the installed bundle as pinned to a specific upstream version or HEAD — no pin exists (config open item 2).
- Do not expect the skill to change analysis depth, tool behavior, gates, or PDLF steps — it is output shaping only; break-rule 6 (harness wins) governs every collision.
