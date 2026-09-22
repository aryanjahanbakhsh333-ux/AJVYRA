from __future__ import annotations

import argparse
import json


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA Cinematic Final Build"
        )
    )

    parser.add_argument(
        "--catalog-only",
        action="store_true",
    )

    parser.add_argument(
        "--verify",
        action="store_true",
    )

    args = parser.parse_args()

    from ajvyra_cinematic_30_site_catalog_builder import (
        AJVYRACinematic30SiteCatalogBuilder,
    )

    builder = (
        AJVYRACinematic30SiteCatalogBuilder()
    )

    catalog = builder.build()

    print(
        f"Real watchable films: "
        f"{catalog['total_ready']}/30"
    )

    if args.verify:

        from ajvyra_cinematic_production_build_gate import (
            AJVYRACinematicProductionBuildGate,
        )

        gate = (
            AJVYRACinematicProductionBuildGate()
        )

        result = gate.validate()

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return 0 if result["allowed"] else 2

    if args.catalog_only:
        return 0

    print()
    print(
        "AJVYRA cinematic site catalog rebuilt."
    )
    print(
        "Only real READY MP4 files are watchable."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
