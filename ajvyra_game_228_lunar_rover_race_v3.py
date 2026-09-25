from dataclasses import dataclass


@dataclass
class LunarRover:
    name: str
    speed: int = 60
    grip: int = 60
    battery: int = 100
    damage: int = 0


class LunarRoverRace:
    def __init__(self):
        self.driver = "Vera Knox"
        self.rover = LunarRover("Apollo-X")
        self.distance = 0
        self.track_length = 500
        self.lap = 1
        self.score = 0
        self.credits = 200
        self.finished = False

    def accelerate(self):
        if self.rover.battery < 12:
            return False

        self.rover.battery -= 12
        self.distance += self.rover.speed
        self.score += 10
        return True

    def lunar_drift(self):
        if self.rover.battery < 15:
            return False

        self.rover.battery -= 15

        if self.rover.grip >= 50:
            self.distance += 70
            self.score += 30
            return True

        self.rover.damage += 15
        return False

    def jump_crater(self):
        if self.rover.battery < 20:
            return False

        self.rover.battery -= 20

        if self.rover.speed >= 50:
            self.distance += 90
            self.score += 40
            return True

        self.rover.damage += 10
        return False

    def recharge(self):
        if self.credits < 30:
            return False

        self.credits -= 30
        self.rover.battery = min(100, self.rover.battery + 40)
        return True

    def check_finish(self):
        if self.distance >= self.track_length:
            self.finished = True
            self.score += 250
            return True

        return False

    def upgrade(self):
        if self.credits < 100:
            return False

        self.credits -= 100
        self.rover.speed += 10
        self.rover.grip += 5
        return True

    def status(self):
        return {
            "driver": self.driver,
            "rover": self.rover.name,
            "distance": self.distance,
            "track_length": self.track_length,
            "battery": self.rover.battery,
            "damage": self.rover.damage,
            "credits": self.credits,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return LunarRoverRace()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.lunar_drift()
    game.jump_crater()
    game.check_finish()
    print(game.status())
