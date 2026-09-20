from typing import List


class AnimeRecommendationEngine:
    def __init__(self, catalog=None):
        self.catalog = catalog or []

    def recommend(
        self,
        anime,
        limit: int = 5
    ) -> List[object]:

        candidates = []

        for item in self.catalog:
            if getattr(item, "number", None) == getattr(anime, "number", None):
                continue

            score = 0

            if getattr(item, "genre", None) == getattr(anime, "genre", None):
                score += 3

            if getattr(item, "mood", None) == getattr(anime, "mood", None):
                score += 2

            if score > 0:
                candidates.append(
                    (score, item)
                )

        candidates.sort(
            key=lambda pair: (
                -pair[0],
                getattr(pair[1], "number", 999)
            )
        )

        return [
            item
            for _, item in candidates[:limit]
        ]

    def recommend_by_genre(
        self,
        genre: str,
        limit: int = 5
    ):
        return [
            anime
            for anime in self.catalog
            if getattr(anime, "genre", "").lower()
            == genre.lower()
        ][:limit]
