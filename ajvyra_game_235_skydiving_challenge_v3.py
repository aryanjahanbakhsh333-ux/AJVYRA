from dataclasses import dataclass


@dataclass
class Skydiver:
    name: str
    control: int = 65
    courage: int = 70
    stamina: int = 100
    style: int = 40


class SkydivingChallenge:
    def __init__(self):
        self.diver = Skydiver("Zane Aero")
        self.altitude = 4000
        self.score = 0
        self.coins = 100
        self.combo = 0
        self.landed = False

    def dive(self):
        if self.altitude <= 500 or self.diver.stamina < 15:
            return False

        self.altitude -= 600
        self.diver.stamina -= 15
        self.combo += 1
        self.score += 20 * self.combo
        return True

    def aerial_trick(self):
        if self.altitude < 1000 or self.diver.stamina < 20:
            return False

        self.diver.stamina -= 20

        if self.diver.control >= 55:
            self.diver.style += 5
            self.combo += 1
            self.score += 50 * self.combo
            return True

        self.combo = 0
        return False

    def stabilize(self):
        self.diver.stamina = min(100, self.diver.stamina + 10)
        self.combo = max(0, self.combo - 1)

    def deploy_parachute(self):
        if self.altitude > 900:
            return False

        self.altitude = 0
        self.score += 150
        self.coins += self.score // 50
        self.landed = True
        return True

    def status(self):
        return {
            "diver": self.diver.name,
            "altitude": self.altitude,
            "stamina": self.diver.stamina,
            "style": self.diver.style,
            "combo": self.combo,
            "score": self.score,
            "coins": self.coins,
            "landed": self.landed,
        }


def create_game():
    return SkydivingChallenge()


if __name__ == "__main__":
    game = create_game()
    game.dive()
    game.aerial_trick()
    game.dive()
    game.deploy_parachute()
    print(game.status())
