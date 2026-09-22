from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class ReleaseVerification:
    required_movies: int
    watchable_movies: int
    missing_movies: list[str]
    ready: bool


class AJVYRACinematicReleaseVerifier:
    def __init__(
        self,
        expected_count: int = 30,
    ) -> None:
        self.expected_count = expected_count

    def verify(
        self,
        registry_path: str | Path,
    ) -> ReleaseVerification:

        path = Path(registry_path)

        if not path.exists():
            return ReleaseVerification(
                required_movies=self.expected_count,
                watchable_movies=0,
                missing_movies=["registry"],
                ready=False,
            )

        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        movies = data.get("movies", [])

        watchable = [
            movie
            for movie in movies
            if movie.get("watchable") is True
        ]

        missing_count = max(
            self.expected_count - len(watchable),
            0,
        )

        missing = []

        for movie in movies:
            if not movie.get("watchable"):
                missing.append(movie.get("film_id", "unknown"))

        for index in range(missing_count):
            missing.append(
                f"unproduced-film-{index + 1}"
            )

        return ReleaseVerification(
            required_movies=self.expected_count,
            watchable_movies=len(watchable),
            missing_movies=missing,
            ready=(
                len(watchable) >= self.expected_count
                and len(movies) >= self.expected_count
            ),
        )

    def save_report(
        self,
        verification: ReleaseVerification,
        output: str | Path,
    ) -> Path:

        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                {
                    "required_movies": verification.required_movies,
                    "watchable_movies": verification.watchable_movies,
                    "missing_movies": verification.missing_movies,
                    "ready": verification.ready,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
