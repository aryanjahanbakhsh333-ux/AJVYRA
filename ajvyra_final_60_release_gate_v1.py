from __future__ import annotations

import json
from pathlib import Path


class AJVYRAFinal60ReleaseGate:

    def __init__(
        self,
        catalog: str = (
            "site/assets/releases/"
            "ajvyra-final-site-catalog.json"
        ),
        approval_file: str = (
            "site/assets/releases/"
            "AJVYRA_RELEASE_APPROVED.json"
        ),
    ):
        self.catalog = Path(catalog)
        self.approval_file = Path(
            approval_file
        )

    def verify(self):

        if not self.catalog.exists():
            raise RuntimeError(
                "FINAL RELEASE BLOCKED: "
                "site catalog does not exist."
            )

        data = json.loads(
            self.catalog.read_text(
                encoding="utf-8"
            )
        )

        anime = data.get(
            "anime",
            [],
        )

        games = data.get(
            "games",
            [],
        )

        if len(anime) != 30:
            raise RuntimeError(
                f"FINAL RELEASE BLOCKED: "
                f"anime={len(anime)}/30"
            )

        if len(games) != 30:
            raise RuntimeError(
                f"FINAL RELEASE BLOCKED: "
                f"games={len(games)}/30"
            )

        for item in anime:

            if item.get("real_asset") is not True:
                raise RuntimeError(
                    f"Fake anime asset: "
                    f"{item.get('title')}"
                )

            if item.get("ready") is not True:
                raise RuntimeError(
                    f"Anime not ready: "
                    f"{item.get('title')}"
                )

            if item.get("published") is not True:
                raise RuntimeError(
                    f"Anime not published: "
                    f"{item.get('title')}"
                )

            video = Path(
                item["site_video"]
            )

            if (
                not video.exists()
                or video.stat().st_size < 10_000
            ):
                raise RuntimeError(
                    f"Anime video missing: "
                    f"{item.get('title')}"
                )

        for item in games:

            if item.get("real_build") is not True:
                raise RuntimeError(
                    f"Fake game build: "
                    f"{item.get('title')}"
                )

            if item.get("ready") is not True:
                raise RuntimeError(
                    f"Game not ready: "
                    f"{item.get('title')}"
                )

            if item.get("published") is not True:
                raise RuntimeError(
                    f"Game not published: "
                    f"{item.get('title')}"
                )

            build = Path(
                item["site_build"]
            )

            if (
                not build.exists()
                or build.stat().st_size <= 1024
            ):
                raise RuntimeError(
                    f"Game build missing: "
                    f"{item.get('title')}"
                )

        approval = {
            "approved": True,
            "real_assets_only": True,
            "anime": 30,
            "games": 30,
            "total": 60,
            "site_can_publish": True,
        }

        self.approval_file.write_text(
            json.dumps(
                approval,
                indent=2,
            ),
            encoding="utf-8",
        )

        print(
            "\n"
            "====================================\n"
            "       AJVYRA FINAL RELEASE\n"
            "====================================\n"
            "30 / 30 REAL ANIME       ✓\n"
            "30 / 30 REAL GAMES       ✓\n"
            "60 / 60 REAL ASSETS      ✓\n"
            "SITE RELEASE APPROVED    ✓\n"
            "====================================\n"
        )

        return True


if __name__ == "__main__":
    AJVYRAFinal60ReleaseGate().verify()
