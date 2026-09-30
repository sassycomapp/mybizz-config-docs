---
title: "gbrain-upgrade-checklist"
doc-id: "mb-47fa9b6f"
---
# GBrain upgrade checklist

Current version: 0.46.1.0.
Target: 0.59.18.0 (tested end to end in a sandbox). The newest release is 0.60.11.0 (link parser tested only).
Authority: David decides. No agent starts this. Decision made by David on 2026-09-30: upgrade to 0.59.18.0.
Sources: upstream CHANGELOG (v0.50.0.0), upstream `docs/guides/authorization-upgrade.md`, GBrain source code at tags v0.46.1.0 and v0.59.18.0.

## Rules

1. Upgrade only after David has recorded the decision and the reason in `gbrain-config.md` open item 1.
2. Never run `gbrain upgrade`, `gbrain self-upgrade`, `gbrain post-upgrade` or `gbrain apply-migrations --yes` for this upgrade. They can run setup phases that start autopilot.
3. Never install from the npm registry. The only source is `github.com/garrytan/gbrain`.
4. Never run old and new workers together.
5. Never start any service while an old queued job is neither authorized nor cancelled.
6. If any step prints something this list does not describe, stop and paste the output to Claude.
7. Keep backups and job previews private. They can contain secrets and job payloads.

## Facts that shape the steps

- Bun 1.3.11 or newer is required.
- The `gbrain` command is a link to `~/.bun/install/global/node_modules/gbrain/src/cli.ts` (seen 2026-09-30). The Git checkout at `/home/dev-p/gbrain` is clean at commit `b6250c43`. Step 3 finds out whether the global entry is a link to that checkout (variant B in step 10) or a separate Bun package (variant A).
- Old queued jobs become untrusted after the upgrade. Each one must be reviewed and authorized, or cancelled.
- Rollback means restoring the database and the application version together.
- Cross-repository links need version 0.51.8.0 or newer. A plain sync does not write them. `gbrain extract --stale` does.
- Compared in a sandbox: no command and no agent tool that exists in 0.46.1.0 is removed in 0.59.18.0. No tool loses a parameter or gains a required one. This covers names and inputs only. It does not cover behavior, permissions, queued jobs or database layout.
- Federating a source makes it part of default search. In 0.59.18.0 it also lets that source write cross-repository links.
- Read from GBrain's code (both versions): every `gbrain call` picks its source in this order: the `--source` flag, then the `GBRAIN_SOURCE` environment variable, then a `.gbrain-source` file, then the registered source whose folder contains the current folder, then the brain default set by `gbrain sources default`. `remember` writes the fact into that source. In 0.46.1.0, `recall` reads facts from that one source only. In 0.59.18.0, `recall` reads facts from that source and from every federated source, unless `source_id` is given.
- The governor's worker runs in `/home/dev-p/memory-governor`, which is the registered source `memory-governor-code`. Which source its writes really reach is not yet verified. Steps 6 and 19 check where the facts live.
- Behavior changes in the release notes that touch memory writes (not exhaustive): fact writes and page writes now resolve to the same target file (0.46.25.0); a forgotten fact stays forgotten after a reconcile, and a reconcile no longer deletes facts while the file on disk is newer than the database (0.48.5.0); `recall <entity> --since` now returns only the facts in that window (0.48.5.0); queued background jobs need authorization after the upgrade (0.50.0.0).

## The plan

### A. Decide and prepare

1. Record the decision and the reason.

[Write it in `C:\mybizz\mybizz-config-docs\gbrain\gbrain-config.md`, open item 1. Suggested wording: "Decision 2026-09-30 (David): upgrade GBrain from 0.46.1.0 to 0.59.18.0. Reason: cross-repository links need source-qualified wikilinks, which need version 0.51.8.0 or newer. This is a developer decision that overrides the standing rule to upgrade only on check failure."]
[Do not go on until this is done.]

2. Check Bun.

```
bun --version
```

[If the version is below 1.3.11, stop.]

3. Confirm the install type and record the current version.

```
ls -ld ~/.bun/install/global/node_modules/gbrain
readlink -f ~/.bun/install/global/node_modules/gbrain
cat ~/.bun/install/global/package.json
git -C /home/dev-p/gbrain rev-parse HEAD
git -C /home/dev-p/gbrain describe --tags --always
git -C /home/dev-p/gbrain status --short
git -C /home/dev-p/gbrain remote -v
git -C /home/dev-p/gbrain ls-remote --tags origin v0.59.18.0
```

