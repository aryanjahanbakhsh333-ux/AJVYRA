"""
AJVYRA 136 — Cyber City Runner
Genre: Neon Action / Parkour
"""

from dataclasses import dataclass


@dataclass
class Mission:
    name: str
    distance: int
    difficulty: int
    completed: bool = False


class CyberCityRunner:
    title = "Cyber City Runner"
    runner = "Zero Kai"

    def __init__(self):
        self.energy = 100
        self.credits = 250
        self.reputation = 0
        self.combo = 0
        self.score = 0

        self.missions = [
            Mission("Neon Courier", 600, 30),
            Mission("Skybridge Run", 900, 50),
            Mission("Night Grid", 1400, 75),
            Mission("Quantum Chase", 2000, 95),
        ]

    def run(self, index, precision):
        if not 0 <= index < len(self.missions):
            return False

        mission = self.missions[index]

        if mission.completed:
            return False

        energy_cost = mission.distance // 40

        if self.energy < energy_cost:
            return False

        self.energy -= energy_cost

        performance = precision + self.combo * 5

        if performance >= mission.difficulty:
            mission.completed = True
            self.combo += 1
            reward = mission.difficulty * 10
            self.credits += reward
            self.score += reward + mission.distance
            self.reputation += 5
            return True

        self.combo = 0
        return False

    def recharge(self):
        self.energy = min(
            100,
            self.energy + 40,
        )

    def buy_upgrade(self):
        if self.credits < 500:
            return False

        self.credits -= 500
        self.energy = min(
            150,
            self.energy + 25,
        )
        return True

    def status(self):
        return {
            "runner": self.runner,
            "energy": self.energy,
            "credits": self.credits,
            "reputation": self.reputation,
            "combo": self.combo,
            "score": self.score,
            "completed": [
                m.name
                for m in self.missions
                if m.completed
            ],
        }


def create_game():
    return CyberCityRunner()


if __name__ == "__main__":
    game = create_game()

    for i in range(4):
        game.run(i, 100)

    print(game.status())
