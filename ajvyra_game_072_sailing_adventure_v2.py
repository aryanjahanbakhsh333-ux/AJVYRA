from dataclasses import dataclass
import random


@dataclass
class Island:
    name: str
    distance: int
    danger: int
    reward: int


class SailingAdventureGame:
    GAME_ID = "AJVYRA-072"
    TITLE = "Beyond the Blue Horizon"
    GENRE = "Sailing Adventure"

    def __init__(self):
        self.captain = "Aren Sol"
        self.fuel = 100
        self.hull = 100
        self.supplies = 12
        self.gold = 300
        self.position = 0

        self.islands = [
            Island("Moon Reef", 20, 15, 120),
            Island("Storm Crown", 35, 40, 250),
            Island("Emerald Isle", 50, 25, 400),
            Island("Lost Haven", 70, 60, 800),
        ]

    def sail(self, island_index: int):
        if island_index < 0 or island_index >= len(self.islands):
            return False

        island = self.islands[island_index]

        if self.fuel < island.distance:
            return False

        self.fuel -= island.distance
        self.supplies -= 1

        damage = random.randint(0, island.danger)

        self.hull = max(0, self.hull - damage)
        self.gold += island.reward

        self.position = island_index

        return {
            "island": island.name,
            "damage": damage,
            "gold": self.gold,
        }

    def repair(self):
        if self.gold < 100:
            return False

        self.gold -= 100
        self.hull = min(100, self.hull + 30)
        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "captain": self.captain,
            "fuel": self.fuel,
            "hull": self.hull,
            "supplies": self.supplies,
            "gold": self.gold,
            "position": self.position,
        }
