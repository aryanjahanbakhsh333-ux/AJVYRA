from __future__ import annotations

import json
import shutil
from pathlib import Path


class AJVYRAFinal60SiteMaterializer:

    def __init__(
        self,
        anime_index: str = (
            "assets/anime-final/"
            "ajvyra-final-30-anime.json"
        ),
        game_root: str = (
            "games/final-web-builds"
        ),
        site_root: str = "site/assets/releases",
    ):
        self.anime_index = Path(anime_index)
        self.game_root = Path(game_root)
        self.site_root = Path(site_root)

        self.anime_site = (
            self.site_root / "anime"
        )

        self.games_site = (
            self.site_root / "games"
        )

        self.anime_site.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.games_site.mkdir(
            parents=True,
            exist_ok=True,
        )

    def materialize_anime(self):

        data = json.loads(
            self.anime_index.read_text(
                encoding="utf-8"
            )
        )

        items = data["items"]

        if len(items) != 30:
            raise RuntimeError(
                "30 anime required."
            )

        result = []

        for item in items:

            source = Path(
                item["video"]
            )

            if (
                not source.exists()
                or source.stat().st_size < 10_000
            ):
                raise RuntimeError(
                    f"Anime asset missing: "
                    f"{item['title']}"
                )

            destination = (
                self.anime_site /
                source.name
            )

            shutil.copy2(
                source,
                destination,
            )

            result.append(
                {
                    **item,
                    "site_video": str(
                        destination
                    ),
                }
            )

        return result

    def materialize_games(self):

        files = sorted(
            self.game_root.glob(
                "*.final-release.json"
            )
        )

        if len(files) != 30:
            raise RuntimeError(
                f"30 game releases required, "
                f"found {len(files)}"
            )

        result = []

        for file in files:

            item = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            source = Path(
                item["build"]
            )

            if (
                not source.exists()
                or source.stat().st_size <= 1024
            ):
                raise RuntimeError(
                    f"Game build missing: "
                    f"{item['title']}"
                )

            destination = (
                self.games_site /
                f"{item['id']}.zip"
            )

            shutil.copy2(
                source,
                destination,
            )

            result.append(
                {
                    **item,
                    "site_build": str(
                        destination
                    ),
                }
            )

        return result

    def execute(self):

        anime = self.materialize_anime()
        games = self.materialize_games()

        if len(anime) != 30:
            raise RuntimeError(
                "SITE ANIME COUNT INVALID"
            )

        if len(games) != 30:
            raise RuntimeError(
                "SITE GAME COUNT INVALID"
            )

        catalog = {
            "release": "AJVYRA_FINAL",
            "release_approved": True,
            "real_assets_only": True,
            "counts": {
                "anime": len(anime),
                "games": len(games),
                "total": len(anime) + len(games),
            },
            "anime": anime,
            "games": games,
        }

        output = (
            self.site_root /
            "ajvyra-final-site-catalog.json"
        )

        output.write_text(
            json.dumps(
                catalog,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return output


if __name__ == "__main__":
    output = (
        AJVYRAFinal60SiteMaterializer()
        .execute()
    )

    print(
        "\nSITE MATERIALIZATION COMPLETE"
    )

    print(output)
