from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

from ajvyra_digital_voice_config import (
    AJVYRADigitalVoiceConfig,
    DigitalVoiceProfile,
)

from ajvyra_digital_voice_engine import (
    AJVYRADigitalVoiceEngine,
)

from ajvyra_digital_voice_director import (
    AJVYRADigitalVoiceDirector,
)


@dataclass
class AnimeDialogue:
    film_id: str
    segment_index: int

    character_id: str
    character_name: str

    text: str

    emotion: str

    start: float
    end: float


@dataclass
class ProducedDialogue:
    dialogue: AnimeDialogue
    audio_path: str
    success: bool


class AJVYRAAnimeDigitalVoiceProducer:

    def __init__(
        self,
        root: str | Path = "ajvyra_anime_voice_output",
    ):

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.config = (
            AJVYRADigitalVoiceConfig(
                self.root / "profiles"
            )
        )

        self.engine = (
            AJVYRADigitalVoiceEngine()
        )

        self.director = (
            AJVYRADigitalVoiceDirector()
        )

    def create_character_voice(
        self,
        character_id: str,
        character_name: str,
        personality: str,
        emotional_style: str = "cinematic",
    ) -> DigitalVoiceProfile:

        voice_id = (
            f"ajvyra_{character_id}"
        )

        return self.config.create_profile(
            voice_id=voice_id,
            character_id=character_id,
            character_name=character_name,
            personality=personality,
            emotional_style=emotional_style,
        )

    def produce_dialogue(
        self,
        dialogue: AnimeDialogue,
        voice_profile: DigitalVoiceProfile,
    ) -> ProducedDialogue:

        directed = self.director.direct(
            text=dialogue.text,
            emotion=dialogue.emotion,
            base_speed=voice_profile.speed,
            base_pitch=voice_profile.pitch,
            base_energy=voice_profile.energy,
        )

        output = (
            self.root
            / dialogue.film_id
            / voice_profile.voice_id
            / f"segment_{dialogue.segment_index:04d}.wav"
        )

        self.engine.generate(
            text=directed.text,
            output_path=output,
        )

        result = ProducedDialogue(
            dialogue=dialogue,
            audio_path=str(output),
            success=True,
        )

        manifest = (
            output.parent
            / "dialogue_manifest.json"
        )

        existing = []

        if manifest.exists():
            existing = json.loads(
                manifest.read_text(
                    encoding="utf-8"
                )
            )

        existing.append(
            asdict(result)
        )

        manifest.write_text(
            json.dumps(
                existing,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return result
