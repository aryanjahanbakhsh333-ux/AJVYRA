"""
AJVYRA — REAL ANIME POSTER EXTRACTOR v2

Poster از خود ویدیوی واقعی گرفته می‌شود.
هیچ تصویر fake یا placeholder ساخته نمی‌شود.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class RealPosterExtractor:

    def __init__(
        self,
        ffmpeg_binary: str = "ffmpeg",
    ):
        self.ffmpeg = ffmpeg_binary

    def extract(
        self,
        video: Path,
        poster: Path,
        timestamp: float = 30.0,
    ) -> Path:

        if not video.exists():
            raise RuntimeError(
                f"Video missing: {video}"
            )

        poster.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            self.ffmpeg,
            "-y",
            "-ss",
            str(timestamp),
            "-i",
            str(video),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(poster),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Poster extraction failed:\n"
                + result.stderr[-3000:]
            )

        if not poster.exists():
            raise RuntimeError(
                "FFmpeg did not create poster."
            )

        if poster.stat().st_size < 10_000:
            raise RuntimeError(
                "Poster is suspiciously small."
            )

        return poster
