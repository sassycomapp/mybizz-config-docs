---
title: "mb-submit-memory-config"
doc-id: "mb-e76d96dd"
updated: "2026-10-20"
---
# mb-submit-memory — Configuration

State of the governed-submission skill: what exists, what it is set to, and
the issuer's standard for it. Procedures in [[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-reference|Reference: Usage, Invocation, and the Full Cycle]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-reference.md); reasoning in
[[[mybizz-config-docs:mb-submit-memory/mb-submit-memory-explainer|Explainer]]](C:/mybizz/mybizz-config-docs/mb-submit-memory/mb-submit-memory-explainer.md); the skill's own `SKILL.md` is the
authoritative procedure.

## Identity

| Field | Value |
|---|---|
| Issuer | MyBizz |
| Installed version | Commit `30eb158` of the canonical source; the installed copy is body-identical (13,272 B, sha256 `e3acd8d9…`) |
| Standard taken from | `30eb158` — the canonical source at the installed version |
| Last researched | 2026-10-20 |

## Skill

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Canonical skill source | The canonical file is the skill's authoritative text | `/mnt/c/mybizz/mb-submit-memory/mb-submit-memory.md` (12,625 B) | `/mnt/c/mybizz/mb-submit-memory/mb-submit-memory.md` | |
| Installed copy | Body identical to the canonical source; frontmatter differs by design | One physical file at two directory entries: `~/.config/opencode/skills/mb-submit-memory/SKILL.md` and `~/.config/skills/mb-submit-memory/` | Live body diff | L1, L2 |
| Invocation | `/mb-submit-memory (path)`; the path is always given explicitly; never auto-triggered | Same as standard | `/mnt/c/mybizz/mb-submit-memory/mb-submit-memory.md` | |
| Run cycle | Learnings → backup → detect → report → approval → apply → verify → log → learnings, one continuous run | Same as standard | `/mnt/c/mybizz/mb-submit-memory/mb-submit-memory.md` | |
| Writer credentials | Two credentials, chosen by invocation context, referenced by name only | `MEMORY_GOVERNOR_WRITER_MANUAL_SUBMISSION` and `MEMORY_GOVERNOR_WRITER_PDLF_STEP_SYNC`, environment variables in `/home/dev-p/memory-governor/.env` | `/mnt/c/mybizz/mb-submit-memory/mb-submit-memory.md` | |
| Submission command form | One WSL command, `(set -a; . /home/dev-p/memory-governor/.env; set +a; curl …)`, credential inside the command | Same as standard | `/mnt/c/mybizz/mb-submit-memory/mb-submit-memory.md` | |
| Visibility | `project_local` | `project_local` — the default, agent-recallable | `/mnt/c/mybizz/mb-submit-memory/mb-submit-memory.md`; live recall | L3 |

## Downstream system — memory governor

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| App location | — | `/home/dev-p/memory-governor` (WSL-native; git remote `sassycomapp/memory-governor.git`) | Live check | |
| Version | — | pyproject `0.1.0`, commit `486ae4b` | Live check | |
| API | — | `http://127.0.0.1:8321`, one listener | Live probe | |
| Auth gate | — | Unauthenticated `GET /memory/review-queue` answers HTTP 422 | Live probe | |
| Auto-start | — | systemd user units `memory-governor-api` and `memory-governor-worker`, active and enabled, `Restart=on-failure`, `EnvironmentFile=.env` | Unit files | |
| Database | — | Recorded in the governor suite | [[[mybizz-config-docs:memory-governor/memory-governor-config\|Memory Governor Configuration]]](C:/mybizz/mybizz-config-docs/memory-governor/memory-governor-config.md) | |
| Governor's GBrain source | — | `memory-governor-code`, registered (46 pages) | `gbrain sources list` | |
| Past-run evidence | — | `registers/candidates/` candidate records and the run-log lane | Live check | |

## GBrain dependency

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| GBrain version | — | 0.59.18.0 — full GBrain state recorded in the gbrain suite | `gbrain --version` | |
| MEMORY_VERBS surface | — | Enabled (`gbrain config get mcp_surface` → `verbs`) | Live check | |
| Reranker | — | On — recorded in the gbrain suite | [[[mybizz-config-docs:gbrain/gbrain-config\|GBrain Configuration]]](C:/mybizz/mybizz-config-docs/gbrain/gbrain-config.md) | |
| This skill's source page | — | `mb-submit-memory` source, federated (1 page) | `gbrain sources list` | |

## Governance chain

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Cupcake enforcement | — | Active and enforcing — standing policy | [[[mybizz-config-docs:cupcake/cupcake-config\|Cupcake Configuration]]](C:/mybizz/mybizz-config-docs/cupcake/cupcake-config.md) › Operational status | |
| Outbound-network rule | Loopback destinations are always allowed | The active rule's loopback exemption names the governor API at 127.0.0.1:8321 | Cupcake active policy | |
| mg-grant / mg-revoke | — | Cupcake's cross-project grant tools (`~/.config/cupcake/bin/`); no connection to the memory governor | Live check | |

## Logs lane

| Setting | Issuer standard | MyBizz value | Source | Learning |
|---|---|---|---|---|
| Log location | — | `/mnt/c/mybizz/logs/mb-submit-memory/` — four run logs and `learnings.md` (9 entries) | Live check | |

## Open items

None.
