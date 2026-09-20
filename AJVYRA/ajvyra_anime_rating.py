from pathlib import Path
import json


class AnimeRatingSystem:
    def __init__(self, file_path="anime_ratings.json"):
        self.file_path = Path(file_path)
        self.ratings = self._load()

    def _load(self):
        if not self.file_path.exists():
            return {}

        try:
            return json.loads(
                self.file_path.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError):
            return {}

    def _save(self):
        self.file_path.write_text(
            json.dumps(
                self.ratings,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def rate(self, anime_id: int, rating: int):
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")

        key = str(anime_id)

        if key not in self.ratings:
            self.ratings[key] = []

        self.ratings[key].append(rating)
        self._save()

    def average(self, anime_id: int):
        values = self.ratings.get(str(anime_id), [])

        if not values:
            return 0

        return round(sum(values) / len(values), 2)

    def count(self, anime_id: int):
        return len(
            self.ratings.get(str(anime_id), [])
        )

    def summary(self, anime_id: int):
        return {
            "anime_id": anime_id,
            "average": self.average(anime_id),
            "votes": self.count(anime_id),
        }
