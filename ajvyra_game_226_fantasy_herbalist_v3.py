from dataclasses import dataclass


@dataclass
class Herb:
    name: str
    rarity: int
    healing: int
    value: int


class FantasyHerbalist:
    def __init__(self):
        self.herbalist = "Elara Moss"
        self.energy = 100
        self.reputation = 20
        self.gold = 120
        self.level = 1
        self.score = 0
        self.inventory = {}
        self.discovered = 0

        self.herbs = [
            Herb("Moonleaf", 20, 15, 25),
            Herb("Ember Root", 35, 30, 45),
            Herb("Frost Mint", 50, 40, 70),
            Herb("Dragon Bloom", 80, 70, 150),
        ]

    def gather(self, herb_name: str):
        herb = next(
            (h for h in self.herbs if h.name == herb_name),
            None
        )

        if herb is None or self.energy < 12:
            return False

        self.energy -= 12
        self.inventory[herb.name] = self.inventory.get(herb.name, 0) + 1
        self.score += herb.rarity
        self.discovered += 1
        return True

    def brew(self, herb_name: str):
        if self.inventory.get(herb_name, 0) <= 0:
            return False

        herb = next(h for h in self.herbs if h.name == herb_name)

        self.inventory[herb.name] -= 1
        self.gold += herb.value
        self.reputation += herb.rarity // 10
        self.score += herb.healing * 2

        if self.score >= self.level * 300:
            self.level += 1

        return True

    def study(self):
        if self.energy < 10:
            return False

        self.energy -= 10
        self.reputation += 5
        self.score += 20
        return True

    def rest(self):
        self.energy = min(100, self.energy + 35)

    def status(self):
        return {
            "herbalist": self.herbalist,
            "level": self.level,
            "energy": self.energy,
            "gold": self.gold,
            "reputation": self.reputation,
            "score": self.score,
            "discovered": self.discovered,
            "inventory": dict(self.inventory),
        }


def create_game():
    return FantasyHerbalist()


if __name__ == "__main__":
    game = create_game()
    game.gather("Moonleaf")
    game.brew("Moonleaf")
    game.study()
    print(game.status())
