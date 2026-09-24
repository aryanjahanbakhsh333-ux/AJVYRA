from dataclasses import dataclass


@dataclass
class Civilization:
    name: str
    population: int
    food: int
    technology: int
    culture: int


class CivilizationEvolutionGame:
    GAME_ID = "AJVYRA-091"
    TITLE = "Dawn of Civilizations"
    GENRE = "Civilization Strategy"

    def __init__(self):
        self.leader = "Aren Sol"
        self.year = 1
        self.resources = 500

        self.civilization = Civilization(
            "Solara",
            population=100,
            food=200,
            technology=10,
            culture=10,
        )

    def develop(self, branch: str):
        costs = {
            "technology": 80,
            "culture": 60,
            "agriculture": 50,
        }

        if branch not in costs or self.resources < costs[branch]:
            return False

        self.resources -= costs[branch]

        if branch == "technology":
            self.civilization.technology += 5
        elif branch == "culture":
            self.civilization.culture += 5
        elif branch == "agriculture":
            self.civilization.food += 80
            self.civilization.population += 20

        return True

    def advance_year(self):
        self.year += 1

        food_needed = self.civilization.population * 2

        if self.civilization.food >= food_needed:
            self.civilization.food -= food_needed
            self.civilization.population += 10
            self.resources += 100
        else:
            self.civilization.population = max(
                1,
                self.civilization.population - 15
            )

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "year": self.year,
            "resources": self.resources,
            "civilization": self.civilization.__dict__.copy(),
        }
