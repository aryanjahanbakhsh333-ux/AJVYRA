"""
AJVYRA — REAL ANIME WEB MANIFEST v2

Manifest فقط animeهایی را وارد سایت می‌کند که
ویدیوی واقعی و معتبر دارند.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_anime_studio import (
    ANIME,
)

from ajvyra_real_anime_duration_lock_v2 import (
    AnimeDurationLock,
)


class RealAnimeManifestBuilder:

    def __init__(
        self,
        root: Path,
        ffprobe: str = "ffprobe",
    ):
        self.root = root

        self.lock = AnimeDurationLock(
            ffprobe
        )

    def build(self) -> dict:

        if len(ANIME) != 30:
            raise RuntimeError(
                "Anime catalog is not exactly 30."
            )

        items = []

        for anime in ANIME:

            video = (
                self.root
                / anime.video
            )

            poster = (
                self.root
                / anime.poster
            )

            if not video.exists():
                raise RuntimeError(
                    f"Missing real anime video: "
                    f"{video}"
                )

            if not poster.exists():
                raise RuntimeError(
                    f"Missing real anime poster: "
                    f"{poster}"
                )

            duration = self.lock.require_30_minutes(
                video
            )

            items.append(
                {
                    "id": f"anime-{anime.number:02d}",
                    "number": anime.number,
                    "title": anime.title,
                    "title_fa": anime.title_fa,
                    "title_ja": anime.title_ja,
                    "genre": anime.genre,
                    "mood": anime.mood,
                    "description": anime.logline,
                    "duration_seconds": duration[
                        "duration_seconds"
                    ],
                    "video": anime.video,
                    "poster": anime.poster,
                    "available": True,
                }
            )

        return {
            "project": "AJVYRA",
            "type": "anime",
            "count": 30,
            "runtime_seconds": 1800,
            "items": items,
        }

    def write(
        self,
        destination: Path,
    ) -> Path:

        manifest = self.build()

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return destination
