from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from ajvyra_cinematic_30_film_release_controller import (
    AJVYRA30FilmReleaseController,
)

from ajvyra_cinematic_final_release_gate import (
    AJVYRAFinalCinematicReleaseGate,
)

from ajvyra_cinematic_external_media_manifest import (
    AJVYRAExternalMediaManifest,
)


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA complete cinematic "
            "30-film production system"
        )
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
        "--no-resume",
        action="store_true",
    )

    parser.add_argument(
        "--status",
        action="store_true",
    )

    parser.add_argument(
        "--verify",
        action="store_true",
    )

    parser.add_argument(
        "--media-base-url",
        default=os.getenv(
            "AJVYRA_MEDIA_BASE_URL"
        ),
    )

    return parser.parse_args()


def main() -> int:

    args = parse_args()

    production_root = Path(
        "production/ajvyra_cinematic"
    )

    public_root = Path(
        "public"
    )

    controller = (
        AJVYRA30FilmReleaseController(
            production_root=production_root,
            public_root=public_root,
            external_media_base_url=(
                args.media_base_url
            ),
        )
    )

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    if args.status:

        status = controller.status()

        print(
            json.dumps(
                status,
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0

    # ---------------------------------------------------------
    # VERIFY
    # ---------------------------------------------------------

    if args.verify:

        try:

            gate = (
                AJVYRAFinalCinematicReleaseGate(
                    production_root=production_root,
                    public_root=public_root,
                )
            )

            result = gate.verify()

            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2,
                )
            )

            return 0

        except RuntimeError as exc:

            print(
                str(exc)
            )

            return 1

    # ---------------------------------------------------------
    # PRODUCTION
    # ---------------------------------------------------------

    results = controller.run(
        start=args.start,
        end=args.end,
        resume=not args.no_resume,
    )

    print(
        "\n=============================="
    )

    print(
        "AJVYRA PRODUCTION SUMMARY"
    )

    print(
        "=============================="
    )

    for result in results:

        print(
            f"{result.film_id:<12} "
            f"{result.title:<15} "
            f"{result.status:<30}"
        )

    ready = [
        result
        for result in results
        if result.site_ready
    ]

    print(
        f"\nREADY: {len(ready)}/{len(results)}"
    )

    # ---------------------------------------------------------
    # If only part of 30 was generated,
    # do not release.
    # ---------------------------------------------------------

    if len(results) < 30:

        print(
            "\nProduction batch finished."
        )

        print(
            "Release remains BLOCKED until "
            "all 30 films pass."
        )

        return 0

    # ---------------------------------------------------------
    # FINAL GATE
    # ---------------------------------------------------------

    try:

        gate = (
            AJVYRAFinalCinematicReleaseGate(
                production_root=production_root,
                public_root=public_root,
            )
        )

        release = gate.verify()

    except RuntimeError as exc:

        print(
            f"\n{exc}"
        )

        return 1

    # ---------------------------------------------------------
    # BUILD SITE MANIFEST
    # ---------------------------------------------------------

    manifest_builder = (
        AJVYRAExternalMediaManifest(
            public_root=public_root,
            media_base_url=(
                args.media_base_url
            ),
        )
    )

    catalog = (
        manifest_builder.build(
            release["movies"]
        )
    )

    print(
        "\n=============================="
    )

    print(
        "AJVYRA CINEMATIC RELEASE READY"
    )

    print(
        "=============================="
    )

    print(
        f"Movies: "
        f"{catalog['watchable_count']}/30"
    )

    print(
        "Site manifest:"
        " public/cinematic_player_manifest.json"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
