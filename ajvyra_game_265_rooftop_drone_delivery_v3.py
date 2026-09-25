from dataclasses import dataclass


@dataclass
class DeliveryDrone:
    name: str
    battery: int = 100
    speed: int = 70
    stability: int = 65
    cargo_capacity: int = 5
    cargo: int = 0


class RooftopDroneDelivery:
    def __init__(self):
        self.pilot = "Juno Sky"
        self.drone = DeliveryDrone("Falcon-X")
        self.rooftop = "Central Tower"
        self.distance = 0
        self.money = 100
        self.score = 0
        self.deliveries = 0

    def load_package(self, amount: int):
        if amount <= 0:
            return False

        if self.drone.cargo + amount > self.drone.cargo_capacity:
            return False

        self.drone.cargo += amount
        self.score += amount * 5
        return True

    def fly(self, distance: int):
        cost = max(5, distance // 10)

        if self.drone.battery < cost:
            return False

        self.drone.battery -= cost
        self.distance += distance
        self.score += distance // 2
        return True

    def rooftop_landing(self):
        if self.drone.battery < 10:
            return False

        self.drone.battery -= 10

        if self.drone.stability >= 60:
            self.score += 50
            return True

        self.drone.cargo = max(0, self.drone.cargo - 1)
        return False

    def deliver(self):
        if self.drone.cargo <= 0:
            return False

        reward = self.drone.cargo * 40
        self.money += reward
        self.score += reward
        self.deliveries += self.drone.cargo
        self.drone.cargo = 0
        return True

    def recharge(self):
        self.drone.battery = min(100, self.drone.battery + 45)

    def status(self):
        return {
            "pilot": self.pilot,
            "drone": self.drone.name,
            "battery": self.drone.battery,
            "cargo": self.drone.cargo,
            "distance": self.distance,
            "deliveries": self.deliveries,
            "money": self.money,
            "score": self.score,
        }


def create_game():
    return RooftopDroneDelivery()


if __name__ == "__main__":
    game = create_game()
    game.load_package(3)
    game.fly(200)
    game.rooftop_landing()
    game.deliver()
    print(game.status())
