from dataclasses import dataclass


@dataclass
class Colony:
    workers: int
    soldiers: int
    food: int
    larvae: int


class AntColonyGame:
    GAME_ID = "AJVYRA-094"
    TITLE = "Empire Beneath"
    GENRE = "Colony Simulation"

    def __init__(self):
        self.queen = "Queen Nyra"
        self.day = 1

        self.colony = Colony(
            workers=20,
            soldiers=5,
            food=100,
            larvae=8,
        )

    def gather(self):
        gathered = self.colony.workers * 3
        self.colony.food += gathered

        return gathered

    def train_soldiers(self, amount: int):
        if amount <= 0 or self.colony.workers < amount:
            return False

        self.colony.workers -= amount
        self.colony.soldiers += amount

        return True

    def hatch(self, amount: int):
        if amount <= 0 or self.colony.larvae < amount:
            return False

        self.colony.larvae -= amount
        self.colony.workers += amount

        return True

    def advance_day(self):
        self.day += 1

        consumption = (
            self.colony.workers + self.colony.soldiers
        )

        self.colony.food -= consumption

        if self.colony.food < 0:
            self.colony.food = 0
            self.colony.workers = max(
                1,
                self.colony.workers - 2
            )

        self.colony.larvae += max(1, self.colony.workers // 10)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "queen": self.queen,
            "day": self.day,
            "colony": self.colony.__dict__.copy(),
        }
