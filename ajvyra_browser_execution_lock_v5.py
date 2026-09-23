from __future__ import annotations

import json
import re
from pathlib import Path


class BrowserExecutionLock:
    REQUIRED = [
        r"<canvas",
        r"requestAnimationFrame",
        r"addEventListener",
        r"touch",
        r"keydown",
        r"restart",
        r"score",
    ]

    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def validate(self, number):
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

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        missing = [
            pattern
            for pattern in self.REQUIRED
            if not re.search(pattern, text, re.I)
        ]

        return {
            "id": number,
            "valid": not missing,
            "missing": missing,
        }

    def run(self):
        games = [
            self.validate(i)
            for i in range(1, 31)
        ]

        report = {
            "stage": "BROWSER_EXECUTION_LOCK",
            "passed": all(x["valid"] for x in games),
            "games": games,
            "delivery": "HTML5_BROWSER",
            "pygame_required_for_player": False,
        }

        (self.root / "BROWSER_EXECUTION_LOCK_V5.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        BrowserExecutionLock().run(),
        indent=2,
        ensure_ascii=False,
    ))
