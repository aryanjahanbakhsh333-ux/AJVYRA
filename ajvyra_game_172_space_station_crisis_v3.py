"""
AJVYRA 172 — Space Station Crisis
Genre: Sci-Fi / Strategy / Emergency
"""

from dataclasses import dataclass


@dataclass
class StationSystem:
    name: str
    health: int
    critical: bool = False


class SpaceStationCrisis:
    title = "Space Station Crisis"
    engineer = "Vera Quill"

    def __init__(self):
        self.oxygen = 100
        self.energy = 100
        self.crew = 12
        self.score = 0
        self.turn = 1

        self.systems = [
            StationSystem("Life Support", 80),
            StationSystem("Reactor", 65),
            StationSystem("Navigation", 75),
            StationSystem("Communications", 55),
        ]

    def repair(self, system_name):
        system = self._find(system_name)

        if system is None or self.energy < 15:
            return False

        self.energy -= 15
        system.health = min(
            100,
            system.health + 20,
        )
        system.critical = system.health < 30
        self.score += 120
        return True

    def reroute_power(self):
        if self.energy < 25:
            return False

        self.energy -= 25

        for system in self.systems:
            system.health = min(
                100,
                system.health + 5,
            )

        self.score += 150
        return True

    def stabilize_oxygen(self):
        if self.energy < 20:
            return False

        self.energy -= 20
        self.oxygen = min(
            100,
            self.oxygen + 25,
        )
        self.score += 100
        return True

    def next_turn(self):
        self.turn += 1
        self.oxygen = max(
            0,
            self.oxygen - 5,
        )

        self.energy = max(
            0,
            self.energy - 4,
        )

        for system in self.systems:
            if system.health < 50:
                system.health = max(
                    0,
                    system.health - 5,
                )

    def crisis_resolved(self):
        return (
            self.oxygen >= 70
            and all(
                system.health >= 70
                for system in self.systems
            )
        )

    def _find(self, name):
        return next(
            (
                s for s in self.systems
                if s.name == name
            ),
            None,
        )

    def status(self):
        return {
            "engineer": self.engineer,
            "turn": self.turn,
            "oxygen": self.oxygen,
            "energy": self.energy,
            "crew": self.crew,
            "score": self.score,
            "resolved": self.crisis_resolved(),
        }


def create_game():
    return SpaceStationCrisis()


if __name__ == "__main__":
    game = create_game()
    game.repair("Reactor")
    game.stabilize_oxygen()
    print(game.status())
