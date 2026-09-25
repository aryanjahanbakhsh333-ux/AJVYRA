from dataclasses import dataclass


@dataclass
class Thief:
    name: str
    stealth: int = 70
    agility: int = 65
    focus: int = 60
    reputation: int = 10


class ShadowThiefPuzzle:
    def __init__(self):
        self.thief = Thief("Varyn Shade")
        self.location = "Old Gallery"
        self.alert = 0
        self.time_left = 15
        self.clues = 0
        self.score = 0
        self.artifacts = 0
        self.escaped = False

    def move_silently(self):
        if self.time_left <= 0:
            return False

        self.time_left -= 1

        if self.thief.stealth >= 60:
            self.score += 20
            return True

        self.alert += 10
        return False

    def study_lock(self):
        if self.time_left <= 0 or self.thief.focus < 40:
            return False

        self.time_left -= 2
        self.clues += 1
        self.score += 30
        return True

    def bypass_security(self):
        if self.clues < 2 or self.time_left <= 0:
            return False

        self.time_left -= 2

        if self.thief.focus + self.thief.stealth >= 120:
            self.alert = max(0, self.alert - 15)
            self.score += 80
            return True

        self.alert += 20
        return False

    def collect_artifact(self):
        if self.clues < 3 or self.time_left <= 0:
            return False

        self.time_left -= 2
        self.artifacts += 1
        self.score += 150
        return True

    def escape(self):
        if self.artifacts <= 0 or self.alert >= 80:
            return False

        self.escaped = True
        self.score += 250
        self.thief.reputation += 20
        return True

    def status(self):
        return {
            "thief": self.thief.name,
            "location": self.location,
            "alert": self.alert,
            "time_left": self.time_left,
            "clues": self.clues,
            "artifacts": self.artifacts,
            "reputation": self.thief.reputation,
            "score": self.score,
            "escaped": self.escaped,
        }


def create_game():
    return ShadowThiefPuzzle()


if __name__ == "__main__":
    game = create_game()
    game.move_silently()
    game.study_lock()
    game.study_lock()
    game.bypass_security()
    print(game.status())
