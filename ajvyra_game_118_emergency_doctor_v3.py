"""
AJVYRA 118 — Emergency Doctor
Genre: Educational Medical Decision Game

Educational simulation only.
No real-world medical diagnosis or treatment guidance.
"""

from dataclasses import dataclass


@dataclass
class PatientCase:
    name: str
    symptoms: tuple[str, ...]
    correct_priority: str
    stabilized: bool = False


class EmergencyDoctor:
    title = "Emergency Doctor"
    doctor = "Dr. Elara Quinn"

    def __init__(self):
        self.score = 0
        self.reputation = 50
        self.cases = [
            PatientCase(
                "Case A",
                ("confusion", "weakness"),
                "urgent_assessment",
            ),
            PatientCase(
                "Case B",
                ("minor_cut", "stable"),
                "basic_assessment",
            ),
            PatientCase(
                "Case C",
                ("breathing_difficulty", "distress"),
                "urgent_assessment",
            ),
            PatientCase(
                "Case D",
                ("mild_headache", "stable"),
                "basic_assessment",
            ),
        ]
        self.completed = []

    def assess(self, index, priority):
        if not 0 <= index < len(self.cases):
            return False

        case = self.cases[index]

        if case.stabilized:
            return False

        if priority == case.correct_priority:
            case.stabilized = True
            self.score += 100
            self.reputation += 5
            self.completed.append(case.name)
            return True

        self.score = max(0, self.score - 20)
        self.reputation = max(0, self.reputation - 5)
        return False

    def remaining_cases(self):
        return [
            {
                "name": c.name,
                "symptoms": c.symptoms,
                "completed": c.stabilized,
            }
            for c in self.cases
            if not c.stabilized
        ]

    def status(self):
        return {
            "doctor": self.doctor,
            "score": self.score,
            "reputation": self.reputation,
            "completed": list(self.completed),
            "remaining": self.remaining_cases(),
        }


def create_game():
    return EmergencyDoctor()


if __name__ == "__main__":
    game = create_game()
    game.assess(0, "urgent_assessment")
    print(game.status())
