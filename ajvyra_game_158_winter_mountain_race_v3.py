"""
AJVYRA 158 — Winter Mountain Race
Genre: Extreme Sports / Racing
"""

from dataclasses import dataclass


@dataclass
class SnowRacer:
    name: str
    speed: int
    balance: int
    control: int
    stamina: int = 100


class WinterMountainRace:
    title = "Winter Mountain Race"
    racer_name = "Zane Frost"

    def __init__(self):
        self.racer = SnowRacer(
            self.racer_name,
            82,
            79,
            85,
        )

        self.distance = 100
        self.score = 0
        self.coins = 700
        self.finished = False

    def accelerate(self):
        if self.racer.stamina < 10:
            return False

        self.racer.stamina -= 10

        progress = (
            self.racer.speed // 6
            + self.racer.control // 12
        )

        self.distance = max(
            0,
            self.distance - progress,
        )

        self.score += progress * 8

        if self.distance == 0:
            self.finished = True

        return True

    def jump(self):
        if self.racer.stamina < 15:
            return False

        self.racer.stamina -= 15

        success = (
            self.racer.balance
            + self.racer.control
            >= 160
        )

        if success:
            self.score += 180
            self.distance = max(
                0,
                self.distance - 8,
            )
            return True

        self.racer.stamina = max(
            0,
            self.racer.stamina - 15,
        )
        return False

    def rest(self):
        self.racer.stamina = min(
            100,
            self.racer.stamina + 25,
        )

    def status(self):
        return {
            "racer": self.racer.name,
            "distance": self.distance,
            "stamina": self.racer.stamina,
            "score": self.score,
            "coins": self.coins,
            "finished": self.finished,
        }


def create_game():
    return WinterMountainRace()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.jump()
    game.rest()
    print(game.status())
