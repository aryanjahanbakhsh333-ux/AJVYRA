from dataclasses import dataclass


@dataclass
class FutureCity:
    name: str
    population: int = 1000
    energy: int = 500
    water: int = 500
    happiness: int = 60
    technology: int = 40
    stability: int = 70


class FutureCityArchitect:
    def __init__(self):
        self.architect = "Ayla Nova"
        self.city = FutureCity("Astra Prime")
        self.credits = 1000
        self.day = 1
        self.score = 0
        self.level = 1

    def build(self, structure: str):
        costs = {
            "sky_habitat": 220,
            "fusion_core": 300,
            "water_recycler": 180,
            "ai_transit": 250,
            "research_dome": 280,
        }

        if structure not in costs:
            return False

        if self.credits < costs[structure]:
            return False

        self.credits -= costs[structure]

        if structure == "sky_habitat":
            self.city.population += 300
            self.city.happiness += 5

        elif structure == "fusion_core":
            self.city.energy += 400
            self.city.stability += 5

        elif structure == "water_recycler":
            self.city.water += 350

        elif structure == "ai_transit":
            self.city.happiness += 12
            self.city.stability += 4

        elif structure == "research_dome":
            self.city.technology += 20

        self.score += costs[structure] // 2
        return True

    def optimize_energy(self):
        if self.city.technology < 30:
            return False

        self.city.energy += 150
        self.city.stability = min(
            100,
            self.city.stability + 8
        )
        self.score += 50
        return True

    def improve_happiness(self):
        if self.credits < 100:
            return False

        self.credits -= 100
        self.city.happiness = min(
            100,
            self.city.happiness + 10
        )
        self.score += 40
        return True

    def advance_day(self):
        self.day += 1

        self.city.energy = max(
            0,
            self.city.energy - self.city.population // 5
        )
        self.city.water = max(
            0,
            self.city.water - self.city.population // 6
        )

        self.credits += self.city.population // 12

        if self.score >= self.level * 700:
            self.level += 1

    def status(self):
        return {
            "architect": self.architect,
            "city": self.city.name,
            "day": self.day,
            "level": self.level,
            "population": self.city.population,
            "energy": self.city.energy,
            "water": self.city.water,
            "happiness": self.city.happiness,
            "technology": self.city.technology,
            "stability": self.city.stability,
            "credits": self.credits,
            "score": self.score,
        }


def create_game():
    return FutureCityArchitect()


if __name__ == "__main__":
    game = create_game()
    game.build("fusion_core")
    game.build("water_recycler")
    game.build("research_dome")
    game.optimize_energy()
    game.advance_day()
    print(game.status())
