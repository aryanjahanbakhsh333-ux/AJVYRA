from dataclasses import dataclass


@dataclass
class Passenger:
    name: str
    clue: str
    suspicious: int
    questioned: bool = False


class MysteryTrainDetective:
    def __init__(self):
        self.detective = "Rian Cross"
        self.carriage = 1
        self.time_left = 12
        self.clues = 0
        self.score = 0
        self.case_solved = False
        self.accusation = None

        self.passengers = [
            Passenger("Mira Lane", "silver watch", 20),
            Passenger("Jon Vale", "old ticket", 35),
            Passenger("Elia Stone", "coded letter", 60),
            Passenger("Corin Ash", "missing key", 90),
        ]

    def move_carriage(self):
        if self.time_left <= 0:
            return False

        self.carriage += 1
        self.time_left -= 1
        self.score += 10
        return True

    def question_passenger(self, index: int):
        if not 0 <= index < len(self.passengers):
            return False

        passenger = self.passengers[index]

        if passenger.questioned or self.time_left <= 0:
            return False

        passenger.questioned = True
        self.time_left -= 1
        self.clues += 1
        self.score += passenger.suspicious
        return passenger.clue

    def inspect_luggage(self):
        if self.time_left <= 0:
            return False

        self.time_left -= 1
        self.clues += 1
        self.score += 40
        return True

    def connect_clues(self):
        if self.clues < 3:
            return False

        self.score += 100
        return True

    def accuse(self, index: int):
        if not 0 <= index < len(self.passengers):
            return False

        if self.clues < 4:
            return False

        self.accusation = self.passengers[index].name

        if self.passengers[index].suspicious >= 80:
            self.case_solved = True
            self.score += 300
            return True

        self.score -= 100
        return False

    def status(self):
        return {
            "detective": self.detective,
            "carriage": self.carriage,
            "time_left": self.time_left,
            "clues": self.clues,
            "score": self.score,
            "accusation": self.accusation,
            "case_solved": self.case_solved,
        }


def create_game():
    return MysteryTrainDetective()


if __name__ == "__main__":
    game = create_game()
    game.question_passenger(0)
    game.question_passenger(2)
    game.inspect_luggage()
    print(game.status())
