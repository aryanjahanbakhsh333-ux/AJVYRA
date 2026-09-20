from dataclasses import dataclass
from typing import List


@dataclass
class SearchAnime:
    number: int
    title: str
    genre: str
    mood: str
    logline: str


class AnimeSearchEngine:
    def __init__(self, catalog=None):
        self.catalog = catalog or []

    def search(self, query: str) -> List[object]:
        query = query.lower().strip()

        if not query:
            return list(self.catalog)

        results = []

        for anime in self.catalog:
            fields = [
                str(getattr(anime, "number", "")),
                getattr(anime, "title", ""),
                getattr(anime, "genre", ""),
                getattr(anime, "mood", ""),
                getattr(anime, "logline", ""),
            ]

            text = " ".join(fields).lower()

            if query in text:
                results.append(anime)

        return results

    def by_genre(self, genre: str) -> List[object]:
        return [
            anime for anime in self.catalog
            if getattr(anime, "genre", "").lower() == genre.lower()
        ]

    def by_mood(self, mood: str) -> List[object]:
        return [
            anime for anime in self.catalog
            if getattr(anime, "mood", "").lower() == mood.lower()
        ]
