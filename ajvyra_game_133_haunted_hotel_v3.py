"""
AJVYRA 133 — Haunted Hotel
Genre: Horror / Investigation
"""

from dataclasses import dataclass


@dataclass
class Room:
    number: int
    fear: int
    clue: str
    investigated: bool = False


class HauntedHotel:
    title = "Haunted Hotel"
    investigator = "Eli Voss"

    def __init__(self):
        self.sanity = 100
        self.battery = 100
        self.evidence = []
        self.score = 0
        self.current_room = 101

        self.rooms = {
            101: Room(101, 15, "old photograph"),
            202: Room(202, 30, "broken bell"),
            303: Room(303, 55, "locked diary"),
            404: Room(404, 80, "silver key"),
        }

    def enter(self, room_number):
        if room_number not in self.rooms:
            return False

        room = self.rooms[room_number]

        self.current_room = room_number
        self.sanity = max(
            0,
            self.sanity - room.fear // 5,
        )
        return True

    def investigate(self):
        room = self.rooms[self.current_room]

        if room.investigated:
            return False

        if self.battery < 10:
            return False

        self.battery -= 10
        room.investigated = True
        self.evidence.append(room.clue)
        self.score += room.fear + 25
        return room.clue

    def calm_down(self):
        self.sanity = min(
            100,
            self.sanity + 20,
        )

    def solve_mystery(self):
        required = {
            "old photograph",
            "broken bell",
            "locked diary",
            "silver key",
        }

        return required.issubset(set(self.evidence))

    def status(self):
        return {
            "investigator": self.investigator,
            "room": self.current_room,
            "sanity": self.sanity,
            "battery": self.battery,
            "evidence": list(self.evidence),
            "score": self.score,
            "mystery_solved": self.solve_mystery(),
        }


def create_game():
    return HauntedHotel()


if __name__ == "__main__":
    game = create_game()

    for room in (101, 202, 303, 404):
        game.enter(room)
        game.investigate()

    print(game.status())
