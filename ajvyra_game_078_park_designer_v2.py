from dataclasses import dataclass


@dataclass
class Attraction:
    name: str
    cost: int
    fun: int
    capacity: int


class ParkDesignerGame:
    GAME_ID = "AJVYRA-078"
    TITLE = "Dreamland Park"
    GENRE = "Theme Park Design"

    def __init__(self):
        self.money = 5000
        self.rating = 50
        self.visitors = 0

        self.attractions = [
            Attraction("Sky Wheel", 1200, 25, 40),
            Attraction("Mirror Maze", 800, 18, 25),
            Attraction("Rocket Ride", 1800, 35, 60),
            Attraction("Water Kingdom", 2200, 40, 80),
        ]

        self.built = []

    def build(self, index: int):
        if index < 0 or index >= len(self.attractions):
            return False

        attraction = self.attractions[index]

        if attraction.name in self.built:
            return False

        if self.money < attraction.cost:
            return False

        self.money -= attraction.cost
        self.built.append(attraction.name)

        self.rating = min(100, self.rating + attraction.fun // 3)
        self.visitors += attraction.capacity

        return True

    def daily_income(self):
        income = self.visitors * max(1, self.rating // 25)
        self.money += income
        return income

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "money": self.money,
            "rating": self.rating,
            "visitors": self.visitors,
            "built": self.built[:],
        }
