from dataclasses import dataclass


@dataclass
class Runner:
    name: str
    speed: int = 70
    balance: int = 75
    energy: int = 100
    style: int = 0
    distance: int = 0


class NeonSkateParkour:
    def __init__(self):
        self.runner = Runner("Vex Arlo")
        self.city_zone = "Neon District"
        self.score = 0
        self.combo = 0
        self.finished = False

    def sprint(self):
        if self.runner.energy < 8:
            return False

        self.runner.energy -= 8
        self.runner.distance += self.runner.speed
        self.combo += 1
        self.score += 10 * self.combo
        return True

    def wall_jump(self):
        if self.runner.energy < 12:
            return False

        success = self.runner.balance >= 60

        self.runner.energy -= 12

        if success:
            self.runner.distance += 65
            self.runner.style += 15
            self.combo += 1
            self.score += 25 * self.combo
        else:
            self.combo = 0
            self.runner.balance -= 10

        return success

    def rail_grind(self):
        if self.runner.energy < 15:
            return False

        self.runner.energy -= 15
        self.runner.balance -= 4
        self.runner.distance += 80
        self.runner.style += 20
        self.combo += 2
        self.score += 30 * self.combo
        return True

    def recover(self):
        self.runner.energy = min(
            100,
            self.runner.energy + 25
        )
        self.combo = 0

    def finish_run(self):
        if self.runner.distance >= 1000:
            self.finished = True
            self.score += self.runner.style * 2 + 250
            return True

        return False

    def status(self):
        return {
            "runner": self.runner.name,
            "zone": self.city_zone,
            "distance": self.runner.distance,
            "energy": self.runner.energy,
            "balance": self.runner.balance,
            "style": self.runner.style,
            "combo": self.combo,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return NeonSkateParkour()


def demo():
    game = create_game()

    for _ in range(5):
        game.sprint()

    game.wall_jump()
    game.rail_grind()
    game.recover()
    game.finish_run()

    return game.status()


if __name__ == "__main__":
    print(demo())
