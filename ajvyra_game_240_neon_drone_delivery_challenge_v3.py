from dataclasses import dataclass


@dataclass
class DeliveryDrone:
    name: str
    speed: int = 65
    battery: int = 100
    cargo_capacity: int = 5
    reputation: int = 20


class NeonDroneDeliveryChallenge:
    def __init__(self):
        self.pilot = "Vex Rowan"
        self.drone = DeliveryDrone("NX-9")
        self.city_distance = 0
        self.deliveries = 0
        self.score = 0
        self.money = 100
        self.combo = 0
        self.level = 1

    def fly(self, distance: int):
        if distance <= 0 or self.drone.battery < distance // 5:
            return False

        self.drone.battery -= distance // 5
        self.city_distance += distance
        self.score += distance // 2
        return True

    def deliver(self):
        if self.drone.battery < 10:
            return False

        self.drone.battery -= 10
        self.deliveries += 1
        self.combo += 1
        reward = 40 + self.combo * 10
        self.money += reward
        self.score += reward
        return True

    def avoid_traffic(self):
        if self.drone.battery < 8:
            return False

        self.drone.battery -= 8
        self.drone.speed += 3
        self.score += 20
        return True

    def recharge(self):
        self.drone.battery = min(100, self.drone.battery + 40)

    def upgrade(self):
        if self.money < 120:
            return False

        self.money -= 120
        self.drone.speed += 10
        self.drone.cargo_capacity += 1
        self.level += 1
        self.score += 50
        return True

    def status(self):
        return {
            "pilot": self.pilot,
            "drone": self.drone.name,
            "battery": self.drone.battery,
            "speed": self.drone.speed,
            "cargo_capacity": self.drone.cargo_capacity,
            "deliveries": self.deliveries,
            "combo": self.combo,
            "money": self.money,
            "score": self.score,
            "level": self.level,
        }


def create_game():
    return NeonDroneDeliveryChallenge()


if __name__ == "__main__":
    game = create_game()
    game.fly(100)
    game.avoid_traffic()
    game.deliver()
    game.recharge()
    print(game.status())
