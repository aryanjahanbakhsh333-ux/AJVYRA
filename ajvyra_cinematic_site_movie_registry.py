from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
import subprocess


@dataclass
class RegisteredMovie:
    film_id: str
    title: str
    local_file: str
    duration_seconds: float
    sha256: str
    watchable: bool


class AJVYRACinematicSiteMovieRegistry:
    def __init__(
        self,
        production_root: str | Path = "public/cinematic_anime",
    ) -> None:
        self.root = Path(production_root)

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()

    def _duration(self, path: Path) -> float:
        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return 0.0

        try:
            return float(result.stdout.strip())
        except ValueError:
            return 0.0

    def inspect_movie(
        self,
        film_id: str,
        title: str,
    ) -> RegisteredMovie | None:

        movie_path = self.root / film_id / "movie.mp4"

        if not movie_path.exists():
            return None

        if movie_path.stat().st_size < 1024 * 1024:
            return None

        duration = self._duration(movie_path)

        if duration < 1500:
            return None

        checksum = self._sha256(movie_path)

        return RegisteredMovie(
            film_id=film_id,
            title=title,
            local_file=str(movie_path),
            duration_seconds=duration,
            sha256=checksum,
            watchable=True,
        )

    def build_registry(
        self,
        catalog: list[dict],
    ) -> list[RegisteredMovie]:

        registered: list[RegisteredMovie] = []

        for item in catalog:
            film_id = str(item["film_id"])
            title = str(item["title"])

            movie = self.inspect_movie(
                film_id=film_id,
                title=title,
            )

            if movie is not None:
                registered.append(movie)

        return registered

    def save_registry(
        self,
        movies: list[RegisteredMovie],
        output: str | Path,
    ) -> Path:

        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "version": "1",
            "watchable_count": len(movies),
            "movies": [
                {
                    "film_id": movie.film_id,
                    "title": movie.title,
                    "local_file": movie.local_file,
                    "duration_seconds": movie.duration_seconds,
                    "sha256": movie.sha256,
                    "watchable": movie.watchable,
                }
                for movie in movies
            ],
        }

        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return output_path
