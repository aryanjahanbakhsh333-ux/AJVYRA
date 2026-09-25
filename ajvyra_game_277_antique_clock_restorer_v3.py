from dataclasses import dataclass


@dataclass
class AntiqueClock:
    name: str
    condition: int
    rarity: int
    restored: bool = False


class AntiqueClockRestorer:
    def __init__(self):
        self.restorer = "Theo Bell"
        self.money = 300
        self.tools = 60
        self.reputation = 20
        self.score = 0
        self.restored_count = 0

        self.clocks = [
            AntiqueClock("Royal Pendulum", 40, 50),
            AntiqueClock("Moon Dial", 55, 70),
            AntiqueClock("Golden Tower", 30, 100),
            AntiqueClock("Eclipse Chronometer", 20, 150),
        ]

    def clean(self, index: int):
        if not 0 <= index < len(self.clocks):
            return False

        if self.tools < 5:
            return False

        clock = self.clocks[index]
        self.tools -= 5
        clock.condition = min(
            100,
            clock.condition + 12
        )
        self.score += 20
        return True

    def repair(self, index: int):
        if not 0 <= index < len(self.clocks):
            return False

        if self.tools < 15:
            return False

        clock = self.clocks[index]
        self.tools -= 15
        clock.condition = min(
            100,
            clock.condition + 25
        )
        self.score += 45
        return True

    def polish(self, index: int):
        if not 0 <= index < len(self.clocks):
            return False

        clock = self.clocks[index]

        if clock.condition < 70:
            return False

        clock.condition = min(
            100,
            clock.condition + 10
        )
        self.score += 30
        return True

    def restore(self, index: int):
        if not 0 <= index < len(self.clocks):
            return False

        clock = self.clocks[index]

        if clock.condition < 90 or clock.restored:
            return False

        clock.restored = True
        self.restored_count += 1
        reward = clock.rarity * 3
        self.money += reward
        self.reputation += clock.rarity // 20
        self.score += reward
        return True

    def buy_tools(self):
        if self.money < 60:
            return False

        self.money -= 60
        self.tools += 30
        return True

    def status(self):
        return {
            "restorer": self.restorer,
            "money": self.money,
            "tools": self.tools,
            "reputation": self.reputation,
            "restored": self.restored_count,
            "score": self.score,
        }


def create_game():
    return AntiqueClockRestorer()


if __name__ == "__main__":
    game = create_game()
    game.clean(0)
    game.repair(0)
    game.polish(0)
    print(game.status())
