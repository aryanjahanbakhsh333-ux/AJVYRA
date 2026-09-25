from dataclasses import dataclass


@dataclass
class CableCar:
    name: str
    capacity: int = 12
    condition: int = 100
    speed: int = 60


class MountainCableCarManager:
    def __init__(self):
        self.manager = "Lena Frost"
        self.car = CableCar("Summit Express")
        self.passengers = 0
        self.money = 300
        self.reputation = 40
        self.energy = 100
        self.score = 0
        self.trips = 0

    def board_passengers(self, amount: int):
        if amount <= 0:
            return False

        available = self.car.capacity - self.passengers

        if amount > available:
            return False

        self.passengers += amount
        self.score += amount * 5
        return True

    def run_trip(self):
        if self.passengers <= 0:
            return False

        if self.energy < 15 or self.car.condition < 20:
            return False

        self.energy -= 15
        self.car.condition -= 5

        revenue = self.passengers * 25
        self.money += revenue
        self.score += revenue
        self.trips += 1
        self.passengers = 0

        self.reputation = min(
            100,
            self.reputation + 2
        )
        return True

    def repair(self):
        if self.money < 80:
            return False

        self.money -= 80
        self.car.condition = min(
            100,
            self.car.condition + 30
        )
        self.score += 30
        return True

    def upgrade(self):
        if self.money < 200:
            return False

        self.money -= 200
        self.car.capacity += 4
        self.car.speed += 8
        self.score += 100
        return True

    def recharge(self):
        self.energy = min(100, self.energy + 40)

    def status(self):
        return {
            "manager": self.manager,
            "cable_car": self.car.name,
            "capacity": self.car.capacity,
            "condition": self.car.condition,
            "speed": self.car.speed,
            "passengers": self.passengers,
            "energy": self.energy,
            "money": self.money,
            "reputation": self.reputation,
            "trips": self.trips,
            "score": self.score,
        }


def create_game():
    return MountainCableCarManager()


if __name__ == "__main__":
    game = create_game()
    game.board_passengers(8)
    game.run_trip()
    game.upgrade()
    print(game.status())
