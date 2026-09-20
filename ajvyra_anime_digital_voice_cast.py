from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class DigitalVoiceActor:
    voice_id: str

    voice_name: str
    gender_style: str = "neutral"
    age_style: str = "young_adult"

    languages: List[str] = field(
        default_factory=lambda: ["fa", "ja"]
    )

    pitch: float = 1.0
    speed: float = 1.0

    personality_style: str = "natural"
    emotional_range: List[str] = field(
        default_factory=lambda: [
            "calm",
            "sad",
            "happy",
            "angry",
            "fear"
        ]
    )

    provider: str = "tts"
    provider_voice_id: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class DigitalVoiceCast:

    def __init__(self):
        self.voices: Dict[str, DigitalVoiceActor] = {}
        self.character_assignments: Dict[str, str] = {}

    def add_voice(
        self,
        voice: DigitalVoiceActor
    ):
        if voice.voice_id in self.voices:
            raise ValueError("Voice ID already exists.")

        self.voices[voice.voice_id] = voice

    def assign(
        self,
        character_id: str,
        voice_id: str
    ):
        if voice_id not in self.voices:
            raise KeyError("Voice actor does not exist.")

        self.character_assignments[character_id] = voice_id

    def voice_for(
        self,
        character_id: str
    ) -> DigitalVoiceActor | None:

        voice_id = self.character_assignments.get(character_id)

        if voice_id is None:
            return None

        return self.voices.get(voice_id)

    def available_voices(self) -> List[Dict]:
        return [
            voice.to_dict()
            for voice in self.voices.values()
        ]


if __name__ == "__main__":
    cast = DigitalVoiceCast()

    cast.add_voice(
        DigitalVoiceActor(
            voice_id="VOICE-001",
            voice_name="Veyra",
            gender_style="female",
            personality_style="soft cinematic"
        )
    )

    cast.add_voice(
        DigitalVoiceActor(
            voice_id="VOICE-002",
            voice_name="Kaelor",
            gender_style="male",
            personality_style="deep calm"
        )
    )

    cast.assign("CHAR-001", "VOICE-002")

    voice = cast.voice_for("CHAR-001")

    if voice:
        print(voice.voice_name)
