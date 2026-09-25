"""
AJVYRA 128 — Museum Heist
Genre: Stealth Puzzle
"""

from dataclasses import dataclass


@dataclass
class SecuritySystem:
    name: str
    difficulty: int
    disabled: bool = False


class MuseumHeist:
    title = "Museum Heist"
    infiltrator = "Nox Reed"

    def __init__(self):
        self.alert = 0
        self.time = 60
        self.score = 0
        self.vault_open = False
        self.artifact_taken = False

        self.systems = [
            SecuritySystem("Laser Grid", 30),
            SecuritySystem("Camera Network", 25),
            SecuritySystem("Motion Sensors", 35),
            SecuritySystem("Vault Lock", 45),
        ]

    def disable(self, name, skill):
        system = next(
            (
                item for item in self.systems
                if item.name.lower() == name.lower()
            ),
            None,
        )

        if system is None or system.disabled:
            return False

        self.time -= system.difficulty // 5

        if skill >= system.difficulty:
            system.disabled = True
            self.score += 50
            return True

        self.alert += 20
        return False

    def open_vault(self):
        vault = next(
            s for s in self.systems
            if s.name == "Vault Lock"
        )

        if not vault.disabled:
            self.alert += 25
            return False

        self.vault_open = True
        self.score += 100
        return True

    def take_artifact(self):
        if not self.vault_open or self.artifact_taken:
            return False

        if self.alert >= 100:
            return False

        self.artifact_taken = True
        self.score += 250
        return True

    def escape(self):
        return self.artifact_taken and self.alert < 100

    def status(self):
        return {
            "infiltrator": self.infiltrator,
            "time": self.time,
            "alert": self.alert,
            "score": self.score,
            "vault_open": self.vault_open,
            "artifact_taken": self.artifact_taken,
            "escaped": self.escape(),
            "systems": {
                s.name: s.disabled
                for s in self.systems
            },
        }


def create_game():
    return MuseumHeist()


if __name__ == "__main__":
    game = create_game()

    for system in (
        "Laser Grid",
        "Camera Network",
        "Motion Sensors",
        "Vault Lock",
    ):
        game.disable(system, 100)

    game.open_vault()
    game.take_artifact()
    print(game.status())
