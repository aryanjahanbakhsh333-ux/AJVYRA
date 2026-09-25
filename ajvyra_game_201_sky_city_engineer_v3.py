from dataclasses import dataclass, field
from typing import Dict


@dataclass
class SkyCity:
    name: str
    population: int = 35
    energy: int = 100
    water: int = 90
    stability: int = 85
    credits: int = 180
    buildings: Dict[str, int] = field(default_factory=dict)


class SkyCityEngineer:
    def __init__(self):
        self.engineer = "Ari Voss"
        self.city = SkyCity("Aurelia")
        self.day = 1
        self.score = 0

    def construct(self, building: str):
        costs = {
            "wind_turbine": 30,
            "water_collector": 25,
            "residential_deck": 40,
            "research_lab": 55,
            "stabilizer": 70,
        }

        if building not in costs:
            return False

        cost = costs[building]

        if self.city.credits < cost:
            return False

        self.city.credits -= cost
        self.city.buildings[building] = \
            self.city.buildings.get(building, 0) + 1

        self.score += cost * 2
        return True

    def generate_energy(self):
        turbines = self.city.buildings.get("wind_turbine", 0)
        amount = 10 + turbines * 18

        self.city.energy = min(100, self.city.energy + amount)
        self.score += amount
        return amount

    def collect_water(self):
        collectors = self.city.buildings.get("water_collector", 0)
        amount = 8 + collectors * 14

        self.city.water = min(100, self.city.water + amount)
        self.score += amount
        return amount

    def stabilize_city(self):
        stabilizers = self.city.buildings.get("stabilizer", 0)

        if stabilizers <= 0 or self.city.energy < 20:
            return False

        self.city.energy -= 20
        self.city.stability = min(
            100,
            self.city.stability + 20 * stabilizers
        )
        self.score += 50
        return True

    def next_day(self):
        self.day += 1

        self.city.energy = max(0, self.city.energy - 8)
        self.city.water = max(0, self.city.water - 6)

        if self.city.stability < 50:
            self.city.population = max(
                10,
                self.city.population - 2
            )

        self.city.credits += self.city.population * 2

    def status(self):
        return {
            "engineer": self.engineer,
            "city": self.city.name,
            "day": self.day,
            "population": self.city.population,
            "energy": self.city.energy,
            "water": self.city.water,
            "stability": self.city.stability,
            "credits": self.city.credits,
            "score": self.score,
            "buildings": dict(self.city.buildings),
        }


def create_game():
    return SkyCityEngineer()


def demo():
    game = create_game()
    game.construct("wind_turbine")
    game.construct("water_collector")
    game.construct("stabilizer")
    game.generate_energy()
    game.collect_water()
    game.stabilize_city()
    game.next_day()

    return game.status()


if __name__ == "__main__":
    print(demo())
