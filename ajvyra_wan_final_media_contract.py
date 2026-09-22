from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Optional


@dataclass
class FinalMediaAsset:
    asset_id: str
    asset_type: str
    path: str
    duration_seconds: float = 0.0
    sha256: str = ""
    required: bool = True
    ready: bool = False


@dataclass
class FinalFilmState:
    film_id: str
    title: str

    expected_duration_seconds: int

    video_segments: list[FinalMediaAsset]
    dialogue_assets: list[FinalMediaAsset]
    music_assets: list[FinalMediaAsset]
    sfx_assets: list[FinalMediaAsset]
    subtitle_assets: list[FinalMediaAsset]

    assembled_video: Optional[str] = None
    final_movie: Optional[str] = None

    video_ready: bool = False
    dialogue_ready: bool = False
    music_ready: bool = False
    subtitles_ready: bool = False
    final_ready: bool = False

    error: Optional[str] = None

    def all_required_assets_ready(self) -> bool:
        groups = [
            self.video_segments,
            self.dialogue_assets,
            self.music_assets,
            self.subtitle_assets,
        ]

        for group in groups:
            for asset in group:
                if asset.required and not asset.ready:
                    return False

        return True

    def release_ready(self) -> bool:
        return (
            self.video_ready
            and self.dialogue_ready
            and self.music_ready
            and self.subtitles_ready
            and self.final_ready
            and bool(self.final_movie)
        )


class AJVYRAFinalMediaContract:

    @staticmethod
    def sha256(path: str | Path) -> str:
        path = Path(path)

        digest = hashlib.sha256()

        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def inspect_asset(
        asset: FinalMediaAsset,
    ) -> FinalMediaAsset:

        path = Path(asset.path)

        if not path.exists():
            asset.ready = False
            return asset

        if path.stat().st_size <= 0:
            asset.ready = False
            return asset

        asset.sha256 = AJVYRAFinalMediaContract.sha256(path)
        asset.ready = True

        return asset

    @staticmethod
    def save_state(
        state: FinalFilmState,
        path: str | Path,
    ) -> None:

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                asdict(state),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def load_state(
        path: str | Path,
    ) -> FinalFilmState:

        data = json.loads(
            Path(path).read_text(
                encoding="utf-8"
            )
        )

        return FinalFilmState(**data)
