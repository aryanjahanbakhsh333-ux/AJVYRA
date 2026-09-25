from dataclasses import dataclass


@dataclass
class DeliveryMech:
    name: str
    speed: int = 60
    armor: int = 80
    battery: int = 100
    cargo_capacity: int = 5


class NeonDeliveryMech:
    def __init__(self):
        self.pilot = "Vex Orion"
        self.mech = DeliveryMech("Courier-X")
        self.cargo = 0
        self.distance = 0
        self.money = 200
        self.reputation = 20
        self.score = 0
        self.deliveries = 0

    def load_package(self, amount: int = 1):
        if amount <= 0:
            return False

        if self.cargo + amount > self.mech.cargo_capacity:
            return False

        self.cargo += amount
        return True

    def move(self, distance: int = 100):
        battery_cost = max(5, distance // 20)

        if self.mech.battery < battery_cost:
            return False

        self.mech.battery -= battery_cost
        self.distance += distance
        self.score += distance // 5
        return True

    def mech_boost(self):
        if self.mech.battery < 20:
            return False

        self.mech.battery -= 20
        self.distance += self.mech.speed * 3
        self.score += 70
        return True

    def deliver(self):
        if self.cargo <= 0:
            return False

        reward = self.cargo * 80
        self.money += reward
        self.reputation = min(
            100,
            self.reputation + self.cargo * 2
        )
        self.score += reward
        self.deliveries += self.cargo
        self.cargo = 0
        return True

    def repair(self):
        if self.money < 60:
            return False

        self.money -= 60
        self.mech.armor = min(100, self.mech.armor + 25)
        return True

    def recharge(self):
        self.mech.battery = min(
            100,
            self.mech.battery + 40
        )

    def upgrade(self):
        if self.money < 250:
            return False

        self.money -= 250
        self.mech.speed += 10
        self.mech.cargo_capacity += 2
        self.score += 100
        return True

    def status(self):
        return {
            "pilot": self.pilot,
            "mech": self.mech.name,
            "battery": self.mech.battery,
            "armor": self.mech.armor,
            "cargo": self.cargo,
            "capacity": self.mech.cargo_capacity,
            "distance": self.distance,
            "money": self.money,
            "reputation": self.reputation,
            "deliveries": self.deliveries,
            "score": self.score,
        }


def create_game():
    return NeonDeliveryMech()


if __name__ == "__main__":
    game = create_game()
    game.load_package(2)
    game.move(200)
    game.deliver()
    print(game.status())
