from dataclasses import dataclass, asdict, field
from typing import List, Dict
import random
import string


SYLLABLES = [
    "ae", "va", "ri", "no", "ka", "el",
    "ly", "za", "th", "or", "mi", "ra",
    "ven", "shi", "ar", "en", "ix", "ia"
]


@dataclass
class AnimeCharacter:
    character_id: str
    name: str

    role: str = "supporting"
    age: int = 18

    personality: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)

    hair: str = ""
    eyes: str = ""
    clothing: str = ""

    background: str = ""
    relationships: Dict[str, str] = field(default_factory=dict)

    voice_actor_id: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class CharacterCreator:

    def __init__(self):
        self.used_names = set()

    def fictional_name(self) -> str:

        while True:
            parts = random.randint(2, 3)

            name = "".join(
                random.choice(SYLLABLES)
                for _ in range(parts)
            ).capitalize()

            if name.lower() not in self.used_names:
                self.used_names.add(name.lower())
                return name

    def character_id(self) -> str:
        return "CHAR-" + "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(8)
        )

    def create(
        self,
        role: str = "supporting",
        age: int = 18,
        personality: List[str] | None = None
    ) -> AnimeCharacter:

        return AnimeCharacter(
            character_id=self.character_id(),
            name=self.fictional_name(),
            role=role,
            age=age,
            personality=personality or []
        )


if __name__ == "__main__":
    creator = CharacterCreator()

    for _ in range(5):
        character = creator.create(
            role="main",
            personality=["calm", "curious"]
        )

        print(character.name)
