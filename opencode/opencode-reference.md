---
title: "opencode-reference"
doc-id: "opencode-reference"
---
# OpenCode Reference — Commands, Verification, Troubleshooting

Companion to [[opencode-config|OpenCode Configuration]] (current state),
[[opencode-permission-access-control-model|Permission & Access Control Model]] (the permission layers),
[[opencode-project-session-data-integrity|Project & Session Data Integrity]] (session database
maintenance), and [[opencode-explainer|OpenCode Explainer]] (mechanics and real incidents).
Config-management set: [[opencode-exam-plan|Exam Plan]] (transient job-spec — read
second, every run), [[opencode-exam-report|Exam Report]] (last verified state),
[[opencode-log|Log]] (chronological events), [[opencode-learnings|Learnings]]
(transient knowledge). Agent-facing.

---

## Inspecting current configuration

```bash
cat ~/.config/opencode/opencode.jsonc
cat <project-root>/opencode.json 2>/dev/null || echo "no per-project override"
```

**Inspecting the RESOLVED configuration** (global + project merged, as
OpenCode will actually apply it) — added 2026-09-09:

```bash
cd <project-root> && opencode debug config
```

This is the authoritative way to answer any "which setting wins?" question
— it prints the fully merged, resolved configuration including managed
settings. Verified live 2026-09-09: a per-project `permission.bash`
override and the global deny patterns were both present in the resolved
output (deep merge confirmed).

## Restarting OpenCode (required after any plugin or global config change)

```bash
pkill -f "opencode web"
cd <project-root>
opencode web --hostname 0.0.0.0
```

Plugin and global config changes are only read at process start — see
[[opencode-explainer|OpenCode Explainer]] §2. There is no reload mechanism; a full restart
is the only way to pick up a change. Verified live 2026-09-08 (the Cupcake
reactivation) and 2026-09-09 (the plugin re-rename).

## Confirming a plugin is loaded exactly once

```bash
grep -ia 'loading plugin' ~/.local/share/opencode/log/*.log | tail -5
```

Check the most recent session's timestamp block specifically. Exactly one
line per real plugin file is correct. Two lines for the same plugin in the
same session means it's discoverable from two separate paths — find and
remove the duplicate discovery path, not the plugin itself.

## Verifying a skill is genuinely discoverable

```bash
test -r ~/.config/opencode/skills/<skill-name>/SKILL.md && echo "readable"
```

Confirms the real file resolves and is readable through OpenCode's actual
discovery path — not just that a folder or symlink exists.

## Verifying the bash deny-list is live

The global config's destructive-command deny patterns are enforced on real
tool calls — confirmed live 2026-09-09: an agent command containing
`rm -rf` was refused by the `rm -rf *` deny pattern (the harness
permission layer, not Cupcake — the denial message names the OpenCode
permission rules). Any command whose text matches a deny pattern is
refused before execution; construct commands knowing this, and never
work around a deny by rephrasing.

## Creating a correct, Windows-visible symlink

**Never** create it from WSL pointing at a Windows-drive target — see
[[opencode-explainer|OpenCode Explainer]] §4. From the Windows side instead (Developer Mode
must be enabled):

```bash
cmd.exe /c mklink /D C:\path\to\link C:\path\to\real\target
```

Verify from both sides:

```bash
# Windows
cmd.exe /c dir C:\path\to\ 
# should show <SYMLINKD> link [C:\path\to\real\target]

# WSL
readlink -v /mnt/c/path/to/link
ls -la /mnt/c/path/to/
```

Both must agree before trusting the link.

## Checking whether Developer Mode is enabled

```bash
reg.exe query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /v AllowDevelopmentWithoutDevLicense 2>&1
```

A missing key or value `0` means it's off. Enable via **Settings →
Privacy & Security → For Developers → Developer Mode** if a real, native
symlink (`mklink /D`) is needed rather than a junction.

## Recovering from a stale/wrong project on startup

```bash
bash /mnt/c/mybizz/scripts/opencode-db-cleanup.sh
```

Run this proactively, right after renaming or moving any project's own
root folder. On-demand only, deliberately not scheduled. Full detail:
`daily-ops.md`.

## Running any Windows-triggered command against WSL

```
wsl.exe -d Ubuntu -u dev-p -- <command>
```

**Always specify `-d` and `-u` explicitly.** Verified live 2026-09-09:
the machine's distros are `Ubuntu-22.04` (the DEFAULT — and stopped) and
`Ubuntu` (the working environment). Omitting either flag risks silently
running against the wrong one, with no visible error.

## Do not

- Do not assume a plugin or config edit takes effect without a full
  restart (`pkill` + relaunch) — no hot-reload exists.
- Do not create a symlink from WSL pointing at a Windows-drive target —
  confirmed unreadable by Windows Explorer.
- Do not invoke `wsl.exe` from any Windows-triggered command (a
  scheduled task, a shortcut) without explicit `-d`/`-u` flags.
- Do not trust a single-sided symlink check — verify from both Windows
  and WSL before treating a link as working.
- Do not assume per-skill permission rules are achievable — no
  skill-identity field reaches any plugin, confirmed against OpenCode's
  own source.
- Do not include `rm -rf`, destructive git, or piped-curl patterns in a
  command whose text might also match an allow intent — the deny patterns
  match the command TEXT and refuse it before execution (confirmed live
  2026-09-09). Rephrase or split the command instead.
