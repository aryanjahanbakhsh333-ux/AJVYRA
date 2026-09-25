from dataclasses import dataclass


@dataclass
class Exhibit:
    name: str
    historical_value: int
    condition: int = 100
    secured: bool = True


class MuseumTimekeeper:
    def __init__(self):
        self.timekeeper = "Orin Bell"
        self.hour = 8
        self.energy = 100
        self.money = 250
        self.score = 0
        self.reputation = 30

        self.exhibits = [
            Exhibit("Solar Compass", 60),
            Exhibit("Royal Manuscript", 80),
            Exhibit("Ancient Clock", 100),
            Exhibit("Star Map", 120),
        ]

    def inspect_exhibit(self, index: int):
        if not 0 <= index < len(self.exhibits):
            return None

        exhibit = self.exhibits[index]
        self.energy = max(0, self.energy - 5)
        self.score += 10

        return {
            "name": exhibit.name,
            "condition": exhibit.condition,
            "value": exhibit.historical_value,
        }

    def restore_exhibit(self, index: int):
        if not 0 <= index < len(self.exhibits):
            return False

        exhibit = self.exhibits[index]

        if self.money < 50 or self.energy < 10:
            return False

        self.money -= 50
        self.energy -= 10
        exhibit.condition = min(100, exhibit.condition + 20)
        self.score += 30
        return True

    def secure_gallery(self):
        secured = 0

        for exhibit in self.exhibits:
            if not exhibit.secured:
                exhibit.secured = True
                secured += 1

        self.score += secured * 20
        return secured

    def research_history(self, index: int):
        if not 0 <= index < len(self.exhibits):
            return False

        exhibit = self.exhibits[index]

        if self.energy < 15:
            return False

        self.energy -= 15
        self.reputation += exhibit.historical_value // 20
        self.score += exhibit.historical_value
        return True

    def next_hour(self):
        self.hour += 1
        self.energy = min(100, self.energy + 15)
        self.money += 10

    def status(self):
        return {
            "timekeeper": self.timekeeper,
            "hour": self.hour,
            "energy": self.energy,
            "money": self.money,
            "reputation": self.reputation,
            "score": self.score,
            "exhibits": len(self.exhibits),
        }


def create_game():
    return MuseumTimekeeper()


if __name__ == "__main__":
    game = create_game()
    game.inspect_exhibit(0)
    game.restore_exhibit(0)
    game.research_history(0)
    print(game.status())
