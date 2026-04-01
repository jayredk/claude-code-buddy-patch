#!/usr/bin/env python3
"""Buddy patch for Claude Code.

This script updates ~/.claude.json (or %USERPROFILE%\\.claude.json on Windows)
and patches npm-installed Claude Code's cli.js when available.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


COMPANION = {
    "name": "Nyx",
    "personality": 'A cheeky little ghost monarch who giggles at messy state, side-eyes every "quick" useEffect, and quietly fixes things before the rerenders begin.',
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

PATCH_MARKERS = {
    "bones": 'species:"ghost"',
    "art": '"    ~  ~    "',
}


def home_dir() -> Path:
    return Path.home()


def claude_json_path() -> Path:
    return home_dir() / ".claude.json"


def state_dir() -> Path:
    if sys.platform == "win32":
        return home_dir() / ".claude-buddy"
    return home_dir() / ".local/share/claude-buddy"


def backup_file(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_name(f"{path.name}.{stamp}.bak")
    shutil.copy2(path, backup)
    return backup


def find_cli_js() -> Path | None:
    home = home_dir()
    candidates: list[Path] = []

    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            candidates.append(Path(appdata) / "npm/node_modules/@anthropic-ai/claude-code/cli.js")
        candidates.append(home / "AppData/Roaming/npm/node_modules/@anthropic-ai/claude-code/cli.js")
    else:
        candidates.append(home / ".npm-global/lib/node_modules/@anthropic-ai/claude-code/cli.js")

    for candidate in candidates:
        if candidate.exists():
            return candidate

    try:
        npm_root = subprocess.run(
            ["npm", "root", "-g"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception:
        npm_root = ""

    if npm_root:
        npm_candidate = Path(npm_root) / "@anthropic-ai/claude-code/cli.js"
        if npm_candidate.exists():
            return npm_candidate

    nvm_root = home / ".nvm/versions/node"
    if nvm_root.exists():
        matches = sorted(nvm_root.glob("*/lib/node_modules/@anthropic-ai/claude-code/cli.js"))
        if matches:
            return matches[-1]

    return None


def read_state(state_file: Path) -> dict:
    if not state_file.exists():
        return {}
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_state(state_file: Path, data: dict) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ensure_companion() -> None:
    config_path = claude_json_path()
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config file: {config_path}")

    data = json.loads(config_path.read_text(encoding="utf-8"))
    hatched_at = data.get("companion", {}).get("hatchedAt", 1775020915832)
    desired = {
        "name": COMPANION["name"],
        "personality": COMPANION["personality"],
        "hatchedAt": hatched_at,
        "rarity": COMPANION["rarity"],
        "species": COMPANION["species"],
        "eye": COMPANION["eye"],
        "hat": COMPANION["hat"],
        "shiny": COMPANION["shiny"],
        "stats": COMPANION["stats"],
    }

    if data.get("companion") == desired and data.get("companionMuted") is False:
        return

    backup_file(config_path)
    data["companion"] = desired
    data["companionMuted"] = False
    data["autoUpdates"] = True
    config_path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")


def replace_ghost_art_block(content: str) -> str:
    marker = "[dT8]:[["
    start = content.find(marker)
    if start == -1:
        raise RuntimeError("Buddy patch target '[dT8]:[[' not found in cli.js")

    depth = 0
    end = None
    for i in range(start + len("[dT8]:"), len(content)):
        if content[i] == "[":
            depth += 1
        elif content[i] == "]":
            depth -= 1
        if depth == 0:
            end = i + 1
            break

    if end is None:
        raise RuntimeError("Buddy patch target art block is malformed")

    new_art = (
        '[dT8]:[["            ","   .----.   ","  / {E}  {E} \\\\  ",'
        '"  |      |  ","  ~`~``~`~  "],["            ","   .----.   ",'
        '"  / {E}  {E} \\\\  ","  |      |  ","  `~`~~`~`  "],'
        '["    ~  ~    ","   .----.   ","  / {E}  {E} \\\\  ",'
        '"  |      |  ","  ~~`~~`~~  "]]'
    )
    return content[:start] + new_art + content[end:]


def patch_cli() -> bool:
    cli_js = find_cli_js()
    if cli_js is None or not cli_js.exists():
        raise FileNotFoundError("npm-installed cli.js not found")

    content = cli_js.read_text(encoding="utf-8")
    already_patched = (
        all(marker in content for marker in PATCH_MARKERS.values())
        and 'hat:"beanie"' in content
        and 'rarity:"epic"' in content
    )
    if already_patched:
        return False

    original = content

    old_zk = re.search(
        r'function WE_\(q\)\{let K=JE_\(q\);return\{bones:\{rarity:K,species:Zk6\(q,W54\),eye:Zk6\(q,D54\),hat:K==="common"\?"none":Zk6\(q,f54\),shiny:q\(\)<0\.01,stats:XE_\(q,K\)\},inspirationSeed:Math\.floor\(q\(\)\*1e9\)\}\}',
        content,
    )
    if not old_zk:
        raise RuntimeError("Buddy patch target 'WE_' not found in cli.js")

    new_zk = (
        'function WE_(q){let K=JE_(q),_=Math.floor(q()*1e9),Y={bones:{rarity:K,'
        'species:Zk6(q,W54),eye:Zk6(q,D54),hat:K==="common"?"none":Zk6(q,f54),'
        'shiny:q()<0.01,stats:XE_(q,K)},inspirationSeed:_};'
        'return Y.bones={...Y.bones,rarity:"epic",species:"ghost",'
        'eye:"@",hat:"beanie",shiny:!0,stats:{DEBUGGING:100,PATIENCE:83,CHAOS:77,'
        'WISDOM:100,SNARK:61}},Y}'
    )
    content = content[: old_zk.start()] + new_zk + content[old_zk.end() :]
    content = replace_ghost_art_block(content)

    if content == original:
        return False

    backup = backup_file(cli_js)
    cli_js.write_text(content, encoding="utf-8")

    state_file = state_dir() / "state.json"
    state = read_state(state_file)
    state.update(
        {
            "lastPatchedAt": datetime.now().isoformat(timespec="seconds"),
            "cliPath": str(cli_js),
            "backupPath": str(backup),
        }
    )
    write_state(state_file, state)
    return True


def main() -> int:
    try:
        ensure_companion()
        changed = patch_cli()
    except Exception as exc:
        print(f"[buddy-patch] {exc}", file=sys.stderr)
        return 1

    if changed:
        print("[buddy-patch] applied")
    else:
        print("[buddy-patch] already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
