from __future__ import annotations

import hashlib
import importlib
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class WanFilmStorySpec:
    film_id: str
    title: str
    logline: str
    protagonist: str
    antagonist: str
    world: str
    emotional_core: str
    visual_style: str
    ending_type: str

    def stable_seed(self, segment_index: int) -> int:
        raw = f"{self.film_id}|{segment_index}|AJVYRA|WAN"
        digest = hashlib.sha256(raw.encode("utf-8")).digest()
        return int.from_bytes(digest[:4], "big")

    def base_prompt(self) -> str:
        return (
            f"Cinematic anime film titled {self.title}. "
            f"Story: {self.logline}. "
            f"Main protagonist: {self.protagonist}. "
            f"Antagonistic force: {self.antagonist}. "
            f"World: {self.world}. "
            f"Emotional core: {self.emotional_core}. "
            f"Visual language: {self.visual_style}. "
            f"Ending direction: {self.ending_type}. "
            "High-end cinematic anime production, coherent character anatomy, "
            "consistent costume design, expressive acting, controlled camera motion, "
            "strong composition, atmospheric lighting, detailed environment."
        )


class AJVYRAWanCinematicStoryAdapter:
    """
    Loads the existing 30-film story bible without recreating it.

    Expected source module:
        ajvyra_cinematic_30_film_story_bible.py

    The adapter is intentionally defensive because the existing Story Bible
    may expose its collection under different names.
    """

    MODULE_NAME = "ajvyra_cinematic_30_film_story_bible"

    def __init__(self) -> None:
        self.module = importlib.import_module(self.MODULE_NAME)
        self.stories = self._discover_stories()

    def _discover_stories(self) -> Dict[str, WanFilmStorySpec]:
        candidates = []

        for name in dir(self.module):
            if name.startswith("_"):
                continue

            value = getattr(self.module, name)

            if isinstance(value, dict):
                candidates.append(value)

            elif isinstance(value, (list, tuple)):
                candidates.append(value)

        result: Dict[str, WanFilmStorySpec] = {}

        for collection in candidates:
            if isinstance(collection, dict):
                values = list(collection.values())
            else:
                values = list(collection)

            for item in values:
                spec = self._convert(item)

                if spec is not None:
                    result[spec.film_id] = spec

        return result

    @staticmethod
    def _get(item: Any, key: str, default: str = "") -> str:
        if isinstance(item, dict):
            value = item.get(key, default)
        else:
            value = getattr(item, key, default)

        if value is None:
            return default

        return str(value)

    def _convert(self, item: Any) -> WanFilmStorySpec | None:
        title = self._get(item, "title")

        if not title:
            return None

        film_id = self._get(item, "film_id")

        if not film_id:
            film_id = self._get(item, "id")

        if not film_id:
            film_id = (
                title.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )

        return WanFilmStorySpec(
            film_id=film_id,
            title=title,
            logline=self._get(item, "logline"),
            protagonist=self._get(item, "protagonist"),
            antagonist=self._get(item, "antagonist"),
            world=self._get(item, "world"),
            emotional_core=self._get(item, "emotional_core"),
            visual_style=self._get(item, "visual_style"),
            ending_type=self._get(item, "ending_type"),
        )

    def get(self, film_id: str) -> WanFilmStorySpec:
        if film_id not in self.stories:
            raise KeyError(
                f"No Story Bible entry found for film_id={film_id!r}"
            )

        return self.stories[film_id]

    def all(self) -> list[WanFilmStorySpec]:
        return list(self.stories.values())

    def build_segment_prompt(
        self,
        film_id: str,
        segment_index: int,
        action: str,
        camera: str,
        emotion: str,
        continuity: str,
    ) -> str:
        story = self.get(film_id)

        return (
            f"{story.base_prompt()} "
            f"Current segment: {segment_index}. "
            f"Action: {action}. "
            f"Camera: {camera}. "
            f"Emotional state: {emotion}. "
            f"Continuity requirements: {continuity}. "
            "The current shot must feel like a direct continuation of the "
            "previous shot, not a redesign of the characters or world."
        )
