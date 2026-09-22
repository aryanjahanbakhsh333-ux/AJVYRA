from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def check_requirements() -> None:
    missing = []

    if shutil.which("ffmpeg") is None:
        missing.append("ffmpeg")

    if shutil.which("ffprobe") is None:
        missing.append("ffprobe")

    if not (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    ):
        missing.append("GEMINI_API_KEY or GOOGLE_API_KEY")

    if missing:
        raise RuntimeError(
            "Missing requirements: "
            + ", ".join(missing)
        )


def build_factory():
    from ajvyra_cinematic_veo_real_runner import (
        AJVYRACinematicVeoRealRunner,
    )

    from ajvyra_cinematic_real_provider_bridge import (
        AJVYRACinematicRealProviderBridge,
    )

    from ajvyra_cinematic_segment_planner import (
        AJVYRACinematicSegmentPlanner,
    )

    from ajvyra_cinematic_real_film_factory import (
        AJVYRACinematicRealFilmFactory,
    )

    from ajvyra_cinematic_real_30_film_factory import (
        AJVYRACinematicReal30FilmFactory,
    )

    runner = AJVYRACinematicVeoRealRunner()

    provider = AJVYRACinematicRealProviderBridge(
        veo_runner=runner
    )

    planner = AJVYRACinematicSegmentPlanner(
        segment_seconds=8,
        target_minutes=30,
    )

    film_factory = AJVYRACinematicRealFilmFactory(
        provider=provider,
        planner=planner,
        root="public/cinematic_anime",
        retries=3,
    )

    factory = AJVYRACinematicReal30FilmFactory(
        film_factory=film_factory,
        root="public/cinematic_anime",
    )

    return factory


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA Real 30-Film Cinematic Factory"
        )
    )

    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="First film number.",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=30,
        help="Last film number.",
    )

    parser.add_argument(
        "--film",
        type=int,
        default=None,
        help="Generate only one film.",
    )

    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Regenerate existing segments.",
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show factory status only.",
    )

    args = parser.parse_args()

    try:
        check_requirements()

        factory = build_factory()

        if args.status:
            print(factory.status())
            return 0

        if args.film is not None:
            start = args.film
            end = args.film
        else:
            start = args.start
            end = args.end

        print()
        print("=" * 70)
        print("AJVYRA CINEMATIC REAL FILM FACTORY")
        print("=" * 70)
        print(
            f"Producing films {start} → {end}"
        )
        print(
            "Existing valid segments will be resumed."
        )
        print()

        result = factory.run(
            start=start,
            end=end,
            resume=not args.no_resume,
        )

        print()
        print("=" * 70)
        print("FACTORY RESULT")
        print("=" * 70)

        print(
            f"Requested: {result['requested']}"
        )
        print(
            f"Ready:    {result['ready']}"
        )
        print(
            f"Failed:   {result['failed']}"
        )

        for item in result["results"]:
            print(
                f"{item['film_id']:12} "
                f"{item['title']:15} "
                f"{item['status']}"
            )

        print()

        return (
            0
            if result["failed"] == 0
            else 2
        )

    except KeyboardInterrupt:
        print(
            "\nFactory stopped safely. "
            "Run again with --resume."
        )
        return 130

    except Exception as exc:
        print(
            f"\nFACTORY ERROR: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
