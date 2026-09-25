from dataclasses import dataclass


@dataclass
class RallyVehicle:
    name: str
    speed: int = 70
    handling: int = 65
    fuel: int = 100
    condition: int = 100


class DesertRallyNavigator:
    def __init__(self):
        self.driver = "Rex Dune"
        self.vehicle = RallyVehicle("Sand Viper")
        self.distance = 0
        self.goal = 2500
        self.temperature = 35
        self.score = 0
        self.money = 250
        self.checkpoints = 0
        self.finished = False

    def drive(self):
        if self.vehicle.fuel < 10:
            return False

        self.vehicle.fuel -= 10
        self.vehicle.condition -= 3
        self.distance += self.vehicle.speed
        self.temperature += 2
        self.score += 20
        return True

    def drift_dunes(self):
        if self.vehicle.fuel < 15:
            return False

        self.vehicle.fuel -= 15

        if self.vehicle.handling >= 60:
            self.distance += 140
            self.score += 60
            return True

        self.vehicle.condition -= 15
        return False

    def navigate_checkpoint(self):
        self.checkpoints += 1
        self.score += 45
        self.temperature = max(
            25,
            self.temperature - 5
        )
        return True

    def repair(self):
        if self.money < 70:
            return False

        self.money -= 70
        self.vehicle.condition = min(
            100,
            self.vehicle.condition + 30
        )
        return True

    def refuel(self):
        if self.money < 50:
            return False

        self.money -= 50
        self.vehicle.fuel = 100
        return True

    def finish_rally(self):
        if self.distance < self.goal:
            return False

        self.finished = True
        self.score += 400
        self.money += 300
        return True

    def status(self):
        return {
            "driver": self.driver,
            "vehicle": self.vehicle.name,
            "distance": self.distance,
            "goal": self.goal,
            "fuel": self.vehicle.fuel,
            "condition": self.vehicle.condition,
            "temperature": self.temperature,
            "checkpoints": self.checkpoints,
            "money": self.money,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return DesertRallyNavigator()


if __name__ == "__main__":
    game = create_game()
    game.drive()
    game.drift_dunes()
    game.navigate_checkpoint()
    print(game.status())
