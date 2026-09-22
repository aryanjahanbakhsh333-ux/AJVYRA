from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, asdict, field
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


@dataclass
class ProductionAsset:
    kind: str
    path: str
    language: str | None = None
    required: bool = True
    exists: bool = False


@dataclass
class ProductionManifest:
    anime_id: int
    title: str
    status: str = "created"
    duration_seconds: int = 1800
    fps: int = 24

    story_ready: bool = False
    characters_ready: bool = False
    locations_ready: bool = False
    scenes_ready: bool = False
    dialogue_ready: bool = False
    voices_ready: bool = False
    visuals_ready: bool = False
    animation_ready: bool = False
    video_ready: bool = False
    subtitles_ready: bool = False
    published: bool = False

    assets: list[ProductionAsset] = field(
        default_factory=list
    )

    created_at: str = ""
    updated_at: str = ""
    production_hash: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()

        if not self.created_at:
            self.created_at = now

        self.updated_at = now

    def touch(self):
        self.updated_at = datetime.now(
            timezone.utc
        ).isoformat()

    def add_asset(
        self,
        kind: str,
        path: str,
        language: str | None = None,
        required: bool = True,
    ):
        self.assets.append(
            ProductionAsset(
                kind=kind,
                path=path,
                language=language,
                required=required,
                exists=Path(path).exists(),
            )
        )

        self.touch()

    def refresh_assets(self):
        for asset in self.assets:
            asset.exists = Path(asset.path).exists()

        self.touch()

    def calculate_hash(self) -> str:
        payload = {
            "anime_id": self.anime_id,
            "title": self.title,
            "duration": self.duration_seconds,
            "fps": self.fps,
            "assets": [
                asdict(asset)
                for asset in self.assets
            ],
        }

        raw = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
        ).encode("utf-8")

        self.production_hash = hashlib.sha256(
            raw
        ).hexdigest()

        return self.production_hash

    def ready_for_publish(self) -> bool:
        self.refresh_assets()

        required_assets_missing = any(
            asset.required and not asset.exists
            for asset in self.assets
        )

        return (
            self.story_ready
            and self.characters_ready
            and self.locations_ready
            and self.scenes_ready
            and self.dialogue_ready
            and self.voices_ready
            and self.visuals_ready
            and self.animation_ready
            and self.video_ready
            and self.subtitles_ready
            and not required_assets_missing
        )

    def to_dict(self) -> dict[str, Any]:
        self.calculate_hash()

        return asdict(self)

    def save(self, path: str | Path):
        path = Path(path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.calculate_hash()

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.to_dict(),
                file,
                ensure_ascii=False,
                indent=2,
            )

    @classmethod
    def load(
        cls,
        path: str | Path,
    ) -> "ProductionManifest":
        path = Path(path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        assets = [
            ProductionAsset(**item)
            for item in data.pop(
                "assets",
                [],
            )
        ]

        manifest = cls(
            **data,
            assets=assets,
        )

        manifest.refresh_assets()

        return manifest


class ManifestRegistry:
    def __init__(
        self,
        root: str | Path = "ajvyra_projects/manifests",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def path_for(
        self,
        anime_id: int,
    ) -> Path:
        return (
            self.root
            / f"anime_{anime_id:02d}.json"
        )

    def create(
        self,
        anime_id: int,
        title: str,
        duration_seconds: int = 1800,
        fps: int = 24,
    ) -> ProductionManifest:
        manifest = ProductionManifest(
            anime_id=anime_id,
            title=title,
            duration_seconds=duration_seconds,
            fps=fps,
        )

        manifest.save(
            self.path_for(anime_id)
        )

        return manifest

    def load(
        self,
        anime_id: int,
    ) -> ProductionManifest:
        return ProductionManifest.load(
            self.path_for(anime_id)
        )

    def update(
        self,
        manifest: ProductionManifest,
    ):
        manifest.save(
            self.path_for(
                manifest.anime_id
            )
        )

    def list_all(self) -> list[ProductionManifest]:
        results = []

        for path in sorted(
            self.root.glob("anime_*.json")
        ):
            try:
                results.append(
                    ProductionManifest.load(path)
                )
            except Exception:
                continue

        return results
