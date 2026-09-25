from dataclasses import dataclass


@dataclass
class TrainClue:
    name: str
    location: str
    value: int
    discovered: bool = False


class HauntedTrainMystery:
    def __init__(self):
        self.detective = "Mira Solen"
        self.carriage = 1
        self.time_left = 20
        self.sanity = 100
        self.evidence = 0
        self.score = 0
        self.clues = [
            TrainClue("Broken Pocket Watch", "Carriage 2", 15),
            TrainClue("Black Ticket", "Carriage 4", 20),
            TrainClue("Old Photograph", "Carriage 6", 25),
            TrainClue("Silver Key", "Carriage 8", 30),
        ]

    def move(self, carriage: int):
        if carriage < 1 or carriage > 10:
            return False

        distance = abs(carriage - self.carriage)
        self.time_left -= distance
        self.carriage = carriage
        self.sanity -= distance // 3

        return self.time_left > 0

    def investigate(self):
        found = []

        for clue in self.clues:
            if clue.location == f"Carriage {self.carriage}" and not clue.discovered:
                clue.discovered = True
                self.evidence += clue.value
                self.score += clue.value
                found.append(clue.name)

        if not found:
            self.time_left -= 1
            self.sanity -= 2

        return found

    def inspect_train_window(self):
        self.time_left -= 1

        if self.carriage in (3, 7, 9):
            self.sanity -= 5
            return "A strange reflection appeared."

        return "Only darkness outside."

    def solve_mystery(self):
        discovered = sum(clue.discovered for clue in self.clues)

        if discovered == len(self.clues) and self.evidence >= 80:
            self.score += 100
            return True, "The mystery of the midnight train is solved."

        return False, "More evidence is required."

    def status(self):
        return {
            "detective": self.detective,
            "carriage": self.carriage,
            "time_left": self.time_left,
            "sanity": max(0, self.sanity),
            "evidence": self.evidence,
            "score": self.score,
            "clues_found": sum(c.discovered for c in self.clues),
        }


def create_game():
    return HauntedTrainMystery()


def demo():
    game = create_game()
    game.move(2)
    game.investigate()
    game.move(4)
    game.investigate()
    return game.status()


if __name__ == "__main__":
    print(demo())
