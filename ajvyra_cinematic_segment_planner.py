from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json
import math


@dataclass
class CinematicSegment:
    film_id: str
    segment_id: str
    index: int

    duration_seconds: int
    chapter: int
    scene: int

    description: str
    emotional_direction: str
    camera_direction: str
    lighting_direction: str

    prompt: str

    previous_segment: str | None = None
    next_segment: str | None = None


class AJVYRACinematicSegmentPlanner:
    """
    Converts a film-level concept into provider-compatible
    cinematic generation segments.

    The provider may generate short clips.
    AJVYRA owns the film-level structure.
    """

    def __init__(
        self,
        segment_seconds: int = 8,
        target_minutes: int = 30,
    ):
        self.segment_seconds = max(4, min(segment_seconds, 8))
        self.target_minutes = max(1, target_minutes)

    def plan_film(
        self,
        film_id: str,
        title: str,
        genre: str,
        story: str,
        characters: list[dict[str, Any]] | None = None,
        world: dict[str, Any] | None = None,
    ) -> list[CinematicSegment]:

        characters = characters or []
        world = world or {}

        target_seconds = self.target_minutes * 60
        segment_count = math.ceil(
            target_seconds / self.segment_seconds
        )

        segments: list[CinematicSegment] = []

        chapter_count = 6
        scenes_per_chapter = max(
            1,
            math.ceil(segment_count / chapter_count),
        )

        for index in range(segment_count):
            chapter = min(
                chapter_count,
                index // scenes_per_chapter + 1,
            )

            scene = (
                index // max(1, scenes_per_chapter // 5)
            ) + 1

            emotional_direction = self._emotion_for_position(
                index,
                segment_count,
            )

            camera_direction = self._camera_for_position(
                index,
                segment_count,
            )

            lighting_direction = self._lighting_for_position(
                index,
                segment_count,
            )

            character_text = self._characters_text(characters)
            world_text = self._world_text(world)

            description = (
                f"Cinematic moment {index + 1} of {title}. "
                f"Genre: {genre}. "
                f"Story context: {story}. "
                f"Emotional direction: {emotional_direction}."
            )

            prompt = f"""
Create one cinematic anime film segment.

FILM:
Title: {title}
Genre: {genre}

STORY CONTEXT:
{story}

CHARACTERS:
{character_text}

WORLD:
{world_text}

CURRENT MOMENT:
{description}

CAMERA:
{camera_direction}

LIGHTING:
{lighting_direction}

EMOTION:
{emotional_direction}

CONTINUITY:
Preserve the same character identities, clothing,
hair, facial structure, proportions, environment,
time of day, color language and cinematic style
established by the previous moments.

STYLE:
High-quality cinematic anime.
Professional composition.
Natural movement.
Expressive acting.
Film-like camera movement.
No subtitles.
No logos.
No text on screen.
No random character replacement.
No unexplained costume changes.

The segment must feel like one continuous part
of a larger feature-length animated film.
""".strip()

            segment = CinematicSegment(
                film_id=film_id,
                segment_id=f"seg_{index + 1:04d}",
                index=index,
                duration_seconds=self.segment_seconds,
                chapter=chapter,
                scene=scene,
                description=description,
                emotional_direction=emotional_direction,
                camera_direction=camera_direction,
                lighting_direction=lighting_direction,
                prompt=" ".join(prompt.split()),
            )

            segments.append(segment)

        for i, segment in enumerate(segments):
            if i > 0:
                segment.previous_segment = segments[i - 1].segment_id

            if i < len(segments) - 1:
                segment.next_segment = segments[i + 1].segment_id

        return segments

    def save(
        self,
        segments: list[CinematicSegment],
        path: str | Path,
    ) -> Path:

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = [
            asdict(segment)
            for segment in segments
        ]

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    @staticmethod
    def _characters_text(
        characters: list[dict[str, Any]],
    ) -> str:
        if not characters:
            return "Characters are defined by the film intelligence layer."

        lines = []

        for character in characters:
            name = character.get("name", "Character")
            appearance = character.get("appearance", "")
            clothing = character.get("clothing", "")

            lines.append(
                f"{name}: appearance={appearance}; clothing={clothing}"
            )

        return "\n".join(lines)

    @staticmethod
    def _world_text(
        world: dict[str, Any],
    ) -> str:
        if not world:
            return "World is defined by the cinematic film intelligence layer."

        return "; ".join(
            f"{key}={value}"
            for key, value in world.items()
        )

    @staticmethod
    def _emotion_for_position(
        index: int,
        total: int,
    ) -> str:
        ratio = index / max(1, total - 1)

        if ratio < 0.12:
            return "mystery, curiosity, quiet anticipation"
        if ratio < 0.30:
            return "wonder, discovery, emotional attachment"
        if ratio < 0.48:
            return "tension, uncertainty, internal conflict"
        if ratio < 0.68:
            return "pain, loss, fear, emotional pressure"
        if ratio < 0.84:
            return "desperation, confrontation, emotional climax"

        return "aftermath, reflection, resolution, lingering emotion"

    @staticmethod
    def _camera_for_position(
        index: int,
        total: int,
    ) -> str:
        ratio = index / max(1, total - 1)

        if ratio < 0.25:
            return "slow cinematic tracking shots and intimate close-ups"

        if ratio < 0.55:
            return "controlled handheld movement, medium shots and dramatic push-ins"

        if ratio < 0.80:
            return "dynamic cinematic movement, wide shots and dramatic close-ups"

        return "slow stable camera movement with emotionally restrained framing"

    @staticmethod
    def _lighting_for_position(
        index: int,
        total: int,
    ) -> str:
        ratio = index / max(1, total - 1)

        if ratio < 0.30:
            return "soft atmospheric cinematic lighting"

        if ratio < 0.65:
            return "stronger contrast with emotional shadows"

        if ratio < 0.85:
            return "dramatic high-contrast cinematic lighting"

        return "soft reflective light with subdued contrast"
