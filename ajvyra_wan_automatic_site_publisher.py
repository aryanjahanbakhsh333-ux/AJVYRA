from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Optional


class AJVYRAWanAutomaticSitePublisher:

    def __init__(
        self,
        production_root: str | Path = (
            "production/wan_films"
        ),
        public_root: str | Path = "public",
        media_base_url: Optional[str] = None,
    ) -> None:

        self.production_root = Path(
            production_root
        )

        self.public_root = Path(
            public_root
        )

        self.media_base_url = (
            media_base_url.rstrip("/")
            if media_base_url
            else None
        )

    def publish_movie(
        self,
        film_id: str,
        title: str,
    ) -> dict:

        movie = (
            self.production_root
            / film_id
            / "movie.mp4"
        )

        if not movie.exists():

            raise RuntimeError(
                f"Movie does not exist: {film_id}"
            )

        if movie.stat().st_size <= 1024:

            raise RuntimeError(
                f"Movie is invalid: {film_id}"
            )

        checksum = (
            self._sha256(movie)
        )

        if self.media_base_url:

            movie_url = (
                f"{self.media_base_url}/"
                f"{film_id}/movie.mp4"
            )

        else:

            site_dir = (
                self.public_root
                / "cinematic_anime"
                / film_id
            )

            site_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            destination = (
                site_dir
                / "movie.mp4"
            )

            shutil.copy2(
                movie,
                destination,
            )

            movie_url = (
                f"/cinematic_anime/"
                f"{film_id}/movie.mp4"
            )

        entry = {
            "film_id": film_id,
            "title": title,
            "watchable": True,
            "movie_url": movie_url,
            "sha256": checksum,
            "file_size_bytes": (
                movie.stat().st_size
            ),
        }

        return entry

    def build_catalog(
        self,
        films: list[tuple[str, str]],
    ) -> dict:

        movies = []

        for film_id, title in films:

            try:

                entry = self.publish_movie(
                    film_id,
                    title,
                )

                movies.append(
                    entry
                )

            except RuntimeError as exc:

                print(
                    f"[SITE BLOCKED] "
                    f"{film_id}: {exc}"
                )

        catalog = {
            "version": 1,
            "total_watchable": len(
                movies
            ),
            "release_ready": (
                len(movies) == len(films)
            ),
            "movies": movies,
        }

        self.public_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            self.public_root
            / "cinematic_player_manifest.json"
        )

        path.write_text(
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
