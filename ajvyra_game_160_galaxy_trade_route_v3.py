"""
AJVYRA 160 — Galaxy Trade Route
Genre: Space / Trading / Strategy
"""

from dataclasses import dataclass


@dataclass
class Planet:
    name: str
    price: int
    demand: int


class GalaxyTradeRoute:
    title = "Galaxy Trade Route"
    captain = "Orin Flux"

    def __init__(self):
        self.credits = 2500
        self.cargo = {}
        self.capacity = 30
        self.fuel = 100
        self.reputation = 10
        self.score = 0

        self.planets = {
            "Nova": Planet("Nova", 40, 70),
            "Vega": Planet("Vega", 65, 45),
            "Orion": Planet("Orion", 90, 85),
            "Lumen": Planet("Lumen", 55, 95),
        }

        self.location = "Nova"

    def cargo_count(self):
        return sum(self.cargo.values())

    def buy(self, item, amount):
        if amount <= 0:
            return False

        planet = self.planets.get(self.location)

        if planet is None:
            return False

        cost = planet.price * amount

        if (
            self.credits < cost
            or self.cargo_count() + amount > self.capacity
        ):
            return False

        self.credits -= cost
        self.cargo[item] = (
            self.cargo.get(item, 0) + amount
        )

        return True

    def sell(self, item, amount):
        current = self.cargo.get(item, 0)

        if amount <= 0 or current < amount:
            return False

        planet = self.planets[self.location]

        revenue = (
            planet.price
            * amount
            * planet.demand
            // 70
        )

        self.cargo[item] -= amount
        self.credits += revenue
        self.score += revenue
        self.reputation += amount
        return True

    def travel(self, destination):
        if destination not in self.planets:
            return False

        if destination == self.location:
            return False

        fuel_cost = 15

        if self.fuel < fuel_cost:
            return False

        self.fuel -= fuel_cost
        self.location = destination
        self.score += 50
        return True

    def refuel(self):
        if self.credits < 200:
            return False

        self.credits -= 200
        self.fuel = 100
        return True

    def status(self):
        return {
            "captain": self.captain,
            "location": self.location,
            "credits": self.credits,
            "fuel": self.fuel,
            "capacity": self.capacity,
            "cargo": dict(self.cargo),
            "reputation": self.reputation,
            "score": self.score,
        }


def create_game():
    return GalaxyTradeRoute()


if __name__ == "__main__":
    game = create_game()
    game.buy("crystal", 10)
    game.travel("Vega")
    game.sell("crystal", 5)
    print(game.status())
