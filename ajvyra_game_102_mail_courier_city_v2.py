"""
AJVYRA Game 102 - Mail Courier City
Genre: Route Optimization
"""

from dataclasses import dataclass
from random import choice


@dataclass
class Courier:
    name: str = "Niko Vale"
    stamina: int = 100
    reputation: int = 0
    money: int = 20


@dataclass
class Delivery:
    destination: str
    reward: int
    deadline: int
    delivered: bool = False


class MailCourierCity:
    title = "Mail Courier City"

    def __init__(self):
        self.courier = Courier()
        self.time = 0
        self.distance = 0
        self.deliveries = [
            Delivery("Old Market", 12, 8),
            Delivery("River District", 18, 12),
            Delivery("Clock Tower", 15, 16),
            Delivery("Harbor Gate", 25, 22),
        ]
        self.log = []

    def travel(self, distance):
        if distance <= 0:
            return False

        stamina_cost = max(1, distance // 2)

        if stamina_cost > self.courier.stamina:
            self.log.append("Niko is too tired to continue.")
            return False

        self.courier.stamina -= stamina_cost
        self.time += distance
        self.distance += distance
        self.log.append(f"Courier traveled {distance} blocks.")
        self.check_deadlines()
        return True

    def deliver(self, destination):
        for package in self.deliveries:
            if (
                package.destination.lower() == destination.lower()
                and not package.delivered
            ):
                if self.time <= package.deadline:
                    package.delivered = True
                    self.courier.money += package.reward
                    self.courier.reputation += 5
                    self.log.append(
                        f"Package delivered to {package.destination}."
                    )
                    return True

                self.log.append("The delivery deadline was missed.")
                return False

        self.log.append("No active package found.")
        return False

    def rest(self):
        self.time += 2
        self.courier.stamina = min(100, self.courier.stamina + 25)
        self.log.append("Niko rests at a courier station.")

    def check_deadlines(self):
        for package in self.deliveries:
            if not package.delivered and self.time > package.deadline:
                package.delivered = True
                self.log.append(
                    f"Delivery to {package.destination} expired."
                )

    def choose_shortcut(self):
        shortcuts = {
            "Old Market": 2,
            "River District": 4,
            "Clock Tower": 3,
            "Harbor Gate": 5,
        }
        return choice(list(shortcuts.items()))

    def snapshot(self):
        return {
            "courier": self.courier.name,
            "time": self.time,
            "stamina": self.courier.stamina,
            "money": self.courier.money,
            "reputation": self.courier.reputation,
            "deliveries": [
                {
                    "destination": d.destination,
                    "reward": d.reward,
                    "deadline": d.deadline,
                    "delivered": d.delivered,
                }
                for d in self.deliveries
            ],
        }


def create_game():
    return MailCourierCity()


if __name__ == "__main__":
    game = create_game()
    game.travel(3)
    game.deliver("Old Market")
    print(game.snapshot())
