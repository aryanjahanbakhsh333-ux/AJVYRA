from dataclasses import dataclass
from typing import List


@dataclass
class HologramClue:
    name: str
    reliability: int
    found: bool = False


class HologramDetective:
    def __init__(self):
        self.detective = "Iris Venn"
        self.energy = 100
        self.insight = 50
        self.score = 0
        self.case_solved = False

        self.clues: List[HologramClue] = [
            HologramClue("Blue Reflection", 70),
            HologramClue("Broken Signal", 80),
            HologramClue("Missing Timestamp", 90),
            HologramClue("Unknown Face", 75),
        ]

    def scan_scene(self):
        if self.energy < 10:
            return False

        self.energy -= 10

        for clue in self.clues:
            if not clue.found:
                clue.found = True
                self.insight += clue.reliability // 10
                self.score += clue.reliability // 2
                return clue.name

        return None

    def reconstruct(self, index: int):
        if not 0 <= index < len(self.clues):
            return False

        clue = self.clues[index]

        if not clue.found:
            return False

        self.energy -= 5
        self.insight += 5
        self.score += 20
        return True

    def connect_evidence(self):
        found = sum(
            clue.found
            for clue in self.clues
        )

        if found < 3 or self.insight < 75:
            return False

        self.case_solved = True
        self.score += 250
        return True

    def recharge(self):
        self.energy = min(
            100,
            self.energy + 30
        )

    def status(self):
        return {
            "detective": self.detective,
            "energy": self.energy,
            "insight": self.insight,
            "score": self.score,
            "clues": sum(
                clue.found
                for clue in self.clues
            ),
            "case_solved": self.case_solved,
        }


def create_game():
    return HologramDetective()


def demo():
    game = create_game()

    for _ in range(4):
        game.scan_scene()

    game.reconstruct(0)
    game.reconstruct(1)
    game.reconstruct(2)
    game.connect_evidence()

    return game.status()


if __name__ == "__main__":
    print(demo())
