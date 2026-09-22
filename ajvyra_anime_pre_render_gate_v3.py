from __future__ import annotations

import json
from pathlib import Path


class AJVYRAAnimePreRenderGateV3:

    REQUIRED_FILMS = 30

    def __init__(self, release_manifest: str):
        self.release_manifest = Path(release_manifest)

    def load(self) -> dict:
        if not self.release_manifest.exists():
            raise RuntimeError(
                "PRE-RENDER BLOCKED: release manifest does not exist."
            )

        return json.loads(
            self.release_manifest.read_text(
                encoding="utf-8"
            )
        )

    def verify(self) -> dict:
        manifest = self.load()

        films = manifest.get("films", [])

        if len(films) != self.REQUIRED_FILMS:
            raise RuntimeError(
                f"PRE-RENDER BLOCKED: "
                f"{self.REQUIRED_FILMS} films required, "
                f"{len(films)} found."
            )

        failures = []

        for film in films:
            film_id = film.get("id", "unknown")
            video = film.get("video")

            if not video:
                failures.append(
                    f"{film_id}: missing video path"
                )
                continue

            path = Path(video)

            if not path.exists():
                failures.append(
                    f"{film_id}: MP4 missing"
                )
                continue

            if path.stat().st_size <= 0:
                failures.append(
                    f"{film_id}: MP4 empty"
                )
                continue

            if path.suffix.lower() != ".mp4":
                failures.append(
                    f"{film_id}: not an MP4"
                )

        if failures:
            raise RuntimeError(
                "PRE-RENDER BLOCKED:\n"
                + "\n".join(failures)
            )

        return {
            "allowed": True,
            "films": 30,
            "message": (
                "All 30 anime files exist. "
                "Site rendering may proceed."
            ),
        }
