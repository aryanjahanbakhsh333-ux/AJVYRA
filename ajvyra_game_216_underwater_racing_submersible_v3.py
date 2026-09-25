from dataclasses import dataclass


@dataclass
class Submersible:
    pilot: str
    speed: int = 65
    handling: int = 70
    battery: int = 100
    hull: int = 100
    distance: int = 0


class UnderwaterRacingSubmersible:
    def __init__(self):
        self.sub = Submersible("Kai Renn")
        self.course = "Abyss Circuit"
        self.score = 0
        self.lap = 1
        self.finished = False

    def accelerate(self):
        if self.sub.battery < 8:
            return False

        self.sub.battery -= 8
        self.sub.distance += self.sub.speed
        self.sub.hull -= 2
        self.score += 12
        return True

    def turbo(self):
        if self.sub.battery < 20:
            return False

        self.sub.battery -= 20
        self.sub.distance += self.sub.speed * 2
        self.sub.hull -= 6
        self.score += 35
        return True

    def sharp_turn(self):
        if self.sub.handling < 45:
            self.sub.hull -= 10
            return False

        self.sub.battery -= 5
        self.sub.handling -= 3
        self.sub.distance += 45
        self.score += 20
        return True

    def repair(self):
        self.sub.hull = min(
            100,
            self.sub.hull + 15
        )
        self.sub.battery = max(
            0,
            self.sub.battery - 5
        )

    def finish_race(self):
        if self.sub.distance >= 1200:
            self.finished = True
            self.score += 300
            return True

        return False

    def status(self):
        return {
            "pilot": self.sub.pilot,
            "course": self.course,
            "distance": self.sub.distance,
            "battery": self.sub.battery,
            "hull": self.sub.hull,
            "handling": self.sub.handling,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return UnderwaterRacingSubmersible()


def demo():
    game = create_game()

    for _ in range(7):
        game.accelerate()

    game.turbo()
    game.sharp_turn()
    game.repair()
    game.finish_race()

    return game.status()


if __name__ == "__main__":
    print(demo())
