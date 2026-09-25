"""
AJVYRA 137 — Puzzle Island
Genre: Adventure / Logic Puzzle
"""

from dataclasses import dataclass


@dataclass
class Puzzle:
    name: str
    answer: int
    solved: bool = False


class PuzzleIsland:
    title = "Puzzle Island"
    explorer = "Mira Sol"

    def __init__(self):
        self.energy = 100
        self.keys = 0
        self.score = 0

        self.puzzles = [
            Puzzle("Stone Gate", 8),
            Puzzle("Ancient Tower", 13),
            Puzzle("Moon Temple", 21),
            Puzzle("Final Observatory", 34),
        ]

    def solve(self, index, answer):
        if not 0 <= index < len(self.puzzles):
            return False

        puzzle = self.puzzles[index]

        if puzzle.solved:
            return False

        self.energy -= 10

        if answer == puzzle.answer:
            puzzle.solved = True
            self.keys += 1
            self.score += 100 + index * 50
            return True

        return False

    def open_gate(self):
        if self.keys < 2:
            return False

        self.score += 150
        return True

    def final_chamber(self):
        return all(
            puzzle.solved
            for puzzle in self.puzzles
        )

    def status(self):
        return {
            "explorer": self.explorer,
            "energy": self.energy,
            "keys": self.keys,
            "score": self.score,
            "solved": [
                p.name
                for p in self.puzzles
                if p.solved
            ],
            "island_complete": self.final_chamber(),
        }


def create_game():
    return PuzzleIsland()


if __name__ == "__main__":
    game = create_game()

    for i, answer in enumerate((8, 13, 21, 34)):
        game.solve(i, answer)

    print(game.status())
