from dataclasses import dataclass


@dataclass
class Building:
    name: str
    floors: int
    fire: int
    civilians: int


class FirefighterRescueGame:
    GAME_ID = "AJVYRA-088"
    TITLE = "Redline Rescue"
    GENRE = "Emergency Rescue"

    def __init__(self):
        self.firefighter = "Kane Ryo"
        self.water = 100
        self.health = 100
        self.rescued = 0

        self.buildings = [
            Building("Metro Hotel", 8, 70, 12),
            Building("East Tower", 15, 90, 24),
            Building("Old Theater", 5, 55, 8),
        ]

    def extinguish(self, index: int):
        if index < 0 or index >= len(self.buildings):
            return False

        if self.water <= 0:
            return False

        building = self.buildings[index]

        amount = min(20, self.water)
        building.fire = max(0, building.fire - amount)
        self.water -= amount

        return building.fire

    def rescue(self, index: int):
        if index < 0 or index >= len(self.buildings):
            return False

        building = self.buildings[index]

        if building.fire > 30:
            return False

        rescued_now = building.civilians
        building.civilians = 0
        self.rescued += rescued_now

        return rescued_now

    def refill_water(self):
        self.water = 100

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "firefighter": self.firefighter,
            "water": self.water,
            "health": self.health,
            "rescued": self.rescued,
            "buildings": [b.__dict__.copy() for b in self.buildings],
        }
