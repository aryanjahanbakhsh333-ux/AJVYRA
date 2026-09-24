"""
AJVYRA Game 104 - Piano Perfect
Genre: Music / Timing
"""

from dataclasses import dataclass


@dataclass
class Note:
    key: str
    beat: float


class PianoPerfect:
    title = "Piano Perfect"
    character = "Elian Noct"

    def __init__(self):
        self.song = [
            Note("C", 1.0),
            Note("E", 2.0),
            Note("G", 3.0),
            Note("B", 4.0),
            Note("G", 5.0),
            Note("E", 6.0),
            Note("C", 7.0),
            Note("D", 8.0),
        ]

        self.index = 0
        self.combo = 0
        self.best_combo = 0
        self.score = 0
        self.misses = 0

    def press_key(self, key, current_beat):
        if self.index >= len(self.song):
            return {"finished": True}

        note = self.song[self.index]

        if key.upper() != note.key:
            self.misses += 1
            self.combo = 0
            return {"hit": False, "reason": "wrong_key"}

        difference = abs(current_beat - note.beat)

        if difference <= 0.18:
            points = 100
            rating = "perfect"
        elif difference <= 0.40:
            points = 60
            rating = "good"
        elif difference <= 0.70:
            points = 25
            rating = "late_early"
        else:
            self.misses += 1
            self.combo = 0
            return {"hit": False, "reason": "timing"}

        self.score += points + self.combo * 5
        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        self.index += 1

        return {
            "hit": True,
            "rating": rating,
            "score": self.score,
            "combo": self.combo,
        }

    def current_note(self):
        if self.index >= len(self.song):
            return None
        return self.song[self.index].key

    def finished(self):
        return self.index >= len(self.song)

    def snapshot(self):
        return {
            "player": self.character,
            "score": self.score,
            "combo": self.combo,
            "best_combo": self.best_combo,
            "misses": self.misses,
            "finished": self.finished(),
            "next_note": self.current_note(),
        }


def create_game():
    return PianoPerfect()


if __name__ == "__main__":
    game = create_game()
    game.press_key("C", 1.0)
    game.press_key("E", 2.0)
    print(game.snapshot())
