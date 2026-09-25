from dataclasses import dataclass


@dataclass
class HotelRoom:
    number: int
    comfort: int
    paranormal: int
    occupied: bool = False


class HauntedHotelManager:
    def __init__(self):
        self.manager = "Milo Graves"
        self.money = 500
        self.reputation = 30
        self.energy = 100
        self.guests = 0
        self.score = 0
        self.night = 1

        self.rooms = [
            HotelRoom(101, 70, 20),
            HotelRoom(102, 65, 35),
            HotelRoom(201, 80, 50),
            HotelRoom(202, 90, 75),
        ]

    def prepare_room(self, index: int):
        if not 0 <= index < len(self.rooms):
            return False

        room = self.rooms[index]

        if self.energy < 8:
            return False

        self.energy -= 8
        room.comfort = min(100, room.comfort + 15)
        self.score += 25
        return True

    def calm_spirit(self, index: int):
        if not 0 <= index < len(self.rooms):
            return False

        room = self.rooms[index]

        if self.energy < 15:
            return False

        self.energy -= 15
        room.paranormal = max(
            0,
            room.paranormal - 20
        )
        self.score += 45
        return True

    def check_in_guest(self, index: int):
        if not 0 <= index < len(self.rooms):
            return False

        room = self.rooms[index]

        if room.occupied or room.comfort < 50:
            return False

        room.occupied = True
        self.guests += 1
        self.money += 120
        self.reputation += 3
        self.score += 80
        return True

    def upgrade_hotel(self):
        if self.money < 200:
            return False

        self.money -= 200

        for room in self.rooms:
            room.comfort = min(100, room.comfort + 10)

        self.score += 100
        return True

    def next_night(self):
        self.night += 1
        self.energy = min(100, self.energy + 25)

        for room in self.rooms:
            room.occupied = False
            room.paranormal = min(
                100,
                room.paranormal + 5
            )

    def status(self):
        return {
            "manager": self.manager,
            "night": self.night,
            "money": self.money,
            "reputation": self.reputation,
            "energy": self.energy,
            "guests": self.guests,
            "score": self.score,
        }


def create_game():
    return HauntedHotelManager()


if __name__ == "__main__":
    game = create_game()
    game.prepare_room(0)
    game.calm_spirit(0)
    game.check_in_guest(0)
    print(game.status())
