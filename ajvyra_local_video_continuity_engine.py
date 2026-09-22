from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import hashlib
import json


@dataclass
class AJVYRACharacterVisualReference:
    character_id: str
    reference_image: str

    appearance_description: str = ""
    clothing_description: str = ""
    hair_description: str = ""
    eye_description: str = ""

    def validate(self) -> None:
        path = Path(self.reference_image)

        if not path.exists():
            raise FileNotFoundError(
                f"Character reference not found: {path}"
            )

        if not self.character_id.strip():
            raise ValueError(
                "character_id cannot be empty"
            )


@dataclass
class AJVYRAContinuityState:
    film_id: str
    scene_id: str
    shot_index: int

    previous_video: Optional[str] = None
    previous_frame: Optional[str] = None

    character_ids: tuple[str, ...] = ()
    location_id: Optional[str] = None

    visual_token: str = ""

    def fingerprint(self) -> str:
        payload = {
            "film_id": self.film_id,
            "scene_id": self.scene_id,
            "shot_index": self.shot_index,
            "previous_video": self.previous_video,
            "previous_frame": self.previous_frame,
            "character_ids": self.character_ids,
            "location_id": self.location_id,
            "visual_token": self.visual_token,
        }

        encoded = json.dumps(
            payload,
            sort_keys=True,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()


class AJVYRALocalVideoContinuityEngine:
    """
    Keeps visual identity information stable across generated shots.

    This is orchestration around the video model, not a claim that
    the underlying model guarantees perfect identity preservation.
    """

    def __init__(
        self,
        workspace: str = "./generated_video/continuity",
    ):
        self.workspace = Path(workspace)
        self.workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.characters: dict[
            str,
            AJVYRACharacterVisualReference
        ] = {}

        self.states: dict[
            str,
            AJVYRAContinuityState
        ] = {}

    def register_character(
        self,
        reference: AJVYRACharacterVisualReference,
    ) -> None:

        reference.validate()

        self.characters[
            reference.character_id
        ] = reference

    def build_visual_prompt(
        self,
        character_ids: list[str] | tuple[str, ...],
        base_prompt: str,
    ) -> str:

        parts = [base_prompt.strip()]

        for character_id in character_ids:
            reference = self.characters.get(character_id)

            if reference is None:
                raise KeyError(
                    f"Unknown character: {character_id}"
                )

            parts.append(
                f"Character {character_id}: "
                f"{reference.appearance_description}. "
                f"Hair: {reference.hair_description}. "
                f"Eyes: {reference.eye_description}. "
                f"Clothing: {reference.clothing_description}."
            )

        parts.append(
            "Maintain the same character identity, "
            "facial structure, hairstyle, eye design, "
            "clothing design and visual proportions "
            "throughout the shot."
        )

        return "\n".join(parts)

    def create_state(
        self,
        film_id: str,
        scene_id: str,
        shot_index: int,
        character_ids: list[str] | tuple[str, ...] = (),
        location_id: Optional[str] = None,
        previous_video: Optional[str] = None,
        previous_frame: Optional[str] = None,
        visual_token: str = "",
    ) -> AJVYRAContinuityState:

        state = AJVYRAContinuityState(
            film_id=film_id,
            scene_id=scene_id,
            shot_index=shot_index,
            previous_video=previous_video,
            previous_frame=previous_frame,
            character_ids=tuple(character_ids),
            location_id=location_id,
            visual_token=visual_token,
        )

        key = (
            f"{film_id}:"
            f"{scene_id}:"
            f"{shot_index}"
        )

        self.states[key] = state

        return state

    def save_state(
        self,
        state: AJVYRAContinuityState,
    ) -> Path:

        filename = (
            f"{state.film_id}_"
            f"{state.scene_id}_"
            f"{state.shot_index}.json"
        )

        path = self.workspace / filename

        payload = asdict(state)
        payload["fingerprint"] = state.fingerprint()

        path.write_text(
            json.dumps(
                payload,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def load_state(
        self,
        path: str | Path,
    ) -> AJVYRAContinuityState:

        data = json.loads(
            Path(path).read_text(
                encoding="utf-8"
            )
        )

        data.pop("fingerprint", None)

        state = AJVYRAContinuityState(
            **data
        )

        key = (
            f"{state.film_id}:"
            f"{state.scene_id}:"
            f"{state.shot_index}"
        )

        self.states[key] = state

        return state

    def next_state(
        self,
        previous: AJVYRAContinuityState,
        new_shot_index: int,
        previous_video: Optional[str] = None,
        previous_frame: Optional[str] = None,
    ) -> AJVYRAContinuityState:

        return self.create_state(
            film_id=previous.film_id,
            scene_id=previous.scene_id,
            shot_index=new_shot_index,
            character_ids=previous.character_ids,
            location_id=previous.location_id,
            previous_video=(
                previous_video
                or previous.previous_video
            ),
            previous_frame=(
                previous_frame
                or previous.previous_frame
            ),
            visual_token=previous.visual_token,
        )
