"""
AJVYRA 168 — Forest Guardian
Genre: Adventure / Nature
"""

from dataclasses import dataclass


@dataclass
class ForestZone:
    name: str
    health: int
    wildlife: int
    danger: int
    protected: bool = False


class ForestGuardian:
    title = "Forest Guardian"
    guardian_name = "Eira Moss"

    def __init__(self):
        self.energy = 100
        self.spirit = 60
        self.score = 0

        self.zones = [
            ForestZone("Silver Grove", 70, 80, 15),
            ForestZone("Whisper Valley", 60, 65, 25),
            ForestZone("Ancient Root", 45, 90, 40),
            ForestZone("Shadow Marsh", 35, 55, 60),
        ]

    def restore(self, zone_name):
        zone = self._find(zone_name)

        if zone is None or self.energy < 15:
            return False

        self.energy -= 15
        zone.health = min(
            100,
            zone.health + 15,
        )

        zone.wildlife = min(
            100,
            zone.wildlife + 5,
        )

        self.spirit += 5
        self.score += 100
        return True

    def protect(self, zone_name):
        zone = self._find(zone_name)

        if zone is None or zone.protected:
            return False

        if zone.health < 60:
            return False

        zone.protected = True
        self.score += 250
        self.spirit += 10
        return True

    def communicate_with_wildlife(self, zone_name):
        zone = self._find(zone_name)

        if zone is None or self.energy < 20:
            return False

        self.energy -= 20
        zone.wildlife = min(
            100,
            zone.wildlife + 12,
        )
        self.score += 150
        return True

    def rest(self):
        self.energy = min(
            100,
            self.energy + 30,
        )

    def _find(self, name):
        return next(
            (
                z for z in self.zones
                if z.name == name
            ),
            None,
        )

    def status(self):
        return {
            "guardian": self.guardian_name,
            "energy": self.energy,
            "spirit": self.spirit,
            "score": self.score,
            "protected_zones": [
                z.name
                for z in self.zones
                if z.protected
            ],
        }


def create_game():
    return ForestGuardian()


if __name__ == "__main__":
    game = create_game()
    game.restore("Silver Grove")
    game.communicate_with_wildlife(
        "Silver Grove"
    )
    game.protect("Silver Grove")
    print(game.status())
