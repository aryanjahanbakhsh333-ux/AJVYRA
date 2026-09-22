from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class AJVYRAAnimeSiteWatchGateway:

    def __init__(
        self,
        catalog_path: str = (
            "generated/anime_site/"
            "watchable_catalog.json"
        ),
    ):
        self.catalog_path = Path(
            catalog_path
        )

    def catalog(self) -> Dict[str, Any]:

        if not self.catalog_path.exists():
            return {
                "status": "NOT_READY",
                "total_watchable": 0,
                "anime": [],
            }

        return json.loads(
            self.catalog_path.read_text(
                encoding="utf-8"
            )
        )

    def get_anime(
        self,
        anime_id: str,
    ) -> Dict[str, Any]:

        catalog = self.catalog()

        for anime in catalog.get(
            "anime",
            [],
        ):
            if anime.get("anime_id") == anime_id:
                return anime

        return {
            "status": "NOT_FOUND",
            "anime_id": anime_id,
        }

    def can_watch(
        self,
        anime_id: str,
    ) -> bool:

        anime = self.get_anime(
            anime_id
        )

        return (
            anime.get("status")
            == "WATCHABLE"
            and bool(
                anime.get("watch_url")
            )
        )


if __name__ == "__main__":

    gateway = (
        AJVYRAAnimeSiteWatchGateway()
    )

    print(
        json.dumps(
            gateway.catalog(),
            ensure_ascii=False,
            indent=2,
        )
    )
