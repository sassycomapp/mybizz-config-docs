---
title: "13-plan"
doc-id: "mb-e628633b"
updated: "2026-10-01"
---
# Work Package 13 — Graphify Git Hook Evaluation

Read-only evaluation of Graphify Git hook behaviour. No hook installed, no
files modified, no GBrain change, no AGENTS.md/agents.md change, no
`.gitignore` change, no packages installed, no graph rebuild, no cluster-only,
no commit/push, no sync-gbrain.

---

## Current state (verified)

- `graphify hook status` → `post-commit: not installed`, `post-checkout: not
  installed`, `merge driver: not registered`.
- `.git/hooks/` contains **only `.sample` files** — no active hooks of any kind.
- `git config --local --list` → minimal (repositoryformat, filemode, bare,
  logallrefupdates, ignorecase, remote origin, branch.master). **No
  `core.hooksPath`** (unset local and global). **No merge-driver config.**
- **No `.gitattributes`** exists.
- Graphify version 0.9.40, source at
  `/home/dev-p/.local/lib/python3.12/site-packages/graphify/hooks.py` (read in
  full).

## 1. Exact hook behaviour

`graphify hook install` performs **three** actions, unconditionally (no flag to
split them):

1. **`post-commit` hook** — appended to `.git/hooks/post-commit`, delimited by
   `# graphify-hook-start` / `# graphify-hook-end`. On commit: computes
   `git diff --name-only HEAD~1 HEAD`; skips if empty, skips if only
   `graphify-out/` changed, skips during rebase/merge/cherry-pick, skips in
   linked worktrees, honours `GRAPHIFY_SKIP_HOOK=1`; then **launches a detached
   background rebuild** (`_rebuild_code` with `changed_paths`) and returns
   immediately.
2. **`post-checkout` hook** — delimited by `# graphify-checkout-hook-start` /
   `-end`. Runs **only on branch switches** (not file checkouts), only if
   `graphify-out/` exists; same skips; launches a detached **full** rebuild (no
   `changed_paths`).
3. **Graph.json union merge driver** — runs `git config merge.graphify.name`
   and `merge.graphify.driver` (pinned-python `-m graphify merge-driver %O %A
   %B`), and **appends `graphify-out/graph.json merge=graphify` to
   `.gitattributes`** (creating the file if absent).

## 2. Files and Git configuration it would modify

| Target | Change |
|---|---|
| `.git/hooks/post-commit` | created (or appended) with graphify block |
| `.git/hooks/post-checkout` | created (or appended) with graphify block |
| `.gitattributes` | **created** (new tracked file) with `graphify-out/graph.json merge=graphify` |
| `.git/config` (local) | adds `merge.graphify.name` + `merge.graphify.driver` |
| `graphify-out/…` (at rebuild time) | `graph.json`, `graph.html`, `GRAPH_REPORT.md`, `manifest.json`, `.graphify_analysis.json`, `.graphify_labels.json`, `.graphify_labels.json.sig`, `.graphify_build.json` (+ `memory/reflections/LESSONS.md` best-effort) |
| `~/.cache/graphify-rebuild.log` | detached rebuild log (outside repo) |

It does **not** touch source files, `AGENTS.md`/mb-3-cs, `.gitignore`,
GBrain, or `opencode.json`.

## 3. Are existing hooks preserved?

**Yes.** `_install_hook` appends to an existing hook (never overwrites) using
start/end markers; uninstall strips only the marker-delimited section and
deletes the file only if nothing else remains. Today there is nothing to
preserve — the repo has no active hooks, only `.sample` files.

## 4. Graphify command executed by the hook

Detached `python -c …` running `graphify.watch._rebuild_code` — i.e. **AST
code-only re-extraction + build + deterministic clustering + report + HTML**,
**no LLM**. It is the `update --code-only` path, **not** `extract`
(semantic/LLM), **not** `cluster-only`. For `post-commit` it passes the changed
file list; for `post-checkout` it does a full rebuild. It re-applies the
persisted `gitignore`/exclude flags from `.graphify_build.json`.

## 5. Performance and failure risks

- **Performance:** non-blocking by design — the rebuild is detached
  (`start_new_session`/Windows detached flags), so `git commit`/`checkout`
  return immediately. The code-only rebuild for ~180 source files / 537 nodes
  is seconds; a 600 s `SIGALRM`/thread watchdog caps runaway rebuilds.
  `PYTHONHASHSEED=0` is pinned for deterministic clustering.
- **Failure risks:**
  - If graphify's Python can't be located, the hook prints to stderr and
    `exit 0` — commits never blocked by a missing interpreter.
  - Rebuild failures go to the log, not to git.
  - **Merge driver is dead weight here:** `graphify-out/graph.json` is
    gitignored and never tracked, so the driver can never fire — yet installing
    it still creates a **tracked `.gitattributes`** and local config churn.
  - **Scope nuance:** `.graphify_build.json` is `{"gitignore": false}`, so the
    hook rebuild respects `.graphifyignore` but **not** `.gitignore` —
    gitignored *code* trees (e.g. `tests/`) remain graphed (they already are),
    and non-`.graphifyignore`d gitignored files are scanned (though only
    AST-extractable code yields nodes).

## 6. Secrets / ignored content

- **Secrets:** the hook only rewrites the local, **gitignored** `graphify-out/`
  graph (and a local log). It never commits, pushes, or publishes anything.
  WP12 confirmed the current graph holds no secrets; the hook adds no new
  exposure channel. Risk is limited to whatever is already in the local working
  tree.
- **Ignored content:** not added to Git (graph stays gitignored); the
  merge-driver/`.gitattributes` is the only *tracked* surface added, and it
  references a gitignored path.

## 7. Rollback method

- `graphify hook uninstall` — removes both hook blocks (preserving any other
  hook content), unregisters the merge driver (`git config --unset
  merge.graphify.name` / `…driver`), and removes the `graph.json merge=graphify`
  line from `.gitattributes` (deleting the file if left empty).
- Manual equivalent: delete the two marker-delimited blocks from
  `.git/hooks/post-commit` and `post-checkout`; run the two `git config --unset`
  commands; remove the one `.gitattributes` line (or the file).

## 8. Recommendation: Do not install (at this stage)

Rationale:

1. The useful half (auto-fresh provenance) is bundled with a useless half — a
   merge driver + new tracked `.gitattributes` for a graph that is gitignored
   and never merged. There is no `--no-merge-driver` flag to isolate it.
2. The repo is **production-adjacent** and this whole Graphify setup has been
   deliberately kept **local-only and gitignored** (WP11/WP12). Installing would
   add a tracked `.gitattributes`, local git config keys, and a detached
   process on every commit/checkout — surface area with no current requirement.
3. Provenance freshness is already achievable on demand with a single manual
   command (`graphify update .`, API-free), which WP12 flagged as *optional*
   only.

**Next Build-mode action: none.** If fresh provenance is ever wanted, run
`graphify update .` after code changes manually — no hook, no `.gitattributes`,
no merge-driver churn. If you later want automatic rebuilds *without* the merge
driver, that would require a Graphify feature change (split `hook install`) and
is out of scope.

## Next steps

- **Build →** none (recommendation is not to install).
- **Plan/developer →** optional manual `graphify update .` after code changes.
- Housekeeping (asked separately): commit/push approval; GBrain sync approval.
