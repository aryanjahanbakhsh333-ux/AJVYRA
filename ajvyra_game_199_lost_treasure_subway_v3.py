from dataclasses import dataclass
from typing import Dict


@dataclass
class TreasureHunter:
    name: str
    stamina: int = 100
    flashlight: int = 100
    keys: int = 0
    artifacts: int = 0


class LostTreasureSubway:
    def __init__(self):
        self.hunter = TreasureHunter("Milo Venn")
        self.station = "Platform Zero"
        self.score = 0
        self.depth = 0

        self.stations: Dict[str, int] = {
            "Platform Zero": 0,
            "Abandoned Line": 20,
            "Flooded Station": 40,
            "Royal Tunnel": 60,
            "Hidden Vault": 80,
        }

    def travel(self, station: str):
        if station not in self.stations:
            return False

        distance = self.stations[station]
        stamina_cost = max(5, distance // 4)

        if self.hunter.stamina < stamina_cost:
            return False

        self.hunter.stamina -= stamina_cost
        self.hunter.flashlight -= 8
        self.station = station
        self.depth = distance
        self.score += distance
        return True

    def search(self):
        if self.hunter.flashlight < 10:
            return False

        self.hunter.flashlight -= 10
        self.score += 25

        if self.station in ("Flooded Station", "Royal Tunnel"):
            self.hunter.keys += 1
            self.score += 60
            return True

        return False

    def unlock_vault(self):
        if self.station != "Hidden Vault":
            return False

        if self.hunter.keys < 2:
            return False

        self.hunter.keys -= 2
        self.hunter.artifacts += 3
        self.score += 300
        return True

    def recharge_flashlight(self):
        self.hunter.flashlight = min(
            100,
            self.hunter.flashlight + 35
        )

    def return_to_surface(self):
        self.station = "Platform Zero"
        self.depth = 0
        self.hunter.stamina = min(100, self.hunter.stamina + 25)

    def status(self):
        return {
            "hunter": self.hunter.name,
            "station": self.station,
            "depth": self.depth,
            "stamina": self.hunter.stamina,
            "flashlight": self.hunter.flashlight,
            "keys": self.hunter.keys,
            "artifacts": self.hunter.artifacts,
            "score": self.score,
        }


def create_game():
    return LostTreasureSubway()


def demo():
    game = create_game()
    game.travel("Flooded Station")
    game.search()
    game.travel("Royal Tunnel")
    game.search()
    game.travel("Hidden Vault")
    game.unlock_vault()
    game.return_to_surface()
    return game.status()


if __name__ == "__main__":
    print(demo())
