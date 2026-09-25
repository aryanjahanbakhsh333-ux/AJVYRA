from dataclasses import dataclass


@dataclass
class TimeCapsule:
    name: str
    era: int
    rarity: int
    discovered: bool = False


class TimeCapsuleArchaeologist:
    def __init__(self):
        self.archaeologist = "Iris Quinn"
        self.year = 2120
        self.energy = 100
        self.score = 0
        self.reputation = 20
        self.capsules = [
            TimeCapsule("Silver Box", 1985, 20),
            TimeCapsule("School Memory", 2025, 35),
            TimeCapsule("Future Journal", 2080, 60),
            TimeCapsule("Unknown Capsule", 2140, 100),
        ]
        self.discovered = 0

    def scan(self):
        if self.energy < 10:
            return False

        self.energy -= 10
        self.score += 15
        return True

    def excavate(self, index: int):
        if index < 0 or index >= len(self.capsules):
            return False

        capsule = self.capsules[index]

        if capsule.discovered or self.energy < 15:
            return False

        self.energy -= 15
        capsule.discovered = True
        self.discovered += 1
        self.score += capsule.rarity
        return True

    def analyze(self, index: int):
        if index < 0 or index >= len(self.capsules):
            return False

        capsule = self.capsules[index]

        if not capsule.discovered:
            return False

        self.energy -= 5
        self.reputation += capsule.rarity // 10
        self.score += capsule.rarity * 2
        return True

    def restore_energy(self):
        self.energy = min(100, self.energy + 30)

    def complete_collection(self):
        if self.discovered == len(self.capsules):
            self.score += 300
            self.reputation += 50
            return True
        return False

    def status(self):
        return {
            "archaeologist": self.archaeologist,
            "year": self.year,
            "energy": self.energy,
            "score": self.score,
            "reputation": self.reputation,
            "discovered": self.discovered,
            "total": len(self.capsules),
        }


def create_game():
    return TimeCapsuleArchaeologist()


if __name__ == "__main__":
    game = create_game()
    game.scan()
    game.excavate(0)
    game.analyze(0)
    print(game.status())
