from dataclasses import dataclass


@dataclass
class Drone:
    name: str
    speed: int = 60
    handling: int = 60
    battery: int = 100
    boost: int = 3
    points: int = 0


class DroneRacingLeague:
    def __init__(self):
        self.pilot = "Niko Ray"
        self.drone = Drone("Falcon-X")
        self.lap = 1
        self.distance = 0
        self.checkpoints = 0
        self.finished = False

    def accelerate(self):
        if self.drone.battery < 5:
            return False

        self.distance += self.drone.speed
        self.drone.battery -= 5
        self.checkpoints += 1
        self.drone.points += 10
        return True

    def boost_forward(self):
        if self.drone.boost <= 0 or self.drone.battery < 15:
            return False

        self.distance += self.drone.speed * 2
        self.drone.boost -= 1
        self.drone.battery -= 15
        self.drone.points += 30
        return True

    def sharp_turn(self):
        if self.drone.handling < 40:
            self.drone.battery -= 8
            return False

        self.drone.handling -= 3
        self.distance += 35
        self.drone.battery -= 8
        self.drone.points += 15
        return True

    def recharge(self):
        self.drone.battery = min(100, self.drone.battery + 25)

    def check_finish(self):
        if self.distance >= 1000:
            self.finished = True
            self.drone.points += 100
            return True

        return False

    def status(self):
        return {
            "pilot": self.pilot,
            "drone": self.drone.name,
            "distance": self.distance,
            "battery": self.drone.battery,
            "handling": self.drone.handling,
            "boosts": self.drone.boost,
            "points": self.drone.points,
            "finished": self.finished,
        }


def create_game():
    return DroneRacingLeague()


def demo():
    game = create_game()

    for _ in range(6):
        game.accelerate()

    game.boost_forward()
    game.sharp_turn()
    game.check_finish()

    return game.status()


if __name__ == "__main__":
    print(demo())
