from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from ajvyra_native_visual_engine import (
    NativeVisualEngine,
    VisualCharacter,
)


@dataclass
class CharacterSpec:
    character_id: str
    name: str
    gender: str = "unknown"
    age_group: str = "young"
    hair: str = "dark"
    skin: str = "light"
    outfit: str = "dark"
    eye_style: str = "sharp"
    personality: str = "calm"
    default_expression: str = "neutral"


class NativeCharacterRenderer:
    """
    Creates deterministic visual identities for characters.

    The same character_id always receives the same visual identity.
    """

    def __init__(self, root: str | Path = "ajvyra_projects/characters"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.engine = NativeVisualEngine()

    def _stable_hash(self, value: str) -> int:
        digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
        return int(digest[:12], 16)

    def create_character(self, spec: CharacterSpec) -> Dict:
        identity_seed = self._stable_hash(
            f"{spec.character_id}:{spec.name}"
        )

        profile = {
            "character_id": spec.character_id,
            "name": spec.name,
            "gender": spec.gender,
            "age_group": spec.age_group,
            "hair": spec.hair,
            "skin": spec.skin,
            "outfit": spec.outfit,
            "eye_style": spec.eye_style,
            "personality": spec.personality,
            "default_expression": spec.default_expression,
            "visual_seed": identity_seed,
        }

        path = self.root / f"{spec.character_id}.json"

        with path.open("w", encoding="utf-8") as f:
            json.dump(
                profile,
                f,
                ensure_ascii=False,
                indent=2,
            )

        return profile

    def load_character(self, character_id: str) -> Dict:
        path = self.root / f"{character_id}.json"

        if not path.exists():
            raise FileNotFoundError(
                f"Character not found: {character_id}"
            )

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def render_character(
        self,
        character_id: str,
        output: str | Path,
        expression: str | None = None,
    ) -> Path:
        data = self.load_character(character_id)

        character = VisualCharacter(
            name=data["name"],
            x=0.50,
            y=0.91,
            scale=1.35,
            hair=data["hair"],
            skin=data["skin"],
            outfit=data["outfit"],
            expression=expression or data["default_expression"],
        )

        return self.engine.render_preview(
            output=output,
            scene_type="default",
            characters=[character],
        )

    def render_expression_set(
        self,
        character_id: str,
        output_dir: str | Path,
    ) -> List[Path]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        expressions = [
            "neutral",
            "sad",
            "happy",
            "angry",
            "fear",
        ]

        results = []

        for expression in expressions:
            path = output_dir / f"{expression}.png"

            self.render_character(
                character_id,
                path,
                expression=expression,
            )

            results.append(path)

        return results


if __name__ == "__main__":
    renderer = NativeCharacterRenderer()

    renderer.create_character(
        CharacterSpec(
            character_id="vey_001",
            name="Veyrion",
            hair="black",
            skin="pale",
            outfit="dark",
            personality="quiet",
            default_expression="sad",
        )
    )

    renderer.render_expression_set(
        "vey_001",
        "ajvyra_projects/characters/vey_001/expressions",
    )

    print("Character visual package created.")
