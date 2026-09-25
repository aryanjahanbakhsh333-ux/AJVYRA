from dataclasses import dataclass


@dataclass
class Festival:
    name: str
    popularity: int
    cost: int
    prepared: bool = False


class FantasyKingdomFestival:
    def __init__(self):
        self.organizer = "Elara Moon"
        self.gold = 700
        self.reputation = 30
        self.happiness = 50
        self.score = 0
        self.day = 1

        self.festivals = [
            Festival("Moonlight Fair", 60, 100),
            Festival("Dragon Lantern Night", 85, 180),
            Festival("Royal Music Feast", 75, 150),
            Festival("Crystal Carnival", 95, 240),
        ]

    def prepare_festival(self, index: int):
        if not 0 <= index < len(self.festivals):
            return False

        festival = self.festivals[index]

        if festival.prepared or self.gold < festival.cost:
            return False

        self.gold -= festival.cost
        festival.prepared = True
        self.score += festival.popularity
        return True

    def host_festival(self, index: int):
        if not 0 <= index < len(self.festivals):
            return False

        festival = self.festivals[index]

        if not festival.prepared:
            return False

        festival.prepared = False
        reward = festival.popularity * 3
        self.gold += reward
        self.reputation += festival.popularity // 15
        self.happiness = min(100, self.happiness + 10)
        self.score += reward
        return True

    def decorate(self):
        if self.gold < 60:
            return False

        self.gold -= 60
        self.happiness = min(100, self.happiness + 5)
        self.score += 25
        return True

    def invite_travelers(self):
        self.reputation += 5
        self.score += 30

    def next_day(self):
        self.day += 1
        self.happiness = max(0, self.happiness - 2)

    def status(self):
        return {
            "organizer": self.organizer,
            "day": self.day,
            "gold": self.gold,
            "reputation": self.reputation,
            "happiness": self.happiness,
            "score": self.score,
            "prepared": sum(
                festival.prepared for festival in self.festivals
            ),
        }


def create_game():
    return FantasyKingdomFestival()


if __name__ == "__main__":
    game = create_game()
    game.prepare_festival(0)
    game.decorate()
    game.host_festival(0)
    print(game.status())
