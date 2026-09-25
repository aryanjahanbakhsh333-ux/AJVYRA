from dataclasses import dataclass


@dataclass
class Diver:
    name: str
    oxygen: int = 100
    stamina: int = 100
    exploration: int = 60
    sonar: int = 50


class UnderwaterAncientCityExplorer:
    def __init__(self):
        self.explorer = Diver("Aris Tide")
        self.depth = 0
        self.distance = 0
        self.artifacts = 0
        self.score = 0
        self.coins = 100
        self.city_sector = "Outer Ruins"
        self.completed = False

    def dive(self, depth: int):
        if depth <= 0 or self.explorer.oxygen < depth // 20:
            return False

        self.depth += depth
        self.explorer.oxygen -= max(5, depth // 20)
        self.explorer.stamina -= 5
        self.score += depth // 2
        return True

    def explore_sector(self, sector: str):
        if self.explorer.stamina < 15:
            return False

        self.explorer.stamina -= 15
        self.city_sector = sector
        self.distance += 50
        self.score += 30
        return True

    def scan_ruins(self):
        if self.explorer.sonar < 10:
            return False

        self.explorer.sonar -= 10
        self.score += 25
        return True

    def recover_artifact(self):
        if self.depth < 300 or self.explorer.stamina < 20:
            return False

        self.explorer.stamina -= 20
        self.artifacts += 1
        self.coins += 50
        self.score += 100
        return True

    def surface(self):
        self.depth = max(0, self.depth - 400)
        self.explorer.oxygen = min(100, self.explorer.oxygen + 40)
        self.explorer.stamina = min(100, self.explorer.stamina + 25)

    def complete_expedition(self):
        if self.artifacts >= 5:
            self.completed = True
            self.score += 300
            return True
        return False

    def status(self):
        return {
            "explorer": self.explorer.name,
            "sector": self.city_sector,
            "depth": self.depth,
            "oxygen": self.explorer.oxygen,
            "stamina": self.explorer.stamina,
            "artifacts": self.artifacts,
            "coins": self.coins,
            "score": self.score,
            "completed": self.completed,
        }


def create_game():
    return UnderwaterAncientCityExplorer()


if __name__ == "__main__":
    game = create_game()
    game.dive(300)
    game.scan_ruins()
    game.explore_sector("Royal District")
    game.recover_artifact()
    game.surface()
    print(game.status())
