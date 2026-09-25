from dataclasses import dataclass, field
from typing import Dict


@dataclass
class MoonColony:
    name: str
    population: int = 8
    oxygen: int = 100
    energy: int = 100
    food: int = 80
    minerals: int = 40
    structures: Dict[str, int] = field(default_factory=dict)


class MoonColonyArchitect:
    def __init__(self):
        self.hero = "Liora Venn"
        self.colony = MoonColony("Aster-9")
        self.day = 1
        self.score = 0
        self.reputation = 0

    def build(self, structure: str):
        costs = {
            "habitat": 15,
            "solar_array": 20,
            "greenhouse": 18,
            "oxygen_station": 25,
            "mining_hub": 30,
        }

        cost = costs.get(structure)
        if cost is None:
            return False, "Unknown structure."

        if self.colony.minerals < cost:
            return False, "Not enough minerals."

        self.colony.minerals -= cost
        self.colony.structures[structure] = \
            self.colony.structures.get(structure, 0) + 1

        self.score += cost * 3
        self.reputation += 1

        return True, f"{structure} constructed."

    def mine(self):
        amount = 10 + self.colony.structures.get("mining_hub", 0) * 6
        self.colony.minerals += amount
        self.score += amount
        return amount

    def grow_food(self):
        greenhouses = self.colony.structures.get("greenhouse", 0)

        if greenhouses == 0:
            return 0

        amount = greenhouses * 12
        self.colony.food += amount
        self.score += amount * 2
        return amount

    def generate_energy(self):
        solar = self.colony.structures.get("solar_array", 0)
        amount = 10 + solar * 15
        self.colony.energy = min(100, self.colony.energy + amount)
        return amount

    def next_day(self):
        self.day += 1

        oxygen_use = max(2, self.colony.population // 3)
        food_use = max(3, self.colony.population // 2)

        self.colony.oxygen -= oxygen_use
        self.colony.food -= food_use
        self.colony.energy -= 5

        if self.colony.structures.get("oxygen_station", 0):
            self.colony.oxygen += 12

        self.colony.oxygen = max(0, min(100, self.colony.oxygen))
        self.colony.food = max(0, self.colony.food)
        self.colony.energy = max(0, self.colony.energy)

        return self.status()

    def status(self):
        return {
            "architect": self.hero,
            "colony": self.colony.name,
            "day": self.day,
            "population": self.colony.population,
            "oxygen": self.colony.oxygen,
            "energy": self.colony.energy,
            "food": self.colony.food,
            "minerals": self.colony.minerals,
            "structures": dict(self.colony.structures),
            "score": self.score,
            "reputation": self.reputation,
        }


def create_game():
    return MoonColonyArchitect()


def demo():
    game = create_game()
    game.mine()
    game.build("mining_hub")
    game.build("solar_array")
    game.build("greenhouse")
    game.grow_food()
    game.generate_energy()
    return game.next_day()


if __name__ == "__main__":
    print(demo())
