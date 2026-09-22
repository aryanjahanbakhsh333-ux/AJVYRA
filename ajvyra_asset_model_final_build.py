import json
from pathlib import Path

from ajvyra_game_asset_runtime_connector import (
    AJVYRAAssetRuntimeConnector,
)


class AJVYRAAssetModelFinalBuild:

    def __init__(
        self,
        games_root="generated/final_games",
    ):
        self.games_root = Path(games_root)

        self.connector = (
            AJVYRAAssetRuntimeConnector(
                games_root=games_root,
                assets_root="generated/ajvyra_assets",
            )
        )

    def build(self):
        if not self.games_root.exists():
            raise FileNotFoundError(
                "generated/final_games does not exist. "
                "Build the 70 games first."
            )

        results = (
            self.connector.connect_all()
        )

        success = [
            item
            for item in results
            if item.get("success")
        ]

        failed = [
            item
            for item in results
            if not item.get("success")
        ]

        report = {
            "project": "AJVYRA",
            "system": "ASSET_MODEL_FINAL",
            "games_expected": 70,
            "games_connected": len(success),
            "games_failed": len(failed),
            "complete": len(success) == 70,
            "results": results,
        }

        report_path = (
            self.games_root /
            "asset_model_build_report.json"
        )

        report_path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print(
            f"AJVYRA Asset/Model connection: "
            f"{len(success)}/70"
        )

        if failed:
            print(
                "Failed games:",
                [
                    x["game_id"]
                    for x in failed
                ],
            )

        return report


if __name__ == "__main__":
    builder = (
        AJVYRAAssetModelFinalBuild()
    )

    result = builder.build()

    print(
        json.dumps(
            {
                "complete": result["complete"],
                "connected":
                    result["games_connected"],
                "failed":
                    result["games_failed"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
