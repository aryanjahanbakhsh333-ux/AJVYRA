from dataclasses import dataclass


@dataclass
class GridSector:
    name: str
    demand: int
    supply: int
    stability: int = 100
    powered: bool = True


class CityElectricGridOperator:
    def __init__(self):
        self.operator = "Juno Hart"
        self.money = 300
        self.energy_reserve = 500
        self.score = 0
        self.hour = 1
        self.blackout_risk = 0

        self.sectors = [
            GridSector("Central District", 120, 150),
            GridSector("Harbor", 90, 110),
            GridSector("Old Town", 70, 80),
            GridSector("Research Zone", 160, 180),
        ]

    def route_power(self, sector_name: str, amount: int):
        sector = next(
            (s for s in self.sectors if s.name == sector_name),
            None
        )

        if sector is None or amount <= 0:
            return False

        if self.energy_reserve < amount:
            return False

        self.energy_reserve -= amount
        sector.supply += amount
        sector.stability = min(100, sector.stability + 5)
        self.score += amount // 2
        return True

    def balance_sector(self, sector_name: str):
        sector = next(
            (s for s in self.sectors if s.name == sector_name),
            None
        )

        if sector is None:
            return False

        difference = sector.supply - sector.demand

        if difference >= 0:
            sector.stability = min(100, sector.stability + 10)
            self.score += 20
        else:
            sector.stability = max(0, sector.stability + difference // 2)
            self.blackout_risk += abs(difference) // 10

        return True

    def repair_grid(self, sector_name: str):
        sector = next(
            (s for s in self.sectors if s.name == sector_name),
            None
        )

        if sector is None or self.money < 50:
            return False

        self.money -= 50
        sector.stability = min(100, sector.stability + 25)
        self.blackout_risk = max(0, self.blackout_risk - 5)
        self.score += 35
        return True

    def advance_hour(self):
        self.hour += 1

        for sector in self.sectors:
            sector.demand += 5

        self.energy_reserve = min(800, self.energy_reserve + 100)
        self.money += 20

        if self.blackout_risk >= 80:
            for sector in self.sectors:
                sector.powered = False

    def stabilize_city(self):
        return (
            all(s.stability >= 70 for s in self.sectors)
            and self.blackout_risk < 50
        )

    def status(self):
        return {
            "operator": self.operator,
            "hour": self.hour,
            "money": self.money,
            "energy_reserve": self.energy_reserve,
            "blackout_risk": self.blackout_risk,
            "score": self.score,
            "stable": self.stabilize_city(),
            "sectors": {
                s.name: {
                    "demand": s.demand,
                    "supply": s.supply,
                    "stability": s.stability,
                    "powered": s.powered,
                }
                for s in self.sectors
            },
        }


def create_game():
    return CityElectricGridOperator()


if __name__ == "__main__":
    game = create_game()
    game.route_power("Central District", 40)
    game.balance_sector("Central District")
    game.repair_grid("Harbor")
    print(game.status())
