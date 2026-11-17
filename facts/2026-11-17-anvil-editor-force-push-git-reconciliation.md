---
title: "2026-11-17-anvil-editor-force-push-git-reconciliation"
doc-id: "mb-f6a2984f"
updated: "2026-11-17"
---
# Anvil editor git commits force-push: reconcile a divergent pull

The Anvil editor's own commit force-pushes rewritten history to the app repository. After work done in the Anvil editor, a plain `git pull` in the app repository fails with "divergent branches" because Anvil's force update replaced the remote's commits. When the local branch holds no unique commits (its head was the replaced commit) and the working tree has only uncommitted changes, reconcile with exactly: `git stash push -m <label> <changed tracked files>`, then `git reset --hard origin/master`, then `git stash pop`. Untracked files are untouched by the reset; the stash preserves tracked modifications across it. Never reset while local holds unique commits — check `git log --oneline HEAD..origin/master` and `git log --oneline origin/master..HEAD` first. Set by the Step 17 close-out of mb-3-cs run app1, 2026-11-17.
