from pathlib import Path
import json


class AnimeWatchlist:
    def __init__(self, file_path="anime_watchlist.json"):
        self.file_path = Path(file_path)
        self.items = self._load()

    def _load(self):
        if not self.file_path.exists():
            return []

        try:
            return json.loads(
                self.file_path.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            return []

    def _save(self):
        self.file_path.write_text(
            json.dumps(
                self.items,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def add(self, anime_id: int):
        if anime_id not in self.items:
            self.items.append(anime_id)
            self._save()

    def remove(self, anime_id: int):
        if anime_id in self.items:
            self.items.remove(anime_id)
            self._save()

    def toggle(self, anime_id: int):
        if anime_id in self.items:
            self.remove(anime_id)
            return False

        self.add(anime_id)
        return True

    def contains(self, anime_id: int) -> bool:
        return anime_id in self.items

    def all(self):
        return list(self.items)
