---
title: "gbrain-upgrade-checklist"
doc-id: "mb-47fa9b6f"
updated: "2026-10-04"
---
# GBrain upgrade checklist

Procedure for upgrading GBrain on this computer. GBrain is a linked Git checkout at `/home/dev-p/gbrain`, so an upgrade is a checkout of a release tag plus a database migration. The target release is chosen in step 2.
Authority: David decides. No agent starts this.
Sources: the upstream CHANGELOG, upstream `docs/guides/authorization-upgrade.md`, and the GBrain source code at the old and the new tag.

## Rules

1. Upgrade only after David has recorded the decision and the reason in the open items of `gbrain-config.md`. Never on newness alone.
2. Never run `gbrain upgrade`, `gbrain self-upgrade`, `gbrain post-upgrade` or `gbrain apply-migrations --yes` for this upgrade. They can run setup phases that start autopilot.
3. Never install from the npm registry. The only source is `github.com/garrytan/gbrain`.
4. Never run old and new workers together.
5. Never start any service while an old queued job is neither authorized nor cancelled.
6. If any step prints something this list does not describe, stop and paste the output to Claude.
7. Keep backups and job previews private. They can contain secrets and job payloads.
8. Never remove `memory-governor-code`, or any code source, before the facts stored in it are understood.

## Facts that shape the steps

- Bun 1.3.11 or newer is required.
- The `gbrain` command is a link to `~/.bun/install/global/node_modules/gbrain/src/cli.ts`, and that global entry is a link to the Git checkout. The checkout stays in detached HEAD on the release tag in use.
- Old queued jobs become untrusted after an upgrade. Each one must be reviewed and authorized, or cancelled. No GBrain worker runs here, so the jobs that syncs create wait unprocessed; cancelling them before the upgrade is the normal case.
- Rollback means restoring the databases and the application version together.
- Links between repositories need version 0.51.8.0 or newer. A plain sync does not write them, and neither does `gbrain extract --stale`, because the sync has already marked its pages as done. Only the full read `gbrain extract links --source db` writes them; `sync-gbrain.sh` ends with it.
- Before upgrading, compare the old and the new release in a sandbox: the names and inputs of commands and agent tools. This does not cover behavior, permissions, queued jobs or database layout.
- Federating a source makes it part of default search and lets that source write links to other sources.
- Read from GBrain's code: every `gbrain call` picks its source in this order: the `--source` flag, then the `GBRAIN_SOURCE` environment variable, then a `.gbrain-source` file, then the registered source whose folder contains the current folder, then the brain default set by `gbrain sources default`. `remember` writes the fact into that source. `recall` reads the facts of that one source (`source_id` names another single source).
- The governor's worker names the owning project's own documentation source on every write (`GBRAIN_SOURCE` on the `gbrain remember` call), so governed facts land there. The worker also sets the brain default to the owning project before each write; a default that names a source that does not exist stops every sync.
- The page-name rule of `mb-doc-check` must equal GBrain's own. After every upgrade, `mb-doc-check.py slug-selftest` must report 0 differences.
- Behavior changes in the release notes that touch memory writes (not exhaustive): fact writes and page writes now resolve to the same target file (0.46.25.0); a forgotten fact stays forgotten after a reconcile, and a reconcile no longer deletes facts while the file on disk is newer than the database (0.48.5.0); `recall <entity> --since` now returns only the facts in that window (0.48.5.0); queued background jobs need authorization after the upgrade (0.50.0.0).

## The plan

### A. Decide and prepare

1. Record the decision and the reason.

[Write it in `C:\mybizz\mybizz-config-docs\gbrain\gbrain-config.md`, in the open items: the date, the old and the new version, and the reason.]
[Do not go on until this is done.]

2. Choose the release and write it down.

[Release tag chosen by David: v____________. Its commit id, from `git ls-remote` in step 4: ____________]
[In every terminal you use for this procedure, first run `TAG=` followed by the tag, for example `TAG=v0.60.25.0`. The commands below use `$TAG`.]

3. Check Bun.

```
bun --version
```

[If the version is below 1.3.11, stop.]

4. Confirm the install.

```
ls -ld ~/.bun/install/global/node_modules/gbrain
readlink -f ~/.bun/install/global/node_modules/gbrain
git -C /home/dev-p/gbrain rev-parse HEAD
git -C /home/dev-p/gbrain describe --tags --always
git -C /home/dev-p/gbrain status --short
git -C /home/dev-p/gbrain remote -v
git -C /home/dev-p/gbrain ls-remote --tags origin "$TAG"
```

