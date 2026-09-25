from dataclasses import dataclass


@dataclass
class RadioSegment:
    title: str
    audience: int
    difficulty: int
    reputation: int


class UndercoverRadioHost:
    def __init__(self):
        self.host = "Noah Reed"
        self.station = "Night Signal"
        self.audience = 120
        self.reputation = 30
        self.energy = 100
        self.cash = 150
        self.clues = 0
        self.broadcasts = 0
        self.score = 0
        self.segments = [
            RadioSegment("Midnight Stories", 80, 20, 8),
            RadioSegment("City Secrets", 130, 45, 15),
            RadioSegment("Hidden Frequency", 180, 65, 25),
            RadioSegment("Final Signal", 250, 80, 40),
        ]

    def prepare_segment(self, index: int):
        if index < 0 or index >= len(self.segments):
            return False

        if self.energy < 15:
            return False

        self.energy -= 15
        self.score += 10
        return self.segments[index]

    def investigate_signal(self):
        if self.energy < 20:
            return False

        self.energy -= 20
        self.clues += 1
        self.score += 30
        return True

    def broadcast(self, index: int):
        if index < 0 or index >= len(self.segments):
            return False

        segment = self.segments[index]

        if self.energy < segment.difficulty // 2:
            return False

        self.energy -= segment.difficulty // 2
        self.audience += segment.audience // 5
        self.reputation += segment.reputation
        self.cash += segment.audience // 4
        self.score += segment.audience + self.clues * 10
        self.broadcasts += 1

        return True

    def expose_signal(self):
        if self.clues < 3:
            return False

        self.reputation += 50
        self.score += 100
        return True

    def rest(self):
        self.energy = min(100, self.energy + 30)

    def status(self):
        return {
            "host": self.host,
            "station": self.station,
            "audience": self.audience,
            "reputation": self.reputation,
            "energy": self.energy,
            "cash": self.cash,
            "clues": self.clues,
            "broadcasts": self.broadcasts,
            "score": self.score,
        }


def create_game():
    return UndercoverRadioHost()


if __name__ == "__main__":
    game = create_game()
    game.prepare_segment(0)
    game.broadcast(0)
    game.investigate_signal()
    print(game.status())
