"""
AJVYRA 111 — Air Rescue Pilot
Genre: Helicopter Rescue / Resource Management
"""

from dataclasses import dataclass, field
from math import hypot


@dataclass
class Survivor:
    name: str
    x: float
    y: float
    rescued: bool = False


@dataclass
class Helicopter:
    x: float = 0.0
    y: float = 0.0
    fuel: float = 100.0
    health: float = 100.0
    capacity: int = 3


@dataclass
class Mission:
    title: str
    target: str
    completed: bool = False


class AirRescuePilot:
    title = "Air Rescue Pilot"
    pilot = "Riven Cole"

    def __init__(self):
        self.helicopter = Helicopter()
        self.survivors = [
            Survivor("Mara", 12, 8),
            Survivor("Eli", -10, 15),
            Survivor("Soren", 18, -12),
            Survivor("Nia", -16, -9),
        ]
        self.missions = [
            Mission("Mountain Call", "Mara"),
            Mission("River Call", "Eli"),
            Mission("Storm Call", "Soren"),
            Mission("Night Call", "Nia"),
        ]
        self.rescued_count = 0
        self.score = 0
        self.time = 0
        self.log: list[str] = []

    def fly_to(self, x: float, y: float):
        distance = hypot(x - self.helicopter.x, y - self.helicopter.y)
        fuel_cost = distance * 0.8

        if fuel_cost > self.helicopter.fuel:
            self.log.append("Not enough fuel.")
            return False

        self.helicopter.x = x
        self.helicopter.y = y
        self.helicopter.fuel -= fuel_cost
        self.time += max(1, int(distance))
        return True

    def rescue(self):
        if self.rescued_count >= self.helicopter.capacity:
            self.log.append("The helicopter is full.")
            return False

        for survivor in self.survivors:
            if not survivor.rescued:
                distance = hypot(
                    survivor.x - self.helicopter.x,
                    survivor.y - self.helicopter.y,
                )

                if distance <= 3:
                    survivor.rescued = True
                    self.rescued_count += 1
                    self.score += 100
                    self.log.append(f"{survivor.name} rescued.")
                    return True

        self.log.append("No survivor is close enough.")
        return False

    def refuel(self):
        self.helicopter.fuel = min(100, self.helicopter.fuel + 50)
        self.log.append("Helicopter refueled.")

    def land_at_base(self):
        if self.fly_to(0, 0):
            self.rescued_count = 0
            self.log.append("Survivors delivered safely.")
            self.score += 50
            return True
        return False

    def status(self):
        return {
            "pilot": self.pilot,
            "position": (self.helicopter.x, self.helicopter.y),
            "fuel": round(self.helicopter.fuel, 1),
            "health": self.helicopter.health,
            "rescued": self.rescued_count,
            "total_rescued": sum(s.rescued for s in self.survivors),
            "score": self.score,
            "time": self.time,
        }


def create_game():
    return AirRescuePilot()


if __name__ == "__main__":
    game = create_game()
    game.fly_to(12, 8)
    game.rescue()
    game.land_at_base()
    print(game.status())
