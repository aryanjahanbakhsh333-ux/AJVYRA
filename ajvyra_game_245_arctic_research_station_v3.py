from dataclasses import dataclass


@dataclass
class ResearchSystem:
    name: str
    condition: int = 100
    efficiency: int = 70


class ArcticResearchStation:
    def __init__(self):
        self.scientist = "Nora Ice"
        self.temperature = -25
        self.food = 100
        self.energy = 100
        self.data = 0
        self.score = 0
        self.day = 1

        self.systems = [
            ResearchSystem("Weather Scanner"),
            ResearchSystem("Ice Core Lab"),
            ResearchSystem("Satellite Link"),
            ResearchSystem("Heating System"),
        ]

    def collect_ice_core(self):
        if self.energy < 20:
            return False

        self.energy -= 20
        self.data += 30
        self.score += 50
        return True

    def analyze_data(self):
        if self.data < 20 or self.energy < 10:
            return False

        self.data -= 20
        self.energy -= 10
        self.score += 70
        return True

    def repair_system(self, index: int):
        if not 0 <= index < len(self.systems):
            return False

        system = self.systems[index]

        if self.energy < 15:
            return False

        self.energy -= 15
        system.condition = min(100, system.condition + 25)
        system.efficiency = min(100, system.efficiency + 5)
        self.score += 30
        return True

    def generate_power(self):
        heating = self.systems[3]

        if heating.condition < 30:
            self.temperature -= 5
            return False

        self.energy = min(100, self.energy + 30)
        self.temperature = min(-10, self.temperature + 2)
        self.score += 20
        return True

    def survive_day(self):
        self.day += 1
        self.food = max(0, self.food - 8)
        self.energy = max(0, self.energy - 10)

        for system in self.systems:
            system.condition = max(
                0,
                system.condition - 2
            )

    def status(self):
        return {
            "scientist": self.scientist,
            "day": self.day,
            "temperature": self.temperature,
            "food": self.food,
            "energy": self.energy,
            "data": self.data,
            "score": self.score,
        }


def create_game():
    return ArcticResearchStation()


if __name__ == "__main__":
    game = create_game()
    game.collect_ice_core()
    game.analyze_data()
    game.repair_system(0)
    print(game.status())
