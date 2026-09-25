from dataclasses import dataclass


@dataclass
class LibraryRoom:
    name: str
    mystery: int
    searched: bool = False
    solved: bool = False


class HauntedLibraryEscape:
    def __init__(self):
        self.player = "Noah Vale"
        self.sanity = 100
        self.focus = 80
        self.time_left = 20
        self.keys = 0
        self.score = 0
        self.exit_open = False
        self.escaped = False

        self.rooms = [
            LibraryRoom("Dust Hall", 20),
            LibraryRoom("Forbidden Wing", 40),
            LibraryRoom("Clock Archive", 60),
            LibraryRoom("Shadow Reading Room", 80),
        ]

    def search_room(self, index: int):
        if not 0 <= index < len(self.rooms):
            return False

        if self.time_left <= 0 or self.focus < 8:
            return False

        room = self.rooms[index]
        self.time_left -= 2
        self.focus -= 8
        room.searched = True
        self.score += room.mystery
        return True

    def solve_mystery(self, index: int):
        if not 0 <= index < len(self.rooms):
            return False

        room = self.rooms[index]

        if not room.searched or room.solved:
            return False

        if self.focus < room.mystery // 5:
            return False

        self.focus -= room.mystery // 5
        room.solved = True
        self.keys += 1
        self.score += room.mystery * 2
        return True

    def stay_calm(self):
        self.sanity = min(100, self.sanity + 15)
        self.focus = min(100, self.focus + 20)
        self.time_left -= 1

    def open_exit(self):
        if self.keys < 4:
            return False

        self.exit_open = True
        self.score += 150
        return True

    def escape(self):
        if not self.exit_open or self.time_left <= 0:
            return False

        self.escaped = True
        self.score += 400
        return True

    def status(self):
        return {
            "player": self.player,
            "sanity": self.sanity,
            "focus": self.focus,
            "time_left": self.time_left,
            "keys": self.keys,
            "score": self.score,
            "exit_open": self.exit_open,
            "escaped": self.escaped,
        }


def create_game():
    return HauntedLibraryEscape()


if __name__ == "__main__":
    game = create_game()
    game.search_room(0)
    game.solve_mystery(0)
    game.stay_calm()
    print(game.status())
