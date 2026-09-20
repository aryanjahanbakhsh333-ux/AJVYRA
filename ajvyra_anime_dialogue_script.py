from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Dialogue:
    dialogue_id: str
    scene_id: str
    character_id: str

    text_fa: str = ""
    text_ja: str = ""
    text_en: str = ""

    emotion: str = "neutral"

    pause_before: float = 0.0
    pause_after: float = 0.0

    voice_id: str = ""

    def to_dict(self):
        return asdict(self)


class DialogueScript:

    def __init__(self):
        self.lines: List[Dialogue] = []

    def add(self, dialogue: Dialogue):
        if any(
            line.dialogue_id == dialogue.dialogue_id
            for line in self.lines
        ):
            raise ValueError(
                "Dialogue ID already exists."
            )

        self.lines.append(dialogue)

    def scene(self, scene_id: str):
        return [
            line
            for line in self.lines
            if line.scene_id == scene_id
        ]

    def character(self, character_id: str):
        return [
            line
            for line in self.lines
            if line.character_id == character_id
        ]

    def count(self):
        return len(self.lines)


if __name__ == "__main__":
    script = DialogueScript()

    script.add(
        Dialogue(
            "D001",
            "SCENE-001",
            "CHAR-001",
            "صدای چی بود؟",
            "何の音だった？",
            "What was that sound?",
            "confused",
            voice_id="V001-A1"
        )
    )

    print(script.count())
