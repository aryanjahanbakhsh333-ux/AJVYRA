from pathlib import Path
import json

from ajvyra_asset_model_registry import (
    AJVYRAAssetModelRegistry,
)

from ajvyra_procedural_asset_factory import (
    AJVYRAProceduralAssetFactory,
)

from ajvyra_browser_asset_model_loader import (
    AJVYRAAssetBrowserLoader,
)


class AJVYRAAssetRuntimeConnector:

    def __init__(
        self,
        games_root="generated/final_games",
        assets_root="generated/ajvyra_assets",
    ):
        self.games_root = Path(games_root)
        self.assets_root = Path(assets_root)

        self.registry = (
            AJVYRAAssetModelRegistry(
                assets_root
            )
        )

        self.factory = (
            AJVYRAProceduralAssetFactory()
        )

        self.loader = (
            AJVYRAAssetBrowserLoader()
        )

    def connect_game(self, game_id):
        game_dir = (
            self.games_root /
            f"game_{game_id:02d}"
        )

        metadata_path = (
            game_dir /
            "metadata.json"
        )

        if not metadata_path.exists():
            raise FileNotFoundError(
                f"Missing metadata for game {game_id}"
            )

        metadata = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

        registry = (
            self.registry.create_game_registry(
                game_id=game_id,
                genre=metadata["genre"],
                title=metadata["title"],
            )
        )

        asset_manifest = (
            self.factory.generate_game_assets(
                game_id=game_id,
                genre=metadata["genre"],
                registry=registry,
                output_root=str(
                    self.assets_root
                ),
            )
        )

        self.loader.inject_into_game(
            game_directory=str(game_dir),
            game_id=game_id,
            asset_manifest=asset_manifest,
        )

        connection = {
            "game_id": game_id,
            "genre": metadata["genre"],
            "title": metadata["title"],
            "asset_registry": (
                f"../ajvyra_assets/"
                f"game_{game_id:02d}/"
                f"asset_registry.json"
            ),
            "asset_manifest": (
                f"../ajvyra_assets/"
                f"game_{game_id:02d}/"
                f"asset_manifest.json"
            ),
            "runtime_connected": True,
        }

        (game_dir / "asset_connection.json").write_text(
            json.dumps(
                connection,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return connection

    def connect_all(self):
        results = []

        for game_id in range(1, 71):
            try:
                result = self.connect_game(
                    game_id
                )

                result["success"] = True

            except Exception as exc:
                result = {
                    "game_id": game_id,
                    "success": False,
                    "error": str(exc),
                }

            results.append(result)

        return results
