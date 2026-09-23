from __future__ import annotations

import json
import re
from pathlib import Path


REQUIRED = [
    r"<canvas\b",
    r"requestAnimationFrame",
    r"addEventListener",
    r"touch",
    r"keydown",
    r"score",
    r"restart",
    r"gameover|gameOver|game-over",
]


class BrowserGameFinalValidator:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def validate_one(self, number):
        path = (
            self.root
            / "games"
            / f"game_{number:02d}"
            / "index.html"
        )

        if not path.exists():
            return {
                "id": number,
                "valid": False,
                "reason": "missing",
            }

        text = path.read_text(encoding="utf-8", errors="ignore")

        missing = [
            pattern
            for pattern in REQUIRED
            if not re.search(pattern, text, re.I)
        ]

        return {
            "id": number,
            "valid": not missing,
            "missing": missing,
        }

    def run(self):
        games = [self.validate_one(i) for i in range(1, 31)]

        report = {
            "count": len(games),
            "passed": all(x["valid"] for x in games),
            "games": games,
        }

        output = self.root / "browser_game_final_validation.json"
        output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        BrowserGameFinalValidator().run(),
        indent=2,
        ensure_ascii=False,
    ))
