"""
AJVYRA 148 — Island Survivor
Genre: Survival / Exploration
"""

from dataclasses import dataclass


@dataclass
class Survivor:
    name: str
    health: int = 100
    energy: int = 100
    morale: int = 75


class IslandSurvivor:
    title = "Island Survivor"
    survivor_name = "Noa Reef"

    def __init__(self):
        self.day = 1
        self.water = 70
        self.food = 60
        self.wood = 50
        self.score = 0

        self.player = Survivor(
            self.survivor_name
        )

    def gather(self):
        self.energy_cost(10)

        self.wood += 20
        self.food += 8
        self.score += 30

    def build_shelter(self):
        if self.wood < 30:
            return False

        self.wood -= 30
        self.player.morale = min(
            100,
            self.player.morale + 10,
        )
        self.score += 75
        return True

    def find_water(self):
        if self.player.energy < 10:
            return False

        self.player.energy -= 10
        self.water += 35
        self.score += 25
        return True

    def energy_cost(self, amount):
        self.player.energy = max(
            0,
            self.player.energy - amount,
        )

    def survive_day(self):
        self.food = max(
            0,
            self.food - 10,
        )

        self.water = max(
            0,
            self.water - 12,
        )

        self.player.energy = max(
            0,
            self.player.energy - 5,
        )

        if self.food == 0:
            self.player.health = max(
                0,
                self.player.health - 10,
            )

        if self.water == 0:
            self.player.health = max(
                0,
                self.player.health - 15,
            )

        self.day += 1

    def rest(self):
        self.player.energy = min(
            100,
            self.player.energy + 35,
        )

    def status(self):
        return {
            "survivor": self.survivor_name,
            "day": self.day,
            "health": self.player.health,
            "energy": self.player.energy,
            "morale": self.player.morale,
            "water": self.water,
            "food": self.food,
            "wood": self.wood,
            "score": self.score,
        }


def create_game():
    return IslandSurvivor()


if __name__ == "__main__":
    game = create_game()
    game.gather()
    game.find_water()
    game.build_shelter()
    game.survive_day()
    print(game.status())
