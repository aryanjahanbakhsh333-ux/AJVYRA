import random


class TreasureDiverGame:
    GAME_ID = "AJVYRA-096"
    TITLE = "Pearl of the Abyss"
    GENRE = "Underwater Treasure Hunt"

    def __init__(self):
        self.diver = "Lena Kai"
        self.depth = 0
        self.air = 100
        self.treasure = 0
        self.score = 0

    def descend(self):
        if self.air < 10:
            return False

        self.depth += 20
        self.air -= 10

        return self.depth

    def search(self):
        if self.depth <= 0 or self.air < 15:
            return 0

        self.air -= 15

        chance = random.randint(1, 100)

        if chance <= 55:
            value = random.randint(20, 150)
            self.treasure += value
            self.score += value

            return value

        return 0

    def ascend(self):
        self.depth = max(0, self.depth - 40)
        self.air = min(100, self.air + 20)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "diver": self.diver,
            "depth": self.depth,
            "air": self.air,
            "treasure": self.treasure,
            "score": self.score,
        }
