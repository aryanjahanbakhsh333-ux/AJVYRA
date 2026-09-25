"""
AJVYRA 179 — Time Travel Postman
Genre: Adventure / Puzzle / Time Travel
"""

from dataclasses import dataclass


@dataclass
class Delivery:
    recipient: str
    year: int
    message: str
    delivered: bool = False


class TimeTravelPostman:
    title = "Time Travel Postman"
    courier = "Milo Chron"

    def __init__(self):
        self.year = 2026
        self.energy = 100
        self.stamps = 10
        self.score = 0

        self.deliveries = [
            Delivery(
                "Eren",
                1920,
                "The blue letter",
            ),
            Delivery(
                "Nia",
                2080,
                "The silver message",
            ),
            Delivery(
                "Sol",
                1750,
                "The sealed map",
            ),
            Delivery(
                "Aya",
                2300,
                "The final signal",
            ),
        ]

    def travel_time(self, target_year):
        cost = max(
            10,
            abs(target_year - self.year) // 10,
        )

        if self.energy < cost:
            return False

        self.energy -= cost
        self.year = target_year
        self.score += 50
        return True

    def deliver(self, recipient):
        delivery = next(
            (
                d for d in self.deliveries
                if d.recipient == recipient
            ),
            None,
        )

        if delivery is None:
            return False

        if delivery.delivered:
            return False

        if self.year != delivery.year:
            return False

        if self.stamps <= 0:
            return False

        self.stamps -= 1
        delivery.delivered = True
        self.score += 300
        return True

    def recharge(self):
        self.energy = min(
            100,
            self.energy + 30,
        )

    def completed(self):
        return all(
            d.delivered
            for d in self.deliveries
        )

    def status(self):
        return {
            "courier": self.courier,
            "year": self.year,
            "energy": self.energy,
            "stamps": self.stamps,
            "score": self.score,
            "completed": self.completed(),
        }


def create_game():
    return TimeTravelPostman()


if __name__ == "__main__":
    game = create_game()
    game.travel_time(1920)
    game.deliver("Eren")
    print(game.status())
