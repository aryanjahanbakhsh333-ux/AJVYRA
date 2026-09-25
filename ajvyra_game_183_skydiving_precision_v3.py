from dataclasses import dataclass


@dataclass
class Skydiver:
    name: str
    altitude: int = 4000
    stability: int = 100
    accuracy: int = 50
    style: int = 0
    score: int = 0


class SkydivingPrecision:
    def __init__(self):
        self.player = Skydiver("Kai Arven")
        self.wind = 12
        self.target_distance = 500
        self.landed = False

    def stabilize(self):
        self.player.stability = min(100, self.player.stability + 15)
        self.player.score += 10

    def adjust_course(self, direction: str):
        if direction not in ("left", "right", "center"):
            return False

        if direction == "center":
            self.player.accuracy += 12
        else:
            self.player.accuracy += 6

        self.player.stability -= 4
        self.player.altitude -= 300
        self.player.score += 8

        return True

    def perform_trick(self, difficulty: int):
        if difficulty < 1 or difficulty > 5:
            return False

        self.player.style += difficulty * 5
        self.player.stability -= difficulty * 7
        self.player.altitude -= 500
        self.player.score += difficulty * 15

        return self.player.stability > 0

    def deploy_parachute(self):
        if self.player.altitude > 1200:
            return False

        self.player.altitude = 0
        self.landed = True

        landing_bonus = max(0, 100 - self.target_distance // 10)
        self.player.score += landing_bonus

        return True

    def status(self):
        return {
            "name": self.player.name,
            "altitude": self.player.altitude,
            "stability": self.player.stability,
            "accuracy": self.player.accuracy,
            "style": self.player.style,
            "score": self.player.score,
            "landed": self.landed,
        }


def create_game():
    return SkydivingPrecision()


def demo():
    game = create_game()
    game.adjust_course("center")
    game.perform_trick(2)
    game.stabilize()
    game.player.altitude = 1000
    game.deploy_parachute()
    return game.status()


if __name__ == "__main__":
    print(demo())
