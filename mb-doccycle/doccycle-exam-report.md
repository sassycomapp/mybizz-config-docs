---
title: "doccycle-exam-report"
doc-id: "doccycle-exam-report"
---
# mb-doccycle — Exam Report (Run #1, formal, 2026-09-22)

**Verdict: HEALTHY** — Tiers 0–2 all PASS; zero DOWN / UNHEALTHY / DRIFT
findings; one GAP-recommendation gate item (`.gitignore` for the source
repo's `__pycache__`); Tier 3 Locked (two carried items CY3-1/CY3-2).

## Tier 0 — Invocability

| ID | Expected | Actual | Result |
|---|---|---|---|
| DCY0-1 | Installed SKILL.md md5 == source (`a8336c843c79c900cf98afe0c54c2f69`) | `2 a8336c843c79c900cf98afe0c54c2f69` — identical | PASS |
| DCY0-2 | Three phase specs installed | A-structure.md, B-consistency.md, C-conversion.md present | PASS |
| DCY0-3 | Tool version `0.1.0` | `0.1.0` | PASS |

## Tier 1 — State conformance

| ID | Expected | Actual | Result |
|---|---|---|---|
| DCY1-1 | 8 suite files + full skill source | 9 files in suite (8 + skill source); source home: SKILL.md, phases\ (3), tool\, tests\ | PASS |
| DCY1-2 | Clean or known-pending; HEAD pushed (fd9b22e) | 2 untracked `__pycache__` dirs (known noise — GAP recommendation below); HEAD fd9b22e on pushed master | PASS (with gate item) |
| DCY1-3 | Logs structure complete | run-index.md ✓, learnings\ (3 seeds) ✓, in-progress\ empty ✓, last-completed-run\ (1 WP8 record) ✓, abandoned-runs\ ✓ | PASS |
| DCY1-4 | Backup evidence intact | wp8 folder = 5 files ✓ (wp7 retirement folder present) | PASS |
| DCY1-5 | Enforcement integration present | git-grant ✓; commits policy references git_grants_data (2) ✓; grants file parses (package line ✓; dynamic content, no content-drift check) | PASS |
| DCY1-6 | Retired skills absent both locations; backup intact | 0 hits in skills\, 0 in config-docs ✓ | PASS |
| DCY1-7 | Registers conform | register-local: 10 Retired rows (9 retirement + 1 pre-existing), 13 doccycle mentions incl. the 4 registered rows; config-manager register: doccycle Installed row + 3 Retired rows ✓ | PASS |

## Tier 2 — Functional proof

| ID | Expected | Actual | Result |
|---|---|---|---|
| DCY2-1 | Tool JSON probe; fixture unchanged | pairs=1, files=1; fixture md5 `6000efc6…` identical before/after — read-only contract live | PASS |
| DCY2-2 | 27/27 tests OK | unittest OK (27 tests, 0 failures) | PASS |
| DCY2-3 | Run-record trail present | run-index WP8 row + record in last-completed-run ✓ | PASS |

## Findings

| ID | Class | Evidence | Recommended repair | Risk |
|---|---|---|---|---|
| F-1 | GAP | mb-doccycle source tree carries untracked `tests/__pycache__/` + `tool/__pycache__/` (test-run artifacts) | Add a `.gitignore` (`__pycache__/`) to the source home; developer-applied commit | Low — noise only; no behavior impact |
| F-2 | Carried (Tier 3) | CY3-1 full corpus cycle on a second corpus; CY3-2 detector amendment (2 WP8 defects: folder-token suffix matching + empty display; universe scaffold filtering) | Developer decision at gate: unlock / defer | Low — queued corrections, triage layer already proven to catch the false pairs |

## Deferred items

None beyond F-2's carried tier (all checks agent-runnable; no guard
denials this run).

## Spec-doc flags (docs governance)

None — [[doccycle-config|the spec]] matched live state on every checked
value.