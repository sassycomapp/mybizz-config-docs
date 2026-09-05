# OpenCode Reference — Commands, Verification, Troubleshooting

Companion to `opencode-config.md` (current state) and `opencode-explainer.md`
(mechanics and real incidents). Agent-facing.

---

## Inspecting current configuration

```bash
cat ~/.config/opencode/opencode.jsonc
cat <project-root>/opencode.json 2>/dev/null || echo "no per-project override"
```

## Restarting OpenCode (required after any plugin or global config change)

```bash
pkill -f "opencode web"
cd <project-root>
opencode web --hostname 0.0.0.0
```

Plugin and global config changes are only read at process start — see
`opencode-explainer.md` §2. There is no reload mechanism; a full restart
is the only way to pick up a change.

## Confirming a plugin is loaded exactly once

```bash
grep -ia 'loading plugin' ~/.local/share/opencode/log/*.log | tail -5
```

Check the most recent session's timestamp block specifically. Exactly
one line per real plugin file is correct. Two lines for the same
plugin in the same session means it's discoverable from two separate
paths — find and remove the duplicate discovery path, not the plugin
itself.

## Verifying a skill is genuinely discoverable

```bash
test -r ~/.config/opencode/skills/<skill-name>/SKILL.md && echo "readable"
```

Confirms the real file resolves and is readable through OpenCode's
actual discovery path — not just that a folder or symlink exists.

## Creating a correct, Windows-visible symlink

**Never** create it from WSL pointing at a Windows-drive target — see
`opencode-explainer.md` §4. From the Windows side instead (Developer
Mode must be enabled):

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
Privacy & Security → For Developers → Developer Mode** if a real,
native symlink (`mklink /D`) is needed rather than a junction.

## Recovering from a stale/wrong project on startup

```bash
bash /mnt/c/mybizz/scripts/opencode-db-cleanup.sh
```

Run this proactively, right after renaming or moving any project's own
root folder. On-demand only, deliberately not scheduled. Full detail:
`daily-ops.md`.

## Running any Windows-triggered command against WSL

```
wsl.exe -d <distro-name> -u dev-p -- <command>
```

**Always specify `-d` and `-u` explicitly.** This machine has two WSL
distributions installed; omitting either flag risks silently running
against the wrong one, with no visible error. Confirm the real distro
name first:

```bash
wsl.exe -l -v
```

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
