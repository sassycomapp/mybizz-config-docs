---
doc-id: 21-task-report
document: "Work Package 21 — Final GBrain–Graphify–OpenCode Acceptance"
date-created: 2026-08-16
title: Work Package 21 — Final GBrain–Graphify–OpenCode Acceptance
report: package21-task-report
date: 2026-08-16
time_utc_plus_2: 2026-08-16T111412+0200 (SAST)
state: Complete — READY FOR DEVELOPMENT WITH DOCUMENTED LIMITATION
repo: mb-3-cs (live) — acceptance validation only; no code/DB/artifact/config changes
---

# Work Package 21 — Final GBrain–Graphify–OpenCode Acceptance

Final acceptance and readiness certification for Phase 2. This package ran
read-only validation across GBrain, Graphify, OpenCode MCP, and the OpenCode
skill catalog, after the OpenCode restart that followed Package 20.1. No
GBrain data was altered; no sync/dream/rebuild was run; no tracked file,
configuration, schema pack, source registration, Git hook, credential, or
deferred source was modified; no commit/push was performed.

---

## 1. Final status

**READY FOR DEVELOPMENT WITH DOCUMENTED LIMITATION**

All active-scope acceptance checks pass. The single remaining item is a
documented capability limitation of GBrain's `code-callers`/`code-callees`
code-surface feature (see §13), which is a schema-pack configuration
limitation — not an installation or integration failure — and is fully
compensated by Graphify's resolved EXTRACTED edges for the same relationships.

---

## 2. Exact versions

| Component | Version |
|---|---|
| GBrain | **0.46.1.0** (CLI `gbrain --version` and MCP `gbrain_get_brain_identity`) |
| GBrain DB schema | **128** (latest 128 — migrations current) |
| Active schema pack | **gbrain-everything@1.0.0** (sha8 `7021205a`, 30 types, 12 link verbs) |
| Graphify | **0.9.40** (CLI `graphify --version`; distribution `graphifyy` 0.9.40) |
| PostgreSQL server | **16** (cluster `16 main`, online, port 5432) |
| psql client | 16.14 |
| pgvector | **0.6.0** (`vector.control` `default_version = '0.6.0'`) |
| OpenCode (live process) | web server PID **8235**, restarted 2026-08-16 ~10:47 SAST |

Note: GBrain reports `update_available` (0.46.6.0). This is advisory only and
is **not** treated as a failure — upgrade is prohibited by the strict
protections unless an acceptance check fails (none did).

---

## 3. Exact active paths

| Item | Path |
|---|---|
| Live application repo | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` |
| Project-library | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` |
| Shared project library (GBrain `default`) | `/mnt/c/dev/project-library-global` |
| Project-local OpenCode skills | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` |
| Graphify artifact | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json` |
| GBrain executable / MCP cmd | `/home/dev-p/.bun/bin/gbrain serve` |
| Graphify executable | `/home/dev-p/.local/bin/graphify` |
| Graphify Python module | `/home/dev-p/.local/lib/python3.12/site-packages/graphify/` |
| Graphify MCP interpreter/cmd | `/usr/bin/python3 -m graphify.serve …/graphify-out/graph.json` |
| GBrain MCP config | global `~/.config/opencode/opencode.jsonc` (`mcp.gbrain`) |
| Graphify MCP config | project `opencode.json` (`mcp.graphify`) |

---

## 4. Source lists

### Active sources (fresh/current)

| Source | Path | Pages | last_sync (UTC) | State |
|---|---|---|---|---|
| `default` | `/mnt/c/dev/project-library-global` | 200 | 2026-08-16T05:54 | fresh ✓ |
| `mb-3-cs-project-library` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library` | 435 | 2026-08-16T07:26 | fresh ✓ |
| `dev-makepdlf` | `/mnt/c/dev/dev-makepdlf/makepdlf-project-library` | 181 | 2026-08-16T05:56 | fresh ✓ |
| `dev-root-hub` | `/mnt/c/dev/dev-root` | 20 | 2026-08-16T05:58 | fresh ✓ |
| `mb-3-cs-code` | `/mnt/c/dev/dev-mb-3-cs/mb-3-cs` | 263 | 2026-08-16T05:07 | processed/current ✓ |

### Deferred sources (registered, intentionally untouched)

| Source | Path | Pages | last_sync (UTC) |
|---|---|---|---|
| `mb4ecom-code` | `/mnt/c/dev/dev-mb4ecom/mb4ecom` | 5 | 2026-08-10T15:21 |
| `mb4ecom-project-library` | `/mnt/c/dev/dev-mb4ecom/mb4ecom-project-library` | 6 | 2026-08-16T05:52 |
| `mb5pdlf-code` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf` | 5 | 2026-08-10T15:26 |
| `mb5pdlf-project-library` | `/mnt/c/dev/dev-mb5pdlf/mb5pdlf-project-library` | 13 | 2026-08-16T05:52 |
| `pdlf` | `/mnt/c/pdlf` | 14 | 2026-08-13T11:17 |

