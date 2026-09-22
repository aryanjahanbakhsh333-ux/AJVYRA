from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class LiveReleaseDecision:
    ready: bool
    expected_movies: int
    actual_movies: int
    missing_films: tuple[str, ...]
    message: str


class AJVYRALiveCinematicReleaseGate:
    """
    Prevents a deployment from claiming that the cinematic library
    is complete unless all expected films are actually present in the
    browser-facing manifest.
    """

    def verify(
        self,
        manifest_path: str | Path,
        expected_film_ids: list[str],
    ) -> LiveReleaseDecision:
        path = Path(manifest_path)

        if not path.is_file():
            return LiveReleaseDecision(
                ready=False,
                expected_movies=len(expected_film_ids),
                actual_movies=0,
                missing_films=tuple(expected_film_ids),
                message="Release blocked: manifest does not exist.",
            )

        payload = json.loads(
            path.read_text(encoding="utf-8")
        )

        movies = payload.get("movies", [])

        if not isinstance(movies, list):
            movies = []

        available: set[str] = set()

        for movie in movies:
            if not isinstance(movie, Mapping):
                continue

            if not movie.get("watchable"):
                continue

            film_id = str(
                movie.get("film_id", "")
            ).strip()

            movie_url = str(
                movie.get("movie_url", "")
            ).strip()

            if film_id and movie_url:
                available.add(film_id)

        expected = {
            str(film_id).strip()
            for film_id in expected_film_ids
            if str(film_id).strip()
        }

        missing = tuple(
            sorted(expected - available)
        )

        ready = (
            len(missing) == 0
            and len(available) >= len(expected)
        )

        if ready:
            message = (
                f"Release verified: "
                f"{len(expected)} cinematic movies "
                "are available."
            )
        else:
            message = (
                f"Release blocked: "
                f"{len(missing)} cinematic movies "
                "are missing."
            )

        return LiveReleaseDecision(
            ready=ready,
            expected_movies=len(expected),
            actual_movies=len(available),
            missing_films=missing,
            message=message,
        )

    def save_report(
        self,
        decision: LiveReleaseDecision,
        output_path: str | Path,
    ) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload: dict[str, Any] = {
            "ready": decision.ready,
            "expected_movies": decision.expected_movies,
            "actual_movies": decision.actual_movies,
            "missing_films": list(
                decision.missing_films
            ),
            "message": decision.message,
        }

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
