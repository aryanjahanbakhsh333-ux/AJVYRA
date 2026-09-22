from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ajvyra_cinematic_30_film_release_controller import (
    AJVYRA_30_FILMS,
)


class AJVYRAFinalCinematicReleaseGate:

    EXPECTED_FILMS = 30

    def __init__(
        self,
        production_root: str | Path = (
            "production/ajvyra_cinematic"
        ),
        public_root: str | Path = "public",
    ) -> None:

        self.production_root = Path(
            production_root
        )

        self.public_root = Path(
            public_root
        )

    def verify(
        self,
    ) -> dict[str, Any]:

        movies = []

        missing = []

        invalid = []

        for film_id, title in AJVYRA_30_FILMS:

            state_path = (
                self.production_root
                / film_id
                / "factory_state.json"
            )

            if not state_path.exists():

                missing.append(
                    {
                        "film_id": film_id,
                        "title": title,
                        "reason": (
                            "No production state."
                        ),
                    }
                )

                continue

            try:

                state = json.loads(
                    state_path.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception as exc:

                invalid.append(
                    {
                        "film_id": film_id,
                        "title": title,
                        "reason": str(exc),
                    }
                )

                continue

            movie_path = state.get(
                "movie_path"
            )

            if (
                not state.get(
                    "qc_passed",
                    False,
                )
                or not state.get(
                    "site_ready",
                    False,
                )
                or not movie_path
            ):

                invalid.append(
                    {
                        "film_id": film_id,
                        "title": title,
                        "reason": (
                            "QC/site readiness failed."
                        ),
                    }
                )

                continue

            movie = Path(
                movie_path
            )

            if not movie.exists():

                invalid.append(
                    {
                        "film_id": film_id,
                        "title": title,
                        "reason": (
                            "Movie file missing."
                        ),
                    }
                )

                continue

            if movie.stat().st_size <= 1024:

                invalid.append(
                    {
                        "film_id": film_id,
                        "title": title,
                        "reason": (
                            "Movie file is empty "
                            "or invalid."
                        ),
                    }
                )

                continue

            movies.append(
                {
                    "film_id": film_id,
                    "title": title,
                    "movie_path": str(movie),
                    "duration_seconds": state.get(
                        "duration_seconds",
                        0,
                    ),
                }
            )

        ready = (
            len(movies)
            == self.EXPECTED_FILMS
            and not missing
            and not invalid
        )

        result = {
            "release_ready": ready,
            "expected": self.EXPECTED_FILMS,
            "actual_ready": len(movies),
            "missing": missing,
            "invalid": invalid,
            "movies": movies,
        }

        self._save(
            result
        )

        if not ready:

            raise RuntimeError(
                "AJVYRA CINEMATIC RELEASE BLOCKED: "
                f"{len(movies)}/30 real films are ready."
            )

        return result

    def _save(
        self,
        result: dict[str, Any],
    ) -> None:

        self.public_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            self.public_root
            / "cinematic_release_gate.json"
        )

        path.write_text(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
