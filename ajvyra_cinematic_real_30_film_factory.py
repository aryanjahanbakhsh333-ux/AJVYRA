from __future__ import annotations

from pathlib import Path
from typing import Any
import importlib
import json
import time


DEFAULT_FILMS = [
    "Veylora",
    "Aelvryn",
    "Nyxara",
    "Kaelith",
    "Orivane",
    "Zeravia",
    "Vaelune",
    "Ravelyth",
    "Solvarya",
    "Xaveren",
    "Elyvara",
    "Neravelle",
    "Vaerith",
    "Lunavyr",
    "Averlyn",
    "Neyvara",
    "Elvaria",
    "Virelya",
    "Caelora",
    "Seravyn",
    "Mouravia",
    "Noxelya",
    "Vaelora",
    "Eryndra",
    "Neylith",
    "Auralyne",
    "Velmora",
    "Seyravia",
    "Oryvane",
    "Luminarae",
]


class AJVYRACinematicReal30FilmFactory:

    def __init__(
        self,
        film_factory: Any,
        root: str | Path = "public/cinematic_anime",
    ):
        self.film_factory = film_factory
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.state_path = (
            self.root / "30_film_factory_state.json"
        )

        self.state = self._load_state()

    def run(
        self,
        start: int = 1,
        end: int = 30,
        resume: bool = True,
    ) -> dict[str, Any]:

        start = max(1, start)
        end = min(30, end)

        results = []

        for number in range(start, end + 1):

            film_id = f"anime_{number:02d}"

            title = DEFAULT_FILMS[number - 1]

            existing = self.state.get(
                film_id,
                {},
            )

            movie = (
                self.root
                / film_id
                / "movie.mp4"
            )

            if (
                resume
                and existing.get("status") == "READY"
                and movie.exists()
                and movie.stat().st_size > 10_000
            ):
                results.append({
                    "film_id": film_id,
                    "title": title,
                    "status": "READY",
                    "skipped": True,
                })
                continue

            story = self._build_story(
                number,
                title,
            )

            characters = self._build_characters(
                number,
                title,
            )

            world = self._build_world(
                number,
                title,
            )

            result = self.film_factory.produce(
                film_id=film_id,
                title=title,
                genre=self._genre(number),
                story=story,
                characters=characters,
                world=world,
            )

            record = {
                "film_id": film_id,
                "title": title,
                "status": result.status,
                "segment_count": result.segment_count,
                "completed_segments": result.completed_segments,
                "movie": result.final_movie,
                "error": result.error,
            }

            self.state[film_id] = record
            self._save_state()

            results.append(record)

        return {
            "requested": end - start + 1,
            "results": results,
            "ready": sum(
                1
                for item in results
                if item["status"] == "READY"
            ),
            "failed": sum(
                1
                for item in results
                if item["status"] == "FAILED"
            ),
        }

    def status(self) -> dict[str, Any]:
        ready = 0
        failed = 0
        running = 0

        for number in range(1, 31):
            film_id = f"anime_{number:02d}"
            record = self.state.get(
                film_id,
                {},
            )

            status = record.get(
                "status",
                "PENDING",
            )

            if status == "READY":
                ready += 1
            elif status == "FAILED":
                failed += 1
            elif status == "RUNNING":
                running += 1

        return {
            "total": 30,
            "ready": ready,
            "failed": failed,
            "running": running,
            "pending": 30 - ready - failed - running,
        }

    def _build_story(
        self,
        number: int,
        title: str,
    ) -> str:

        themes = [
            "identity, memory and forbidden truth",
            "friendship, sacrifice and loneliness",
            "love, loss and impossible choices",
            "dark fantasy and the price of power",
            "hope surviving inside a collapsing world",
            "revenge transforming into forgiveness",
        ]

        theme = themes[
            (number - 1) % len(themes)
        ]

        return (
            f"{title} is an original cinematic anime story "
            f"centered around {theme}. "
            f"The protagonist discovers a hidden truth that "
            f"changes the meaning of their past. "
            f"The story gradually escalates toward a major "
            f"emotional and cinematic climax before reaching "
            f"a meaningful ending."
        )

    @staticmethod
    def _build_characters(
        number: int,
        title: str,
    ) -> list[dict[str, Any]]:

        return [
            {
                "name": f"{title} Protagonist",
                "appearance": (
                    "adult fictional anime protagonist, "
                    "distinct facial structure, "
                    "dark expressive eyes"
                ),
                "clothing": (
                    "consistent cinematic outfit "
                    "throughout the film"
                ),
            },
            {
                "name": f"{title} Companion",
                "appearance": (
                    "adult fictional anime character, "
                    "distinct silhouette and facial design"
                ),
                "clothing": (
                    "consistent secondary character outfit"
                ),
            },
        ]

    @staticmethod
    def _build_world(
        number: int,
        title: str,
    ) -> dict[str, Any]:

        return {
            "setting": "original fictional anime world",
            "visual_style": "dark cinematic anime",
            "weather": "variable according to story",
            "time_progression": "continuous",
            "continuity": (
                "preserve locations, clothing, "
                "character appearance and lighting logic"
            ),
        }

    @staticmethod
    def _genre(number: int) -> str:
        genres = [
            "Dark Fantasy",
            "Action Drama",
            "Psychological Mystery",
            "Romance Drama",
            "Supernatural Horror",
            "Adventure",
        ]

        return genres[
            (number - 1) % len(genres)
        ]

    def _load_state(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return {}

        try:
            return json.loads(
                self.state_path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return {}

    def _save_state(self) -> None:
        self.state_path.write_text(
            json.dumps(
                self.state,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
