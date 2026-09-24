from dataclasses import dataclass
import random


@dataclass
class Dragon:
    name: str
    element: str
    power: int
    bond: int = 30
    health: int = 100


class DragonTamerGame:
    GAME_ID = "AJVYRA-065"
    TITLE = "Emberbond"
    GENRE = "Creature Training Adventure"

    def __init__(self):
        self.tamer = "Aren Vey"
        self.gold = 600
        self.level = 1

        self.dragons = [
            Dragon("Raku", "Fire", 72),
            Dragon("Nyra", "Storm", 68),
            Dragon("Elios", "Light", 61),
        ]

    def train(self, index: int):
        if index < 0 or index >= len(self.dragons):
            return False

        dragon = self.dragons[index]

        if self.gold < 50:
            return False

        self.gold -= 50
        dragon.power = min(100, dragon.power + random.randint(2, 6))
        dragon.bond = min(100, dragon.bond + 8)

        return True

    def battle(self, index: int, enemy_power: int):
        dragon = self.dragons[index]

        attack = dragon.power + dragon.bond // 2
        chance = max(0.15, min(0.9, attack / (attack + enemy_power)))

        won = random.random() < chance

        if won:
            self.gold += 120
            self.level += 1
            dragon.bond = min(100, dragon.bond + 5)
            return "victory"

        dragon.health = max(1, dragon.health - 25)
        return "defeat"

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "tamer": self.tamer,
            "gold": self.gold,
            "level": self.level,
            "dragons": [dragon.__dict__.copy() for dragon in self.dragons],
        }
