"""
AJVYRA 138 — Desert Rally
Genre: Racing / Vehicle Strategy
"""

from dataclasses import dataclass


@dataclass
class Vehicle:
    name: str
    speed: int
    handling: int
    durability: int
    fuel: int = 100


class DesertRally:
    title = "Desert Rally"
    driver = "Kai Mercer"

    def __init__(self):
        self.vehicle = Vehicle(
            "Dune X",
            speed=82,
            handling=76,
            durability=88,
        )

        self.stage = 1
        self.distance = 0
        self.time = 0
        self.score = 0
        self.repairs = 3

    def accelerate(self):
        fuel_cost = 8

        if self.vehicle.fuel < fuel_cost:
            return False

        self.vehicle.fuel -= fuel_cost
        self.distance += self.vehicle.speed // 10
        self.time += 4
        self.score += self.vehicle.speed
        return True

    def drift(self):
        if self.vehicle.fuel < 5:
            return False

        self.vehicle.fuel -= 5
        self.distance += self.vehicle.handling // 12
        self.time += 2
        self.score += self.vehicle.handling * 2
        return True

    def repair(self):
        if self.repairs <= 0:
            return False

        self.repairs -= 1
        self.vehicle.durability = min(
            100,
            self.vehicle.durability + 20,
        )
        return True

    def finish_stage(self):
        if self.distance < 100:
            return False

        self.stage += 1
        self.distance = 0
        self.vehicle.fuel = min(
            100,
            self.vehicle.fuel + 30,
        )
        self.score += 500
        return True

    def status(self):
        return {
            "driver": self.driver,
            "vehicle": self.vehicle.name,
            "stage": self.stage,
            "distance": self.distance,
            "fuel": self.vehicle.fuel,
            "durability": self.vehicle.durability,
            "time": self.time,
            "score": self.score,
        }


def create_game():
    return DesertRally()


if __name__ == "__main__":
    game = create_game()

    for _ in range(8):
        game.accelerate()

    game.finish_stage()
    print(game.status())
