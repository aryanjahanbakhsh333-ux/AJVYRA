"""
AJVYRA 112 — Undercover Detective
Genre: Investigation / Interactive Mystery
"""

from dataclasses import dataclass


@dataclass
class Suspect:
    name: str
    statement: str
    clue: str
    suspicion: int = 0


class UndercoverDetective:
    title = "Undercover Detective"
    detective = "Vera Knox"

    def __init__(self):
        self.suspects = [
            Suspect(
                "Darian",
                "I never entered the archive.",
                "muddy_bootprint",
            ),
            Suspect(
                "Mika",
                "I was repairing the lights.",
                "broken_wire",
            ),
            Suspect(
                "Jonas",
                "I left before midnight.",
                "train_ticket",
            ),
            Suspect(
                "Selene",
                "I was at the cafe.",
                "receipt",
            ),
        ]

        self.collected_clues: set[str] = set()
        self.trust = 50
        self.case_progress = 0
        self.accusation = None
        self.log = []

    def inspect_scene(self):
        clues = {
            "muddy_bootprint",
            "broken_wire",
            "train_ticket",
            "receipt",
        }

        self.collected_clues.update(clues)
        self.case_progress += 20
        self.log.append("The crime scene was inspected.")

    def question(self, name: str, question_type: str):
        suspect = next(
            (s for s in self.suspects if s.name.lower() == name.lower()),
            None,
        )

        if suspect is None:
            return False

        if question_type == "evidence":
            if suspect.clue in self.collected_clues:
                suspect.suspicion += 10
                self.case_progress += 10
            else:
                self.trust -= 5

        elif question_type == "pressure":
            suspect.suspicion += 5
            self.trust -= 2

        elif question_type == "friendly":
            self.trust += 5

        self.log.append(
            f"{suspect.name} was questioned using {question_type}."
        )
        return True

    def accuse(self, name: str):
        suspect = next(
            (s for s in self.suspects if s.name.lower() == name.lower()),
            None,
        )

        if suspect is None:
            return False

        if suspect.suspicion >= 20 and self.case_progress >= 50:
            self.accusation = suspect.name
            self.case_progress = 100
            self.log.append(f"Case solved: {suspect.name}.")
            return True

        self.trust -= 15
        self.log.append("Insufficient evidence.")
        return False

    def status(self):
        return {
            "detective": self.detective,
            "progress": self.case_progress,
            "trust": self.trust,
            "clues": list(self.collected_clues),
            "suspects": {
                s.name: s.suspicion for s in self.suspects
            },
            "accusation": self.accusation,
        }


def create_game():
    return UndercoverDetective()


if __name__ == "__main__":
    game = create_game()
    game.inspect_scene()
    game.question("Darian", "evidence")
    print(game.status())
