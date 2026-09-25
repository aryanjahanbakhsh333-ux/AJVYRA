from dataclasses import dataclass


@dataclass
class Runner:
    name: str
    speed: int = 60
    agility: int = 65
    stamina: int = 100
    heat_resistance: int = 40


class VolcanicMagmaRunner:
    def __init__(self):
        self.runner = Runner("Kael Ryn")
        self.distance = 0
        self.goal = 1000
        self.heat = 0
        self.score = 0
        self.gems = 0
        self.finished = False

    def sprint(self):
        if self.runner.stamina < 15:
            return False

        self.runner.stamina -= 15
        self.distance += self.runner.speed
        self.heat += 12
        self.score += 15
        return True

    def lava_jump(self):
        if self.runner.stamina < 20:
            return False

        self.runner.stamina -= 20

        if self.runner.agility >= 55:
            self.distance += 90
            self.score += 35
            return True

        self.heat += 20
        return False

    def collect_gem(self):
        if self.distance < 100:
            return False

        self.gems += 1
        self.score += 50
        self.heat += 8
        return True

    def cool_down(self):
        self.heat = max(0, self.heat - 30)
        self.runner.stamina = min(100, self.runner.stamina + 20)

    def finish(self):
        if self.distance >= self.goal and self.heat < 100:
            self.finished = True
            self.score += 300
            return True
        return False

    def status(self):
        return {
            "runner": self.runner.name,
            "distance": self.distance,
            "goal": self.goal,
            "stamina": self.runner.stamina,
            "heat": self.heat,
            "gems": self.gems,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return VolcanicMagmaRunner()


if __name__ == "__main__":
    game = create_game()
    game.sprint()
    game.lava_jump()
    game.cool_down()
    print(game.status())
