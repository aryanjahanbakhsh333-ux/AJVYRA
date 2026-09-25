from dataclasses import dataclass


@dataclass
class CableCar:
    name: str
    capacity: int
    speed: int
    condition: int = 100
    passengers: int = 0


class MountainCableCarOperator:
    def __init__(self):
        self.operator = "Lena Frost"
        self.money = 400
        self.reputation = 25
        self.energy = 100
        self.score = 0
        self.station = "Valley"
        self.weather = "Clear"

        self.cars = [
            CableCar("Aurora", 20, 60),
            CableCar("Summit", 16, 55),
            CableCar("Eagle", 24, 50),
        ]

    def board_passengers(self, car_index: int, passengers: int):
        if not 0 <= car_index < len(self.cars):
            return False

        car = self.cars[car_index]

        if passengers <= 0:
            return False

        if car.passengers + passengers > car.capacity:
            return False

        car.passengers += passengers
        self.money += passengers * 3
        self.score += passengers * 5
        return True

    def transport(self, car_index: int):
        if not 0 <= car_index < len(self.cars):
            return False

        car = self.cars[car_index]

        if car.passengers <= 0 or car.condition < 30:
            return False

        distance_bonus = car.speed // 5
        self.station = "Summit"
        self.score += car.passengers * distance_bonus
        self.reputation += 3
        car.passengers = 0
        car.condition -= 5
        return True

    def inspect_car(self, car_index: int):
        if not 0 <= car_index < len(self.cars):
            return False

        return {
            "name": self.cars[car_index].name,
            "condition": self.cars[car_index].condition,
            "passengers": self.cars[car_index].passengers,
        }

    def repair_car(self, car_index: int):
        if not 0 <= car_index < len(self.cars):
            return False

        if self.money < 60:
            return False

        self.money -= 60
        self.cars[car_index].condition = min(
            100,
            self.cars[car_index].condition + 25
        )
        self.score += 30
        return True

    def change_weather(self):
        options = ["Clear", "Snow", "Wind", "Heavy Snow"]
        current = options.index(self.weather)
        self.weather = options[(current + 1) % len(options)]

    def status(self):
        return {
            "operator": self.operator,
            "station": self.station,
            "weather": self.weather,
            "money": self.money,
            "reputation": self.reputation,
            "energy": self.energy,
            "score": self.score,
            "cars": [
                {
                    "name": car.name,
                    "capacity": car.capacity,
                    "condition": car.condition,
                    "passengers": car.passengers,
                }
                for car in self.cars
            ],
        }


def create_game():
    return MountainCableCarOperator()


if __name__ == "__main__":
    game = create_game()
    game.board_passengers(0, 10)
    game.transport(0)
    print(game.status())
