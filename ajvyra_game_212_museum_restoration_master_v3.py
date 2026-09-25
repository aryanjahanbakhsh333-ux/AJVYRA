from dataclasses import dataclass
from typing import List


@dataclass
class Artifact:
    name: str
    condition: int
    rarity: int
    restored: bool = False


class MuseumRestorationMaster:
    def __init__(self):
        self.curator = "Elian Ro"
        self.money = 300
        self.reputation = 10
        self.score = 0

        self.artifacts: List[Artifact] = [
            Artifact("Golden Mask", 45, 5),
            Artifact("Ancient Vase", 60, 3),
            Artifact("Royal Compass", 35, 4),
            Artifact("Crystal Statue", 50, 5),
        ]

    def inspect(self, index: int):
        if not 0 <= index < len(self.artifacts):
            return False

        artifact = self.artifacts[index]
        self.score += artifact.rarity * 5
        return artifact.condition

    def restore(self, index: int):
        if not 0 <= index < len(self.artifacts):
            return False

        artifact = self.artifacts[index]

        if artifact.restored:
            return False

        cost = max(20, (100 - artifact.condition) * 2)

        if self.money < cost:
            return False

        self.money -= cost
        artifact.condition = 100
        artifact.restored = True

        self.reputation += artifact.rarity * 2
        self.score += artifact.rarity * 30

        return True

    def exhibit(self, index: int):
        if not 0 <= index < len(self.artifacts):
            return False

        artifact = self.artifacts[index]

        if not artifact.restored:
            return False

        self.money += artifact.rarity * 25
        self.reputation += artifact.rarity
        self.score += artifact.rarity * 20
        return True

    def museum_level(self):
        return 1 + self.reputation // 20

    def status(self):
        return {
            "curator": self.curator,
            "money": self.money,
            "reputation": self.reputation,
            "museum_level": self.museum_level(),
            "score": self.score,
            "restored": sum(
                artifact.restored
                for artifact in self.artifacts
            ),
        }


def create_game():
    return MuseumRestorationMaster()


def demo():
    game = create_game()

    for index in range(4):
        game.inspect(index)
        game.restore(index)
        game.exhibit(index)

    return game.status()


if __name__ == "__main__":
    print(demo())
