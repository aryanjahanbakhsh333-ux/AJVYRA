"""
AJVYRA 135 — Railway Empire
Genre: Transportation / Economic Strategy
"""

from dataclasses import dataclass


@dataclass
class Station:
    name: str
    population: int
    demand: dict


class RailwayEmpire:
    title = "Railway Empire"
    founder = "Leon Cross"

    def __init__(self):
        self.money = 10000
        self.reputation = 20
        self.trains = 1
        self.routes = []

        self.stations = {
            "Northvale": Station(
                "Northvale",
                800,
                {"food": 30, "steel": 10},
            ),
            "Riverton": Station(
                "Riverton",
                1200,
                {"food": 15, "steel": 35},
            ),
            "Eastmere": Station(
                "Eastmere",
                1800,
                {"food": 45, "steel": 20},
            ),
            "Stonegate": Station(
                "Stonegate",
                900,
                {"food": 20, "steel": 50},
            ),
        }

    def build_route(self, origin, destination):
        if (
            origin not in self.stations
            or destination not in self.stations
            or origin == destination
        ):
            return False

        route = (origin, destination)

        if route in self.routes or route[::-1] in self.routes:
            return False

        cost = (
            self.stations[origin].population
            + self.stations[destination].population
        ) // 100

        if self.money < cost:
            return False

        self.money -= cost
        self.routes.append(route)
        self.reputation += 5
        return True

    def run_train(self, route_index, cargo_value):
        if not 0 <= route_index < len(self.routes):
            return False

        if cargo_value <= 0:
            return False

        income = cargo_value * (self.reputation / 20)
        self.money += int(income)
        self.reputation += 1
        return True

    def buy_train(self):
        cost = 2500

        if self.money < cost:
            return False

        self.money -= cost
        self.trains += 1
        return True

    def status(self):
        return {
            "founder": self.founder,
            "money": self.money,
            "reputation": self.reputation,
            "trains": self.trains,
            "routes": list(self.routes),
        }


def create_game():
    return RailwayEmpire()


if __name__ == "__main__":
    game = create_game()
    game.build_route("Northvale", "Riverton")
    game.build_route("Riverton", "Eastmere")
    game.run_train(0, 400)
    print(game.status())
