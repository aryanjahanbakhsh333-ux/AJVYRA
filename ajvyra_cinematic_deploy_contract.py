from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import json


@dataclass(frozen=True)
class CinematicDeployMovie:
    film_id: str
    title: str
    movie_path: str
    duration_seconds: float
    sha256: str
    watchable: bool
    source: str = "ajvyra-cinematic-factory"


@dataclass
class CinematicDeployContract:
    version: str
    generated_at: str
    base_url: str
    movies: list[CinematicDeployMovie]

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "base_url": self.base_url,
            "movies": [asdict(movie) for movie in self.movies],
        }

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    @classmethod
    def load(cls, path: Path) -> "CinematicDeployContract":
        data = json.loads(path.read_text(encoding="utf-8"))

        movies = [
            CinematicDeployMovie(**movie)
            for movie in data.get("movies", [])
        ]

        return cls(
            version=str(data.get("version", "1")),
            generated_at=str(data.get("generated_at", "")),
            base_url=str(data.get("base_url", "")),
            movies=movies,
        )
