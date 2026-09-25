from dataclasses import dataclass


@dataclass
class FarmRobot:
    name: str
    efficiency: int = 70
    battery: int = 100
    capacity: int = 20


class RobotFarmFuture:
    def __init__(self):
        self.farmer = "Niko Green"
        self.robot = FarmRobot("AGRO-9")
        self.crops = 0
        self.water = 300
        self.money = 300
        self.energy = 100
        self.score = 0
        self.harvests = 0

    def plant(self, amount: int = 5):
        if self.water < amount * 2:
            return False

        self.water -= amount * 2
        self.crops += amount
        self.score += amount * 5
        return True

    def robot_harvest(self):
        if self.crops <= 0 or self.robot.battery < 15:
            return False

        amount = min(
            self.crops,
            self.robot.capacity
        )

        self.crops -= amount
        self.robot.battery -= 15
        self.money += amount * 30
        self.harvests += amount
        self.score += amount * 25
        return True

    def recharge_robot(self):
        if self.energy < 20:
            return False

        self.energy -= 20
        self.robot.battery = min(
            100,
            self.robot.battery + 45
        )
        return True

    def upgrade_robot(self):
        if self.money < 200:
            return False

        self.money -= 200
        self.robot.efficiency += 10
        self.robot.capacity += 5
        self.score += 100
        return True

    def install_irrigation(self):
        if self.money < 150:
            return False

        self.money -= 150
        self.water += 250
        self.score += 70
        return True

    def status(self):
        return {
            "farmer": self.farmer,
            "robot": self.robot.name,
            "battery": self.robot.battery,
            "efficiency": self.robot.efficiency,
            "capacity": self.robot.capacity,
            "crops": self.crops,
            "water": self.water,
            "money": self.money,
            "harvests": self.harvests,
            "score": self.score,
        }


def create_game():
    return RobotFarmFuture()


if __name__ == "__main__":
    game = create_game()
    game.plant(10)
    game.robot_harvest()
    game.recharge_robot()
    print(game.status())
