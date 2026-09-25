from dataclasses import dataclass


@dataclass
class Climber:
    name: str
    grip: int = 70
    stamina: int = 100
    balance: int = 65
    rope_strength: int = 80


class CanyonClimber:
    def __init__(self):
        self.climber = Climber("Kian Rock")
        self.height = 0
        self.goal = 1800
        self.weather = "clear"
        self.score = 0
        self.checkpoints = 0
        self.reached_top = False

    def climb(self):
        if self.climber.stamina < 12:
            return False

        self.climber.stamina -= 12

        progress = self.climber.grip + self.climber.balance
        self.height += progress // 3
        self.score += 30
        return True

    def secure_rope(self):
        if self.climber.rope_strength < 30:
            return False

        self.climber.rope_strength -= 10
        self.climber.stamina = min(
            100,
            self.climber.stamina + 15
        )
        self.checkpoints += 1
        self.score += 45
        return True

    def find_ledge(self):
        self.height += 100
        self.climber.stamina = min(
            100,
            self.climber.stamina + 10
        )
        self.score += 55
        return True

    def handle_wind(self):
        if self.weather != "wind":
            return True

        if self.climber.balance < 60:
            self.height = max(0, self.height - 60)
            return False

        self.score += 40
        return True

    def rest(self):
        self.climber.stamina = min(
            100,
            self.climber.stamina + 30
        )

    def change_weather(self, weather: str):
        if weather not in {"clear", "wind", "fog"}:
            return False

        self.weather = weather
        return True

    def reach_top(self):
        if self.height < self.goal:
            return False

        self.reached_top = True
        self.score += 500
        return True

    def status(self):
        return {
            "climber": self.climber.name,
            "height": self.height,
            "goal": self.goal,
            "weather": self.weather,
            "stamina": self.climber.stamina,
            "grip": self.climber.grip,
            "balance": self.climber.balance,
            "rope": self.climber.rope_strength,
            "checkpoints": self.checkpoints,
            "score": self.score,
            "reached_top": self.reached_top,
        }


def create_game():
    return CanyonClimber()


if __name__ == "__main__":
    game = create_game()
    game.climb()
    game.secure_rope()
    game.find_ledge()
    print(game.status())
