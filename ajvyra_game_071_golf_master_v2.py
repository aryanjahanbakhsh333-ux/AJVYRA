from dataclasses import dataclass
import math


@dataclass
class GolfHole:
    number: int
    par: int
    distance: float
    wind: float


class GolfMasterGame:
    GAME_ID = "AJVYRA-071"
    TITLE = "Silent Greens"
    GENRE = "Golf Simulation"

    def __init__(self):
        self.player = "Kael Veyron"
        self.strokes = 0
        self.hole_index = 0
        self.score = 0

        self.holes = [
            GolfHole(1, 3, 120, 1.2),
            GolfHole(2, 4, 210, -2.1),
            GolfHole(3, 5, 390, 3.0),
            GolfHole(4, 3, 145, -1.4),
            GolfHole(5, 4, 250, 0.8),
        ]

    def hit(self, power: float, angle: float):
        if self.hole_index >= len(self.holes):
            return False

        hole = self.holes[self.hole_index]

        effective_power = power - abs(hole.wind * 4)
        distance_error = abs(effective_power - hole.distance)
        angle_error = abs(angle + hole.wind)

        strokes = 1

        if distance_error > 80:
            strokes += 2
        elif distance_error > 35:
            strokes += 1

        if angle_error > 12:
            strokes += 1

        self.strokes += strokes
        self.hole_index += 1

        self.score += hole.par - strokes
        return strokes

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "player": self.player,
            "hole": self.hole_index + 1,
            "strokes": self.strokes,
            "score": self.score,
            "finished": self.hole_index >= len(self.holes),
        }
