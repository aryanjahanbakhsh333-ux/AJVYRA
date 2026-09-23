from __future__ import annotations

import subprocess
from pathlib import Path


class QualityGate:

    def __init__(
        self,
        minimum_size=50_000
    ):
        self.minimum_size = (
            minimum_size
        )

    def check_video(
        self,
        file: Path
    ):

        errors = []

        if not file.exists():
            errors.append(
                "missing video"
            )
            return errors

        if file.stat().st_size < self.minimum_size:
            errors.append(
                "video is too small"
            )

        if file.suffix.lower() != ".mp4":
            errors.append(
                "video is not MP4"
            )

        try:

            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=nw=1:nk=1",
                    str(file)
                ],
                capture_output=True,
                text=True,
                check=True
            )

            duration = float(
                result.stdout.strip()
            )

            if duration <= 0:
                errors.append(
                    "video has zero duration"
                )

        except Exception as exc:

            errors.append(
                "ffprobe validation failed: "
                + str(exc)
            )

        return errors

    def check_anime(
        self,
        folder: Path
    ):

        clips = sorted(
            folder.glob(
                "clips/*.mp4"
            )
        )

        errors = []

        if not clips:
            errors.append(
                "no generated clips"
            )

        for clip in clips:
            errors.extend(
                self.check_video(
                    clip
                )
            )

        return errors
