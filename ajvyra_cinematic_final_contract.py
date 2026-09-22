from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional
import json


class ProductionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class MediaType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"
    IMAGE = "image"


@dataclass
class CharacterState:
    character_id: str
    name: str
    age_group: str
    appearance: dict[str, Any] = field(default_factory=dict)
    clothing: dict[str, Any] = field(default_factory=dict)
    personality: dict[str, Any] = field(default_factory=dict)
    emotional_state: dict[str, Any] = field(default_factory=dict)
    reference_images: list[str] = field(default_factory=list)


@dataclass
class WorldState:
    location_id: str
    name: str
    time_of_day: str
    weather: str
    lighting: str
    environment: dict[str, Any] = field(default_factory=dict)


@dataclass
class CinematicMoment:
    moment_id: str
    order: int
    duration_target: float
    description: str

    characters: list[str] = field(default_factory=list)

    emotion: dict[str, Any] = field(default_factory=dict)
    camera: dict[str, Any] = field(default_factory=dict)
    lighting: dict[str, Any] = field(default_factory=dict)
    sound: dict[str, Any] = field(default_factory=dict)

    first_frame: Optional[str] = None
    last_frame: Optional[str] = None

    generated_media: list[str] = field(default_factory=list)


@dataclass
class CinematicFilmContract:
    film_id: str
    title: str
    genre: str
    target_duration_seconds: int

    language: str = "fa"

    characters: dict[str, CharacterState] = field(
        default_factory=dict
    )

    worlds: dict[str, WorldState] = field(
        default_factory=dict
    )

    moments: list[CinematicMoment] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    status: ProductionStatus = ProductionStatus.PENDING

    def add_character(
        self,
        character: CharacterState,
    ) -> None:
        self.characters[character.character_id] = character

    def add_world(
        self,
        world: WorldState,
    ) -> None:
        self.worlds[world.location_id] = world

    def add_moment(
        self,
        moment: CinematicMoment,
    ) -> None:
        self.moments.append(moment)
        self.moments.sort(
            key=lambda item: item.order
        )

    def total_target_duration(self) -> float:
        return sum(
            max(0.0, moment.duration_target)
            for moment in self.moments
        )

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.film_id.strip():
            errors.append("film_id is empty")

        if not self.title.strip():
            errors.append("title is empty")

        if self.target_duration_seconds <= 0:
            errors.append(
                "target_duration_seconds must be positive"
            )

        if not self.moments:
            errors.append("film has no cinematic moments")

        seen: set[str] = set()

        for moment in self.moments:
            if moment.moment_id in seen:
                errors.append(
                    f"duplicate moment_id: {moment.moment_id}"
                )

            seen.add(moment.moment_id)

            if moment.duration_target <= 0:
                errors.append(
                    f"invalid duration for {moment.moment_id}"
                )

            for character_id in moment.characters:
                if character_id not in self.characters:
                    errors.append(
                        f"{moment.moment_id}: "
                        f"unknown character {character_id}"
                    )

        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def save(
        self,
        path: str,
    ) -> None:
        with open(
            path,
            "w",
            encoding="utf-8",
        ) as handle:
            json.dump(
                self.to_dict(),
                handle,
                ensure_ascii=False,
                indent=2,
            )
