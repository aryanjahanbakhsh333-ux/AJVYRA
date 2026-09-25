from dataclasses import dataclass


@dataclass
class Skydiver:
    name: str
    control: int = 70
    balance: int = 65
    courage: int = 75
    altitude: int = 4000
    stamina: int = 100


class SkydivingLandingChallenge:
    def __init__(self):
        self.skydiver = Skydiver("Kael Storm")
        self.wind = 45
        self.target_distance = 0
        self.distance = 0
        self.score = 0
        self.combo = 0
        self.landed = False

    def dive(self):
        if self.skydiver.stamina < 8 or self.skydiver.altitude <= 0:
            return False

        self.skydiver.altitude -= 600
        self.skydiver.stamina -= 8
        self.distance += self.wind // 2
        self.score += 20
        return True

    def control_fall(self):
        if self.skydiver.stamina < 10:
            return False

        self.skydiver.stamina -= 10

        if self.skydiver.control >= 65:
            self.wind = max(10, self.wind - 8)
            self.combo += 1
            self.score += 35 * self.combo
            return True

        self.combo = 0
        self.distance += 80
        return False

    def aerial_trick(self):
        if self.skydiver.stamina < 15:
            return False

        self.skydiver.stamina -= 15
        self.combo += 1
        self.score += 60 * self.combo
        return True

    def brake_canopy(self):
        if self.skydiver.altitude > 1800:
            return False

        self.skydiver.altitude = max(
            0,
            self.skydiver.altitude - 200
        )
        self.distance = max(0, self.distance - self.wind)
        self.score += 40
        return True

    def land(self):
        if self.skydiver.altitude > 200:
            return False

        accuracy = abs(self.distance - self.target_distance)

        if accuracy <= 100:
            self.score += 300
            self.landed = True
            return True

        self.score += 50
        self.landed = True
        return False

    def status(self):
        return {
            "skydiver": self.skydiver.name,
            "altitude": self.skydiver.altitude,
            "wind": self.wind,
            "distance": self.distance,
            "score": self.score,
            "combo": self.combo,
            "landed": self.landed,
        }


def create_game():
    return SkydivingLandingChallenge()


if __name__ == "__main__":
    game = create_game()
    game.dive()
    game.control_fall()
    game.aerial_trick()
    print(game.status())
