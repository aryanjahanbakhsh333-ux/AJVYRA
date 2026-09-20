from pathlib import Path
import json


class AnimeProgress:
    def __init__(self, file_path="anime_progress.json"):
        self.file_path = Path(file_path)
        self.data = self._load()

    def _load(self):
        if not self.file_path.exists():
            return {}

        try:
            return json.loads(
                self.file_path.read_text(
                    encoding="utf-8"
                )
            )
        except (json.JSONDecodeError, OSError):
            return {}

    def _save(self):
        self.file_path.write_text(
            json.dumps(
                self.data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def update(
        self,
        anime_id: int,
        seconds: float,
        duration: float
    ):
        progress = 0

        if duration > 0:
            progress = min(
                100,
                max(
                    0,
                    (seconds / duration) * 100
                )
            )

        self.data[str(anime_id)] = {
            "seconds": round(seconds, 2),
            "duration": round(duration, 2),
            "percent": round(progress, 2),
            "completed": progress >= 95,
        }

        self._save()

    def get(self, anime_id: int):
        return self.data.get(
            str(anime_id),
            {
                "seconds": 0,
                "duration": 0,
                "percent": 0,
                "completed": False,
            }
        )

    def completed(self, anime_id: int):
        return self.get(anime_id)["completed"]
