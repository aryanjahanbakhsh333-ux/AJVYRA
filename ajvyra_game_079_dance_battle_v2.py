import random


class DanceBattleGame:
    GAME_ID = "AJVYRA-079"
    TITLE = "Beat Clash"
    GENRE = "Dance Rhythm Battle"

    def __init__(self):
        self.dancer = "Zeya Ray"
        self.energy = 100
        self.score = 0
        self.combo = 0

        self.moves = [
            "left",
            "right",
            "up",
            "down",
            "spin",
            "jump",
        ]

    def perform(self, move: str, expected: str):
        if self.energy <= 0:
            return False

        self.energy -= 5

        if move == expected:
            self.combo += 1
            points = 20 + self.combo * 5
            self.score += points
            return {
                "success": True,
                "points": points,
            }

        self.combo = 0
        self.score = max(0, self.score - 10)

        return {
            "success": False,
            "points": 0,
        }

    def random_move(self):
        return random.choice(self.moves)

    def recover(self):
        self.energy = min(100, self.energy + 20)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "dancer": self.dancer,
            "energy": self.energy,
            "score": self.score,
            "combo": self.combo,
        }
