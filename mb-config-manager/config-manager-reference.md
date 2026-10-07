---
title: "config-manager-reference"
doc-id: "mb-8ddcefac"
updated: "2026-10-07"
---
# mb-config-manager — Reference

Agent-facing procedures for running the config-management system. Architecture and
file model: [[[mybizz-config-docs:mb-config-manager/config-manager-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-explainer.md). Routing table:
[[[mybizz-config-docs:mb-config-manager/config-manager-register|Register: Managed Systems]]](C:/mybizz/mybizz-config-docs/mb-config-manager/config-manager-register.md).

## Invocation

| Form | Meaning |
|---|---|
| `/mb-config-manager (all)` | Developer-initiated system-wide health scan — every Installed system |
| `/mb-config-manager (system)` | Targeted single-system exam (e.g. `/mb-config-manager (postgresql)`) — used when the developer suspects a problem with a particular system, or an agent has reported config problems on one |

Both forms run the same cycle; the form determines scope only.

## Running an exam (one cycle — plan-driven)

0. **Self-validation (step 0)** — verify own functional consistency: register rows
   ↔ installed skills ↔ suite files agree; each installed skill's text below its
   frontmatter is identical to its source's (compared by sha256, read via the
   approved glob form `mb-config-*/SKILL.md`), and the row's body hash is
   re-recorded. Inconsistency = log + report, never self-heal.
1. **Synthesize the exam-plan** (per the agent MO): read config spec + last report
   (deferred **and erred** items) + log + learnings → write `{system}-exam-plan.md`
   (header: date, Tier-3 unlock state, bundled developer-run requests;
   carried-forward items; erred-last-run items; log-driven items; learnings-driven
   items; standing checks per the skill's inventory + expected-value sources;
   report requirements; gate protocol). The file is live; its contents are
   transient — rewritten each cycle.
2. Run the target system's exam skill **with the plan in hand** (`(all)` = every
   Installed system). Detection is autonomous — no questions until the gate.
3. Each system skill writes its current exam report (`{system}-exam-report.md` —
   one file, overwritten per run; no history).
4. Aggregate findings; classify: `DOWN` / `UNHEALTHY` / `DRIFT` / `GAP`.
5. Present the gate: per finding — evidence, class, recommended repair (allowlist
   only), rollback plan, risk. Developer: approve / reject / defer.
6. Apply approved heals one at a time: capture pre-state → apply → verify → next.
   Failed verify = rollback + halt the run.
7. Re-exam the touched systems; report the outcome.
8. **Record**: append one run row to `{system}-log.md` (format below); file new
   learnings; prune absorbed log/learning entries (absorption = written into plan
   items, skill rows, or governance flags).

## Installing a system module (skill)

1. Build the exam skill draft as `{system}/{system}-skill.md` in the system folder.
2. Verify the exam once from the draft (detection-only) — the skill must be proven
   before it gets a runtime identity.
3. Install by **copy, never move** (canonical source stays in the repo). The
   source is a document, with frontmatter `title`, `doc-id` and `updated`; the
   installed `SKILL.md` needs frontmatter `name` and `description` so OpenCode
   can load it. So install copies only the source's text below its frontmatter
   into `~/.config/opencode/skills/<skill-name>/SKILL.md`, below the installed
   frontmatter:
   - First install: write the installed frontmatter — `name: <skill-name>` and a
     `description` stating what the skill exams and when to use it.
   - Re-install: keep the installed frontmatter exactly as it is; replace only the
     text below it.
   One skill per completion — never a batch migration.
4. Record the install date and the first 16 hex of the sha256 of the text below
   the frontmatter in the register row. Source and installed copy have the same
   body hash when they are in sync; step 0 compares them every cycle.
5. Write access outside the current project goes through the normal grant path:
   `mg-grant --path <folder> --count N`. Exceptions only when genuinely unavoidable
   (e.g. cupcake-token guards) — then hand the developer the exact commands.
6. Flip the register state (below).

