from __future__ import annotations

from pathlib import Path
import json


AJVYRA_30_FILMS = [
    "Veylora",
    "Aelvryn",
    "Nyxara",
    "Kaelith",
    "Orivane",
    "Zeravia",
    "Vaelune",
    "Ravelyth",
    "Solvarya",
    "Xaveren",
    "Elyvara",
    "Neravelle",
    "Vaerith",
    "Lunavyr",
    "Averlyn",
    "Neyvara",
    "Elvaria",
    "Virelya",
    "Caelora",
    "Seravyn",
    "Mouravia",
    "Noxelya",
    "Vaelora",
    "Eryndra",
    "Neylith",
    "Auralyne",
    "Velmora",
    "Seyravia",
    "Oryvane",
    "Luminarae",
]


class AJVYRACinematic30SiteCatalogBuilder:

    def __init__(
        self,
        output: str | Path = (
            "public/cinematic_anime_catalog.json"
        ),
    ):
        self.output = Path(output)

    def build(self) -> dict:

        titles = {
            f"anime_{index:02d}": title
            for index, title in enumerate(
                AJVYRA_30_FILMS,
                start=1,
            )
        }

        from ajvyra_cinematic_site_sync import (
            AJVYRACinematicSiteSync,
        )

        sync = AJVYRACinematicSiteSync(
            catalog_path=self.output
        )

        return sync.rebuild(titles)


if __name__ == "__main__":
    result = (
        AJVYRACinematic30SiteCatalogBuilder()
        .build()
    )

    print(
        f"Ready films: {result['total_ready']}"
    )
