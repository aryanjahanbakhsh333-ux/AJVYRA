from dataclasses import dataclass


@dataclass
class Airship:
    name: str
    hull: int = 100
    fuel: int = 100
    speed: int = 60
    crew: int = 5
    cargo: int = 0


class FantasyAirshipPirate:
    def __init__(self):
        self.captain = "Riven Storm"
        self.ship = Airship("Black Comet")
        self.gold = 200
        self.reputation = 15
        self.score = 0
        self.location = "Skyport"

    def fly(self, distance: int):
        fuel_cost = max(5, distance // 10)

        if self.ship.fuel < fuel_cost:
            return False

        self.ship.fuel -= fuel_cost
        self.location = f"Sky Sector {distance}"
        self.score += distance
        return True

    def explore_cloud_ruins(self):
        if self.ship.fuel < 15:
            return False

        self.ship.fuel -= 15
        self.ship.cargo += 2
        self.score += 70
        return True

    def repair_ship(self):
        if self.gold < 50:
            return False

        self.gold -= 50
        self.ship.hull = min(100, self.ship.hull + 25)
        self.score += 20
        return True

    def recruit_crew(self):
        if self.gold < 80:
            return False

        self.gold -= 80
        self.ship.crew += 1
        self.ship.speed += 2
        self.reputation += 5
        return True

    def sell_cargo(self):
        if self.ship.cargo <= 0:
            return False

        value = self.ship.cargo * 80
        self.gold += value
        self.score += value // 2
        self.ship.cargo = 0
        return True

    def status(self):
        return {
            "captain": self.captain,
            "ship": self.ship.name,
            "location": self.location,
            "hull": self.ship.hull,
            "fuel": self.ship.fuel,
            "crew": self.ship.crew,
            "cargo": self.ship.cargo,
            "gold": self.gold,
            "reputation": self.reputation,
            "score": self.score,
        }


def create_game():
    return FantasyAirshipPirate()


if __name__ == "__main__":
    game = create_game()
    game.fly(100)
    game.explore_cloud_ruins()
    game.sell_cargo()
    print(game.status())
