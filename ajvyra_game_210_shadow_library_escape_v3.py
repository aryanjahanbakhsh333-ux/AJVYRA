from dataclasses import dataclass
from typing import List


@dataclass
class EscapeCharacter:
    name: str
    intelligence: int = 80
    stealth: int = 70
    energy: int = 100


@dataclass
class LibraryDoor:
    name: str
    code_length: int
    solved: bool = False


class ShadowLibraryEscape:
    def __init__(self):
        self.player = EscapeCharacter("Nyra Vale")
        self.room = 1
        self.time_left = 30
        self.keys = 0
        self.score = 0
        self.escaped = False

        self.doors: List[LibraryDoor] = [
            LibraryDoor("Archive Door", 3),
            LibraryDoor("Forbidden Wing", 4),
            LibraryDoor("Observatory Gate", 5),
        ]

    def search_shelves(self):
        if self.player.energy < 8:
            return False

        self.player.energy -= 8
        self.time_left -= 2
        self.keys += 1
        self.score += 30
        return True

    def decode_door(self, index: int):
        if not 0 <= index < len(self.doors):
            return False

        door = self.doors[index]

        if door.solved:
            return True

        difficulty = door.code_length * 15

        if self.player.intelligence < difficulty:
            self.time_left -= 4
            self.player.energy -= 6
            return False

        door.solved = True
        self.keys += 1
        self.time_left -= door.code_length
        self.score += door.code_length * 30

        return True

    def move_forward(self):
        if self.keys <= 0:
            return False

        self.keys -= 1
        self.room += 1
        self.score += 20
        return True

    def hide(self):
        if self.player.energy < 10:
            return False

        self.player.energy -= 10
        self.player.stealth += 5
        self.time_left -= 1
        return True

    def escape(self):
        if (
            self.room >= 4
            and self.time_left > 0
            and self.player.stealth >= 70
        ):
            self.escaped = True
            self.score += 400
            return True

        return False

    def status(self):
        return {
            "character": self.player.name,
            "room": self.room,
            "time_left": self.time_left,
            "energy": self.player.energy,
            "intelligence": self.player.intelligence,
            "stealth": self.player.stealth,
            "keys": self.keys,
            "score": self.score,
            "doors_solved": sum(
                door.solved for door in self.doors
            ),
            "escaped": self.escaped,
        }


def create_game():
    return ShadowLibraryEscape()


def demo():
    game = create_game()

    game.search_shelves()

    for i in range(3):
        game.decode_door(i)
        game.move_forward()

    game.hide()
    game.escape()

    return game.status()


if __name__ == "__main__":
    print(demo())
