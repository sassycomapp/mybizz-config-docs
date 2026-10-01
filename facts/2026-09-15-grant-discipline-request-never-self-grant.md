---
title: "2026-09-15-grant-discipline-request-never-self-grant"
doc-id: "mb-7aa71251"
updated: "2026-10-01"
---
# Fact — grant discipline: request, never self-grant

Standing rule (developer instruction, 2026-09-15, session 003–005; encoded in
the config-setup-prompt.md clarity-discipline amendment): **when Cupcake
blocks an operation, the agent requests the grant from the developer in the
chat interface and does nothing else.** An agent never issues a grant request
and then grants the authority itself — that situation may not occur. The
developer executes the grant in the WSL terminal and returns the result to
the agent in chat.

Prescribed commands (developer-run):
- `mg-grant --path <folder> --count N`
- `mg-revoke --path <folder>`
- `net-grant --domain <domain> --count NN`
- `net-revoke --domain <domain>`

Related disciplines proven this session: grant counts are requested to match
the work actually needed; a denied item is never retried (same shape or
reshaped) — it becomes a developer-run command with its exact text, and
results return verbatim as developer-verified.
