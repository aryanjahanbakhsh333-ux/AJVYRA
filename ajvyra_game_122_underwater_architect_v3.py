"""
AJVYRA 122 — Underwater Architect
Genre: Construction / Resource Management
"""

from dataclasses import dataclass


@dataclass
class Module:
    name: str
    oxygen: int
    energy: int
    durability: int
    cost: int


class UnderwaterArchitect:
    title = "Underwater Architect"
    architect = "Nera Voss"

    def __init__(self):
        self.money = 1500
        self.oxygen = 100
        self.energy = 80
        self.pressure = 20
        self.score = 0
        self.modules = []

        self.available = {
            "habitat": Module(
                "Habitat", 25, 10, 80, 300
            ),
            "reactor": Module(
                "Reactor", 0, 35, 70, 400
            ),
            "greenhouse": Module(
                "Greenhouse", 30, 5, 60, 350
            ),
            "laboratory": Module(
                "Laboratory", 10, 15, 65, 450
            ),
        }

    def build(self, module_name):
        if module_name not in self.available:
            return False

        module = self.available[module_name]

        if self.money < module.cost:
            return False

        self.money -= module.cost
        self.modules.append(module)
        self.oxygen += module.oxygen
        self.energy += module.energy
        self.score += 100
        return True

    def reinforce(self):
        if self.money < 150:
            return False

        self.money -= 150
        self.pressure = max(0, self.pressure - 10)
        self.score += 25
        return True

    def simulate_day(self):
        oxygen_use = max(1, len(self.modules) * 3)
        self.oxygen = max(0, self.oxygen - oxygen_use)

        self.energy = max(
            0,
            self.energy - len(self.modules),
        )

        self.pressure += 3

        if self.pressure > 80:
            self.score = max(0, self.score - 50)

    def stable(self):
        return (
            self.oxygen > 20
            and self.energy > 10
            and self.pressure < 70
        )

    def status(self):
        return {
            "architect": self.architect,
            "money": self.money,
            "oxygen": self.oxygen,
            "energy": self.energy,
            "pressure": self.pressure,
            "modules": [m.name for m in self.modules],
            "score": self.score,
            "stable": self.stable(),
        }


def create_game():
    return UnderwaterArchitect()


if __name__ == "__main__":
    game = create_game()
    game.build("habitat")
    game.build("reactor")
    game.build("greenhouse")
    game.simulate_day()
    print(game.status())
