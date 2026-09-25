"""
AJVYRA 127 — Robot Courier
Genre: Programming / Route Optimization
"""

from dataclasses import dataclass


@dataclass
class Delivery:
    destination: tuple[int, int]
    package: str
    delivered: bool = False


class RobotCourier:
    title = "Robot Courier"
    robot = "RX-7"

    def __init__(self):
        self.x = 0
        self.y = 0
        self.battery = 100
        self.score = 0
        self.deliveries = [
            Delivery((4, 2), "Medicine"),
            Delivery((-3, 5), "Letters"),
            Delivery((6, -4), "Circuit"),
        ]
        self.commands = []

    def move(self, dx, dy):
        distance = abs(dx) + abs(dy)

        if self.battery < distance:
            return False

        self.x += dx
        self.y += dy
        self.battery -= distance
        self.commands.append(("move", dx, dy))
        return True

    def deliver(self):
        for delivery in self.deliveries:
            if delivery.delivered:
                continue

            if (
                delivery.destination
                == (self.x, self.y)
            ):
                delivery.delivered = True
                self.score += 100
                return delivery.package

        return None

    def recharge(self):
        self.battery = 100

    def optimize_route(self):
        remaining = [
            d for d in self.deliveries
            if not d.delivered
        ]

        return sorted(
            remaining,
            key=lambda d:
                abs(d.destination[0] - self.x)
                + abs(d.destination[1] - self.y),
        )

    def status(self):
        return {
            "robot": self.robot,
            "position": (self.x, self.y),
            "battery": self.battery,
            "score": self.score,
            "delivered": [
                d.package
                for d in self.deliveries
                if d.delivered
            ],
            "remaining": [
                d.package
                for d in self.deliveries
                if not d.delivered
            ],
        }


def create_game():
    return RobotCourier()


if __name__ == "__main__":
    game = create_game()
    game.move(4, 2)
    game.deliver()
    print(game.status())
