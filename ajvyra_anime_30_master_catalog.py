from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass
class AnimeMasterEntry:
    anime_id: str
    title: str
    genre: str
    description: str
    season: int = 1
    first_episode: int = 1
    episode_duration_seconds: int = 1800
    production_status: str = "queued"
    published: bool = False


class AJVYRA30AnimeMasterCatalog:

    ANIME = [
        ("Veylora", "Fantasy"),
        ("Aelvryn", "Action"),
        ("Nyxara", "Horror"),
        ("Kaelith", "Romance"),
        ("Orivane", "Adventure"),
        ("Zeravia", "Sad"),
        ("Vaelune", "Heartbreak"),
        ("Ravelyth", "Fantasy"),
        ("Solvarya", "Action"),
        ("Xaveren", "Horror"),
        ("Elyvara", "Romance"),
        ("Neravelle", "Adventure"),
        ("Vaerith", "Sad"),
        ("Lunavyr", "Heartbreak"),
        ("Averlyn", "Fantasy"),
        ("Neyvara", "Action"),
        ("Elvaria", "Horror"),
        ("Virelya", "Romance"),
        ("Caelora", "Adventure"),
        ("Seravyn", "Sad"),
        ("Mouravia", "Heartbreak"),
        ("Noxelya", "Fantasy"),
        ("Vaelora", "Action"),
        ("Eryndra", "Horror"),
        ("Neylith", "Romance"),
        ("Auralyne", "Adventure"),
        ("Velmora", "Sad"),
        ("Seyravia", "Heartbreak"),
        ("Oryvane", "Fantasy"),
        ("Luminarae", "Action"),
    ]

    def __init__(
        self,
        root: str = "generated/anime_production",
    ):
        self.root = Path(root)

    def build(self) -> List[AnimeMasterEntry]:

        entries = []

        for index, (title, genre) in enumerate(
            self.ANIME,
            start=1,
        ):
            anime_id = f"anime_{index:02d}"

            entries.append(
                AnimeMasterEntry(
                    anime_id=anime_id,
                    title=title,
                    genre=genre,
                    description=(
                        f"An original AJVYRA {genre.lower()} "
                        f"anime centered around {title}."
                    ),
                )
            )

        return entries

    def save(self) -> Path:

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        entries = self.build()

        output = self.root / "30_anime_master_catalog.json"

        output.write_text(
            json.dumps(
                {
                    "total_anime": len(entries),
                    "episode_duration_seconds": 1800,
                    "entries": [
                        asdict(item)
                        for item in entries
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output


if __name__ == "__main__":
    path = AJVYRA30AnimeMasterCatalog().save()
    print(f"Catalog created: {path}")
