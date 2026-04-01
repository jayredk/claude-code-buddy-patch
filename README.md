# Buddy Patch

Reusable Claude Code buddy patch for npm-based installs.

The current bundled buddy theme is:
  - `name`: `Nyx`
  - `species`: `ghost`
  - `rarity`: `epic`
  - `hat`: `beanie`

## Files

- `patch-buddy.py`
  Cross-platform patch script. Works on macOS/Linux and also supports Windows npm installs.

- `patch-buddy.bat`
  Windows one-shot launcher for the Python patch script.

- `claude-patched.bat`
  Windows launcher that reapplies the patch, then starts Claude.

- `README.md`
  This file.

## Disclaimer

This project patches installed Claude Code files on your machine.

- It is unofficial and not affiliated with Anthropic.
- It relies on Claude Code internal implementation details that may change without notice.
- Review the script before running it.
- Use it at your own risk.

## What The Patch Does

The script updates two layers:

1. Claude config
   It writes a complete `companion` object into `~/.claude.json` or `%USERPROFILE%\.claude.json`.

2. npm Claude Code UI internals
   If `cli.js` is found, it patches:
   - buddy bones data
   - buddy rarity / species / hat / stats
   - buddy animation timing
   - ghost ASCII art block

## Supported Install Type

This patch is for npm-based Claude Code installs with a real `cli.js`.

It looks for:

- Windows:
  - `%APPDATA%\npm\node_modules\@anthropic-ai\claude-code\cli.js`
  - `%USERPROFILE%\AppData\Roaming\npm\node_modules\@anthropic-ai\claude-code\cli.js`
  - `npm root -g` + `\@anthropic-ai\claude-code\cli.js`

- macOS / Linux:
  - `~/.nvm/versions/node/*/lib/node_modules/@anthropic-ai/claude-code/cli.js`
  - `~/.npm-global/lib/node_modules/@anthropic-ai/claude-code/cli.js`

If you only use the native installer and there is no `cli.js`, the script can still patch `.claude.json`, but it cannot change the rendered buddy appearance.

## How To Run

### macOS / Linux

```bash
cd buddy-patch
python3 patch-buddy.py
```

### Windows

For a one-time patch, double-click `patch-buddy.bat`, or run:

```bat
patch-buddy.bat
```

To launch Claude with auto-repatch on every start, use:

```bat
claude-patched.bat
```

This is the Windows equivalent of the wrapper workflow: it reapplies the patch, then runs `claude`.

## Backups

Before changing files, the script writes timestamped `.bak` files next to the originals.

Examples:

- `~/.claude.json.20260402-123456.bak`
- `cli.js.20260402-123456.bak`

## Customization

Edit the `COMPANION` block in `patch-buddy.py`:

```python
COMPANION = {
    "name": "Nyx",
    "personality": "...",
    "rarity": "epic",
    "species": "ghost",
    "eye": "@",
    "hat": "beanie",
    "shiny": True,
    "stats": {
        "DEBUGGING": 100,
        "PATIENCE": 83,
        "CHAOS": 77,
        "WISDOM": 100,
        "SNARK": 61,
    },
}
```

Valid built-in style knobs currently used by Claude Code include:

- `rarity`: `common`, `uncommon`, `rare`, `epic`, `legendary`
- `hat`: `none`, `crown`, `tophat`, `propeller`, `halo`, `wizard`, `beanie`, `tinyduck`
- `eye`: `·`, `✦`, `×`, `◉`, `@`, `°`

`species` must be an internal built-in species string that Claude Code knows how to render. Arbitrary values will break the buddy UI.

## Notes

- This patch relies on Claude Code minified internals and may break after upstream updates.
- If Claude Code changes the relevant token names in `cli.js`, the patch script will need to be updated.
- The `.bat` file is the Windows-friendly entry point you asked for. It simply launches the same Python patch logic with UTF-8 enabled.
- `claude-patched.bat` is the Windows wrapper entry point if you want auto-repatch behavior before every launch.
- This project modifies a third-party tool's installed files. Review the script before running it.
