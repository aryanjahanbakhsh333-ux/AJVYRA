"""
AJVYRA 155 — Ocean Rescue Command
Genre: Rescue / Strategy
"""

from dataclasses import dataclass


@dataclass
class RescueBoat:
    name: str
    fuel: int
    capacity: int
    speed: int


@dataclass
class RescueTarget:
    name: str
    distance: int
    people: int
    rescued: bool = False


class OceanRescueCommand:
    title = "Ocean Rescue Command"
    commander = "Nora Tide"

    def __init__(self):
        self.boat = RescueBoat(
            "Aegis",
            fuel=100,
            capacity=8,
            speed=70,
        )

        self.targets = [
            RescueTarget("North Beacon", 20, 3),
            RescueTarget("Storm Point", 45, 5),
            RescueTarget("Broken Pier", 70, 7),
        ]

        self.score = 0
        self.rescued_people = 0

    def travel(self, target_name):
        target = next(
            (
                t for t in self.targets
                if t.name == target_name
            ),
            None,
        )

        if target is None or target.rescued:
            return False

        fuel_cost = max(
            5,
            target.distance // 4,
        )

        if self.boat.fuel < fuel_cost:
            return False

        self.boat.fuel -= fuel_cost
        return True

    def rescue(self, target_name):
        target = next(
            (
                t for t in self.targets
                if t.name == target_name
            ),
            None,
        )

        if target is None or target.rescued:
            return False

        if target.people > self.boat.capacity:
            return False

        target.rescued = True
        self.rescued_people += target.people
        self.score += target.people * 150
        return True

    def refuel(self):
        self.boat.fuel = 100

    def status(self):
        return {
            "commander": self.commander,
            "fuel": self.boat.fuel,
            "capacity": self.boat.capacity,
            "rescued_people": self.rescued_people,
            "score": self.score,
            "completed": all(
                t.rescued for t in self.targets
            ),
        }


def create_game():
    return OceanRescueCommand()


if __name__ == "__main__":
    game = create_game()
    game.travel("North Beacon")
    game.rescue("North Beacon")
    print(game.status())
