from dataclasses import dataclass


@dataclass
class Kingdom:
    name: str
    population: int = 800
    food: int = 500
    gold: int = 700
    happiness: int = 60
    defense: int = 40
    magic: int = 30


class FantasyKingdomArchitect:
    def __init__(self):
        self.ruler = "Elara Vey"
        self.kingdom = Kingdom("Aurelia")
        self.day = 1
        self.score = 0
        self.level = 1

    def build_farm(self):
        if self.kingdom.gold < 100:
            return False

        self.kingdom.gold -= 100
        self.kingdom.food += 180
        self.score += 50
        return True

    def build_castle(self):
        if self.kingdom.gold < 250:
            return False

        self.kingdom.gold -= 250
        self.kingdom.defense += 20
        self.kingdom.happiness += 5
        self.score += 120
        return True

    def build_magic_tower(self):
        if self.kingdom.gold < 300:
            return False

        self.kingdom.gold -= 300
        self.kingdom.magic += 25
        self.score += 150
        return True

    def festival(self):
        if self.kingdom.food < 80:
            return False

        self.kingdom.food -= 80
        self.kingdom.happiness = min(
            100,
            self.kingdom.happiness + 15
        )
        self.score += 70
        return True

    def collect_taxes(self):
        income = self.kingdom.population // 8
        self.kingdom.gold += income
        self.score += income
        return income

    def advance_day(self):
        self.day += 1
        self.kingdom.food = max(
            0,
            self.kingdom.food - self.kingdom.population // 12
        )

        self.collect_taxes()

        if self.score >= self.level * 700:
            self.level += 1

    def status(self):
        return {
            "ruler": self.ruler,
            "kingdom": self.kingdom.name,
            "day": self.day,
            "level": self.level,
            "population": self.kingdom.population,
            "food": self.kingdom.food,
            "gold": self.kingdom.gold,
            "happiness": self.kingdom.happiness,
            "defense": self.kingdom.defense,
            "magic": self.kingdom.magic,
            "score": self.score,
        }


def create_game():
    return FantasyKingdomArchitect()


if __name__ == "__main__":
    game = create_game()
    game.build_farm()
    game.build_castle()
    game.build_magic_tower()
    game.advance_day()
    print(game.status())
