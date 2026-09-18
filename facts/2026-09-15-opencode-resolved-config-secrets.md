---
document: "Fact — OpenCode resolved-config stdout is secret-bearing"
doc-id: 2026-09-15-opencode-resolved-config-secrets
state: Live
date-created: 2026-09-15
---

# Fact — OpenCode resolved-config stdout is secret-bearing

`opencode debug config` resolves and prints the fully merged configuration —
and in doing so it **replaces `{env:...}` placeholders with literal environment
values**. The source config file (`~/.config/opencode/opencode.jsonc`) correctly
holds `{env:OPENAI_API_KEY}` / `{env:ZEROENTROPY_API_KEY}` placeholders, never
literals; the resolved stdout carries the real keys.

Verified live 2026-09-15 (mb-config-opencode run #1): the developer's returned
`opencode debug config` output contained the resolved `OPENAI_API_KEY` and
`ZEROENTROPY_API_KEY` values. The values are not reproduced here.

## Consequences (binding)

- **Treat `opencode debug config` stdout as secret-bearing.** Never paste it
  into shared contexts, never commit it, never echo it in chat or reports.
- **Never retain a capture.** If the command's output must be captured, select
  only the needed non-secret fields and delete the capture immediately.
- **Field extraction is a permanent sensitive-data guard class.** This is why
  the mb-config-opencode exam treats every config-content field check as
  developer-run: the agent's own capture is guard-denied after the fact, and
  the values must never enter agent-managed artifacts.
- **The guard-denial that protects this is correct, not an obstacle.**

## Source

- `opencode/opencode-exam-report.md` — run #1, finding F-6 (2026-09-15)
- `opencode/opencode-skill.md` — credential discipline + graduated lesson:
  config-content field checks are runner D (developer-run)
- Session page: `sessions/2026-09-15-007-opencode-config-suite`