[The first line shows a link, and `readlink` prints `/home/dev-p/gbrain`.]
[`status` must print nothing, the remote must be `github.com/garrytan/gbrain`, and the last line must end with `refs/tags/` and your tag.]
[Anything else: stop and paste the output to Claude.]
[Write the commit id of the tag in step 2. The rollback commit of the old version is saved by the stop-and-back-up step.]

5. Commit and push the documentation repositories listed in [[[mybizz-os-docs:operating-procedures/commit-all-repositories]]](C:/mybizz/mybizz-os-docs/operating-procedures/commit-all-repositories.md), so that nothing is lost.

```
bash /mnt/c/mybizz/scripts/commit-all.sh "Before the GBrain upgrade"
```

6. Save the health report from before.

```
mkdir -p ~/backups
gbrain doctor > ~/backups/doctor-before.txt 2>&1
```

7. Save a before-snapshot of the facts in every source.

[Why: `recall` reads facts from the source that the current folder or environment selects. A snapshot per source shows where the governed facts live and proves nothing is lost.]
[Run it from your home folder, so that the current folder does not select a source.]

```
mkdir -p ~/backups
cd ~
gbrain config get mcp_surface
gbrain sources list --json > ~/backups/sources-before.json
for s in $(gbrain sources list --json | jq -r '.sources[].id'); do GBRAIN_SOURCE=$s gbrain call recall '{"limit": 500}' > ~/backups/recall-before-$s.json 2>&1; done
wc -c ~/backups/recall-before-*.json
```

