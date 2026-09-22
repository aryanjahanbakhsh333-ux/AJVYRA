"""
AJVYRA CINEMATIC STORY INTELLIGENCE
-----------------------------------
Film-level story architecture.

No external LLM is required for the structural engine.
An external/local language model can later plug into the
StoryProvider interface without changing the film engine.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class StoryBeat:
    beat_id: str
    title: str
    start: float
    end: float
    purpose: str
    conflict: str
    emotional_target: str
    intensity: float


@dataclass
class StoryArc:
    premise: str
    protagonist_goal: str
    central_conflict: str
    internal_conflict: str
    stakes: str
    ending_type: str

    beats: List[StoryBeat] = field(
        default_factory=list
    )


@dataclass
class StoryRequest:
    title: str
    genre: str
    duration_seconds: int = 1800

    themes: List[str] = field(
        default_factory=list
    )

    tone: str = "cinematic"
    ending_type: str = "bittersweet"

    protagonist: str = ""
    antagonist: str = ""


class AJVYRACinematicStoryIntelligence:
    VERSION = "1.0.0"

    GENRE_RULES = {
        "fantasy": {
            "conflict": "A hidden power threatens the protagonist's world.",
            "tone": "mysterious",
        },
        "dark_fantasy": {
            "conflict": "A personal loss is connected to a dangerous supernatural truth.",
            "tone": "dark_mysterious",
        },
        "romance": {
            "conflict": "Two people must confront a truth that threatens their relationship.",
            "tone": "intimate",
        },
        "heartbreak": {
            "conflict": "The protagonist must accept a relationship that cannot become what they imagined.",
            "tone": "melancholic",
        },
        "horror": {
            "conflict": "The protagonist discovers that the threat is connected to something they trusted.",
            "tone": "dread",
        },
        "action": {
            "conflict": "A rapidly escalating external threat forces impossible choices.",
            "tone": "intense",
        },
        "sad": {
            "conflict": "A meaningful bond is tested by an irreversible event.",
            "tone": "melancholic",
        },
    }

    def __init__(
        self,
        seed: Optional[int] = None,
    ) -> None:
        self.random = random.Random(seed)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def create_story(
        self,
        request: StoryRequest,
    ) -> StoryArc:
        rules = self.GENRE_RULES.get(
            request.genre.lower(),
            {
                "conflict": (
                    "The protagonist must confront "
                    "a difficult truth."
                ),
                "tone": request.tone,
            },
        )

        protagonist = (
            request.protagonist.strip()
            or "the protagonist"
        )

        antagonist = (
            request.antagonist.strip()
            or "the opposing force"
        )

        central_conflict = rules[
            "conflict"
        ]

        if antagonist != "the opposing force":
            central_conflict = (
                f"{antagonist} becomes the force "
                f"behind the central conflict."
            )

        premise = self._build_premise(
            request,
            protagonist,
            central_conflict,
        )

        arc = StoryArc(
            premise=premise,
            protagonist_goal=(
                f"{protagonist} must discover "
                "what the truth demands."
            ),
            central_conflict=central_conflict,
            internal_conflict=(
                "The protagonist must choose between "
                "what they want and what they know is true."
            ),
            stakes=(
                "The protagonist risks losing both "
                "the external goal and an important bond."
            ),
            ending_type=request.ending_type,
        )

        arc.beats = self._build_beats(
            request.duration_seconds,
            request.ending_type,
        )

        return arc

    # ---------------------------------------------------------
    # Structure
    # ---------------------------------------------------------

    def _build_premise(
        self,
        request: StoryRequest,
        protagonist: str,
        conflict: str,
    ) -> str:
        themes = ", ".join(
            request.themes
        ) or "identity and loss"

        return (
            f"{protagonist} enters a world shaped by "
            f"{themes}, where {conflict.lower()}"
        )

    def _build_beats(
        self,
        duration: int,
        ending_type: str,
    ) -> List[StoryBeat]:
        total = float(duration)

        points = [
            (
                0.00,
                0.08,
                "Opening",
                "Establish the emotional world.",
                "curiosity",
                0.25,
            ),
            (
                0.08,
                0.20,
                "Inciting Incident",
                "Break the protagonist's normal world.",
                "uncertainty",
                0.40,
            ),
            (
                0.20,
                0.35,
                "First Commitment",
                "Force the protagonist to act.",
                "determination",
                0.55,
            ),
            (
                0.35,
                0.50,
                "Relationship Shift",
                "Change an important relationship.",
                "connection",
                0.62,
            ),
            (
                0.50,
                0.62,
                "Midpoint Truth",
                "Reveal information that changes the meaning of earlier events.",
                "shock",
                0.72,
            ),
            (
                0.62,
                0.76,
                "Collapse",
                "Take away the protagonist's apparent solution.",
                "despair",
                0.86,
            ),
            (
                0.76,
                0.90,
                "Final Choice",
                "Make the protagonist choose.",
                "courage",
                0.94,
            ),
            (
                0.90,
                1.00,
                "Resolution",
                "Show the emotional consequence.",
                ending_type,
                0.70,
            ),
        ]

        beats: List[StoryBeat] = []

        for index, (
            start_ratio,
            end_ratio,
            title,
            purpose,
            emotion,
            intensity,
        ) in enumerate(points, start=1):
            beats.append(
                StoryBeat(
                    beat_id=f"beat_{index:02d}",
                    title=title,
                    start=round(
                        total * start_ratio,
                        3,
                    ),
                    end=round(
                        total * end_ratio,
                        3,
                    ),
                    purpose=purpose,
                    conflict="",
                    emotional_target=emotion,
                    intensity=intensity,
                )
            )

        return beats

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(
        self,
        arc: StoryArc,
    ) -> List[str]:
        errors: List[str] = []

        if not arc.premise.strip():
            errors.append(
                "Story premise is empty."
            )

        if not arc.central_conflict.strip():
            errors.append(
                "Central conflict is empty."
            )

        if len(arc.beats) < 5:
            errors.append(
                "Story needs at least five structural beats."
            )

        previous_end = 0.0

        for beat in arc.beats:
            if beat.start < previous_end:
                errors.append(
                    f"Beat overlap: {beat.beat_id}"
                )

            if beat.end <= beat.start:
                errors.append(
                    f"Invalid timing: {beat.beat_id}"
                )

            previous_end = beat.end

        return errors

    def save(
        self,
        arc: StoryArc,
        path: str | Path,
    ) -> Path:
        target = Path(path)
        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                asdict(arc),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target


if __name__ == "__main__":
    intelligence = (
        AJVYRACinematicStoryIntelligence(
            seed=42
        )
    )

    request = StoryRequest(
        title="Veylora",
        genre="dark_fantasy",
        themes=[
            "memory",
            "loneliness",
            "love",
        ],
        tone="dark_cinematic",
        ending_type="bittersweet",
        protagonist="Veylora",
    )

    story = intelligence.create_story(
        request
    )

    errors = intelligence.validate(
        story
    )

    if errors:
        raise RuntimeError(
            "\n".join(errors)
        )

    intelligence.save(
        story,
        "generated/cinematic/veyllora/"
        "story_arc.json",
    )

    print(
        json.dumps(
            asdict(story),
            ensure_ascii=False,
            indent=2,
        )
    )
