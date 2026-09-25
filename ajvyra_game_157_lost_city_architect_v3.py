"""
AJVYRA 157 — Lost City Architect
Genre: Building / Puzzle
"""

from dataclasses import dataclass


@dataclass
class Building:
    name: str
    cost: int
    population: int
    stability: int


class LostCityArchitect:
    title = "Lost City Architect"
    architect = "Eren Vale"

    def __init__(self):
        self.gold = 3000
        self.population = 100
        self.stability = 50
        self.score = 0

        self.available = [
            Building("Water Tower", 400, 20, 15),
            Building("Market", 600, 35, 10),
            Building("Library", 800, 25, 20),
            Building("Sky Garden", 1000, 40, 25),
        ]

        self.built = []

    def build(self, building_name):
        building = next(
            (
                b for b in self.available
                if b.name == building_name
            ),
            None,
        )

        if building is None:
            return False

        if building.name in self.built:
            return False

        if self.gold < building.cost:
            return False

        self.gold -= building.cost
        self.built.append(building.name)

        self.population += building.population
        self.stability = min(
            100,
            self.stability + building.stability,
        )

        self.score += building.cost // 2
        return True

    def collect_taxes(self):
        income = max(
            50,
            self.population // 2,
        )

        self.gold += income
        self.score += income
        return income

    def restore_ruins(self):
        if self.gold < 500:
            return False

        self.gold -= 500
        self.stability = min(
            100,
            self.stability + 12,
        )
        self.score += 200
        return True

    def status(self):
        return {
            "architect": self.architect,
            "gold": self.gold,
            "population": self.population,
            "stability": self.stability,
            "score": self.score,
            "built": list(self.built),
        }


def create_game():
    return LostCityArchitect()


if __name__ == "__main__":
    game = create_game()
    game.build("Water Tower")
    game.build("Market")
    game.collect_taxes()
    print(game.status())
