"""
AJVYRA 131 — Winter Expedition
Genre: Expedition / Survival Strategy
"""

from dataclasses import dataclass


@dataclass
class Explorer:
    name: str
    stamina: int = 100
    warmth: int = 100


class WinterExpedition:
    title = "Winter Expedition"
    leader = "Kael North"

    def __init__(self):
        self.day = 1
        self.distance = 0
        self.food = 90
        self.fuel = 70
        self.weather = 65
        self.morale = 80
        self.score = 0

        self.team = [
            Explorer("Lena"),
            Explorer("Orin"),
            Explorer("Vey"),
        ]

    def travel(self, kilometers):
        if kilometers <= 0 or self.food < kilometers * 2:
            return False

        self.food -= kilometers * 2
        self.distance += kilometers

        for explorer in self.team:
            explorer.stamina = max(
                0,
                explorer.stamina - kilometers * 3,
            )
            explorer.warmth = max(
                0,
                explorer.warmth - kilometers * 2,
            )

        self.score += kilometers * 10
        return True

    def build_shelter(self):
        if self.fuel < 10:
            return False

        self.fuel -= 10

        for explorer in self.team:
            explorer.warmth = min(
                100,
                explorer.warmth + 25,
            )

        self.morale = min(100, self.morale + 5)
        self.score += 40
        return True

    def rest(self):
        for explorer in self.team:
            explorer.stamina = min(
                100,
                explorer.stamina + 30,
            )

        self.morale = min(100, self.morale + 10)

    def next_day(self):
        self.day += 1
        self.weather = max(
            10,
            self.weather + ((self.day * 7) % 21) - 10,
        )

        if self.weather < 35:
            self.fuel = max(0, self.fuel - 5)
            self.morale = max(0, self.morale - 8)

    def expedition_complete(self):
        return self.distance >= 100

    def status(self):
        return {
            "leader": self.leader,
            "day": self.day,
            "distance": self.distance,
            "food": self.food,
            "fuel": self.fuel,
            "weather": self.weather,
            "morale": self.morale,
            "score": self.score,
            "complete": self.expedition_complete(),
        }


def create_game():
    return WinterExpedition()


if __name__ == "__main__":
    game = create_game()
    game.travel(10)
    game.build_shelter()
    game.rest()
    game.next_day()
    print(game.status())
