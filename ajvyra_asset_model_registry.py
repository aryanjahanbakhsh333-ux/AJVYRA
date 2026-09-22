from dataclasses import dataclass, asdict
from pathlib import Path
import json
import hashlib


@dataclass
class AssetSpec:
    asset_id: str
    asset_type: str
    name: str
    role: str
    width: int = 256
    height: int = 256
    format: str = "svg"
    material: str = "standard"
    animation: str = "idle"
    tags: tuple = ()


class AJVYRAAssetModelRegistry:
    """
    Central registry for game assets.

    Every game gets its own asset manifest.
    """

    def __init__(self, root="generated/ajvyra_assets"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def stable_id(self, game_id, name):
        raw = f"ajvyra:{game_id}:{name}".encode()
        return hashlib.sha256(raw).hexdigest()[:16]

    def create_game_registry(self, game_id, genre, title):
        game_dir = self.root / f"game_{game_id:02d}"
        game_dir.mkdir(parents=True, exist_ok=True)

        assets = []

        definitions = [
            ("character", f"hero_{game_id}", "player"),
            ("enemy", f"enemy_{game_id}", "enemy"),
            ("environment", f"world_{game_id}", "background"),
            ("object", f"object_{game_id}", "interactive"),
            ("effect", f"effect_{game_id}", "vfx"),
            ("ui", f"ui_{game_id}", "interface"),
        ]

        for asset_type, name, role in definitions:
            assets.append(
                AssetSpec(
                    asset_id=self.stable_id(game_id, name),
                    asset_type=asset_type,
                    name=name,
                    role=role,
                    tags=(genre, title, role),
                )
            )

        registry = {
            "engine": "AJVYRA_ASSET_MODEL_ENGINE",
            "version": 1,
            "game_id": game_id,
            "genre": genre,
            "title": title,
            "assets": [asdict(asset) for asset in assets],
            "model_system": {
                "coordinate_system": "2D_SCREEN",
                "future_3d": True,
                "renderer": "canvas-webgl-compatible",
                "animation_system": "state-based",
            },
            "materials": [
                "standard",
                "metal",
                "glass",
                "stone",
                "wood",
                "organic",
                "dark",
            ],
            "animations": [
                "idle",
                "walk",
                "run",
                "attack",
                "hit",
                "death",
                "interact",
            ],
        }

        path = game_dir / "asset_registry.json"

        path.write_text(
            json.dumps(
                registry,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return registry

    def read(self, game_id):
        path = (
            self.root /
            f"game_{game_id:02d}" /
            "asset_registry.json"
        )

        if not path.exists():
            return None

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
