from dataclasses import dataclass


@dataclass
class Dragon:
    name: str
    speed: int
    endurance: int
    loyalty: int = 50
    energy: int = 100


@dataclass
class Letter:
    destination: str
    importance: int
    delivered: bool = False


class FantasyDragonPostmaster:
    def __init__(self):
        self.postmaster = "Eryn Vale"
        self.dragon = Dragon("Astra", 80, 75)
        self.gold = 150
        self.score = 0
        self.reputation = 20
        self.distance = 0
        self.deliveries = 0

        self.mail = [
            Letter("Moon Village", 20),
            Letter("Crystal Harbor", 40),
            Letter("Storm Castle", 70),
            Letter("Sky Monastery", 100),
        ]

    def fly(self, distance: int):
        if distance <= 0:
            return False

        energy_cost = max(5, distance // 10)

        if self.dragon.energy < energy_cost:
            return False

        self.dragon.energy -= energy_cost
        self.distance += distance
        self.score += distance // 2
        return True

    def deliver_letter(self, index: int):
        if not 0 <= index < len(self.mail):
            return False

        letter = self.mail[index]

        if letter.delivered or self.dragon.energy < 10:
            return False

        self.dragon.energy -= 10
        letter.delivered = True
        self.deliveries += 1
        self.gold += letter.importance
        self.reputation += letter.importance // 10
        self.score += letter.importance * 2
        return True

    def bond_with_dragon(self):
        if self.gold < 20:
            return False

        self.gold -= 20
        self.dragon.loyalty = min(100, self.dragon.loyalty + 10)
        self.dragon.endurance += 3
        self.score += 25
        return True

    def rest(self):
        self.dragon.energy = min(
            100,
            self.dragon.energy + 35
        )

    def status(self):
        return {
            "postmaster": self.postmaster,
            "dragon": self.dragon.name,
            "dragon_energy": self.dragon.energy,
            "loyalty": self.dragon.loyalty,
            "gold": self.gold,
            "reputation": self.reputation,
            "deliveries": self.deliveries,
            "score": self.score,
        }


def create_game():
    return FantasyDragonPostmaster()


if __name__ == "__main__":
    game = create_game()
    game.fly(100)
    game.deliver_letter(0)
    game.bond_with_dragon()
    print(game.status())
