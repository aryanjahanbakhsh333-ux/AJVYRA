"""
AJVYRA Game 103 - Wildfire Commander
Genre: Environmental Strategy
"""

from dataclasses import dataclass


@dataclass
class FireSector:
    name: str
    heat: int
    trees: int
    protected: bool = False


class WildfireCommander:
    title = "Wildfire Commander"
    character = "Mira Solen"

    def __init__(self):
        self.water = 180
        self.vehicles = 4
        self.day = 1
        self.score = 0
        self.sectors = [
            FireSector("North Ridge", 80, 100),
            FireSector("Pine Valley", 65, 120),
            FireSector("Silver Creek", 50, 90),
            FireSector("East Forest", 75, 110),
        ]
        self.log = []

    def deploy_water(self, index, amount=30):
        if not 0 <= index < len(self.sectors):
            return False

        amount = min(amount, self.water)

        if amount <= 0:
            return False

        sector = self.sectors[index]
        self.water -= amount
        sector.heat = max(0, sector.heat - amount)
        self.score += amount // 5
        self.log.append(
            f"Water deployed to {sector.name}: {amount}."
        )
        return True

    def build_firebreak(self, index):
        if self.vehicles <= 0:
            return False

        sector = self.sectors[index]
        self.vehicles -= 1
        sector.protected = True
        sector.heat = max(0, sector.heat - 10)
        self.log.append(f"Firebreak built at {sector.name}.")
        return True

    def advance_day(self):
        self.day += 1

        for sector in self.sectors:
            if sector.heat > 0:
                growth = 4 if sector.protected else 10
                sector.heat = min(100, sector.heat + growth)

                if sector.heat > 70:
                    sector.trees = max(0, sector.trees - 8)

        self.water = min(180, self.water + 35)
        self.check_status()

    def check_status(self):
        if all(s.heat == 0 for s in self.sectors):
            self.score += 100

    def status(self):
        return {
            "day": self.day,
            "water": self.water,
            "vehicles": self.vehicles,
            "score": self.score,
            "sectors": [
                {
                    "name": s.name,
                    "heat": s.heat,
                    "trees": s.trees,
                    "protected": s.protected,
                }
                for s in self.sectors
            ],
        }


def create_game():
    return WildfireCommander()


if __name__ == "__main__":
    game = create_game()
    game.deploy_water(0, 40)
    game.build_firebreak(0)
    game.advance_day()
    print(game.status())
