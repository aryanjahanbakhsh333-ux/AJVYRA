"""
AJVYRA 166 — Space Miner
Genre: Space / Mining / Exploration
"""

from dataclasses import dataclass


@dataclass
class Asteroid:
    name: str
    minerals: int
    hardness: int
    danger: int


class SpaceMiner:
    title = "Space Miner"
    miner_name = "Kiro Dane"

    def __init__(self):
        self.energy = 100
        self.credits = 800
        self.cargo = 0
        self.capacity = 100
        self.score = 0

        self.asteroids = [
            Asteroid("Quartz-7", 40, 20, 10),
            Asteroid("Titan-4", 70, 50, 20),
            Asteroid("Obsidian-X", 100, 75, 35),
            Asteroid("Core-Prime", 150, 90, 50),
        ]

    def mine(self, index):
        if not 0 <= index < len(self.asteroids):
            return False

        asteroid = self.asteroids[index]

        if self.energy < asteroid.hardness // 2:
            return False

        if self.cargo + asteroid.minerals > self.capacity:
            return False

        self.energy -= asteroid.hardness // 2
        self.cargo += asteroid.minerals
        self.score += (
            asteroid.minerals * 5
            - asteroid.danger
        )

        return True

    def sell_cargo(self):
        if self.cargo <= 0:
            return 0

        value = self.cargo * 8
        self.credits += value
        self.score += value
        self.cargo = 0
        return value

    def recharge(self):
        self.energy = min(
            100,
            self.energy + 40,
        )

    def upgrade_capacity(self):
        if self.credits < 500:
            return False

        self.credits -= 500
        self.capacity += 50
        return True

    def status(self):
        return {
            "miner": self.miner_name,
            "energy": self.energy,
            "credits": self.credits,
            "cargo": self.cargo,
            "capacity": self.capacity,
            "score": self.score,
        }


def create_game():
    return SpaceMiner()


if __name__ == "__main__":
    game = create_game()
    game.mine(0)
    game.mine(1)
    game.sell_cargo()
    print(game.status())
