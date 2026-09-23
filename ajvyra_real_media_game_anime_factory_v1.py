from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AJVYRARealMediaGameAnimeFactory:

    def __init__(
        self,
        anime_root: str = "assets/anime-production",
        game_root: str = "games/builds",
        release_root: str = "assets/releases",
    ):
        self.anime_root = Path(anime_root)
        self.game_root = Path(game_root)
        self.release_root = Path(release_root)

        self.release_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def collect_anime(self) -> list[dict[str, Any]]:
        releases = []

        for file in sorted(
            self.anime_root.glob("*.release.json")
        ):
            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            movie = Path(
                data["final_movie"]["path"]
            )

            if (
                data.get("ready") is True
                and movie.exists()
                and movie.stat().st_size > 1024
            ):
                releases.append(
                    {
                        "type": "anime",
                        "id": file.stem.replace(
                            ".release",
                            ""
                        ),
                        "title": data["title"],
                        "video": str(movie),
                        "ready": True,
                        "published": True,
                    }
                )

        return releases

    def collect_games(self) -> list[dict[str, Any]]:
        games = []

        for file in sorted(
            self.game_root.glob("*.release.json")
        ):
            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            build = Path(
                data["build"]
            )

            if (
                data.get("ready") is True
                and build.exists()
                and build.stat().st_size > 0
            ):
                games.append(
                    {
                        "type": "game",
                        "id": data["id"],
                        "title": data["title"],
                        "build": str(build),
                        "ready": True,
                        "published": True,
                    }
                )

        return games

    def build_site_catalog(
        self,
        require_anime: int = 30,
    ) -> Path:

        anime = self.collect_anime()
        games = self.collect_games()

        if len(anime) != require_anime:
            raise RuntimeError(
                f"SITE RELEASE BLOCKED: "
                f"{require_anime} real anime required, "
                f"but only {len(anime)} are ready."
            )

        if not games:
            raise RuntimeError(
                "SITE RELEASE BLOCKED: "
                "no real playable game build exists."
            )

        catalog = {
            "schema": "ajvyra.real.media.catalog.v1",
            "release": True,
            "anime": anime,
            "games": games,
        }

        output = (
            self.release_root /
            "ajvyra-real-media-site-catalog.json"
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
    factory = AJVYRARealMediaGameAnimeFactory()

    try:
        catalog = factory.build_site_catalog()
        print(
            f"REAL AJVYRA SITE CATALOG READY: {catalog}"
        )
    except Exception as exc:
        print(
            f"AJVYRA RELEASE BLOCKED: {exc}"
        )
        raise
