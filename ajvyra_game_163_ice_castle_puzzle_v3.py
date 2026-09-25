"""
AJVYRA 163 — Ice Castle Puzzle
Genre: Puzzle / Adventure
"""

from dataclasses import dataclass


@dataclass
class Chamber:
    name: str
    symbol: str
    solved: bool = False


class IceCastlePuzzle:
    title = "Ice Castle Puzzle"
    explorer = "Neris Vale"

    def __init__(self):
        self.energy = 100
        self.score = 0
        self.keys = 0

        self.chambers = [
            Chamber("Frozen Gate", "SUN"),
            Chamber("Mirror Hall", "MOON"),
            Chamber("Crystal Room", "STAR"),
            Chamber("Royal Vault", "CROWN"),
        ]

        self.sequence = []

    def inspect(self, chamber_name):
        chamber = next(
            (
                c for c in self.chambers
                if c.name == chamber_name
            ),
            None,
        )

        if chamber is None:
            return None

        return chamber.symbol

    def solve(self, chamber_name, answer):
        chamber = next(
            (
                c for c in self.chambers
                if c.name == chamber_name
            ),
            None,
        )

        if chamber is None or chamber.solved:
            return False

        if self.energy < 10:
            return False

        self.energy -= 10

        if answer != chamber.symbol:
            self.score = max(
                0,
                self.score - 30,
            )
            return False

        chamber.solved = True
        self.keys += 1
        self.score += 150
        self.sequence.append(answer)
        return True

    def open_vault(self):
        if self.keys < 4:
            return False

        self.score += 1000
        return True

    def rest(self):
        self.energy = min(
            100,
            self.energy + 30,
        )

    def status(self):
        return {
            "explorer": self.explorer,
            "energy": self.energy,
            "keys": self.keys,
            "score": self.score,
            "solved_chambers": [
                c.name
                for c in self.chambers
                if c.solved
            ],
        }


def create_game():
    return IceCastlePuzzle()


if __name__ == "__main__":
    game = create_game()

    for chamber in game.chambers:
        game.solve(
            chamber.name,
            chamber.symbol,
        )

    print(game.status())
