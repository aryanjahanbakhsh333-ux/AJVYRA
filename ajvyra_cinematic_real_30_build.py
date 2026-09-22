from __future__ import annotations

import argparse
from pathlib import Path

from ajvyra_cinematic_30_film_story_bible import (
    AJVYRACinematic30FilmStoryBible,
)
from ajvyra_cinematic_real_30_production_controller import (
    AJVYRACinematicReal30ProductionController,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare the real 30-film cinematic anime "
            "production jobs."
        )
    )

    parser.add_argument(
        "--film",
        help="Generate jobs for one film only.",
    )

    parser.add_argument(
        "--segments",
        type=int,
        default=225,
        help="Segments per film. 225 x 8s is about 30 minutes.",
    )

    parser.add_argument(
        "--root",
        default="production/cinematic_anime",
    )

    parser.add_argument(
        "--manifest",
        default=(
            "production/cinematic_anime/"
            "real_30_generation_manifest.json"
        ),
    )

    args = parser.parse_args()

    if args.film:
        AJVYRACinematic30FilmStoryBible.get(
            args.film
        )

    controller = (
        AJVYRACinematicReal30ProductionController(
            production_root=args.root,
            segment_duration=8,
        )
    )

    jobs = controller.create_jobs(
        film_id=args.film,
        segment_count=args.segments,
    )

    output = controller.save_job_manifest(
        jobs,
        args.manifest,
    )

    film_count = (
        len(
            {
                job.film_id
                for job in jobs
            }
        )
    )

    print(
        f"Created {len(jobs)} REAL video-generation jobs "
        f"for {film_count} film(s)."
    )

    print(
        f"Manifest: {Path(output)}"
    )

    print(
        "No placeholder videos were created."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
