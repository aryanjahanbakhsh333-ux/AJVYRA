from dataclasses import dataclass


@dataclass
class Train:
    name: str
    speed: int = 60
    condition: int = 100
    cargo_capacity: int = 20
    passengers: int = 0


class MiniatureTrainWorld:
    def __init__(self):
        self.conductor = "Theo Rail"
        self.train = Train("Little Comet")
        self.money = 300
        self.track_progress = 0
        self.score = 0
        self.stations = 0
        self.day = 1

    def board_passengers(self, amount: int):
        if amount <= 0:
            return False

        if self.train.passengers + amount > 20:
            return False

        self.train.passengers += amount
        self.score += amount * 4
        return True

    def drive(self, distance: int = 100):
        if self.train.condition < 20:
            return False

        self.track_progress += distance
        self.train.condition -= distance // 80
        self.score += distance // 4
        return True

    def arrive_station(self):
        if self.train.passengers <= 0:
            return False

        revenue = self.train.passengers * 15
        self.money += revenue
        self.score += revenue
        self.stations += 1
        self.train.passengers = 0
        return True

    def repair(self):
        if self.money < 50:
            return False

        self.money -= 50
        self.train.condition = min(
            100,
            self.train.condition + 25
        )
        self.score += 25
        return True

    def expand_track(self):
        if self.money < 150:
            return False

        self.money -= 150
        self.train.speed += 8
        self.score += 80
        return True

    def next_day(self):
        self.day += 1
        self.money += 30

    def status(self):
        return {
            "conductor": self.conductor,
            "train": self.train.name,
            "speed": self.train.speed,
            "condition": self.train.condition,
            "passengers": self.train.passengers,
            "money": self.money,
            "track_progress": self.track_progress,
            "stations": self.stations,
            "day": self.day,
            "score": self.score,
        }


def create_game():
    return MiniatureTrainWorld()


if __name__ == "__main__":
    game = create_game()
    game.board_passengers(8)
    game.drive(300)
    game.arrive_station()
    print(game.status())
