from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class VoiceIdentity:
    voice_id: str
    character_id: str
    anime_id: int

    language: str

    age_style: str = "young"
    gender_style: str = "neutral"

    pitch: float = 1.0
    speed: float = 1.0
    energy: float = 1.0

    warmth: float = 0.5
    darkness: float = 0.5
    breathiness: float = 0.2

    emotional_range: float = 0.8


class VoiceIdentityStore:

    def __init__(self, root: str | Path = "ajvyra_tts_data/voices"):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, voice: VoiceIdentity) -> Path:
        path = self.root / f"{voice.voice_id}.json"

        path.write_text(
            json.dumps(
                asdict(voice),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    def load(self, voice_id: str) -> VoiceIdentity:
        path = self.root / f"{voice_id}.json"

        if not path.exists():
            raise FileNotFoundError(
                f"Voice identity not found: {voice_id}"
            )

        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        return VoiceIdentity(**data)

    def create(
        self,
        anime_id: int,
        character_id: str,
        language: str,
        gender_style: str = "neutral",
    ) -> VoiceIdentity:

        voice_id = (
            f"anime_{anime_id:02d}_"
            f"{character_id}_"
            f"{language}"
        )

        voice = VoiceIdentity(
            voice_id=voice_id,
            character_id=character_id,
            anime_id=anime_id,
            language=language,
            gender_style=gender_style,
        )

        self.save(voice)

        return voice
