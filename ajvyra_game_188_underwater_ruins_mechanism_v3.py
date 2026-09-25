from dataclasses import dataclass
from typing import List


@dataclass
class Mechanism:
    name: str
    pattern: List[int]
    progress: int = 0
    solved: bool = False


class UnderwaterRuinsMechanism:
    def __init__(self):
        self.explorer = "Sera Nox"
        self.oxygen = 100
        self.energy = 100
        self.score = 0
        self.keys = 0
        self.mechanisms = [
            Mechanism("Sun Gate", [1, 2, 3]),
            Mechanism("Moon Gate", [3, 1, 2]),
            Mechanism("Tide Gate", [2, 3, 1]),
        ]

    def rotate_symbol(self, mechanism_index: int, symbol: int):
        if self.oxygen <= 0:
            return False

        if mechanism_index < 0 or mechanism_index >= len(self.mechanisms):
            return False

        mechanism = self.mechanisms[mechanism_index]

        if mechanism.solved:
            return True

        self.oxygen -= 2
        self.energy -= 1

        expected = mechanism.pattern[mechanism.progress]

        if symbol == expected:
            mechanism.progress += 1
            self.score += 15

            if mechanism.progress == len(mechanism.pattern):
                mechanism.solved = True
                self.keys += 1
                self.score += 75

            return True

        mechanism.progress = 0
        self.score = max(0, self.score - 10)
        return False

    def recover_oxygen(self):
        self.oxygen = min(100, self.oxygen + 25)

    def open_inner_chamber(self):
        if self.keys < 3:
            return False

        self.score += 250
        return True

    def status(self):
        return {
            "explorer": self.explorer,
            "oxygen": self.oxygen,
            "energy": self.energy,
            "keys": self.keys,
            "score": self.score,
            "mechanisms": [
                {
                    "name": m.name,
                    "progress": m.progress,
                    "solved": m.solved,
                }
                for m in self.mechanisms
            ],
        }


def create_game():
    return UnderwaterRuinsMechanism()


def demo():
    game = create_game()

    for index, pattern in enumerate(
        [ [1, 2, 3], [3, 1, 2], [2, 3, 1] ]
    ):
        for symbol in pattern:
            game.rotate_symbol(index, symbol)

    game.open_inner_chamber()
    return game.status()


if __name__ == "__main__":
    print(demo())
