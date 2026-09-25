from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Kingdom:
    ruler: str
    gold: int = 250
    food: int = 120
    army: int = 50
    happiness: int = 70
    population: int = 100
    buildings: Dict[str, int] = field(default_factory=dict)


class ForgottenKingdomBuilder:
    def __init__(self):
        self.kingdom = Kingdom("Queen Aria")
        self.year = 1
        self.score = 0

    def build(self, building: str):
        costs = {
            "farm": 30,
            "house": 25,
            "barracks": 50,
            "market": 45,
            "library": 60,
        }

        if building not in costs:
            return False

        cost = costs[building]

        if self.kingdom.gold < cost:
            return False

        self.kingdom.gold -= cost
        self.kingdom.buildings[building] = \
            self.kingdom.buildings.get(building, 0) + 1

        self.score += cost * 2
        return True

    def collect_taxes(self):
        market = self.kingdom.buildings.get("market", 0)
        income = 25 + market * 20

        self.kingdom.gold += income
        self.score += income
        return income

    def harvest(self):
        farms = self.kingdom.buildings.get("farm", 0)
        amount = 15 + farms * 20

        self.kingdom.food += amount
        self.score += amount
        return amount

    def train_guard(self):
        barracks = self.kingdom.buildings.get("barracks", 0)

        if barracks <= 0 or self.kingdom.gold < 20:
            return False

        self.kingdom.gold -= 20
        self.kingdom.army += 10 * barracks
        self.score += 35
        return True

    def festival(self):
        if self.kingdom.food < 30:
            return False

        self.kingdom.food -= 30
        self.kingdom.happiness = min(
            100,
            self.kingdom.happiness + 20
        )
        self.score += 60
        return True

    def next_year(self):
        self.year += 1

        food_need = max(
            10,
            self.kingdom.population // 5
        )

        self.kingdom.food = max(
            0,
            self.kingdom.food - food_need
        )

        if self.kingdom.food > 40:
            self.kingdom.population += 10
        else:
            self.kingdom.happiness = max(
                0,
                self.kingdom.happiness - 10
            )

    def status(self):
        return {
            "ruler": self.kingdom.ruler,
            "year": self.year,
            "gold": self.kingdom.gold,
            "food": self.kingdom.food,
            "army": self.kingdom.army,
            "happiness": self.kingdom.happiness,
            "population": self.kingdom.population,
            "score": self.score,
            "buildings": dict(self.kingdom.buildings),
        }


def create_game():
    return ForgottenKingdomBuilder()


def demo():
    game = create_game()

    game.build("farm")
    game.build("market")
    game.build("barracks")
    game.harvest()
    game.collect_taxes()
    game.train_guard()
    game.festival()
    game.next_year()

    return game.status()


if __name__ == "__main__":
    print(demo())
