from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class AJVYRAExternalMediaManifest:

    def __init__(
        self,
        public_root: str | Path = "public",
        media_base_url: str | None = None,
    ) -> None:

        self.public_root = Path(
            public_root
        )

        self.media_base_url = (
            media_base_url.rstrip("/")
            if media_base_url
            else None
        )

    def build(
        self,
        films: list[dict[str, Any]],
    ) -> dict[str, Any]:

        entries = []

        for film in films:

            film_id = film[
                "film_id"
            ]

            movie_path = Path(
                film[
                    "movie_path"
                ]
            )

            if not movie_path.exists():
                continue

            if movie_path.stat().st_size <= 1024:
                continue

            checksum = self._sha256(
                movie_path
            )

            if self.media_base_url:

                movie_url = (
                    f"{self.media_base_url}/"
                    f"{film_id}/movie.mp4"
                )

            else:

                movie_url = (
                    f"/cinematic_anime/"
                    f"{film_id}/movie.mp4"
                )

            entries.append(
                {
                    "film_id": film_id,
                    "title": film.get(
                        "title",
                        film_id,
                    ),
                    "watchable": True,
                    "movie_url": movie_url,
                    "duration_seconds": film.get(
                        "duration_seconds",
                        0,
                    ),
                    "sha256": checksum,
                    "file_size_bytes": (
                        movie_path.stat().st_size
                    ),
                }
            )

        catalog = {
            "version": 1,
            "type": "AJVYRA_CINEMATIC_CATALOG",
            "watchable_count": len(
                entries
            ),
            "movies": entries,
        }

        output = (
            self.public_root
            / "cinematic_player_manifest.json"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                catalog,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return catalog

    @staticmethod
    def _sha256(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as file:

            while True:

                chunk = file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()
