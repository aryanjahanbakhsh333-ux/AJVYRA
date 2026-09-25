from dataclasses import dataclass


@dataclass
class Colony:
    name: str
    population: int = 500
    food: int = 600
    oxygen: int = 700
    energy: int = 500
    happiness: int = 60
    defense: int = 30


class SpaceColonyGovernor:
    def __init__(self):
        self.governor = "Liora Venn"
        self.colony = Colony("Nova Haven")
        self.credits = 800
        self.day = 1
        self.score = 0
        self.level = 1

    def build(self, building: str):
        costs = {
            "farm": 120,
            "oxygen_lab": 180,
            "solar_array": 200,
            "habitat": 250,
            "defense_grid": 220,
        }

        if building not in costs or self.credits < costs[building]:
            return False

        self.credits -= costs[building]

        if building == "farm":
            self.colony.food += 300
        elif building == "oxygen_lab":
            self.colony.oxygen += 350
        elif building == "solar_array":
            self.colony.energy += 300
        elif building == "habitat":
            self.colony.population += 150
            self.colony.happiness += 8
        elif building == "defense_grid":
            self.colony.defense += 25

        self.score += costs[building] // 2
        return True

    def distribute_food(self):
        if self.colony.food < 100:
            return False

        self.colony.food -= 100
        self.colony.happiness = min(
            100,
            self.colony.happiness + 8
        )
        self.score += 25
        return True

    def generate_energy(self):
        if self.colony.energy < 50:
            return False

        self.colony.energy += 120
        self.score += 20
        return True

    def improve_defense(self):
        if self.credits < 100:
            return False

        self.credits -= 100
        self.colony.defense += 12
        self.score += 30
        return True

    def advance_day(self):
        self.day += 1

        self.colony.food = max(
            0,
            self.colony.food - self.colony.population // 5
        )
        self.colony.oxygen = max(
            0,
            self.colony.oxygen - self.colony.population // 4
        )
        self.colony.energy = max(
            0,
            self.colony.energy - self.colony.population // 6
        )

        self.credits += self.colony.population // 10

        if self.score >= self.level * 600:
            self.level += 1

    def status(self):
        return {
            "governor": self.governor,
            "colony": self.colony.name,
            "day": self.day,
            "level": self.level,
            "population": self.colony.population,
            "food": self.colony.food,
            "oxygen": self.colony.oxygen,
            "energy": self.colony.energy,
            "happiness": self.colony.happiness,
            "defense": self.colony.defense,
            "credits": self.credits,
            "score": self.score,
        }


def create_game():
    return SpaceColonyGovernor()


if __name__ == "__main__":
    game = create_game()
    game.build("farm")
    game.build("oxygen_lab")
    game.build("solar_array")
    game.distribute_food()
    game.advance_day()
    print(game.status())
