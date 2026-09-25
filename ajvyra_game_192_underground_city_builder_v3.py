from dataclasses import dataclass, field
from typing import Dict


@dataclass
class UndergroundCity:
    name: str
    population: int = 20
    water: int = 100
    power: int = 100
    food: int = 80
    metal: int = 60
    morale: int = 70
    buildings: Dict[str, int] = field(default_factory=dict)


class UndergroundCityBuilder:
    def __init__(self):
        self.architect = "Tarin Vox"
        self.city = UndergroundCity("Noxhaven")
        self.day = 1
        self.score = 0

    def build(self, building: str):
        costs = {
            "water_station": 20,
            "power_core": 25,
            "farm": 18,
            "housing": 15,
            "workshop": 30,
            "security_hub": 35,
        }

        if building not in costs:
            return False

        cost = costs[building]

        if self.city.metal < cost:
            return False

        self.city.metal -= cost
        self.city.buildings[building] = \
            self.city.buildings.get(building, 0) + 1

        self.score += cost * 3
        return True

    def improve_morale(self):
        if self.city.food < 10:
            return False

        self.city.food -= 10
        self.city.morale = min(100, self.city.morale + 15)
        self.score += 20
        return True

    def produce_metal(self):
        workshops = self.city.buildings.get("workshop", 0)
        amount = 8 + workshops * 10
        self.city.metal += amount
        self.score += amount
        return amount

    def next_day(self):
        self.day += 1

        water_use = max(4, self.city.population // 4)
        food_use = max(5, self.city.population // 3)

        self.city.water -= water_use
        self.city.food -= food_use
        self.city.power -= 6

        self.city.water += self.city.buildings.get(
            "water_station", 0
        ) * 12

        self.city.power += self.city.buildings.get(
            "power_core", 0
        ) * 15

        self.city.food += self.city.buildings.get(
            "farm", 0
        ) * 10

        self.city.water = max(0, min(100, self.city.water))
        self.city.power = max(0, min(100, self.city.power))
        self.city.food = max(0, self.city.food)

    def city_level(self):
        total = sum(self.city.buildings.values())
        return 1 + total // 3

    def status(self):
        return {
            "architect": self.architect,
            "city": self.city.name,
            "day": self.day,
            "population": self.city.population,
            "water": self.city.water,
            "power": self.city.power,
            "food": self.city.food,
            "metal": self.city.metal,
            "morale": self.city.morale,
            "city_level": self.city_level(),
            "score": self.score,
            "buildings": dict(self.city.buildings),
        }


def create_game():
    return UndergroundCityBuilder()


def demo():
    game = create_game()
    game.build("water_station")
    game.build("power_core")
    game.build("farm")
    game.build("workshop")
    game.produce_metal()
    game.improve_morale()
    game.next_day()
    return game.status()


if __name__ == "__main__":
    print(demo())
