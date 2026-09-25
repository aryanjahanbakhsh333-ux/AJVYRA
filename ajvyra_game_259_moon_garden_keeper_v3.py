from dataclasses import dataclass


@dataclass
class MoonPlant:
    name: str
    growth: int
    water_need: int
    rarity: int
    alive: bool = True


class MoonGardenKeeper:
    def __init__(self):
        self.keeper = "Luna Vale"
        self.water = 300
        self.oxygen = 100
        self.energy = 100
        self.score = 0
        self.coins = 100
        self.garden_level = 1

        self.plants = [
            MoonPlant("Silver Fern", 20, 15, 20),
            MoonPlant("Lunar Rose", 35, 20, 40),
            MoonPlant("Star Lily", 50, 25, 65),
            MoonPlant("Eclipse Bloom", 70, 35, 100),
        ]

    def water_plant(self, index: int):
        if not 0 <= index < len(self.plants):
            return False

        plant = self.plants[index]

        if self.water < plant.water_need or not plant.alive:
            return False

        self.water -= plant.water_need
        plant.growth += 15
        self.score += plant.rarity
        return True

    def provide_light(self):
        if self.energy < 15:
            return False

        self.energy -= 15

        for plant in self.plants:
            if plant.alive:
                plant.growth += 5

        self.score += 40
        return True

    def harvest(self, index: int):
        if not 0 <= index < len(self.plants):
            return False

        plant = self.plants[index]

        if plant.growth < 60 or not plant.alive:
            return False

        plant.growth = 0
        self.coins += plant.rarity * 2
        self.score += plant.rarity * 3
        return True

    def collect_oxygen(self):
        self.oxygen = min(100, self.oxygen + 20)
        self.score += 15

    def upgrade_garden(self):
        cost = self.garden_level * 120

        if self.coins < cost:
            return False

        self.coins -= cost
        self.garden_level += 1
        self.water += 80
        self.score += 60
        return True

    def status(self):
        return {
            "keeper": self.keeper,
            "water": self.water,
            "oxygen": self.oxygen,
            "energy": self.energy,
            "coins": self.coins,
            "garden_level": self.garden_level,
            "score": self.score,
            "plants": [
                {
                    "name": plant.name,
                    "growth": plant.growth,
                    "alive": plant.alive,
                }
                for plant in self.plants
            ],
        }


def create_game():
    return MoonGardenKeeper()


if __name__ == "__main__":
    game = create_game()
    game.water_plant(0)
    game.provide_light()
    game.harvest(0)
    print(game.status())
