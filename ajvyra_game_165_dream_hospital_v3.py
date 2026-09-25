"""
AJVYRA 165 — Dream Hospital
Genre: Fantasy / Puzzle Management
"""

from dataclasses import dataclass


@dataclass
class DreamPatient:
    name: str
    fear: int
    hope: int
    memory: int
    recovered: bool = False


class DreamHospital:
    title = "Dream Hospital"
    doctor_name = "Luna Aris"

    def __init__(self):
        self.energy = 100
        self.stars = 50
        self.score = 0

        self.patients = [
            DreamPatient("Eli", 70, 30, 45),
            DreamPatient("Nora", 55, 45, 65),
            DreamPatient("Soren", 80, 20, 35),
            DreamPatient("Mika", 40, 60, 75),
        ]

    def calm(self, name):
        patient = self._find(name)

        if patient is None or self.energy < 10:
            return False

        self.energy -= 10
        patient.fear = max(
            0,
            patient.fear - 15,
        )
        patient.hope = min(
            100,
            patient.hope + 8,
        )

        self.score += 80
        return True

    def restore_memory(self, name):
        patient = self._find(name)

        if patient is None or self.energy < 20:
            return False

        self.energy -= 20
        patient.memory = min(
            100,
            patient.memory + 20,
        )

        self.score += 150
        return True

    def awaken(self, name):
        patient = self._find(name)

        if patient is None:
            return False

        ready = (
            patient.fear <= 35
            and patient.hope >= 60
            and patient.memory >= 70
        )

        if not ready:
            return False

        patient.recovered = True
        self.stars += 100
        self.score += 500
        return True

    def rest(self):
        self.energy = min(
            100,
            self.energy + 35,
        )

    def _find(self, name):
        return next(
            (
                p for p in self.patients
                if p.name.lower() == name.lower()
            ),
            None,
        )

    def status(self):
        return {
            "doctor": self.doctor_name,
            "energy": self.energy,
            "stars": self.stars,
            "score": self.score,
            "recovered": [
                p.name
                for p in self.patients
                if p.recovered
            ],
        }


def create_game():
    return DreamHospital()


if __name__ == "__main__":
    game = create_game()
    game.calm("Eli")
    game.restore_memory("Eli")
    game.calm("Eli")
    game.awaken("Eli")
    print(game.status())
