---
title: "sysdoc-creator-reference"
doc-id: "mb-04e4093c"
updated: "2026-10-20"
---
# sysdoc-creator — Reference

Execution form for the `mb-sysdoc-creator` skill. The canonical definition is
the source repository's `mb-sysdoc-creator.md` (see Authoritative sources); the
installed copy must stay body-identical to it. Why the rules are shaped this
way: [[[mybizz-config-docs:mb-sysdoc-creator/sysdoc-creator-explainer|explainer]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/sysdoc-creator-explainer.md).

## Invocation

- Invoke as `/mb-sysdoc-creator (system-name)`, by the developer, plus
  whatever the developer supplies: description, files, links, any
  combination — leads to verify, never text to copy.
- Never auto-trigger. Explicit invocation only.
- `system-name` is the folder name. Confirm it matches the developer's
  intended naming before drafting; correct with the developer rather
  than silently normalizing.

## Procedure

The skill's procedure is its canonical source: phases 0–7 (Locate, Intake,
Research, Report + first approval, Draft, Present + second approval, Apply,
Close), one continuous run, under its hard rules. The installed SKILL.md
auto-loads on invocation and is the operative copy — never draft from a
restatement here.

## Sync procedure (source → installed)

1. Edit only the canonical source, `C:\mybizz\mb-sysdoc-creator\mb-sysdoc-creator.md`. Never edit the installed copy directly.
2. Copy the body into `~/.config/opencode/skills/mb-sysdoc-creator/SKILL.md`, keeping the installed file's own frontmatter (`name`, `description`) — never a whole-file copy.
3. Verify: strip frontmatter from both files, hash the two bodies, and require equal hashes. A mismatch means step 2 is wrong — repeat it; never let the copies drift silently.

## Authoritative sources

| Source | Link | Issuer version | Date checked |
|---|---|---|---|
| Canonical skill definition (own repository) | [[[mb-sysdoc-creator:mb-sysdoc-creator\|canonical skill definition]]](C:/mybizz/mb-sysdoc-creator/mb-sysdoc-creator.md) — origin `github.com/sassycomapp/mb-sysdoc-creator` | commit `d16e30d` | 2026-10-20 |
| Governing specification for every suite the skill writes | [[[mybizz-config-docs:mb-sysdoc-creator/doc-suite-specification\|doc-suite-specification]]](C:/mybizz/mybizz-config-docs/mb-sysdoc-creator/doc-suite-specification.md) | — | 2026-10-20 |
| OpenCode skill mechanism (install location, auto-load) | `~/.config/opencode/skills/` — [[[mybizz-os-docs:os-reference-docs/skills-catalog\|skills catalog]]](C:/mybizz/mybizz-os-docs/os-reference-docs/skills-catalog.md) | — | 2026-10-20 |

## Checks

| Check | Method | Run by |
|---|---|---|
| Installed version | `git -C /mnt/c/mybizz/mb-sysdoc-creator log -1 --format='%h %ci'`; then `git -C /mnt/c/mybizz/mb-sysdoc-creator status --porcelain` — non-empty output means the canonical file carries edits beyond that commit. No version field exists; the source commit is the version | agent |
| Sync (source ↔ installed) | Strip frontmatter from both files, hash each body, take the first 16 hex characters; equal means current | agent |
| Works | The installed SKILL.md is present and loadable (it appears in the harness skill list), and the specification file exists — checked at Phase 0 of every run | agent |
| Each config setting | Read the row's Source file live | agent |

## Do not

- Do not edit the installed SKILL.md directly — edit the canonical source, then run the sync procedure.
- Do not restate the skill's procedure in this suite; the canonical source is its only home.
- Do not rename any of the four documents.
- Do not commit — the developer runs commit-all.
