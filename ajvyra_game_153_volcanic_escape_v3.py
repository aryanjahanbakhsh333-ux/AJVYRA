"""
AJVYRA 153 — Volcanic Escape
Genre: Action / Survival
"""

from dataclasses import dataclass


@dataclass
class Explorer:
    name: str
    stamina: int = 100
    health: int = 100
    heat_resistance: int = 60


class VolcanicEscape:
    title = "Volcanic Escape"
    explorer_name = "Rae Kest"

    def __init__(self):
        self.player = Explorer(
            self.explorer_name
        )
        self.distance = 100
        self.supplies = 5
        self.score = 0
        self.escaped = False

    def run(self):
        if self.player.stamina < 15:
            return False

        self.player.stamina -= 15

        progress = (
            12
            + self.player.stamina // 20
            + self.player.heat_resistance // 20
        )

        self.distance = max(
            0,
            self.distance - progress,
        )

        self.player.health = max(
            0,
            self.player.health - 4,
        )

        self.score += progress * 10

        if self.distance == 0:
            self.escaped = True

        return True

    def drink(self):
        if self.supplies <= 0:
            return False

        self.supplies -= 1
        self.player.stamina = min(
            100,
            self.player.stamina + 30,
        )
        return True

    def shield_from_heat(self):
        self.player.heat_resistance = min(
            100,
            self.player.heat_resistance + 12,
        )

    def status(self):
        return {
            "explorer": self.player.name,
            "distance": self.distance,
            "health": self.player.health,
            "stamina": self.player.stamina,
            "supplies": self.supplies,
            "heat_resistance": self.player.heat_resistance,
            "score": self.score,
            "escaped": self.escaped,
        }


def create_game():
    return VolcanicEscape()


if __name__ == "__main__":
    game = create_game()

    for _ in range(3):
        game.run()

    game.drink()
    print(game.status())
