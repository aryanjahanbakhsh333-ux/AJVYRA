from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class CharacterReference:
    character_id: str
    name: str
    description: str
    reference_image: Optional[str] = None


@dataclass
class ReferenceState:
    film_id: str
    segment_index: int
    character_references: list[CharacterReference]
    previous_segment: Optional[str] = None
    continuity_token: str = ""


class AJVYRAWanReferenceFramePipeline:
    """
    Persistent reference/continuity registry.

    This layer does not fabricate reference images.
    It stores and validates real references supplied by the production system.
    """

    def __init__(self, root: str | Path = "ajvyra_wan_references") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def film_directory(self, film_id: str) -> Path:
        path = self.root / film_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def register_character(
        self,
        film_id: str,
        character_id: str,
        name: str,
        description: str,
        reference_image: str | None = None,
    ) -> CharacterReference:

        if reference_image:
            image_path = Path(reference_image)

            if not image_path.exists():
                raise FileNotFoundError(
                    f"Character reference does not exist: {reference_image}"
                )

        ref = CharacterReference(
            character_id=character_id,
            name=name,
            description=description,
            reference_image=reference_image,
        )

        path = self.film_directory(film_id) / "characters.json"

        existing = []

        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))

        existing = [
            item for item in existing
            if item.get("character_id") != character_id
        ]

        existing.append(asdict(ref))

        path.write_text(
            json.dumps(existing, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return ref

    def load_characters(self, film_id: str) -> list[CharacterReference]:
        path = self.film_directory(film_id) / "characters.json"

        if not path.exists():
            return []

        data = json.loads(path.read_text(encoding="utf-8"))

        return [
            CharacterReference(**item)
            for item in data
        ]

    def build_continuity_token(
        self,
        film_id: str,
        segment_index: int,
        previous_segment: str | None = None,
    ) -> str:

        characters = self.load_characters(film_id)

        payload = {
            "film_id": film_id,
            "segment_index": segment_index,
            "previous_segment": previous_segment,
            "characters": [asdict(item) for item in characters],
        }

        raw = json.dumps(
            payload,
            sort_keys=True,
            ensure_ascii=False,
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    def build_reference_prompt(
        self,
        film_id: str,
        segment_index: int,
        previous_segment: str | None = None,
    ) -> str:

        characters = self.load_characters(film_id)

        if not characters:
            raise RuntimeError(
                f"No real character references registered for {film_id}. "
                "Production cannot claim character continuity."
            )

        lines = []

        for character in characters:
            lines.append(
                f"Character {character.name}: {character.description}"
            )

            if character.reference_image:
                lines.append(
                    f"Visual reference file: {character.reference_image}"
                )

        token = self.build_continuity_token(
            film_id,
            segment_index,
            previous_segment,
        )

        return (
            "CONTINUITY LOCK. "
            + " ".join(lines)
            + f" Continuity token: {token}. "
            "Do not redesign faces, hair, body proportions, costume, "
            "age, or defining visual traits between shots."
        )

    def save_segment_state(
        self,
        state: ReferenceState,
    ) -> Path:

        if not state.continuity_token:
            state.continuity_token = self.build_continuity_token(
                state.film_id,
                state.segment_index,
                state.previous_segment,
            )

        path = (
            self.film_directory(state.film_id)
            / f"segment_{state.segment_index:04d}_continuity.json"
        )

        path.write_text(
            json.dumps(
                asdict(state),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return path
