from dataclasses import dataclass
from typing import List


@dataclass
class Artifact:
    name: str
    rarity: str
    value: int
    condition: int = 100
    displayed: bool = False


class MuseumCuratorGame:
    GAME_ID = "AJVYRA-063"
    TITLE = "Museum After Midnight"
    GENRE = "Museum Simulation"

    def __init__(self):
        self.money = 3000
        self.reputation = 10
        self.visitors = 0

        self.artifacts: List[Artifact] = [
            Artifact("The Glass Moon", "Rare", 800),
            Artifact("Clock of Oris", "Epic", 1400),
            Artifact("Blue Pharaoh", "Legendary", 2500),
            Artifact("Silent Crown", "Rare", 950),
        ]

    def display_artifact(self, name: str) -> bool:
        for artifact in self.artifacts:
            if artifact.name == name:
                artifact.displayed = True
                self.reputation += 2
                self.visitors += artifact.value // 100
                return True

        return False

    def restore_artifact(self, name: str) -> bool:
        for artifact in self.artifacts:
            if artifact.name == name and artifact.condition < 100:
                cost = (100 - artifact.condition) * 4

                if self.money < cost:
                    return False

                self.money -= cost
                artifact.condition = 100
                self.reputation += 1
                return True

        return False

    def museum_income(self):
        displayed = sum(a.displayed for a in self.artifacts)
        income = displayed * 150 + self.reputation * 10

        self.money += income
        self.visitors += displayed * 20

        return income

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "money": self.money,
            "reputation": self.reputation,
            "visitors": self.visitors,
            "artifacts": [
                {
                    "name": a.name,
                    "rarity": a.rarity,
                    "value": a.value,
                    "condition": a.condition,
                    "displayed": a.displayed,
                }
                for a in self.artifacts
            ],
        }
