from dataclasses import dataclass, asdict, field
from typing import Dict, List


@dataclass
class DialogueLine:
    dialogue_id: str
    scene_id: str

    character_id: str

    text: str
    language: str = "en"

    emotion: str = "neutral"
    intensity: float = 0.5

    speed: float = 1.0
    pitch: float = 1.0

    pause_before_ms: int = 0
    pause_after_ms: int = 0

    voice_id: str = ""

    audio_file: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class DialogueEngine:

    SUPPORTED_LANGUAGES = {"fa", "ja", "en"}

    def __init__(self):
        self.dialogues: Dict[str, DialogueLine] = {}

    def create(
        self,
        dialogue_id: str,
        scene_id: str,
        character_id: str,
        text: str,
        language: str = "fa",
        emotion: str = "neutral"
    ) -> DialogueLine:

        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        if dialogue_id in self.dialogues:
            raise ValueError("Dialogue ID already exists.")

        line = DialogueLine(
            dialogue_id=dialogue_id,
            scene_id=scene_id,
            character_id=character_id,
            text=text,
            language=language,
            emotion=emotion
        )

        self.dialogues[dialogue_id] = line

        return line

    def assign_voice(
        self,
        dialogue_id: str,
        voice_id: str
    ):
        self.dialogues[dialogue_id].voice_id = voice_id

    def set_emotion(
        self,
        dialogue_id: str,
        emotion: str,
        intensity: float
    ):
        line = self.dialogues[dialogue_id]

        line.emotion = emotion
        line.intensity = max(
            0.0,
            min(1.0, intensity)
        )

    def get(
        self,
        dialogue_id: str
    ) -> DialogueLine | None:

        return self.dialogues.get(dialogue_id)

    def scene_dialogues(
        self,
        scene_id: str
    ) -> List[DialogueLine]:

        return [
            line
            for line in self.dialogues.values()
            if line.scene_id == scene_id
        ]


if __name__ == "__main__":
    engine = DialogueEngine()

    line = engine.create(
        "DIALOGUE-001",
        "SCENE-001",
        "CHAR-001",
        "من نمی‌دونم چرا برگشتی.",
        language="fa",
        emotion="sad"
    )

    engine.assign_voice(
        "DIALOGUE-001",
        "VOICE-002"
    )

    print(line.to_dict())
