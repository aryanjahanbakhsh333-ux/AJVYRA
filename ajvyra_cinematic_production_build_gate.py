from __future__ import annotations

from pathlib import Path
import json
from typing import Any


class AJVYRACinematicProductionBuildGate:

    def __init__(
        self,
        catalog_path: str | Path = (
            "public/cinematic_anime_catalog.json"
        ),
    ):
        self.catalog_path = Path(catalog_path)

    def validate(self) -> dict[str, Any]:

        if not self.catalog_path.exists():
            return {
                "allowed": False,
                "ready": 0,
                "error": (
                    "Cinematic catalog does not exist."
                ),
            }

        try:
            catalog = json.loads(
                self.catalog_path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception as exc:
            return {
                "allowed": False,
                "ready": 0,
                "error": str(exc),
            }

        films = catalog.get("films", [])

        invalid = []

        for film in films:

            movie_url = film.get("video_url")
            film_id = film.get("film_id")

            if not movie_url or not film_id:
                invalid.append(film_id)

        return {
            "allowed": len(invalid) == 0,
            "ready": len(films),
            "invalid": invalid,
            "error": None,
        }

    def require_valid(self) -> None:

        result = self.validate()

        if not result["allowed"]:
            raise RuntimeError(
                "Cinematic production build gate failed: "
                + str(result)
            )
