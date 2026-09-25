from dataclasses import dataclass


@dataclass
class Kingdom:
    name: str
    population: int = 1000
    happiness: int = 60
    defense: int = 40
    food: int = 500
    magic: int = 30


class FantasyKingdomArchitect:
    def __init__(self):
        self.ruler = "Aren Sol"
        self.kingdom = Kingdom("Elarion")
        self.gold = 600
        self.day = 1
        self.score = 0
        self.level = 1

    def build(self, building: str):
        costs = {
            "farm": 100,
            "castle": 250,
            "library": 180,
            "magic_tower": 300,
            "market": 150,
        }

        if building not in costs or self.gold < costs[building]:
            return False

        self.gold -= costs[building]

        if building == "farm":
            self.kingdom.food += 250
            self.kingdom.population += 100
        elif building == "castle":
            self.kingdom.defense += 25
        elif building == "library":
            self.kingdom.happiness += 10
            self.kingdom.magic += 10
        elif building == "magic_tower":
            self.kingdom.magic += 30
        elif building == "market":
            self.gold += 80
            self.kingdom.happiness += 5

        self.score += costs[building] // 2
        return True

    def organize_festival(self):
        if self.gold < 80 or self.kingdom.food < 100:
            return False

        self.gold -= 80
        self.kingdom.food -= 100
        self.kingdom.happiness = min(100, self.kingdom.happiness + 20)
        self.score += 40
        return True

    def train_guard(self):
        if self.gold < 100:
            return False

        self.gold -= 100
        self.kingdom.defense += 15
        self.score += 35
        return True

    def advance_day(self):
        self.day += 1
        self.kingdom.food = max(
            0,
            self.kingdom.food - self.kingdom.population // 20
        )

        self.gold += self.kingdom.population // 100
        self.kingdom.happiness = max(
            0,
            self.kingdom.happiness - 2
        )

        if self.score >= self.level * 500:
            self.level += 1

    def status(self):
        return {
            "ruler": self.ruler,
            "kingdom": self.kingdom.name,
            "day": self.day,
            "level": self.level,
            "gold": self.gold,
            "score": self.score,
            "population": self.kingdom.population,
            "happiness": self.kingdom.happiness,
            "defense": self.kingdom.defense,
            "food": self.kingdom.food,
            "magic": self.kingdom.magic,
        }


def create_game():
    return FantasyKingdomArchitect()


if __name__ == "__main__":
    game = create_game()
    game.build("farm")
    game.build("castle")
    game.organize_festival()
    print(game.status())
