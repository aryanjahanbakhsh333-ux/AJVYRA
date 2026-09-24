from dataclasses import dataclass
import math


@dataclass
class Target:
    distance: float
    wind: float
    score_zone: int


class ArcheryChallengeGame:
    GAME_ID = "AJVYRA-066"
    TITLE = "Arrow of Dawn"
    GENRE = "Archery Precision"

    def __init__(self):
        self.arrows = 12
        self.score = 0
        self.combo = 0

        self.targets = [
            Target(20, 1.2, 10),
            Target(30, -0.8, 10),
            Target(40, 2.4, 10),
            Target(50, -1.5, 10),
        ]

    def shoot(self, target_index: int, angle: float, power: float):
        if self.arrows <= 0:
            return 0

        if target_index < 0 or target_index >= len(self.targets):
            return 0

        target = self.targets[target_index]
        self.arrows -= 1

        effective_angle = angle + target.wind
        trajectory_error = abs(math.sin(math.radians(effective_angle))) * 20

        distance_error = abs(power - target.distance) * 0.8
        error = trajectory_error + distance_error

        if error < 3:
            points = 50
        elif error < 7:
            points = 30
        elif error < 14:
            points = 15
        else:
            points = 0

        if points:
            self.combo += 1
            points += self.combo * 2
        else:
            self.combo = 0

        self.score += points
        return points

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "arrows": self.arrows,
            "score": self.score,
            "combo": self.combo,
        }
