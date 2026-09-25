from dataclasses import dataclass
from typing import List


@dataclass
class MysticPlant:
    name: str
    water_need: int
    magic: int
    growth: int = 0
    healthy: bool = True


class MysticGardenKeeper:
    def __init__(self):
        self.keeper = "Elara Wyn"
        self.water = 120
        self.mana = 80
        self.score = 0
        self.garden_level = 1

        self.plants: List[MysticPlant] = [
            MysticPlant("Moon Lily", 10, 15),
            MysticPlant("Silver Vine", 12, 20),
            MysticPlant("Star Orchid", 18, 35),
            MysticPlant("Dream Moss", 8, 12),
        ]

    def water_plant(self, index: int):
        if not (0 <= index < len(self.plants)):
            return False

        plant = self.plants[index]

        if self.water < plant.water_need:
            return False

        self.water -= plant.water_need
        plant.growth += 10
        self.score += 15
        return True

    def magic_growth(self, index: int):
        if not (0 <= index < len(self.plants)):
            return False

        plant = self.plants[index]

        if self.mana < plant.magic:
            return False

        self.mana -= plant.magic
        plant.growth += 25
        self.score += plant.magic * 2
        return True

    def harvest(self, index: int):
        if not (0 <= index < len(self.plants)):
            return False

        plant = self.plants[index]

        if plant.growth < 50:
            return False

        plant.growth -= 40
        self.score += 80
        return True

    def restore_garden(self):
        healthy = sum(plant.healthy for plant in self.plants)

        self.mana = min(100, self.mana + healthy * 5)
        self.water = min(150, self.water + 20)
        self.garden_level += 1
        self.score += 50

    def status(self):
        return {
            "keeper": self.keeper,
            "water": self.water,
            "mana": self.mana,
            "garden_level": self.garden_level,
            "score": self.score,
            "plants": [
                {
                    "name": p.name,
                    "growth": p.growth,
                    "healthy": p.healthy,
                }
                for p in self.plants
            ],
        }


def create_game():
    return MysticGardenKeeper()


def demo():
    game = create_game()

    for i in range(4):
        game.water_plant(i)
        game.magic_growth(i)

    game.harvest(2)
    game.restore_garden()

    return game.status()


if __name__ == "__main__":
    print(demo())
