from dataclasses import dataclass


@dataclass
class Horse:
    name: str
    speed: int
    stamina: int
    health: int = 100


class WesternRanchGame:
    GAME_ID = "AJVYRA-099"
    TITLE = "Dust & Hooves"
    GENRE = "Ranch Simulation"

    def __init__(self):
        self.rancher = "Rai Mercer"
        self.money = 1000
        self.feed = 100

        self.horses = [
            Horse("Comet", 80, 70),
            Horse("Shadow", 72, 85),
            Horse("Dusty", 65, 90),
        ]

    def feed_horse(self, index: int):
        if index < 0 or index >= len(self.horses):
            return False

        if self.feed < 10:
            return False

        self.feed -= 10

        horse = self.horses[index]
        horse.health = min(100, horse.health + 10)
        horse.stamina = min(100, horse.stamina + 8)

        return True

    def train(self, index: int):
        if index < 0 or index >= len(self.horses):
            return False

        horse = self.horses[index]

        if horse.stamina < 15:
            return False

        horse.stamina -= 15
        horse.speed = min(100, horse.speed + 3)

        return True

    def sell_horse(self, index: int):
        if index < 0 or index >= len(self.horses):
            return False

        horse = self.horses.pop(index)
        value = horse.speed * 5 + horse.health * 2

        self.money += value

        return value

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "rancher": self.rancher,
            "money": self.money,
            "feed": self.feed,
            "horses": [h.__dict__.copy() for h in self.horses],
        }
