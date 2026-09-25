from dataclasses import dataclass


@dataclass
class CabinKeeper:
    name: str
    warmth: int = 75
    food: int = 60
    firewood: int = 50
    morale: int = 70


class WinterCabinSurvival:
    def __init__(self):
        self.survivor = CabinKeeper("Evan Rook")
        self.day = 1
        self.snowstorm = 35
        self.score = 0
        self.cabin_integrity = 85

    def chop_wood(self):
        if self.survivor.warmth < 10:
            return False

        self.survivor.warmth -= 10
        self.survivor.firewood += 20
        self.score += 15
        return True

    def light_fire(self):
        if self.survivor.firewood < 10:
            return False

        self.survivor.firewood -= 10
        self.survivor.warmth = min(
            100,
            self.survivor.warmth + 25
        )
        self.score += 20
        return True

    def cook(self):
        if self.survivor.food < 8:
            return False

        self.survivor.food -= 8
        self.survivor.warmth = min(
            100,
            self.survivor.warmth + 8
        )
        self.survivor.morale = min(
            100,
            self.survivor.morale + 10
        )
        self.score += 25
        return True

    def reinforce_cabin(self):
        if self.survivor.firewood < 15:
            return False

        self.survivor.firewood -= 15
        self.cabin_integrity = min(
            100,
            self.cabin_integrity + 20
        )
        self.score += 30
        return True

    def survive_night(self):
        self.day += 1

        self.survivor.food = max(
            0,
            self.survivor.food - 10
        )
        self.survivor.warmth = max(
            0,
            self.survivor.warmth - self.snowstorm // 5
        )
        self.cabin_integrity = max(
            0,
            self.cabin_integrity - self.snowstorm // 10
        )

        if self.survivor.warmth > 40:
            self.score += 40

        self.snowstorm = max(10, self.snowstorm - 3)

    def completed(self):
        return self.day >= 7 and self.cabin_integrity >= 40

    def status(self):
        return {
            "survivor": self.survivor.name,
            "day": self.day,
            "warmth": self.survivor.warmth,
            "food": self.survivor.food,
            "firewood": self.survivor.firewood,
            "morale": self.survivor.morale,
            "snowstorm": self.snowstorm,
            "cabin_integrity": self.cabin_integrity,
            "score": self.score,
            "completed": self.completed(),
        }


def create_game():
    return WinterCabinSurvival()


def demo():
    game = create_game()

    for _ in range(3):
        game.chop_wood()

    game.light_fire()
    game.cook()
    game.reinforce_cabin()

    for _ in range(6):
        game.survive_night()

    return game.status()


if __name__ == "__main__":
    print(demo())