[Variant B (linked checkout): the first line shows a link, `readlink` prints `/home/dev-p/gbrain`, and `package.json` contains `link:gbrain` or a path to the checkout.]
[Variant A (Bun package): the first line shows a plain folder, and `package.json` contains `github:garrytan/gbrain`.]
[Anything else: stop and paste the output to Claude.]
[The checkout must be clean, the remote must be `github.com/garrytan/gbrain`, and the tag line must end with `refs/tags/v0.59.18.0`.]
[Write the commit id here for rollback: ____________________]

4. Commit and push all eight document repositories.

[Use the status block and the commit block from Claude's message. A clean start avoids losing work.]

5. Save the health report from before.

```
mkdir -p ~/backups
gbrain doctor > ~/backups/doctor-before.txt 2>&1
```

6. Save a before-snapshot of the facts in every source.

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

7. Choose the release.

[Chosen tag: v0.59.18.0. Write a different tag here only if David decides so: ____________]

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

10. Install the release. Do not run any setup helper. Use only the variant that step 3 found.

Variant B, linked checkout:

```
git -C /home/dev-p/gbrain fetch --tags
git -C /home/dev-p/gbrain checkout v0.59.18.0
cd /home/dev-p/gbrain && bun install --ignore-scripts
gbrain --version
```

Variant A, Bun package:

```
bun install --global --ignore-scripts github:garrytan/gbrain#v0.59.18.0
gbrain --version
```

[The version must print 0.59.18.0. If it does not, stop.]
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

[If nothing is unfinished, go to step 12.]
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

[Checked against `gbrain sources list` on 2026-09-30: federated are `default`, `anvil-agent-references-code`, `data-mybizz-mgt`, `dev-root-hub`, `makepdlf-project-library`, `mb-3-cs-project-library`, `mybizz-config-docs`, `mybizz-os-docs`, `pdlf`.]
[Shown as `unset` (not part of default search): `mb-3-cs-code`, `mb4ecom-code`, `mb4ecom-project-library`, `mb5pdlf-code`, `mb5pdlf-project-library`, `memory-governor-code`. Leave them as they are unless David decides otherwise.]
[Only the source that holds a link needs to be federated for that link to reach another source. The target can be in any source.]
[After the upgrade, run the same list again. The states must be unchanged.]

```
gbrain sources list
```

16. Add one step to `C:\mybizz\scripts\sync-gbrain.sh`, after the loop and before the embed step.

```
echo "[2b/3] Collecting links across sources..."
if ! gbrain extract --stale; then
  echo "ERROR: gbrain extract --stale failed" >&2
  FAILED=$((FAILED + 1))
fi
```

[A plain sync does not write cross-repository links. This step does.]

17. Run the sync script once, then check health again.

```
setsid bash /mnt/c/mybizz/scripts/sync-gbrain.sh > /tmp/sync-output.txt 2>&1 &
gbrain doctor
```

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
[The governor test suite must report 304 passed and 0 failed. It writes test facts into the live brain and expires them itself, as designed.]
[Then run `/mb-submit-memory` on one small file, when David is ready. Approve it only if the report shows the same kind of related facts as before.]

19. Write the result in `gbrain-config.md` and in the GBrain version records.

[Update in the governor reference and configuration documents the statement that no GBrain mechanism scopes recall to a source. In 0.59.18.0 `recall` accepts an optional `source_id`.]
[Update the recorded GBrain version in the documents that state 0.46.1.0.]

### D. Rollback

Stop all services first. Then restore both together.

```
# variant B (linked checkout):
git -C /home/dev-p/gbrain checkout COMMIT
cd /home/dev-p/gbrain && bun install --ignore-scripts
# variant A (Bun package): use instead
# bun install --global --ignore-scripts github:garrytan/gbrain#v0.46.1.0
pg_restore --clean --if-exists -d gbrain ~/backups/gbrain-before-upgrade.dump
pg_restore --clean --if-exists -d memory_governor ~/backups/memory-governor-before-upgrade.dump
gbrain --version
```

[Replace COMMIT with the commit id from step 3.]
[An old worker must never run against the upgraded database.]

### E. Not yet decided

- A rehearsal on a copy of the database. It needs a scratch database. The commands are not written.
- Whether `recall` in 0.59.18.0 returns the same facts as before for the memory components. Steps 6 and 18 prove it. Not yet proven.
- Where the governed facts live. The per-source snapshot shows the largest set of facts in `memory-governor-code`. The worker sets only the brain default before each write, and the worker runs inside the memory-governor folder, which outranks the default. The governor documents say facts are brain-global. The code shows they are per source. Review after the upgrade.
- Never remove `memory-governor-code`, or any code source, before the facts stored in it are understood.
- Optional after the upgrade: the governor could pass `source_id` to `remember` instead of switching the global default source before every write. Not needed for the upgrade.
- The link change for all repositories: `[[[source-id:page-name]]](relative/path.md)`. This starts only after section C has passed.

### F. Records to update after the upgrade (upgrade done 2026-09-30)

Facts to record: GBrain 0.59.18.0 (tag v0.59.18.0, commit 045a6138), schema 169 (was 128), install = linked checkout `/home/dev-p/gbrain` in detached HEAD on the tag; branch `master` still holds the local diagnostic commit `b6250c43`, also on `pre-upgrade-backup`; backups in `~/backups`; new doctor baseline `~/backups/doctor-after-sync2.txt` (score 30/100, only FAIL: `cycle_freshness`).

1. `mybizz-config-docs\gbrain\gbrain-config.md`: version, schema, install type, upgrade date, the closed decision (open item 1) with its reason, federation states, sync script changes (`--no-pull`, `extract --stale`), doctor baseline, backup location.
2. `gbrain-reference.md`: upgrade procedure for this install type (git checkout of the tag, `bun install --ignore-scripts`, never `gbrain upgrade` or `self-upgrade`); cutover scripts and rollback; incidents: stale brain default `diag-mg-sec4` (detect: `gbrain config get sources.default`; fix: `gbrain sources default default`), and the `latest-stable` tag that a plain `git fetch --tags` refuses to overwrite.
3. `gbrain-explainer.md`: why the upgrade was made (source-qualified links across repositories), and how sources, federation and facts work.
4. `gbrain-exam-plan.md`, `gbrain-exam-report.md`, `gbrain-log.md`, `gbrain-learnings.md`: expected version, one log entry for the upgrade.
5. `memory-governor\memory-governor-config.md`, `-reference.md`, `-explainer.md`: facts are stored per source and are not brain-global; governed facts land in `memory-governor-code`, because the worker runs inside that folder and the folder outranks the brain default (proven 2026-09-30: 49 to 50); the worker leaves the brain default set to the last owning project; the test runner is not aware of the systemd services; verified 2026-09-30: services active, 422, 85 facts before and after; new optional `source_id` on `remember` and `recall`.
6. `mb-submit-memory\mb-submit-memory-config.md`, `-reference.md`, `-explainer.md`, `submit-memory-learnings.md`, `-log.md`: the recall gap is explained (governed facts sit in the source `memory-governor-code`, which is not federated); the governor project `mybizz-os-docs` was registered on 2026-09-30; proven end to end on 0.59.18.0.
7. `mybizz-os-docs\os-reference-docs\repo-organization.md`: row for `anvil-agent-references-code` with its note; `mb4ecom-project-library` and `mb5pdlf-project-library` federated; `anvil-agent-references-code` isolated; 15 sources; `-code` is only part of some source ids.
8. `mybizz-os-docs\os-reference-docs\memory-master-explainer.md`: version, per-source facts, federation, the recall gap.
9. `mybizz-os-docs\operating-procedures\daily-ops.md`: how to run the sync (`bash /mnt/c/mybizz/scripts/sync-gbrain.sh`), what it does, `--no-pull`, updating the Anvil clone by hand.
10. `mybizz-os-docs\os-reference-docs\frontmatter conventions.md`: `doc-id` is a permanent code `mb-xxxxxxxx`, added by the commit hook.
11. `mybizz-os-docs\os-reference-docs\wsl-path-references.md`: location of the scripts in `C:\mybizz\scripts`.

Still open, not caused by the upgrade: docmap references to `projects-config-register` and to the config YAML rule; the two ADRs that define `doc-id`; the retirement of the exam suites of `mb-doc-maintainer` and `mb-doc-auditor`; a documentation suite for `mb-doc-check`; the AGENTS.md pointer in `makepdlf`; the 114 older broken links; the code sources and Graphify; the link rollout.
