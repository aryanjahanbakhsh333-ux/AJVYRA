"""
AJVYRA 177 — Pirate Island Adventure
Genre: Adventure / Exploration / Naval
"""

from dataclasses import dataclass


@dataclass
class PirateShip:
    name: str
    hull: int
    speed: int
    cargo: int
    capacity: int


class PirateIslandAdventure:
    title = "Pirate Island Adventure"
    captain = "Riven Crow"

    def __init__(self):
        self.ship = PirateShip(
            "Black Comet",
            100,
            78,
            0,
            50,
        )

        self.gold = 700
        self.reputation = 10
        self.score = 0
        self.location = "Port Azure"

        self.islands = {
            "Port Azure": 20,
            "Skull Bay": 60,
            "Emerald Isle": 90,
            "Moon Reef": 120,
        }

    def sail(self, destination):
        if destination not in self.islands:
            return False

        if destination == self.location:
            return False

        distance = self.islands[destination]

        damage = max(
            2,
            distance // 20,
        )

        self.ship.hull = max(
            0,
            self.ship.hull - damage,
        )

        self.location = destination
        self.score += distance
        return True

    def explore(self):
        reward = 100 + self.islands[
            self.location
        ]

        self.gold += reward
        self.score += reward
        self.reputation += 3
        return reward

    def repair(self):
        if self.gold < 200:
            return False

        self.gold -= 200
        self.ship.hull = min(
            100,
            self.ship.hull + 30,
        )
        return True

    def load_treasure(self, amount):
        if amount <= 0:
            return False

        if (
            self.ship.cargo + amount
            > self.ship.capacity
        ):
            return False

        self.ship.cargo += amount
        self.score += amount * 10
        return True

    def sell_treasure(self):
        value = self.ship.cargo * 25
        self.gold += value
        self.score += value
        self.ship.cargo = 0
        return value

    def status(self):
        return {
            "captain": self.captain,
            "ship": self.ship.name,
            "location": self.location,
            "hull": self.ship.hull,
            "cargo": self.ship.cargo,
            "gold": self.gold,
            "reputation": self.reputation,
            "score": self.score,
        }


def create_game():
    return PirateIslandAdventure()


if __name__ == "__main__":
    game = create_game()
    game.sail("Skull Bay")
    game.explore()
    game.load_treasure(10)
    print(game.status())
