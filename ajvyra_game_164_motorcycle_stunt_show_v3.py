"""
AJVYRA 164 — Motorcycle Stunt Show
Genre: Racing / Stunts
"""

from dataclasses import dataclass


@dataclass
class Rider:
    name: str
    speed: int
    balance: int
    control: int
    reputation: int = 0


class MotorcycleStuntShow:
    title = "Motorcycle Stunt Show"
    rider_name = "Rex Calder"

    def __init__(self):
        self.rider = Rider(
            self.rider_name,
            speed=85,
            balance=78,
            control=82,
        )

        self.money = 600
        self.combo = 0
        self.score = 0

    def wheelie(self):
        if self.rider.balance < 60:
            return False

        self.rider.balance -= 2
        self.combo += 1
        self.score += 100 * self.combo
        return True

    def jump(self):
        difficulty = 75

        skill = (
            self.rider.speed
            + self.rider.control
        ) // 2

        if skill >= difficulty:
            self.combo += 2
            self.score += 250 * self.combo
            return True

        self.combo = 0
        return False

    def drift(self):
        if self.rider.control < 50:
            return False

        self.rider.control -= 3
        self.combo += 1
        self.score += 120 * self.combo
        return True

    def finish_show(self):
        reward = self.score // 5
        self.money += reward
        self.rider.reputation += self.combo * 3
        self.combo = 0
        return reward

    def upgrade(self, attribute):
        if self.money < 250:
            return False

        if attribute not in {
            "speed",
            "balance",
            "control",
        }:
            return False

        self.money -= 250

        setattr(
            self.rider,
            attribute,
            getattr(self.rider, attribute) + 5,
        )

        return True

    def status(self):
        return {
            "rider": self.rider.name,
            "speed": self.rider.speed,
            "balance": self.rider.balance,
            "control": self.rider.control,
            "reputation": self.rider.reputation,
            "money": self.money,
            "combo": self.combo,
            "score": self.score,
        }


def create_game():
    return MotorcycleStuntShow()


if __name__ == "__main__":
    game = create_game()
    game.wheelie()
    game.jump()
    game.drift()
    game.finish_show()
    print(game.status())
