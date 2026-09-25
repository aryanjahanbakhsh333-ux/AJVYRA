from dataclasses import dataclass


@dataclass
class Runner:
    name: str
    stamina: int = 100
    agility: int = 70
    protection: int = 50


class VolcanoEscapeRunner:
    def __init__(self):
        self.runner = Runner("Kairo Flint")
        self.distance = 0
        self.goal = 1500
        self.heat = 20
        self.score = 0
        self.supplies = 3
        self.finished = False

    def run(self):
        if self.runner.stamina < 10:
            return False

        self.runner.stamina -= 10
        self.distance += 100 + self.runner.agility
        self.heat += 8
        self.score += 20
        return True

    def dodge_rocks(self):
        if self.runner.stamina < 8:
            return False

        self.runner.stamina -= 8

        if self.runner.agility >= 65:
            self.distance += 120
            self.score += 45
            return True

        self.heat += 15
        return False

    def use_protection(self):
        if self.supplies <= 0:
            return False

        self.supplies -= 1
        self.heat = max(0, self.heat - 25)
        self.score += 30
        return True

    def rest(self):
        self.runner.stamina = min(100, self.runner.stamina + 30)
        self.heat = max(0, self.heat - 10)

    def escape(self):
        if self.distance < self.goal:
            return False

        self.finished = True
        self.score += 300
        return True

    def status(self):
        return {
            "runner": self.runner.name,
            "distance": self.distance,
            "goal": self.goal,
            "stamina": self.runner.stamina,
            "heat": self.heat,
            "supplies": self.supplies,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return VolcanoEscapeRunner()


if __name__ == "__main__":
    game = create_game()
    game.run()
    game.dodge_rocks()
    game.use_protection()
    print(game.status())
