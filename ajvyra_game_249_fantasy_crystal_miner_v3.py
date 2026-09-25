from dataclasses import dataclass


@dataclass
class Crystal:
    name: str
    hardness: int
    value: int
    magical_power: int


class FantasyCrystalMiner:
    def __init__(self):
        self.miner = "Daren Flint"
        self.energy = 100
        self.gold = 100
        self.score = 0
        self.depth = 0
        self.pickaxe_level = 1
        self.crystals = []

        self.available = [
            Crystal("Azure Shard", 20, 30, 10),
            Crystal("Ruby Core", 40, 60, 25),
            Crystal("Moon Crystal", 60, 100, 45),
            Crystal("Dragon Crystal", 90, 180, 80),
        ]

    def descend(self, amount: int):
        if amount <= 0 or self.energy < amount // 10:
            return False

        self.energy -= amount // 10
        self.depth += amount
        self.score += amount // 2
        return True

    def mine(self, index: int):
        if not 0 <= index < len(self.available):
            return False

        crystal = self.available[index]
        required = max(5, crystal.hardness // 10)

        if self.energy < required:
            return False

        self.energy -= required

        power = self.pickaxe_level * 30

        if power < crystal.hardness:
            return False

        self.crystals.append(crystal)
        self.score += crystal.value
        return True

    def sell_crystals(self):
        if not self.crystals:
            return False

        value = sum(c.value for c in self.crystals)
        self.gold += value
        self.crystals.clear()
        self.score += value // 2
        return True

    def upgrade_pickaxe(self):
        cost = self.pickaxe_level * 100

        if self.gold < cost:
            return False

        self.gold -= cost
        self.pickaxe_level += 1
        self.score += 30
        return True

    def rest(self):
        self.energy = min(100, self.energy + 35)

    def status(self):
        return {
            "miner": self.miner,
            "energy": self.energy,
            "depth": self.depth,
            "pickaxe_level": self.pickaxe_level,
            "gold": self.gold,
            "crystals": len(self.crystals),
            "score": self.score,
        }


def create_game():
    return FantasyCrystalMiner()


if __name__ == "__main__":
    game = create_game()
    game.descend(100)
    game.mine(0)
    game.sell_crystals()
    print(game.status())
