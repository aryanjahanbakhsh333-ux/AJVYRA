from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from ajvyra_cinematic_final_contract import (
    CinematicFilmContract,
)

from ajvyra_cinematic_final_production_engine import (
    AJVYRACinematicFinalProductionEngine,
)

from ajvyra_cinematic_veo_real_runner import (
    AJVYRACinematicVeoRealRunner,
)


def load_contract(
    path: str | Path,
) -> CinematicFilmContract:

    data = json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )

    from ajvyra_cinematic_final_contract import (
        CharacterState,
        WorldState,
        CinematicMoment,
        ProductionStatus,
    )

    characters = {}

    for key, raw in data.get(
        "characters",
        {},
    ).items():

        characters[key] = CharacterState(
            **raw
        )

    worlds = {}

    for key, raw in data.get(
        "worlds",
        {},
    ).items():

        worlds[key] = WorldState(
            **raw
        )

    moments = []

    for raw in data.get(
        "moments",
        [],
    ):

        moments.append(
            CinematicMoment(
                **raw
            )
        )

    status = data.get(
        "status",
        ProductionStatus.PENDING.value,
    )

    return CinematicFilmContract(
        film_id=data["film_id"],
        title=data["title"],
        genre=data["genre"],
        target_duration_seconds=int(
            data["target_duration_seconds"]
        ),
        language=data.get(
            "language",
            "fa",
        ),
        characters=characters,
        worlds=worlds,
        moments=moments,
        metadata=data.get(
            "metadata",
            {},
        ),
        status=ProductionStatus(
            status
        ),
    )


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA real cinematic production boot"
        )
    )

    parser.add_argument(
        "--contract",
        required=True,
        help="Path to cinematic film contract JSON",
    )

    parser.add_argument(
        "--workspace",
        default="ajvyra_cinematic_workspace",
    )

    parser.add_argument(
        "--model",
        default=os.getenv(
            "AJVYRA_VEO_MODEL",
            "veo-3.1-generate-preview",
        ),
    )

    parser.add_argument(
        "--poll-seconds",
        type=int,
        default=10,
    )

    args = parser.parse_args()

    api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    if not api_key:
        print(
            "ERROR: GEMINI_API_KEY or "
            "GOOGLE_API_KEY is not configured."
        )
        return 2

    contract = load_contract(
        args.contract
    )

    errors = contract.validate()

    if errors:
        print(
            "CONTRACT INVALID:"
        )

        for error in errors:
            print(
                f" - {error}"
            )

        return 3

    runner = (
        AJVYRACinematicVeoRealRunner(
            api_key=api_key,
            poll_seconds=args.poll_seconds,
        )
    )

    # Keep the selected model configurable through the
    # runner/provider contract rather than hard-coding
    # model assumptions elsewhere.
    runner.default_model = args.model

    engine = (
        AJVYRACinematicFinalProductionEngine(
            workspace=args.workspace,
            media_provider=runner,
        )
    )

    print(
        f"Starting REAL production: "
        f"{contract.title}"
    )

    print(
        f"Film ID: {contract.film_id}"
    )

    print(
        f"Target duration: "
        f"{contract.target_duration_seconds}s"
    )

    result = engine.produce(
        contract
    )

    print(
        f"STATUS: {result.status}"
    )

    if result.movie_path:
        print(
            f"MOVIE: {result.movie_path}"
        )

    print(
        f"DURATION: "
        f"{result.duration_seconds:.2f}s"
    )

    print(
        f"SEGMENTS: "
        f"{result.generated_segments}"
    )

    if result.error:
        print(
            f"ERROR: {result.error}"
        )

    return (
        0
        if result.status == "COMPLETED"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
