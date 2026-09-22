from __future__ import annotations

import json
from pathlib import Path


class AJVYRAAnimeSiteCatalogV3:

    def __init__(
        self,
        asset_index: str,
    ):
        self.asset_index = Path(
            asset_index
        )

    def load(self) -> dict:

        if not self.asset_index.exists():
            raise RuntimeError(
                "Anime catalog is unavailable."
            )

        data = json.loads(
            self.asset_index.read_text(
                encoding="utf-8"
            )
        )

        if data.get("anime_count") != 30:
            raise RuntimeError(
                "Anime catalog does not contain "
                "all 30 films."
            )

        return data

    def get_all(self) -> list[dict]:

        data = self.load()

        films = data.get(
            "assets",
            []
        )

        if len(films) != 30:
            raise RuntimeError(
                "Final site catalog requires "
                "30 ready anime assets."
            )

        return films

    def get(self, film_id: str) -> dict:

        for film in self.get_all():
            if film["id"] == film_id:
                return film

        raise KeyError(
            f"Anime not found: {film_id}"
        )
