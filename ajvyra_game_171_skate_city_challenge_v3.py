"""
AJVYRA 171 — Skate City Challenge
Genre: Sports / Arcade / Stunts
"""

from dataclasses import dataclass


@dataclass
class Skater:
    name: str
    speed: int
    balance: int
    trick: int
    stamina: int = 100


class SkateCityChallenge:
    title = "Skate City Challenge"
    skater_name = "Kai Drift"

    def __init__(self):
        self.skater = Skater(
            self.skater_name,
            82,
            86,
            79,
        )
        self.score = 0
        self.coins = 500
        self.combo = 0
        self.distance = 0

    def push(self):
        if self.skater.stamina < 8:
            return False

        self.skater.stamina -= 8
        progress = self.skater.speed // 7
        self.distance += progress
        self.score += progress * 10
        self.combo += 1
        return True

    def trick(self, difficulty):
        if self.skater.stamina < 12:
            return False

        skill = (
            self.skater.balance
            + self.skater.trick
        ) // 2

        self.skater.stamina -= 12

        if skill >= difficulty:
            self.combo += 1
            reward = 100 * self.combo
            self.score += reward
            return True

        self.combo = 0
        return False

    def grind(self):
        if self.skater.balance < 60:
            return False

        self.skater.stamina -= 10
        self.score += 130 + self.combo * 20
        self.combo += 1
        return True

    def finish_run(self):
        reward = self.score // 10
        self.coins += reward
        self.combo = 0
        return reward

    def rest(self):
        self.skater.stamina = min(
            100,
            self.skater.stamina + 30,
        )

    def status(self):
        return {
            "skater": self.skater.name,
            "distance": self.distance,
            "score": self.score,
            "coins": self.coins,
            "stamina": self.skater.stamina,
            "combo": self.combo,
        }


def create_game():
    return SkateCityChallenge()


if __name__ == "__main__":
    game = create_game()
    game.push()
    game.trick(70)
    game.grind()
    print(game.status())
