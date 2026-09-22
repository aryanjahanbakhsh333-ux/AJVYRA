from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class DigitalVoiceProfile:
    voice_id: str
    character_id: str
    character_name: str

    language: str = "fa"

    gender_style: str = "neutral"
    age_style: str = "young_adult"

    personality: str = "calm"
    emotional_style: str = "cinematic"

    speed: float = 1.0
    pitch: float = 0.0
    energy: float = 1.0

    model_id: str = (
        "KEYHAN-A/aava-tts-persian-3b"
    )


class AJVYRADigitalVoiceConfig:

    def __init__(
        self,
        root: str | Path = "ajvyra_digital_voices",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_profile(
        self,
        voice_id: str,
        character_id: str,
        character_name: str,
        personality: str,
        emotional_style: str = "cinematic",
        speed: float = 1.0,
        pitch: float = 0.0,
        energy: float = 1.0,
    ) -> DigitalVoiceProfile:

        profile = DigitalVoiceProfile(
            voice_id=voice_id,
            character_id=character_id,
            character_name=character_name,
            personality=personality,
            emotional_style=emotional_style,
            speed=max(0.5, min(speed, 1.5)),
            pitch=max(-6.0, min(pitch, 6.0)),
            energy=max(0.2, min(energy, 2.0)),
        )

        self.save(profile)

        return profile

    def save(
        self,
        profile: DigitalVoiceProfile,
    ) -> Path:

        path = (
            self.root
            / f"{profile.voice_id}.json"
        )

        path.write_text(
            json.dumps(
                asdict(profile),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return path

    def load(
        self,
        voice_id: str,
    ) -> DigitalVoiceProfile:

        path = (
            self.root
            / f"{voice_id}.json"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Voice profile not found: {voice_id}"
            )

        return DigitalVoiceProfile(
            **json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        )
