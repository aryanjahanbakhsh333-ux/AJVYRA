"""
AJVYRA CINEMATIC CHARACTER INTELLIGENCE
---------------------------------------
Persistent character identity and development system.

Designed to keep a character consistent across a complete
cinematic film rather than treating each visual generation
as an unrelated image.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


def identity_hash(data: Dict) -> str:
    raw = json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


@dataclass
class AppearanceProfile:
    face: str = ""
    hair: str = ""
    eyes: str = ""
    body: str = ""
    skin_description: str = ""

    default_clothing: str = ""

    color_palette: List[str] = field(
        default_factory=list
    )

    visual_style: str = (
        "cinematic_anime"
    )


@dataclass
class PersonalityProfile:
    traits: List[str] = field(
        default_factory=list
    )

    strengths: List[str] = field(
        default_factory=list
    )

    weaknesses: List[str] = field(
        default_factory=list
    )

    fears: List[str] = field(
        default_factory=list
    )

    desires: List[str] = field(
        default_factory=list
    )

    speech_style: str = ""


@dataclass
class CharacterArc:
    starting_state: str = ""
    midpoint_change: str = ""
    lowest_point: str = ""
    final_state: str = ""


@dataclass
class CinematicCharacter:
    character_id: str
    name: str

    age_descriptor: str = (
        "adult fictional character"
    )

    role: str = "protagonist"

    appearance: AppearanceProfile = field(
        default_factory=AppearanceProfile
    )

    personality: PersonalityProfile = field(
        default_factory=PersonalityProfile
    )

    arc: CharacterArc = field(
        default_factory=CharacterArc
    )

    current_emotion: str = "neutral"
    current_location: str = ""

    clothing_state: str = ""
    physical_state: str = "healthy"

    memories: List[str] = field(
        default_factory=list
    )

    relationships: Dict[str, str] = field(
        default_factory=dict
    )

    visual_references: List[str] = field(
        default_factory=list
    )

    voice_identity: Dict[str, str] = field(
        default_factory=dict
    )

    continuity_hash: str = ""


class AJVYRACinematicCharacterIntelligence:
    VERSION = "1.0.0"

    def __init__(self) -> None:
        self.characters: Dict[
            str,
            CinematicCharacter,
        ] = {}

    # ---------------------------------------------------------
    # Character creation
    # ---------------------------------------------------------

    def create(
        self,
        character_id: str,
        name: str,
        role: str,
        appearance: Optional[
            AppearanceProfile
        ] = None,
        personality: Optional[
            PersonalityProfile
        ] = None,
        arc: Optional[CharacterArc] = None,
    ) -> CinematicCharacter:

        if character_id in self.characters:
            raise ValueError(
                f"Character already exists: "
                f"{character_id}"
            )

        character = CinematicCharacter(
            character_id=character_id,
            name=name,
            role=role,
            appearance=(
                appearance
                or AppearanceProfile()
            ),
            personality=(
                personality
                or PersonalityProfile()
            ),
            arc=arc or CharacterArc(),
        )

        character.clothing_state = (
            character.appearance.default_clothing
        )

        self._refresh_hash(character)

        self.characters[
            character_id
        ] = character

        return character

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    def identity_payload(
        self,
        character_id: str,
    ) -> Dict:
        character = self.get(
            character_id
        )

        if character is None:
            raise KeyError(character_id)

        return {
            "character_id": character.character_id,
            "name": character.name,
            "role": character.role,
            "age_descriptor": (
                character.age_descriptor
            ),
            "appearance": asdict(
                character.appearance
            ),
            "personality": asdict(
                character.personality
            ),
            "voice_identity": dict(
                character.voice_identity
            ),
            "visual_references": list(
                character.visual_references
            ),
            "identity_lock": (
                character.continuity_hash
            ),
        }

    # ---------------------------------------------------------
    # State changes
    # ---------------------------------------------------------

    def set_emotion(
        self,
        character_id: str,
        emotion: str,
    ) -> None:
        character = self._require(
            character_id
        )

        character.current_emotion = (
            emotion
        )

        self._refresh_hash(character)

    def move(
        self,
        character_id: str,
        location: str,
    ) -> None:
        character = self._require(
            character_id
        )

        character.current_location = (
            location
        )

        self._refresh_hash(character)

    def change_clothing(
        self,
        character_id: str,
        clothing: str,
    ) -> None:
        character = self._require(
            character_id
        )

        if not clothing.strip():
            raise ValueError(
                "Clothing state cannot be empty."
            )

        character.clothing_state = clothing
        self._refresh_hash(character)

    def set_physical_state(
        self,
        character_id: str,
        state: str,
    ) -> None:
        character = self._require(
            character_id
        )

        character.physical_state = state
        self._refresh_hash(character)

    def remember(
        self,
        character_id: str,
        memory: str,
    ) -> None:
        character = self._require(
            character_id
        )

        if memory and memory not in character.memories:
            character.memories.append(
                memory
            )

        self._refresh_hash(character)

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    def set_relationship(
        self,
        character_id: str,
        other_character_id: str,
        state: str,
    ) -> None:
        character = self._require(
            character_id
        )

        character.relationships[
            other_character_id
        ] = state

        self._refresh_hash(character)

    # ---------------------------------------------------------
    # References / voice
    # ---------------------------------------------------------

    def add_visual_reference(
        self,
        character_id: str,
        reference_path: str,
    ) -> None:
        character = self._require(
            character_id
        )

        if reference_path not in character.visual_references:
            character.visual_references.append(
                reference_path
            )

        self._refresh_hash(character)

    def set_voice_identity(
        self,
        character_id: str,
        language: str,
        voice_id: str,
    ) -> None:
        character = self._require(
            character_id
        )

        character.voice_identity[
            language
        ] = voice_id

        self._refresh_hash(character)

    # ---------------------------------------------------------
    # Continuity
    # ---------------------------------------------------------

    def continuity_check(
        self,
        character_id: str,
    ) -> Dict[str, object]:
        character = self._require(
            character_id
        )

        problems: List[str] = []

        if not character.name.strip():
            problems.append(
                "Missing character name."
            )

        if not character.appearance.face.strip():
            problems.append(
                "Face identity is undefined."
            )

        if not character.appearance.hair.strip():
            problems.append(
                "Hair identity is undefined."
            )

        if not character.appearance.eyes.strip():
            problems.append(
                "Eye identity is undefined."
            )

        if not character.clothing_state.strip():
            problems.append(
                "Current clothing state is undefined."
            )

        return {
            "character_id": character_id,
            "valid": not problems,
            "problems": problems,
            "identity_lock": (
                character.continuity_hash
            ),
        }

    # ---------------------------------------------------------
    # Export
    # ---------------------------------------------------------

    def export(
        self,
        directory: str | Path,
    ) -> Path:
        directory = Path(directory)
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = directory / (
            "cinematic_character_bible.json"
        )

        data = {
            "version": self.VERSION,
            "characters": {
                cid: asdict(character)
                for cid, character
                in self.characters.items()
            },
        }

        output.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return output

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def get(
        self,
        character_id: str,
    ) -> Optional[CinematicCharacter]:
        return self.characters.get(
            character_id
        )

    def _require(
        self,
        character_id: str,
    ) -> CinematicCharacter:
        character = self.get(
            character_id
        )

        if character is None:
            raise KeyError(
                f"Unknown character: "
                f"{character_id}"
            )

        return character

    def _refresh_hash(
        self,
        character: CinematicCharacter,
    ) -> None:
        payload = {
            "appearance": asdict(
                character.appearance
            ),
            "personality": asdict(
                character.personality
            ),
            "voice": character.voice_identity,
        }

        character.continuity_hash = (
            identity_hash(payload)
        )


if __name__ == "__main__":
    engine = (
        AJVYRACinematicCharacterIntelligence()
    )

    engine.create(
        character_id="char_vey_01",
        name="Veylora",
        role="protagonist",
        appearance=AppearanceProfile(
            face=(
                "adult female anime face, "
                "distinctive narrow jaw"
            ),
            hair=(
                "long silver-black hair"
            ),
            eyes=(
                "large cold violet eyes"
            ),
            body=(
                "slender adult silhouette"
            ),
            default_clothing=(
                "long black cinematic coat"
            ),
            color_palette=[
                "black",
                "silver",
                "violet",
            ],
        ),
        personality=PersonalityProfile(
            traits=[
                "quiet",
                "observant",
                "kind",
            ],
            strengths=[
                "loyalty",
                "courage",
            ],
            weaknesses=[
                "self-isolation",
            ],
            fears=[
                "losing someone again",
            ],
            desires=[
                "discover the truth",
            ],
            speech_style=(
                "short, restrained, emotional"
            ),
        ),
        arc=CharacterArc(
            starting_state=(
                "emotionally closed"
            ),
            midpoint_change=(
                "allows herself to trust"
            ),
            lowest_point=(
                "believes trust caused the loss"
            ),
            final_state=(
                "accepts truth without abandoning herself"
            ),
        ),
    )

    engine.set_voice_identity(
        "char_vey_01",
        "ja",
        "vey_voice_ja_01",
    )

    engine.set_voice_identity(
        "char_vey_01",
        "fa",
        "vey_voice_fa_01",
    )

    engine.move(
        "char_vey_01",
        "Moonlit Harbor",
    )

    print(
        json.dumps(
            engine.identity_payload(
                "char_vey_01"
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
