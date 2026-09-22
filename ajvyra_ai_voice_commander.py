from dataclasses import dataclass
from typing import Any


@dataclass
class VoiceInstruction:
    anime_id: int
    character_id: str
    language: str
    text: str
    emotion: str
    intensity: float = 1.0


class VoiceCommander:

    def __init__(self, tts_core=None):
        self.tts_core = tts_core

    def attach_core(self, tts_core) -> None:
        self.tts_core = tts_core

    def create_instruction(
        self,
        anime_id: int,
        character_id: str,
        language: str,
        text: str,
        emotion: str = "neutral",
        intensity: float = 1.0,
    ) -> VoiceInstruction:

        return VoiceInstruction(
            anime_id=anime_id,
            character_id=character_id,
            language=language,
            text=text,
            emotion=emotion,
            intensity=max(0.0, min(1.0, intensity)),
        )

    def prepare(self, instruction: VoiceInstruction) -> dict[str, Any]:
        return {
            "anime_id": instruction.anime_id,
            "character_id": instruction.character_id,
            "language": instruction.language,
            "text": instruction.text,
            "emotion": instruction.emotion,
            "intensity": instruction.intensity,
        }

    def execute(self, instruction: VoiceInstruction):
        if self.tts_core is None:
            raise RuntimeError(
                "No AJVYRA TTS core has been attached."
            )

        return self.tts_core.forward(
            request=self.tts_core.TTSInput(
                text=instruction.text,
                language=instruction.language,
                emotion=instruction.emotion,
                emotion_intensity=instruction.intensity,
            ),
            speaker_embedding=self.tts_core.create_speaker_embedding(
                instruction.character_id
            ),
        )
