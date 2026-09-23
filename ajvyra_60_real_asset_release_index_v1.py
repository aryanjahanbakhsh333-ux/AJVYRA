from __future__ import annotations

import json
from pathlib import Path


class AJVYRA60RealAssetReleaseIndex:

    def __init__(
        self,
        anime_root: str = "assets/anime-final",
        game_root: str = "games/real-builds",
        output: str = (
            "assets/releases/"
            "ajvyra-60-real-release-index.json"
        ),
    ):
        self.anime_root = Path(anime_root)
        self.game_root = Path(game_root)
        self.output = Path(output)

        self.output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def collect_anime(self):

        releases = []

        for file in sorted(
            self.anime_root.glob(
                "*.release.json"
            )
        ):
            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            video = Path(
                data["final_video"]
            )

            if (
                data.get("real_generated") is True
                and data.get("ready") is True
                and video.exists()
                and video.stat().st_size > 10_000
            ):
                releases.append(
                    {
                        "type": "anime",
                        "id": data["id"],
                        "title": data["title"],
                        "video": str(video),
                        "real": True,
                        "ready": True,
                        "published": True,
                    }
                )

        return releases

    def collect_games(self):

        releases = []

        for file in sorted(
            self.game_root.glob(
                "*.release.json"
            )
        ):
            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

            entry = Path(
                data["entry"]
            )

            if (
                data.get("real_build") is True
                and data.get("ready") is True
                and entry.exists()
            ):
                releases.append(
                    {
                        "type": "game",
                        "id": data["id"],
                        "title": data["title"],
                        "genre": data["genre"],
                        "build": str(
                            Path(data["build"])
                        ),
                        "entry": str(entry),
                        "real": True,
                        "ready": True,
                        "published": True,
                    }
                )

        return releases

    def build(self):

        anime = self.collect_anime()
        games = self.collect_games()

        print(
            f"ANIME: {len(anime)}/30"
        )

        print(
            f"GAMES: {len(games)}/30"
        )

        if len(anime) != 30:
            raise RuntimeError(
                "RELEASE BLOCKED: "
                "30 real anime are required."
            )

        if len(games) != 30:
            raise RuntimeError(
                "RELEASE BLOCKED: "
                "30 real games are required."
            )

        assets = anime + games

        if len(assets) != 60:
            raise RuntimeError(
                "RELEASE BLOCKED: "
                "60 real assets required."
            )

        if any(
            item["real"] is not True
            for item in assets
        ):
            raise RuntimeError(
                "RELEASE BLOCKED: "
                "fake asset detected."
            )

        catalog = {
            "schema": (
                "ajvyra.60.real.release.v1"
            ),
            "release_approved": True,
            "counts": {
                "anime": 30,
                "games": 30,
                "total": 60,
            },
            "anime": anime,
            "games": games,
        }

        self.output.write_text(
            json.dumps(
                catalog,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return self.output


if __name__ == "__main__":
    index = AJVYRA60RealAssetReleaseIndex()

    output = index.build()

    print(
        "AJVYRA 60/60 REAL ASSETS READY:"
    )

    print(output)
