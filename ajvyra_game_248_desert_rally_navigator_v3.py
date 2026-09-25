from dataclasses import dataclass


@dataclass
class RallyCar:
    name: str
    speed: int = 70
    handling: int = 60
    durability: int = 100
    fuel: int = 100


class DesertRallyNavigator:
    def __init__(self):
        self.driver = "Kian Dune"
        self.car = RallyCar("Sand Phantom")
        self.distance = 0
        self.goal = 1200
        self.stage = 1
        self.score = 0
        self.money = 200
        self.navigation = 65
        self.finished = False

    def accelerate(self):
        if self.car.fuel < 10 or self.car.durability <= 0:
            return False

        self.car.fuel -= 10
        self.distance += self.car.speed
        self.car.durability -= 2
        self.score += 15
        return True

    def navigate_dunes(self):
        if self.car.fuel < 15:
            return False

        self.car.fuel -= 15

        if self.navigation >= 60:
            self.distance += 100
            self.score += 50
            return True

        self.distance += 40
        self.car.durability -= 10
        self.score += 10
        return False

    def repair(self):
        if self.money < 60:
            return False

        self.money -= 60
        self.car.durability = min(
            100,
            self.car.durability + 25
        )
        return True

    def refuel(self):
        if self.money < 40:
            return False

        self.money -= 40
        self.car.fuel = 100
        return True

    def finish_rally(self):
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
            "durability": self.car.durability,
            "navigation": self.navigation,
            "money": self.money,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return DesertRallyNavigator()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.navigate_dunes()
    game.repair()
    print(game.status())
