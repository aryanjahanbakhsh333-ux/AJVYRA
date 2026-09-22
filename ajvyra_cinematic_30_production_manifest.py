from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class CinematicFilmManifest:
    film_id: str
    title: str
    genre: str
    duration_seconds: int = 1800

    primary_language: str = "fa"
    subtitle_languages: List[str] = field(
        default_factory=lambda: ["fa", "en", "ja"]
    )

    status: str = "queued"

    output_directory: str = ""
    final_movie: str = ""

    metadata: Dict = field(
        default_factory=dict
    )


class AJVYRACinematic30ProductionManifest:

    def __init__(
        self,
        root: str | Path = "cinematic_production",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.films: Dict[
            str,
            CinematicFilmManifest
        ] = {}

    def add(
        self,
        manifest: CinematicFilmManifest,
    ) -> None:

        if manifest.film_id in self.films:
            raise ValueError(
                f"Duplicate film id: {manifest.film_id}"
            )

        film_root = (
            self.root / manifest.film_id
        )

        film_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifest.output_directory = str(
            film_root
        )

        manifest.final_movie = str(
            film_root / "movie.mp4"
        )

        self.films[
            manifest.film_id
        ] = manifest

    def get(
        self,
        film_id: str,
    ) -> CinematicFilmManifest:

        if film_id not in self.films:
            raise KeyError(
                f"Unknown film: {film_id}"
            )

        return self.films[film_id]

    def save(
        self,
        filename: str = "manifest_30.json",
    ) -> Path:

        path = self.root / filename

        path.write_text(
            json.dumps(
                {
                    "films": [
                        asdict(film)
                        for film in self.films.values()
                    ]
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    @property
    def count(self) -> int:
        return len(self.films)
