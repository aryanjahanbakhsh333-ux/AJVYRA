from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from ajvyra_cinematic_local_production_qc import (
    AJVYRACinematicLocalProductionQC,
    LocalFilmQCResult,
)


class AJVYRACinematicLocalReleaseRunner:

    def __init__(
        self,
        production_root: str | Path = (
            "production/cinematic_local"
        ),
        public_root: str | Path = "public",
        expected_films: int = 30,
    ) -> None:

        self.production_root = Path(
            production_root
        )

        self.public_root = Path(
            public_root
        )

        self.expected_films = (
            expected_films
        )

        self.qc = (
            AJVYRACinematicLocalProductionQC(
                minimum_duration_seconds=1.0,
                maximum_duration_seconds=7200.0,
            )
        )

    def verify_and_prepare_release(
        self,
        films: Iterable[
            tuple[str, str]
        ],
    ) -> dict:

        film_list = list(films)

        results: list[
            LocalFilmQCResult
        ] = []

        for film_id, movie_path in film_list:

            result = self.qc.check(
                film_id,
                movie_path,
            )

            results.append(result)

        passed = [
            result
            for result in results
            if result.passed
        ]

        release_ready = (
            len(film_list)
            == self.expected_films
            and len(passed)
            == self.expected_films
        )

        manifest = {
            "release_ready": release_ready,
            "expected_films": self.expected_films,
            "checked_films": len(film_list),
            "watchable_films": len(passed),
            "blocked_films": [
                result.film_id
                for result in results
                if not result.passed
            ],
            "movies": [
                {
                    "film_id": result.film_id,
                    "duration_seconds": (
                        result.duration_seconds
                    ),
                    "watchable": True,
                }
                for result in passed
            ],
            "qc": [
                asdict(result)
                for result in results
            ],
        }

        self._save_manifest(
            manifest
        )

        if not release_ready:

            raise RuntimeError(
                "RELEASE BLOCKED: "
                f"{len(passed)}/"
                f"{self.expected_films} "
                "required cinematic films passed QC."
            )

        return manifest

    def discover_movies(
        self,
    ) -> list[tuple[str, str]]:

        movies: list[
            tuple[str, str]
        ] = []

        if not self.production_root.exists():
            return movies

        for film_dir in sorted(
            self.production_root.iterdir()
        ):

            if not film_dir.is_dir():
                continue

            movie = (
                film_dir
                / "movie.mp4"
            )

            if movie.exists():
                movies.append(
                    (
                        film_dir.name,
                        str(movie),
                    )
                )

        return movies

    def release_from_production(
        self,
    ) -> dict:

        movies = (
            self.discover_movies()
        )

        return self.verify_and_prepare_release(
            movies
        )

    def _save_manifest(
        self,
        manifest: dict,
    ) -> Path:

        self.public_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            self.public_root
            / "cinematic_local_release.json"
        )

        path.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path


def main() -> int:

    runner = (
        AJVYRACinematicLocalReleaseRunner()
    )

    try:

        manifest = (
            runner.release_from_production()
        )

        print(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0

    except RuntimeError as exc:

        print(str(exc))

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
