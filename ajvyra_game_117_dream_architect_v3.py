"""
AJVYRA 117 — Dream Architect
Genre: Creative World Building
"""

from dataclasses import dataclass


@dataclass
class DreamElement:
    name: str
    energy_cost: int
    stability: int


class DreamArchitect:
    title = "Dream Architect"
    architect = "Aeris Vonn"

    def __init__(self):
        self.energy = 100
        self.stability = 50
        self.dream_score = 0

        self.elements = {
            "floating_island": DreamElement(
                "Floating Island", 20, 15
            ),
            "moon_river": DreamElement(
                "Moon River", 15, 10
            ),
            "glass_forest": DreamElement(
                "Glass Forest", 25, -5
            ),
            "endless_stairs": DreamElement(
                "Endless Stairs", 10, -10
            ),
            "golden_city": DreamElement(
                "Golden City", 30, 20
            ),
        }

        self.world = []
        self.log = []

    def add_element(self, element_name):
        if element_name not in self.elements:
            return False

        element = self.elements[element_name]

        if self.energy < element.energy_cost:
            self.log.append("The dream has insufficient energy.")
            return False

        self.energy -= element.energy_cost
        self.stability += element.stability
        self.world.append(element.name)

        self.dream_score += (
            20 + max(0, element.stability)
        )

        return True

    def remove_element(self, element_name):
        if element_name not in self.world:
            return False

        element = self.elements[
            next(
                key
                for key, value in self.elements.items()
                if value.name == element_name
            )
        ]

        self.world.remove(element_name)
        self.energy = min(100, self.energy + element.energy_cost)
        self.stability -= element.stability
        self.dream_score = max(
            0,
            self.dream_score - 20,
        )
        return True

    def stabilize(self):
        self.energy = max(0, self.energy - 10)
        self.stability += 15

    def dream_state(self):
        if self.stability >= 80:
            return "stable"
        if self.stability >= 40:
            return "unstable"
        return "collapsing"

    def status(self):
        return {
            "architect": self.architect,
            "energy": self.energy,
            "stability": self.stability,
            "dream_score": self.dream_score,
            "state": self.dream_state(),
            "world": list(self.world),
        }


def create_game():
    return DreamArchitect()


if __name__ == "__main__":
    game = create_game()
    game.add_element("floating_island")
    game.add_element("moon_river")
    game.add_element("golden_city")
    print(game.status())
