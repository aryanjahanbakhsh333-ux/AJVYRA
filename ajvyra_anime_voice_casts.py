from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class VoiceProfile:
    voice_id: str
    name: str

    gender_style: str
    age_style: str

    languages: List[str]

    personality: str
    emotion_range: List[str]

    pitch: float = 1.0
    speed: float = 1.0

    def to_dict(self):
        return asdict(self)


class VoiceCastManager:

    def __init__(self):
        self.casts: Dict[int, Dict[str, VoiceProfile]] = {}

    def create_cast(self, anime_id: int):
        self.casts.setdefault(anime_id, {})

    def add_voice(
        self,
        anime_id: int,
        voice: VoiceProfile
    ):
        self.create_cast(anime_id)

        if voice.voice_id in self.casts[anime_id]:
            raise ValueError(
                "Voice ID already exists in this cast."
            )

        self.casts[anime_id][voice.voice_id] = voice

    def assign(
        self,
        anime_id: int,
        character_id: str,
        voice_id: str
    ):
        self.create_cast(anime_id)

        if voice_id not in self.casts[anime_id]:
            raise KeyError("Voice does not exist.")

        return {
            "anime_id": anime_id,
            "character_id": character_id,
            "voice_id": voice_id
        }

    def get_cast(self, anime_id: int):
        return list(
            self.casts.get(anime_id, {}).values()
        )


if __name__ == "__main__":
    manager = VoiceCastManager()

    manager.add_voice(
        1,
        VoiceProfile(
            "V001-A1",
            "VaelithVoice",
            "male",
            "young",
            ["fa", "ja"],
            "quiet and serious",
            ["calm", "sad", "angry", "fear"]
        )
    )

    print(manager.get_cast(1))
