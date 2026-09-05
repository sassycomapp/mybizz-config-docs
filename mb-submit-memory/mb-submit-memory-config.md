# mb-submit-memory — Configuration

Canonical current-state configuration record. Agent-facing. Reflects the real,
confirmed state of the `mb-submit-memory` skill as of 2026-09-05, drawn directly
from its `SKILL.md` and its one confirmed real run. This document states facts,
not history — where a decision was made and the reasoning matters, see
`mb-submit-memory-explainer.md`.

---

## Identity

| Item | Value |
|---|---|
| Skill name | `mb-submit-memory` |
| Location | `~/.config/opencode/skills/mb-submit-memory/SKILL.md` (WSL-native path) |
| Invocation | `/mb-submit-memory (path)` — path always given explicitly by the developer, never inferred |
| Structure | **Single file** — `SKILL.md` (13,502 bytes) plus its `Zone.Identifier` sidecar only. Unlike Docs Manager, this skill has **no separate sub-agent files** — one continuous run, one file, despite sharing Docs Manager's/mb-wikilinks' "single continuous run" modus operandi. |
| Modus operandi | learnings → backup → detect → report → **pause for inline approval** → apply → verify → log → learnings, all in one continuous run. The run pauses in place at the report step and resumes in the same conversational continuum once the developer approves — never requires re-invocation. |
| Sibling skills (same modus operandi) | Docs Manager, mb-wikilinks |

## What it does — one line

Submits real, developer-authored file content into durable GBrain memory,
exclusively through the memory-governor's API — the single, correct governed
path. Never calls `gbrain remember` or `gbrain sync` directly.

## Hard prerequisites (Section 0 of SKILL.md)

| Rule | Detail |
|---|---|
| Target path must already be inside a registered GBrain source | Checked via `gbrain sources list` before anything else. If not found, the run STOPs and reports it — this skill never registers a new source itself (that's a separate, later step, not this skill's job). |
| Memory-governor API address | `http://127.0.0.1:8321` — confirmed live 2026-08-25, a real `uvicorn` process serving `app.main:app` inside WSL. Only reachable from inside that same WSL environment. See `memory-governor-config.md` § "Local installation & infrastructure" for the live-verified (2026-09-05) confirmation of this same address and process. |
| Credential selection | Never hardcoded. `manual_submission` when the developer invokes directly, themselves, right now. `pdlf_step_sync` when a PDLF step's own housekeeping invokes it automatically at step-end. If genuinely unclear which applies, the skill asks the developer rather than guessing. |
| Folder paths | Never submitted in one API call. Every real file inside is enumerated and run through the full detect/report/approve/apply cycle **individually** — never a shared or batched judgment. Standing content-scope exclusions apply (`obsolete`, `archive`, anything with `backup` in the name, dotfolders). |
| Confidence score | Never a fixed/default value — always genuinely formed per Step 3's concrete method (see `mb-submit-memory-reference.md`). |

## Confirmed real environment (from the one logged run, 2026-08-27)

| Item | Value |
|---|---|
| Governor app location | `~/memory-governor` (`.venv`) — matches `memory-governor-config.md`'s confirmed `/home/dev-p/memory-governor` |
| Governor API | `127.0.0.1:8321` |
| Governor's Postgres | `memory_governor` database, **WSL-native PostgreSQL 16** — explicitly distinct from the **Windows PostgreSQL 15** `pdlf` ledger database, and from a separately-documented `localhost` ambiguity (see `spec-postgres-ledger.md` in the PDLF docs repo) |
| Log/learnings location | `/mnt/c/mybizz/logs/mb-submit-memory/` — real files confirmed present: `2026-08-27T060743+0200.md` (a submission log) and `learnings.md` |

## Open item — carried from the 2026-08-27 log, not yet independently re-confirmed

The log recorded a naming drift: the gbrain source for the PDLF docs folder
was still `dev-makepdlf` while the governor's `owning_project` and the actual
folder name had already moved to `makepdlf-project-library`. Current
`gbrain sources list` output (checked 2026-09-05, this session) already shows
the source as `makepdlf-project-library` — consistent with this being
resolved — **but the governor's own `owning_project` field for related
candidates has not been independently re-checked against this**. Confirm
before treating this as fully closed.

## Do not

- Do not call `gbrain remember` or `gbrain sync` directly for anything meant to be submitted through this skill — defeats the governor's entire purpose.
- Do not submit a folder path in a single call, or share one confidence/contradiction judgment across multiple files.
- Do not assign a placeholder or default confidence score, ever.
- Do not proceed past a `needs_review`/`under_review` outcome on the developer's behalf, and do not resubmit with a different confidence value to try to force auto-promotion.
- Do not auto-trigger this skill — invocation is always explicit, always developer-given.
