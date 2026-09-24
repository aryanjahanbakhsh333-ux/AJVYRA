from dataclasses import dataclass


@dataclass
class Hive:
    name: str
    bees: int
    honey: int
    health: int = 100


class BeekeeperSimulatorGame:
    GAME_ID = "AJVYRA-074"
    TITLE = "Golden Hive"
    GENRE = "Nature Simulation"

    def __init__(self):
        self.player = "Nera Bloom"
        self.money = 500
        self.hives = [
            Hive("Sun Hive", 80, 10),
            Hive("Forest Hive", 60, 5),
            Hive("Moon Hive", 45, 2),
        ]

    def feed(self, hive_index: int):
        if hive_index < 0 or hive_index >= len(self.hives):
            return False

        hive = self.hives[hive_index]

        if self.money < 20:
            return False

        self.money -= 20
        hive.bees += 10
        hive.health = min(100, hive.health + 8)

        return True

    def collect_honey(self, hive_index: int):
        if hive_index < 0 or hive_index >= len(self.hives):
            return 0

        hive = self.hives[hive_index]

        amount = min(hive.honey, hive.bees // 10)

        hive.honey -= amount
        self.money += amount * 15

        return amount

    def daily_cycle(self):
        for hive in self.hives:
            hive.honey += max(1, hive.bees // 20)
            hive.health = max(0, hive.health - 2)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "player": self.player,
            "money": self.money,
            "hives": [h.__dict__.copy() for h in self.hives],
        }
