from dataclasses import dataclass


@dataclass
class Locomotive:
    name: str
    speed: int = 65
    fuel: int = 100
    condition: int = 100
    cargo_capacity: int = 10


class WildWestTrainDriver:
    def __init__(self):
        self.driver = "Cole Mercer"
        self.train = Locomotive("Red Arrow")
        self.location = "Dust Valley"
        self.distance = 0
        self.goal = 1800
        self.cargo = 0
        self.money = 200
        self.score = 0
        self.finished = False

    def accelerate(self):
        if self.train.fuel < 10 or self.train.condition <= 0:
            return False

        self.train.fuel -= 10
        self.train.condition -= 2
        self.distance += self.train.speed
        self.score += 15
        return True

    def load_cargo(self, amount: int):
        if amount <= 0:
            return False

        if self.cargo + amount > self.train.cargo_capacity:
            return False

        self.cargo += amount
        self.score += amount * 5
        return True

    def deliver_cargo(self):
        if self.cargo <= 0:
            return False

        reward = self.cargo * 60
        self.money += reward
        self.score += reward // 2
        self.cargo = 0
        return True

    def repair_train(self):
        if self.money < 60:
            return False

        self.money -= 60
        self.train.condition = min(
            100,
            self.train.condition + 30
        )
        return True

    def refuel(self):
        if self.money < 50:
            return False

        self.money -= 50
        self.train.fuel = 100
        return True

    def finish_route(self):
        if self.distance < self.goal:
            return False

        self.finished = True
        self.score += 350
        return True

    def status(self):
        return {
            "driver": self.driver,
            "train": self.train.name,
            "location": self.location,
            "distance": self.distance,
            "goal": self.goal,
            "fuel": self.train.fuel,
            "condition": self.train.condition,
            "cargo": self.cargo,
            "money": self.money,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return WildWestTrainDriver()


if __name__ == "__main__":
    game = create_game()
    game.load_cargo(5)
    game.accelerate()
    game.deliver_cargo()
    print(game.status())
