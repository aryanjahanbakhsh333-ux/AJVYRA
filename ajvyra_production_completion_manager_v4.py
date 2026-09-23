from __future__ import annotations

import json
from pathlib import Path


class ProductionCompletionManager:
    """
    Controls the transition from production to publication.

    RELEASE_READY is impossible unless all required assets
    physically exist and all validation gates pass.
    """

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
        asset = self.read("asset_integrity_report.json")
        games = self.read("browser_game_final_validation.json")
        anime = self.read("anime_final_validation.json")
        links = self.read("site_link_validation.json")

        gates = {
            "asset_integrity": asset.get("passed") is True,
            "browser_games": games.get("passed") is True,
            "anime": anime.get("passed") is True,
            "site_links": links.get("passed") is True,
        }

        ready = all(gates.values())

        state = {
            "project": "AJVYRA",
            "production_complete": ready,
            "publication_allowed": ready,
            "gates": gates,
            "status": (
                "RELEASE_READY"
                if ready
                else "RELEASE_BLOCKED"
            ),
        }

        output = self.root / "AJVYRA_PRODUCTION_STATE.json"
        output.write_text(
            json.dumps(state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return state


if __name__ == "__main__":
    print(json.dumps(
        ProductionCompletionManager().run(),
        indent=2,
        ensure_ascii=False,
    ))
