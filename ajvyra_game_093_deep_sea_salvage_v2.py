from dataclasses import dataclass
import random


@dataclass
class Wreck:
    name: str
    depth: int
    value: int
    danger: int
    recovered: bool = False


class DeepSeaSalvageGame:
    GAME_ID = "AJVYRA-093"
    TITLE = "Abyss Salvagers"
    GENRE = "Deep Sea Salvage"

    def __init__(self):
        self.diver = "Nera Voss"
        self.air = 100
        self.hull = 100
        self.money = 400

        self.wrecks = [
            Wreck("The Silver Dawn", 80, 300, 15),
            Wreck("Black Mariner", 150, 600, 30),
            Wreck("Atlas", 240, 1200, 45),
            Wreck("Abyss Queen", 400, 2500, 70),
        ]

    def dive(self, index: int):
        if index < 0 or index >= len(self.wrecks):
            return False

        wreck = self.wrecks[index]

        if wreck.recovered or self.air < 20:
            return False

        self.air -= 20

        danger_roll = random.randint(1, 100)

        if danger_roll <= wreck.danger:
            self.hull = max(0, self.hull - random.randint(5, 20))
            return {"success": False, "danger": True}

        wreck.recovered = True
        self.money += wreck.value

        return {
            "success": True,
            "treasure": wreck.name,
            "value": wreck.value,
        }

    def surface(self):
        self.air = 100

    def repair(self):
        if self.money < 150:
            return False

        self.money -= 150
        self.hull = min(100, self.hull + 30)

        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "diver": self.diver,
            "air": self.air,
            "hull": self.hull,
            "money": self.money,
            "wrecks": [w.__dict__.copy() for w in self.wrecks],
        }
