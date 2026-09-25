from dataclasses import dataclass


@dataclass
class HotelRoom:
    number: int
    comfort: int
    mystery: int
    occupied: bool = False
    cleaned: bool = True


class HauntedHotelManager:
    def __init__(self):
        self.manager = "Mara Voss"
        self.money = 500
        self.reputation = 30
        self.energy = 100
        self.score = 0
        self.night = 1
        self.rooms = [
            HotelRoom(101, 60, 20),
            HotelRoom(202, 70, 40),
            HotelRoom(303, 80, 65),
            HotelRoom(404, 90, 90),
        ]

    def clean_room(self, number: int):
        room = self._room(number)

        if room is None or room.cleaned or self.energy < 10:
            return False

        self.energy -= 10
        room.cleaned = True
        self.score += 15
        return True

    def prepare_room(self, number: int):
        room = self._room(number)

        if room is None or not room.cleaned:
            return False

        room.occupied = True
        self.money += room.comfort
        self.reputation += 5
        self.score += room.comfort
        return True

    def investigate_room(self, number: int):
        room = self._room(number)

        if room is None or self.energy < 15:
            return False

        self.energy -= 15

        if room.mystery >= 60:
            self.score += room.mystery
            self.reputation += 10
            return "mystery_found"

        self.score += 10
        return "quiet"

    def upgrade_room(self, number: int):
        room = self._room(number)

        if room is None or self.money < 100:
            return False

        self.money -= 100
        room.comfort = min(100, room.comfort + 15)
        self.score += 25
        return True

    def next_night(self):
        self.night += 1
        self.energy = min(100, self.energy + 40)

        for room in self.rooms:
            room.occupied = False

    def _room(self, number):
        return next(
            (room for room in self.rooms if room.number == number),
            None
        )

    def status(self):
        return {
            "manager": self.manager,
            "money": self.money,
            "reputation": self.reputation,
            "energy": self.energy,
            "score": self.score,
            "night": self.night,
            "rooms": len(self.rooms),
        }


def create_game():
    return HauntedHotelManager()


if __name__ == "__main__":
    game = create_game()
    game.prepare_room(101)
    game.investigate_room(303)
    game.upgrade_room(202)
    print(game.status())
