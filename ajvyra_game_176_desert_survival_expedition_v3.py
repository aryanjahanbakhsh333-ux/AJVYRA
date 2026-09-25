"""
AJVYRA 176 — Desert Survival Expedition
Genre: Survival / Exploration
"""

from dataclasses import dataclass


@dataclass
class Traveler:
    name: str
    health: int = 100
    stamina: int = 100
    navigation: int = 75


class DesertSurvivalExpedition:
    title = "Desert Survival Expedition"
    traveler_name = "Sora Vale"

    def __init__(self):
        self.player = Traveler(
            self.traveler_name
        )

        self.water = 100
        self.food = 80
        self.distance = 0
        self.goal = 500
        self.score = 0
        self.day = 1

    def travel(self):
        if self.player.stamina < 15:
            return False

        if self.water < 8 or self.food < 5:
            return False

        self.player.stamina -= 15
        self.water -= 8
        self.food -= 5

        progress = (
            25
            + self.player.navigation // 5
        )

        self.distance += progress
        self.score += progress

        if self.distance >= self.goal:
            self.distance = self.goal

        return True

    def find_oasis(self):
        self.water = min(
            100,
            self.water + 40,
        )
        self.player.stamina = min(
            100,
            self.player.stamina + 15,
        )
        self.score += 150
        return True

    def rest(self):
        self.player.stamina = min(
            100,
            self.player.stamina + 30,
        )
        self.day += 1

    def navigate(self, success):
        if success:
            self.player.navigation = min(
                100,
                self.player.navigation + 5,
            )
            self.score += 80
        else:
            self.player.health = max(
                0,
                self.player.health - 10,
            )

    def completed(self):
        return self.distance >= self.goal

    def status(self):
        return {
            "traveler": self.player.name,
            "day": self.day,
            "health": self.player.health,
            "stamina": self.player.stamina,
            "water": self.water,
            "food": self.food,
            "distance": self.distance,
            "goal": self.goal,
            "score": self.score,
            "completed": self.completed(),
        }


def create_game():
    return DesertSurvivalExpedition()


if __name__ == "__main__":
    game = create_game()
    game.travel()
    game.find_oasis()
    game.rest()
    print(game.status())
