"""
AJVYRA CINEMATIC VISUAL DIRECTOR
--------------------------------
Creates production-ready visual specifications from:

- character identity
- world state
- emotion
- genre
- cinematic direction

The output is provider-neutral.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class VisualCharacterState:
    character_id: str
    identity_lock: str
    name: str
    appearance: str
    clothing: str
    emotion: str
    body_language: str
    eye_direction: str


@dataclass
class VisualEnvironment:
    location: str
    time_of_day: str
    weather: str
    lighting: str
    atmosphere: str
    architecture: str = ""
    foreground: str = ""
    background: str = ""


@dataclass
class CinematicVisualSpec:
    film_id: str
    moment_id: str

    aspect_ratio: str
    resolution: str

    visual_style: str
    composition: str
    camera: Dict[str, str]

    characters: List[
        VisualCharacterState
    ] = field(default_factory=list)

    environment: Optional[
        VisualEnvironment
    ] = None

    prompt: str = ""
    negative_prompt: str = ""

    continuity_token: str = ""


class AJVYRACinematicVisualDirector:
    VERSION = "1.0.0"

    def __init__(
        self,
        film_id: str,
        genre: str,
        visual_style: str = (
            "cinematic original anime"
        ),
    ) -> None:
        self.film_id = film_id
        self.genre = genre
        self.visual_style = visual_style

    def build(
        self,
        moment_id: str,
        characters: List[
            VisualCharacterState
        ],
        environment: VisualEnvironment,
        camera: Dict[str, str],
        emotion: str,
        composition: str = (
            "cinematic balanced composition"
        ),
        aspect_ratio: str = "16:9",
        resolution: str = "1920x1080",
    ) -> CinematicVisualSpec:

        continuity_token = self._continuity_token(
            characters,
            environment,
        )

        prompt = self._build_prompt(
            characters=characters,
            environment=environment,
            camera=camera,
            emotion=emotion,
            composition=composition,
        )

        negative_prompt = self._negative_prompt()

        return CinematicVisualSpec(
            film_id=self.film_id,
            moment_id=moment_id,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            visual_style=self.visual_style,
            composition=composition,
            camera=camera,
            characters=characters,
            environment=environment,
            prompt=prompt,
            negative_prompt=negative_prompt,
            continuity_token=continuity_token,
        )

    def _build_prompt(
        self,
        characters: List[
            VisualCharacterState
        ],
        environment: VisualEnvironment,
        camera: Dict[str, str],
        emotion: str,
        composition: str,
    ) -> str:

        character_text = []

        for character in characters:
            character_text.append(
                (
                    f"{character.name}: "
                    f"{character.appearance}; "
                    f"wearing {character.clothing}; "
                    f"emotion {character.emotion}; "
                    f"body language "
                    f"{character.body_language}; "
                    f"eye direction "
                    f"{character.eye_direction}; "
                    f"identity lock "
                    f"{character.identity_lock}"
                )
            )

        characters_block = "\n".join(
            character_text
        )

        return f"""
Create a cinematic original anime moment.

STYLE:
{self.visual_style}

GENRE:
{self.genre}

EMOTIONAL STATE:
{emotion}

COMPOSITION:
{composition}

CAMERA:
shot scale: {camera.get("shot_scale", "medium")}
angle: {camera.get("angle", "eye level")}
movement: {camera.get("movement", "subtle")}
lens: {camera.get("lens_feel", "cinematic")}
focus: {camera.get("focus_target", "primary subject")}
depth of field: {camera.get("depth_of_field", "moderate")}

CHARACTERS:
{characters_block}

ENVIRONMENT:
location: {environment.location}
time: {environment.time_of_day}
weather: {environment.weather}
lighting: {environment.lighting}
atmosphere: {environment.atmosphere}
architecture: {environment.architecture}
foreground: {environment.foreground}
background: {environment.background}

PRIORITIES:
- preserve character identity
- preserve clothing continuity
- preserve environment continuity
- preserve emotional acting
- cinematic composition
- natural body movement
- coherent spatial relationships
- no random character redesign
""".strip()

    @staticmethod
    def _negative_prompt() -> str:
        return (
            "character identity drift, inconsistent face, "
            "different hairstyle, random clothing change, "
            "extra fingers, malformed hands, duplicate limbs, "
            "duplicate character, broken anatomy, "
            "unmotivated camera movement, random text, "
            "watermark, logo, UI, low detail, "
            "inconsistent lighting, inconsistent environment"
        )

    @staticmethod
    def _continuity_token(
        characters: List[
            VisualCharacterState
        ],
        environment: VisualEnvironment,
    ) -> str:
        payload = {
            "characters": [
                asdict(character)
                for character in characters
            ],
            "environment": asdict(
                environment
            ),
        }

        raw = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:32]

    def save(
        self,
        spec: CinematicVisualSpec,
        path: str | Path,
    ) -> Path:
        target = Path(path)
        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                asdict(spec),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target


if __name__ == "__main__":
    director = (
        AJVYRACinematicVisualDirector(
            film_id="veyllora_01",
            genre="dark_fantasy",
        )
    )

    spec = director.build(
        moment_id="moment_0042",
        emotion="restrained grief",
        characters=[
            VisualCharacterState(
                character_id="vey_01",
                identity_lock="vey_identity_001",
                name="Veylora",
                appearance=(
                    "adult anime woman, "
                    "silver-black hair, "
                    "violet eyes"
                ),
                clothing=(
                    "long black cinematic coat"
                ),
                emotion="restrained grief",
                body_language=(
                    "almost completely still"
                ),
                eye_direction="downward",
            )
        ],
        environment=VisualEnvironment(
            location="Moonlit Harbor",
            time_of_day="night",
            weather="light rain",
            lighting="cold soft side light",
            atmosphere="mist and distant rain",
            architecture="old coastal buildings",
            foreground="wet stone pavement",
            background="dark ocean and harbor lights",
        ),
        camera={
            "shot_scale": "close_up",
            "angle": "eye_level",
            "movement": "very_slow_push_in",
            "lens_feel": "compressed_intimate",
            "focus_target": "Veylora",
            "depth_of_field": "shallow",
        },
    )

    print(
        json.dumps(
            asdict(spec),
            ensure_ascii=False,
            indent=2,
        )
    )
