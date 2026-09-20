from pathlib import Path
import json
import time


class AnimeHistory:
    def __init__(self, file_path="anime_history.json"):
        self.file_path = Path(file_path)
        self.history = self._load()

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
                self.history,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def record(
        self,
        anime_id: int,
        position: float,
        duration: float
    ):
        entry = {
            "anime_id": anime_id,
            "position": round(position, 2),
            "duration": round(duration, 2),
            "progress": (
                round(position / duration * 100, 2)
                if duration > 0 else 0
            ),
            "updated_at": int(time.time())
        }

        self.history = [
            item
            for item in self.history
            if item["anime_id"] != anime_id
        ]

        self.history.insert(0, entry)
        self.history = self.history[:100]

        self._save()

    def get(self, anime_id: int):
        for item in self.history:
            if item["anime_id"] == anime_id:
                return item

        return None

    def recent(self, limit=10):
        return self.history[:limit]

    def clear(self):
        self.history = []
        self._save()
