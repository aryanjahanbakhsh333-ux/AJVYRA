"""
AJVYRA 152 — Haunted Hotel
Genre: Horror / Investigation
"""

from dataclasses import dataclass


@dataclass
class Room:
    number: int
    clue: str
    danger: int
    searched: bool = False


class HauntedHotel:
    title = "Haunted Hotel"
    investigator = "Mira Voss"

    def __init__(self):
        self.sanity = 100
        self.flashlight = 80
        self.evidence = []
        self.score = 0

        self.rooms = [
            Room(101, "A frozen clock", 15),
            Room(203, "A torn photograph", 25),
            Room(307, "A hidden diary", 40),
            Room(404, "A black key", 55),
        ]

    def search_room(self, number):
        room = next(
            (r for r in self.rooms if r.number == number),
            None,
        )

        if room is None or room.searched:
            return False

        if self.flashlight < 10:
            return False

        self.flashlight -= 10
        room.searched = True
        self.evidence.append(room.clue)

        self.sanity = max(
            0,
            self.sanity - room.danger // 4,
        )

        self.score += room.danger * 5
        return True

    def calm_down(self):
        self.sanity = min(
            100,
            self.sanity + 15,
        )

    def recharge_light(self):
        self.flashlight = min(
            100,
            self.flashlight + 25,
        )

    def solve_mystery(self):
        if len(self.evidence) < 3:
            return False

        self.score += 1000
        return True

    def status(self):
        return {
            "investigator": self.investigator,
            "sanity": self.sanity,
            "flashlight": self.flashlight,
            "evidence": list(self.evidence),
            "score": self.score,
        }


def create_game():
    return HauntedHotel()


if __name__ == "__main__":
    game = create_game()
    game.search_room(101)
    game.search_room(203)
    game.search_room(307)
    print(game.status())
