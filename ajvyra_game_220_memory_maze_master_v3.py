from dataclasses import dataclass
from typing import List


@dataclass
class MazePlayer:
    name: str
    memory: int = 70
    focus: int = 80
    energy: int = 100
    keys: int = 0


class MemoryMazeMaster:
    def __init__(self):
        self.player = MazePlayer("Nero Ash")
        self.room = 0
        self.score = 0
        self.level = 1
        self.exit_found = False

        self.patterns: List[List[int]] = [
            [1, 3, 2],
            [2, 4, 1, 3],
            [4, 2, 3, 1, 5],
        ]

    def memorize(self):
        if self.player.energy < 8:
            return False

        self.player.energy -= 8
        self.player.memory += 5
        self.score += 20
        return True

    def choose_path(self, value: int):
        pattern = self.patterns[
            min(self.level - 1, len(self.patterns) - 1)
        ]

        if self.player.energy < 5:
            return False

        self.player.energy -= 5

        if value in pattern:
            self.room += 1
            self.score += 25

            if self.room >= len(pattern):
                self.player.keys += 1
                self.score += 75

            return True

        self.player.focus -= 8
        self.score = max(0, self.score - 10)
        return False

    def focus_burst(self):
        if self.player.energy < 15:
            return False

        self.player.energy -= 15
        self.player.focus = min(
            100,
            self.player.focus + 20
        )
        self.score += 30
        return True

    def unlock_exit(self):
        if self.player.keys < self.level:
            return False

        self.exit_found = True
        self.score += 200
        return True

    def next_level(self):
        if not self.exit_found:
            return False

        self.level += 1
        self.room = 0
        self.exit_found = False
        self.player.energy = min(
            100,
            self.player.energy + 20
        )
        self.score += 100
        return True

    def status(self):
        return {
            "player": self.player.name,
            "level": self.level,
            "room": self.room,
            "memory": self.player.memory,
            "focus": self.player.focus,
            "energy": self.player.energy,
            "keys": self.player.keys,
            "score": self.score,
            "exit_found": self.exit_found,
        }


def create_game():
    return MemoryMazeMaster()


def demo():
    game = create_game()

    game.memorize()

    for value in [1, 3, 2]:
        game.choose_path(value)

    game.unlock_exit()
    game.next_level()

    return game.status()


if __name__ == "__main__":
    print(demo())
