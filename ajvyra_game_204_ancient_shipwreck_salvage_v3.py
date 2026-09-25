from dataclasses import dataclass
from typing import List


@dataclass
class Diver:
    name: str
    oxygen: int = 100
    depth_limit: int = 80
    stamina: int = 100
    cargo: int = 0


@dataclass
class Artifact:
    name: str
    depth: int
    value: int
    recovered: bool = False


class AncientShipwreckSalvage:
    def __init__(self):
        self.diver = Diver("Soren Kai")
        self.depth = 0
        self.money = 100
        self.score = 0

        self.artifacts: List[Artifact] = [
            Artifact("Bronze Compass", 30, 80),
            Artifact("Royal Coin", 45, 120),
            Artifact("Glass Crown", 60, 180),
            Artifact("Captain's Seal", 75, 250),
        ]

    def dive(self, target_depth: int):
        if target_depth <= 0 or target_depth > self.diver.depth_limit:
            return False

        oxygen_cost = target_depth // 8

        if self.diver.oxygen < oxygen_cost:
            return False

        self.diver.oxygen -= oxygen_cost
        self.diver.stamina -= target_depth // 15
        self.depth = target_depth
        self.score += target_depth
        return True

    def recover_artifact(self, name: str):
        for artifact in self.artifacts:
            if artifact.name != name or artifact.recovered:
                continue

            if self.depth < artifact.depth:
                return False

            if self.diver.cargo >= 5:
                return False

            artifact.recovered = True
            self.diver.cargo += 1
            self.score += artifact.value
            return True

        return False

    def return_surface(self):
        self.depth = 0
        self.diver.oxygen = min(
            100,
            self.diver.oxygen + 35
        )
        self.diver.stamina = min(
            100,
            self.diver.stamina + 25
        )

    def sell_cargo(self):
        recovered = [
            a for a in self.artifacts if a.recovered
        ]

        if not recovered:
            return False

        total = sum(a.value for a in recovered)
        self.money += total
        self.diver.cargo = 0
        self.score += total // 2
        return total

    def status(self):
        return {
            "diver": self.diver.name,
            "depth": self.depth,
            "oxygen": self.diver.oxygen,
            "stamina": self.diver.stamina,
            "cargo": self.diver.cargo,
            "money": self.money,
            "score": self.score,
            "artifacts": sum(
                a.recovered for a in self.artifacts
            ),
        }


def create_game():
    return AncientShipwreckSalvage()


def demo():
    game = create_game()
    game.dive(45)
    game.recover_artifact("Royal Coin")
    game.return_surface()
    game.dive(60)
    game.recover_artifact("Glass Crown")
    game.return_surface()
    game.sell_cargo()

    return game.status()


if __name__ == "__main__":
    print(demo())
