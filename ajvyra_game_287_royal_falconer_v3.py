from dataclasses import dataclass


@dataclass
class Falcon:
    name: str
    speed: int = 70
    focus: int = 70
    bond: int = 40
    stamina: int = 100


class RoyalFalconer:
    def __init__(self):
        self.falconer = "Aren Vale"
        self.falcon = Falcon("Silverwing")
        self.food = 40
        self.training = 0
        self.score = 0
        self.reputation = 20
        self.completed_trials = 0

    def train_speed(self):
        if self.food < 3 or self.falcon.stamina < 10:
            return False

        self.food -= 3
        self.falcon.stamina -= 10
        self.falcon.speed += 4
        self.training += 1
        self.score += 35
        return True

    def train_focus(self):
        if self.food < 3 or self.falcon.stamina < 8:
            return False

        self.food -= 3
        self.falcon.stamina -= 8
        self.falcon.focus += 5
        self.training += 1
        self.score += 40
        return True

    def bond_with_falcon(self):
        self.falcon.bond = min(
            100,
            self.falcon.bond + 12
        )
        self.score += 30
        return True

    def royal_trial(self):
        if self.falcon.stamina < 20:
            return False

        self.falcon.stamina -= 20

        power = (
            self.falcon.speed
            + self.falcon.focus
            + self.falcon.bond
        )

        if power >= 220:
            self.completed_trials += 1
            self.reputation += 8
            self.score += 180
            return True

        self.score += 20
        return False

    def rest(self):
        self.falcon.stamina = min(
            100,
            self.falcon.stamina + 35
        )
        self.food += 5

    def status(self):
        return {
            "falconer": self.falconer,
            "falcon": self.falcon.name,
            "speed": self.falcon.speed,
            "focus": self.falcon.focus,
            "bond": self.falcon.bond,
            "stamina": self.falcon.stamina,
            "food": self.food,
            "training": self.training,
            "trials": self.completed_trials,
            "reputation": self.reputation,
            "score": self.score,
        }


def create_game():
    return RoyalFalconer()


if __name__ == "__main__":
    game = create_game()
    game.train_speed()
    game.train_focus()
    game.bond_with_falcon()
    game.royal_trial()
    print(game.status())
