from __future__ import annotations

import json
from pathlib import Path


class AJVYRAWan30ReleaseLockV2:

    REQUIRED_FILMS = 30

    def __init__(
        self,
        manifest_path: str,
    ):
        self.manifest_path = Path(
            manifest_path
        )

    def verify(
        self,
    ) -> dict:

        if not self.manifest_path.exists():
            raise RuntimeError(
                "AJVYRA release is blocked: "
                "final manifest does not exist."
            )

        data = json.loads(
            self.manifest_path.read_text(
                encoding="utf-8"
            )
        )

        films = data.get(
            "films",
            []
        )

        if len(films) != self.REQUIRED_FILMS:
            raise RuntimeError(
                "AJVYRA release blocked: "
                f"expected {self.REQUIRED_FILMS} films, "
                f"found {len(films)}."
            )

        for film in films:

            if film.get("status") != "READY":
                raise RuntimeError(
                    "AJVYRA release blocked: "
                    f"{film.get('id')} is not READY."
                )

            video = Path(
                film.get(
                    "video",
                    "",
                )
            )

            if not video.exists():
                raise RuntimeError(
                    "AJVYRA release blocked: "
                    f"missing video for {film.get('id')}"
                )

            if video.stat().st_size <= 0:
                raise RuntimeError(
                    "AJVYRA release blocked: "
                    f"empty video for {film.get('id')}"
                )

        return {
            "release_allowed": True,
            "film_count": len(films),
            "project": "AJVYRA",
        }
