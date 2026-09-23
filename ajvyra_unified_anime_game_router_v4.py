from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote


class AJVYRAUnifiedRouter:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def routes(self):
        result = {
            "home": "site/index.html",
            "anime": {},
            "games": {},
        }

        for i in range(1, 31):
            anime = self.root / "anime" / f"anime_{i:02d}"
            game = self.root / "games" / f"game_{i:02d}"

            if anime.exists():
                result["anime"][str(i)] = (
                    f"anime/anime_{i:02d}/index.html"
                )

            if game.exists():
                result["games"][str(i)] = (
                    f"games/game_{i:02d}/index.html"
                )

        return result

    def write(self):
        routes = self.routes()

        output = self.root / "AJVYRA_ROUTES.json"
        output.write_text(
            json.dumps(routes, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return output


if __name__ == "__main__":
    print(AJVYRAUnifiedRouter().write())
