import json
from pathlib import Path
from typing import Dict, List

from ajvyra_ai_game_variation_engine import (
    AJVYRAIGameVariationEngine,
)

from ajvyra_game_template_factory import (
    AJVYGameTemplateFactory,
)


class AJVYRA70GameProductionController:
    """
    Production controller for the 70 playable AJVYRA games.

    It creates independent browser-playable game folders.
    """

    def __init__(
        self,
        output_root: str = "generated/games_70",
    ):
        self.output_root = Path(output_root)

        self.variation_engine = (
            AJVYRAIGameVariationEngine()
        )

        self.template_factory = (
            AJVYGameTemplateFactory()
        )

    def build_game(self, game_id: int) -> Dict:
        if not 1 <= game_id <= 70:
            raise ValueError(
                "game_id must be between 1 and 70."
            )

        variation = (
            self.variation_engine.create_variation(
                game_id
            )
        )

        profile = (
            self.variation_engine.build_runtime_profile(
                variation
            )
        )

        game_dir = (
            self.output_root /
            f"game_{game_id:02d}"
        )

        self.template_factory.build(
            output_dir=game_dir,
            game_id=variation.game_id,
            title=variation.title,
            genre=variation.genre,
            profile=profile,
            objective=variation.objective,
            seed=variation.seed,
        )

        report = {
            "game_id": variation.game_id,
            "title": variation.title,
            "genre": variation.genre,
            "objective": variation.objective,
            "mechanics": variation.mechanics,
            "difficulty_factor": (
                variation.difficulty_factor
            ),
            "seed": variation.seed,
            "playable": True,
            "files": [
                "index.html",
                "game.js",
                "game.css",
                "metadata.json",
            ],
        }

        (game_dir / "production_report.json").write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return report

    def build_all(self) -> List[Dict]:
        reports = []

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        for game_id in range(1, 71):
            report = self.build_game(game_id)
            reports.append(report)

            print(
                f"[AJVYRA] "
                f"{game_id:02d}/70 "
                f"{report['genre']} - "
                f"{report['title']}"
            )

        self._write_catalog(reports)

        return reports

    def _write_catalog(
        self,
        reports: List[Dict],
    ) -> None:

        catalog_path = (
            self.output_root /
            "games_catalog.json"
        )

        catalog_path.write_text(
            json.dumps(
                {
                    "total_games": len(reports),
                    "playable_games": sum(
                        1 for r in reports
                        if r["playable"]
                    ),
                    "games": reports,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def validate(self) -> Dict:
        results = []

        for game_id in range(1, 71):
            game_dir = (
                self.output_root /
                f"game_{game_id:02d}"
            )

            required = [
                game_dir / "index.html",
                game_dir / "game.js",
                game_dir / "game.css",
                game_dir / "metadata.json",
            ]

            exists = all(
                path.exists()
                for path in required
            )

            results.append({
                "game_id": game_id,
                "exists": exists,
            })

        return {
            "total": 70,
            "ready": sum(
                1 for item in results
                if item["exists"]
            ),
            "missing": [
                item["game_id"]
                for item in results
                if not item["exists"]
            ],
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AJVYRA 70 Game Production Controller"
    )

    parser.add_argument(
        "--game",
        type=int,
        help="Build one game.",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all 70 games.",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate generated games.",
    )

    args = parser.parse_args()

    controller = (
        AJVYRA70GameProductionController()
    )

    if args.game:
        report = controller.build_game(args.game)
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
        )

    elif args.all:
        controller.build_all()

    elif args.validate:
        print(
            json.dumps(
                controller.validate(),
                ensure_ascii=False,
                indent=2,
            )
        )

    else:
        parser.print_help()
