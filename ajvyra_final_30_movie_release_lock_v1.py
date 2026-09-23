"""
AJVYRA Final 30-Movie Release Lock V1

The website may only be published when all 30 final MP4 files exist.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


FILMS = [
    "Veylora",
    "Aelvryn",
    "Nyxara",
    "Kaelith",
    "Orivane",
    "Zeravia",
    "Vaelune",
    "Ravelyth",
    "Solvarya",
    "Xaveren",
    "Elyvara",
    "Neravelle",
    "Vaerith",
    "Lunavyr",
    "Averlyn",
    "Neyvara",
    "Elvaria",
    "Virelya",
    "Caelora",
    "Seravyn",
    "Mouravia",
    "Noxelya",
    "Vaelora",
    "Eryndra",
    "Neylith",
    "Auralyne",
    "Velmora",
    "Seyravia",
    "Oryvane",
    "Luminarae",
]


def now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--movies",
        required=True
    )

    parser.add_argument(
        "--manifest",
        required=True
    )

    args = parser.parse_args()

    movie_root = Path(
        args.movies
    )

    releases = []

    for number, title in enumerate(
        FILMS,
        start=1
    ):

        film_id = (
            f"ajv-film-{number:02d}-"
            f"{title.lower()}"
        )

        movie = (
            movie_root /
            f"{film_id}.mp4"
        )

        ready = (
            movie.exists()
            and movie.is_file()
            and movie.stat().st_size > 1024
        )

        releases.append({
            "number": number,
            "id": film_id,
            "title": title,
            "ready": ready,
            "video": str(movie)
            if ready else None
        })

    all_ready = all(
        item["ready"]
        for item in releases
    )

    manifest = {
        "project": "AJVYRA",
        "generated_at": now(),
        "total_anime": 30,
        "ready_anime": sum(
            item["ready"]
            for item in releases
        ),
        "release_approved": all_ready,
        "website_publish_allowed": all_ready,
        "anime": releases
    }

    manifest_path = Path(
        args.manifest
    )

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        manifest_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            manifest,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(
        f"AJVYRA: "
        f"{manifest['ready_anime']}/30 films ready."
    )

    if not all_ready:
        print(
            "RELEASE LOCKED."
        )
        raise SystemExit(1)

    print(
        "RELEASE APPROVED."
    )


if __name__ == "__main__":
    main()
