from dataclasses import dataclass
from typing import Dict


@dataclass
class Captain:
    name: str
    diplomacy: int = 70
    leadership: int = 75
    fuel: int = 100
    reputation: int = 20


class StarshipCaptainDiplomacy:
    def __init__(self):
        self.captain = Captain("Selene Varr")
        self.location = "Orion Gate"
        self.credits = 300
        self.score = 0
        self.alliances: Dict[str, int] = {
            "Lunaris": 0,
            "Veyra": 0,
            "Kron": 0,
        }

    def travel(self, destination: str):
        routes = {
            "Orion Gate": 0,
            "Lunaris": 20,
            "Veyra": 35,
            "Kron": 50,
        }

        if destination not in routes:
            return False

        fuel_cost = max(5, routes[destination] // 5)

        if self.captain.fuel < fuel_cost:
            return False

        self.captain.fuel -= fuel_cost
        self.location = destination
        self.score += 10
        return True

    def negotiate(self, faction: str, approach: str):
        if faction not in self.alliances:
            return False

        values = {
            "trade": 8,
            "peace": 12,
            "technology": 15,
            "respect": 10,
        }

        gain = values.get(approach)

        if gain is None:
            return False

        bonus = self.captain.diplomacy // 20
        self.alliances[faction] += gain + bonus
        self.captain.reputation += 2
        self.score += gain * 5

        return True

    def inspire_crew(self):
        self.captain.leadership += 3
        self.score += 25
        return True

    def establish_alliance(self, faction: str):
        if self.alliances.get(faction, 0) < 30:
            return False

        self.score += 150
        self.captain.reputation += 10
        return True

    def status(self):
        return {
            "captain": self.captain.name,
            "location": self.location,
            "fuel": self.captain.fuel,
            "credits": self.credits,
            "reputation": self.captain.reputation,
            "leadership": self.captain.leadership,
            "diplomacy": self.captain.diplomacy,
            "alliances": dict(self.alliances),
            "score": self.score,
        }


def create_game():
    return StarshipCaptainDiplomacy()


def demo():
    game = create_game()
    game.travel("Lunaris")
    game.negotiate("Lunaris", "peace")
    game.negotiate("Lunaris", "technology")
    game.negotiate("Lunaris", "trade")
    game.inspire_crew()
    game.establish_alliance("Lunaris")

    return game.status()


if __name__ == "__main__":
    print(demo())
