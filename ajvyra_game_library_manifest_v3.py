"""
Final browser-game catalog manifest.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_browser_game_runtime_v3 import GAMES


def build_manifest(root: Path) -> dict:
    items = []

    for game in GAMES:
        path = (
            root
            / "games"
            / f"game_{game.number:02d}"
            / "index.html"
        )

        if not path.exists():
            raise RuntimeError(
                f"Game {game.number:02d} is missing."
            )

        items.append({
            "id": f"game_{game.number:02d}",
            "number": game.number,
            "title": game.title,
            "genre": game.genre,
            "description": game.description,
            "mode": game.mode,
            "goal": game.goal,
            "playable": True,
            "url": f"/games/game_{game.number:02d}/index.html",
        })

    return {
        "project": "AJVYRA",
        "section": "games",
        "version": 3,
        "game_count": 30,
        "runtime": "AJVYRA HTML5 Canvas Runtime",
        "free_runtime": True,
        "games": items,
    }


def write_manifest(root: Path) -> Path:
    manifest = build_manifest(root)

    if len(manifest["games"]) != 30:
        raise RuntimeError("Game manifest must contain 30 games.")

    output = root / "ajvyra_games_manifest_v3.json"

    output.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return output
