from dataclasses import dataclass
from typing import Dict


@dataclass
class JungleExplorer:
    name: str
    health: int = 100
    stamina: int = 100
    supplies: int = 80
    relics: int = 0


class JungleRuinsExplorer:
    def __init__(self):
        self.explorer = JungleExplorer("Tara Venn")
        self.location = "Jungle Edge"
        self.score = 0
        self.ruins_unlocked = False

        self.locations: Dict[str, int] = {
            "Jungle Edge": 0,
            "Stone Bridge": 20,
            "Sun Temple": 40,
            "Hidden Ruins": 70,
        }

    def travel(self, location: str):
        if location not in self.locations:
            return False

        cost = max(5, self.locations[location] // 4)

        if self.explorer.stamina < cost:
            return False

        self.explorer.stamina -= cost
        self.explorer.supplies -= 3
        self.location = location
        self.score += cost
        return True

    def search_ruins(self):
        if self.location not in (
            "Sun Temple",
            "Hidden Ruins",
        ):
            return False

        if self.explorer.stamina < 10:
            return False

        self.explorer.stamina -= 10
        self.explorer.relics += 1
        self.score += 80
        return True

    def solve_inscription(self, answer: int):
        if answer != 42:
            self.score = max(0, self.score - 20)
            self.explorer.stamina -= 5
            return False

        self.ruins_unlocked = True
        self.score += 120
        return True

    def recover(self):
        self.explorer.stamina = min(
            100,
            self.explorer.stamina + 25
        )
        self.explorer.supplies = max(
            0,
            self.explorer.supplies - 5
        )

    def status(self):
        return {
            "explorer": self.explorer.name,
            "location": self.location,
            "stamina": self.explorer.stamina,
            "supplies": self.explorer.supplies,
            "relics": self.explorer.relics,
            "score": self.score,
            "ruins_unlocked": self.ruins_unlocked,
        }


def create_game():
    return JungleRuinsExplorer()


def demo():
    game = create_game()
    game.travel("Stone Bridge")
    game.travel("Sun Temple")
    game.search_ruins()
    game.solve_inscription(42)
    game.travel("Hidden Ruins")
    game.search_ruins()
    return game.status()


if __name__ == "__main__":
    print(demo())
