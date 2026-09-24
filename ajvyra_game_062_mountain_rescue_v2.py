from dataclasses import dataclass
import random


@dataclass
class Survivor:
    name: str
    health: int
    warmth: int
    rescued: bool = False


class MountainRescueGame:
    GAME_ID = "AJVYRA-062"
    TITLE = "White Peak Rescue"
    GENRE = "Mountain Rescue"

    def __init__(self):
        self.energy = 100
        self.rope = 100
        self.supplies = 8
        self.time = 0
        self.weather = "snow"
        self.position = [0, 0]

        self.survivors = [
            Survivor("Luma Rei", 75, 55),
            Survivor("Niko Arden", 60, 40),
            Survivor("Sera Voss", 90, 65),
        ]

    def move(self, direction: str) -> bool:
        cost = 8

        if self.energy < cost:
            return False

        directions = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
        }

        if direction not in directions:
            return False

        dx, dy = directions[direction]
        self.position[0] += dx
        self.position[1] += dy
        self.energy -= cost
        self.time += 1

        self._weather_damage()
        return True

    def _weather_damage(self):
        for survivor in self.survivors:
            if not survivor.rescued:
                survivor.warmth = max(0, survivor.warmth - random.randint(1, 5))

                if survivor.warmth < 20:
                    survivor.health = max(
                        0, survivor.health - random.randint(2, 6)
                    )

    def rescue(self, index: int) -> bool:
        if index < 0 or index >= len(self.survivors):
            return False

        survivor = self.survivors[index]

        if survivor.rescued or self.supplies <= 0:
            return False

        survivor.rescued = True
        survivor.health = min(100, survivor.health + 10)
        survivor.warmth = min(100, survivor.warmth + 20)

        self.supplies -= 1
        return True

    def use_rope(self):
        if self.rope >= 20 and self.energy >= 10:
            self.rope -= 20
            self.energy -= 10
            return True
        return False

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "position": self.position[:],
            "energy": self.energy,
            "rope": self.rope,
            "supplies": self.supplies,
            "survivors": [
                {
                    "name": s.name,
                    "health": s.health,
                    "warmth": s.warmth,
                    "rescued": s.rescued,
                }
                for s in self.survivors
            ],
        }
