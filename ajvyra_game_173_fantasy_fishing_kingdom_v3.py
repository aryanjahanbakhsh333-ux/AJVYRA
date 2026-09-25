"""
AJVYRA 173 — Fantasy Fishing Kingdom
Genre: Fishing / Fantasy / Collection
"""

from dataclasses import dataclass


@dataclass
class Fish:
    name: str
    rarity: int
    value: int
    difficulty: int


class FantasyFishingKingdom:
    title = "Fantasy Fishing Kingdom"
    angler_name = "Finn Marrow"

    def __init__(self):
        self.energy = 100
        self.gold = 500
        self.score = 0
        self.caught = []

        self.fish = [
            Fish("Moon Carp", 1, 30, 25),
            Fish("Crystal Pike", 2, 70, 45),
            Fish("Storm Eel", 3, 140, 65),
            Fish("Royal Leviathan", 5, 500, 90),
        ]

    def cast(self, fish_name):
        target = next(
            (
                f for f in self.fish
                if f.name == fish_name
            ),
            None,
        )

        if target is None or self.energy < 12:
            return False

        self.energy -= 12

        if target.difficulty <= 75:
            self.caught.append(target.name)
            self.gold += target.value
            self.score += target.value * target.rarity
            return True

        return False

    def bait_upgrade(self):
        if self.gold < 150:
            return False

        self.gold -= 150

        for fish in self.fish:
            fish.difficulty = max(
                10,
                fish.difficulty - 5,
            )

        return True

    def rest(self):
        self.energy = min(
            100,
            self.energy + 35,
        )

    def sell_collection(self):
        if not self.caught:
            return 0

        value = len(self.caught) * 50
        self.gold += value
        self.score += value
        self.caught.clear()
        return value

    def status(self):
        return {
            "angler": self.angler_name,
            "energy": self.energy,
            "gold": self.gold,
            "score": self.score,
            "caught": list(self.caught),
        }


def create_game():
    return FantasyFishingKingdom()


if __name__ == "__main__":
    game = create_game()
    game.cast("Moon Carp")
    game.cast("Crystal Pike")
    print(game.status())
