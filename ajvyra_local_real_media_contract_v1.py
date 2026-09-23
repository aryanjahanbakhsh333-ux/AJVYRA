"""
AJVYRA — LOCAL REAL MEDIA CONTRACT v1

قانون اصلی:
این پروژه فقط Media واقعی را قبول می‌کند.

هیچ placeholder، فایل خالی، فایل جعلی یا manifest-only
به عنوان خروجی معتبر پذیرفته نمی‌شود.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


MIN_VIDEO_BYTES = 100_000
MIN_VIDEO_DURATION_SECONDS = 1.0


@dataclass(frozen=True)
class RealMediaRequirement:
    anime_number: int
    segment_number: int
    required_duration: float
    output_path: Path
    prompt: str


@dataclass(frozen=True)
class RealMediaResult:
    path: Path
    duration_seconds: float
    size_bytes: int
    is_real: bool
    reason: str = ""


def is_real_media_file(path: Path) -> bool:
    if not path.exists():
        return False

    if not path.is_file():
        return False

    if path.stat().st_size < MIN_VIDEO_BYTES:
        return False

    return True


def require_real_media(path: Path) -> None:
    if not is_real_media_file(path):
        raise RuntimeError(
            f"REAL MEDIA REQUIRED: invalid or missing media: {path}"
        )


def require_range(value: int, minimum: int, maximum: int, name: str) -> None:
    if not minimum <= value <= maximum:
        raise ValueError(
            f"{name} must be between {minimum} and {maximum}; got {value}"
        )


def require_anime_number(number: int) -> None:
    require_range(number, 1, 30, "anime_number")


def require_segment_number(number: int) -> None:
    require_range(number, 1, 12, "segment_number")


def expected_segment_path(root: Path, anime_number: int, segment_number: int) -> Path:
    require_anime_number(anime_number)
    require_segment_number(segment_number)

    return (
        root
        / f"anime_{anime_number:02d}"
        / "segments"
        / f"segment_{segment_number:02d}.mp4"
    )


def expected_final_path(root: Path, anime_number: int) -> Path:
    require_anime_number(anime_number)

    return (
        root
        / f"anime_{anime_number:02d}"
        / "video"
        / "main.mp4"
    )
