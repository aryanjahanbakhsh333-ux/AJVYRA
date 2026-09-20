from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class DownloadItem:
    anime_id: int
    kind: str
    language: str
    path: str
    available: bool


class AnimeDownloadManager:
    def __init__(self, root: str = "anime_assets"):
        self.root = Path(root)

    def get_items(self, anime_id: int) -> List[DownloadItem]:
        folder = self.root / f"anime_{anime_id:02d}"

        items = [
            DownloadItem(
                anime_id,
                "video",
                "original",
                str(folder / "video" / "main.mp4"),
                (folder / "video" / "main.mp4").exists(),
            ),
            DownloadItem(
                anime_id,
                "audio",
                "fa",
                str(folder / "voice" / "fa_full.mp3"),
                (folder / "voice" / "fa_full.mp3").exists(),
            ),
            DownloadItem(
                anime_id,
                "audio",
                "ja",
                str(folder / "voice" / "ja_full.mp3"),
                (folder / "voice" / "ja_full.mp3").exists(),
            ),
        ]

        return items

    def available_downloads(self, anime_id: int):
        return [
            item for item in self.get_items(anime_id)
            if item.available
        ]


if __name__ == "__main__":
    manager = AnimeDownloadManager()
    for item in manager.get_items(1):
        print(item)
