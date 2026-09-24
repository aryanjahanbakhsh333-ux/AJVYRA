import random


class MemoryDimensionGame:
    GAME_ID = "AJVYRA-100"
    TITLE = "Echoes of Memory"
    GENRE = "Memory Puzzle Adventure"

    def __init__(self):
        self.hero = "Eli Vey"
        self.level = 1
        self.score = 0
        self.lives = 3

        self.sequence = []
        self.player_sequence = []

        self.generate_sequence()

    def generate_sequence(self):
        symbols = [
            "moon",
            "star",
            "fox",
            "key",
            "eye",
            "wave",
        ]

        self.sequence = random.sample(
            symbols,
            min(3 + self.level, len(symbols))
        )

        self.player_sequence = []

    def remember(self, symbol: str):
        if self.lives <= 0:
            return False

        self.player_sequence.append(symbol)

        index = len(self.player_sequence) - 1

        if self.player_sequence[index] != self.sequence[index]:
            self.lives -= 1
            self.player_sequence = []
            return False

        if len(self.player_sequence) == len(self.sequence):
            self.score += self.level * 100
            self.level += 1
            self.generate_sequence()
            return True

        return None

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "hero": self.hero,
            "level": self.level,
            "score": self.score,
            "lives": self.lives,
            "sequence_length": len(self.sequence),
        }
