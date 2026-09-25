from dataclasses import dataclass


@dataclass
class Submarine:
    name: str
    speed: int = 60
    oxygen: int = 100
    sonar: int = 50
    armor: int = 40


class UnderwaterTreasureRacer:
    def __init__(self):
        self.pilot = "Niko Reef"
        self.submarine = Submarine("Blue Comet")
        self.depth = 0
        self.distance = 0
        self.treasure = 0
        self.score = 0
        self.money = 100

    def dive(self):
        if self.submarine.oxygen < 15:
            return False

        self.submarine.oxygen -= 15
        self.depth += 200
        self.score += 15
        return True

    def sonar_scan(self):
        if self.submarine.sonar < 10:
            return False

        self.submarine.sonar -= 10
        self.score += 20
        return True

    def boost(self):
        if self.submarine.oxygen < 20:
            return False

        self.submarine.oxygen -= 20
        self.distance += self.submarine.speed * 2
        self.score += 35
        return True

    def recover_treasure(self):
        if self.depth < 400:
            return False

        self.treasure += 1
        self.score += 80
        return True

    def surface(self):
        self.depth = max(0, self.depth - 500)
        self.submarine.oxygen = min(100, self.submarine.oxygen + 35)
        return True

    def sell_treasure(self):
        if self.treasure <= 0:
            return False

        self.money += self.treasure * 120
        self.treasure = 0
        return True

    def status(self):
        return {
            "pilot": self.pilot,
            "submarine": self.submarine.name,
            "depth": self.depth,
            "distance": self.distance,
            "oxygen": self.submarine.oxygen,
            "treasure": self.treasure,
            "money": self.money,
            "score": self.score,
        }


def create_game():
    return UnderwaterTreasureRacer()


if __name__ == "__main__":
    game = create_game()
    game.dive()
    game.sonar_scan()
    game.dive()
    game.recover_treasure()
    game.surface()
    print(game.status())
