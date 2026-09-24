import random


class BowlingMasterGame:
    GAME_ID = "AJVYRA-082"
    TITLE = "Ten Pin Night"
    GENRE = "Bowling"

    def __init__(self):
        self.player = "Kiro Vale"
        self.frame = 1
        self.total_score = 0
        self.pins = 10

    def roll(self, power: float, accuracy: float):
        if self.frame > 10:
            return None

        power = max(0, min(100, power))
        accuracy = max(0, min(100, accuracy))

        base = (power * 0.45) + (accuracy * 0.55)
        randomness = random.randint(-2, 2)

        knocked = int(base / 10) + randomness
        knocked = max(0, min(self.pins, knocked))

        self.pins -= knocked
        self.total_score += knocked

        result = {
            "knocked": knocked,
            "remaining": self.pins,
        }

        if self.pins == 0:
            self.total_score += 10
            self.frame += 1
            self.pins = 10
            result["strike_or_clear"] = True

        return result

    def next_frame(self):
        if self.frame <= 10:
            self.frame += 1
            self.pins = 10

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "player": self.player,
            "frame": self.frame,
            "score": self.total_score,
            "pins": self.pins,
        }
