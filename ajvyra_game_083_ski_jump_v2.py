import math


class SkiJumpGame:
    GAME_ID = "AJVYRA-083"
    TITLE = "Skyline Jump"
    GENRE = "Ski Jumping"

    def __init__(self):
        self.rider = "Eron Vale"
        self.speed = 0
        self.altitude = 0
        self.distance = 0
        self.balance = 100
        self.score = 0

    def launch(self, power: float):
        self.speed = min(120, power * 1.2)
        self.altitude = self.speed * 0.65
        self.distance = self.speed * 1.8

        return self.state()

    def balance_in_air(self, angle: float):
        error = abs(angle)

        self.balance = max(0, self.balance - int(error * 2))

        if self.balance > 70:
            multiplier = 1.4
        elif self.balance > 40:
            multiplier = 1.0
        else:
            multiplier = 0.6

        self.score = int(self.distance * multiplier)

        return self.score

    def land(self):
        if self.balance >= 45:
            self.score += 100
            return "PERFECT_LANDING"

        self.score = max(0, self.score - 50)
        return "ROUGH_LANDING"

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "rider": self.rider,
            "speed": round(self.speed, 2),
            "altitude": round(self.altitude, 2),
            "distance": round(self.distance, 2),
            "balance": self.balance,
            "score": self.score,
        }
