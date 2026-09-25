"""
AJVYRA 124 — Wildlife Rescue
Genre: Wildlife Rescue / Simulation
"""

from dataclasses import dataclass


@dataclass
class Animal:
    name: str
    species: str
    stress: int
    health: int
    habitat: str
    rescued: bool = False


class WildlifeRescue:
    title = "Wildlife Rescue"
    ranger = "Ayla Fern"

    def __init__(self):
        self.animals = [
            Animal(
                "Kiro",
                "fox",
                70,
                55,
                "forest",
            ),
            Animal(
                "Mavi",
                "eagle",
                60,
                65,
                "mountain",
            ),
            Animal(
                "Noro",
                "deer",
                80,
                45,
                "forest",
            ),
            Animal(
                "Sia",
                "otter",
                50,
                70,
                "river",
            ),
        ]

        self.supplies = 100
        self.reputation = 0
        self.score = 0

    def calm(self, animal_name):
        animal = self._find(animal_name)

        if not animal or animal.rescued:
            return False

        if self.supplies < 5:
            return False

        self.supplies -= 5
        animal.stress = max(0, animal.stress - 25)
        self.score += 20
        return True

    def treat(self, animal_name):
        animal = self._find(animal_name)

        if not animal or animal.rescued:
            return False

        if self.supplies < 15:
            return False

        self.supplies -= 15
        animal.health = min(100, animal.health + 30)
        self.score += 35
        return True

    def release(self, animal_name):
        animal = self._find(animal_name)

        if not animal:
            return False

        if animal.health >= 75 and animal.stress <= 30:
            animal.rescued = True
            self.reputation += 10
            self.score += 100
            return True

        return False

    def _find(self, name):
        return next(
            (
                animal
                for animal in self.animals
                if animal.name.lower() == name.lower()
            ),
            None,
        )

    def status(self):
        return {
            "ranger": self.ranger,
            "supplies": self.supplies,
            "reputation": self.reputation,
            "score": self.score,
            "animals": [
                {
                    "name": a.name,
                    "species": a.species,
                    "stress": a.stress,
                    "health": a.health,
                    "habitat": a.habitat,
                    "released": a.rescued,
                }
                for a in self.animals
            ],
        }


def create_game():
    return WildlifeRescue()


if __name__ == "__main__":
    game = create_game()
    game.calm("Kiro")
    game.treat("Kiro")
    game.release("Kiro")
    print(game.status())
