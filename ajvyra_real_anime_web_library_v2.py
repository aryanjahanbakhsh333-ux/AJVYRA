"""
AJVYRA — REAL ANIME WEB LIBRARY v2

یک لایه ساده و framework-independent برای سایت.

Frontend می‌تواند این manifest را بخواند و ویدیوها را مستقیماً
از مسیرهای واقعی پخش کند.
"""

from __future__ import annotations

import json
from pathlib import Path


class RealAnimeWebLibrary:

    def __init__(
        self,
        manifest_path: Path,
    ):
        self.manifest_path = manifest_path

        if not manifest_path.exists():
            raise FileNotFoundError(
                f"Anime manifest missing: "
                f"{manifest_path}"
            )

        self.data = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

        if self.data.get("count") != 30:
            raise RuntimeError(
                "Web library must contain exactly 30 anime."
            )

    def all(self) -> list[dict]:
        return list(
            self.data["items"]
        )

    def get(
        self,
        anime_number: int,
    ) -> dict:

        for item in self.data["items"]:

            if item["number"] == anime_number:
                return item

        raise KeyError(
            f"Anime {anime_number} not found."
        )

    def search(
        self,
        query: str,
    ) -> list[dict]:

        query = query.strip().lower()

        return [
            item
            for item in self.data["items"]
            if (
                query in item["title"].lower()
                or query in item["title_fa"].lower()
                or query in item["genre"].lower()
            )
        ]

    def require_all_available(self):

        if len(self.data["items"]) != 30:
            raise RuntimeError(
                "Not all 30 anime are registered."
            )

        for item in self.data["items"]:

            if not item.get("available"):
                raise RuntimeError(
                    f"Anime unavailable: "
                    f"{item['number']}"
                )

            if item.get(
                "duration_seconds",
                0,
            ) < 1799:
                raise RuntimeError(
                    f"Anime duration invalid: "
                    f"{item['number']}"
                )

        return True
