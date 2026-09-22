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
    reference_image: str
    continuity_token: str
    clothing: str
    hair: str
    eyes: str
    visual_style: str


class AJVYRACinematicReferenceContinuity:
    """
    Stores persistent visual references for cinematic characters.
    """

    def __init__(
        self,
        workspace: str | Path,
    ) -> None:
        self.workspace = Path(workspace)
        self.workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.references: dict[
            str,
            CharacterReference
        ] = {}

    def register(
        self,
        *,
        character_id: str,
        name: str,
        reference_image: str,
        clothing: str = "",
        hair: str = "",
        eyes: str = "",
        visual_style: str = "cinematic anime",
    ) -> CharacterReference:

        image = Path(reference_image)

        if not image.exists():
            raise FileNotFoundError(
                f"Character reference does not exist: {image}"
            )

        if image.stat().st_size <= 0:
            raise RuntimeError(
                f"Character reference is empty: {image}"
            )

        token_source = "|".join(
            [
                character_id,
                name,
                clothing,
                hair,
                eyes,
                visual_style,
                str(image.resolve()),
            ]
        )

        continuity_token = hashlib.sha256(
            token_source.encode("utf-8")
        ).hexdigest()[:24]

        reference = CharacterReference(
            character_id=character_id,
            name=name,
            reference_image=str(image.resolve()),
            continuity_token=continuity_token,
            clothing=clothing,
            hair=hair,
            eyes=eyes,
            visual_style=visual_style,
        )

        self.references[character_id] = reference
        self._save(reference)

        return reference

    def get(
        self,
        character_id: str,
    ) -> Optional[CharacterReference]:
        return self.references.get(character_id)

    def build_prompt(
        self,
        character_id: str,
        scene_prompt: str,
    ) -> str:

        reference = self.get(character_id)

        if reference is None:
            raise KeyError(
                f"Character '{character_id}' has no reference."
            )

        return (
            f"{reference.visual_style}. "
            f"Maintain the same fictional character identity. "
            f"Character: {reference.name}. "
            f"Hair: {reference.hair}. "
            f"Eyes: {reference.eyes}. "
            f"Clothing: {reference.clothing}. "
            f"Continuity token: {reference.continuity_token}. "
            f"Scene direction: {scene_prompt}"
        )

    def all_references(self) -> list[CharacterReference]:
        return list(self.references.values())

    def _save(
        self,
        reference: CharacterReference,
    ) -> None:

        path = (
            self.workspace
            / "character_references"
            / f"{reference.character_id}.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                asdict(reference),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
