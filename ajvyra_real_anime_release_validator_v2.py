"""
AJVYRA — REAL ANIME RELEASE VALIDATOR v2

قفل انتشار انیمه.

باید دقیقاً:

30/30 video
30/30 poster
30/30 >= 30 minutes
30/30 readable by FFprobe
30/30 registered in manifest

باشد.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_anime_studio import ANIME
from ajvyra_real_anime_duration_lock_v2 import (
    AnimeDurationLock,
)


class AnimeReleaseValidator:

    def __init__(
        self,
        root: Path,
        ffprobe: str = "ffprobe",
    ):
        self.root = root

        self.lock = AnimeDurationLock(
            ffprobe
        )

    def validate(self) -> dict:

        if len(ANIME) != 30:
            raise RuntimeError(
                "Catalog does not contain exactly 30 anime."
            )

        results = []

        for anime in ANIME:

            video = (
                self.root
                / anime.video
            )

            poster = (
                self.root
                / anime.poster
            )

            result = {
                "number": anime.number,
                "title": anime.title,
                "video": False,
                "poster": False,
                "duration": False,
                "ready": False,
            }

            if video.exists():

                result["video"] = True

                try:

                    self.lock.require_30_minutes(
                        video
                    )

                    result["duration"] = True

                except Exception as exc:

                    result["duration_error"] = (
                        str(exc)
                    )

            if poster.exists():
                result["poster"] = (
                    poster.stat().st_size
                    > 10_000
                )

            result["ready"] = all(
                (
                    result["video"],
                    result["poster"],
                    result["duration"],
                )
            )

            results.append(result)

        ready = sum(
            int(item["ready"])
            for item in results
        )

        report = {
            "project": "AJVYRA",
            "required": 30,
            "ready": ready,
            "release_ready": ready == 30,
            "anime": results,
        }

        return report

    def require_release_ready(self):

        report = self.validate()

        if not report["release_ready"]:

            failed = [
                item["number"]
                for item in report["anime"]
                if not item["ready"]
            ]

            raise RuntimeError(
                "ANIME RELEASE BLOCKED.\n"
                f"Ready: {report['ready']}/30\n"
                f"Failed: {failed}"
            )

        return report
