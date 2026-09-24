from dataclasses import dataclass


@dataclass
class Module:
    name: str
    power: int
    oxygen: int
    damage: int = 0


class SpaceStationEngineerGame:
    GAME_ID = "AJVYRA-095"
    TITLE = "Station Zero"
    GENRE = "Space Station Engineering"

    def __init__(self):
        self.engineer = "Vey Korr"
        self.energy = 500
        self.oxygen = 100
        self.crew = 8

        self.modules = [
            Module("Command", 100, 20),
            Module("Habitat", 80, 50),
            Module("Laboratory", 120, 10),
            Module("Reactor", 200, 0),
        ]

    def repair(self, index: int):
        if index < 0 or index >= len(self.modules):
            return False

        module = self.modules[index]

        if module.damage <= 0 or self.energy < 30:
            return False

        self.energy -= 30
        module.damage = max(0, module.damage - 25)

        return True

    def stabilize(self):
        total_damage = sum(m.damage for m in self.modules)

        if total_damage > 100:
            self.oxygen = max(0, self.oxygen - 10)
            self.energy = max(0, self.energy - 40)
        else:
            self.oxygen = min(100, self.oxygen + 5)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "engineer": self.engineer,
            "energy": self.energy,
            "oxygen": self.oxygen,
            "crew": self.crew,
            "modules": [m.__dict__.copy() for m in self.modules],
        }
