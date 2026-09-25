from dataclasses import dataclass
from typing import Dict


@dataclass
class Explorer:
    name: str
    stamina: int = 100
    heat_resistance: int = 60
    supplies: int = 80
    discoveries: int = 0


class VolcanicIslandExpedition:
    def __init__(self):
        self.hero = Explorer("Riven Kael")
        self.location = "Coastal Camp"
        self.day = 1
        self.score = 0
        self.reputation = 0

        self.locations: Dict[str, int] = {
            "Coastal Camp": 0,
            "Ash Valley": 20,
            "Obsidian Ridge": 35,
            "Lava Observatory": 50,
            "Ancient Crater": 70,
        }

    def travel(self, destination: str):
        if destination not in self.locations:
            return False

        distance = self.locations[destination]
        stamina_cost = max(5, distance // 2)

        if self.hero.stamina < stamina_cost:
            return False

        self.hero.stamina -= stamina_cost
        self.hero.supplies -= max(2, distance // 10)
        self.location = destination
        self.score += distance
        return True

    def survey(self):
        if self.hero.stamina < 8:
            return False

        self.hero.stamina -= 8
        self.hero.discoveries += 1
        self.hero.supplies -= 3
        self.score += 35
        self.reputation += 2
        return True

    def collect_obsidian(self):
        if self.location not in ("Obsidian Ridge", "Ancient Crater"):
            return False

        if self.hero.stamina < 12:
            return False

        self.hero.stamina -= 12
        self.score += 60
        self.reputation += 3
        return True

    def rest(self):
        self.day += 1
        self.hero.stamina = min(100, self.hero.stamina + 30)
        self.hero.supplies = max(0, self.hero.supplies - 5)

    def expedition_complete(self):
        return (
            self.hero.discoveries >= 4
            and self.hero.reputation >= 8
        )

    def status(self):
        return {
            "hero": self.hero.name,
            "location": self.location,
            "day": self.day,
            "stamina": self.hero.stamina,
            "supplies": self.hero.supplies,
            "discoveries": self.hero.discoveries,
            "reputation": self.reputation,
            "score": self.score,
            "complete": self.expedition_complete(),
        }


def create_game():
    return VolcanicIslandExpedition()


def demo():
    game = create_game()
    game.travel("Ash Valley")
    game.survey()
    game.travel("Obsidian Ridge")
    game.survey()
    game.collect_obsidian()
    game.rest()
    return game.status()


if __name__ == "__main__":
    print(demo())
