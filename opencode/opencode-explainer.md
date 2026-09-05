# OpenCode Explainer

## 1. Opening

OpenCode is the actual harness this entire environment runs inside — the program that reads `AGENTS.md`, loads skills, enforces (or fails to enforce) permissions, and decides which tool calls an agent can make. Every other system documented in this project — Cupcake, GBrain, Memory Governor, Sentinel — is either a plugin running inside OpenCode, or a tool OpenCode's agents call. Understanding OpenCode's own real behavior, including its genuine rough edges, matters more than any single tool built on top of it.

This document exists because several real, costly incidents tonight traced back not to Cupcake, not to GBrain, but to OpenCode's own underlying mechanics — behaving in ways that were reasonable, once understood, but genuinely surprising the first time each one was hit.

---

## 2. Plugins Load Once, Not Per-Session

The single most consequential mechanical fact about OpenCode, discovered the hard way, more than once tonight: **a plugin is loaded exactly once, when the OpenCode process itself starts — never per chat session, and never automatically on a file change.**

Editing a plugin's own code on disk, while OpenCode is already running, has zero visible effect. No error. No warning. The old, already-loaded version keeps running silently, exactly as if nothing had changed, until the whole process is fully quit and relaunched. This applies identically to Cupcake's plugin, to MCP server entries like GBrain's, and to any other plugin registered with OpenCode.

**A related, distinct trap: OpenCode does not deduplicate plugins by real file identity — only by the path it was told to load.** If the same plugin exists at two separate discovery paths — even a global copy and a symlink pointing at that exact same file — OpenCode loads both as two independent instances. Confirmed directly: this caused Cupcake's cross-project grant system to decrement its write count by two for every single real write, not one, because the plugin was genuinely running twice. A symlink did not fix this — only removing the second discovery path entirely did. The lesson generalizes beyond Cupake specifically: **a plugin, skill, or MCP entry must exist at exactly one discoverable path, never two, even if both point at identical content.**

---

## 3. Skill Discovery — Several Real, Different Mechanisms, Not One

Skills reach OpenCode through more than one real pathway, and they are not all installed the same way — confirmed directly by a full, real audit of every skill on this machine:

- **Plain, real folders** — no symlink at all. This project's own custom skills (`mb-align-docs`, `mb-docs-manager`, etc.) work this way.
- **Symlinks to a real folder elsewhere on the same drive** — most third-party skills (Anvil, GStack's individual skills, Archify).
- **A hybrid pattern** — GStack's own top-level entry is a real folder, but individual skills *inside* that folder are themselves further symlinks to yet another location.
- **A two-hop pattern** — Magdoub's wireframe skill points to an empty intermediate folder, which in turn points to the real content sitting in a completely separate directory tree (`~/.claude/skills/`).

No single "correct" install method exists across every skill-set; what matters is that whichever method is used, it resolves correctly from OpenCode's own real discovery path.

---

## 4. The `drvfs` Symlink Trap — Windows and WSL Disagree About What a Link Is

A real, structural incompatibility, confirmed directly through forensic inspection of the actual filesystem reparse-point tags: **a symlink created from inside WSL, pointing at a folder on the Windows drive, produces a special "LX symlink" type that Windows Explorer cannot read at all** — it shows as an empty, 0-byte file, not a broken link, not an error, just apparently nothing.

The reverse direction has the opposite problem: a symlink created from the *Windows* side, pointing back *into* WSL's own internal filesystem, displays correctly in Explorer but cannot be resolved from WSL's own side.

**The only combination that works reliably both ways: create the symlink from the Windows side, using `mklink /D`, pointing at a target that itself lives on the Windows drive** — never a WSL-internal path. This requires Windows Developer Mode to be enabled for an unprivileged account to create this specific kind of link at all; without it, only a junction (a different, slightly less capable link type) is available without elevated permissions.

---

## 5. Global vs. Per-Project Configuration

Two separate, distinct config layers exist, and they are not the same question as the one covered above:

- **Global** — `~/.config/opencode/opencode.jsonc`, applies everywhere, every project, unless overridden.
- **Per-project** — an `opencode.json` sitting inside a specific project's own folder, overriding the global config for that project only. The stricter rule wins on any genuine conflict between the two.

**A separate, now-resolved incident: the global folder itself briefly held two files at once** — `opencode.json` and `opencode.jsonc`, both real, both loaded, with genuinely different content in each, and no clear, verified answer for which one would win if they ever conflicted. Confirmed and fixed 2026-09-01: consolidated into a single `opencode.jsonc`, the other deleted. One file, one source of truth, going forward — see `opencode-config.md` for the real, current content.

---

## 6. Stale Database Rows, and the Two-WSL-Distro Risk

OpenCode tracks known projects and sessions in its own local database, with no built-in cleanup when a project folder is renamed or moved — the old row simply lingers, sometimes causing OpenCode to open the wrong, stale project on startup. A real, dedicated script (`opencode-db-cleanup.sh`) exists specifically for this, run manually, right after any project rename or move — never scheduled automatically, since a false positive (like a temporarily unmounted drive) could otherwise delete real history unattended.

**A separate, more subtle risk, confirmed real on this specific machine: two WSL distributions are installed, and the actual working environment lives in the non-default one.** Any command triggered from the Windows side — a scheduled task, a shortcut — that invokes `wsl.exe` without explicitly naming the correct distro and user risks silently running against the wrong environment entirely, with no visible error. Every real, Windows-triggered command touching this environment must explicitly specify `-d <distro> -u <user>`.

---

## 7. Known Limitations, Honestly Stated

**No native session-start hook exists.** There is no OpenCode mechanism that automatically runs a checklist or prompt at the start of every session — the session-start checklist is a human-run practice, pasted manually, not a technical control.

**No skill-identity field reaches any plugin.** Confirmed directly, from OpenCode's own real source: the event a plugin receives for any tool call carries the tool name, arguments, and session ID — never which skill, if any, triggered the call. Per-skill permission rules are not currently possible for this reason, confirmed structurally, not assumed.

**Plugin deduplication is by path, not identity** — covered fully in Section 2. Anything relying on a plugin's state (like a count or a cache) must ensure that plugin is discoverable from exactly one path.

---

*Companion document: `opencode-config.md` (current configuration, real skill inventory, active-project standard).*

*End of document*
