"""
AJVYRA 169 — Cyber City Runner
Genre: Action / Runner / Cyberpunk
"""

from dataclasses import dataclass


@dataclass
class Runner:
    name: str
    speed: int
    reflex: int
    stamina: int = 100


class CyberCityRunner:
    title = "Cyber City Runner"
    runner_name = "Nyx Zero"

    def __init__(self):
        self.runner = Runner(
            self.runner_name,
            speed=85,
            reflex=88,
        )

        self.distance = 0
        self.data = 0
        self.credits = 300
        self.combo = 0
        self.score = 0

    def run(self):
        if self.runner.stamina < 10:
            return False

        self.runner.stamina -= 10

        progress = (
            self.runner.speed // 8
            + self.runner.reflex // 15
        )

        self.distance += progress
        self.score += progress * 10
        self.combo += 1
        return True

    def dodge(self, difficulty):
        skill = (
            self.runner.reflex
            + self.runner.speed
        ) // 2

        if skill >= difficulty:
            self.combo += 2
            self.score += 150 * self.combo
            return True

        self.combo = 0
        self.runner.stamina = max(
            0,
            self.runner.stamina - 20,
        )
        return False

    def collect_data(self, amount):
        if amount <= 0:
            return False

        self.data += amount
        self.credits += amount * 4
        self.score += amount * 20
        return True

    def boost(self):
        if self.credits < 100:
            return False

        self.credits -= 100
        self.runner.speed += 5
        self.runner.reflex += 3
        return True

    def rest(self):
        self.runner.stamina = min(
            100,
            self.runner.stamina + 30,
        )

    def status(self):
        return {
            "runner": self.runner.name,
            "distance": self.distance,
            "data": self.data,
            "credits": self.credits,
            "stamina": self.runner.stamina,
            "combo": self.combo,
            "score": self.score,
        }


def create_game():
    return CyberCityRunner()


if __name__ == "__main__":
    game = create_game()
    game.run()
    game.dodge(70)
    game.collect_data(10)
    print(game.status())
