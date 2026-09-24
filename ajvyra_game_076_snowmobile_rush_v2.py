import random


class SnowmobileRushGame:
    GAME_ID = "AJVYRA-076"
    TITLE = "Frostline Rush"
    GENRE = "Snowmobile Racing"

    def __init__(self):
        self.rider = "Kiro Ash"
        self.speed = 0
        self.distance = 0
        self.fuel = 100
        self.health = 100
        self.score = 0

    def accelerate(self):
        if self.fuel <= 0 or self.health <= 0:
            return False

        self.speed = min(120, self.speed + 12)
        self.fuel -= 3

        obstacle = random.randint(1, 100)

        if obstacle <= 12:
            self.health -= random.randint(5, 15)
            self.speed = max(0, self.speed - 20)

        self.distance += self.speed // 5
        self.score += self.speed

        return True

    def brake(self):
        self.speed = max(0, self.speed - 20)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "rider": self.rider,
            "speed": self.speed,
            "distance": self.distance,
            "fuel": self.fuel,
            "health": self.health,
            "score": self.score,
        }
