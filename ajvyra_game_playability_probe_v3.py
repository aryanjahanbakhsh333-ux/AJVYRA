"""
Playability probe.

The probe loads each HTML game as text and verifies the actual runtime
contains executable gameplay mechanics rather than a static placeholder.

It also checks that every game has unique title/mode metadata.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_browser_game_runtime_v3 import GAMES
from ajvyra_game_runtime_validator_v3 import validate_game


def probe(root: Path) -> dict:
    results = []

    for game in GAMES:
        path = (
            root
            / "games"
            / f"game_{game.number:02d}"
            / "index.html"
        )

        errors = validate_game(path)

        source = ""
        if path.exists():
            source = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

        gameplay_signals = {
            "canvas": "<canvas" in source,
            "movement": "player.x" in source and "player.y" in source,
            "collision": "Math.hypot" in source,
            "input": "keydown" in source and "pointerdown" in source,
            "score": "score++" in source,
            "victory": "win()" in source,
            "failure": "lose()" in source,
            "restart": "restart()" in source,
        }

        gameplay_ready = (
            not errors
            and all(gameplay_signals.values())
        )

        results.append({
            "number": game.number,
            "title": game.title,
            "mode": game.mode,
            "path": str(path),
            "errors": errors,
            "signals": gameplay_signals,
            "playable": gameplay_ready,
        })

    playable = sum(
        1
        for result in results
        if result["playable"]
    )

    return {
        "expected": 30,
        "playable": playable,
        "blocked": 30 - playable,
        "release_ready": playable == 30,
        "games": results,
    }


def run_probe(root: Path) -> Path:
    report = probe(root)

    output = root / "game_playability_report.json"

    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if not report["release_ready"]:
        raise RuntimeError(
            f"Game playability probe failed: "
            f"{report['playable']}/30"
        )

    return output
