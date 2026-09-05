# Anvil Agent Skills Reference

## What This Is

Reference material and agent skills for working with Anvil apps — `github.com/anvil-works/anvil-agent-references`. Official Anvil-maintained repository, generated from Anvil's own source repository. Independent of GStack, GBrain, and Matt Pocock's skills.

**Not officially built for OpenCode.** The repo documents install methods for Codex (plugin) and Claude Code (plugin) only. It also documents a generic manual method (symlinking into `~/.agents/skills/`) with no host restriction — that generic method is what this system uses, and it works correctly with OpenCode.

---

## Install Architecture

**Source clone (authoritative):** `C:\mybizz\anvil-agent-references` (WSL: `/mnt/c/mybizz/anvil-agent-references`).

**Live install:** `~/.agents/skills/` — shared with Matt Pocock's 35 skills (see `matt-pocock-skills-reference.md`).

**Mechanism:** each of the 5 skill folders under `~/.agents/skills/` is a symbolic link into the source clone above. Nothing is copied.

**Browsable via Windows Explorer:** `C:\mybizz\skills-collective\anvil-skills` — a Windows symbolic link into `C:\mybizz\anvil-agent-references` directly (not into `~/.agents/skills/` — this one points straight at the source clone, since that's where the full repo content — docs, stubs, reference — actually lives, not just the skills subfolder).

**Total: 5 skills installed** — `anvil-yaml`, `client-forms`, `client-modules`, `data-models`, `server-code`.

---

## Repo Structure

```
/mnt/c/mybizz/anvil-agent-references/
├── AGENTS.md       — template guidance; copy relevant sections into an app project's own AGENTS.md
├── CLAUDE.md        — same, for Claude Code-style agents
├── README.md        — install instructions (Codex/Claude Code plugin + manual methods)
├── docs/             — agent-oriented Anvil documentation
├── reference/
│   └── types/        — generated .d.ts reference material for anvil.yaml and form templates
├── skills/
│   ├── anvil-yaml/
│   ├── client-forms/
│   ├── client-modules/
│   ├── data-models/
│   └── server-code/
└── stubs/
    ├── client/        — read-only Anvil API .pyi stubs for client_code/
    └── server/        — read-only Anvil API .pyi stubs for server_code/
```

---

## Mandatory Per-Project Setup

**Symlinking the skills alone is not sufficient.** Per the repo's own `AGENTS.md`, an agent working inside a separate app project does not automatically read this repo's guidance — the relevant resource-path section must be copied into that project's own `AGENTS.md`.

**Section to copy, verbatim, into the target project's `AGENTS.md`:**

```markdown
## Anvil Agent References (skills available via ~/.agents/skills/)

Anvil skills (`server-code`, `client-forms`, `client-modules`, `data-models`, `anvil-yaml`) are installed and available. Source checkout: `/mnt/c/mybizz/anvil-agent-references/`.

Resource paths, per the source repo's own AGENTS.md:
- Anvil client stubs: `/mnt/c/mybizz/anvil-agent-references/stubs/client/`
- Anvil server stubs: `/mnt/c/mybizz/anvil-agent-references/stubs/server/`
- Anvil type references: `/mnt/c/mybizz/anvil-agent-references/reference/types/`
- Anvil agent docs: `/mnt/c/mybizz/anvil-agent-references/docs/`
```

**Currently confirmed done in:** `makepdlf-project-library`.

**Not yet done in:** `mb-3-cs`, `mb4ecom`, `mb5pdlf` — the actual real Anvil app projects. Required before agents working in any of those projects can use these skills with full resource-path awareness.

---

## Skill Scope

| Skill | Covers |
|---|---|
| `client-forms` | Form Python, HTML templates, styling, simple event wiring, RepeatingPanel item templates, reusable Forms, legacy YAML conversion |
| `data-models` | Data Table model classes, live rows, buffering/drafts, Data Bindings, server methods |
| `client-modules` | Client modules (Python only, not forms) |
| `server-code` | Server modules |
| `anvil-yaml` | `anvil.yaml` |

---

## Editing Boundaries (from the repo's own AGENTS.md — binding)

- Treat the app checkout being worked on as user-owned code.
- Do not edit the `anvil-agent-references` checkout itself while working on an app — it's a generated reference, not editable source.
- Do not edit `.anvil/` dependency material inside an app checkout.
- Inspect `.anvil/deps/<package>/anvil.yaml` and dependency docs before guessing at a dependency's API.

---

## Validation

```bash
anvil --json validate <path>
```

Validates `anvil.yaml`, HTML/YAML form templates under `client_code/`, and Python files under `client_code/` or `server_code/`.

---

## OpenCode Integration

Skills are invoked as slash commands in OpenCode chat (e.g. `/server-code`, `/data-models`). OpenCode reads directly from `~/.agents/skills/`, same mechanism as Matt Pocock's skills.

**Verify a skill is reachable:**

```bash
cat ~/.agents/skills/<skill-name>/SKILL.md | head -5
```

---

## Update Procedure

```bash
cd /mnt/c/mybizz/anvil-agent-references
git pull
```

Symlinked skills update automatically.

**Verify after update — content is generated from Anvil's own source repo, so skill names could change between releases:**

```bash
ls /mnt/c/mybizz/anvil-agent-references/skills/
ls ~/.agents/skills/ | grep -E "anvil-yaml|client-forms|client-modules|data-models|server-code"
```

If the first list shows names not in the second, symlink the new ones:

```bash
ln -s /mnt/c/mybizz/anvil-agent-references/skills/<new-name> ~/.agents/skills/<new-name>
```

---

*End of document*
