import argparse
import json

from ajvyra_final_70_game_builder import (
    AJVYRAFinal70GameBuilder,
)

from ajvyra_final_game_validator import (
    AJVYRAFinalGameValidator,
)

from ajvyra_games_release_manager import (
    AJVYRAGamesReleaseManager,
)


def build():
    builder = AJVYRAFinal70GameBuilder()

    result = builder.build_all()

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


def validate():
    validator = AJVYRAFinalGameValidator()

    result = validator.validate_all(
        "generated/final_games",
        70,
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )


def release():
    manager = AJVYRAGamesReleaseManager()

    result = manager.prepare()

    print(
        json.dumps(
            {
                "release": "FINAL",
                "games": result["total_games"],
                "path": str(manager.release),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(
        description="AJVYRA FINAL Games System"
    )

    parser.add_argument(
        "command",
        choices=[
            "build",
            "validate",
            "release",
        ],
    )

    args = parser.parse_args()

    if args.command == "build":
        build()

    elif args.command == "validate":
        validate()

    elif args.command == "release":
        release()


if __name__ == "__main__":
    main()
