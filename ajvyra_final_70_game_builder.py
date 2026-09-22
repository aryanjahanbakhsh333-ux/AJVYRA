import json
from pathlib import Path

from ajvyra_ai_game_variation_engine import (
    AJVYRAIGameVariationEngine,
)

from ajvyra_final_game_compiler import (
    AJVYRAFinalGameCompiler,
)

from ajvyra_final_game_validator import (
    AJVYRAFinalGameValidator,
)


class AJVYRAFinal70GameBuilder:
    """
    Final production builder.

    Builds all 70 games into:
        generated/final_games/
    """

    def __init__(
        self,
        output_root="generated/final_games",
    ):
        self.output_root = Path(output_root)

        self.variation =
            AJVYRAIGameVariationEngine()

        self.compiler =
            AJVYRAFinalGameCompiler()

        self.validator =
            AJVYRAFinalGameValidator()

    def build_one(self, game_id: int):
        variation = (
            self.variation.create_variation(
                game_id
            )
        )

        directory = (
            self.output_root /
            f"game_{game_id:02d}"
        )

        profile = (
            self.variation.build_runtime_profile(
                variation
            )
        )

        self.compiler.compile(
            output_dir=str(directory),
            game_id=variation.game_id,
            title=variation.title,
            genre=variation.genre,
            seed=variation.seed,
            difficulty=variation.difficulty_factor,
        )

        report = {
            "game_id": game_id,
            "title": variation.title,
            "genre": variation.genre,
            "objective": variation.objective,
            "mechanics": variation.mechanics,
            "difficulty": variation.difficulty_factor,
            "seed": variation.seed,
            "runtime_profile": profile,
        }

        (directory / "production.json").write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        validation = (
            self.validator.validate_game(
                str(directory)
            )
        )

        if not validation["valid"]:
            raise RuntimeError(
                f"Game {game_id} failed validation: "
                f"{validation['errors']}"
            )

        print(
            f"[AJVYRA FINAL] "
            f"{game_id:02d}/70 | "
            f"{variation.genre.upper()} | "
            f"{variation.title}"
        )

        return report

    def build_all(self):
        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        reports = []

        for game_id in range(1, 71):
            reports.append(
                self.build_one(game_id)
            )

        catalog = {
            "project": "AJVYRA",
            "system": "FINAL_GAMES",
            "total_games": len(reports),
            "playable_games": len(reports),
            "games": reports,
        }

        (self.output_root / "catalog.json").write_text(
            json.dumps(
                catalog,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        final_validation = (
            self.validator.validate_all(
                str(self.output_root),
                70,
            )
        )

        (self.output_root / "final_validation.json").write_text(
            json.dumps(
                final_validation,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return final_validation


if __name__ == "__main__":
    builder = AJVYRAFinal70GameBuilder()

    result = builder.build_all()

    print(
        "\nFINAL RESULT"
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )
