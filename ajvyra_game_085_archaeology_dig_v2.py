from dataclasses import dataclass
import random


@dataclass
class Artifact:
    name: str
    rarity: str
    value: int


class ArchaeologyDigGame:
    GAME_ID = "AJVYRA-085"
    TITLE = "Buried Kingdom"
    GENRE = "Archaeology Exploration"

    def __init__(self):
        self.archaeologist = "Sera Nox"
        self.energy = 100
        self.discovery = 0
        self.money = 300

        self.artifacts = [
            Artifact("Sun Disc", "Common", 100),
            Artifact("Royal Seal", "Rare", 300),
            Artifact("Obsidian Mask", "Epic", 600),
            Artifact("Crown of Asha", "Legendary", 1200),
        ]

    def dig(self, index: int):
        if self.energy < 10:
            return False

        self.energy -= 10

        if index < 0 or index >= len(self.artifacts):
            return False

        artifact = self.artifacts[index]

        chance = random.randint(1, 100)

        if chance <= 65:
            self.discovery += artifact.value
            self.money += artifact.value
            return {
                "found": True,
                "artifact": artifact.name,
                "value": artifact.value,
            }

        return {
            "found": False,
            "artifact": None,
        }

    def rest(self):
        self.energy = min(100, self.energy + 30)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "archaeologist": self.archaeologist,
            "energy": self.energy,
            "discovery": self.discovery,
            "money": self.money,
        }
