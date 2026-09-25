from dataclasses import dataclass


@dataclass
class RaceCar:
    name: str
    speed: int = 70
    handling: int = 65
    fuel: int = 100
    condition: int = 100


class CityTrafficRacer:
    def __init__(self):
        self.driver = "Zev Carter"
        self.car = RaceCar("Street Phantom")
        self.distance = 0
        self.goal = 1500
        self.score = 0
        self.money = 150
        self.combo = 0
        self.finished = False

    def accelerate(self):
        if self.car.fuel < 12 or self.car.condition <= 0:
            return False

        self.car.fuel -= 12
        self.distance += self.car.speed
        self.car.condition -= 2
        self.score += 15
        return True

    def traffic_weave(self):
        if self.car.fuel < 15:
            return False

        self.car.fuel -= 15

        if self.car.handling >= 60:
            self.distance += 110
            self.combo += 1
            self.score += 40 * self.combo
            return True

        self.car.condition -= 15
        self.combo = 0
        return False

    def nitro(self):
        if self.car.fuel < 25:
            return False

        self.car.fuel -= 25
        self.distance += self.car.speed * 2
        self.car.condition -= 8
        self.score += 70
        return True

    def refuel(self):
        if self.money < 40:
            return False

        self.money -= 40
        self.car.fuel = 100
        return True

    def repair(self):
        if self.money < 60:
            return False

        self.money -= 60
        self.car.condition = min(100, self.car.condition + 30)
        return True

    def finish_race(self):
        if self.distance < self.goal:
            return False

        self.finished = True
        self.score += 300
        self.money += 200
        return True

    def status(self):
        return {
            "driver": self.driver,
            "car": self.car.name,
            "distance": self.distance,
            "goal": self.goal,
            "fuel": self.car.fuel,
            "condition": self.car.condition,
            "combo": self.combo,
            "money": self.money,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return CityTrafficRacer()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.traffic_weave()
    game.nitro()
    print(game.status())
