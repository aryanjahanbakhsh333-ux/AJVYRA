"""
Static validation of every browser game.

This does not merely check that a filename exists.
It checks that the generated HTML contains:
- canvas
- update loop
- input handling
- action handling
- victory state
- failure state
- restart
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List


REQUIRED_MARKERS = (
    "<canvas",
    "requestAnimationFrame",
    "function update",
    "function action",
    "function restart",
    "function win",
    "function lose",
    "keydown",
    "pointerdown",
    "touch",
)


def validate_game(path: Path) -> List[str]:
    errors: List[str] = []

    if not path.exists():
        return ["missing file"]

    if path.stat().st_size < 5000:
        errors.append("file is too small")

    source = path.read_text(encoding="utf-8", errors="replace")

    for marker in REQUIRED_MARKERS:
        if marker.lower() not in source.lower():
            errors.append(f"missing runtime marker: {marker}")

    if not re.search(r"const\s+GAME\s*=", source):
        errors.append("missing game definition")

    if not re.search(r"let\s+score", source):
        errors.append("missing score state")

    if not re.search(r"let\s+timeLeft", source):
        errors.append("missing timer state")

    return errors


def validate_all(root: Path) -> Dict[str, object]:
    games_root = root / "games"

    results = {}
    ready = 0

    for number in range(1, 31):
        path = games_root / f"game_{number:02d}" / "index.html"
        errors = validate_game(path)

        results[str(number)] = {
            "path": str(path),
            "ready": not errors,
            "errors": errors,
        }

        if not errors:
            ready += 1

    return {
        "expected": 30,
        "ready": ready,
        "blocked": 30 - ready,
        "games": results,
        "release_ready": ready == 30,
    }


def write_report(root: Path) -> Path:
    import json

    report = validate_all(root)

    output = root / "game_runtime_validation.json"
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if not report["release_ready"]:
        raise RuntimeError(
            f"Browser game runtime validation failed: "
            f"{report['ready']}/30"
        )

    return output
