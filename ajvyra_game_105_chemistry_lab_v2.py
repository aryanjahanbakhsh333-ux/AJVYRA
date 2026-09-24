"""
AJVYRA Game 105 - Chemistry Lab
Genre: Educational Puzzle
"""

from dataclasses import dataclass


@dataclass
class Experiment:
    name: str
    target: str
    ingredients: tuple[str, ...]
    solved: bool = False


class ChemistryLab:
    title = "Chemistry Lab"
    character = "Dr. Luma"

    def __init__(self):
        self.score = 0
        self.experiments = [
            Experiment(
                "Water Formation",
                "H2O",
                ("H", "H", "O"),
            ),
            Experiment(
                "Carbon Dioxide",
                "CO2",
                ("C", "O", "O"),
            ),
            Experiment(
                "Oxygen Molecule",
                "O2",
                ("O", "O"),
            ),
        ]
        self.log = []

    @staticmethod
    def normalize(items):
        return tuple(sorted(items))

    def solve(self, experiment_index, ingredients):
        if not 0 <= experiment_index < len(self.experiments):
            return False

        experiment = self.experiments[experiment_index]

        if self.normalize(ingredients) == self.normalize(
            experiment.ingredients
        ):
            experiment.solved = True
            self.score += 100
            self.log.append(
                f"{experiment.name} solved: {experiment.target}."
            )
            return True

        self.score = max(0, self.score - 10)
        self.log.append("The selected atoms do not match.")
        return False

    def available_experiments(self):
        return [
            {
                "name": e.name,
                "target": e.target,
                "solved": e.solved,
            }
            for e in self.experiments
        ]

    def snapshot(self):
        return {
            "scientist": self.character,
            "score": self.score,
            "experiments": self.available_experiments(),
        }


def create_game():
    return ChemistryLab()


if __name__ == "__main__":
    game = create_game()
    game.solve(0, ["H", "H", "O"])
    print(game.snapshot())
