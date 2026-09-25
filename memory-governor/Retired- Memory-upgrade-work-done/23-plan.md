---
title: "23-plan"
doc-id: "23-plan"
---
# Work Package 23 — Resolve Remaining Open Items (Plan)

Plan mode made **zero changes**. Read-only inspection only. No secret value was
printed — only keyword presence, SET/ABSENT, and safe metadata.

---

## Part A — Security status

| Check | Result |
|---|---|
| 1. Supabase credential file absent | **ABSENT** (confirmed — deleted in WP22.2) |
| 2. Supabase account "closed" in local records | **Present** — `C:\mybizz\WIP\opencode-output\open-items.md:25` "Case closed - Supabase account closed" |
| 3. Config references Supabase / OpenRouter | **None** (gbrain config contains neither) |
| 4. `OPENROUTER_API_KEY` in environment | **ABSENT** |
| 5. GBrain uses local PostgreSQL + OpenAI | **Yes** — `engine: postgres`, `embedding_model: openai:text-embedding-3-large` |
| 6. External revocation | **Not required** (account closed by user) |

**Security decision: `closed`.** No external action needed; no secret was inspected or printed.

---

## Part B — [[agents|mb-3-cs]] (12-line diff)

- **Exact content:** a new `## Anvil Agent References (skills available via ~/.agents/skills/)`
  section listing the five Anvil skills (`server-code`, `client-forms`, `client-modules`,
  `data-models`, `anvil-yaml`) and resource paths under
  `/mnt/c/mybizz/anvil-agent-references/` (client/server stubs, type references, docs).
- **Purpose/provenance:** user-authored documentation of the Anvil Agent References skill
  source and paths.
- **Conflict with GBrain/Graphify/OpenCode guidance:** **none** (unrelated — Anvil skills).
- **Duplicates/complements:** **complements** (new guidance not previously recorded).
- **Proposed action:** **commit separately** (valid, coherent, no secrets; the
  `/mnt/c/mybizz/…` paths are documented resource paths, not secrets).
- **Proposed commit message:** `docs(agents): document Anvil Agent References skill paths`
- **Note:** explicitly deferred in WP22.3 — requires user confirmation before committing.

---

## Part C — `project-template`

- **Exact change (opencode.json, 1 line):** `"C:\\dev\\dev-mb-3-cs\\mb-3-cs\\**": "allow"` →
  `"C:\\dev\\dev-{SLUG}\\{SLUG}\\**": "allow"`.
- **Backup (`opencode.json.backup-2026-08-13`, 592 B):** no secret patterns; holds the pre-edit
  file (old hardcoded `mb-3-cs` path — machine-specific, not secret).
- **Valid template improvement?** **Yes** — replacing the concrete project path with `{SLUG}`.
- **Proposed action:** **commit the `opencode.json` improvement**; **exclude/delete** the
  `.backup` file (transient, stale machine path).
- **GBrain sync:** **none required** — `project-template` is not a registered GBrain source.

---

## Part D — global `~/.config/opencode/AGENTS.md`

- Lines 116–117: line 116 `docmap.md` (unchanged), line 117
  `C:\mybizz\config\projects-config-register.md`.
- Old `project-inventory.md` reference: **absent**.
- `projects-config-register.md`: **exists and readable** (2825 B).
- No unrelated change in the section; **no commit/push applicable** (not a Git repo).

---

## Part E — [[agents|mb-3-cs]] (Access Model + GRAPH MEMORY GUIDANCE)

- **Overlap:** `## Access Model` (GBrain semantic search available; Graphify installed, "Task
  3.7" ref) and the `GRAPH MEMORY GUIDANCE` managed block (Graphify = code structure, GBrain =
  decisions/history, 5-point authority order) both describe the two tools.
- **Contradictions:** **none** — consistent and complementary.
- **Access Model:** **retain as-is.** Minor optional note: its [[master-task-list|mybizz-OS]] Task 3.7
  cross-reference could drift; not worth editing now.
- **Managed block:** **remain local-only and managed** — `<!-- BEGIN/END GRAPH MEMORY GUIDANCE
  -->` delimiters mark a sync-gbrain-owned block; do not hand-edit.
- **Exact proposed edit:** **none required.**
- **Gitignored:** **yes** — [[agents|mb-3-cs]] (lowercase) is listed in `.gitignore` line 6.

---

## Part F — deferred deletion history

- `mb4ecom-project-library` and `mb5pdlf-project-library`: `AGENTS.md` + `opencode.json` are
  **uncommitted working-tree deletions** (` D`). They still exist in `HEAD`; reflog shows **no
  restore/undo**.
- **Assessment:** appears **deliberate cleanup** (consistent with the `{slug}-config.yaml`
  migration), left **uncommitted** because these are deferred repos.
- **Recommendation:** **leave pending user confirmation** — do not restore, commit, push, sync,
  or dream now (deferred repos).

---

## Part G — version and Graphify hook policy

1. GBrain **0.46.1.0**; available **0.46.6.0**.
2. Current policy: pinned; no upgrade unless a failed acceptance check requires it (none did).
3. Recommended review cadence: at the next scheduled maintenance phase.
4. Graphify hooks/merge-driver: **not installed**.
5. Current workflow requires hooks? **No** — MCP is read-only; artifact regenerated on demand.
6. Recommended policy: **keep hooks disabled; rebuild on demand and verify
   `built_at_commit == HEAD`.**

---

## Commit groups (only if approved — none mandatory)

| Group | Repo | Files | Message |
|---|---|---|---|
| 1 (optional) | `mb-3-cs-project-library` | [[agents|mb-3-cs]] | `docs(agents): document Anvil Agent References skill paths` |
| 2 (optional) | `project-template/dev-(SLUG)/(slug)-project-library` | `opencode.json` (exclude `.backup`) | `fix(template): generalize external-directory path to {SLUG}` |

## Items closed as "not required"

Supabase account (closed); credential file (deleted); global AGENTS.md reference (fixed);
dev-root links (fixed); Graphify hooks (intentionally disabled); deferred-source freshness
(intentional); GBrain upgrade (no acceptance failure); Graphify artifact rebuild (aligned to
HEAD).

## Items requiring user confirmation

1. Commit [[agents|mb-3-cs]] separately? (Part B)
2. Commit the `project-template/opencode.json` template fix (+ delete the `.backup`)? (Part C)
3. Deferred `AGENTS.md`/`opencode.json` deletions — leave as-is pending, or schedule cleanup
   when those repos re-enter scope? (Part F)

## Build-mode repair package needed?

**Optional only.** No repair is required — the environment is fully closed. If either/both
optional commits are approved, a single small Build package can execute them (exact-file commit
+ push; no GBrain sync for `project-template`, and a `--no-pull` sync only for
`mb-3-cs-project-library` if the [[agents|mb-3-cs]] change is committed).

## Final recommended policy

- **GBrain upgrades:** stay pinned at 0.46.1.0; upgrade only on an explicit maintenance
  decision, never reactively.
- **Graphify hooks:** remain disabled; on-demand rebuild with `built_at_commit == HEAD`
  verification.
- **Local-only integration:** `.opencode/skills/`, `graphify-out/`, and lowercase [[agents|mb-3-cs]]
  stay gitignored/local; the two managed blocks (`GRAPH MEMORY GUIDANCE`, gbrain search
  guidance) remain managed by their owning tools.
- **Deferred sources:** `mb4ecom-*`, `mb5pdlf-*`, `pdlf` remain registered and untouched; their
  staleness is intentional lifecycle state — no sync/dream/commit/push.

---

## Confirmation

Plan mode made **no changes** — read-only inspection only.
