"""
AJVYRA 123 — Time Detective
Genre: Mystery / Time Manipulation
"""

from dataclasses import dataclass


@dataclass
class TimelineEvent:
    year: int
    event: str
    clue: str


class TimeDetective:
    title = "Time Detective"
    detective = "Orion Vale"

    def __init__(self):
        self.current_year = 2042
        self.energy = 100
        self.clues = []
        self.timeline = [
            TimelineEvent(
                1989,
                "The Clockmaker vanished.",
                "silver_key",
            ),
            TimelineEvent(
                2012,
                "A hidden workshop was discovered.",
                "blueprint",
            ),
            TimelineEvent(
                2030,
                "A mysterious clock appeared.",
                "broken_watch",
            ),
            TimelineEvent(
                2042,
                "The city lost twelve minutes.",
                "time_fragment",
            ),
        ]
        self.case_progress = 0
        self.score = 0

    def travel_to(self, year):
        cost = abs(self.current_year - year) // 5 + 5

        if self.energy < cost:
            return False

        self.energy -= cost
        self.current_year = year
        return True

    def investigate(self):
        for event in self.timeline:
            if event.year == self.current_year:
                if event.clue not in self.clues:
                    self.clues.append(event.clue)
                    self.case_progress += 25
                    self.score += 75
                    return event.event

        return None

    def connect_clues(self):
        if len(self.clues) >= 4:
            self.case_progress = 100
            self.score += 300
            return True

        return False

    def restore_energy(self):
        self.energy = min(100, self.energy + 30)

    def status(self):
        return {
            "detective": self.detective,
            "year": self.current_year,
            "energy": self.energy,
            "clues": list(self.clues),
            "progress": self.case_progress,
            "score": self.score,
            "case_solved": self.case_progress >= 100,
        }


def create_game():
    return TimeDetective()


if __name__ == "__main__":
    game = create_game()

    for year in (1989, 2012, 2030, 2042):
        game.travel_to(year)
        game.investigate()

    game.connect_clues()
    print(game.status())
