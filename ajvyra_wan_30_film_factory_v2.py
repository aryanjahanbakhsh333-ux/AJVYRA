from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ajvyra_wan_30_film_shot_factory_v2 import (
    AJVYRA30FilmShotFactoryV2,
)


class AJVYRAWan30FilmFactoryV2:

    FILM_IDS = [
        "veylora",
        "aelvryn",
        "nyxara",
        "kaelith",
        "orivane",
        "zeravia",
        "vaelune",
        "ravelyth",
        "solvarya",
        "xaveren",
        "elyvara",
        "neravelle",
        "vaerith",
        "lunavyr",
        "averlyn",
        "neyvara",
        "elvaria",
        "virelya",
        "caelora",
        "seravyn",
        "mouravia",
        "noxelya",
        "vaelora",
        "eryndra",
        "neylith",
        "auralyne",
        "velmora",
        "seyravia",
        "oryvane",
        "luminarae",
    ]

    def __init__(
        self,
        shot_factory: AJVYRA30FilmShotFactoryV2,
        manifest_path: str,
    ):
        self.shot_factory = shot_factory
        self.manifest_path = Path(manifest_path)

    def load_manifest(self) -> dict[str, Any]:
        if not self.manifest_path.exists():
            raise FileNotFoundError(
                f"30-film production manifest not found: "
                f"{self.manifest_path}"
            )

        data = json.loads(
            self.manifest_path.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, dict):
            raise ValueError(
                "Film manifest must contain an object."
            )

        return data

    def validate_manifest(
        self,
        manifest: dict[str, Any],
    ) -> None:

        for film_id in self.FILM_IDS:

            film = manifest.get(film_id)

            if not isinstance(film, dict):
                raise ValueError(
                    f"Missing film manifest: {film_id}"
                )

            title = film.get("title")
            shots = film.get("shots")

            if not title:
                raise ValueError(
                    f"Missing title: {film_id}"
                )

            if not isinstance(shots, list) or not shots:
                raise ValueError(
                    f"No shots defined for: {film_id}"
                )

    def produce_all(
        self,
    ) -> dict[str, list[str]]:

        manifest = self.load_manifest()
        self.validate_manifest(manifest)

        results: dict[str, list[str]] = {}

        for film_id in self.FILM_IDS:

            film = manifest[film_id]

            generated = self.shot_factory.generate_film(
                film_id=film_id,
                film_title=film["title"],
                shots=film["shots"],
            )

            results[film_id] = [
                str(path)
                for path in generated
            ]

        return results
