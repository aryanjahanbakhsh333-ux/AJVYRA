from dataclasses import dataclass
from typing import List


@dataclass
class StoryAssignment:
    title: str
    location: str
    rarity: int
    completed: bool = False


class PhotojournalistWorldTour:
    def __init__(self):
        self.journalist = "Noa Vey"
        self.location = "Istanbul"
        self.money = 150
        self.reputation = 0
        self.score = 0
        self.photos = 0
        self.assignments: List[StoryAssignment] = [
            StoryAssignment("Morning Harbor", "Istanbul", 2),
            StoryAssignment("Desert Lights", "Marrakesh", 3),
            StoryAssignment("Mountain Silence", "Almaty", 4),
            StoryAssignment("Midnight Festival", "Tokyo", 5),
        ]

    def travel(self, destination: str):
        destinations = {
            "Istanbul": 0,
            "Marrakesh": 40,
            "Almaty": 55,
            "Tokyo": 80,
        }

        if destination not in destinations:
            return False

        cost = destinations[destination]

        if self.money < cost:
            return False

        self.money -= cost
        self.location = destination
        self.score += 10
        return True

    def photograph(self, assignment_title: str):
        for assignment in self.assignments:
            if assignment.title != assignment_title:
                continue

            if assignment.completed or assignment.location != self.location:
                return False

            assignment.completed = True
            self.photos += 1
            self.reputation += assignment.rarity * 4
            self.score += assignment.rarity * 30
            self.money += assignment.rarity * 20
            return True

        return False

    def sell_photo(self):
        if self.photos <= 0:
            return False

        self.photos -= 1
        self.money += 35
        self.score += 20
        return True

    def portfolio_complete(self):
        return all(a.completed for a in self.assignments)

    def status(self):
        return {
            "journalist": self.journalist,
            "location": self.location,
            "money": self.money,
            "reputation": self.reputation,
            "photos": self.photos,
            "score": self.score,
            "portfolio_complete": self.portfolio_complete(),
        }


def create_game():
    return PhotojournalistWorldTour()


def demo():
    game = create_game()

    game.photograph("Morning Harbor")
    game.travel("Marrakesh")
    game.photograph("Desert Lights")
    game.travel("Almaty")
    game.photograph("Mountain Silence")
    game.travel("Tokyo")
    game.photograph("Midnight Festival")

    return game.status()


if __name__ == "__main__":
    print(demo())
