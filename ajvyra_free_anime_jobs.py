from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

from ajvyra_free_local_models import AnimeJob


NEGATIVE = (
    "low quality, blurry, distorted, deformed, "
    "extra fingers, extra limbs, duplicate character, "
    "flickering, broken anatomy, watermark, logo, "
    "text, subtitles, photorealistic live action"
)


def load_existing_catalog(
    root: Path
):
    file = root / "ajvyra_anime_studio.py"

    if not file.exists():
        raise FileNotFoundError(
            f"Existing catalog not found: {file}"
        )

    spec = importlib.util.spec_from_file_location(
        "ajvyra_existing_catalog",
        str(file)
    )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    spec.loader.exec_module(
        module
    )

    catalog = getattr(
        module,
        "ANIME",
        None
    )

    if catalog is None:
        raise RuntimeError(
            "ANIME catalog was not found."
        )

    if len(catalog) != 30:
        raise RuntimeError(
            f"Expected 30 anime, found {len(catalog)}"
        )

    return catalog


def seed_for(
    anime_number: int,
    segment_number: int
):
    value = (
        f"AJVYRA-{anime_number}-"
        f"{segment_number}"
    )

    digest = hashlib.sha256(
        value.encode()
    ).hexdigest()

    return int(
        digest[:8],
        16
    )


def make_jobs(
    root: Path,
    output: Path
):

    catalog = load_existing_catalog(
        root
    )

    jobs = []

    for anime in catalog:

        for index, segment in enumerate(
            anime.segments,
            start=1
        ):

            prompt = (
                "Original cinematic 2D anime. "
                f"Series: {anime.title}. "
                f"Genre: {anime.genre}. "
                f"Story: {anime.description}. "
                f"Scene: {segment}. "
                "Keep character identity consistent. "
                "Keep clothing and environment consistent. "
                "Expressive anime acting, cinematic "
                "camera movement, detailed background, "
                "smooth animation, dramatic lighting, "
                "original characters and original world. "
                "No copyrighted characters."
            )

            destination = (
                output
                / "anime"
                / f"anime_{anime.number:02d}"
                / "clips"
                / f"segment_{index:02d}.mp4"
            )

            jobs.append(
                AnimeJob(
                    job_id=(
                        f"anime_{anime.number:02d}_"
                        f"segment_{index:02d}"
                    ),
                    anime_number=anime.number,
                    anime_id=(
                        f"anime_{anime.number:02d}"
                    ),
                    segment_number=index,
                    segment_title=str(segment),
                    prompt=prompt,
                    negative_prompt=NEGATIVE,
                    output_file=str(
                        destination
                    ),
                )
            )

    return jobs