[The first command must print `verbs`.]
[Paste the byte counts to Claude. A source with a large count holds facts. Claude uses the counts to see where the governor's facts go.]

### B. Cutover

8. Stop everything that uses GBrain.

[Close every OpenCode session. Each one holds a GBrain process.]
[Stop the governor API first, so that no new candidate arrives. Wait 60 seconds, because the worker polls every 60 seconds and delivers what is already promoted. Then stop the worker.]

```
systemctl --user stop memory-governor-api
sleep 60
systemctl --user stop memory-governor-worker
systemctl --user status memory-governor-api memory-governor-worker --no-pager | grep -E 'Active|Loaded'
ps aux | grep -i -E 'gbrain|governor' | grep -v grep
```

[Both services must show inactive. The last command must print nothing. If it prints anything, stop.]
[Autopilot is off. Confirm that no dream cycle is running.]

9. Back up the stopped system.

```
pg_dump -Fc gbrain > ~/backups/gbrain-before-upgrade.dump
pg_dump -Fc memory_governor > ~/backups/memory-governor-before-upgrade.dump
tar czf ~/backups/dot-gbrain-before-upgrade.tgz -C ~ .gbrain
ls -l ~/backups
```

[The database names `gbrain` and `memory_governor` are assumptions. List the real names first with `psql -l`. Correct the two commands if they differ.]
[If pg_dump cannot connect, stop. Use the backup procedure in `gbrain-config.md`.]
[All three files must be listed and not empty.]

10. Install the release. Do not run any setup helper.

```
git -C /home/dev-p/gbrain fetch origin "refs/tags/$TAG:refs/tags/$TAG"
git -C /home/dev-p/gbrain rev-parse "$TAG^{commit}"
```

[A plain `git fetch --tags` returns an error when the floating tag `latest-stable` has moved. Fetch only the release tag.]
[The commit id printed must equal the one you wrote in step 2. If it differs, stop.]

```
git -C /home/dev-p/gbrain checkout "$TAG"
cd /home/dev-p/gbrain && bun install --ignore-scripts
gbrain --version
```

[The version printed must be the one you chose. If it does not, stop and go to Rollback.]
[Never use `gbrain upgrade --swap-only` for this. It can still run install scripts.]

11. Apply the database changes only.

```
gbrain apply-migrations --force-schema --yes
```

[If it says that active historical work blocks the migration, stop. Go to Rollback.]

12. Review the old queued jobs.

```
gbrain jobs list --json
```

[If nothing is unfinished, go to step 13.]
[For each unfinished job, either cancel it, or preview it and authorize it.]

```
gbrain jobs authorize-legacy --ids ID1,ID2 --json
gbrain jobs authorize-legacy --ids ID1,ID2 --expect DIGEST --yes --json
```

[Replace ID1,ID2 with the job ids. Replace DIGEST with the digest that the preview prints. Read the preview before you authorize.]

13. Check health.

```
gbrain doctor > ~/backups/doctor-after.txt 2>&1
diff ~/backups/doctor-before.txt ~/backups/doctor-after.txt | head -60
```

[Paste the difference to Claude before you go on.]

14. Start the services again: the memory governor first, then OpenCode.

```
systemctl --user start memory-governor-api memory-governor-worker
systemctl --user status memory-governor-api memory-governor-worker --no-pager | grep -E 'Active|Loaded'
ss -tlnp | grep 8321
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8321/memory/review-queue
```

[Both services must show active. Port 8321 must be held by one process. The curl command must print 422.]
[The worker unit carries the `~/.bun/bin` path line. Without it every delivery fails. Confirm that the unit file still contains it.]

### C. After the upgrade

15. Federation state.

[Run the list again. The states must be unchanged from before the upgrade. The expected states are in `repo-organization.md`.]
[Only the source that holds a link needs to be federated for that link to reach another source. The target can be in any source.]

```
gbrain sources list
```

16. Check that the sync script still ends with the full link read.

```
grep -n "extract links --source db" /mnt/c/mybizz/scripts/sync-gbrain.sh
```

[It must print one line. If it prints nothing, the script is wrong: links between repositories will stop being written.]

17. Run the sync, then check health, the page-name rule and the links between repositories.

```
setsid bash /mnt/c/mybizz/scripts/sync-gbrain.sh > /tmp/sync-output.txt 2>&1 &
gbrain doctor
python3 /mnt/c/mybizz/scripts/mb-doc-check.py slug-selftest
python3 /mnt/c/mybizz/scripts/mb-doc-check.py sources-check
GBRAIN_SOURCE=mybizz-os-docs gbrain call get_links '{"slug":"operating-procedures/daily-ops"}' | grep -c '"to_source_id": "mybizz-config-docs"'
```

[Wait for the sync to finish first (it can take several minutes). `slug-selftest` must report 0 differences, `sources-check` must say "everything matches", and the last command must print a number above 0.]

18. Prove that the memory components still work.

```
cd ~
gbrain config get mcp_surface
gbrain sources list --json > ~/backups/sources-after.json
for s in $(gbrain sources list --json | jq -r '.sources[].id'); do GBRAIN_SOURCE=$s gbrain call recall '{"limit": 500}' > ~/backups/recall-after-$s.json 2>&1; done
for s in $(gbrain sources list --json | jq -r '.sources[].id'); do echo "== $s"; diff ~/backups/recall-before-$s.json ~/backups/recall-after-$s.json | head -10; done
/home/dev-p/memory-governor/scripts/run-tests-deterministic.sh
```

[`mcp_surface` must still print `verbs`.]
[The differences may show only new facts. A fact that disappeared is a failure. Stop and paste it to Claude.]
[The governor test suite must report the same passed count as the last run and 0 failed. It writes test facts into the live brain and expires them itself, as designed.]
[Then run `/mb-submit-memory` on one small file, when David is ready. Approve it only if the report shows the same kind of related facts as before.]

19. Update the records.

[The documents that state the GBrain version or describe behavior that changed: `gbrain-config.md` (version, schema, install, date, the resolved decision, backups), `gbrain-reference.md` and `gbrain-explainer.md` (the version line and any changed behavior), the GBrain dream cycle documents (parent system row), the memory governor and `mb-submit-memory` documents, `memory-master-explainer.md`, and `repo-organization.md` if the sources changed. The four GBrain exam files are rewritten by the next exam run.]
[Commit with `commit-all.sh`.]

### D. Rollback

Stop all services first. Then restore both together.

```
git -C /home/dev-p/gbrain checkout COMMIT
cd /home/dev-p/gbrain && bun install --ignore-scripts
pg_restore --clean --if-exists -d gbrain ~/backups/gbrain-before-upgrade.dump
pg_restore --clean --if-exists -d memory_governor ~/backups/memory-governor-before-upgrade.dump
gbrain --version
```

[Replace COMMIT with the commit id of the old version, saved in `~/backups/rollback-commit.txt` or noted before the upgrade.]
[An old worker must never run against the upgraded database.]

### E. Tested shortcuts

The cutover scripts in `C:\mybizz\scripts\` run steps 8 to 14 and the rollback with checks at every stage: `cutover-block1.sh` (record, stop, back up), `cutover-block2.sh` (install and migrate), `cutover-block3.sh` (start and prove), `cutover-rollback.sh`. They were written for one specific upgrade. Before reuse, change the tag, the expected commit and the version text at the top of `cutover-block2.sh`, and read the rollback script, which returns to the saved commit and prints the version it expects.
