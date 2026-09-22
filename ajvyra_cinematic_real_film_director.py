from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ajvyra_cinematic_30_film_story_bible import (
    AJVYRACinematic30FilmStoryBible,
    FilmStory,
)


@dataclass(frozen=True)
class CinematicDirectorMoment:
    film_id: str
    sequence: int
    chapter: int
    emotion: str
    camera: str
    lighting: str
    action: str
    continuity: str
    prompt: str


class AJVYRACinematicRealFilmDirector:
    """
    Converts a film's narrative identity into actual generation moments.

    These prompts are intended for the real video provider.
    """

    EMOTIONS = (
        "quiet anticipation",
        "uncertainty",
        "fear",
        "tension",
        "hope",
        "grief",
        "determination",
        "intimacy",
        "despair",
        "release",
    )

    CAMERAS = (
        "wide establishing shot",
        "slow cinematic tracking shot",
        "medium character shot",
        "intimate close-up",
        "over-the-shoulder shot",
        "low-angle dramatic shot",
        "high-angle environmental shot",
        "slow push-in",
    )

    LIGHTING = (
        "cold moonlight",
        "soft overcast light",
        "rain reflections",
        "warm practical lights",
        "deep blue night lighting",
        "dramatic backlight",
        "dim candlelight",
        "pale dawn light",
    )

    def __init__(self, story: FilmStory) -> None:
        self.story = story

    @classmethod
    def for_film(
        cls,
        film_id: str,
    ) -> "AJVYRACinematicRealFilmDirector":
        return cls(
            AJVYRACinematic30FilmStoryBible.get(
                film_id
            )
        )

    def create_moment(
        self,
        sequence: int,
        chapter: int,
        emotion: str | None = None,
    ) -> CinematicDirectorMoment:
        emotion = (
            emotion
            or self.EMOTIONS[
                (sequence - 1) % len(self.EMOTIONS)
            ]
        )

        camera = self.CAMERAS[
            (sequence - 1) % len(self.CAMERAS)
        ]

        lighting = self.LIGHTING[
            (sequence - 1) % len(self.LIGHTING)
        ]

        action = self._action(sequence)

        continuity = (
            f"Maintain the established visual identity of "
            f"{self.story.title}. "
            f"Keep protagonist {self.story.protagonist} "
            f"visually consistent across shots. "
            f"Preserve clothing, hairstyle, facial structure, "
            f"age, proportions and environment continuity."
        )

        prompt = self._build_prompt(
            sequence=sequence,
            chapter=chapter,
            emotion=emotion,
            camera=camera,
            lighting=lighting,
            action=action,
            continuity=continuity,
        )

        return CinematicDirectorMoment(
            film_id=self.story.film_id,
            sequence=sequence,
            chapter=chapter,
            emotion=emotion,
            camera=camera,
            lighting=lighting,
            action=action,
            continuity=continuity,
            prompt=prompt,
        )

    def build_segment_plan(
        self,
        segment_count: int = 225,
    ) -> list[CinematicDirectorMoment]:
        if segment_count < 1:
            raise ValueError(
                "segment_count must be positive."
            )

        moments: list[CinematicDirectorMoment] = []

        for index in range(segment_count):
            sequence = index + 1

            chapter = min(
                5,
                ((index * 5) // segment_count) + 1,
            )

            moments.append(
                self.create_moment(
                    sequence=sequence,
                    chapter=chapter,
                )
            )

        return moments

    def _action(self, sequence: int) -> str:
        actions = (
            "walking through the environment",
            "observing something unexpected",
            "slowly approaching another character",
            "reacting to a distant sound",
            "running through the environment",
            "stopping and looking back",
            "facing an emotional realization",
            "moving through dangerous surroundings",
            "confronting the central conflict",
            "remaining still as the environment changes",
        )

        return actions[
            (sequence - 1) % len(actions)
        ]

    def _build_prompt(
        self,
        sequence: int,
        chapter: int,
        emotion: str,
        camera: str,
        lighting: str,
        action: str,
        continuity: str,
    ) -> str:
        return (
            f"Cinematic original anime film scene. "
            f"Film: {self.story.title}. "
            f"Genre: {self.story.genre}. "
            f"Chapter {chapter}, sequence {sequence}. "
            f"World: {self.story.world}. "
            f"Story premise: {self.story.logline}. "
            f"Emotional core: {self.story.emotional_core}. "
            f"Visual style: {self.story.visual_style}. "
            f"Current emotion: {emotion}. "
            f"Action: {action}. "
            f"Camera: {camera}. "
            f"Lighting: {lighting}. "
            f"Create coherent cinematic movement, "
            f"natural body motion, expressive eyes, "
            f"subtle facial acting and believable environmental motion. "
            f"No logos, no text overlays, no watermark, "
            f"no recognizable existing copyrighted characters. "
            f"{continuity}"
        )
