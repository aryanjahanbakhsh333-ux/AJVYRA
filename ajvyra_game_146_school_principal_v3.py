"""
AJVYRA 146 — School Principal
Genre: Educational Management
"""

from dataclasses import dataclass


@dataclass
class Student:
    name: str
    learning: int
    happiness: int
    attendance: int


class SchoolPrincipal:
    title = "School Principal"
    principal = "Mira Dawn"

    def __init__(self):
        self.budget = 5000
        self.day = 1
        self.reputation = 50

        self.students = [
            Student("Lio", 65, 75, 90),
            Student("Nia", 80, 68, 95),
            Student("Ren", 55, 88, 82),
            Student("Aya", 72, 80, 91),
        ]

    def lesson(self, student_name):
        student = self._find(student_name)

        if student is None:
            return False

        student.learning = min(
            100,
            student.learning + 6,
        )
        student.happiness = max(
            0,
            student.happiness - 2,
        )
        return True

    def activity(self):
        if self.budget < 200:
            return False

        self.budget -= 200

        for student in self.students:
            student.happiness = min(
                100,
                student.happiness + 8,
            )

        self.reputation += 3
        return True

    def upgrade_classroom(self):
        if self.budget < 700:
            return False

        self.budget -= 700

        for student in self.students:
            student.learning = min(
                100,
                student.learning + 4,
            )

        self.reputation += 5
        return True

    def next_day(self):
        self.day += 1

        self.budget += 100

        for student in self.students:
            student.attendance = min(
                100,
                student.attendance + 1,
            )

    def _find(self, name):
        return next(
            (
                s for s in self.students
                if s.name.lower() == name.lower()
            ),
            None,
        )

    def average_learning(self):
        return round(
            sum(s.learning for s in self.students)
            / len(self.students),
            2,
        )

    def status(self):
        return {
            "principal": self.principal,
            "day": self.day,
            "budget": self.budget,
            "reputation": self.reputation,
            "average_learning": self.average_learning(),
        }


def create_game():
    return SchoolPrincipal()


if __name__ == "__main__":
    game = create_game()
    game.lesson("Lio")
    game.activity()
    game.upgrade_classroom()
    game.next_day()
    print(game.status())
