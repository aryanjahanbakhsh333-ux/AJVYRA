from dataclasses import dataclass
import random


@dataclass
class Swimmer:
    name: str
    distance: int
    stamina: int
    rescued: bool = False


class BeachLifeguardGame:
    GAME_ID = "AJVYRA-098"
    TITLE = "Blue Watch"
    GENRE = "Lifeguard Rescue"

    def __init__(self):
        self.lifeguard = "Kai Renn"
        self.energy = 100
        self.rescues = 0
        self.score = 0

        self.swimmers = [
            Swimmer("Mina", 40, 70),
            Swimmer("Joren", 75, 55),
            Swimmer("Sia", 110, 35),
        ]

    def swim_to(self, index: int):
        if index < 0 or index >= len(self.swimmers):
            return False

        swimmer = self.swimmers[index]

        if swimmer.rescued or self.energy <= 0:
            return False

        cost = max(5, swimmer.distance // 8)

        self.energy -= cost
        swimmer.distance = max(0, swimmer.distance - 35)
        swimmer.stamina = max(0, swimmer.stamina - 8)

        return True

    def rescue(self, index: int):
        if index < 0 or index >= len(self.swimmers):
            return False

        swimmer = self.swimmers[index]

        if swimmer.rescued or swimmer.distance > 15:
            return False

        swimmer.rescued = True
        self.rescues += 1
        self.score += 100

        return True

    def scan(self):
        for swimmer in self.swimmers:
            if not swimmer.rescued:
                swimmer.stamina = max(
                    0,
                    swimmer.stamina - random.randint(1, 5)
                )

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "lifeguard": self.lifeguard,
            "energy": self.energy,
            "rescues": self.rescues,
            "score": self.score,
            "swimmers": [s.__dict__.copy() for s in self.swimmers],
        }
