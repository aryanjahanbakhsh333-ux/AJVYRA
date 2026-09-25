"""
AJVYRA 116 — Treasure Map Maker
Genre: Map Creation / Puzzle
"""

from dataclasses import dataclass


@dataclass
class Landmark:
    name: str
    x: int
    y: int


class TreasureMapMaker:
    title = "Treasure Map Maker"
    cartographer = "Orin Vale"

    GRID_SIZE = 10

    def __init__(self):
        self.landmarks = [
            Landmark("Ancient Tree", 2, 3),
            Landmark("Stone Arch", 7, 1),
            Landmark("Blue Lake", 5, 7),
            Landmark("Ruined Tower", 8, 8),
        ]

        self.treasure = (6, 4)
        self.map = []
        self.clues = []
        self.score = 0

    def add_clue(self, landmark_name):
        landmark = next(
            (
                item
                for item in self.landmarks
                if item.name.lower() == landmark_name.lower()
            ),
            None,
        )

        if landmark is None:
            return False

        self.clues.append(
            {
                "landmark": landmark.name,
                "position": (landmark.x, landmark.y),
            }
        )
        self.score += 10
        return True

    def calculate_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve_coordinates(self, x, y):
        distance = self.calculate_distance(
            (x, y),
            self.treasure,
        )

        if distance == 0:
            self.score += 150
            return "treasure_found"

        if distance <= 2:
            self.score += 30
            return "very_close"

        if distance <= 5:
            self.score += 15
            return "near"

        return "far"

    def create_grid(self):
        grid = [
            ["."] * self.GRID_SIZE
            for _ in range(self.GRID_SIZE)
        ]

        for landmark in self.landmarks:
            grid[landmark.y][landmark.x] = "L"

        grid[self.treasure[1]][self.treasure[0]] = "X"
        self.map = grid
        return grid

    def status(self):
        return {
            "cartographer": self.cartographer,
            "score": self.score,
            "clues": list(self.clues),
            "treasure": self.treasure,
            "map": self.create_grid(),
        }


def create_game():
    return TreasureMapMaker()


if __name__ == "__main__":
    game = create_game()
    game.add_clue("Ancient Tree")
    game.add_clue("Blue Lake")
    print(game.solve_coordinates(6, 4))
    print(game.status())
