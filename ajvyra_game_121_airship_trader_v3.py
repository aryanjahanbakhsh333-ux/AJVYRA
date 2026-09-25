"""
AJVYRA 121 — Airship Trader
Genre: Trading / Route Strategy
"""

from dataclasses import dataclass


@dataclass
class Port:
    name: str
    prices: dict[str, int]
    danger: int


class AirshipTrader:
    title = "Airship Trader"
    captain = "Veyron Ash"

    def __init__(self):
        self.money = 1000
        self.fuel = 100
        self.cargo_capacity = 40
        self.cargo = {}
        self.location = "Cloudport"
        self.reputation = 10
        self.score = 0

        self.ports = {
            "Cloudport": Port(
                "Cloudport",
                {"silk": 12, "crystal": 25, "spice": 18},
                10,
            ),
            "Ironhaven": Port(
                "Ironhaven",
                {"silk": 20, "crystal": 14, "spice": 25},
                25,
            ),
            "Sunreach": Port(
                "Sunreach",
                {"silk": 28, "crystal": 30, "spice": 10},
                35,
            ),
            "Frostgate": Port(
                "Frostgate",
                {"silk": 15, "crystal": 40, "spice": 22},
                20,
            ),
        }

        self.routes = {
            ("Cloudport", "Ironhaven"): 18,
            ("Cloudport", "Sunreach"): 30,
            ("Cloudport", "Frostgate"): 24,
            ("Ironhaven", "Sunreach"): 22,
            ("Ironhaven", "Frostgate"): 16,
            ("Sunreach", "Frostgate"): 28,
        }

    def cargo_count(self):
        return sum(self.cargo.values())

    def buy(self, item, amount):
        if item not in self.ports[self.location].prices:
            return False

        if amount <= 0:
            return False

        if self.cargo_count() + amount > self.cargo_capacity:
            return False

        cost = self.ports[self.location].prices[item] * amount

        if cost > self.money:
            return False

        self.money -= cost
        self.cargo[item] = self.cargo.get(item, 0) + amount
        return True

    def sell(self, item, amount):
        if self.cargo.get(item, 0) < amount:
            return False

        price = self.ports[self.location].prices[item]
        self.cargo[item] -= amount
        self.money += price * amount
        self.score += amount * 5
        return True

    def travel(self, destination):
        if destination not in self.ports:
            return False

        if destination == self.location:
            return False

        key = tuple(sorted((self.location, destination)))

        if key not in {
            tuple(sorted(route))
            for route in self.routes
        }:
            return False

        distance = self.routes.get(
            (self.location, destination),
            self.routes.get((destination, self.location), 0),
        )

        if self.fuel < distance:
            return False

        danger = self.ports[destination].danger
        self.fuel -= distance

        self.location = destination

        if danger > 30:
            self.reputation = max(0, self.reputation - 1)

        return True

    def refuel(self):
        self.fuel = 100

    def status(self):
        return {
            "captain": self.captain,
            "location": self.location,
            "money": self.money,
            "fuel": self.fuel,
            "cargo": dict(self.cargo),
            "reputation": self.reputation,
            "score": self.score,
        }


def create_game():
    return AirshipTrader()


if __name__ == "__main__":
    game = create_game()
    game.buy("silk", 10)
    game.travel("Ironhaven")
    game.sell("silk", 10)
    print(game.status())
