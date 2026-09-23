"""
AJVYRA — REAL ANIME DURATION LOCK v2

هر anime نهایی باید تقریباً دقیقاً 30:00 باشد.

تلورانس بسیار کوچک فقط برای خطای container/timestamp است.
"""

from __future__ import annotations

from pathlib import Path

from ajvyra_real_ffprobe_validator_v1 import (
    RealVideoValidator,
)


TARGET_SECONDS = 1800.0
MIN_SECONDS = 1799.0
MAX_SECONDS = 1801.0


class AnimeDurationLock:

    def __init__(
        self,
        ffprobe_binary: str = "ffprobe",
    ):
        self.validator = RealVideoValidator(
            ffprobe_binary
        )

    def validate(
        self,
        path: Path,
    ):

        probe = self.validator.require_valid(
            path,
            minimum_duration=MIN_SECONDS,
        )

        if probe.duration > MAX_SECONDS:
            raise RuntimeError(
                f"Anime is longer than allowed: "
                f"{probe.duration:.3f}s"
            )

        return probe

    def require_30_minutes(
        self,
        path: Path,
    ):

        probe = self.validate(path)

        return {
            "path": str(path),
            "duration_seconds": probe.duration,
            "target_seconds": TARGET_SECONDS,
            "within_lock": True,
        }
