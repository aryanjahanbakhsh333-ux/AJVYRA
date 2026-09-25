from dataclasses import dataclass


@dataclass
class AsteroidPort:
    name: str
    ore_price: int
    crystal_price: int
    fuel_price: int


class AsteroidColonyTrader:
    def __init__(self):
        self.trader = "Riven Cole"
        self.location = "Nova Rock"
        self.credits = 800
        self.cargo_capacity = 20
        self.ore = 0
        self.crystals = 0
        self.fuel = 100
        self.reputation = 20
        self.score = 0

        self.ports = [
            AsteroidPort("Nova Rock", 20, 80, 30),
            AsteroidPort("Titan Belt", 35, 60, 45),
            AsteroidPort("Eclipse Mine", 55, 120, 40),
            AsteroidPort("Orion Colony", 30, 150, 25),
        ]

    def current_port(self):
        for port in self.ports:
            if port.name == self.location:
                return port
        return self.ports[0]

    def travel(self, destination: str):
        names = [p.name for p in self.ports]

        if destination not in names or destination == self.location:
            return False

        if self.fuel < 15:
            return False

        self.fuel -= 15
        self.location = destination
        self.score += 30
        return True

    def buy_ore(self, amount: int):
        port = self.current_port()
        cost = amount * port.ore_price

        if amount <= 0 or self.ore + self.crystals + amount > self.cargo_capacity:
            return False

        if self.credits < cost:
            return False

        self.credits -= cost
        self.ore += amount
        return True

    def buy_crystals(self, amount: int):
        port = self.current_port()
        cost = amount * port.crystal_price

        if amount <= 0 or self.ore + self.crystals + amount > self.cargo_capacity:
            return False

        if self.credits < cost:
            return False

        self.credits -= cost
        self.crystals += amount
        return True

    def sell_cargo(self):
        port = self.current_port()

        revenue = (
            self.ore * port.ore_price
            + self.crystals * port.crystal_price
        )

        if revenue <= 0:
            return False

        self.credits += revenue
        self.score += revenue // 2
        self.reputation = min(100, self.reputation + 2)

        self.ore = 0
        self.crystals = 0
        return True

    def refuel(self):
        port = self.current_port()

        if self.credits < port.fuel_price:
            return False

        self.credits -= port.fuel_price
        self.fuel = 100
        return True

    def upgrade_ship(self):
        if self.credits < 300:
            return False

        self.credits -= 300
        self.cargo_capacity += 10
        self.score += 120
        return True

    def status(self):
        return {
            "trader": self.trader,
            "location": self.location,
            "credits": self.credits,
            "cargo": self.ore + self.crystals,
            "capacity": self.cargo_capacity,
            "ore": self.ore,
            "crystals": self.crystals,
            "fuel": self.fuel,
            "reputation": self.reputation,
            "score": self.score,
        }


def create_game():
    return AsteroidColonyTrader()


if __name__ == "__main__":
    game = create_game()
    game.buy_ore(5)
    game.travel("Titan Belt")
    game.sell_cargo()
    print(game.status())
