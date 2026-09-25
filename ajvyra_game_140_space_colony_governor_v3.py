"""
AJVYRA 140 — Space Colony Governor
Genre: Colony Management / Strategy
"""

from dataclasses import dataclass


@dataclass
class ColonySector:
    name: str
    population: int
    housing: int
    energy: int
    food: int


class SpaceColonyGovernor:
    title = "Space Colony Governor"
    governor = "Nova Rey"

    def __init__(self):
        self.day = 1
        self.credits = 12000
        self.reputation = 50
        self.research = 0
        self.happiness = 75

        self.sectors = [
            ColonySector(
                "Aurora",
                300,
                350,
                100,
                100,
            ),
            ColonySector(
                "Helios",
                250,
                300,
                120,
                90,
            ),
        ]

    def build_sector(self, name):
        if self.credits < 2000:
            return False

        self.credits -= 2000

        self.sectors.append(
            ColonySector(
                name,
                100,
                180,
                70,
                70,
            )
        )

        self.reputation += 8
        return True

    def research_project(self, cost=100):
        if self.credits < cost:
            return False

        self.credits -= cost
        self.research += 25
        return True

    def develop(self, sector_name):
        sector = next(
            (
                s for s in self.sectors
                if s.name.lower()
                == sector_name.lower()
            ),
            None,
        )

        if sector is None or self.credits < 500:
            return False

        self.credits -= 500
        sector.housing += 40
        sector.energy += 20
        sector.food += 20
        self.happiness = min(
            100,
            self.happiness + 3,
        )
        return True

    def simulate_day(self):
        total_population = sum(
            s.population
            for s in self.sectors
        )

        total_housing = sum(
            s.housing
            for s in self.sectors
        )

        total_food = sum(
            s.food
            for s in self.sectors
        )

        if total_housing < total_population:
            self.happiness = max(
                0,
                self.happiness - 5,
            )

        if total_food < total_population:
            self.happiness = max(
                0,
                self.happiness - 8,
            )

        self.credits += max(
            50,
            total_population // 4,
        )

        for sector in self.sectors:
            sector.food = max(
                0,
                sector.food - sector.population // 20,
            )

        self.day += 1

    def colony_level(self):
        value = (
            len(self.sectors) * 20
            + self.research
            + self.reputation
            + self.happiness
        )

        if value >= 500:
            return "advanced"
        if value >= 300:
            return "developing"
        return "frontier"

    def status(self):
        return {
            "governor": self.governor,
            "day": self.day,
            "credits": self.credits,
            "reputation": self.reputation,
            "research": self.research,
            "happiness": self.happiness,
            "sectors": len(self.sectors),
            "colony_level": self.colony_level(),
        }


def create_game():
    return SpaceColonyGovernor()


if __name__ == "__main__":
    game = create_game()
    game.build_sector("Nova")
    game.develop("Nova")
    game.research_project()
    game.simulate_day()
    print(game.status())
