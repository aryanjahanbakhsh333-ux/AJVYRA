"""
AJVYRA 151 — Desert Rally
Genre: Racing / Navigation
"""

from dataclasses import dataclass


@dataclass
class RallyCar:
    name: str
    speed: int
    grip: int
    durability: int
    fuel: int = 100


class DesertRally:
    title = "Desert Rally"
    driver = "Kian Rook"

    def __init__(self):
        self.car = RallyCar(
            "Dune-X",
            speed=82,
            grip=70,
            durability=88,
        )
        self.stage = 1
        self.money = 1200
        self.time = 0
        self.score = 0

    def accelerate(self):
        if self.car.fuel < 8:
            return False

        self.car.fuel -= 8
        self.time += max(
            1,
            12 - self.car.speed // 10,
        )
        self.score += self.car.speed
        return True

    def drift(self):
        if self.car.fuel < 6:
            return False

        self.car.fuel -= 6

        control = self.car.grip + self.car.speed // 4

        if control >= 85:
            self.score += 150
            self.time = max(0, self.time - 3)
            return True

        self.car.durability = max(
            0,
            self.car.durability - 8,
        )
        self.time += 8
        return False

    def repair(self):
        if self.money < 150:
            return False

        self.money -= 150
        self.car.durability = min(
            100,
            self.car.durability + 25,
        )
        return True

    def refuel(self):
        if self.money < 100:
            return False

        self.money -= 100
        self.car.fuel = 100
        return True

    def finish_stage(self):
        if self.car.durability <= 0:
            return False

        reward = max(
            100,
            800 - self.time * 5,
        )

        self.money += reward
        self.score += reward
        self.stage += 1

        self.car.fuel = max(
            0,
            self.car.fuel - 15,
        )
        return True

    def status(self):
        return {
            "driver": self.driver,
            "stage": self.stage,
            "money": self.money,
            "time": self.time,
            "score": self.score,
            "fuel": self.car.fuel,
            "durability": self.car.durability,
        }


def create_game():
    return DesertRally()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.drift()
    game.finish_stage()
    print(game.status())
