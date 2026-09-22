from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any


class AJVYRACinematicSiteSync:

    def __init__(
        self,
        root: str | Path = "public/cinematic_anime",
        catalog_path: str | Path = (
            "public/cinematic_anime_catalog.json"
        ),
    ):
        self.root = Path(root)
        self.catalog_path = Path(catalog_path)

    def rebuild(
        self,
        film_titles: dict[str, str],
    ) -> dict[str, Any]:

        from ajvyra_cinematic_site_readiness import (
            AJVYRACinematicSiteReadiness,
        )

        checker = AJVYRACinematicSiteReadiness(
            self.root
        )

        entries = []

        for film_id, title in film_titles.items():

            result = checker.inspect(film_id)

            if not result.ready:
                continue

            movie = Path(result.movie_path)

            entries.append({
                "film_id": film_id,
                "title": title,
                "status": "READY",
                "watchable": True,
                "video_url": (
                    f"/cinematic_anime/"
                    f"{film_id}/movie.mp4"
                ),
                "duration_seconds": (
                    result.duration_seconds
                ),
                "sha256": self._sha256(movie),
            })

        payload = {
            "generated_by": (
                "AJVYRA Cinematic Site Sync"
            ),
            "total_ready": len(entries),
            "films": entries,
        }

        self.catalog_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.catalog_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return payload

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(
                lambda: handle.read(1024 * 1024),
                b"",
            ):
                digest.update(chunk)

        return digest.hexdigest()
