from dataclasses import dataclass


@dataclass
class Hoverboard:
    name: str
    speed: int = 75
    handling: int = 65
    battery: int = 100
    boost: int = 60


class NeonHoverboardRace:
    def __init__(self):
        self.rider = "Zane Pulse"
        self.board = Hoverboard("Neon Phantom")
        self.distance = 0
        self.goal = 2500
        self.score = 0
        self.combo = 0
        self.finished = False

    def accelerate(self):
        if self.board.battery < 8:
            return False

        self.board.battery -= 8
        self.distance += self.board.speed
        self.score += 25
        return True

    def drift(self):
        if self.board.battery < 12:
            return False

        self.board.battery -= 12

        if self.board.handling >= 60:
            self.combo += 1
            self.score += 45 * self.combo
            return True

        self.combo = 0
        return False

    def boost(self):
        if self.board.battery < 25 or self.board.boost <= 0:
            return False

        self.board.battery -= 25
        self.board.boost -= 20
        self.distance += 250
        self.score += 100
        return True

    def recharge(self):
        self.board.battery = min(
            100,
            self.board.battery + 30
        )

    def upgrade(self):
        self.board.speed += 5
        self.board.handling += 3
        self.board.boost = min(
            100,
            self.board.boost + 10
        )
        self.score += 80

    def finish_race(self):
        if self.distance < self.goal:
            return False

        self.finished = True
        self.score += 500
        return True

    def status(self):
        return {
            "rider": self.rider,
            "board": self.board.name,
            "distance": self.distance,
            "goal": self.goal,
            "speed": self.board.speed,
            "handling": self.board.handling,
            "battery": self.board.battery,
            "boost": self.board.boost,
            "combo": self.combo,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return NeonHoverboardRace()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.drift()
    game.boost()
    print(game.status())