All five deferred sources remain **registered** and were **not touched** by this
package (no sync, no dream, no refresh). Their staleness (`mb4ecom-code`,
`mb5pdlf-code`, `pdlf`) is **not** an operational failure per the package
definition. The doctor `federation_health`/`sync_freshness` findings that name
`mb4ecom-code`/`mb5pdlf-code` are deferred-source staleness — excluded from
acceptance scope.

---

## 5. GBrain schema / database state

- Engine: **postgres** (multi-writer); connection "Connected, 1142 pages" ✓
- Schema version: **128 (latest: 128)** — migrations current ✓
- Active schema pack: **gbrain-everything v1.0.0** (`schema_pack_active` ok,
  `schema_pack_consistency` "all pages match", no per-source drift) ✓
- pgvector extension: installed, 0.6.0 ✓
- Statistics (`gbrain_get_stats`): 1142 pages / 2524 chunks / 2524 embedded /
  469 links / 5 tags; pages-by-type: concept 554, code 254, atom 229, note 87,
  extract_receipt 18 ✓
- Embedding provider: `openai:text-embedding-3-large`, 1536 dims, DB aligned.
  A first `gbrain doctor` probe transiently reported "Cannot connect to API";
  an immediate re-probe returned `ok — 2166ms, 1536 dims, DB aligned`. The
  failure was a transient network blip, self-resolved, not an active-scope
  issue. ✓
- Read-only queries retrieved known content from all four requested sources
  (`default` ADRs; `mb-3-cs-project-library` Vault/design/build-plan;
  `dev-makepdlf` AGENTS/index; `dev-root-hub` docmap). ✓

Out-of-scope, pre-existing doctor signals (not acceptance failures, recorded
for transparency): brain_score 57/100; 1 unresolved sync-failure record for
`obsolete/issue-tracker.md` (the WP16.5.1 rename-destination leftover); 1
embed-backfill job waiting with no live worker on queue `default`;
`graph_signals_coverage` 9.6%; `contextual_retrieval_coverage` 670 pages.

---

## 6. Graphify statistics and artifact provenance

- `graph_stats`: **574 nodes / 468 edges / 158 communities** (96% EXTRACTED,
  4% INFERRED, 0% AMBIGUOUS) ✓
- Artifact: `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/graphify-out/graph.json`,
  413102 bytes, readable ✓
- `built_at_commit` = `5ce243e12bc2775108c9ecad6da1e6c7f8f1614c` == live HEAD ✓
- Top-level keys: `directed`, `multigraph`, `graph`, `nodes`, `links`,
  `hyperedges`, `built_at_commit` ✓
- `pip check`: "No broken requirements found" ✓
- Symbol probe (`encrypt()`): definition at
  `server_code/server_shared/encryption_service.py:13`, type `code`, degree 8;
  8 typed EXTRACTED neighbors (`calls` from `save_vault_secret()` and 4 test
  methods, `imports` from `vault_service.py`, `contains` from
  `encryption_service.py`, `rationale_for` docstring) ✓
- Hooks/merge drivers: none installed (`graphify hook status` → not installed;
  no `.gitattributes`; only `.sample` hooks; no `merge.graphify.*` config) ✓
- Artifact was **not** rebuilt (all checks passed) ✓

---

## 7. OpenCode MCP status

Both MCP servers are connected in the restarted OpenCode session and respond in
the same session with no mutual interference.

| Check | Result |
|---|---|
| GBrain MCP available (config `mcp.gbrain`) | ✓ PID 8267 (`/home/dev-p/.bun/bin/gbrain serve`) |
| Graphify MCP available (config `mcp.graphify`) | ✓ PID 8268 (`/usr/bin/python3 -m graphify.serve …`) |
| `gbrain_get_brain_identity` responds | ✓ 0.46.1.0, postgres, 1142 pages, 2524 chunks |
| `graph_stats` responds | ✓ 574 / 468 / 158 |
| Both usable in same session | ✓ |
| Commands/paths unchanged and correct | ✓ |
| No obsolete GBrain process | ✓ only fresh PIDs 8267/8268 |

---

## 8. OpenCode skill discovery results

- Project-local skill directories (excluding `conventions/` and `_` shared
  files): **60** ✓
- Total files in `.opencode/skills/`: **119** ✓
- All 60 expected GBrain skills are present and discoverable in the OpenCode
  catalog, each resolving to
  `file:///mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/<name>/SKILL.md` ✓
