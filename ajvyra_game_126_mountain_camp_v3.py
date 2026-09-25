"""
AJVYRA 126 — Mountain Camp
Genre: Expedition / Camp Management
"""

from dataclasses import dataclass


@dataclass
class Camper:
    name: str
    stamina: int = 100
    morale: int = 80


class MountainCamp:
    title = "Mountain Camp"
    leader = "Rowan Peak"

    def __init__(self):
        self.day = 1
        self.food = 100
        self.firewood = 80
        self.weather = 50
        self.altitude = 1200
        self.score = 0

        self.team = [
            Camper("Iris"),
            Camper("Tao"),
            Camper("Mika"),
        ]

    def climb(self):
        if self.food < 10 or self.firewood < 5:
            return False

        self.food -= 10
        self.firewood -= 5
        self.altitude += 300

        for camper in self.team:
            camper.stamina = max(0, camper.stamina - 20)

        self.score += 50
        return True

    def establish_camp(self):
        self.firewood += 20
        self.food += 15

        for camper in self.team:
            camper.morale = min(
                100,
                camper.morale + 10,
            )

        self.score += 20

    def survive_night(self):
        self.food = max(0, self.food - len(self.team) * 3)
        self.firewood = max(0, self.firewood - 10)

        if self.firewood == 0:
            for camper in self.team:
                camper.morale = max(
                    0,
                    camper.morale - 20,
                )

        self.day += 1

    def rest(self):
        for camper in self.team:
            camper.stamina = min(
                100,
                camper.stamina + 25,
            )

    def status(self):
        return {
            "leader": self.leader,
            "day": self.day,
            "altitude": self.altitude,
            "food": self.food,
            "firewood": self.firewood,
            "weather": self.weather,
            "score": self.score,
            "team": [
                {
                    "name": c.name,
                    "stamina": c.stamina,
                    "morale": c.morale,
                }
                for c in self.team
            ],
        }


def create_game():
    return MountainCamp()


if __name__ == "__main__":
    game = create_game()
    game.establish_camp()
    game.climb()
    game.survive_night()
    game.rest()
    print(game.status())
