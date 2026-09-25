"""
AJVYRA 113 — Volcano Researcher
Genre: Exploration / Risk Management
"""

from dataclasses import dataclass
from random import randint


@dataclass
class Researcher:
    name: str
    heat_protection: int = 100
    stamina: int = 100
    samples: int = 0


class VolcanoResearcher:
    title = "Volcano Researcher"
    researcher = "Kaia Ember"

    def __init__(self):
        self.player = Researcher(self.researcher)
        self.altitude = 0
        self.temperature = 35
        self.activity = 20
        self.score = 0
        self.research_data = []
        self.log = []

    def climb(self):
        if self.player.stamina < 10:
            self.log.append("Too exhausted to climb.")
            return False

        self.altitude += 10
        self.player.stamina -= 10
        self.temperature += randint(2, 7)
        self.activity += randint(0, 5)
        return True

    def collect_sample(self):
        if self.altitude < 30:
            self.log.append("The research zone has not been reached.")
            return False

        if self.player.heat_protection < 20:
            self.log.append("Heat protection is too low.")
            return False

        self.player.heat_protection -= 15
        self.player.samples += 1
        self.score += 75
        self.research_data.append(
            {
                "altitude": self.altitude,
                "temperature": self.temperature,
                "activity": self.activity,
            }
        )
        return True

    def cool_down(self):
        self.temperature = max(20, self.temperature - 8)
        self.player.stamina = min(100, self.player.stamina + 20)

    def retreat(self):
        self.altitude = max(0, self.altitude - 20)
        self.temperature = max(20, self.temperature - 10)
        self.player.stamina = min(100, self.player.stamina + 10)

    def eruption_warning(self):
        return self.activity >= 70

    def status(self):
        return {
            "researcher": self.researcher,
            "altitude": self.altitude,
            "temperature": self.temperature,
            "volcanic_activity": self.activity,
            "heat_protection": self.player.heat_protection,
            "stamina": self.player.stamina,
            "samples": self.player.samples,
            "score": self.score,
            "eruption_warning": self.eruption_warning(),
        }


def create_game():
    return VolcanoResearcher()


if __name__ == "__main__":
    game = create_game()

    for _ in range(4):
        game.climb()

    game.collect_sample()
    print(game.status())