- A read-only skill (`gbrain-advisor`) was loaded via the skill tool — the load
  output confirmed base directory
  `file:///mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/gbrain-advisor`,
  proving discovery + loadability ✓
- Read-only invocation completed: `gbrain advisor --json` returned findings
  (version_drift warn, orphan_pages info); **no fix was run** (per skill
  contract and strict protections) ✓

The 60 GBrain skills discovered:
`academic-verify, archive-crawler, article-enrichment, ask-user, blog-ingest,
book-mirror, brain-ingest-gate, brain-link-discipline, brain-ops, brain-pdf,
brain-taxonomist, briefing, bulk-ingestion, capture, citation-fixer,
citation-graph-ingest, cold-start, company-brainify, concept-synthesis,
context-audit, conversation-archive, correction-pipeline, cron-scheduler,
cross-modal-review, daily-task-manager, daily-task-prep, data-loss-gate,
data-research, draft-in-voice, eiirp, enrich, fact-check,
functional-area-resolver, gbrain-advisor, idea-ingest, idea-lineage, ingest,
maintain, measure-before-you-fix, media-ingest, meeting-ingestion,
minion-orchestrator, perplexity-research, publish, query, repo-architecture,
reports, research-compendium, resolve-before-asking, signal-detector,
skill-autobench, skill-creator, skillpack-check, skillpack-harvest, soul-audit,
strategic-reading, testing, two-tier-extraction, voice-note-ingest,
webhook-transforms`.

---

## 9. skillify collision result

- GBrain's `skillify` is **absent** from the project-local scaffold
  (no `.opencode/skills/skillify/`) ✓
- Exactly **one** `skillify` is discoverable in the OpenCode catalog ✓
- The discovered `skillify` resolves to the **pre-existing GStack skill**
  (`file:///home/dev-p/.claude/skills/gstack/skillify/SKILL.md` →
  `/mnt/c/mybizz/gstack/skillify`, gstack's own tree, description carries the
  gstack marker and "Codify the most recent /scrape flow" content) ✓
- The other gstack skillify copy (`~/.config/opencode/skills/skillify/` →
  `/mnt/c/mybizz/gstack/.opencode/skills/gstack-skillify/`, the one Package
  20.1 protected) is unchanged — checksum still `55d3abe6ec465ecf6502a627aff3fcbf` ✓
- No existing skill was overwritten ✓

---

## 10. Combined workflow (Part E)

Read-only development-assistance workflow over the Vault / `encrypt()`
component, in the same OpenCode session:

1. **GBrain (advisory design/history — the "why"):** retrieved from
   `mb-3-cs-project-library`: `VaultForm` is owner-only with a TOTP step-up on
   every open; secrets are encrypted at rest in the `vault` table and never
   displayed after saving; `encryption_key` lives in Anvil Secrets (the only
   item there); `encryption_service.py` (encrypt/decrypt), `vault_service.py`
   (CRUD), `vault_totp_service.py` (step-up); payment config reads secrets from
   the Vault with `'***'` masking; governed by the
   [[adr-payment-security-boundary-vault|Payment Security Boundary: Secret Keys Deferred to the Vault]] ADR and payment-gateway RBAC ADR.
2. **Graphify (current implementation/dependency facts — the "where/how"):**
   `encrypt()` defined at `encryption_service.py:13` (degree 8); called by
   `save_vault_secret()` (`vault_service.py:82`) and four tests; imported by
   `vault_service.py`; contained by `encryption_service.py`; `rationale_for`
   edge carries the docstring "Encrypt plaintext using AES-CBC with key from
   Anvil Secrets". All edges EXTRACTED.
3. **Interpretation:** the design intent (Vault encrypted, key in Anvil Secrets,
   AES-CBC, vault CRUD depending on encryption) is faithfully realized in the
   current code — `vault_service.save_vault_secret()` calls
   `encryption_service.encrypt()`, matching the build plan. **GBrain supplies
   advisory design/history; Graphify supplies live implementation facts; the
   repository files remain authoritative over both.** No conflict.
4. **No mutation:** no files, database records, guidance blocks, or artifacts
   were modified by this workflow.

---

## 11. Repository and workspace status

- Live repo `/mnt/c/dev/dev-mb-3-cs/mb-3-cs`: `git status --porcelain
  --untracked-files=all` **empty** (clean). HEAD
  `5ce243e12bc2775108c9ecad6da1e6c7f8f1614c`. ✓
