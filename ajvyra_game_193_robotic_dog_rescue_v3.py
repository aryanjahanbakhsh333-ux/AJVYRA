from dataclasses import dataclass
from typing import List


@dataclass
class RescueDog:
    name: str
    energy: int = 100
    battery: int = 100
    trust: int = 20
    rescued: bool = False


class RoboticDogRescue:
    def __init__(self):
        self.operator = "Juno Hart"
        self.dog = RescueDog("Bolt")
        self.location = 0
        self.score = 0

        self.targets: List[str] = [
            "Collapsed Alley",
            "Flooded Basement",
            "Abandoned Warehouse",
            "Mountain Tunnel",
        ]

    def move(self, distance: int):
        if distance <= 0:
            return False

        cost = distance * 4

        if self.dog.battery < cost:
            return False

        self.dog.battery -= cost
        self.location += distance
        self.score += distance * 5
        return True

    def scan(self):
        if self.dog.battery < 8:
            return False

        self.dog.battery -= 8
        self.score += 20
        return True

    def locate_survivor(self):
        if self.location < 3:
            return False

        self.dog.trust = min(100, self.dog.trust + 15)
        self.score += 50
        return True

    def rescue(self):
        if self.dog.trust < 30:
            return False

        self.dog.energy -= 20
        self.dog.trust += 20
        self.dog.rescued = True
        self.score += 120
        return True

    def recharge(self):
        self.dog.battery = min(100, self.dog.battery + 35)
        self.dog.energy = min(100, self.dog.energy + 20)

    def status(self):
        return {
            "operator": self.operator,
            "robotic_dog": self.dog.name,
            "location": self.location,
            "battery": self.dog.battery,
            "energy": self.dog.energy,
            "trust": self.dog.trust,
            "rescued": self.dog.rescued,
            "score": self.score,
        }


def create_game():
    return RoboticDogRescue()


def demo():
    game = create_game()
    game.move(2)
    game.scan()
    game.move(2)
    game.locate_survivor()
    game.rescue()
    return game.status()


if __name__ == "__main__":
    print(demo())
