from dataclasses import dataclass
from typing import Dict


@dataclass
class Caravan:
    owner: str
    gold: int = 250
    reputation: int = 10
    cargo_capacity: int = 20
    cargo: Dict[str, int] = None
    fuel: int = 100


class FantasyCaravanTrader:
    def __init__(self):
        self.caravan = Caravan(
            "Mira Dawn",
            cargo={}
        )

        self.location = "Silvergate"
        self.distance = {
            "Silvergate": 0,
            "Ember Village": 20,
            "Moon Harbor": 40,
            "Crystal City": 65,
        }

        self.market = {
            "Ember Village": {
                "spice": 8,
                "crystal": 20,
                "cloth": 5,
            },
            "Moon Harbor": {
                "spice": 14,
                "crystal": 12,
                "cloth": 9,
            },
            "Crystal City": {
                "spice": 20,
                "crystal": 30,
                "cloth": 14,
            },
        }

        self.score = 0

    def travel(self, destination: str):
        if destination not in self.distance:
            return False

        fuel_cost = max(
            5,
            self.distance[destination] // 5
        )

        if self.caravan.fuel < fuel_cost:
            return False

        self.caravan.fuel -= fuel_cost
        self.location = destination
        self.score += 10
        return True

    def buy(self, item: str, amount: int):
        if self.location not in self.market:
            return False

        price = self.market[self.location].get(item)

        if price is None:
            return False

        used = sum(self.caravan.cargo.values())

        if used + amount > self.caravan.cargo_capacity:
            return False

        cost = price * amount

        if self.caravan.gold < cost:
            return False

        self.caravan.gold -= cost
        self.caravan.cargo[item] = \
            self.caravan.cargo.get(item, 0) + amount

        self.score += amount * 5
        return True

    def sell(self, item: str, amount: int):
        if self.caravan.cargo.get(item, 0) < amount:
            return False

        price = self.market.get(
            self.location,
            {}
        ).get(item)

        if price is None:
            return False

        self.caravan.cargo[item] -= amount
        self.caravan.gold += price * amount
        self.caravan.reputation += amount
        self.score += price * amount

        return True

    def upgrade(self):
        cost = 100

        if self.caravan.gold < cost:
            return False

        self.caravan.gold -= cost
        self.caravan.cargo_capacity += 10
        self.score += 75
        return True

    def status(self):
        return {
            "owner": self.caravan.owner,
            "location": self.location,
            "gold": self.caravan.gold,
            "reputation": self.caravan.reputation,
            "capacity": self.caravan.cargo_capacity,
            "cargo": dict(self.caravan.cargo),
            "fuel": self.caravan.fuel,
            "score": self.score,
        }


def create_game():
    return FantasyCaravanTrader()


def demo():
    game = create_game()
    game.travel("Ember Village")
    game.buy("spice", 5)
    game.buy("cloth", 4)
    game.travel("Crystal City")
    game.sell("spice", 5)
    game.upgrade()

    return game.status()


if __name__ == "__main__":
    print(demo())
