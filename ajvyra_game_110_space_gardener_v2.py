"""
AJVYRA Game 110 - Space Gardener
Genre: Space Farming / Resource Management
"""

from dataclasses import dataclass


@dataclass
class Plant:
    name: str
    water: int
    light: int
    growth: int = 0
    alive: bool = True


class SpaceGardener:
    title = "Space Gardener"
    character = "Lio Astra"

    def __init__(self):
        self.day = 1
        self.water = 100
        self.oxygen = 20
        self.energy = 100
        self.score = 0

        self.plants = [
            Plant("Moon Basil", 30, 60),
            Plant("Red Tomato", 35, 70),
            Plant("Star Bean", 25, 50),
            Plant("Orbit Flower", 20, 80),
        ]

        self.log = []

    def water_plant(self, index, amount=15):
        if not 0 <= index < len(self.plants):
            return False

        if self.water < amount:
            self.log.append("The water tank is empty.")
            return False

        plant = self.plants[index]

        if not plant.alive:
            return False

        self.water -= amount
        plant.water += amount
        self.log.append(f"{plant.name} received water.")
        return True

    def adjust_light(self, index, amount):
        if not 0 <= index < len(self.plants):
            return False

        plant = self.plants[index]
        plant.light = max(0, min(100, plant.light + amount))
        self.energy = max(0, self.energy - 2)
        return True

    def grow(self):
        for plant in self.plants:
            if not plant.alive:
                continue

            water_ok = 20 <= plant.water <= 80
            light_ok = 40 <= plant.light <= 90

            if water_ok and light_ok:
                plant.growth += 12
                self.oxygen += 3
                self.score += 10
            else:
                plant.growth = max(0, plant.growth - 3)

            plant.water = max(0, plant.water - 10)

            if plant.water == 0:
                plant.alive = False

        self.day += 1
        self.water = min(100, self.water + 25)
        self.energy = min(100, self.energy + 20)

    def harvest(self, index):
        if not 0 <= index < len(self.plants):
            return False

        plant = self.plants[index]

        if plant.growth >= 100 and plant.alive:
            self.score += 100
            plant.growth = 0
            plant.water = 30
            self.log.append(f"{plant.name} was harvested.")
            return True

        return False

    def snapshot(self):
        return {
            "gardener": self.character,
            "day": self.day,
            "water": self.water,
            "oxygen": self.oxygen,
            "energy": self.energy,
            "score": self.score,
            "plants": [
                {
                    "name": p.name,
                    "water": p.water,
                    "light": p.light,
                    "growth": p.growth,
                    "alive": p.alive,
                }
                for p in self.plants
            ],
        }


def create_game():
    return SpaceGardener()


if __name__ == "__main__":
    game = create_game()

    for _ in range(5):
        game.water_plant(0)
        game.grow()

    print(game.snapshot())
