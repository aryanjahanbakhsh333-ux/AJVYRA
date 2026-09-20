from dataclasses import dataclass, asdict, field
from typing import Dict, List


@dataclass
class CharacterRecord:
    character_id: str
    anime_id: int
    name: str

    role: str
    personality: List[str] = field(default_factory=list)

    goal: str = ""
    fear: str = ""
    background: str = ""

    age: int = 18
    visual_identity: str = ""

    voice_id: str = ""

    def to_dict(self):
        return asdict(self)


class CharacterRegistry:

    def __init__(self):
        self.characters: Dict[str, CharacterRecord] = {}
        self.names = set()

    def register(self, character: CharacterRecord):

        normalized = character.name.strip().lower()

        if normalized in self.names:
            raise ValueError(
                f"Character name already used: {character.name}"
            )

        if character.character_id in self.characters:
            raise ValueError("Character ID already exists.")

        self.characters[character.character_id] = character
        self.names.add(normalized)

    def get(self, character_id: str):
        return self.characters.get(character_id)

    def anime_characters(self, anime_id: int):
        return [
            character
            for character in self.characters.values()
            if character.anime_id == anime_id
        ]

    def character_names(self, anime_id: int):
        return [
            character.name
            for character in self.anime_characters(anime_id)
        ]

    def name_available(self, name: str) -> bool:
        return name.strip().lower() not in self.names

    def count(self) -> int:
        return len(self.characters)


if __name__ == "__main__":
    registry = CharacterRegistry()

    registry.register(
        CharacterRecord(
            "CHAR-001",
            1,
            "Vaelith",
            "protagonist",
            ["quiet", "curious"],
            "discover the truth",
            "losing his identity",
            "Raised near the abandoned district.",
            18
        )
    )

    print(registry.character_names(1))
