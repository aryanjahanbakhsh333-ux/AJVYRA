from dataclasses import dataclass
from typing import Dict


@dataclass
class Airship:
    captain: str
    hull: int = 100
    fuel: int = 100
    cargo_capacity: int = 15
    cargo: int = 0
    reputation: int = 10


class DesertAirshipPirates:
    def __init__(self):
        self.ship = Airship("Rook Vey")
        self.location = "Dust Harbor"
        self.gold = 200
        self.score = 0

        self.routes: Dict[str, int] = {
            "Dust Harbor": 0,
            "Red Canyon": 20,
            "Storm Market": 40,
            "Golden Ruins": 65,
        }

    def fly_to(self, destination: str):
        if destination not in self.routes:
            return False

        cost = max(
            5,
            self.routes[destination] // 4
        )

        if self.ship.fuel < cost:
            return False

        self.ship.fuel -= cost
        self.location = destination
        self.score += cost * 2
        return True

    def salvage(self):
        if self.ship.cargo >= self.ship.cargo_capacity:
            return False

        amount = min(
            5,
            self.ship.cargo_capacity - self.ship.cargo
        )

        self.ship.cargo += amount
        self.score += amount * 20
        return amount

    def sell_cargo(self):
        if self.ship.cargo <= 0:
            return False

        value = self.ship.cargo * 30
        self.gold += value
        self.ship.reputation += self.ship.cargo
        self.score += value
        self.ship.cargo = 0
        return value

    def repair(self):
        if self.gold < 50:
            return False

        self.gold -= 50
        self.ship.hull = min(
            100,
            self.ship.hull + 25
        )
        return True

    def refuel(self):
        if self.gold < 30:
            return False

        self.gold -= 30
        self.ship.fuel = min(
            100,
            self.ship.fuel + 35
        )
        return True

    def status(self):
        return {
            "captain": self.ship.captain,
            "location": self.location,
            "hull": self.ship.hull,
            "fuel": self.ship.fuel,
            "cargo": self.ship.cargo,
            "gold": self.gold,
            "reputation": self.ship.reputation,
            "score": self.score,
        }


def create_game():
    return DesertAirshipPirates()


def demo():
    game = create_game()
    game.fly_to("Red Canyon")
    game.salvage()
    game.salvage()
    game.fly_to("Golden Ruins")
    game.salvage()
    game.sell_cargo()
    game.repair()
    return game.status()


if __name__ == "__main__":
    print(demo())
