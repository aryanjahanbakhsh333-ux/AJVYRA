import math


class MiniGolfArcadeGame:
    GAME_ID = "AJVYRA-073"
    TITLE = "Neon Putt"
    GENRE = "Arcade Mini Golf"

    def __init__(self):
        self.level = 1
        self.score = 0
        self.ball_x = 0.0
        self.ball_y = 0.0
        self.hole_x = 100.0
        self.hole_y = 0.0

    def shoot(self, angle: float, force: float):
        radians = math.radians(angle)

        self.ball_x += math.cos(radians) * force
        self.ball_y += math.sin(radians) * force

        distance = math.sqrt(
            (self.ball_x - self.hole_x) ** 2
            + (self.ball_y - self.hole_y) ** 2
        )

        if distance < 8:
            self.score += max(100 - self.level * 5, 20)
            self.level += 1

            self.ball_x = 0
            self.ball_y = 0

            return "hole_complete"

        return distance

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "level": self.level,
            "score": self.score,
            "ball": [self.ball_x, self.ball_y],
        }
