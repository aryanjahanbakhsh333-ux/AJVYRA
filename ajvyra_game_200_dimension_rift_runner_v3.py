from dataclasses import dataclass


@dataclass
class RiftRunner:
    name: str
    energy: int = 100
    stability: int = 100
    distance: int = 0
    fragments: int = 0
    combo: int = 0


class DimensionRiftRunner:
    def __init__(self):
        self.runner = RiftRunner("Aven Cross")
        self.dimension = "Neon Rift"
        self.score = 0
        self.level = 1
        self.finished = False

    def dash(self):
        if self.runner.energy < 10:
            return False

        self.runner.energy -= 10
        self.runner.distance += 70
        self.runner.combo += 1
        self.score += 15 * self.runner.combo
        return True

    def phase_shift(self):
        if self.runner.energy < 18:
            return False

        self.runner.energy -= 18
        self.runner.stability -= 6
        self.runner.distance += 120
        self.runner.combo += 2
        self.score += 35 * self.runner.combo
        return True

    def collect_fragment(self):
        if self.runner.energy < 5:
            return False

        self.runner.energy -= 5
        self.runner.fragments += 1
        self.runner.stability -= 2
        self.score += 40
        return True

    def stabilize(self):
        if self.runner.fragments < 2:
            return False

        self.runner.fragments -= 2
        self.runner.stability = min(
            100,
            self.runner.stability + 25
        )
        self.runner.energy = min(
            100,
            self.runner.energy + 20
        )
        self.score += 60
        return True

    def next_dimension(self):
        dimensions = [
            "Neon Rift",
            "Crystal Rift",
            "Shadow Rift",
            "Solar Rift",
            "Final Rift",
        ]

        if self.level >= len(dimensions):
            self.finished = True
            return True

        self.level += 1
        self.dimension = dimensions[self.level - 1]
        self.runner.combo = 0
        self.score += 100
        return True

    def victory(self):
        if self.level == 5 and self.runner.distance >= 1500:
            self.finished = True
            self.score += 500
            return True

        return False

    def status(self):
        return {
            "runner": self.runner.name,
            "dimension": self.dimension,
            "level": self.level,
            "energy": self.runner.energy,
            "stability": self.runner.stability,
            "distance": self.runner.distance,
            "fragments": self.runner.fragments,
            "combo": self.runner.combo,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return DimensionRiftRunner()


def demo():
    game = create_game()

    for _ in range(8):
        game.dash()

    game.collect_fragment()
    game.collect_fragment()
    game.stabilize()
    game.phase_shift()

    for _ in range(4):
        game.next_dimension()

    game.victory()
    return game.status()


if __name__ == "__main__":
    print(demo())