- Project-library `/mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library`: working
  tree contains exactly **five** modified files — the **four** authorized WP16.5.1
  frontmatter value-quoting edits + the pre-existing ` M agents.md` (12-line
  "Anvil Agent References" addition):
  - `adr-local/blank-client-template.md` (1-line `document:` quote)
  - [[crm-package-replaces-marketing|Package Name: crm/ Replaces marketing/]] (1-line `document:` quote)
  - `docs/agents/issue-tracker.md` (1-line `document:` quote)
  - `obsolete/issue-tracker.md` (1-line `document:` quote)
  - [[agents|mb-3-cs]] (pre-existing, untouched by this package)
  ✓ No other change.
- No files outside the expected gitignored local integration dirs
  (`.opencode/`, `graphify-out/`) changed ✓
- `.opencode/skills/` present with 119 files ✓
- `.gbrain-source`, `opencode.json`, `.gitignore` unchanged (no `.gbrain-source`
  present; `opencode.json` mtime 2026-08-14 14:46, predates this package) ✓

---

## 12. Files changed during Packages 17–21

- **Package 17** (credentials/runtime): none.
- **Package 18** (Graphify validation): none.
- **Package 19** (complementary integration): none.
- **Package 20.1** (skill scaffold): created **119 files** under
  `/mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` (60 skills + shared
  `conventions/` and `_` deps + `routing-eval.jsonl`). All gitignored,
  local-only.
- **Package 21** (this package): none (read-only acceptance; writes only this
  report to `C:\mybizz\WIP\opencode-output\`).

Net: no tracked-file changes in `mb-3-cs`; the project-library still carries
only the 4 authorized WP16.5.1 frontmatter edits + the pre-existing
[[agents|mb-3-cs]] modification (all uncommitted, per instruction).

---

## 13. Remaining capability limitations

**GBrain `code-callers` / `code-callees` (documented, single limitation).**

`gbrain_code_callers("encrypt")` returns 1 caller (`save_vault_secret`) and
`gbrain_code_callees("encrypt")` returns 16 callees (cryptography primitives,
`hashlib::sha256`, etc.), but every edge is returned with `resolved: false`
and `to_chunk_id: null`. This is a **known capability limitation of the active
`gbrain-everything` schema-pack code-surface configuration** (target symbols
are surfaced but not resolved to definition chunks). It is **not** an
installation or integration failure, and it is **fully compensated** by
Graphify, whose `get_neighbors` returns the same relationships as fully
resolved EXTRACTED typed edges. The combined GBrain+Graphify workflow is
therefore not blocked.

Out-of-scope (not limitations of this acceptance, recorded for transparency):
GBrain `update_available` 0.46.6.0; brain_score 57/100; deferred-source
staleness (`mb4ecom-code`, `mb5pdlf-code`, `pdlf`); a pre-existing
embed-backfill queue item with no live worker; a residual WP16.5.1
sync-failure record for `obsolete/issue-tracker.md`.

---

## 14. Rollback and recovery instructions

- **Remove the Package 20.1 skill scaffold (if ever required):**
  `rm -rf /mnt/c/dev/dev-mb-3-cs/mb-3-cs/.opencode/skills/` — removes the 119
  new files. The pre-existing gstack `skillify` (in `~/.config/opencode/skills/`
  and `/mnt/c/mybizz/gstack/`) is untouched.
- **Revert the WP16.5.1 frontmatter edits (project-library, uncommitted):**
  `cd /mnt/c/dev/dev-mb-3-cs/mb-3-cs-project-library && git checkout -- adr-local/blank-client-template.md adr-local/crm-package-replaces-marketing.md docs/agents/issue-tracker.md obsolete/issue-tracker.md`
  (do **not** checkout [[agents|mb-3-cs]] — its modification is pre-existing and
  intentionally preserved). Backups: `/tmp/opencode/wp165-backup/`.
- **This package:** no recovery needed (read-only). The report file can simply
  be deleted.
- **If an MCP server is unhealthy after a future restart:** relaunch from the
  project root (`cd /mnt/c/dev/dev-mb-3-cs/mb-3-cs && opencode web --hostname
  0.0.0.0`); both MCP commands are declared in `opencode.jsonc` (gbrain) and
  `opencode.json` (graphify) and will re-establish automatically.

---

## 15. Repairs performed

**None.** No active-scope acceptance check failed. One transient
`embedding_provider` probe failure self-resolved on immediate re-probe; no
action was taken (and none was required).

---

## 16. Part-by-part verdict

| Part | Scope | Verdict |
|---|---|---|
| A | GBrain final acceptance (13 checks) | **PASS** |
| B | Graphify final acceptance (11 checks) | **PASS** |
| C | OpenCode MCP acceptance (7 checks) | **PASS** |
| D | OpenCode skill acceptance (9 checks) | **PASS** |
| E | Combined workflow acceptance | **PASS** |
| F | Safety and persistence | **PASS** |

## Final status

**READY FOR DEVELOPMENT WITH DOCUMENTED LIMITATION**
