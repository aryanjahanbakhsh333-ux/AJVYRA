"""
AJVYRA 30-Minute Film Duration Expander V1

Converts an existing AJVYRA production queue into a long-form
30-minute film plan.

No video is faked or marked READY.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGET_MINUTES = 30
TARGET_SECONDS = TARGET_MINUTES * 60
CLIP_SECONDS = 5
SHOTS_PER_FILM = TARGET_SECONDS // CLIP_SECONDS


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(path)


def expand_queue(source, destination):
    data = load(source)
    jobs = data.get("jobs", [])

    films = {}

    for job in jobs:
        films.setdefault(
            job["film_id"],
            {
                "film": job["film_title"],
                "jobs": []
            }
        )["jobs"].append(job)

    expanded = []

    for film_id, film_data in films.items():
        original = film_data["jobs"]

        for index in range(SHOTS_PER_FILM):
            template = original[index % len(original)].copy()

            scene_number = (index // 6) + 1
            shot_number = (index % 6) + 1

            template["scene_number"] = scene_number
            template["shot_number"] = shot_number

            template["job_id"] = (
                f"{film_id}-"
                f"scene-{scene_number:03d}-"
                f"shot-{shot_number:02d}"
            )

            template["status"] = "QUEUED"

            template["output_file"] = str(
                Path("outputs")
                / film_data["film"]
                / f"scene_{scene_number:03d}"
                / f"shot_{shot_number:02d}.mp4"
            )

            expanded.append(template)

    output = {
        "schema": "AJVYRA_30_MINUTE_PRODUCTION_QUEUE",
        "target_minutes": TARGET_MINUTES,
        "estimated_clip_seconds": CLIP_SECONDS,
        "shots_per_film": SHOTS_PER_FILM,
        "jobs": expanded
    }

    save(destination, output)

    print("AJVYRA 30-MINUTE QUEUE")
    print(f"Films: {len(films)}")
    print(f"Shots per film: {SHOTS_PER_FILM}")
    print(f"Total shots: {len(expanded)}")
    print(f"Output: {destination}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True
    )

    parser.add_argument(
        "--output",
        required=True
    )

    args = parser.parse_args()

    expand_queue(
        Path(args.input),
        Path(args.output)
    )


if __name__ == "__main__":
    main()
