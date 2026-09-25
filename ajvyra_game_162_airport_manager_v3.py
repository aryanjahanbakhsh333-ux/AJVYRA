"""
AJVYRA 162 — Airport Manager
Genre: Management / Strategy
"""

from dataclasses import dataclass


@dataclass
class Flight:
    code: str
    passengers: int
    fuel_needed: int
    delay: int = 0


class AirportManager:
    title = "Airport Manager"
    manager_name = "Elara Venn"

    def __init__(self):
        self.money = 10000
        self.reputation = 50
        self.day = 1
        self.score = 0

        self.gates = 4
        self.staff = 12
        self.fuel = 500

        self.flights = [
            Flight("AV101", 120, 80),
            Flight("AV204", 180, 110),
            Flight("AV315", 90, 60),
        ]

    def assign_gate(self, flight_code):
        flight = self._find(flight_code)

        if flight is None or self.gates <= 0:
            return False

        self.gates -= 1
        flight.delay = max(
            0,
            flight.delay - 10,
        )

        self.score += flight.passengers
        return True

    def refuel(self, flight_code):
        flight = self._find(flight_code)

        if flight is None:
            return False

        if self.fuel < flight.fuel_needed:
            return False

        self.fuel -= flight.fuel_needed
        self.money += flight.passengers * 3
        self.reputation += 2
        return True

    def hire_staff(self):
        if self.money < 700:
            return False

        self.money -= 700
        self.staff += 2
        self.gates += 1
        return True

    def upgrade_terminal(self):
        if self.money < 1500:
            return False

        self.money -= 1500
        self.gates += 2
        self.reputation += 5
        self.score += 300
        return True

    def next_day(self):
        self.day += 1
        self.gates = min(
            self.gates + 2,
            10,
        )
        self.fuel += 250

    def _find(self, code):
        return next(
            (
                f for f in self.flights
                if f.code == code
            ),
            None,
        )

    def status(self):
        return {
            "manager": self.manager_name,
            "day": self.day,
            "money": self.money,
            "reputation": self.reputation,
            "gates": self.gates,
            "staff": self.staff,
            "fuel": self.fuel,
            "score": self.score,
        }


def create_game():
    return AirportManager()


if __name__ == "__main__":
    game = create_game()
    game.assign_gate("AV101")
    game.refuel("AV101")
    game.hire_staff()
    print(game.status())
