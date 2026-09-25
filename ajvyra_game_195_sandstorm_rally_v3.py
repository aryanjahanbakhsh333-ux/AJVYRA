from dataclasses import dataclass


@dataclass
class RallyCar:
    driver: str
    speed: int = 70
    handling: int = 70
    durability: int = 100
    fuel: int = 100
    distance: int = 0
    score: int = 0


class SandstormRally:
    def __init__(self):
        self.car = RallyCar("Zane Kiro")
        self.stage = 1
        self.sandstorm = 35
        self.finished = False

    def accelerate(self):
        if self.car.fuel < 8 or self.car.durability < 10:
            return False

        self.car.distance += self.car.speed
        self.car.fuel -= 8
        self.car.durability -= self.sandstorm // 20
        self.car.score += 12
        return True

    def drift(self):
        if self.car.fuel < 10:
            return False

        self.car.distance += self.car.handling // 2
        self.car.fuel -= 10
        self.car.handling -= 2
        self.car.score += 25
        return True

    def repair(self):
        self.car.durability = min(100, self.car.durability + 20)
        self.car.fuel = max(0, self.car.fuel - 5)
        self.car.score += 10

    def navigate_storm(self, skill: int):
        if skill < 1 or skill > 10:
            return False

        if skill >= self.sandstorm // 5:
            self.car.score += 40
            self.sandstorm = max(5, self.sandstorm - 5)
            return True

        self.car.durability -= 10
        return False

    def finish_stage(self):
        if self.car.distance >= 1000:
            self.finished = True
            self.car.score += 200
            return True

        return False

    def status(self):
        return {
            "driver": self.car.driver,
            "stage": self.stage,
            "distance": self.car.distance,
            "fuel": self.car.fuel,
            "durability": self.car.durability,
            "sandstorm": self.sandstorm,
            "score": self.car.score,
            "finished": self.finished,
        }


def create_game():
    return SandstormRally()


def demo():
    game = create_game()

    for _ in range(8):
        game.accelerate()

    game.navigate_storm(8)
    game.drift()
    game.finish_stage()

    return game.status()


if __name__ == "__main__":
    print(demo())
