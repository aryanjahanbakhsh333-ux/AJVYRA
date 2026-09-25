from dataclasses import dataclass


@dataclass
class Watchtower:
    name: str
    visibility: int = 70
    equipment: int = 80
    radio: int = 60


class ForestFireWatchtower:
    def __init__(self):
        self.ranger = "Maya Rowan"
        self.tower = Watchtower("North Ridge")
        self.water = 100
        self.energy = 100
        self.alert_level = 0
        self.fires_detected = 0
        self.score = 0
        self.day = 1

    def scan_forest(self):
        if self.energy < 10:
            return False

        self.energy -= 10
        self.score += self.tower.visibility
        self.fires_detected += 1
        return True

    def report_fire(self):
        if self.tower.radio < 30:
            return False

        self.tower.radio -= 10
        self.alert_level += 15
        self.score += 50
        return True

    def deploy_water(self):
        if self.water < 20:
            return False

        self.water -= 20
        self.alert_level = max(0, self.alert_level - 20)
        self.score += 60
        return True

    def repair_equipment(self):
        if self.energy < 15:
            return False

        self.energy -= 15
        self.tower.equipment = min(
            100,
            self.tower.equipment + 20
        )
        self.score += 25
        return True

    def next_day(self):
        self.day += 1
        self.energy = min(100, self.energy + 35)
        self.water = min(100, self.water + 25)
        self.alert_level = max(0, self.alert_level - 5)

    def status(self):
        return {
            "ranger": self.ranger,
            "tower": self.tower.name,
            "day": self.day,
            "energy": self.energy,
            "water": self.water,
            "fires_detected": self.fires_detected,
            "alert_level": self.alert_level,
            "score": self.score,
        }


def create_game():
    return ForestFireWatchtower()


if __name__ == "__main__":
    game = create_game()
    game.scan_forest()
    game.report_fire()
    game.deploy_water()
    print(game.status())
