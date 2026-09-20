from pathlib import Path
from typing import Dict


class AnimeAssetManager:
    ASSET_TYPES = {
        "video": ("video", ".mp4"),
        "poster": ("poster", ".jpg"),
        "fa_voice": ("voice", "fa_full.mp3"),
        "ja_voice": ("voice", "ja_full.mp3"),
        "en_subtitle": ("subtitles", "en.srt"),
        "fa_subtitle": ("subtitles", "fa.srt"),
        "ja_subtitle": ("subtitles", "ja.srt"),
    }

    def __init__(self, root="anime_assets"):
        self.root = Path(root)

    def anime_folder(self, anime_id: int):
        return self.root / f"anime_{anime_id:02d}"

    def asset_path(self, anime_id: int, asset_type: str):
        if asset_type not in self.ASSET_TYPES:
            raise ValueError(
                f"Unknown asset type: {asset_type}"
            )

        folder, filename = self.ASSET_TYPES[asset_type]

        return (
            self.anime_folder(anime_id)
            / folder
            / filename
        )

    def exists(self, anime_id: int, asset_type: str):
        return self.asset_path(
            anime_id,
            asset_type
        ).exists()

    def report(self, anime_id: int) -> Dict[str, bool]:
        return {
            asset_type: self.exists(
                anime_id,
                asset_type
            )
            for asset_type in self.ASSET_TYPES
        }

    def missing(self, anime_id: int):
        report = self.report(anime_id)

        return [
            asset
            for asset, exists in report.items()
            if not exists
        ]
