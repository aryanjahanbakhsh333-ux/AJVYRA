from __future__ import annotations

import json
from pathlib import Path


class AJVYRAFinalReleaseGate:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def read(self, name):
        path = self.root / name

        if not path.exists():
            return {}

        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def run(self):
        production = self.read(
            "AJVYRA_PRODUCTION_STATE.json"
        )

        required = [
            "asset_integrity_report.json",
            "browser_game_final_validation.json",
            "anime_final_validation.json",
            "site_link_validation.json",
            "AJVYRA_FINAL_RELEASE_MANIFEST_V4.json",
        ]

        missing = [
            name
            for name in required
            if not (self.root / name).exists()
        ]

        ready = (
            production.get("publication_allowed") is True
            and not missing
        )

        result = {
            "project": "AJVYRA",
            "status": (
                "RELEASE_READY"
                if ready
                else "RELEASE_BLOCKED"
            ),
            "publication_allowed": ready,
            "missing_reports": missing,
            "anime": 30,
            "games": 30,
        }

        output = self.root / "AJVYRA_FINAL_RELEASE_GATE_V4.json"

        output.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return result


if __name__ == "__main__":
    print(json.dumps(
        AJVYRAFinalReleaseGate().run(),
        indent=2,
        ensure_ascii=False,
    ))
