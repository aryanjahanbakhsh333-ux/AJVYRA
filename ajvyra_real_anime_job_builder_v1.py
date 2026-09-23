"""
AJVYRA — REAL ANIME JOB BUILDER v1

۳۰ انیمه × ۱۲ بخش واقعی

هر بخش:
۱۵۰ ثانیه

هر انیمه:
۱۲ × ۱۵۰ = ۱۸۰۰ ثانیه = ۳۰ دقیقه
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ajvyra_anime_studio import ANIME


@dataclass(frozen=True)
class RealAnimeSegmentJob:
    anime_number: int
    anime_title: str
    segment_number: int
    segment_title: str
    duration_seconds: int
    prompt: str
    seed: int
    output_path: Path


def stable_seed(*values: Any) -> int:
    raw = "|".join(
        str(value)
        for value in values
    )

    digest = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()

    return int(
        digest[:12],
        16,
    )


def build_anime_jobs(
    production_root: Path,
) -> list[RealAnimeSegmentJob]:

    if len(ANIME) != 30:
        raise RuntimeError(
            f"AJVYRA catalog must contain 30 anime; found {len(ANIME)}."
        )

    jobs = []

    for anime in ANIME:

        if len(anime.segments) != 12:
            raise RuntimeError(
                f"{anime.title} does not contain 12 segments."
            )

        for index, segment_title in enumerate(
            anime.segments,
            start=1,
        ):

            seed = stable_seed(
                "AJVYRA",
                anime.number,
                index,
            )

            prompt = (
                "Original anime cinematic scene. "
                f"Series: {anime.title}. "
                f"Genre: {anime.genre}. "
                f"Mood: {anime.mood}. "
                f"Story: {anime.logline}. "
                f"Scene: {segment_title}. "
                "Maintain consistent original characters, "
                "wardrobe, environment and cinematic identity. "
                "Professional animated cinematography, "
                "clear action, coherent motion, "
                "detailed backgrounds, intentional camera movement. "
                "No copyrighted characters, no logos, no text overlays."
            )

            output = (
                production_root
                / f"anime_{anime.number:02d}"
                / "segments"
                / f"segment_{index:02d}.mp4"
            )

            jobs.append(
                RealAnimeSegmentJob(
                    anime_number=anime.number,
                    anime_title=anime.title,
                    segment_number=index,
                    segment_title=segment_title,
                    duration_seconds=150,
                    prompt=prompt,
                    seed=seed,
                    output_path=output,
                )
            )

    if len(jobs) != 360:
        raise RuntimeError(
            f"Expected 360 real segment jobs; got {len(jobs)}."
        )

    return jobs
