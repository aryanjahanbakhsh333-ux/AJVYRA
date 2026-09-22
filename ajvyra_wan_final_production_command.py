from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ajvyra_wan_final_cinematic_release_factory import (
    AJVYRAWanFinalCinematicReleaseFactory,
)

from ajvyra_wan_final_30_release_gate import (
    AJVYRAWanFinal30ReleaseGate,
)


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA final local Wan cinematic "
            "production and release system"
        )
    )

    parser.add_argument(
        "--film",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--start",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--end",
        type=int,
        default=30,
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=1800,
    )

    parser.add_argument(
        "--model",
        default=(
            "Wan-AI/"
            "Wan2.1-T2V-1.3B-Diffusers"
        ),
    )

    parser.add_argument(
        "--site-only",
        action="store_true",
    )

    args = parser.parse_args()

    if args.site_only:

        gate = (
            AJVYRAWanFinal30ReleaseGate()
        )

        release = gate.build(
            expected=30
        )

        return (
            0
            if release.release_ready
            else 2
        )

    factory = (
        AJVYRAWanFinalCinematicReleaseFactory(
            model_id=args.model
        )
    )

    stories = factory.story.all()

    if args.film:

        selected = [
            story
            for story in stories
            if story.film_id == args.film
        ]

        if not selected:

            print(
                f"Film not found: {args.film}"
            )

            return 2

    else:

        selected = stories[
            max(0, args.start - 1):
            min(args.end, len(stories))
        ]

    print()
    print(
        "======================================"
    )
    print(
        "   AJVYRA FINAL WAN FILM FACTORY"
    )
    print(
        "======================================"
    )

    print(
        f"Films selected: {len(selected)}"
    )

    for index, story in enumerate(
        selected,
        start=1,
    ):

        print()
        print(
            f"[{index}/{len(selected)}] "
            f"{story.title}"
        )

        result = (
            factory.create_release(
                film_id=story.film_id,
                duration_seconds=args.duration,
            )
        )

        if result.final_movie_ready:

            print(
                f"READY: {story.title}"
            )

        else:

            print(
                f"FAILED: {story.title}"
            )

            print(
                f"ERROR: {result.error}"
            )

            print(
                "Production continues with "
                "the next film."
            )

    print()
    print(
        "Building final website release..."
    )

    gate = (
        AJVYRAWanFinal30ReleaseGate()
    )

    release = gate.build(
        expected=30
    )

    print()
    print(
        "======================================"
    )
    print(
        "           FINAL RESULT"
    )
    print(
        "======================================"
    )

    print(
        f"Real movies on site: "
        f"{release.ready}/30"
    )

    if release.release_ready:

        print(
            "AJVYRA RELEASE READY."
        )

        return 0

    print(
        "AJVYRA RELEASE BLOCKED."
    )

    print(
        "Every one of the 30 films must have "
        "a valid real final MP4."
    )

    return 2


if __name__ == "__main__":
    sys.exit(
        main()
    )
