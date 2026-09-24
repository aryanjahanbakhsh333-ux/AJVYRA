import random


class CyberPuzzleGame:
    GAME_ID = "AJVYRA-092"
    TITLE = "Neon Cipher"
    GENRE = "Cyber Puzzle"

    def __init__(self):
        self.player = "Zero Kade"
        self.level = 1
        self.security = 100
        self.score = 0
        self.code = self._generate_code()

    def _generate_code(self):
        return random.randint(1000, 9999)

    def attempt(self, guess: int):
        if self.security <= 0:
            return "LOCKED"

        if guess == self.code:
            self.score += self.security * 2
            self.level += 1
            self.security = min(100, self.security + 20)
            self.code = self._generate_code()

            return "CRACKED"

        self.security -= 10

        if guess < self.code:
            return "HIGHER"

        return "LOWER"

    def use_hint(self):
        if self.security < 20:
            return None

        self.security -= 20

        return {
            "last_digit": self.code % 10,
            "range": (
                self.code // 1000,
                self.code // 1000 + 1,
            ),
        }

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "player": self.player,
            "level": self.level,
            "security": self.security,
            "score": self.score,
        }