## Register state-flip

- **Draft-complete → `Installed`:** only after (a) skill draft verified once from
  the suite folder, (b) file **copied** to
  `~/.config/opencode/skills/<name>/SKILL.md` below its installed frontmatter
  (source stays), (c) body hash + install date recorded in the register row. Then update the row: state `Installed`.
- The register is current state only — old states are overwritten, never
  historized.

## Report discipline (write-then-replace)

- Compose the full new report, verify it well-formed, *then* replace
  `{system}-exam-report.md`. A failed, interrupted, or incomplete run never
  touches the previous report — it is logged as errored with findings-so-far in
  the run row.
- The report is written before any pruning happens.

## Gate durability

- Every gate outcome is recorded per-item (item id → approve/reject/defer) in the
  log run-row's `disposition` field.
- Unresolved defers become the next plan's carried-forward items.
- Session death mid-gate: recovery = read log + last report; never re-ask
  silently, never silently skip.

## Developer-returned results (evidence format)

- Results returned by the developer for developer-run checks are recorded
  **verbatim**, tagged `developer-verified`, with the exact commands supplied
  listed alongside — so the next run can re-request precisely.

## Tier-3 standing authorizations

- A Tier-3 item may be authorized **standing** (all future runs) only as a
  configuration item in `{system}-config.md`, added only after the developer
  approves it at the gate.
- The exam-plan header reads the standing authorization and may **narrow** it for
  a run, never widen.

## First-run bootstrap

- A system's first exam run may have no report, no log, no learnings — expected,
  not silence: synthesize the plan from the config spec alone, log a `GAP`
  finding for each missing suite file, proceed.

## Log run-row format (one row per exam run)

| field | content |
|---|---|
| date | run date |
| run | system + invocation form (e.g. `postgresql (single)`) |
| tiers | tiers executed (e.g. `0–2`) |
| verdict | `DOWN` / `UNHEALTHY` / `HEALTHY` / `HEALTHY+FLAGS` |
| findings | count + classes |
| dev-requests | what was requested developer-run |
| disposition | heals applied / flags routed / deferred |

## Learnings procedure

- One entry per pattern in the system's `{system}-learnings.md`:
  the pattern + the right action + its destination. No narrative, no history.
- Graduation, dual track: into the **skill** → agent-applied directly, then
  re-installed; into **config / reference / explainer** → proposed at the gate,
  applied only after the developer approves it.
- On graduation, **delete the entry immediately** — verification of the graduated
  item belongs to the next exam-plan (as a carried-forward item), not to the
  learnings file. Entries never accumulate.

## Log procedure

- One run row per exam run (format above).
- Free rows for notable events between runs: crashes, incidents, upgrades,
  error reports, significant guard denials — problems the system experienced
  **and problems the system caused**. Appended at observation time by whichever
  session witnesses the event — not only during exams; never leave an incident
  unlogged because no exam is running. The config-manager additionally sweeps
  for unlogged notable events at plan-synthesis time.
- Pruned under the absorption rule: an entry goes once its content is absorbed
  (into a learning, a skill row, a plan item, or a governance flag) and is
  resolved. The log holds recent + unresolved signal, nothing more.

## Credential rule

Credentials are referenced by variable name only — never printed, never copied into
reports, outputs, or learning entries.

## Healed vs flagged

- System config artifacts (`{system}-config.md` spec docs): **flagged, not healed** —
  drift is raised as a gate item with a proposed correction, applied only after
  the developer approves it and committed through close-out
  (close-out-process).
- Live system state: healed through the gate, allowlist repairs only.

## Guard denials

A guard denial is honored absolutely — never retried through an alternate path,
never token-dodged (proven live: the cupcake exec guard denies even non-execution
commands whose argument text contains the token `cupcake`). A denied check becomes
a developer-run request in the run's bundled request list, and the class is
recorded as a learning if new.

## Build status

- Every system the register lists as `Installed` has completed a formal plan-driven exam run. The register is the authority for what runs.
